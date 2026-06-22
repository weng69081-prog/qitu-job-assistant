"""插入新职业数据到 career.py"""
import json, re
from pathlib import Path

data_dir = Path("/Users/wendao/interview-agent/backend/data")
career_py = Path("/Users/wendao/interview-agent/backend/routers/career.py")
content = career_py.read_text("utf-8")
lines = content.split("\n")

# 读取所有生成的数据
all_new = {}
for f in sorted(data_dir.glob("career_*.json")):
    cat_name = f.name.replace("career_", "").replace(".json", "")
    with open(f, "r", encoding="utf-8") as fh:
        careers = json.load(fh)
    all_new[cat_name] = careers

def clean_career(c):
    """规范化职业数据"""
    # 确保 match 是数字
    if isinstance(c.get("match"), str):
        m = re.search(r"(\d+)", c["match"])
        c["match"] = int(m.group(1)) if m else 85
    
    # 标准化 difficulty
    d = c.get("difficulty", "初级")
    if "初级" in d or "初" in d: d = "初级"
    elif "中级" in d or "中等" in d or "中" in d: d = "中级"
    elif "高级" in d or "高" in d: d = "高级"
    else: d = "初级"
    c["difficulty"] = d
    
    # 标准化 salary - 确保用 K 格式
    sal = c.get("salary", "8K-20K")
    # 如果是 8-15k/月 格式，转成 8K-15K
    sal = sal.replace("k", "K").replace("k/月", "K").replace("/月", "")
    if not "K" in sal:
        sal = "8K-20K"
    c["salary"] = sal
    
    # 确保 growth_path 是数组
    gp = c.get("growth_path", [])
    if isinstance(gp, list):
        c["growth_path"] = gp
    else:
        c["growth_path"] = ["初级(1-2年)→基础阶段", "中级(2-4年)→独立负责", "高级(4年+)→专家"]
    
    # 确保 trend 存在
    if not c.get("trend"):
        c["trend"] = "行业需求稳定增长"
    
    return c

def fmt_career(c):
    """格式化为单行紧凑JSON"""
    clean_career(c)
    return json.dumps(c, ensure_ascii=False, separators=(",", ":"))

# 定义每类的插入位置（行号，0-indexed）
# 行 157, 161, 165, 170, 175, 179, 183, 187
cat_positions = [
    ("计算机类", 156),  # 在 ], 之前一行
    ("机电土木类", 160),
    ("经管财会类", 164),
    ("文法艺术类", 169),
    ("医药护理类", 174),
    ("教育师范类", 178),
    ("农林类", 182),
    ("轻工制造类", 186),
]

# 从后往前插入（避免行号变动影响）
cat_positions.reverse()

for cat_name, insert_line in cat_positions:
    if cat_name not in all_new or not all_new[cat_name]:
        continue
    
    entries = [fmt_career(c) for c in all_new[cat_name]]
    insert_text = ",\n        ".join(entries) + ","
    
    # 在 insert_line 之后插入
    # 即：在最后一条职业条目后面，加入新条目 + 逗号
    lines[insert_line] = "        " + insert_text + "\n" + lines[insert_line]
    print(f"✅ {cat_name}: 在行 {insert_line+1} 前插入 {len(entries)} 个新职业")

# 写入文件
career_py.write_text("\n".join(lines), "utf-8")
print(f"\n✅ 已写入 {career_py}")