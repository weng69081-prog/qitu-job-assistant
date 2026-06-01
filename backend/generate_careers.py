"""用 MiMo 批量生成各专业补充职业数据"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from routers.llm import chat

CATEGORIES = [
    ("机电土木类", "机械工程/电气工程/自动化/土木工程/车辆工程/测控技术/能源动力"),
    ("经管财会类", "金融学/会计学/工商管理/市场营销/人力资源管理/国际贸易/电子商务/物流管理"),
    ("文法艺术类", "法学/新闻学/汉语言文学/广告学/视觉传达/环境设计/广播电视编导"),
    ("医药护理类", "临床医学/护理学/药学/医学检验/康复治疗/口腔医学/中医学"),
    ("教育师范类", "教育学/学前教育/小学教育/汉语言文学(师范)/数学(师范)/英语(师范)/教育技术"),
    ("农林类", "农学/园艺/植物保护/动物科学/林学/水产养殖/食品科学与工程/农业资源"),
    ("轻工制造类", "食品科学与工程/纺织工程/印刷工程/包装工程/轻化工程/材料科学与工程"),
]

for cat_name, sub_majors in CATEGORIES:
    print(f"\n=== {cat_name} ===")
    prompt = f"""你是一名职业规划专家。请为「{cat_name}」专业（包含{sub_majors}等子专业）推荐8-10个最适合的对口职业。

请返回JSON数组（不要markdown代码块）：
[
  {{
    "career": "职业名称",
    "match": 匹配度0-100,
    "difficulty": "初级"/"中级"/"高级",
    "salary": "薪资范围如8K-20K",
    "responsibilities": ["职责1", "职责2", "职责3", "职责4"],
    "hard_requirements": ["硬性要求1", "硬性要求2", "硬性要求3"],
    "soft_requirements": ["软性要求1", "软性要求2", "软性要求3"],
    "growth_path": ["初级(1-2年,XK-YK)→描述", "中级(2-4年,XK-YK)→描述", "高级(4年+,XK-YK)→描述"],
    "trend": "行业趋势一句话（30字内）"
  }}
]

要求：
- 职业要涵盖不同方向（技术、管理、市场等）
- 薪资和成长路径符合真实市场水平
- 职责和要求要专业、具体
- 只返回JSON，不要其他文字"""
    
    text = chat(prompt, system="你是专业的职业规划师，熟悉各类专业的就业方向和市场行情。", max_tokens=3000)
    try:
        text = text.strip()
        if text.startswith("```"): 
            lines = text.split("\n", 1)
            text = lines[1] if len(lines) > 1 else text
            if text.endswith("```"): text = text[:-3]
        data = json.loads(text)
        print(f"  生成了 {len(data)} 个职业")
        for c in data:
            print(f"  - {c['career']} (匹配度{c['match']}, {c['difficulty']})")
        # Save to JSON file
        out = f"/Users/wendao/interview-agent/backend/data/career_{cat_name}.json"
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  已保存到 {out}")
    except Exception as e:
        print(f"  ❌ 解析失败: {e}")
        print(f"  返回内容: {text[:200]}")