from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from database import engine, Base
from routers import career, interview, resume, job_match, user, exam, bilibili, delivery, assistant
import json
import os

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

DEBUG_LOG_PATH = 'debug_logs.jsonl'

@app.post('/api/debug-log')
async def debug_log(request: Request):
    body = await request.json()
    with open(DEBUG_LOG_PATH, 'a') as f:
        f.write(json.dumps(body, ensure_ascii=False) + '\n')
    return JSONResponse({'ok': True})

@app.get('/api/debug-logs')
async def get_debug_logs():
    if not os.path.exists(DEBUG_LOG_PATH):
        return {'logs': []}
    with open(DEBUG_LOG_PATH, 'r') as f:
        lines = [json.loads(l) for l in f if l.strip()]
    return {'logs': lines[-20:]}

@app.delete('/api/debug-logs')
async def clear_debug_logs():
    if os.path.exists(DEBUG_LOG_PATH):
        os.remove(DEBUG_LOG_PATH)
    return {'ok': True}

# 注册路由
app.include_router(career.router)
app.include_router(interview.router)
app.include_router(resume.router)
app.include_router(job_match.router)
app.include_router(user.router)
app.include_router(exam.router)
app.include_router(bilibili.router)
app.include_router(delivery.router)
app.include_router(assistant.router)

@app.get("/")
def root():
    return {"status": "ok", "message": "多模态模拟面试评测智能体 API 已启动"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)