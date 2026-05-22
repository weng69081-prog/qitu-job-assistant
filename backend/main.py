from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import career, interview, resume, job_match

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="多模态模拟面试评测智能体",
    description="面向高校学生的求职全流程智能工具",
    version="1.0.0"
)

# 允许前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(career.router)
app.include_router(interview.router)
app.include_router(resume.router)
app.include_router(job_match.router)

@app.get("/")
def root():
    return {"status": "ok", "message": "多模态模拟面试评测智能体 API 已启动"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)