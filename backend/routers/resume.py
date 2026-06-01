import base64
import json
import os
import sqlite3
import tempfile
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
from resume_generator import generate_resume_docx

router = APIRouter(prefix="/api/resume", tags=["简历优化"])

# ── 简历历史记录表 ──
HISTORY_DB = "data/resume_history.db"

def init_history_db():
    os.makedirs("data", exist_ok=True)
    with sqlite3.connect(HISTORY_DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS resume_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                template_id TEXT DEFAULT 'classic',
                template_name TEXT DEFAULT '',
                career TEXT DEFAULT '',
                name TEXT DEFAULT '',
                form_data TEXT DEFAULT '{}',
                generated_text TEXT DEFAULT '',
                created_at TEXT DEFAULT (datetime('now','localtime'))
            )
        """)

init_history_db()

# ── 数据模型 ──


class Education(BaseModel):
    school: str = ""
    major: str = ""
    degree: str = ""
    start_date: str = ""
    end_date: str = ""
    courses: str = ""


class ExperienceItem(BaseModel):
    company: str = ""
    position: str = ""
    period: str = ""
    content: str = ""


class ProjectItem(BaseModel):
    name: str = ""
    period: str = ""
    role: str = ""
    achievement: str = ""


class Skills(BaseModel):
    office: str = ""
    professional: str = ""
    programming: str = ""
    certificates: str = ""
    languages: str = ""


class CampusItem(BaseModel):
    name: str = ""
    period: str = ""
    role: str = ""


class AwardItem(BaseModel):
    name: str = ""
    period: str = ""
    issuer: str = ""


class ResumeGenerateRequest(BaseModel):
    name: str = ""
    gender: str = ""
    age: str = ""
    phone: str = ""
    email: str = ""
    address: str = ""
    job_intention: str = ""
    target_location: str = ""
    wechat: str = ""
    photo: str = ""  # base64 照片数据
    education: Education = Education()
    experiences: List[ExperienceItem] = []
    projects: List[ProjectItem] = []
    skills: Skills = Skills()
    campus_activities: List[CampusItem] = []
    awards: List[AwardItem] = []
    self_evaluation: str = ""
    career: str = ""
    template_id: str = ""
    requirements: str = ""


class TemplateGenerateRequest(BaseModel):
    template_id: str = ""
    mode: str = "optimize"
    resume_text: str = ""
    requirements: str = ""
    career: str = ""
    name: str = ""


# ── 模板定义 ──
TEMPLATES = {
    "classic": {"name": "简约经典", "desc": "标准结构，适合所有岗位"},
    "skill-first": {"name": "技能突出", "desc": "技能前置，技术岗首选"},
    "project-focused": {"name": "项目驱动", "desc": "项目详细展开"},
    "fresh-grad": {"name": "应届生友好", "desc": "教育+校园突出"},
    "management": {"name": "管理型", "desc": "成果量化突出"},
    "minimal": {"name": "简约现代", "desc": "干净清爽"},
}


# ── 接口 ──


@router.post("/upload-file")
async def upload_resume_file(file: UploadFile = File(...)):
    content = await file.read()
    filename = file.filename or "unknown"
    ext = os.path.splitext(filename)[1].lower()
    if ext == ".txt":
        text = content.decode("utf-8", errors="replace")
    else:
        text = (
            f"[{ext.upper()} 格式待支持，粘贴文本到文本框使用]\n"
            f"文件：{filename}\n大小：{len(content)} 字节\n\n"
            + content.decode("utf-8", errors="replace")[:2000]
        )
    return {"filename": filename, "text": text, "size": len(content), "format": ext}


@router.get("/templates")
def list_templates():
    return {"templates": [{"id": k, "desc": v["desc"]} for k, v in TEMPLATES.items()]}


@router.post("/generate-with-template")
def generate_with_template(data: TemplateGenerateRequest):
    """根据模板+需求+原始文本生成简历"""
    tpl = TEMPLATES.get(data.template_id, TEMPLATES["classic"])
    career = data.career or "目标岗位"
    lines = []
    lines.append(f"# 个人简历")
    if career:
        lines.append(f"**求职意向：{career}**")
    if data.requirements:
        lines.append(f"*需求：{data.requirements}*")
    lines.append("")
    if data.mode == "optimize" and data.resume_text:
        lines.append(f"** 优化后的简历 **")
        lines.append("")
        for line in data.resume_text.strip().split("\n"):
            lines.append(line)
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append(f"**{tpl['name']}模板 · 优化建议（待接入AI）**")
        if data.requirements:
            lines.append(f"- 根据需求：{data.requirements}")
        lines.append("- 补充量化数据")
        lines.append("- 使用行动动词")
    else:
        lines.append(f"**请填写信息后生成——{tpl['name']}模板（待接入AI）**")
    return {"resume": "\n".join(lines), "template_id": data.template_id, "message": f"已基于「{tpl['name']}」模板生成"}


@router.post("/upload")
def upload_resume():
    return {"status": "ok", "message": "简历上传功能待实现"}


@router.post("/optimize")
def optimize_resume(original_text: str = "", career: str = "", name: str = ""):
    suggestions = [
        "在项目经历中添加具体数据（如提升XX%、服务XX用户）",
        "技能部分分类为：精通/熟练/了解",
        "工作描述使用行动动词开头",
        "每段经历浓缩为3-5个要点",
    ]
    if career:
        suggestions.insert(0, f"根据「{career}」调整关键词")
    return {
        "optimized": original_text + "\n\n——— AI优化建议———\n"
        "1. 每段前加概述\n2. 主动动词\n3. 量化数据\n4. 删不相关内容",
        "suggestions": suggestions,
    }


@router.post("/generate")
def generate_resume(data: ResumeGenerateRequest):
    """根据用户信息+模板生成结构化简历（返回Markdown文本预览）"""
    return {
        "resume": _format_resume_text(data),
        "message": f"已基于「{TEMPLATES.get(data.template_id, TEMPLATES['classic'])['name']}」模板生成",
    }


@router.post("/download")
def download_resume(data: ResumeGenerateRequest):
    """根据用户信息+模板生成 .docx 文件并下载"""
    tmp = tempfile.NamedTemporaryFile(suffix=".docx", delete=False)
    tmp_path = tmp.name
    tmp.close()
    try:
        # 解码照片 base64
        photo_bytes = None
        if data.photo:
            try:
                # 兼容 data:image/...;base64, 格式
                raw = data.photo
                if "," in raw:
                    raw = raw.split(",")[1]
                photo_bytes = base64.b64decode(raw)
            except Exception:
                photo_bytes = None  # 解码失败则忽略

        generate_resume_docx(data, tmp_path, photo_bytes)
        tpl_name = TEMPLATES.get(data.template_id, TEMPLATES["classic"])["name"]
        name_part = data.name or "个人"
        filename = f"简历_{name_part}_{tpl_name}.docx"
        return FileResponse(
            tmp_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=filename,
        )
    except Exception as e:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise HTTPException(status_code=500, detail=f"生成简历文件失败：{str(e)}")


# ── 简历历史记录 ──

class SaveResumeRequest(BaseModel):
    form_data: str = "{}"  # 完整表单 JSON
    generated_text: str = ""
    template_id: str = ""
    career: str = ""
    name: str = ""


@router.post("/save")
def save_resume(data: SaveResumeRequest):
    """保存一份简历到历史记录"""
    tpl_name = TEMPLATES.get(data.template_id, TEMPLATES["classic"])["name"]
    with sqlite3.connect(HISTORY_DB) as conn:
        cur = conn.execute(
            "INSERT INTO resume_history (template_id, template_name, career, name, form_data, generated_text) VALUES (?,?,?,?,?,?)",
            (data.template_id, tpl_name, data.career, data.name, data.form_data, data.generated_text)
        )
        record_id = cur.lastrowid
    return {"ok": True, "id": record_id}


@router.get("/history")
def list_history():
    """列出所有保存的简历（倒序，最多30条）"""
    with sqlite3.connect(HISTORY_DB) as conn:
        rows = conn.execute(
            "SELECT id, template_name, career, name, created_at FROM resume_history ORDER BY id DESC LIMIT 30"
        ).fetchall()
    return {
        "records": [
            {
                "id": r[0], "template_name": r[1], "career": r[2],
                "name": r[3], "created_at": r[4]
            }
            for r in rows
        ]
    }


@router.get("/history/{record_id}")
def get_history(record_id: int):
    """获取某条历史记录的完整数据（用于恢复）"""
    with sqlite3.connect(HISTORY_DB) as conn:
        row = conn.execute("SELECT * FROM resume_history WHERE id=?", (record_id,)).fetchone()
    if not row:
        raise HTTPException(404, "记录不存在")
    return {
        "id": row[0], "template_id": row[1],
        "template_name": row[2], "career": row[3],
        "name": row[4], "form_data": json.loads(row[5]),
        "generated_text": row[6], "created_at": row[7],
    }


@router.delete("/history/{record_id}")
def delete_history(record_id: int):
    """删除一条历史记录"""
    with sqlite3.connect(HISTORY_DB) as conn:
        conn.execute("DELETE FROM resume_history WHERE id=?", (record_id,))
    return {"ok": True}


# ── 格式化文本预览 ──


def _format_resume_text(data: ResumeGenerateRequest) -> str:
    """生成 Markdown 文本预览（与 .docx 内容一致但不含排版）"""
    tpl = TEMPLATES.get(data.template_id, TEMPLATES["classic"])
    career_label = data.career or data.job_intention or "目标岗位"
    lines = []
    lines.append(f"# {data.name or '个人简历'}")
    lines.append(f"**求职意向：{career_label}**")
    if data.requirements:
        lines.append(f"*{data.requirements}*")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 个人信息")
    info = []
    if data.name: info.append(f"- 姓名：{data.name}")
    if data.gender: info.append(f"- 性别：{data.gender}")
    if data.age: info.append(f"- 年龄：{data.age}")
    if data.phone: info.append(f"- 电话：{data.phone}")
    if data.email: info.append(f"- 邮箱：{data.email}")
    if data.address: info.append(f"- 现居：{data.address}")
    if data.wechat: info.append(f"- 微信：{data.wechat}")
    if data.job_intention or data.target_location:
        parts = [data.job_intention, data.target_location]
        info.append(f"- 求职意向：{' · '.join(p for p in parts if p)}")
    lines.extend(info)
    lines.append("")

    edu = data.education
    if edu.school or edu.major:
        lines.append("## 教育经历")
        edu_line = edu.school or ""
        if edu.major: edu_line += f" | {edu.major}"
        if edu.degree: edu_line += f" | {edu.degree}"
        lines.append(f"**{edu_line}**")
        if edu.start_date or edu.end_date:
            lines.append(f"*{edu.start_date} — {edu.end_date}*")
        if edu.courses:
            lines.append(f"主修课程：{edu.courses}")
        lines.append("")

    if data.experiences:
        lines.append("## 工作/实习经历")
        for exp in data.experiences:
            header = exp.company or ""
            if exp.position: header += f" · {exp.position}"
            if exp.period: header += f"  ({exp.period})"
            lines.append(f"- **{header}**")
            if exp.content:
                for c in exp.content.split("\n"):
                    c = c.strip()
                    if c: lines.append(f"  · {c}")
            lines.append("")

    if data.projects:
        lines.append("## 项目经历")
        for proj in data.projects:
            header = proj.name or ""
            if proj.period: header += f"  ({proj.period})"
            lines.append(f"- **{header}**")
            if proj.role: lines.append(f"  职责：{proj.role}")
            if proj.achievement:
                for a in proj.achievement.split("\n"):
                    a = a.strip()
                    if a: lines.append(f"  · {a}")
            lines.append("")

    sk = data.skills
    if any([sk.office, sk.professional, sk.programming, sk.certificates, sk.languages]):
        lines.append("## 专业技能")
        if sk.office: lines.append(f"- 办公软件：{sk.office}")
        if sk.professional: lines.append(f"- 专业软件：{sk.professional}")
        if sk.programming: lines.append(f"- 编程语言：{sk.programming}")
        if sk.certificates: lines.append(f"- 证书：{sk.certificates}")
        if sk.languages: lines.append(f"- 语言能力：{sk.languages}")
        lines.append("")

    if data.campus_activities:
        lines.append("## 校园经历")
        for act in data.campus_activities:
            header = act.name or ""
            if act.period: header += f" · {act.period}"
            lines.append(f"- **{header}**")
            if act.role: lines.append(f"  {act.role}")
            lines.append("")

    if data.awards:
        lines.append("## 荣誉奖项")
        for aw in data.awards:
            name = aw.name or ""
            extra = ""
            if aw.period: extra = f"（{aw.period}）"
            if aw.issuer: extra += f" 颁发：{aw.issuer}"
            lines.append(f"- **{name}** {extra}".strip())
        lines.append("")

    if data.self_evaluation:
        lines.append("## 自我评价")
        for line in data.self_evaluation.split("\n"):
            line = line.strip()
            if line: lines.append(f"{line}")
        lines.append("")

    return "\n".join(lines)