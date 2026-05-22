from fastapi import APIRouter

router = APIRouter(prefix="/api/resume", tags=["简历优化"])

@router.post("/upload")
def upload_resume():
    """上传简历文件 → 返回解析结果（占位）"""
    return {"status": "ok", "message": "简历上传功能待实现"}

@router.post("/optimize")
def optimize_resume(original_text: str = ""):
    """AI优化简历（当前返回占位数据）"""
    return {
        "optimized": original_text + "\n\n[AI优化建议：添加量化成果、使用行动动词]",
        "suggestions": [
            "建议在项目经历中添加具体数据（如提升XX%）",
            "技能部分建议分类为：精通/熟练/了解",
        ]
    }

@router.post("/generate")
def generate_resume(education: str = "", skills: str = "", projects: str = "", experience: str = ""):
    """根据用户信息自动生成简历（当前返回占位模板）"""
    return {
        "resume": f"# 个人简历\n\n## 教育背景\n{education}\n\n## 技能\n{skills}\n\n## 项目经历\n{projects}\n\n## 实习经历\n{experience}",
        "message": "简历已生成"
    }