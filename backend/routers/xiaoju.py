"""小橘智能助手 — 三层记忆：角色设定 + 持久记忆 + 最近对话"""
from fastapi import APIRouter, Query
from database import SessionLocal
from models import XiaoJuSession, XiaoJuMessage, XiaoJuMemory
from routers.llm import chat
import json
from datetime import datetime

router = APIRouter(prefix="/api/xiaoju", tags=["小橘助手"])

XIAOJU_SYSTEM = """你是小橘，一个温暖活泼的橘猫学习助手，用户的好伙伴。
你的性格：友善、耐心、偶尔会用"喵~"口癖，但不做作。语气亲切但不啰嗦。

你的角色：
1. 帮助用户理解学习内容，解答知识点疑问
2. 鼓励用户坚持学习，给出学习建议
3. 记录用户的学习偏好和重要信息

回答原则：
- 简洁明了，不废话
- 先回答用户问题，再给建议
- 不知道就说不知道，不编造
- 使用适当的表情符号让对话更生动"""


@router.get("/sessions")
def list_sessions(user_id: int = 1, node_id: int = 0):
    """列出用户的会话列表"""
    db = SessionLocal()
    try:
        q = db.query(XiaoJuSession).filter(XiaoJuSession.user_id == user_id)
        if node_id > 0:
            q = q.filter(XiaoJuSession.node_id == node_id)
        sessions = q.order_by(XiaoJuSession.updated_at.desc()).all()
        return {
            "items": [
                {
                    "id": s.id,
                    "topic": s.topic or "新对话",
                    "node_id": s.node_id,
                    "message_count": s.message_count,
                    "is_archived": s.is_archived,
                    "created_at": s.created_at.strftime("%m-%d %H:%M") if s.created_at else "",
                    "updated_at": s.updated_at.strftime("%m-%d %H:%M") if s.updated_at else "",
                }
                for s in sessions
            ]
        }
    finally:
        db.close()


@router.post("/sessions")
def create_session(user_id: int = 1, node_id: int = 0, topic: str = ""):
    """创建新会话"""
    db = SessionLocal()
    try:
        session = XiaoJuSession(
            user_id=user_id,
            node_id=node_id,
            topic=topic or "新对话",
            message_count=0,
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return {"id": session.id, "topic": session.topic}
    finally:
        db.close()


@router.delete("/sessions/{session_id}")
def delete_session(session_id: int):
    """彻底删除会话及其消息"""
    db = SessionLocal()
    try:
        db.query(XiaoJuMessage).filter(
            XiaoJuMessage.session_id == session_id
        ).delete()
        db.query(XiaoJuSession).filter(
            XiaoJuSession.id == session_id
        ).delete()
        db.commit()
        return {"ok": True}
    finally:
        db.close()


@router.post("/sessions/{session_id}/clear")
def clear_session(session_id: int):
    """清除会话消息（保留会话本身）"""
    db = SessionLocal()
    try:
        session = db.query(XiaoJuSession).filter(
            XiaoJuSession.id == session_id
        ).first()
        if session:
            db.query(XiaoJuMessage).filter(
                XiaoJuMessage.session_id == session_id
            ).delete()
            session.message_count = 0
            session.context_summary = ""
            session.updated_at = datetime.utcnow()
            db.commit()
            return {"ok": True}
        return {"ok": False, "error": "not found"}
    finally:
        db.close()


@router.get("/sessions/{session_id}/messages")
def get_messages(session_id: int):
    """获取会话消息列表"""
    db = SessionLocal()
    try:
        session = db.query(XiaoJuSession).filter(
            XiaoJuSession.id == session_id
        ).first()
        msgs = db.query(XiaoJuMessage).filter(
            XiaoJuMessage.session_id == session_id
        ).order_by(XiaoJuMessage.created_at.asc()).all()
        return {
            "session": {
                "id": session.id,
                "topic": session.topic,
                "node_id": session.node_id,
                "context_summary": session.context_summary if session else "",
                "is_archived": session.is_archived if session else 0,
            } if session else {},
            "messages": [
                {
                    "id": m.id,
                    "role": m.role,
                    "content": m.content,
                    "created_at": m.created_at.strftime("%H:%M") if m.created_at else "",
                }
                for m in msgs
            ]
        }
    finally:
        db.close()


def _archived_old_messages(session, db):
    """超过15轮自动压缩摘要存档，保留最新15轮"""
    max_visible = 30  # 15轮对话 = 30条消息（15 user + 15 assistant）
    count = db.query(XiaoJuMessage).filter(
        XiaoJuMessage.session_id == session.id
    ).count()
    if count > max_visible:
        # 取前 count - max_visible 条做摘要
        old_msgs = db.query(XiaoJuMessage).filter(
            XiaoJuMessage.session_id == session.id
        ).order_by(XiaoJuMessage.created_at.asc()).limit(count - max_visible).all()

        summary_text = "\n".join([
            f"{'用户' if m.role == 'user' else '小橘'}: {m.content[:100]}"
            for m in old_msgs
        ])
        prompt = f"""请将以下对话压缩成一段摘要（50字内），保留关键信息和决策：\n\n{summary_text}"""
        summary = chat(prompt, max_tokens=100)

        # 存档
        old_summary = session.context_summary or ""
        if old_summary:
            session.context_summary = old_summary + "\n" + summary
        else:
            session.context_summary = summary
        session.message_count = max_visible

        # 删除旧消息
        for m in old_msgs:
            db.delete(m)
        db.commit()


@router.post("/sessions/{session_id}/chat")
def send_message(session_id: int, content: str = ""):
    """发送消息给AI并获取回复（自动管理上下文）"""
    if not content:
        return {"reply": "喵？你说什么~"}

    db = SessionLocal()
    try:
        session = db.query(XiaoJuSession).filter(
            XiaoJuSession.id == session_id
        ).first()
        if not session:
            return {"reply": "会话不存在，请重新创建~", "error": "not_found"}

        # 1. 保存用户消息
        user_msg = XiaoJuMessage(
            session_id=session_id, role="user", content=content
        )
        db.add(user_msg)
        session.message_count = (session.message_count or 0) + 1
        session.updated_at = datetime.utcnow()

        # 2. 自动命名对话（第一条消息做主题）
        if session.message_count <= 2 and not session.topic or session.topic == "新对话":
            topic_prompt = f"用5个字以内概括这条消息的主题（只返回主题）：{content[:50]}"
            topic = chat(topic_prompt, max_tokens=20)
            if topic and len(topic) > 0:
                session.topic = topic[:20]

        # 3. 构建上下文
        messages = db.query(XiaoJuMessage).filter(
            XiaoJuMessage.session_id == session_id
        ).order_by(XiaoJuMessage.created_at.asc()).limit(30).all()

        context_messages = []
        # 系统角色
        system = XIAOJU_SYSTEM
        # 持久记忆
        memories = db.query(XiaoJuMemory).filter(
            XiaoJuMemory.user_id == session.user_id
        ).all()
        if memories:
            mem_text = "\n".join([
                f"- {m.key}: {m.value[:100]}"
                for m in memories
            ])
            system += f"\n\n关于用户我知道的信息：\n{mem_text}"
        # 会话摘要
        if session.context_summary:
            system += f"\n\n之前的对话摘要：{session.context_summary[:200]}"
        system += "\n\n请简短回复（100字内优先），用自然的中文，适当用喵~口癖但不多用。"

        for m in messages:
            context_messages.append({
                "role": m.role, "content": m.content
            })

        prompt_text = "\n".join([
            f"{'用户' if m['role'] == 'user' else '你'}: {m['content']}"
            for m in context_messages[-10:]  # 最近5轮
        ])

        reply = chat(
            prompt_text,
            system=system,
            max_tokens=500,
            temperature=0.7,
        )
        if not reply:
            reply = "喵…这个问题让本橘想想🤔 你再说一遍？"

        # 4. 保存AI回复
        ai_msg = XiaoJuMessage(
            session_id=session_id, role="assistant", content=reply
        )
        db.add(ai_msg)
        session.message_count = (session.message_count or 0) + 1
        db.commit()

        # 5. 超过15轮自动压缩
        _archived_old_messages(session, db)

        return {"reply": reply}
    finally:
        db.close()


# ═══════════════════════════════════════════
# 持久记忆管理
# ═══════════════════════════════════════════
@router.get("/memories")
def list_memories(user_id: int = 1):
    db = SessionLocal()
    try:
        items = db.query(XiaoJuMemory).filter(
            XiaoJuMemory.user_id == user_id
        ).all()
        return {
            "items": [
                {"id": m.id, "key": m.key, "value": m.value, "memory_type": m.memory_type}
                for m in items
            ]
        }
    finally:
        db.close()


@router.post("/memories")
def add_memory(user_id: int = 1, key: str = "", value: str = "",
               memory_type: str = "user_info"):
    db = SessionLocal()
    try:
        m = XiaoJuMemory(
            user_id=user_id, key=key, value=value, memory_type=memory_type
        )
        db.add(m)
        db.commit()
        return {"ok": True}
    finally:
        db.close()


@router.delete("/memories/{mid}")
def delete_memory(mid: int):
    db = SessionLocal()
    try:
        m = db.query(XiaoJuMemory).filter(XiaoJuMemory.id == mid).first()
        if m:
            db.delete(m)
            db.commit()
        return {"ok": True}
    finally:
        db.close()
