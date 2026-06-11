"""LLM 调用工具 —— 通过 Xiaomi MiMo API 生成自然语言内容"""
import os, json
from pathlib import Path

# 优先从 backend/.env 加载
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

API_KEY = os.getenv("LLM_API_KEY", "")
BASE_URL = os.getenv("LLM_BASE_URL", "https://api.siliconflow.cn/v1")
MODEL = os.getenv("LLM_MODEL", "Qwen/Qwen3-32B")

import urllib.request

def chat(prompt: str, system: str = "", temperature: float = 0.7, max_tokens: int = 800,
         model: str = "", base_url: str = "", api_key: str = "") -> str:
    """调 LLM Chat API，返回生成文本。失败返回空字符串。
    
    支持覆盖 model/base_url/api_key，不传则用默认配置。
    满足各模块不同模型需求（面试用默认、投递用 MiMo 等）。
    """
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    use_model = model or MODEL
    use_url = base_url or BASE_URL
    use_key = api_key or API_KEY

    body = json.dumps({
        "model": use_model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{use_url}/chat/completions",
        data=body,
        headers={
            "api-key": use_key,
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        import traceback
        err = f"[LLM] 调用失败: {e}\n{traceback.format_exc()}"
        with open("/tmp/llm_error.log", "w") as f:
            f.write(err)
        return ""


def generate_career_analysis(career_name: str, context: dict) -> dict:
    """生成职业分析文案"""
    prompt = f"""你是职业规划专家。请为「{career_name}」生成分析，返回JSON格式（不要markdown代码块）。

用户背景：专业={context.get('major','未知')}，学历={context.get('education','本科')}，城市={context.get('city','北京')}

返回JSON结构（只返回JSON，不要其他文字）：
{{
  "summary": "一句话概述这个职业（20字以内）",
  "suitable_reason": "为什么适合这个专业的学生（30字以内）",
  "daily_work": "日常工作做什么（40字以内）",
  "growth_path": ["初级→1-3年达到什么", "中级→3-5年达到什么", "高级→5年+达到什么"]
}}"""
    text = chat(prompt, system="你是一个务实、接地气的职业规划专家，回答简洁有力，不虚不空。")
    try:
        # 清理可能的 markdown 包裹
        text = text.strip()
        if text.startswith("```"): 
            text = text.split("\n", 1)[1]
            if text.endswith("```"): text = text[:-3]
        return json.loads(text)
    except:
        return {"summary": f"适合{context.get('major','相关专业')}学生考虑的优质职业方向", "suitable_reason": "", "daily_work": "", "growth_path": []}


def generate_company_match_analysis(career: str, company: str, city: str, match_score: int, skill_gaps: list) -> str:
    """生成投递分析的自然语言建议"""
    gaps_text = "、".join(skill_gaps) if skill_gaps else "无"
    prompt = f"""你是求职顾问。用户想投「{company}」的「{career}」岗位，在城市「{city}」，匹配度{match_score}%，技能缺口：{gaps_text}。

请给一句30字以内的投递建议，格式：
- 高匹配(≥80%)：「放心投，你的背景很匹配，建议...」
- 中匹配(50-79%)：「可以冲，但建议先补...」
- 低匹配(<50%)：「当练手，重点看看...」"""
    return chat(prompt, max_tokens=150)


def generate_resume_content(career: str, context: dict) -> dict:
    """生成简历内容建议"""
    prompt = f"""你是资深HR。请为用户生成「{career}」岗位的简历优化建议，返回JSON：

{{
  "self_intro": "一段自我评价模板（40字）",
  "skill_highlights": ["关键技能1", "关键技能2", "关键技能3"],
  "project_tips": ["项目经历写法建议1", "项目经历写法建议2"]
}}

用户背景：学历={context.get('education','本科')}，技能={context.get('skills','')}，城市={context.get('city','')}"""
    text = chat(prompt, system="你是资深HR，写简历建议简洁实用。只返回JSON。")
    try:
        text = text.strip()
        if text.startswith("```"): 
            text = text.split("\n", 1)[1]
            if text.endswith("```"): text = text[:-3]
        return json.loads(text)
    except:
        return {"self_intro": "", "skill_highlights": [], "project_tips": []}


def analyze_emotion(image_base64: str) -> dict:
    """通过 MiMo omni 分析面部表情"""
    import httpx
    payload = {
        "model": "mimo-v2-omni",
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": "请分析这张人脸的面部表情和情绪状态。返回JSON格式：{\"emotion\":\"主情绪\",\"confidence\":0-100,\"details\":{\"开心\":0-100,\"紧张\":0-100,\"自信\":0-100,\"困惑\":0-100,\"平静\":0-100,\"焦虑\":0-100},\"description\":\"一句话描述\"}"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
            ]
        }],
        "max_tokens": 500,
        "temperature": 0.3
    }
    try:
        resp = httpx.post(f"{BASE_URL}/chat/completions", json=payload, headers={"api-key": API_KEY, "Content-Type": "application/json"}, timeout=30)
        resp.raise_for_status()
        text = resp.json()["choices"][0]["message"]["content"]
        import re
        m = re.search(r'\{.*\}', text, re.DOTALL)
        if m:
            return json.loads(m.group())
        return {"emotion": "未知", "confidence": 0, "details": {}, "description": "分析返回格式异常"}
    except Exception as e:
        return {"emotion": "未知", "confidence": 0, "details": {}, "description": f"分析异常: {str(e)[:60]}"}


def chat_messages(messages: list, system: str = "", max_tokens: int = 1024, temperature: float = 0.7) -> str:
    """发送完整消息列表到 MiMo（支持多轮对话）"""
    full_messages = []
    if system:
        full_messages.append({"role": "system", "content": system})
    full_messages.extend(messages)

    body = json.dumps({
        "model": MODEL,
        "messages": full_messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{BASE_URL}/chat/completions",
        data=body,
        headers={"api-key": API_KEY, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        import traceback
        with open("/tmp/llm_error.log", "w") as f:
            f.write(f"[chat_messages] 调用失败: {e}\n{traceback.format_exc()}")
        return ""


# ── 异步版本（供 exam.py 等 async 路由复用） ──
import httpx

async def async_chat(prompt: str, system: str = "", temperature: float = 0.7, max_tokens: int = 800,
                     model: str = "", base_url: str = "", api_key: str = "") -> str:
    """异步调 LLM API。支持模型/URL/Key覆盖，不传则用默认配置。"""
    use_model = model or MODEL
    use_url = base_url or BASE_URL
    use_key = api_key or API_KEY

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": use_model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                f"{use_url}/chat/completions",
                headers={"api-key": use_key, "Content-Type": "application/json"},
                json=payload
            )
            if resp.status_code != 200:
                return ""
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return ""