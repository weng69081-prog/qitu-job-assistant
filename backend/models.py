from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
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


class User(Base):
    """统一用户表（原 data/users.db → 合并到 interview.db）"""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    nickname = Column(String(100), default="")
    avatar = Column(String(500), default="")
    created_at = Column(DateTime, default=datetime.utcnow)


class Profile(Base):
    """用户画像表"""
    __tablename__ = "profiles"
    user_id = Column(Integer, primary_key=True)
    education = Column(String(50), default="本科")
    city = Column(String(100), default="北京")
    skills = Column(String(500), default="")
    salary = Column(String(50), default="8K-12K")
    major_category = Column(String(100), default="")
    major = Column(String(100), default="")
    job_targets = Column(String(500), default="")
    gender = Column(String(10), default="")
    age = Column(Integer, default=22)
    experience = Column(String(500), default="")
    certificate = Column(String(500), default="")
    interests = Column(String(500), default="")
    confusion = Column(String(500), default="")
    grade = Column(String(50), default="大一")
    updated_at = Column(DateTime, default=datetime.utcnow)


class ResumeHistory(Base):
    """简历历史记录"""
    __tablename__ = "resume_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, default=0)
    template_id = Column(String(50), default="classic")
    template_name = Column(String(100), default="")
    career = Column(String(100), default="")
    name = Column(String(100), default="")
    form_data = Column(Text, default="{}")
    generated_text = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)


class InterviewConversation(Base):
    """持久化的对话式面试会话（替代内存 _conv_store）"""
    __tablename__ = "interview_conversations"
    session_id = Column(String(50), primary_key=True)
    job = Column(String(200), default="")
    category = Column(String(100), default="")
    mode = Column(String(20), default="basic")
    system_prompt = Column(Text, default="")
    # JSON: [{"role":"assistant","content":"..."},{"role":"user","content":"..."}]
    messages_json = Column(Text, default="[]")
    # JSON: ["问题1","问题2",...]
    questions_json = Column(Text, default="[]")
    started_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)


class UserSession(Base):
    """持久化用户会话，避免后端重启导致登录失效"""
    __tablename__ = "user_sessions"
    token = Column(String(128), primary_key=True)
    user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# ════════════════════════════════════════════
# 学习中心 & 小橘 新表
# ════════════════════════════════════════════

class WeaknessItem(Base):
    """薄弱知识点（从面试/笔试报告自动提取）"""
    __tablename__ = "weakness_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, default=0)
    name = Column(String(200), default="")            # 知识点名称
    score = Column(Float, default=0.0)                 # 当前掌握度 0-100
    category = Column(String(50), default="interview") # interview/exam
    source = Column(String(100), default="")           # 来源描述
    career = Column(String(100), default="")           # 关联岗位
    detected_count = Column(Integer, default=1)        # 被检测到次数
    mastered = Column(Integer, default=0)              # 0未掌握 1已掌握 2已忽略
    created_at = Column(DateTime, default=datetime.utcnow)


class LearningPath(Base):
    """AI生成的学习路线"""
    __tablename__ = "learning_paths"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, default=0)
    career = Column(String(100), default="")           # 目标岗位
    title = Column(String(200), default="")            # 路线标题
    description = Column(Text, default="")             # 路线描述
    difficulty = Column(String(20), default="beginner") # beginner/intermediate/advanced
    total_nodes = Column(Integer, default=0)
    progress = Column(Float, default=0.0)              # 完成进度 0-100
    is_active = Column(Integer, default=1)             # 是否当前路线
    created_at = Column(DateTime, default=datetime.utcnow)


class LearningNode(Base):
    """学习路线中的节点（可分目录和子节点）"""
    __tablename__ = "learning_nodes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    path_id = Column(Integer, default=0)               # 关联路线ID
    parent_id = Column(Integer, default=0)              # 父节点ID(0=目录节点)
    user_id = Column(Integer, default=0)
    title = Column(String(200), default="")
    description = Column(Text, default="")
    order_index = Column(Integer, default=0)           # 排序
    duration = Column(String(50), default="")           # 预计耗时
    difficulty = Column(String(20), default="medium")
    status = Column(String(20), default="pending")      # pending/in_progress/completed
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class LearningResource(Base):
    """节点下的学习资源"""
    __tablename__ = "learning_resources"
    id = Column(Integer, primary_key=True, autoincrement=True)
    node_id = Column(Integer, default=0)               # 关联节点ID
    user_id = Column(Integer, default=0)
    title = Column(String(200), default="")
    resource_type = Column(String(30), default="article") # article/video/exercise/note
    url = Column(String(500), default="")
    content = Column(Text, default="")
    duration = Column(String(50), default="")
    is_done = Column(Integer, default=0)               # 是否已完成
    created_at = Column(DateTime, default=datetime.utcnow)


class LearningNote(Base):
    """学习笔记"""
    __tablename__ = "learning_notes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, default=0)
    node_id = Column(Integer, default=0)               # 关联节点ID
    resource_id = Column(Integer, default=0)            # 关联资源ID
    title = Column(String(200), default="")
    content = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)


class ReviewSchedule(Base):
    """复习提醒"""
    __tablename__ = "review_schedules"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, default=0)
    weakness_id = Column(Integer, default=0)            # 关联薄弱点ID
    title = Column(String(200), default="")
    review_interval = Column(Integer, default=1)       # 间隔天数
    next_review_at = Column(String(50), default="")    # 下次复习时间
    reviewed_count = Column(Integer, default=0)         # 已复习次数
    last_reviewed_at = Column(String(50), default="")
    created_at = Column(DateTime, default=datetime.utcnow)


class SmartResume(Base):
    """智能简历数据（画像→自动生成简历内容）"""
    __tablename__ = "smart_resumes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, default=0)
    career = Column(String(100), default="")
    summary = Column(Text, default="")                 # AI生成个人总结
    skills_text = Column(Text, default="")             # AI推荐技能清单
    experience_text = Column(Text, default="")         # AI优化经历描述
    education_text = Column(Text, default="")
    match_score = Column(Float, default=0.0)            # 岗位匹配度
    created_at = Column(DateTime, default=datetime.utcnow)


class XiaoJuSession(Base):
    """小橘会话（每知识点独立）"""
    __tablename__ = "xiaoju_sessions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, default=0)
    node_id = Column(Integer, default=0)               # 关联节点ID（0=通用会话）
    topic = Column(String(200), default="")            # 会话主题
    context_summary = Column(Text, default="")         # AI压缩摘要（超过15轮后）
    message_count = Column(Integer, default=0)
    is_archived = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class XiaoJuMessage(Base):
    """小橘消息"""
    __tablename__ = "xiaoju_messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, default=0)             # 关联会话ID
    role = Column(String(10), default="user")           # user/assistant
    content = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)


class XiaoJuMemory(Base):
    """小橘持久记忆（跨会话保存的关键信息）"""
    __tablename__ = "xiaoju_memories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, default=0)
    key = Column(String(100), default="")              # 记忆键名
    value = Column(Text, default="")                    # 记忆内容
    memory_type = Column(String(30), default="user_info") # user_info/preference/learning
    created_at = Column(DateTime, default=datetime.utcnow)