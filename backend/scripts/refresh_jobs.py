"""定时刷新投递岗位数据 - 每周自动生成一批真实岗位"""
import sys, json, os, urllib.request
from pathlib import Path

# 切换到后端目录
os.chdir(str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, ".")

from models import DeliveryJob
from database import SessionLocal

API_KEY = os.getenv("LLM_API_KEY", "sk-cuftttewiw9g8ffl58xxsmcrr6nb6yxfjst4bby8hel4c9kn")
BASE_URL = os.getenv("LLM_BASE_URL", "https://api.xiaomimimo.com/v1")
MODEL = os.getenv("LLM_MODEL", "mimo-v2-flash")

BATCH_SIZE = 3

ALL_COMPANIES = {
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
    "拼多多": "https://careers.pinduoduo.com/",
    "科大讯飞": "https://recruit.iflytek.com/",
    "比亚迪": "https://job.byd.com/",
    "OPPO": "https://careers.oppo.com/",
    "招商银行": "https://career.cmbchina.com/",
    "海康威视": "https://www.hikvision.com/cn/recruit/",
    "蔚来": "https://nio.jobs.feishu.cn/",
    "理想汽车": "https://www.lixiang.com/join",
}

def chat(prompt, max_tokens=3000):
    messages = [{"role": "user", "content": prompt}]
    body = json.dumps({
        "model": MODEL, "messages": messages,
        "temperature": 0.7, "max_tokens": max_tokens, "stream": False,
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/chat/completions", data=body,
        headers={"api-key": API_KEY, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read())["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[ERROR] LLM call failed: {e}")
        return ""

def generate_batch(companies_dict):
    company_list = "\n".join(f"- {name} （招聘页: {url}）" for name, url in companies_dict.items())
    prompt = f"""你是一个招聘数据专家。请为以下{len(companies_dict)}家真实企业各生成2个正在招聘的校招/实习岗位信息。
注意：岗位必须是这些企业真正会招的，用真实技能要求，薪资范围合理，apply_url用企业真实招聘页链接。
{company_list}
返回JSON数组，只返回JSON，不要markdown：
[{{"company_name":"公司名","company_logo":"https://img.icons8.com/color/48/xxx.png","company_website":"https://www.xxx.com","company_size":"巨头/大型/中型","industry":"行业","company_intro":"简介","job_title":"岗位名","job_type":"技术/产品/运营/设计","city":"北京","address":"地址","salary_min":8000,"salary_max":15000,"salary_text":"8K-15K","education":"本科","experience":"应届","job_description":"职责","skills_required":["Python","SQL"],"skills_preferred":["Docker"],"apply_url":"真实招聘页URL","interview_rounds":"2-3轮","interview_form":"线上面试","interview_focus":"面试重点","has_exam":true或false}}]"""

    result = chat(prompt)
    if not result:
        return 0
    if result.startswith("```"):
        result = result.split("\n",1)[1].rsplit("```",1)[0].strip()
        if result.startswith("json"):
            result = result[4:].strip()
    try:
        data = json.loads(result)
        if isinstance(data, dict) and "jobs" in data:
            data = data["jobs"]
        if not isinstance(data, list):
            return 0
        db = SessionLocal()
        count = 0
        for j in data:
            job = DeliveryJob(
                company_name=j.get("company_name",""),
                company_logo=j.get("company_logo",""),
                company_website=j.get("company_website",""),
                company_size=j.get("company_size","中型"),
                industry=j.get("industry",""),
                company_intro=j.get("company_intro",""),
                job_title=j.get("job_title",""),
                job_type=j.get("job_type","技术"),
                city=j.get("city","北京"),
                address=j.get("address",""),
                salary_min=j.get("salary_min",8000),
                salary_max=j.get("salary_max",15000),
                salary_text=j.get("salary_text",""),
                education=j.get("education","本科"),
                experience=j.get("experience","应届"),
                job_description=j.get("job_description",""),
                skills_required=json.dumps(j.get("skills_required",[]), ensure_ascii=False),
                skills_preferred=json.dumps(j.get("skills_preferred",[]), ensure_ascii=False),
                publish_time="2026-06-23",
                deadline="2026-08-23",
                has_exam=1 if j.get("has_exam", False) else 0,
                apply_url=j.get("apply_url",""),
                interview_rounds=j.get("interview_rounds","2-3轮"),
                interview_form=j.get("interview_form","线上面试"),
                interview_focus=j.get("interview_focus",""),
                career_category="",
                source="ai_generated",
            )
            db.add(job)
            count += 1
        db.commit()
        db.close()
        return count
    except (json.JSONDecodeError, Exception) as e:
        print(f"[ERROR] Parse failed: {e}")
        return 0

def main():
    db = SessionLocal()
    # 保留20条旧数据，清掉多余的
    all_jobs = db.query(DeliveryJob).order_by(DeliveryJob.id.desc()).all()
    keep_count = 20
    if len(all_jobs) > keep_count:
        ids_to_del = [j.id for j in all_jobs[keep_count:]]
        db.query(DeliveryJob).filter(DeliveryJob.id.in_(ids_to_del)).delete(synchronize_session=False)
        db.commit()
        print(f"清除了 {len(ids_to_del)} 条旧数据，保留 {keep_count} 条")
    db.close()

    items = list(ALL_COMPANIES.items())
    total = 0
    for i in range(0, len(items), BATCH_SIZE):
        batch = dict(items[i:i+BATCH_SIZE])
        count = generate_batch(batch)
        total += count
        print(f"批次 {i//BATCH_SIZE + 1}: {count} 条")

    print(f"\n总计生成: {total} 条")

if __name__ == "__main__":
    main()
