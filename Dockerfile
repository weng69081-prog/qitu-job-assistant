# ═══════════════════════════════════════════
# Stage 1: 构建前端
# ═══════════════════════════════════════════
FROM node:20-alpine AS build
WORKDIR /build/frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ .
RUN npm run build

# ═══════════════════════════════════════════
# Stage 2: 后端运行环境
# ═══════════════════════════════════════════
FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 安装后端依赖
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir uvicorn

# 复制后端代码
COPY backend/ /app/backend/
WORKDIR /app/backend

# 复制前端构建产物
COPY --from=build /build/frontend/dist /app/frontend/dist

# 端口
EXPOSE 8000

# 启动：后端 API + 前端静态文件同时服务
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]