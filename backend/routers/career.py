from fastapi import APIRouter

router = APIRouter(prefix="/api/career", tags=["职业探索"])

@router.post("/explore")
def explore_career(major: str = "", interests: str = ""):
    """学生输入专业+兴趣 → 返回职业推荐（当前返回占位数据）"""
    return {
        "recommendations": [
            {"career": "前端开发工程师", "reason": "匹配你的专业和兴趣", "skills": ["HTML", "CSS", "JavaScript", "Vue"]},
            {"career": "后端开发工程师", "reason": "匹配你的专业和兴趣", "skills": ["Python", "FastAPI", "SQL"]},
            {"career": "数据分析师", "reason": "匹配你的专业和兴趣", "skills": ["Python", "SQL", "Excel"]},
        ]
    }