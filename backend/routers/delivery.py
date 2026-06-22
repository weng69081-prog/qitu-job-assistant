"""
求职投递助手 API — 岗位数据 + AI分析 + 投递台账 + Agent搜索入口
"""
import json, os, re, requests, random
from datetime import datetime
from urllib.parse import quote_plus
from fastapi import APIRouter, Query, HTTPException, Body
from sqlalchemy.orm import Session
from database import get_db, SessionLocal
from models import DeliveryJob, DeliveryTracking
from routers.user import get_user_id

router = APIRouter(prefix="/api/delivery", tags=["求职投递助手"])

# ── 仿真公司数据集 ──
COMPANIES = [
    {
        "name": "字节跳动",
        "logo": "https://img.icons8.com/color/48/byte.png",
        "website": "https://www.bytedance.com",
        "size": "巨头",
        "industry": "互联网/科技",
        "intro": "字节跳动是全球领先的科技公司，旗下产品包括抖音、今日头条、飞书等，致力于成为最懂创作者的科技公司。"
    },
    {
        "name": "阿里巴巴",
        "logo": "https://img.icons8.com/color/48/alibaba.png",
        "website": "https://www.alibaba.com",
        "size": "巨头",
        "industry": "电子商务/科技",
        "intro": "阿里巴巴集团是全球领先的电子商务和科技公司，业务涵盖电商、云计算、数字媒体与娱乐等领域。"
    },
    {
        "name": "腾讯",
        "logo": "https://img.icons8.com/color/48/tencent.png",
        "website": "https://www.tencent.com",
        "size": "巨头",
        "industry": "互联网/科技",
        "intro": "腾讯是一家世界领先的互联网科技公司，业务覆盖社交、游戏、金融科技、企业服务等多个领域。"
    },
    {
        "name": "美团",
        "logo": "https://img.icons8.com/color/48/meituan.png",
        "website": "https://www.meituan.com",
        "size": "大型",
        "industry": "本地生活/互联网",
        "intro": "美团是中国领先的生活服务电子商务平台，致力于用科技连接消费者和商家，提供优质生活服务。"
    },
    {
        "name": "百度",
        "logo": "https://img.icons8.com/color/48/baidu.png",
        "website": "https://www.baidu.com",
        "size": "大型",
        "industry": "互联网/人工智能",
        "intro": "百度是全球最大的中文搜索引擎，同时深耕人工智能领域，在自动驾驶、智能语音等方面处于行业领先地位。"
    },
    {
        "name": "华为",
        "logo": "https://img.icons8.com/color/48/huawei.png",
        "website": "https://www.huawei.com",
        "size": "巨头",
        "industry": "通信/科技",
        "intro": "华为是全球领先的信息与通信技术解决方案提供商，业务涵盖电信网络、企业网络、终端和云计算。"
    },
    {
        "name": "小米",
        "logo": "https://img.icons8.com/color/48/xiaomi.png",
        "website": "https://www.mi.com",
        "size": "大型",
        "industry": "消费电子/互联网",
        "intro": "小米是一家以智能手机、智能硬件和IoT平台为核心的消费电子及智能制造公司。"
    },
    {
        "name": "网易",
        "logo": "https://img.icons8.com/color/48/netease.png",
        "website": "https://www.163.com",
        "size": "大型",
        "industry": "互联网/游戏",
        "intro": "网易是中国领先的互联网技术公司，业务涵盖游戏、音乐、教育、电商等多个领域。"
    },
    {
        "name": "京东",
        "logo": "https://img.icons8.com/color/48/jd.png",
        "website": "https://www.jd.com",
        "size": "大型",
        "industry": "电子商务/物流",
        "intro": "京东是中国领先的技术驱动型电商公司，以供应链为基础的技术与服务企业。"
    },
    {
        "name": "快手",
        "logo": "https://img.icons8.com/color/48/kuaishou.png",
        "website": "https://www.kuaishou.com",
        "size": "大型",
        "industry": "短视频/社交",
        "intro": "快手是领先的内容社区和社交平台，以短视频和直播为核心，致力于为用户创造更丰富的社交体验。"
    },
]

CITIES = ["北京", "上海", "深圳", "杭州", "广州", "成都", "武汉", "南京", "西安"]
ADDRESSES = {
    "北京": ["海淀区中关村科技园", "朝阳区望京SOHO", "西城区金融街", "海淀区上地信息产业基地", "朝阳区国贸CBD"],
    "上海": ["浦东新区张江高科技园区", "徐汇区漕河泾开发区", "静安区南京西路", "杨浦区五角场", "闵行区虹桥"],
    "深圳": ["南山区科技园", "福田区CBD", "龙岗区坂田", "宝安区前海", "南山区后海"],
    "杭州": ["西湖区文三路", "滨江区物联网小镇", "余杭区未来科技城", "萧山区钱江世纪城"],
    "广州": ["天河区珠江新城", "海珠区琶洲", "番禺区万博", "黄埔区科学城"],
    "成都": ["高新区天府软件园", "武侯区桐梓林", "锦江区春熙路"],
    "武汉": ["东湖高新区光谷", "洪山区街道口", "江汉区建设大道"],
    "南京": ["雨花台区软件谷", "鼓楼区新模范马路", "建邺区河西CBD"],
    "西安": ["高新区锦业路", "雁塔区长安南路", "未央区凤城八路"],
}

SALARIES = [
    (8000, 15000, "8K-15K"), (10000, 18000, "10K-18K"),
    (12000, 25000, "12K-25K"), (15000, 30000, "15K-30K"),
    (18000, 35000, "18K-35K"), (20000, 40000, "20K-40K"),
    (25000, 50000, "25K-50K"), (30000, 60000, "30K-60K"),
]

JOB_TYPES = ["技术", "产品", "运营", "设计", "市场", "职能"]

# 岗位模板
JOB_TEMPLATES = {
    "技术": [
        {
            "title": "后端开发工程师",
            "type": "技术",
            "education": "本科",
            "experience": "应届/1-3年",
            "skills_req": "[\"Java/Python\",\"MySQL\",\"Redis\",\"微服务架构\",\"Git\"]",
            "skills_pref": "[\"Docker\",\"Kubernetes\",\"消息队列\",\"高并发\"]",
            "desc": "负责公司核心业务系统的后端开发与维护，参与系统架构设计与优化，编写高质量代码并保证系统稳定性和可扩展性。",
            "rounds": "3轮",
            "form": "线上面试",
            "focus": "算法与数据结构、系统设计、项目经历深挖、Java/Python基础"
        },
        {
            "title": "前端开发工程师",
            "type": "技术",
            "education": "本科",
            "experience": "应届/1-3年",
            "skills_req": "[\"Vue.js/React\",\"JavaScript/TypeScript\",\"HTML5/CSS3\",\"Webpack/Vite\"]",
            "skills_pref": "[\"Node.js\",\"小程序开发\",\"性能优化\",\"CI/CD\"]",
            "desc": "负责公司Web端产品的前端开发工作，与后端工程师协作完成产品功能迭代，优化用户体验和页面性能。",
            "rounds": "2-3轮",
            "form": "线上面试",
            "focus": "前端基础、框架原理、手写代码、性能优化方案"
        },
        {
            "title": "算法工程师",
            "type": "技术",
            "education": "硕士及以上",
            "experience": "应届/1-3年",
            "skills_req": "[\"Python\",\"深度学习框架\",\"机器学习算法\",\"数据处理\"]",
            "skills_pref": "[\"NLP\",\"计算机视觉\",\"大模型\",\"强化学习\"]",
            "desc": "参与AI算法研发与落地，将机器学习/深度学习技术应用到实际业务场景中，持续优化模型效果。",
            "rounds": "3-4轮",
            "form": "线上面试",
            "focus": "算法推导、模型评估、论文解读、编程能力、数学基础"
        },
        {
            "title": "测试开发工程师",
            "type": "技术",
            "education": "本科",
            "experience": "应届/1-3年",
            "skills_req": "[\"Python/Java\",\"自动化测试框架\",\"Linux\",\"SQL\"]",
            "skills_pref": "[\"性能测试\",\"安全测试\",\"CI/CD\",\"容器化\"]",
            "desc": "负责产品质量保障，开发自动化测试工具和框架，制定测试策略，保证产品高质量交付。",
            "rounds": "2-3轮",
            "form": "线上面试",
            "focus": "测试理论、自动化框架设计、编程能力、问题定位能力"
        },
        {
            "title": "数据工程师",
            "type": "技术",
            "education": "本科",
            "experience": "应届/1-3年",
            "skills_req": "[\"SQL\",\"Python\",\"Hadoop/Spark\",\"数据仓库\"]",
            "skills_pref": "[\"Flink\",\"Kafka\",\"数据治理\",\"流式计算\"]",
            "desc": "负责数据平台建设与维护，设计数据管道，保障数据质量和时效性，为业务分析提供数据基础。",
            "rounds": "2-3轮",
            "form": "线上面试",
            "focus": "SQL优化、数仓建模、数据处理框架、项目经验"
        },
    ],
    "产品": [
        {
            "title": "产品经理",
            "type": "产品",
            "education": "本科",
            "experience": "应届/1-3年",
            "skills_req": "[\"产品设计\",\"用户研究\",\"数据分析\",\"Axure/Figma\"]",
            "skills_pref": "[\"AI产品经验\",\"增长策略\",\"项目管理\",\"技术背景\"]",
            "desc": "负责产品规划与设计，深入理解用户需求，推动产品从需求分析到上线的全流程，持续优化产品体验。",
            "rounds": "3-4轮",
            "form": "线上面试",
            "focus": "产品思维、需求分析、竞品分析、数据分析能力、案例分析"
        },
        {
            "title": "AI产品经理",
            "type": "产品",
            "education": "本科",
            "experience": "应届/1-3年",
            "skills_req": "[\"产品设计\",\"AI基础认知\",\"数据分析\",\"用户调研\"]",
            "skills_pref": "[\"大模型应用\",\"AIGC经验\",\"技术背景\",\"增长思维\"]",
            "desc": "负责AI产品的规划和落地，理解AI技术能力边界，将AI能力转化为可落地的产品方案。",
            "rounds": "3-4轮",
            "form": "线上面试",
            "focus": "AI产品认知、场景化需求分析、技术理解力、案例分析"
        },
    ],
    "运营": [
        {
            "title": "新媒体运营",
            "type": "运营",
            "education": "本科",
            "experience": "应届/1-3年",
            "skills_req": "[\"内容创作\",\"社交媒体运营\",\"数据分析\",\"视频剪辑\"]",
            "skills_pref": "[\"短视频运营\",\"私域流量\",\"KOL合作\",\"社群运营\"]",
            "desc": "负责公司新媒体矩阵的运营，策划优质内容，提升品牌影响力和用户互动。",
            "rounds": "2轮",
            "form": "线上面试",
            "focus": "内容策划、热点敏感度、数据复盘、创意能力"
        },
        {
            "title": "用户运营",
            "type": "运营",
            "education": "本科",
            "experience": "应届/1-3年",
            "skills_req": "[\"用户分析\",\"活动策划\",\"数据分析\",\"文案能力\"]",
            "skills_pref": "[\"增长黑客\",\"用户分群\",\"A/B测试\",\"私域运营\"]",
            "desc": "负责用户增长和留存策略的制定与执行，通过精细化运营提升用户活跃度和转化率。",
            "rounds": "2-3轮",
            "form": "线上面试",
            "focus": "用户分层策略、增长方法论、活动设计、数据分析"
        },
    ],
    "设计": [
        {
            "title": "UI/UX设计师",
            "type": "设计",
            "education": "本科",
            "experience": "应届/1-3年",
            "skills_req": "[\"Figma/Sketch\",\"设计系统\",\"用户研究\",\"交互设计\"]",
            "skills_pref": "[\"动效设计\",\"3D设计\",\"前端基础\",\"品牌设计\"]",
            "desc": "负责产品界面的视觉与交互设计，基于用户研究数据持续优化产品体验，维护设计规范。",
            "rounds": "2-3轮",
            "form": "线上面试",
            "focus": "设计作品集展示、设计思维、交互细节、评审流程"
        },
    ],
    "市场": [
        {
            "title": "市场营销专员",
            "type": "市场",
            "education": "本科",
            "experience": "应届/1-3年",
            "skills_req": "[\"市场调研\",\"活动策划\",\"数据分析\",\"文案撰写\"]",
            "skills_pref": "[\"SEO/SEM\",\"品牌策划\",\"BD谈判\",\"流量投放\"]",
            "desc": "负责市场活动的策划与执行，制定营销策略，提升品牌知名度和市场占有率。",
            "rounds": "2轮",
            "form": "线上面试",
            "focus": "营销案例分析、市场敏感度、策划能力、沟通表达"
        },
    ],
    "职能": [
        {
            "title": "HR专员",
            "type": "职能",
            "education": "本科",
            "experience": "应届/1-3年",
            "skills_req": "[\"招聘流程\",\"员工关系\",\"Excel\",\"沟通能力\"]",
            "skills_pref": "[\"人力资源证书\",\"数据分析\",\"绩效管理\",\"组织发展\"]",
            "desc": "负责公司人才招聘与员工关系维护，参与人力资源体系建设，支持业务团队发展。",
            "rounds": "2-3轮",
            "form": "线上面试",
            "focus": "招聘实务、劳动法规、情景模拟、组织协调"
        },
        {
            "title": "财务助理",
            "type": "职能",
            "education": "本科",
            "experience": "应届/1-3年",
            "skills_req": "[\"财务基础\",\"Excel\",\"会计准则\",\"财务软件\"]",
            "skills_pref": "[\"CPA\",\"审计经验\",\"数据分析\",\"ERP系统\"]",
            "desc": "协助财务团队完成日常账务处理、报表编制和税务申报工作。",
            "rounds": "2轮",
            "form": "线上面试",
            "focus": "财务知识、Excel技能、细心程度、职业素养"
        },
    ],
}

# ── 初始化种子数据 ──
def seed_jobs():
    db = SessionLocal()
    try:
        existing = db.query(DeliveryJob).count()
        if existing > 0:
            return
        import itertools
        job_id = 0
        for company in COMPANIES:
            # 随机选1-3个岗位
            num_jobs = random.randint(1, 3)
            # 随机选岗位类型和技术栈
            job_types = random.sample(list(JOB_TEMPLATES.keys()), min(num_jobs, len(JOB_TEMPLATES)))
            for jt in job_types:
                templates = JOB_TEMPLATES[jt]
                tpl = random.choice(templates)
                city = random.choice(CITIES)
                sal = random.choice(SALARIES)
                addr = random.choice(ADDRESSES[city])
                days_ago = random.randint(1, 30)
                month = random.randint(1, 6)
                day = random.randint(1, 28)
                job_id += 1
                job = DeliveryJob(
                    company_name=company["name"],
                    company_logo=company["logo"],
                    company_website=company["website"],
                    company_size=company["size"],
                    industry=company["industry"],
                    company_intro=company["intro"],
                    job_title=tpl["title"],
                    job_type=tpl["type"],
                    city=city,
                    address=f"{city}{addr}",
                    salary_min=sal[0],
                    salary_max=sal[1],
                    salary_text=sal[2],
                    education=tpl["education"],
                    experience=tpl["experience"],
                    job_description=tpl["desc"],
                    skills_required=tpl["skills_req"],
                    skills_preferred=tpl["skills_pref"],
                    publish_time=f"2026-{month:02d}-{day:02d}",
                    deadline=f"2026-{month+2 if month<=10 else month-10:02d}-{day:02d}",
                    has_exam=random.choice([0, 1]),
                    apply_url=f"{company['website']}/careers/{job_id}",
                    interview_rounds=tpl["rounds"],
                    interview_form=tpl["form"],
                    interview_focus=tpl["focus"],
                    career_category="",
                    source="simulated",
                )
                db.add(job)
        db.commit()
    finally:
        db.close()


from routers.llm import chat as llm_chat

# ── AI 解析（调用小米 MiMo） ──
MIMO_KEY = os.environ.get("MIMO_API_KEY", "")
MIMO_URL = "https://api.xiaomimimo.com/v1"
MIMO_MODEL = "mimo-v2-flash"

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
        content = llm_chat(prompt, temperature=0.3, max_tokens=2000,
                          model=MIMO_MODEL, base_url=MIMO_URL, api_key=MIMO_KEY)
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
    # 兜底：从已知数据库取
    for c in COMPANIES:
        if c["name"] == company_name:
            return c["website"]
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


# ── API: 获取岗位列表 ──
@router.get("/jobs")
def list_jobs(
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