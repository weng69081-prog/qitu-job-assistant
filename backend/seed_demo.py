"""填充完整演示数据"""
from database import SessionLocal, engine, Base
from models import (
    User, Profile, InterviewSession, ExamRecord, WeaknessItem,
    LearningPath, LearningNode, LearningResource, LearningNote,
    ReviewSchedule, SmartResume
)
from datetime import datetime, timedelta
import json, hashlib, secrets


def hash_pw(password: str, salt: str = "") -> tuple:
    if not salt:
        salt = secrets.token_hex(8)
    h = hashlib.sha256((password + salt).encode()).hexdigest()
    return h, salt


def seed_all():
    """填充全部演示数据"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 清空旧数据
        for t in [LearningNode, LearningResource, LearningNote, ReviewSchedule,
                  SmartResume, WeaknessItem, InterviewSession, ExamRecord]:
            db.query(t).delete()
        db.query(Profile).delete()
        db.query(User).delete()
        db.commit()

        # 1. 创建用户
        h, s = hash_pw("demo")
        user = User(username="demo", password_hash=h + ":" + s, nickname="小明")
        db.add(user)
        db.flush()
        uid = user.id

        # 2. 画像（有数据的）
        prof = Profile(
            user_id=uid, education="本科", major="计算机科学与技术",
            city="北京", skills="Java, Python, JavaScript, SQL, Vue, HTML/CSS",
            grade="大一", job_targets="前端开发工程师",
            experience="学校ACM社团项目开发", interests="Web开发、算法",
        )
        db.add(prof)

        now = datetime.utcnow()

        # 3. 面试记录（3条）
        for i, iv in enumerate([
            {"job": "前端开发", "avg": 72, "weak": ["JavaScript异步编程不熟", "CSS布局不够灵活"]},
            {"job": "Java开发", "avg": 65, "weak": ["Java集合框架理解不深", "多线程编程薄弱"]},
            {"job": "前端开发", "avg": 78, "weak": ["Vue响应式原理不熟", "性能优化经验不足"]},
        ]):
            dims = {"专业知识": 65 + i * 5, "代码能力": 70, "算法思维": 60, "项目经验": 55,
                    "语言表达": 78, "沟通协作": 80, "学习能力": 85, "职业素养": 75}
            s = InterviewSession(
                job=iv["job"], category="计算机类",
                average_score=iv["avg"], highest_score=iv["avg"] + 10, lowest_score=iv["avg"] - 10,
                total_questions=5,
                dimensions_json=json.dumps(dims),
                weaknesses_json=json.dumps(iv["weak"]),
                strengths_json=json.dumps(["学习能力强", "态度积极"]),
                suggestions_json=json.dumps(["多练习项目实战"]),
                answers_json="[]",
                created_at=now - timedelta(days=[5, 3, 1][i]),
            )
            db.add(s)

        # 4. 笔试记录（2条）
        for j, ex in enumerate([
            ("专项练习", 10, 6, 65),
            ("模拟卷", 15, 11, 72),
        ]):
            r = ExamRecord(
                career="前端开发", mode=ex[0],
                total_questions=ex[1], correct_count=ex[2],
                wrong_count=ex[1] - ex[2], accuracy=ex[3],
                duration_seconds=1800, answers_json="[]",
                knowledge_json=json.dumps({}),
                created_at=now - timedelta(days=[4, 2][j]),
            )
            db.add(r)

        # 5. 薄弱点（5条）
        for wk in [
            {"n": "JavaScript异步编程", "sc": 45, "ca": "interview"},
            {"n": "CSS布局", "sc": 50, "ca": "interview"},
            {"n": "Vue响应式原理", "sc": 40, "ca": "interview"},
            {"n": "Java集合框架", "sc": 50, "ca": "exam"},
            {"n": "多线程编程", "sc": 35, "ca": "exam"},
        ]:
            db.add(WeaknessItem(user_id=uid, name=wk["n"], score=wk["sc"],
                               category=wk["ca"], source=wk["ca"], career="前端开发", detected_count=2))

        # 6. 学习路线 + 节点
        path = LearningPath(
            user_id=uid, career="前端开发", title="前端开发入门到实战",
            description="从前端基础知识到项目实战的完整学习路径",
            difficulty="beginner", total_nodes=5, progress=20, is_active=1,
        )
        db.add(path)
        db.flush()

        nodes_data = [
            ("HTML/CSS基础", "掌握网页结构搭建和样式设计", 0, "约7天", "easy"),
            ("JavaScript核心", "理解变量、函数、DOM操作等JS基础", 1, "约14天", "easy"),
            ("Vue框架入门", "学习组件化开发、路由、状态管理", 2, "约21天", "medium"),
            ("前端工程化", "Webpack、Vite、ESLint等工具链", 3, "约10天", "hard"),
            ("实战项目", "完成一个完整的前端项目", 4, "约30天", "hard"),
        ]
        for nd in nodes_data:
            n = LearningNode(
                path_id=path.id, user_id=uid,
                title=nd[0], description=nd[1],
                order_index=nd[2], duration=nd[3], difficulty=nd[4],
                status="completed" if nd[2] < 1 else "in_progress" if nd[2] == 1 else "pending",
                completed_at=now - timedelta(days=10) if nd[2] < 1 else None,
            )
            db.add(n)
            db.flush()

        db.commit()
        print(f"✅ 演示数据填充完成！用户: {user.nickname}")

    except Exception as e:
        db.rollback()
        print(f"❌ 错误: {e}")
    finally:
        db.close()


# 直接运行脚本时执行
if __name__ == "__main__":
    seed_all()
