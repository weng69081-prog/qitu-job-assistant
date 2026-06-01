"""Bilibili 视频搜索代理 — 为职业探索页提供职业入门学习视频"""
from fastapi import APIRouter, Query
import httpx, json, re
from routers.llm import chat

router = APIRouter(prefix="/api/bilibili", tags=["B站视频"])

# ═══════════════════════════════════════
# 职业关键词映射 — 让搜索更精准
# ═══════════════════════════════════════
SEARCH_KEYWORDS = {
    "前端开发工程师": "前端开发工程师 入门 职业",
    "后端开发工程师": "后端开发 入门 职业",
    "软件测试工程师": "软件测试 入门 职业",
    "数据分析师": "数据分析 入门 职业",
    "产品经理": "产品经理 入门 职业",
    "网络安全工程师": "网络安全 入门 职业",
    "云计算工程师": "云计算 入门 职业",
    "嵌入式系统开发工程师": "嵌入式开发 入门 职业",
    "游戏开发工程师": "游戏开发 入门 职业",
    "区块链开发工程师": "区块链 入门 职业",
    "新媒体运营": "新媒体运营 入门 职业",
    "平面设计师": "平面设计 入门 职业",
    "法务专员": "法务 职业 入门",
    "律师": "律师 职业 入门",
    "临床医生": "临床医学 职业 入门",
    "护理师": "护理学 职业 入门",
    "药剂师": "药学 职业 入门",
    "中小学教师": "教师资格证 职业 入门",
    "培训讲师": "培训讲师 职业 入门",
    "机械设计工程师": "机械设计 入门 职业",
    "电气工程师": "电气工程 入门 职业",
    "自动化控制工程师": "自动化 入门 职业",
    "土木工程师": "土木工程 职业 入门",
    "车辆工程师": "车辆工程 职业 入门",
    "工业设计师": "工业设计 入门 职业",
    "财务分析师": "财务分析 入门 职业",
    "市场营销专员": "市场营销 入门 职业",
    "会计": "会计 职业 入门",
    "人力资源管理师": "人力资源 入门 职业",
    "电子商务运营": "电子商务 职业 入门",
    "农业技术员": "农学 职业 入门",
    "食品研发工程师": "食品科学 职业 入门",
    "材料工程师": "材料科学 入门 职业",
    "广告策划": "广告策划 入门 职业",
    "内容编辑": "内容编辑 职业 入门",
    "视觉设计师": "视觉设计 入门 职业",
    "法务": "法务 职业 入门",
    "金融投资顾问": "金融 职业 入门",
    "国际贸易专员": "国际贸易 职业 入门",
    "麻醉医生": "麻醉 职业 入门",
    "口腔医生": "口腔医学 职业 入门",
    "中医师": "中医 职业 入门",
    "康复治疗师": "康复治疗 职业 入门",
    "医药代表": "医药代表 职业 入门",
    "医疗器械研发工程师": "医疗器械 入门 职业",
    "高校辅导员": "高校辅导员 职业 入门",
    "教育产品经理": "教育产品 入门 职业",
    "教育技术": "教育技术 入门 职业",
    "学前教育": "学前教育 职业 入门",
    "特殊教育": "特殊教育 入门 职业",
    "园艺设计师": "园艺 职业 入门",
    "动物营养师": "动物科学 入门 职业",
    "水产养殖": "水产养殖 职业 入门",
    "包装工程师": "包装工程 入门 职业",
    "家具设计师": "家具设计 入门 职业",
    "日化产品研发": "日化产品 入门 职业",
    "食品工艺工程师": "食品工艺 入门 职业",
    "印刷工艺": "印刷工艺 入门 职业",
    "机器人工程师": "机器人 入门 职业",
    "智能制造工程师": "智能制造 入门 职业",
    "大数据工程师": "大数据 入门 职业",
    "运维工程师": "运维 入门 职业",
    "实施工程师": "实施工程师 入门 职业",
    "售前工程师": "售前 工程师 入门 职业",
    "项目管理": "项目管理 入门 职业",
    "采购专员": "采购 职业 入门",
    "供应链专员": "供应链 入门 职业",
    "物流专员": "物流 职业 入门",
    "银行柜员": "银行 职业 入门",
    "保险专员": "保险 职业 入门",
    "建筑设计师": "建筑设计 入门 职业",
    "室内设计师": "室内设计 入门 职业",
}

# 大类级别的搜索关键词
CATEGORY_KEYWORDS = {
    "计算机类": "计算机专业 职业规划 入门",
    "机电土木类": "工科 职业规划 入门",
    "经管财会类": "经管专业 职业规划 入门",
    "文法艺术类": "文科 职业规划 入门",
    "医药护理类": "医学 职业 入门",
    "教育师范类": "师范 职业 入门",
    "农林类": "农林 专业 职业 入门",
    "轻工制造类": "轻工 制造 入门 职业",
}


def _search_bilibili(keyword: str, sort: str = "hot", page: int = 1) -> list:
    """通过 B 站搜索 API 获取视频列表"""
    try:
        order = {"hot": "", "new": "pubdate"}.get(sort, "")
        url = "https://api.bilibili.com/x/web-interface/search/all/v2"
        params = {"search_type": "video", "keyword": keyword, "page": page}
        if order:
            params["order"] = order

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://search.bilibili.com/",
        }

        with httpx.Client(timeout=10) as client:
            resp = client.get(url, params=params, headers=headers)
            if resp.status_code != 200:
                return []
            data = resp.json()
            if data.get("code") != 0:
                return []

            # 新版B站API返回结构: result[] 里有多个result_type组，video组才是视频
            raw_results = data.get("data", {}).get("result", [])
            videos = []
            for group in raw_results:
                if group.get("result_type") != "video":
                    continue
                for item in group.get("data", [])[:6]:
                    video = {
                        "title": item.get("title", ""),
                        "bvid": item.get("bvid", ""),
                        "author": item.get("author", ""),
                        "description": item.get("description", ""),
                        "pic": item.get("pic", ""),
                        "play": item.get("play", 0),
                        "danmaku": item.get("video_review", 0),
                        "duration": str(item.get("duration", "")),
                        "url": f"https://www.bilibili.com/video/{item.get('bvid', '')}",
                    }
                    if video["bvid"]:
                        videos.append(video)
            return videos
    except Exception as e:
        print(f"[B站搜索] 请求出错: {e}")
        return []


def _generate_videos_with_mimo(career_name: str, major_category: str = "") -> list:
    """用 MiMo 生成职业推荐视频（作为 B 站搜索的备选）"""
    prompt = f'''你是一名职业规划UP主。请为想成为「{career_name}」的大一新生，推荐4-5个B站上真实存在的入门级学习/科普视频。

要求：
- 视频类型包括：职业介绍类（岗位工作内容、发展路径）、入门科普类（零基础入门讲解）、行业前景类
- 每个视频需给出：标题、UP主名称、简介（一句话说明视频能学到什么）

请返回JSON数组（不要markdown代码）：
[
  {{
    "title": "视频标题",
    "author": "UP主名称",
    "description": "一句话简介，20字内",
    "keyword": "推荐B站搜索关键词"
  }}
]

只返回JSON，不要其他文字。'''

    text = chat(prompt, system="你是懂B站内容的职业教育博主", max_tokens=1200)
    try:
        text = text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            if text.endswith("```"):
                text = text[:-3]
        items = json.loads(text)
        if isinstance(items, list):
            for item in items:
                kw = item.get("keyword", career_name)
                item["url"] = f"https://search.bilibili.com/all?keyword={kw} 入门"
                item["pic"] = ""
                item["bvid"] = ""
                item["play"] = 0
                item["danmaku"] = 0
                item["duration"] = ""
            return items
    except:
        pass
    return []


@router.get("/search")
def search_videos(
    career: str = Query(...),
    major_category: str = Query(""),
    sort: str = Query("hot"),
):
    """搜索某个职业的B站入门学习视频"""
    # 先尝试B站API搜索
    keyword = SEARCH_KEYWORDS.get(career, f"{career} 入门 职业")
    videos = _search_bilibili(keyword, sort)

    # 如果没搜到，换大类关键词再试
    if not videos and major_category:
        cat_kw = CATEGORY_KEYWORDS.get(major_category, "")
        if cat_kw:
            videos = _search_bilibili(cat_kw, sort)

    # 还是没搜到，用 MiMo 生成
    if not videos:
        videos = _generate_videos_with_mimo(career, major_category)

    return {"career": career, "videos": videos[:6]}


@router.get("/batch")
def batch_search(
    careers: str = Query(...),
    major_category: str = Query(""),
):
    """批量获取多个职业的视频（首页一次加载多个）"""
    names = [c.strip() for c in careers.split(",") if c.strip()][:3]
    result = {}
    for name in names:
        result[name] = search_videos(career=name, major_category=major_category)
    return {"videos": result}


@router.get("/keyword-search")
def keyword_search(
    keyword: str = Query(...),
    sort: str = Query("hot"),
):
    """按自定义关键词搜索B站视频（用于路线阶段视频推荐）"""
    videos = _search_bilibili(keyword, sort)
    return {"keyword": keyword, "videos": videos[:4]}