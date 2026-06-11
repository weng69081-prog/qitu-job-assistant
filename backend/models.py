from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from database import Base
from datetime import datetime

class InterviewSession(Base):
    __tablename__ = "interview_sessions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    job = Column(String(100), default="")
    category = Column(String(50), default="")
    mode = Column(String(20), default="basic")
    total_questions = Column(Integer, default=3)
    average_score = Column(Float, default=0.0)
    highest_score = Column(Float, default=0.0)
    lowest_score = Column(Float, default=0.0)
    # JSON: [{"score":75,"dimensions":{...}}]
    answers_json = Column(Text, default="[]")
    # JSON: {"语言表达":78,...}
    dimensions_json = Column(Text, default="{}")
    # JSON: ["优点1","优点2"]
    strengths_json = Column(Text, default="[]")
    weaknesses_json = Column(Text, default="[]")
    suggestions_json = Column(Text, default="[]")
    # JSON: [{"emotion":"自信","confidence":85,"details":{...},"time":...}]
    emotions_json = Column(Text, default="[]")
    created_at = Column(DateTime, default=datetime.utcnow)


class ExamQuestion(Base):
    __tablename__ = "exam_questions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(100), default="")  # 岗位分类
    knowledge_point = Column(String(200), default="")  # 知识点
    career = Column(String(100), default="")  # 适用岗位
    difficulty = Column(String(20), default="medium")  # easy/medium/hard
    question_type = Column(String(20), default="single")  # single(单选)/multi(多选)/judge(判断)
    question = Column(Text, default="")
    options_json = Column(Text, default="[]")  # JSON: [{"label":"A","text":"..."},...]
    answer = Column(String(100), default="")  # e.g. "A" or "A,B" or "对"
    analysis = Column(Text, default="")  # 答案解析
    source = Column(String(50), default="")  # 来源: 行测/专业/综合
    created_at = Column(DateTime, default=datetime.utcnow)


class WrongQuestion(Base):
    __tablename__ = "wrong_questions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, default=0)  # 关联题目ID
    question_type = Column(String(20), default="exam")  # exam(笔试) / interview(面试)
    career = Column(String(100), default="")  # 关联岗位
    # 如果是笔试错题，存原题信息
    category = Column(String(100), default="")
    difficulty = Column(String(20), default="medium")
    question = Column(Text, default="")
    user_answer = Column(Text, default="")  # 用户作答
    correct_answer = Column(Text, default="")  # 正确答案
    options_json = Column(Text, default="[]")  # 原题选项
    analysis = Column(Text, default="")  # 解析
    source = Column(String(50), default="")  # 来源
    wrong_count = Column(Integer, default=1)  # 错了几次
    last_wrong_at = Column(DateTime, default=datetime.utcnow)
    mastered = Column(Integer, default=0)  # 0未掌握 1已掌握
    created_at = Column(DateTime, default=datetime.utcnow)


class SavedQuestion(Base):
    __tablename__ = "saved_questions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, default=0)
    question_type = Column(String(20), default="exam")  # exam(笔试) / interview(面试)
    career = Column(String(100), default="")  # 关联岗位
    category = Column(String(100), default="")
    difficulty = Column(String(20), default="medium")
    question = Column(Text, default="")
    options_json = Column(Text, default="[]")  # 如果是面试题则为空
    source = Column(String(50), default="")
    note = Column(String(500), default="")  # 收藏备注
    created_at = Column(DateTime, default=datetime.utcnow)


class ExamRecord(Base):
    __tablename__ = "exam_records"
    id = Column(Integer, primary_key=True, autoincrement=True)
    career = Column(String(100), default="")  # 目标岗位
    mode = Column(String(50), default="专项练习")  # 专项练习/模拟卷/错题重练
    total_questions = Column(Integer, default=0)
    correct_count = Column(Integer, default=0)
    wrong_count = Column(Integer, default=0)
    accuracy = Column(Float, default=0.0)  # 正确率百分比
    duration_seconds = Column(Integer, default=0)  # 总用时(秒)
    # JSON: [{"id":1,"answer":"A","correct":true},...]
    answers_json = Column(Text, default="[]")
    # JSON: {"薄弱知识点":[{"name":"JS原型链","wrong":1,"total":2},...]}
    knowledge_json = Column(Text, default="{}")
    created_at = Column(DateTime, default=datetime.utcnow)


class DeliveryJob(Base):
    """仿真岗位数据"""
    __tablename__ = "delivery_jobs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(100), default="")
    company_logo = Column(String(500), default="")
    company_website = Column(String(500), default="")
    company_size = Column(String(20), default="中型")
    industry = Column(String(100), default="")
    company_intro = Column(Text, default="")
    job_title = Column(String(200), default="")
    job_type = Column(String(50), default="")
    city = Column(String(50), default="")
    address = Column(String(300), default="")
    salary_min = Column(Integer, default=0)
    salary_max = Column(Integer, default=0)
    salary_text = Column(String(50), default="")
    education = Column(String(20), default="本科")
    experience = Column(String(50), default="")
    job_description = Column(Text, default="")
    skills_required = Column(Text, default="[]")
    skills_preferred = Column(Text, default="[]")
    publish_time = Column(String(50), default="")
    deadline = Column(String(50), default="")
    has_exam = Column(Integer, default=0)
    apply_url = Column(String(500), default="")
    interview_rounds = Column(String(100), default="3轮")
    interview_form = Column(String(100), default="线上面试")
    interview_focus = Column(String(500), default="")
    career_category = Column(String(100), default="")
    source = Column(String(20), default="simulated")
    created_at = Column(DateTime, default=datetime.utcnow)


class DeliveryTracking(Base):
    """用户投递台账"""
    __tablename__ = "delivery_tracking"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, default=0)
    job_id = Column(Integer, default=0)
    company_name = Column(String(100), default="")
    company_logo = Column(String(500), default="")
    company_size = Column(String(20), default="")
    industry = Column(String(100), default="")
    job_title = Column(String(200), default="")
    apply_time = Column(String(50), default="")
    status = Column(String(20), default="已查看")
    notes = Column(String(500), default="")
    interview_time = Column(String(100), default="")
    interview_location = Column(String(300), default="")
    hr_feedback = Column(String(500), default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class UserSession(Base):
    """持久化用户会话，避免后端重启导致登录失效"""
    __tablename__ = "user_sessions"
    token = Column(String(128), primary_key=True)
    user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)