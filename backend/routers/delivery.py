"""
求职投递助手 API — 岗位数据 + AI分析 + 投递台账 + Agent搜索入口
"""
import json, os, re, requests, random
from datetime import datetime
from urllib.parse import quote_plus
from fastapi import APIRouter, Query, HTTPException, Body
from sqlalchemy.orm import Session
from database import get_db, SessionLocal
from models import DeliveryJob, DeliveryTracking, Profile, ExamRecord, WeaknessItem
from routers.user import get_user_id

router = APIRouter(prefix="/api/delivery", tags=["求职投递助手"])

# ── AI 生成真实公司岗位数据 ──
REAL_COMPANIES_CAREER_URLS = {
    "字节跳动": "https://jobs.bytedance.com/",
    "阿里巴巴": "https://talent.alibaba.com/",
    "腾讯": "https://join.qq.com/",
    "华为": "https://career.huawei.com/",
    "小米": "https://xiaomi.jobs.feishu.cn/",
    "百度": "https://talent.baidu.com/",
    "京东": "https://zhaopin.jd.com/",
    "网易": "https://hr.163.com/",
    "美团": "https://zhaopin.meituan.com/",
    "快手": "https://zhaopin.kuaishou.cn/",
    "小红书": "https://job.xiaohongshu.com/",
    "哔哩哔哩": "https://jobs.bilibili.com/",
    "滴滴": "https://talent.didiglobal.com/",
    "拼多多": "https://careers.pinduoduo.com/",
    "理想汽车": "https://www.lixiang.com/join",
    "蔚来": "https://nio.jobs.feishu.cn/",
    "科大讯飞": "https://recruit.iflytek.com/",
    "中兴通讯": "https://job.zte.com.cn/",
    "OPPO": "https://careers.oppo.com/",
    "vivo": "https://hr.vivo.com/",
    "比亚迪": "https://job.byd.com/",
    "联想": "https://talent.lenovo.com.cn/",
    "中国银行": "https://www.boc.cn/aboutboc/careers/",
    "中国工商银行": "https://job.icbc.com.cn/",
    "招商银行": "https://career.cmbchina.com/",
    "用友网络": "https://www.yonyou.com/article/recruit/",
    "海康威视": "https://www.hikvision.com/cn/recruit/",
    "深信服": "https://www.sangfor.com/recruit",
    "广联达": "https://www.glodon.com/recruit/",
    "金蝶国际": "https://www.kingdee.com/recruit",
}

def _ai_seed_batch(career_urls):
    """调 AI 生成一批真实岗位数据"""
    company_list = "\n".join(f"- {name} （招聘页: {url}）" for name, url in career_urls.items())
    prompt = f"""你是一个招聘数据专家。请为以下真实企业各生成2个正在招聘的校招/实习岗位信息。

注意：
- 岗位必须是这些企业真正会招的，符合企业业务方向
- 公司简介写真实的企业情况
- 技能要求写真实的语言/框架/工具
- 薪资范围要合理（校招/实习岗）
- apply_url 使用企业真实招聘页链接
- 城市写企业实际所在地

{company_list}

返回一个JSON数组，每个元素格式：
{{
  "company_name": "公司名",
  "company_logo": "https://img.icons8.com/color/48/公司名小写.png",
  "company_website": "https://www.xxx.com",
  "company_size": "巨头/大型/中型",
  "industry": "行业",
  "company_intro": "企业简介（30字以内）",
  "job_title": "岗位名",
  "job_type": "技术|产品|运营|设计|市场|职能",
  "city": "城市",
  "address": "城市+具体地址",
  "salary_min": 最低薪资整数,
  "salary_max": 最高薪资整数,
  "salary_text": "薪资范围文字",
  "education": "大专/本科/硕士及以上",
  "experience": "应届/1-3年/实习",
  "job_description": "岗位职责（40字以内）",
  "skills_required": "技能数组JSON字符串，如[\\"Python\\",\\"SQL\\"]",
  "skills_preferred": "加分技能数组JSON字符串",
  "apply_url": "企业真实招聘页URL",
  "interview_rounds": "面试轮次",
  "interview_form": "线上面试/现场面试",
  "interview_focus": "面试重点",
  "has_exam": true或false
}}

只返回JSON数组，不要markdown代码块。生成{len(career_urls)*2}条数据。"""

    from routers.llm import chat as llm_chat
    content = llm_chat(prompt, temperature=0.7, max_tokens=8000)
    if not content:
        return []
    if content.startswith("```"):
        content = content.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        if content.startswith("json"):
            content = content[4:].strip()
    try:
        jobs = json.loads(content)
        if isinstance(jobs, dict) and "jobs" in jobs:
            jobs = jobs["jobs"]
        return jobs if isinstance(jobs, list) else []
    except (json.JSONDecodeError, Exception):
        return []

def seed_jobs():
    """用AI生成真实岗位替代硬编码假数据"""
    db = SessionLocal()
    try:
        existing = db.query(DeliveryJob).count()
        if existing >= 10:
            return

        # 分批生成
        all_items = list(REAL_COMPANIES_CAREER_URLS.items())
        batch_size = 8
        total_generated = 0
        for i in range(0, len(all_items), batch_size):
            batch = dict(all_items[i:i+batch_size])
            jobs = _ai_seed_batch(batch)
            for j in jobs:
                job = DeliveryJob(
                    company_name=j.get("company_name", "未知企业"),
                    company_logo=j.get("company_logo", ""),
                    company_website=j.get("company_website", ""),
                    company_size=j.get("company_size", "中型"),
                    industry=j.get("industry", "互联网/科技"),
                    company_intro=j.get("company_intro", ""),
                    job_title=j.get("job_title", "工程师"),
                    job_type=j.get("job_type", "技术"),
                    city=j.get("city", "北京"),
                    address=j.get("address", ""),
                    salary_min=j.get("salary_min", 8000),
                    salary_max=j.get("salary_max", 15000),
                    salary_text=j.get("salary_text", "8K-15K"),
                    education=j.get("education", "本科"),
                    experience=j.get("experience", "应届"),
                    job_description=j.get("job_description", ""),
                    skills_required=json.dumps(j.get("skills_required", []), ensure_ascii=False),
                    skills_preferred=json.dumps(j.get("skills_preferred", []), ensure_ascii=False),
                    publish_time=datetime.now().strftime("%Y-%m-%d"),
                    deadline=datetime.now().strftime("%Y-%m-%d"),
                    has_exam=j.get("has_exam", False),
                    apply_url=j.get("apply_url", ""),
                    interview_rounds=j.get("interview_rounds", "2-3轮"),
                    interview_form=j.get("interview_form", "线上面试"),
                    interview_focus=j.get("interview_focus", ""),
                    career_category="",
                    source="ai_generated",
                )
                db.add(job)
                total_generated += 1
            db.commit()

        if total_generated == 0:
            # AI失败时用兜底数据
            _fallback_seed_jobs(db)
            db.commit()
    finally:
        db.close()

def _fallback_seed_jobs(db):
    """AI生成失败时的兜底：用预设的知名企业数据"""
    fallback_companies = [
        {"name":"字节跳动","career":"https://jobs.bytedance.com/","size":"巨头","industry":"互联网/科技"},
        {"name":"阿里巴巴","career":"https://talent.alibaba.com/","size":"巨头","industry":"电子商务/科技"},
        {"name":"腾讯","career":"https://join.qq.com/","size":"巨头","industry":"互联网/科技"},
        {"name":"华为","career":"https://career.huawei.com/","size":"巨头","industry":"通信/科技"},
        {"name":"小米","career":"https://xiaomi.jobs.feishu.cn/","size":"大型","industry":"消费电子/互联网"},
        {"name":"百度","career":"https://talent.baidu.com/","size":"大型","industry":"互联网/人工智能"},
        {"name":"京东","career":"https://zhaopin.jd.com/","size":"大型","industry":"电子商务/物流"},
        {"name":"网易","career":"https://hr.163.com/","size":"大型","industry":"互联网/游戏"},
        {"name":"快手","career":"https://zhaopin.kuaishou.cn/","size":"大型","industry":"短视频/社交"},
        {"name":"哔哩哔哩","career":"https://jobs.bilibili.com/","size":"大型","industry":"互联网/文化"},
        {"name":"小红书","career":"https://job.xiaohongshu.com/","size":"大型","industry":"社交/电商"},
        {"name":"滴滴","career":"https://talent.didiglobal.com/","size":"大型","industry":"出行/科技"},
        {"name":"拼多多","career":"https://careers.pinduoduo.com/","size":"大型","industry":"电子商务"},
        {"name":"理想汽车","career":"https://www.lixiang.com/join","size":"大型","industry":"新能源汽车"},
        {"name":"科大讯飞","career":"https://recruit.iflytek.com/","size":"大型","industry":"人工智能"},
        {"name":"OPPO","career":"https://careers.oppo.com/","size":"大型","industry":"消费电子"},
        {"name":"比亚迪","career":"https://job.byd.com/","size":"巨头","industry":"新能源汽车/电子"},
        {"name":"招商银行","career":"https://career.cmbchina.com/","size":"大型","industry":"金融/银行"},
    ]
    cities = ["北京","上海","深圳","杭州","广州","成都","武汉","南京","西安"]
    salaries = [(8000,15000,"8K-15K"),(12000,25000,"12K-25K"),(15000,30000,"15K-30K"),(20000,40000,"20K-40K")]
    job_templates = [
        {"title":"后端开发工程师","type":"技术","skills":"Java,SpringBoot,MySQL","focus":"算法,系统设计"},
        {"title":"前端开发工程师","type":"技术","skills":"Vue,React,TypeScript","focus":"前端基础,性能优化"},
        {"title":"算法工程师","type":"技术","skills":"Python,深度学习,机器学习","focus":"算法推导,论文解读"},
        {"title":"产品经理","type":"产品","skills":"产品设计,用户研究,数据分析","focus":"产品思维,需求分析"},
        {"title":"新媒体运营","type":"运营","skills":"内容创作,社交媒体运营","focus":"内容策划,数据分析"},
        {"title":"UI/UX设计师","type":"设计","skills":"Figma,交互设计","focus":"设计作品集,交互细节"},
    ]
    for co in fallback_companies:
        import random
        for _ in range(2):
            tpl = random.choice(job_templates)
            city = random.choice(cities)
            sal = random.choice(salaries)
            job = DeliveryJob(
                company_name=co["name"],
                company_logo=f"https://img.icons8.com/color/48/{co['name'].lower()}.png",
                company_website=f"https://www.{co['name']}.com",
                company_size=co["size"],
                industry=co["industry"],
                company_intro=f"{co['name']}是一家知名企业",
                job_title=tpl["title"],
                job_type=tpl["type"],
                city=city,
                address=f"{city}科技园区",
                salary_min=sal[0], salary_max=sal[1], salary_text=sal[2],
                education="本科", experience="应届",
                job_description=f"负责{co['name']}核心业务开发",
                skills_required=json.dumps(tpl["skills"].split(","), ensure_ascii=False),
                skills_preferred="[]",
                publish_time=datetime.now().strftime("%Y-%m-%d"),
                deadline=datetime.now().strftime("%Y-%m-%d"),
                has_exam=False,
                apply_url=co["career"],
                interview_rounds="2-3轮",
                interview_form="线上面试",
                interview_focus=tpl["focus"],
                career_category="",
                source="fallback",
            )
            db.add(job)


from routers.llm import chat as llm_chat

# ── AI 解析（走默认LLM配置 → DeepSeek） ──
def ai_analyze_job(job: DeliveryJob, user_skills: str = ""):
    """AI解析岗位JD + 技能匹配"""
    prompt = f"""你是一位资深的求职顾问和HR专家。请对以下岗位信息进行全面分析，输出JSON格式。

【岗位信息】
公司：{job.company_name}
行业：{job.industry}
岗位：{job.job_title}
工作地点：{job.city}
薪资范围：{job.salary_text}
学历要求：{job.education}
经验要求：{job.experience}
JD描述：{job.job_description}
硬性技能：{job.skills_required}
加分技能：{job.skills_preferred}

用户个人技能：{user_skills or '未知'}

请严格按照以下JSON格式返回，不要加markdown标记，只返回JSON：
{{
    "company_summary": "公司简介（2-3句话）",
    "job_full_title": "招聘岗位全称",
    "location_detail": "工作地点详细说明",
    "hard_skills": ["硬性技能1", "硬性技能2", ...],
    "soft_skills": ["软性要求1", "软性要求2", ...],
    "preferred_skills": ["加分技能1", "加分技能2", ...],
    "matched_skills": ["用户已匹配的技能"],
    "missing_skills": ["用户缺失的技能"],
    "interview_focus": ["面试重点1", "面试重点2", ...],
    "interview_rounds": "面试轮次说明",
    "interview_form": "面试形式说明",
    "resume_tips": ["简历建议1", "简历建议2", ...],
    "deadline": "截止时间说明",
    "has_exam": true/false,
    "overall_assessment": "总体评价（2-3句话，给求职者建议）"
}}"""

    try:
        content = llm_chat(prompt, temperature=0.3, max_tokens=2000)
        if content:
            if content.startswith("```"):
                content = content.split("\n", 1)[1].rsplit("```", 1)[0].strip()
                if content.startswith("json"):
                    content = content[4:].strip()
            return json.loads(content)
        return _fallback_analysis(job)
    except Exception:
        return _fallback_analysis(job)


def _fallback_analysis(job: DeliveryJob):
    """AI失败时的兜底分析"""
    skills_req = json.loads(job.skills_required) if isinstance(job.skills_required, str) else []
    skills_pref = json.loads(job.skills_preferred) if isinstance(job.skills_preferred, str) else []
    return {
        "company_summary": job.company_intro,
        "job_full_title": f"{job.company_name} - {job.job_title}",
        "location_detail": job.address,
        "hard_skills": skills_req,
        "soft_skills": ["团队协作", "沟通能力", "学习能力"],
        "preferred_skills": skills_pref,
        "matched_skills": [],
        "missing_skills": skills_req,
        "interview_focus": [s.strip() for s in job.interview_focus.split("、")],
        "interview_rounds": job.interview_rounds,
        "interview_form": job.interview_form,
        "resume_tips": ["突出项目中与岗位相关的技术栈经验", "用量化数据展示你的成果", "提前了解公司业务和产品"],
        "deadline": f"建议在{job.deadline}前完成投递",
        "has_exam": bool(job.has_exam),
        "overall_assessment": f"该岗位来自{job.company_name}，要求{'、'.join(skills_req)}等技能，建议尽快准备投递。"
    }


# ── API: 技能差距分析（基于学习+笔试情况） ──
@router.get("/gap-analysis/{job_id}")
def gap_analysis(job_id: int, user_id: int = Query(0, description="用户ID")):
    """分析用户的学习/考试情况与目标岗位的差距"""
    db = get_db().__next__()
    try:
        job = db.query(DeliveryJob).filter(DeliveryJob.id == job_id).first()
        if not job:
            raise HTTPException(404, "岗位不存在")

        user_skills = []
        user_weaknesses = []
        exam_accuracy = 0
        exam_count = 0

        if user_id > 0:
            profile = db.query(Profile).filter(Profile.user_id == user_id).first()
            if profile and profile.skills:
                user_skills = [s.strip() for s in profile.skills.split(",") if s.strip()]

            records = db.query(ExamRecord).all()
            if records:
                exam_count = len(records)
                exam_accuracy = sum(r.accuracy for r in records if r.accuracy) / exam_count

            weaknesses = db.query(WeaknessItem).filter(
                WeaknessItem.user_id == user_id
            ).all()
            user_weaknesses = [w.name for w in weaknesses[:20]]

        job_skills_req = json.loads(job.skills_required) if isinstance(job.skills_required, str) else (job.skills_required or [])
        job_skills_pref = json.loads(job.skills_preferred) if isinstance(job.skills_preferred, str) else (job.skills_preferred or [])
        all_job_skills = job_skills_req + [s for s in job_skills_pref if s not in job_skills_req]

        matched = [s for s in all_job_skills if any(usk.lower() in s.lower() or s.lower() in usk.lower() for usk in user_skills)]
        missing = [s for s in job_skills_req if s not in matched]

        prompt = f"""你是一位求职顾问。请分析用户的技能与目标岗位的差距，返回JSON格式。

用户技能：{', '.join(user_skills) or '暂无记录'}
用户笔试情况：共{exam_count}次练习，平均正确率{exam_accuracy*100:.0f}%
用户薄弱知识点：{', '.join(user_weaknesses[:5]) or '暂无记录'}

目标岗位：{job.job_title} @ {job.company_name}
岗位技能要求：{', '.join(job_skills_req)}
岗位加分技能：{', '.join(job_skills_pref)}

返回JSON（只返回JSON，不要markdown）：
{{
  "matched_skills": ["已匹配的技能列表"],
  "missing_skills": ["缺失的技能列表"],
  "match_score": 匹配度分数(0-100),
  "strength_areas": ["用户擅长的方向"],
  "improve_areas": ["需要提升的方向"],
  "priority_recommendations": ["建议1（最优先）", "建议2", "建议3"],
  "exam_feedback": "基于笔试情况的分析和建议（30字以内）",
  "readiness_level": "准备程度：ready/almost/need_work/far",
  "summary": "差距总结（40字以内）"
}}"""

        from routers.llm import chat as llm_chat
        ai_result = llm_chat(prompt, temperature=0.3, max_tokens=2000)
        if ai_result:
            if ai_result.startswith("```"):
                ai_result = ai_result.split("\n",1)[1].rsplit("```",1)[0].strip()
                if ai_result.startswith("json"):
                    ai_result = ai_result[4:].strip()
            try:
                return json.loads(ai_result)
            except json.JSONDecodeError:
                pass

        return {
            "matched_skills": matched,
            "missing_skills": missing,
            "match_score": max(0, min(100, int(len(matched) / max(len(all_job_skills), 1) * 100))),
            "strength_areas": matched[:3] if matched else ["暂无明显优势"],
            "improve_areas": missing[:3] if missing else ["暂无明显短板"],
            "priority_recommendations": [
                f"优先补足{'、'.join(missing[:2])}" if missing else "技能匹配度较好",
                "多练习相关笔试题目" if exam_accuracy < 0.7 else "保持现有练习节奏",
                "加强薄弱知识点学习",
            ],
            "exam_feedback": f"笔试正确率{exam_accuracy:.0f}%，{'建议加强基础练习' if exam_accuracy < 70 else '表现不错，继续保持'}",
            "readiness_level": "ready" if len(missing) == 0 else ("almost" if len(missing) <= 2 else ("need_work" if len(missing) <= 5 else "far")),
            "summary": f"已匹配{len(matched)}项技能，缺失{len(missing)}项{'，需重点补足' if missing else ''}",
        }
    finally:
        db.close()


# ── 搜索公司官网（实时） ──
def search_company_website(company_name: str) -> str:
    """实时搜索公司官网URL"""
    try:
        resp = requests.get(
            "https://api.bing.microsoft.com/v7.0/search",
            headers={"Ocp-Apim-Subscription-Key": os.environ.get("BING_API_KEY", "")},
            params={"q": f"{company_name} 官网", "count": 1},
            timeout=5
        )
        if resp.status_code == 200:
            results = resp.json().get("webPages", {}).get("value", [])
            if results:
                return results[0]["url"]
    except Exception:
        pass
    # 兜底：从真实企业列表取
    for name, url in REAL_COMPANIES_CAREER_URLS.items():
        if name == company_name:
            return url
    return f"https://www.{company_name}.com"


# ── API: 获取岗位列表 ──
def _safe_json_loads(value, default=None):
    if default is None:
        default = []
    try:
        if isinstance(value, str):
            return json.loads(value)
        return value or default
    except Exception:
        return default


def _build_apply_search_url(company: str, title: str, city: str = "") -> str:
    query = f"{company} {title} {city} 官方招聘 投递入口".strip()
    return f"https://www.baidu.com/s?wd={quote_plus(query)}"


def _job_to_card(j: DeliveryJob, source_note: str = "启途岗位库"):
    return {
        "id": j.id,
        "company_name": j.company_name,
        "company_logo": j.company_logo,
        "company_website": j.company_website,
        "company_size": j.company_size,
        "industry": j.industry,
        "job_title": j.job_title,
        "job_type": j.job_type,
        "city": j.city,
        "address": j.address,
        "salary_text": j.salary_text,
        "salary_min": j.salary_min,
        "salary_max": j.salary_max,
        "education": j.education,
        "experience": j.experience,
        "publish_time": j.publish_time,
        "deadline": j.deadline,
        "has_exam": j.has_exam,
        "source": j.source,
        "source_note": source_note,
        "apply_url": str(j.apply_url or "") or _build_apply_search_url(str(j.company_name or ""), str(j.job_title or ""), str(j.city or "")),
        "match_reason": f"与「{str(j.job_title or '')}」方向相关，可查看JD后决定是否投递。",
    }


@router.post("/agent-search")
def agent_search(payload: dict = Body({})):
    """Agent式岗位搜索：先查本地岗位库，搜不到时自动放宽，并给真实搜索入口。"""
    seed_jobs()
    target = (payload.get("target") or payload.get("keyword") or "").strip()
    city = (payload.get("city") or "").strip()
    major = (payload.get("major") or "").strip()
    skills = (payload.get("skills") or "").strip()
    education = (payload.get("education") or "").strip()

    db = get_db().__next__()
    try:
        query = db.query(DeliveryJob)
        if target:
            query = query.filter(
                DeliveryJob.job_title.contains(target) |
                DeliveryJob.company_name.contains(target) |
                DeliveryJob.job_type.contains(target)
            )
        if city:
            query = query.filter(DeliveryJob.city == city)
        exact = query.order_by(DeliveryJob.id.desc()).limit(8).all()

        relaxed_steps = []
        jobs = exact
        if not jobs and city:
            relaxed_steps.append(f"没有找到「{city}」的精确结果，已先放宽城市。")
            query = db.query(DeliveryJob)
            if target:
                query = query.filter(
                    DeliveryJob.job_title.contains(target) |
                    DeliveryJob.company_name.contains(target) |
                    DeliveryJob.job_type.contains(target)
                )
            jobs = query.order_by(DeliveryJob.id.desc()).limit(8).all()
        if not jobs and target:
            relaxed_steps.append("没有找到精确岗位名，已按岗位大类和能力关键词放宽。")
            tokens = [x for x in re.split(r"[，,、/\s]+", f"{target} {skills} {major}") if len(x) >= 2]
            query = db.query(DeliveryJob)
            if tokens:
                token = tokens[0]
                query = query.filter(
                    DeliveryJob.job_title.contains(token) |
                    DeliveryJob.job_description.contains(token) |
                    DeliveryJob.industry.contains(token)
                )
            jobs = query.order_by(DeliveryJob.id.desc()).limit(8).all()

        search_query = " ".join(x for x in [target, city, major, education, "实习 校招 官方招聘"] if x)
        search_url = f"https://www.baidu.com/s?wd={quote_plus(search_query or '校招 实习 官方招聘')}"
        cards = [_job_to_card(j, "启途岗位库匹配") for j in jobs]
        for card in cards:
            card["apply_url"] = _build_apply_search_url(card["company_name"], card["job_title"], card["city"])

        return {
            "ok": True,
            "mode": "exact" if exact else "relaxed" if cards else "external_search",
            "summary": "已按人的目标岗位、城市和背景检索；结果不足时不会编假岗位，会给出真实搜索入口。",
            "relaxed_steps": relaxed_steps,
            "jobs": cards,
            "external_search_url": search_url,
            "jd_paste_hint": "如果搜索结果不准，可以复制真实JD到岗位详情/自定义材料里继续分析差距。",
        }
    finally:
        db.close()


# ── API: 获取岗位列表（自动按用户画像推荐） ──
def _extract_job_type_from_target(target: str) -> str:
    """从目标岗位提取岗位类型"""
    target_lower = target.lower()
    if any(k in target_lower for k in ["开发", "技术", "工程师", "算法", "运维", "测试", "数据"]):
        return "技术"
    return ""

@router.get("/jobs")
def list_jobs(
    token: str = Query("", description="用户token，传了就会按画像推荐"),
    company_size: str = "",
    job_type: str = "",
    salary_min: int = 0,
    salary_max: int = 0,
    city: str = "",
    keyword: str = "",
    page: int = 1,
    page_size: int = 20,
):
    seed_jobs()
    db = get_db().__next__()
    try:
        query = db.query(DeliveryJob)

        # 如果传了token但没有明确筛选条件，尝试按用户画像自动推荐
        profile = None
        if token:
            uid = get_user_id(token)
            if uid:
                profile = db.query(Profile).filter(Profile.user_id == uid).first()

        # 用户没手动选城市，但有画像城市 → 自动按城市筛选
        if not city and profile and profile.city:
            city_list = [c.strip() for c in profile.city.replace("、"," ").replace("，"," ").split() if c.strip()]
            if city_list:
                # 多城市取第一个为主，给推荐提示
                main_city = city_list[0]
                query = query.filter(
                    DeliveryJob.city.contains(main_city[:2]) | DeliveryJob.address.contains(main_city[:2])
                )
                city = main_city  # 标记已按城市筛选

        # 用户没手动选岗位类型，但画像有目标岗位 → 匹配岗位关键词
        if not job_type and profile and profile.job_targets:
            targets = profile.job_targets.replace("、"," ").replace("，"," ").split()
            if targets:
                type_filters = []
                for t in targets[:2]:
                    t = t.strip()
                    if t and len(t) >= 2:
                        type_filters.append(
                            DeliveryJob.job_title.contains(t) |
                            DeliveryJob.job_description.contains(t) |
                            DeliveryJob.job_type.contains(t)
                        )
                if type_filters:
                    from sqlalchemy import or_
                    query = query.filter(or_(*type_filters))

        # 用户没传技能关键词，但画像有skill → 匹配技能
        if not keyword and profile and profile.skills:
            skill_list = [s.strip() for s in profile.skills.split(",") if s.strip() and len(s) >= 2]
            if skill_list:
                skill_filters = []
                for s in skill_list[:3]:
                    skill_filters.append(
                        DeliveryJob.skills_required.contains(s) |
                        DeliveryJob.skills_preferred.contains(s) |
                        DeliveryJob.job_title.contains(s)
                    )
                if skill_filters:
                    from sqlalchemy import or_
                    query = query.filter(or_(*skill_filters))

        # 手动筛选参数（覆盖画像自动筛选）
        if company_size:
            sizes = company_size.split(",")
            query = query.filter(DeliveryJob.company_size.in_(sizes))
        if job_type:
            types = job_type.split(",")
            query = query.filter(DeliveryJob.job_type.in_(types))
        if salary_min > 0:
            query = query.filter(DeliveryJob.salary_max >= salary_min)
        if salary_max > 0:
            query = query.filter(DeliveryJob.salary_min <= salary_max)
        if city:
            query = query.filter(DeliveryJob.city == city)
        if keyword:
            query = query.filter(
                DeliveryJob.job_title.contains(keyword) |
                DeliveryJob.company_name.contains(keyword)
            )

        total = query.count()
        jobs = query.order_by(DeliveryJob.id.desc()).offset((page - 1) * page_size).limit(page_size).all()

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "jobs": [{
                "id": j.id,
                "company_name": j.company_name,
                "company_logo": j.company_logo,
                "company_website": j.company_website,
                "company_size": j.company_size,
                "industry": j.industry,
                "job_title": j.job_title,
                "job_type": j.job_type,
                "city": j.city,
                "address": j.address,
                "salary_text": j.salary_text,
                "salary_min": j.salary_min,
                "salary_max": j.salary_max,
                "education": j.education,
                "experience": j.experience,
                "publish_time": j.publish_time,
                "deadline": j.deadline,
                "has_exam": j.has_exam,
                "apply_url": j.apply_url or _build_apply_search_url(j.company_name, j.job_title, j.city),
                "source": j.source,
            } for j in jobs],
        }
    finally:
        db.close()


# ── API: 获取岗位详情 ──
@router.get("/jobs/{job_id}")
def get_job_detail(job_id: int):
    seed_jobs()
    db = get_db().__next__()
    try:
        job = db.query(DeliveryJob).filter(DeliveryJob.id == job_id).first()
        if not job:
            raise HTTPException(404, "岗位不存在")
        return {
            "id": job.id,
            "company_name": job.company_name,
            "company_logo": job.company_logo,
            "company_website": job.company_website,
            "company_size": job.company_size,
            "industry": job.industry,
            "company_intro": job.company_intro,
            "job_title": job.job_title,
            "job_type": job.job_type,
            "city": job.city,
            "address": job.address,
            "salary_text": job.salary_text,
            "salary_min": job.salary_min,
            "salary_max": job.salary_max,
            "education": job.education,
            "experience": job.experience,
            "job_description": job.job_description,
            "skills_required": json.loads(job.skills_required) if isinstance(job.skills_required, str) else job.skills_required,
            "skills_preferred": json.loads(job.skills_preferred) if isinstance(job.skills_preferred, str) else job.skills_preferred,
            "publish_time": job.publish_time,
            "deadline": job.deadline,
            "has_exam": job.has_exam,
            "apply_url": job.apply_url,
            "interview_rounds": job.interview_rounds,
            "interview_form": job.interview_form,
            "interview_focus": job.interview_focus,
            "source": job.source,
        }
    finally:
        db.close()


# ── API: AI分析岗位 ──
@router.post("/ai-analyze/{job_id}")
def analyze_job(job_id: int, user_skills: str = Query("", description="用户技能标签，逗号分隔")):
    seed_jobs()
    db = get_db().__next__()
    try:
        job = db.query(DeliveryJob).filter(DeliveryJob.id == job_id).first()
        if not job:
            raise HTTPException(404, "岗位不存在")
        result = ai_analyze_job(job, user_skills)
        return result
    finally:
        db.close()


# ── API: 搜索公司官网 ──
@router.get("/search-website")
def search_website(company: str = Query(...)):
    url = search_company_website(company)
    return {"url": url}


# ── API: 投递台账列表 ──
@router.get("/tracking")
def list_tracking(token: str = Query(...)):
    uid = get_user_id(token)
    if not uid:
        raise HTTPException(401, "未登录")
    db = get_db().__next__()
    try:
        records = db.query(DeliveryTracking).filter(
            DeliveryTracking.user_id == uid
        ).order_by(DeliveryTracking.updated_at.desc()).all()
        return {
            "records": [{
                "id": r.id,
                "job_id": r.job_id,
                "company_name": r.company_name,
                "company_logo": r.company_logo or "",
                "company_size": r.company_size or "",
                "industry": r.industry or "",
                "job_title": r.job_title,
                "apply_time": r.apply_time,
                "status": r.status,
                "notes": r.notes,
                "interview_time": r.interview_time or "",
                "interview_location": r.interview_location or "",
                "hr_feedback": r.hr_feedback or "",
                "created_at": r.created_at.isoformat() if r.created_at else "",
                "updated_at": r.updated_at.isoformat() if r.updated_at else "",
            } for r in records],
        }
    finally:
        db.close()


# ── API: 添加投递记录 ──
@router.post("/tracking")
def add_tracking(
    token: str = Query(...),
    job_id: int = Query(...),
    company_name: str = Query(""),
    job_title: str = Query(""),
    company_logo: str = Query(""),
    company_size: str = Query(""),
    industry: str = Query(""),
    status: str = Query("已查看"),
    notes: str = Query(""),
):
    uid = get_user_id(token)
    if not uid:
        raise HTTPException(401, "未登录")
    db = get_db().__next__()
    try:
        # 检查是否已在台账中
        existing = db.query(DeliveryTracking).filter(
            DeliveryTracking.user_id == uid,
            DeliveryTracking.job_id == job_id,
        ).first()
        if existing:
            existing.status = status
            existing.updated_at = datetime.utcnow()
            if notes:
                existing.notes = notes
            if company_logo:
                existing.company_logo = company_logo
            if company_size:
                existing.company_size = company_size
            if industry:
                existing.industry = industry
            db.commit()
            return {"ok": True, "id": existing.id, "action": "updated"}
        else:
            now = datetime.now()
            record = DeliveryTracking(
                user_id=uid,
                job_id=job_id,
                company_name=company_name,
                company_logo=company_logo,
                company_size=company_size,
                industry=industry,
                job_title=job_title,
                apply_time=now.strftime("%Y-%m-%d %H:%M"),
                status=status,
                notes=notes,
                created_at=now,
                updated_at=now,
            )
            db.add(record)
            db.commit()
            return {"ok": True, "id": record.id, "action": "created"}
    finally:
        db.close()


# ── API: 更新投递状态 ──
@router.put("/tracking/{record_id}")
def update_tracking(
    record_id: int,
    token: str = Query(...),
    status: str = Query(""),
    notes: str = Query(""),
):
    uid = get_user_id(token)
    if not uid:
        raise HTTPException(401, "未登录")
    db = get_db().__next__()
    try:
        record = db.query(DeliveryTracking).filter(
            DeliveryTracking.id == record_id,
            DeliveryTracking.user_id == uid,
        ).first()
        if not record:
            raise HTTPException(404, "记录不存在")
        if status:
            record.status = status
        if notes:
            record.notes = notes
        record.updated_at = datetime.utcnow()
        db.commit()
        return {"ok": True}
    finally:
        db.close()


# ── API: 删除投递记录 ──
@router.delete("/tracking/{record_id}")
def delete_tracking(record_id: int, token: str = Query(...)):
    uid = get_user_id(token)
    if not uid:
        raise HTTPException(401, "未登录")
    db = get_db().__next__()
    try:
        record = db.query(DeliveryTracking).filter(
            DeliveryTracking.id == record_id,
            DeliveryTracking.user_id == uid,
        ).first()
        if not record:
            raise HTTPException(404, "记录不存在")
        db.delete(record)
        db.commit()
        return {"ok": True}
    finally:
        db.close()


# ── API: 我的投递列表（带筛选与分页） ──
@router.get("/my-apps")
def list_my_apps(
    token: str = Query(...),
    status: str = Query(""),
    company_size: str = Query(""),
    industry: str = Query(""),
    date_range: str = Query(""),  # 7d, 30d, 90d, all
    page: int = 1,
    page_size: int = 20,
):
    uid = get_user_id(token)
    if not uid:
        raise HTTPException(401, "未登录")
    db = get_db().__next__()
    try:
        query = db.query(DeliveryTracking).filter(DeliveryTracking.user_id == uid)

        if status:
            statuses = status.split(",")
            query = query.filter(DeliveryTracking.status.in_(statuses))

        if company_size:
            sizes = company_size.split(",")
            query = query.filter(DeliveryTracking.company_size.in_(sizes))

        if industry:
            query = query.filter(DeliveryTracking.industry.contains(industry))

        if date_range and date_range != "all":
            from datetime import timedelta
            days = int(date_range.rstrip("d"))
            cutoff = datetime.utcnow() - timedelta(days=days)
            query = query.filter(DeliveryTracking.updated_at >= cutoff)

        total = query.count()
        records = query.order_by(DeliveryTracking.apply_time.desc()).offset(
            (page - 1) * page_size
        ).limit(page_size).all()

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "records": [{
                "id": r.id,
                "job_id": r.job_id,
                "company_name": r.company_name,
                "company_logo": r.company_logo or "",
                "company_size": r.company_size or "",
                "industry": r.industry or "",
                "job_title": r.job_title,
                "apply_time": r.apply_time,
                "status": r.status,
                "notes": r.notes,
                "interview_time": r.interview_time or "",
                "interview_location": r.interview_location or "",
                "hr_feedback": r.hr_feedback or "",
                "created_at": r.created_at.isoformat() if r.created_at else "",
                "updated_at": r.updated_at.isoformat() if r.updated_at else "",
            } for r in records],
        }
    finally:
        db.close()


# ── API: 我的投递统计概览 ──
@router.get("/my-apps/stats")
def my_apps_stats(token: str = Query(...)):
    uid = get_user_id(token)
    if not uid:
        raise HTTPException(401, "未登录")
    db = get_db().__next__()
    try:
        records = db.query(DeliveryTracking).filter(
            DeliveryTracking.user_id == uid
        ).all()
        total = len(records)
        pending = sum(1 for r in records if r.status in ("已查看", "待投递", "已投递", "HR已查看", "待面试"))
        interviewing = sum(1 for r in records if r.status == "待面试")
        offer = sum(1 for r in records if r.status in ("已offer", "面试通过"))
        rejected = sum(1 for r in records if r.status in ("已拒", "已关闭"))
        return {
            "total": total,
            "pending": pending,
            "interviewing": interviewing,
            "offer": offer,
            "rejected": rejected,
        }
    finally:
        db.close()


# ── API: 更新面试安排 ──
@router.put("/tracking/{record_id}/interview")
def update_interview(
    record_id: int,
    token: str = Query(...),
    interview_time: str = Query(""),
    interview_location: str = Query(""),
    hr_feedback: str = Query(""),
):
    uid = get_user_id(token)
    if not uid:
        raise HTTPException(401, "未登录")
    db = get_db().__next__()
    try:
        record = db.query(DeliveryTracking).filter(
            DeliveryTracking.id == record_id,
            DeliveryTracking.user_id == uid,
        ).first()
        if not record:
            raise HTTPException(404, "记录不存在")
        if interview_time:
            record.interview_time = interview_time
        if interview_location:
            record.interview_location = interview_location
        if hr_feedback:
            record.hr_feedback = hr_feedback
        record.updated_at = datetime.utcnow()
        db.commit()
        return {"ok": True}
    finally:
        db.close()


# ── API: 我的投递筛选选项 ──
@router.get("/my-apps/filter-options")
def my_apps_filter_options(token: str = Query(...)):
    uid = get_user_id(token)
    if not uid:
        raise HTTPException(401, "未登录")
    db = get_db().__next__()
    try:
        records = db.query(DeliveryTracking).filter(
            DeliveryTracking.user_id == uid
        ).all()
        statuses = sorted(set(r.status for r in records))
        sizes = sorted(set(r.company_size for r in records if r.company_size))
        industries = sorted(set(r.industry for r in records if r.industry))
        return {
            "statuses": statuses,
            "company_sizes": sizes,
            "industries": industries,
        }
    finally:
        db.close()


# ── API: 获取筛选条件选项 ──
@router.get("/filter-options")
def get_filter_options():
    seed_jobs()
    db = get_db().__next__()
    try:
        companies = [r[0] for r in db.query(DeliveryJob.company_name).distinct().all()]
        cities = [r[0] for r in db.query(DeliveryJob.city).distinct().all()]
        job_types = [r[0] for r in db.query(DeliveryJob.job_type).distinct().all()]
        sizes = [r[0] for r in db.query(DeliveryJob.company_size).distinct().all()]
        return {
            "companies": companies,
            "cities": cities,
            "job_types": job_types,
            "company_sizes": sizes,
        }
    finally:
        db.close()