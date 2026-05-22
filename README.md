# 多模态模拟面试评测智能体

面向高校学生的求职全流程智能工具。

## 模块

- 🔍 **职业探索** — 专业+兴趣 → AI推荐职业路径
- 🎤 **面试模拟** — 讯飞API多模态评测（核心）
- 📝 **简历优化** — 上传/生成 → AI润色
- 📊 **投递分析** — JD匹配 + 公司推荐

## 启动

### 后端
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 前端
```bash
cd frontend
npm install
npm run dev
```

## 技术栈

- 前端：Vue 3 + Vue Router + Vite
- 后端：Python FastAPI
- 数据库：SQLite
- AI：讯飞星火大模型