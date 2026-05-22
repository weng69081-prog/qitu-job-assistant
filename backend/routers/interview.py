from fastapi import APIRouter

router = APIRouter(prefix="/api/interview", tags=["面试模拟"])

@router.post("/start")
def start_interview(position: str = "", question_type: str = "", duration: int = 15):
    """开始面试 → 返回第一道题（当前返回占位数据）"""
    return {
        "session_id": "demo-001",
        "question": "请用一分钟介绍一下你自己，以及你为什么选择这个岗位？",
        "question_index": 1,
        "total_questions": 5,
        "time_limit": 60,
    }

@router.post("/submit")
def submit_answer(session_id: str = "", answer_text: str = ""):
    """提交回答 → 返回打分结果（当前返回占位数据，后续接讯飞API）"""
    return {
        "score_tech": 85.0,
        "score_express": 78.0,
        "score_emotion": 90.0,
        "comment": "回答流畅，技术点基本覆盖，建议多举实际项目案例。",
        "next_question": "请描述一个你参与过的项目，说说你在其中承担的角色和遇到的挑战？",
    }

@router.post("/report")
def get_report(session_id: str = ""):
    """面试结束 → 返回完整报告（当前返回占位数据）"""
    return {
        "overall_score": 84.3,
        "scores": {"tech": 85, "express": 78, "emotion": 90},
        "radar_data": [85, 78, 90],
        "details": [
            {"question": "自我介绍", "score": 85, "comment": "表达清晰"},
            {"question": "项目经验", "score": 78, "comment": "缺少具体数据支撑"},
        ],
        "suggestions": ["多用STAR法则描述项目", "准备2-3个技术深度问题"],
    }