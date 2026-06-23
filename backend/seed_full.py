"""全量数据填充脚本：设置信息 + 学习中心内容 + 更多数据"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent / ".env")

import json
import hashlib
import secrets
from datetime import datetime
from database import engine, Base, SessionLocal

# 建表
print("📦 创建数据库表...")
Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    from models import User, Profile, LearningPath, LearningNode, LearningResource, LearningNote
    
    # 1. 创建/更新 demo 用户
    user = db.query(User).filter(User.username == "demo").first()
    if not user:
        user = User(username="demo", password=hashlib.sha256("demo".encode()).hexdigest())
        db.add(user)
        db.flush()
    
    # 2. 填充用户资料
    profile = db.query(Profile).filter(Profile.user_id == user.id).first()
    if not profile:
        profile = Profile(user_id=user.id)
        db.add(profile)
    
    profile.nickname = "怡嫚"
    profile.grade = "大一"
    profile.education = "本科"
    profile.major_category = "计算机类"
    profile.major = "计算机科学与技术"
    profile.school = "郑州西亚斯学院"
    profile.city = "郑州"
    profile.interests = json.dumps(["前端开发", "后端开发", "AI应用", "全栈开发"])
    profile.confusion = "对全栈开发的技术栈选择有困惑，不确定应该深入Java还是Python后端"
    profile.skills = "C语言, Python, Vue.js, FastAPI, JavaScript, HTML/CSS, Git"
    profile.target_job = "全栈开发工程师（偏后端）"
    profile.target_city = "郑州、武汉、杭州"
    profile.expected_salary = "8K-15K"
    profile.bio = "郑州西亚斯学院计算机科学与技术专业大一学生，正在从零构建启途AI求职教育平台。"
    print(f"✅ 用户资料已填充: {profile.nickname}")
    
    # 3. 填充学习路线内容
    paths = db.query(LearningPath).all()
    for path in paths:
        nodes = db.query(LearningNode).filter(LearningNode.path_id == path.id).all()
        if nodes:
            for node in nodes:
                # 给每个节点添加学习资源
                existing = db.query(LearningResource).filter(LearningResource.node_id == node.id).first()
                if not existing:
                    resources = [
                        LearningResource(
                            node_id=node.id,
                            title=f"{node.title} 入门教程",
                            url=f"https://www.bilibili.com/search?keyword={node.title}",
                            resource_type="video",
                            content=f"适合{path.title}方向的{node.title}入门学习视频"
                        ),
                        LearningResource(
                            node_id=node.id,
                            title=f"{node.title} 实战项目",
                            url="#",
                            resource_type="article",
                            content=f"通过实战项目掌握{node.title}"
                        ),
                    ]
                    for r in resources:
                        db.add(r)
                # 给每个节点添加笔记示例
                existing_note = db.query(LearningNote).filter(
                    LearningNote.node_id == node.id,
                    LearningNote.user_id == user.id
                ).first()
                if not existing_note and node.description:
                    note = LearningNote(
                        user_id=user.id,
                        node_id=node.id,
                        title=f"{node.title} 学习笔记",
                        content=f"学习{node.title}的笔记：\n1. 理解了核心概念\n2. 完成了基础练习\n3. 可以应用到实际项目中",
                    )
                    db.add(note)
            print(f"  ✅ {path.title}: {len(nodes)}个节点已填充资源+笔记")
    
    # 4. 补充更多学习路线
    extra_paths = [
        {"title": "Java后端开发", "description": "从Java基础到Spring Boot企业级开发", "difficulty": "intermediate", "nodes": [
            ("Java基础语法", "掌握Java核心语法、面向对象编程"),
            ("MySQL数据库", "SQL语句、表设计、索引优化"),
            ("Spring Boot", "REST API开发、依赖注入、自动配置"),
            ("MyBatis/JPA", "ORM框架使用、数据库操作"),
            ("Redis缓存", "缓存策略、分布式锁"),
            ("Docker部署", "容器化部署、Docker Compose"),
        ]},
        {"title": "AI应用开发", "description": "掌握大模型API调用与AI应用构建", "difficulty": "intermediate", "nodes": [
            ("Python基础", "Python语法、数据结构、常用库"),
            ("LLM API调用", "OpenAI/MiMo API调用、Prompt工程"),
            ("RAG应用构建", "向量数据库、文档检索、知识库"),
            ("AI Agent开发", "工具调用、多步推理、Workflow"),
            ("模型微调基础", "LoRA微调、数据集准备"),
        ]},
    ]

    for ep in extra_paths:
        existing = db.query(LearningPath).filter(LearningPath.title == ep["title"]).first()
        if not existing:
            path = LearningPath(
                career=ep["title"],
                title=ep["title"],
                description=ep["description"],
                difficulty=ep["difficulty"],
                total_nodes=len(ep["nodes"]),
                is_active=True,
            )
            db.add(path)
            db.flush()
            
            for i, (n_title, n_desc) in enumerate(ep["nodes"]):
                node = LearningNode(
                    path_id=path.id,
                    title=n_title,
                    description=n_desc,
                    order_index=i + 1,
                    duration="120分钟",
                    difficulty="medium",
                )
                db.add(node)
            print(f"  ➕ 新增学习路线: {ep['title']} ({len(ep['nodes'])}个节点)")
    
    db.commit()
    print("\n🎉 全量数据填充完成！")
    print("   👉 登录账号: demo / demo")
    print("   👉 设置页面已有用户资料")
    print("   👉 学习中心已有完整路+节点+资源+笔记")

except Exception as e:
    db.rollback()
    print(f"❌ 错误: {e}")
    raise
finally:
    db.close()
