from fastapi import APIRouter

router = APIRouter(prefix="/api/jobmatch", tags=["投递分析"])

@router.post("/analyze")
def analyze_match(jd_text: str = "", resume_text: str = ""):
    """粘贴JD + 简历 → 匹配度分析（当前返回占位数据）"""
    return {
        "match_score": 72,
        "details": [
            {"requirement": "Python", "status": "match", "comment": "简历中包含"},
            {"requirement": "Vue.js", "status": "match", "comment": "简历中包含"},
            {"requirement": "Docker", "status": "miss", "comment": "简历中未提及，建议学习"},
            {"requirement": "2年以上经验", "status": "partial", "comment": "有实习经验但年限不足"},
        ],
        "suggestions": ["建议补充Docker容器化经验", "突出实习项目中的团队协作经历"],
        "companies": [
            {"name": "字节跳动", "match": 75, "reason": "技术栈匹配，应届生友好"},
            {"name": "美团", "match": 70, "reason": "后端岗位需求大"},
            {"name": "阿里云", "match": 65, "reason": "Python技术栈匹配"},
        ]
    }