"""
初始化脚本：创建数据库表 + 填充内置初始数据
在新机器上 clone 项目后，跑一次这个脚本就能用：
    cd backend && python setup.py

不需要再手动复制数据库文件。
"""
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

import json
import hashlib
import secrets
from datetime import datetime
from database import engine, Base, SessionLocal

# ─── 建表 ───
print("📦 创建数据库表...")
Base.metadata.create_all(bind=engine)
print("✅ 表结构已就绪")

# ─── 种子数据 ───
db = SessionLocal()
try:
    # 检查是否已有用户（避免重复初始化）
    from models import User, Profile, LearningPath, LearningNode

    user_count = db.query(User).count()
    if user_count == 0:
        print("👤 创建默认用户...")

        def hash_pw(password: str) -> str:
            salt = secrets.token_hex(8)
            h = hashlib.sha256((password + salt).encode()).hexdigest()
            return f"{h}:{salt}"

        demo = User(
            username="demo",
            password_hash=hash_pw("demo"),
            nickname="小明",
            created_at=datetime.utcnow(),
        )
        db.add(demo)
        db.flush()

        # 默认画像
        prof = Profile(
            user_id=demo.id,
            education="本科",
            major="计算机科学与技术",
            city="北京",
            skills="JavaScript, Vue, Python, Java",
            grade="大一",
            job_targets="前端开发工程师",
        )
        db.add(prof)
        db.commit()
        print(f"✅ 默认用户已创建（账号: demo / 密码: demo）")
    else:
        print(f"👤 已有 {user_count} 个用户，跳过")

    # 检查是否已有内置学习路线
    path_count = db.query(LearningPath).count()
    if path_count == 0:
        print("📚 创建内置学习路线...")

        now = datetime.utcnow()

        builtin_paths = [
            {
                "career": "前端开发工程师",
                "title": "前端开发入门到实战",
                "desc": "从前端基础知识到项目实战的完整学习路径，适合零基础或刚接触前端的同学",
                "difficulty": "beginner",
                "nodes": [
                    ("HTML/CSS基础", "掌握网页结构搭建和样式设计，理解盒模型、Flexbox、Grid布局", "约7天", "easy"),
                    ("JavaScript核心", "理解变量、函数、DOM操作、事件循环、ES6+语法", "约14天", "easy"),
                    ("Vue框架入门", "学习组件化开发、路由、状态管理（Pinia）、组合式API", "约21天", "medium"),
                    ("前端工程化", "Vite、ESLint、Git工作流、包管理", "约10天", "hard"),
                    ("实战项目", "完成一个完整的前端项目，含联调、部署", "约30天", "hard"),
                ]
            },
            {
                "career": "后端开发工程师",
                "title": "后端开发技能树",
                "desc": "从编程基础到后端架构的成长路线，侧重Java/Spring生态",
                "difficulty": "beginner",
                "nodes": [
                    ("Java核心基础", "掌握面向对象、集合框架、IO流、多线程", "约14天", "easy"),
                    ("数据库与SQL", "MySQL基础、JDBC、事务、索引优化", "约10天", "easy"),
                    ("Spring Boot入门", "REST API、依赖注入、数据访问、统一异常处理", "约21天", "medium"),
                    ("中间件与架构", "Redis、消息队列、Docker基础", "约14天", "hard"),
                    ("项目实战", "开发一个完整的后端服务（含认证、CRUD、部署）", "约30天", "hard"),
                ]
            },
            {
                "career": "数据分析师",
                "title": "数据分析入门路线",
                "desc": "从零开始学数据分析，覆盖工具、方法和业务思维",
                "difficulty": "beginner",
                "nodes": [
                    ("Excel与SQL基础", "数据清洗、透视表、SQL查询与聚合", "约7天", "easy"),
                    ("Python数据分析", "Pandas、NumPy、Matplotlib基础", "约14天", "easy"),
                    ("统计学基础", "描述性统计、假设检验、回归分析", "约10天", "medium"),
                    ("可视化与报告", "Tableau/Power BI、数据故事化表达", "约10天", "hard"),
                    ("实战分析项目", "完成一个完整的数据分析报告", "约20天", "hard"),
                ]
            },
        ]

        # 用默认用户的ID（如果没有用户则用0）
        uid = db.query(User).first()
        uid = uid.id if uid else 0

        for bp in builtin_paths:
            path = LearningPath(
                user_id=uid,
                career=bp["career"],
                title=bp["title"],
                description=bp["desc"],
                difficulty=bp["difficulty"],
                total_nodes=len(bp["nodes"]),
                progress=0,
                is_active=1,
                created_at=now,
            )
            db.add(path)
            db.flush()

            for idx, nd in enumerate(bp["nodes"]):
                node = LearningNode(
                    path_id=path.id,
                    parent_id=0,
                    user_id=uid,
                    title=nd[0],
                    description=nd[1],
                    order_index=idx,
                    duration=nd[2],
                    difficulty=nd[3],
                    status="pending",
                    created_at=now,
                )
                db.add(node)

        db.commit()
        print(f"✅ {len(builtin_paths)} 条内置学习路线已创建")
    else:
        print(f"📚 已有 {path_count} 条学习路线，跳过")

    print("\n🎉 初始化完成！")
    print("   👉 启动后端:  cd backend && python main.py")
    print("   👉 启动前端:  cd frontend && npm run dev")
    print("   👉 默认登录:  demo / demo")

except Exception as e:
    db.rollback()
    print(f"❌ 初始化失败: {e}")
    raise
finally:
    db.close()
