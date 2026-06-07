"""
Dashboard 数据 — 首页推荐、统计、热力图等
"""
from fastapi import APIRouter
from database import SessionLocal
from models import InterviewSession, ExamRecord
from sqlalchemy import func
import random

router = APIRouter(prefix="/api/dashboard", tags=["首页"])

# ── 题库知识点（用于推荐） ──
TOPIC_POOL = [
    {"text": "HTTP 缓存策略详解", "tag": "面试", "url": "/interview", "type": "interview"},
    {"text": "URL 到渲染：浏览器做了什么？", "tag": "面试", "url": "/interview", "type": "interview"},
    {"text": "前端模块化发展史", "tag": "面试", "url": "/interview", "type": "interview"},
    {"text": "进程与线程的区别", "tag": "面试", "url": "/interview", "type": "interview"},
    {"text": "RESTful API 设计原则", "tag": "面试", "url": "/interview", "type": "interview"},
    {"text": "关系型 vs 非关系型数据库", "tag": "面试", "url": "/interview", "type": "interview"},
    {"text": "面向对象三大特性", "tag": "面试", "url": "/interview", "type": "interview"},
    {"text": "HTTPS 如何保障安全", "tag": "面试", "url": "/interview", "type": "interview"},
    {"text": "行测逻辑推理专项练习", "tag": "笔试", "url": "/exam-practice", "type": "exam"},
    {"text": "数量关系速算技巧", "tag": "笔试", "url": "/exam-practice", "type": "exam"},
    {"text": "资料分析：图表题精练", "tag": "笔试", "url": "/exam-practice", "type": "exam"},
    {"text": "计算机专业基础真题", "tag": "笔试", "url": "/exam-practice", "type": "exam"},
]

CAREER_POOL = [
    {"text": "软件工程师成长路线", "tag": "职业", "url": "/career/软件工程师", "type": "career"},
    {"text": "数据分析师入门攻略", "tag": "职业", "url": "/career/数据分析师", "type": "career"},
    {"text": "产品经理能力模型", "tag": "职业", "url": "/career/产品经理", "type": "career"},
    {"text": "前端开发技能树", "tag": "职业", "url": "/career/前端开发", "type": "career"},
    {"text": "网络安全方向概览", "tag": "职业", "url": "/career/网络安全工程师", "type": "career"},
    {"text": "AI/ML 就业方向", "tag": "职业", "url": "/career/AI工程师", "type": "career"},
]


@router.get("/recommendations")
def get_recommendations():
    """返回 4 条推荐内容：2 面试/笔试 + 2 职业"""
    random.shuffle(TOPIC_POOL)
    random.shuffle(CAREER_POOL)
    items = TOPIC_POOL[:2] + CAREER_POOL[:2]
    # 标记时间标签
    labels = ["今天 · 新", "推荐", "热门", "刚刚更新"]
    result = []
    for i, item in enumerate(items):
        result.append({
            "text": item["text"],
            "tag": item["tag"],
            "url": item["url"],
            "label": labels[i % len(labels)],
        })
    return {"items": result}


@router.get("/stats")
def get_stats():
    """返回首页统计卡片数据"""
    db = SessionLocal()
    try:
        interview_count = db.query(func.count(InterviewSession.id)).scalar() or 0
        exam_count = db.query(func.count(ExamRecord.id)).scalar() or 0
        # 平均分：取最近面试的平均分
        avg_row = db.query(func.avg(InterviewSession.average_score)).scalar()
        avg_score = round(avg_row, 1) if avg_row else 0
    finally:
        db.close()
    return {
        "explored_count": interview_count + exam_count,
        "interview_count": interview_count,
        "optimize_count": 0,  # 简历优化次数暂缺来源
        "avg_score": avg_score,
    }


@router.get("/activities")
def get_activities(limit: int = 5):
    """返回最近操作记录"""
    db = SessionLocal()
    try:
        # 面试记录
        sessions = db.query(InterviewSession).order_by(InterviewSession.created_at.desc()).limit(limit).all()
        exams = db.query(ExamRecord).order_by(ExamRecord.created_at.desc()).limit(limit).all()
    finally:
        db.close()

    acts = []
    for s in sessions:
        career = s.job or "面试"
        acts.append({"text": f"完成「{career}」模拟面试", "time": s.created_at.strftime("%m-%d %H:%M") if s.created_at else "最近"})
    for e in exams:
        career = e.career or "笔试"
        acts.append({"text": f"完成「{career}」{e.mode or '笔试练习'}", "time": e.created_at.strftime("%m-%d %H:%M") if e.created_at else "最近"})
    if not acts:
        acts.append({"text": "欢迎来到启途！开始你的求职之旅", "time": "刚刚"})
    acts.sort(key=lambda x: x["time"], reverse=True)
    return {"items": acts[:limit]}


@router.get("/heatmap")
def get_heatmap(year: int = 0, month: int = 0):
    """返回指定年月活跃格子数据（基于面试/笔试记录日期）"""
    from datetime import datetime
    now = datetime.now()
    y = year if year > 0 else now.year
    m = month if month >= 0 else now.month

    db = SessionLocal()
    try:
        # 收集面试和笔试记录的日期
        session_dates = db.query(func.date(InterviewSession.created_at)).filter(
            func.extract('year', InterviewSession.created_at) == y,
            func.extract('month', InterviewSession.created_at) == m
        ).all()
        exam_dates = db.query(func.date(ExamRecord.created_at)).filter(
            func.extract('year', ExamRecord.created_at) == y,
            func.extract('month', ExamRecord.created_at) == m
        ).all()
    finally:
        db.close()

    active_days = set()
    for (d,) in session_dates:
        if d:
            day = int(d.split("-")[2])
            active_days.add(day)
    for (d,) in exam_dates:
        if d:
            day = int(d.split("-")[2])
            active_days.add(day)

    # 构建 28 列 × 7 行的数据
    import calendar
    total_days = calendar.monthrange(y, m)[1]
    data = []
    for day in range(1, 197):  # 196 = 28*7, 只取真实天数
        if day <= total_days:
            if day in active_days:
                # 根据活跃次数分等级
                level = random.choice(["l1", "l2", "l3", "l4"])
                data.append(level)
            else:
                data.append("")
        else:
            data.append("")
    return {"year": y, "month": m, "data": data}