"""AI 助手 —— 全局右下角悬浮聊天助手"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from routers.llm import chat_messages

router = APIRouter(prefix="/api/assistant", tags=["assistant"])


class ChatRequest(BaseModel):
    messages: list[dict]  # [{"role": "user", "content": "..."}, ...]
    system: str = ""

SYSTEM_PROMPT = """你是「启途」AI求职助手的智能小AI，名叫小橘。你是穿小西装的橘猫形象，既专业又亲切。

你的核心角色：
1. 回答用户关于求职、面试、职业规划的问题
2. 帮助用户了解如何使用启途平台的各项功能
3. 给用户加油打气，缓解求职焦虑

回答风格：
- 活泼但不轻浮，专业但不冰冷
- 用"喵"开头或结尾可以增加亲和力
- 回答要简洁实用，不废话
- 对求职焦虑的用户要多鼓励、给具体建议
- 涉及具体职业问题时，给出实实在在的建议，不虚不空

如果你不知道某个功能的细节，就诚实说，不要瞎编。"""


@router.post("/chat")
def assistant_chat(req: ChatRequest):
    try:
        system = req.system or SYSTEM_PROMPT
        text = chat_messages(req.messages, system=system, max_tokens=1024, temperature=0.7)
        return {"reply": text}
    except Exception as e:
        return JSONResponse({"reply": "喵……小橘刚才走神了，能再说一次吗？", "error": str(e)}, status_code=200)