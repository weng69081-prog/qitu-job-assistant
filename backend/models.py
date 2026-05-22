from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from database import Base
from datetime import datetime

class InterviewRecord(Base):
    __tablename__ = "interview_records"
    id = Column(Integer, primary_key=True, index=True)
    position = Column(String)        # 面试岗位
    question_type = Column(String)   # 题型
    score_tech = Column(Float)       # 技术得分
    score_express = Column(Float)    # 表达得分
    score_emotion = Column(Float)    # 仪态得分
    report = Column(Text)            # 完整报告 JSON
    created_at = Column(DateTime, default=datetime.now)

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(Text)     # 原始简历文本
    optimized_text = Column(Text)    # 优化后简历
    suggestions = Column(Text)       # 修改建议 JSON
    created_at = Column(DateTime, default=datetime.now)