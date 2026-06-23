"""给 111 账号填充数据"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent / ".env")

from database import SessionLocal
from models import User, Profile, LearningNode, LearningNote, LearningResource
import json

db = SessionLocal()
try:
    user = db.query(User).filter(User.username == "111").first()
    if not user:
        print("❌ 用户 111 不存在")
        exit()
    
    uid = user.id
    print(f"✅ 找到用户 111 (id={uid})")
    
    # 填充资料
    profile = db.query(Profile).filter(Profile.user_id == uid).first()
    if not profile:
        profile = Profile(user_id=uid)
        db.add(profile)
    
    profile.nickname = "同学"
    profile.grade = "大一"
    profile.education = "本科"
    profile.major_category = "计算机类"
    profile.major = "计算机科学与技术"
    profile.school = "郑州西亚斯学院"
    profile.city = "郑州"
    profile.interests = json.dumps(["前端开发", "后端开发", "AI应用"])
    profile.confusion = "对职业方向比较迷茫，不确定该学什么技术"
    profile.skills = "Python, HTML, CSS, JavaScript基础"
    profile.target_job = "前端开发工程师"
    profile.target_city = "郑州"
    profile.expected_salary = "8K-12K"
    print("✅ 用户资料已填充")
    
    # 填充学习笔记（给每个已有节点加笔记）
    nodes = db.query(LearningNode).all()
    count = 0
    for node in nodes:
        exists = db.query(LearningNote).filter(
            LearningNote.user_id == uid,
            LearningNote.node_id == node.id
        ).first()
        if not exists:
            note = LearningNote(
                user_id=uid,
                node_id=node.id,
                title=f"{node.title} 学习笔记",
                content=f"学习{node.title}的笔记：\n1. 理解了核心概念\n2. 完成了基础练习\n3. 可以应用到实际项目中"
            )
            db.add(note)
            count += 1
    print(f"✅ 已添加 {count} 条学习笔记")
    
    db.commit()
    print(f"\n🎉 用户 111 数据填充完成！")
    print(f"   资料已填，{count}条学习笔记已添加")
    
except Exception as e:
    db.rollback()
    print(f"❌ 错误: {e}")
finally:
    db.close()
