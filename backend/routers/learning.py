"""学习中心模块 — 画像聚合、路线、薄弱点、匹配度"""
from fastapi import APIRouter, Query
from database import SessionLocal
from models import (
    Profile, InterviewSession, ExamRecord, WeaknessItem,
    LearningPath, LearningNode, LearningResource, LearningNote,
    ReviewSchedule, SmartResume,
    XiaoJuSession, XiaoJuMessage, XiaoJuMemory,
)
from routers.llm import chat
import json, random
from datetime import datetime

router = APIRouter(prefix="/api/learning", tags=["学习中心"])

# ── 帮助函数 ──
def _get_or_default(arr, idx, default=0):
    return arr[idx] if idx < len(arr) else default

def _json_loads(text, default=None):
    try:
        return json.loads(text) if text else default
    except:
        return default

# ═══════════════════════════════════════════
# 1. 画像聚合
# ═══════════════════════════════════════════
@router.get("/profile")
def get_profile(user_id: int = 1):
    """聚合画像：profile基础信息 + 面试/笔试统计 + 薄弱点"""
    db = SessionLocal()
    try:
        prof = db.query(Profile).filter(Profile.user_id == user_id).first()
        # 面试统计
        sessions = db.query(InterviewSession).order_by(InterviewSession.created_at.desc()).limit(20).all()
        exam_total = db.query(ExamRecord).count()
        avg_score = 0
        exam_avg = 0
        if sessions:
            scores = [s.average_score for s in sessions if s.average_score]
            avg_score = round(sum(scores) / len(scores), 1) if scores else 0
        exams = db.query(ExamRecord).all()
        if exams:
            exam_avg = round(sum(e.accuracy for e in exams if e.accuracy) / len(exams), 1) if exams else 0

        # 薄弱点统计
        weaknesses = db.query(WeaknessItem).filter(
            WeaknessItem.user_id == user_id,
            WeaknessItem.mastered == 0
        ).all()
        weak_count = len(weaknesses)
        # 按类别分
        interview_weak = sum(1 for w in weaknesses if w.category == "interview")
        exam_weak = sum(1 for w in weaknesses if w.category == "exam")

        # 8维度估分
        dims = ["专业知识", "代码能力", "算法思维", "项目经验",
                "语言表达", "沟通协作", "学习能力", "职业素养"]
        dim_scores = {}
        for i, d in enumerate(dims):
            base = 60 + i * 5  # 基础分不一样
            if sessions:
                # 取最近面试各维度影响
                latest = sessions[0]
                dims_data = _json_loads(latest.dimensions_json, {})
                if d in dims_data:
                    base = int(dims_data[d])
            # 薄弱点扣分
            penalty = sum(5 for w in weaknesses if d in w.name or w.name in d)
            dim_scores[d] = max(30, min(100, base - penalty))

        return {
            "profile": {
                "education": prof.education if prof else "本科",
                "major": prof.major if prof else "",
                "city": prof.city if prof else "",
                "skills": prof.skills if prof else "",
                "career_targets": prof.job_targets if prof else "",
                "grade": prof.grade if prof else "",
            } if prof else {},
            "stats": {
                "interview_count": len(sessions),
                "exam_count": exam_total,
                "avg_interview_score": avg_score,
                "avg_exam_accuracy": exam_avg,
                "weakness_count": weak_count,
                "interview_weaknesses": interview_weak,
                "exam_weaknesses": exam_weak,
            },
            "dimensions": dim_scores,
        }
    finally:
        db.close()


# ═══════════════════════════════════════════
# 2. 薄弱点列表
# ═══════════════════════════════════════════
@router.get("/weaknesses")
def get_weaknesses(user_id: int = 1, category: str = ""):
    db = SessionLocal()
    try:
        q = db.query(WeaknessItem).filter(WeaknessItem.user_id == user_id)
        if category:
            q = q.filter(WeaknessItem.category == category)
        items = q.order_by(WeaknessItem.score.asc()).all()
        return {
            "items": [
                {
                    "id": w.id,
                    "name": w.name,
                    "score": w.score,
                    "category": w.category,
                    "source": w.source,
                    "career": w.career,
                    "detected_count": w.detected_count,
                    "mastered": w.mastered,
                    "created_at": w.created_at.strftime("%Y-%m-%d %H:%M") if w.created_at else "",
                }
                for w in items
            ]
        }
    finally:
        db.close()


@router.post("/weaknesses/{wid}/master")
def mark_mastered(wid: int):
    db = SessionLocal()
    try:
        w = db.query(WeaknessItem).filter(WeaknessItem.id == wid).first()
        if w:
            w.mastered = 1
            db.commit()
            return {"ok": True}
        return {"ok": False, "error": "not found"}
    finally:
        db.close()


# ═══════════════════════════════════════════
# 3. 学习路线
# ═══════════════════════════════════════════

# ── 内置知识树（AI不可用时的降级） ──
_KB = {
    "前端开发工程师": {
        "title": "前端开发工程师学习路线",
        "description": "从零基础到就业的前端完整知识体系",
        "difficulty": "beginner",
        "nodes": [
            {
                "title": "HTML/CSS 基础", "description": "掌握网页的骨架与样式", "order_index": 0, "duration": "约10天", "difficulty": "easy",
                "children": [
                    {"title": "HTML文档结构", "description": "DOCTYPE、html/head/body骨架", "difficulty": "easy"},
                    {"title": "常用标签与属性", "description": "h1~h6、p、a、img、span、div用法", "difficulty": "easy"},
                    {"title": "列表与表格", "description": "ul/ol有序无序列表、table/tr/td表格", "difficulty": "easy"},
                    {"title": "表单与控件", "description": "form、input各种type、textarea、select", "difficulty": "easy"},
                    {"title": "HTML5语义化标签", "description": "header/nav/main/section/article/ aside", "difficulty": "easy"},
                    {"title": "CSS选择器与优先级", "description": "类/ID/属性/伪类选择器、权重计算", "difficulty": "easy"},
                    {"title": "CSS盒模型", "description": "content/padding/border/margin、box-sizing", "difficulty": "easy"},
                    {"title": "定位与浮动", "description": "relative/absolute/fixed/static、float清除", "difficulty": "easy"},
                    {"title": "Flex弹性布局", "description": "flex容器属性、项目属性、对齐方式", "difficulty": "medium"},
                    {"title": "Grid网格布局", "description": "grid容器、grid项目、网格区域", "difficulty": "medium"},
                ]
            },
            {
                "title": "CSS进阶与预处理器", "description": "响应式、动画与Sass", "order_index": 1, "duration": "约7天", "difficulty": "easy",
                "children": [
                    {"title": "响应式设计", "description": "媒体查询、rem/em/vw/vh单位", "difficulty": "medium"},
                    {"title": "CSS过渡与动画", "description": "transition、@keyframes、animation", "difficulty": "medium"},
                    {"title": "CSS变量与函数", "description": "自定义属性、calc/clamp/min/max", "difficulty": "easy"},
                    {"title": "Sass/SCSS基础", "description": "变量、嵌套、mixin、extends", "difficulty": "medium"},
                    {"title": "移动端适配", "description": "视口设置、rem方案、flexible方案", "difficulty": "medium"},
                    {"title": "图标字体与精灵图", "description": "iconfont、SVG sprites、雪碧图", "difficulty": "easy"},
                ]
            },
            {
                "title": "JavaScript 核心", "description": "从语法到高级特性", "order_index": 2, "duration": "约14天", "difficulty": "medium",
                "children": [
                    {"title": "数据类型与运算符", "description": "基本类型、引用类型、typeof、== vs ===", "difficulty": "easy"},
                    {"title": "作用域与闭包", "description": "全局/函数/块级作用域、闭包应用", "difficulty": "medium"},
                    {"title": "原型链与继承", "description": "prototype、__proto__、原型继承、class", "difficulty": "hard"},
                    {"title": "this指向与call/apply/bind", "description": "this四种绑定规则、硬绑定", "difficulty": "medium"},
                    {"title": "Promise与异步编程", "description": "回调地狱、Promise链、async/await", "difficulty": "hard"},
                    {"title": "ES6+新特性", "description": "解构赋值、箭头函数、模板字符串、模块化", "difficulty": "medium"},
                    {"title": "DOM操作与事件", "description": "增删改查DOM、事件流(冒泡/捕获/委托)", "difficulty": "medium"},
                    {"title": "数组高阶方法", "description": "map/filter/reduce/some/every/find", "difficulty": "medium"},
                    {"title": "正则表达式", "description": "元字符、量词、分组、常用正则", "difficulty": "medium"},
                    {"title": "错误处理与调试", "description": "try-catch-finally、throw、console调试技巧", "difficulty": "easy"},
                ]
            },
            {
                "title": "Vue 3 框架", "description": "响应式组件化开发", "order_index": 3, "duration": "约14天", "difficulty": "medium",
                "children": [
                    {"title": "Vue响应式原理", "description": "ref/reactive、Proxy拦截、依赖收集", "difficulty": "hard"},
                    {"title": "模板语法与指令", "description": "v-bind/v-model/v-if/v-for/v-on", "difficulty": "easy"},
                    {"title": "组件化开发", "description": "组件注册、props/emit、slot插槽", "difficulty": "medium"},
                    {"title": "Composition API", "description": "setup、ref/reactive、computed、watch", "difficulty": "medium"},
                    {"title": "Vue Router路由", "description": "动态路由、路由守卫、懒加载", "difficulty": "medium"},
                    {"title": "Pinia状态管理", "description": "Store定义、actions/getters、持久化", "difficulty": "medium"},
                    {"title": "生命周期与Hook", "description": "onMounted/onUnmounted、keep-alive", "difficulty": "medium"},
                    {"title": "自定义指令与插件", "description": "directive注册、插件封装与发布", "difficulty": "hard"},
                ]
            },
            {
                "title": "TypeScript", "description": "类型系统与工程实践", "order_index": 4, "duration": "约7天", "difficulty": "medium",
                "children": [
                    {"title": "基础类型与接口", "description": "type/interface、联合类型、交叉类型", "difficulty": "easy"},
                    {"title": "泛型编程", "description": "泛型函数/接口/类、约束条件", "difficulty": "medium"},
                    {"title": "类型守卫与断言", "description": "typeof/instanceof、类型断言as", "difficulty": "medium"},
                    {"title": "工具类型", "description": "Partial/Pick/Omit/Record/ReturnType", "difficulty": "hard"},
                    {"title": "TS在Vue中的使用", "description": "defineComponent、类型推导、ref类型", "difficulty": "medium"},
                ]
            },
            {
                "title": "前端工程化", "description": "构建工具与开发规范", "order_index": 5, "duration": "约10天", "difficulty": "hard",
                "children": [
                    {"title": "Vite构建工具", "description": "脚手架、配置、环境变量、HMR热更新", "difficulty": "medium"},
                    {"title": "Git版本管理", "description": "分支策略、冲突解决、PR工作流", "difficulty": "medium"},
                    {"title": "ESLint + Prettier", "description": "代码规范配置、husky、lint-staged", "difficulty": "medium"},
                    {"title": "包管理工具", "description": "npm/yarn/pnpm、依赖管理、workspace", "difficulty": "medium"},
                    {"title": "模块化规范", "description": "ESM/CommonJS/AMD、打包原理", "difficulty": "hard"},
                    {"title": "HTTP与网络", "description": "HTTP状态码、缓存策略、HTTPS、CORS", "difficulty": "medium"},
                    {"title": "性能优化", "description": "懒加载/代码分割/图片优化/首屏加载", "difficulty": "hard"},
                    {"title": "单元测试", "description": "Vitest/Jest、TDD、组件测试", "difficulty": "hard"},
                ]
            },
            {
                "title": "实战项目", "description": "综合项目练习与部署", "order_index": 6, "duration": "约21天", "difficulty": "hard",
                "children": [
                    {"title": "项目架构设计", "description": "目录结构、路由设计、状态管理方案", "difficulty": "hard"},
                    {"title": "API对接与数据请求", "description": "axios封装、请求拦截、错误处理", "difficulty": "medium"},
                    {"title": "权限管理", "description": "路由守卫、角色权限、按钮级别控制", "difficulty": "hard"},
                    {"title": "移动端H5开发", "description": "vant组件库、触屏事件、rem适配", "difficulty": "medium"},
                    {"title": "前端部署", "description": "Nginx配置、CDN、CI/CD流水线", "difficulty": "hard"},
                    {"title": "脚手架搭建", "description": "从零搭建Vue3+TS+Vite项目模板", "difficulty": "hard"},
                ]
            },
        ]
    },
    "Java后端": {
        "title": "Java后端从零到就业",
        "description": "从Java基础到微服务的企业级开发全栈",
        "difficulty": "beginner",
        "nodes": [
            {
                "title": "Java基础核心", "description": "从语法到JVM内存模型", "order_index": 0, "duration": "约14天", "difficulty": "easy",
                "children": [
                    {"title": "数据类型与变量", "description": "8大基本类型、包装类、自动拆装箱", "difficulty": "easy"},
                    {"title": "面向对象三大特性", "description": "封装/继承/多态、super/this、重载重写", "difficulty": "easy"},
                    {"title": "集合框架", "description": "ArrayList vs LinkedList、HashMap原理", "difficulty": "medium"},
                    {"title": "异常处理", "description": "try-catch-finally、受检/非受检异常", "difficulty": "easy"},
                    {"title": "IO流", "description": "字节流/字符流、缓冲流、序列化", "difficulty": "medium"},
                    {"title": "泛型与注解", "description": "泛型擦除、通配符、元注解、自定义注解", "difficulty": "medium"},
                    {"title": "多线程基础", "description": "Thread/Runnable、线程池、synchronized", "difficulty": "hard"},
                    {"title": "JVM内存模型", "description": "堆栈方法区、GC机制、类加载器", "difficulty": "hard"},
                ]
            },
            {
                "title": "数据库与SQL", "description": "MySQL + MyBatis + Redis", "order_index": 1, "duration": "约10天", "difficulty": "medium",
                "children": [
                    {"title": "MySQL基本语法", "description": "CRUD、WHERE、JOIN、GROUP BY、HAVING", "difficulty": "easy"},
                    {"title": "索引原理", "description": "B+树、聚簇索引、最左前缀、慢查询", "difficulty": "hard"},
                    {"title": "事务与锁", "description": "ACID、隔离级别、MVCC、行锁/表锁", "difficulty": "hard"},
                    {"title": "MyBatis框架", "description": "映射配置、动态SQL、缓存、分页", "difficulty": "medium"},
                    {"title": "Redis基础", "description": "5大数据类型、持久化、过期策略", "difficulty": "medium"},
                ]
            },
            {
                "title": "Spring Boot实战", "description": "IoC/AOP/RESTful", "order_index": 2, "duration": "约14天", "difficulty": "medium",
                "children": [
                    {"title": "IoC容器", "description": "Bean生命周期、依赖注入方式", "difficulty": "medium"},
                    {"title": "AOP面向切面", "description": "切点/通知表达式、日志切面实战", "difficulty": "medium"},
                    {"title": "自动配置原理", "description": "@EnableAutoConfiguration、Conditional", "difficulty": "hard"},
                    {"title": "RESTful API", "description": "@RestController、参数校验、统一异常", "difficulty": "medium"},
                    {"title": "拦截器与过滤器", "description": "Interceptor vs Filter、权限拦截", "difficulty": "medium"},
                    {"title": "数据校验与异常", "description": "JSR303校验、全局异常处理器", "difficulty": "medium"},
                ]
            },
            {
                "title": "微服务与中间件", "description": "Spring Cloud + 消息队列", "order_index": 3, "duration": "约14天", "difficulty": "hard",
                "children": [
                    {"title": "Spring Cloud基础", "description": "Nacos注册中心、Gateway网关", "difficulty": "hard"},
                    {"title": "OpenFeign远程调用", "description": "声明式HTTP客户端、负载均衡", "difficulty": "hard"},
                    {"title": "Sentinel限流熔断", "description": "流量控制、熔断降级、热点限流", "difficulty": "hard"},
                    {"title": "RabbitMQ消息队列", "description": "交换机/队列绑定、可靠投递", "difficulty": "hard"},
                    {"title": "Docker容器化", "description": "Dockerfile编写、镜像构建、docker-compose", "difficulty": "medium"},
                ]
            },
            {
                "title": "项目实战", "description": "从零搭建完整后端服务", "order_index": 4, "duration": "约21天", "difficulty": "hard",
                "children": [
                    {"title": "项目架构设计", "description": "分层架构、包结构、模块拆分", "difficulty": "hard"},
                    {"title": "用户认证与授权", "description": "JWT、Spring Security、RBAC权限", "difficulty": "hard"},
                    {"title": "文件上传与处理", "description": "OSS/MinIO、大文件分片上传", "difficulty": "medium"},
                    {"title": "接口文档与测试", "description": "Swagger/Knife4j、Postman测试", "difficulty": "medium"},
                    {"title": "日志与监控", "description": "SLF4J/Logback、ELK、Prometheus", "difficulty": "hard"},
                ]
            },
            {
                "title": "面试冲刺", "description": "高频面试题与系统设计", "order_index": 5, "duration": "约7天", "difficulty": "hard",
                "children": [
                    {"title": "Java基础高频题", "description": "HashMap原理、线程池参数、类加载", "difficulty": "hard"},
                    {"title": "Spring全家桶面试", "description": "IoC/AOP原理、事务失效场景", "difficulty": "hard"},
                    {"title": "MySQL优化面试", "description": "索引失效、慢SQL排查、分库分表", "difficulty": "hard"},
                    {"title": "系统设计", "description": "秒杀系统、短链服务、接口幂等", "difficulty": "hard"},
                ]
            },
        ]
    },
    "算法": {
        "title": "算法与数据结构精进",
        "description": "算法思维训练与LeetCode刷题",
        "difficulty": "intermediate",
        "nodes": [
            {
                "title": "线性表与字符串", "description": "数组、链表、字符串操作", "order_index": 0, "duration": "约7天", "difficulty": "easy",
                "children": [
                    {"title": "数组与双指针", "description": "滑动窗口、三数之和、合并有序数组", "difficulty": "easy"},
                    {"title": "链表操作", "description": "反转链表、快慢指针、环形链表检测", "difficulty": "medium"},
                    {"title": "字符串匹配", "description": "KMP算法、滑动窗口子串、回文串", "difficulty": "medium"},
                    {"title": "栈与队列", "description": "单调栈、优先队列、最小栈", "difficulty": "medium"},
                ]
            },
            {
                "title": "树与图", "description": "二叉树、树的遍历、图论", "order_index": 1, "duration": "约10天", "difficulty": "medium",
                "children": [
                    {"title": "二叉树遍历", "description": "前/中/后序递归与迭代、层序", "difficulty": "easy"},
                    {"title": "二叉搜索树", "description": "BST验证、插入删除、最近公共祖先", "difficulty": "medium"},
                    {"title": "树的序列化", "description": "二叉树序列化反序列化、N叉树", "difficulty": "medium"},
                    {"title": "图的遍历", "description": "DFS/BFS、拓扑排序、并查集", "difficulty": "hard"},
                ]
            },
            {
                "title": "动态规划", "description": "DP思想与经典题型", "order_index": 2, "duration": "约14天", "difficulty": "hard",
                "children": [
                    {"title": "DP基础", "description": "斐波那契、爬楼梯、不同路径", "difficulty": "easy"},
                    {"title": "背包问题", "description": "01背包、完全背包、组合与排列", "difficulty": "hard"},
                    {"title": "区间DP", "description": "回文子串、最长回文子序列", "difficulty": "hard"},
                    {"title": "状态压缩DP", "description": "旅行商问题、位运算状态", "difficulty": "hard"},
                ]
            },
            {
                "title": "排序与查找", "description": "经典排序与二分查找", "order_index": 3, "duration": "约5天", "difficulty": "medium",
                "children": [
                    {"title": "排序算法", "description": "快排/归并/堆排原理与实现", "difficulty": "medium"},
                    {"title": "二分查找", "description": "经典二分、旋转数组、搜索区间", "difficulty": "medium"},
                    {"title": "哈希表", "description": "哈希冲突解决、设计和应用", "difficulty": "medium"},
                ]
            },
            {
                "title": "高频面试150题", "description": "LeetCode热门题精讲", "order_index": 4, "duration": "约21天", "difficulty": "hard",
                "children": [
                    {"title": "数组类高频", "description": "接雨水、最大子序和、合并区间", "difficulty": "hard"},
                    {"title": "字符串类高频", "description": "最长无重复子串、编辑距离", "difficulty": "hard"},
                    {"title": "树类高频", "description": "二叉树最大路径和、层序遍历变体", "difficulty": "hard"},
                    {"title": "设计类", "description": "LRU缓存、LFU缓存、Trie前缀树", "difficulty": "hard"},
                ]
            },
        ]
    },
    "产品经理": {
        "title": "产品经理学习路线",
        "description": "从0到1的产品经理技能体系",
        "difficulty": "beginner",
        "nodes": [
            {
                "title": "产品思维与基础", "description": "什么是产品经理", "order_index": 0, "duration": "约7天", "difficulty": "easy",
                "children": [
                    {"title": "产品经理角色认知", "description": "产品经理职责、能力模型、职业发展", "difficulty": "easy"},
                    {"title": "用户思维", "description": "同理心、用户故事、场景分析", "difficulty": "easy"},
                    {"title": "MVP思维", "description": "最小可行产品、迭代验证、快速试错", "difficulty": "medium"},
                    {"title": "数据思维", "description": "数据驱动决策、指标体系、A/B测试", "difficulty": "medium"},
                ]
            },
            {
                "title": "市场与需求分析", "description": "发现机会、定义需求", "order_index": 1, "duration": "约10天", "difficulty": "medium",
                "children": [
                    {"title": "竞品分析", "description": "竞品选择、功能对比、SWOT分析", "difficulty": "medium"},
                    {"title": "用户调研方法", "description": "访谈法、问卷法、可用性测试", "difficulty": "medium"},
                    {"title": "需求收集与管理", "description": "需求来源、KANO模型、需求优先级", "difficulty": "medium"},
                    {"title": "PRD文档写作", "description": "产品需求文档结构、功能规格说明", "difficulty": "medium"},
                    {"title": "用户画像", "description": "画像维度、Persona构建方法", "difficulty": "easy"},
                ]
            },
            {
                "title": "产品设计", "description": "从原型到交互设计", "order_index": 2, "duration": "约7天", "difficulty": "medium",
                "children": [
                    {"title": "信息架构", "description": "信息层级、导航设计、卡片分类法", "difficulty": "medium"},
                    {"title": "原型设计", "description": "Axure/Figma基础、低保真高保真原型", "difficulty": "medium"},
                    {"title": "交互设计原则", "description": "尼尔森原则、反馈机制、容错设计", "difficulty": "medium"},
                ]
            },
            {
                "title": "项目管理", "description": "推进产品落地", "order_index": 3, "duration": "约7天", "difficulty": "medium",
                "children": [
                    {"title": "敏捷开发", "description": "Scrum框架、Sprint计划、站会", "difficulty": "medium"},
                    {"title": "需求评审", "description": "技术评审、用例评审、验收标准", "difficulty": "medium"},
                    {"title": "跨部门协作", "description": "与设计/开发/测试/运营的协同", "difficulty": "medium"},
                ]
            },
            {
                "title": "数据分析", "description": "用数据驱动产品决策", "order_index": 4, "duration": "约7天", "difficulty": "hard",
                "children": [
                    {"title": "数据指标定义", "description": "DAU/MAU、留存率、转化漏斗", "difficulty": "medium"},
                    {"title": "SQL基础", "description": "数据查询、聚合、报表提取", "difficulty": "medium"},
                    {"title": "Excel数据分析", "description": "透视表、VLOOKUP、可视化图表", "difficulty": "easy"},
                ]
            },
            {
                "title": "产品运营", "description": "产品上线后的持续优化", "order_index": 5, "duration": "约5天", "difficulty": "medium",
                "children": [
                    {"title": "用户增长", "description": "AARRR模型、裂变、渠道投放", "difficulty": "hard"},
                    {"title": "用户反馈管理", "description": "反馈闭环、NPS、满意度调研", "difficulty": "medium"},
                    {"title": "版本迭代管理", "description": "版本规划、发版节奏、灰度发布", "difficulty": "medium"},
                ]
            },
        ]
    },
    "数据分析师": {
        "title": "数据分析师入门到进阶",
        "description": "从0基础到能独立完成数据分析项目",
        "difficulty": "beginner",
        "nodes": [
            {
                "title": "统计学基础", "description": "数据分析的理论基石", "order_index": 0, "duration": "约7天", "difficulty": "easy",
                "children": [
                    {"title": "描述性统计", "description": "均值中位数众数、方差标准差、箱线图", "difficulty": "easy"},
                    {"title": "概率论基础", "description": "条件概率、贝叶斯定理、随机变量", "difficulty": "medium"},
                    {"title": "假设检验", "description": "t检验、卡方检验、p值", "difficulty": "medium"},
                    {"title": "相关系数与回归", "description": "皮尔逊系数、线性回归、残差分析", "difficulty": "medium"},
                ]
            },
            {
                "title": "Excel数据分析", "description": "最常用的分析工具", "order_index": 1, "duration": "约5天", "difficulty": "easy",
                "children": [
                    {"title": "常用函数", "description": "VLOOKUP/SUMIF/COUNTIF/IF嵌套", "difficulty": "easy"},
                    {"title": "数据透视表", "description": "多维汇总、切片器、计算字段", "difficulty": "easy"},
                    {"title": "数据可视化", "description": "条件格式、图表组合、动态图表", "difficulty": "easy"},
                ]
            },
            {
                "title": "SQL数据查询", "description": "从数据库取数的核心技能", "order_index": 2, "duration": "约10天", "difficulty": "medium",
                "children": [
                    {"title": "SQL基础语法", "description": "SELECT/FROM/WHERE/GROUP BY/ORDER BY", "difficulty": "easy"},
                    {"title": "多表连接", "description": "INNER/LEFT/RIGHT JOIN、UNION", "difficulty": "medium"},
                    {"title": "窗口函数", "description": "ROW_NUMBER/RANK/SUM OVER、分区排序", "difficulty": "hard"},
                    {"title": "子查询与CTE", "description": "嵌套查询、公用表表达式、递归查询", "difficulty": "hard"},
                ]
            },
            {
                "title": "Python数据分析", "description": "用Python自动化分析", "order_index": 3, "duration": "约10天", "difficulty": "medium",
                "children": [
                    {"title": "Pandas基础", "description": "DataFrame操作、数据清洗、分组聚合", "difficulty": "medium"},
                    {"title": "NumPy基础", "description": "数组运算、矩阵操作、统计函数", "difficulty": "medium"},
                    {"title": "Matplotlib/Seaborn", "description": "折线图/柱状图/热力图/散点图", "difficulty": "medium"},
                    {"title": "数据清洗实战", "description": "缺失值处理、异常值检测、数据标准化", "difficulty": "medium"},
                ]
            },
            {
                "title": "BI可视化工具", "description": "交互式仪表板制作", "order_index": 4, "duration": "约7天", "difficulty": "medium",
                "children": [
                    {"title": "Tableau基础", "description": "数据连接、工作表、仪表板、故事", "difficulty": "medium"},
                    {"title": "Power BI基础", "description": "数据模型、DAX公式、可视化", "difficulty": "medium"},
                ]
            },
            {
                "title": "业务分析方法论", "description": "用分析驱动业务决策", "order_index": 5, "duration": "约7天", "difficulty": "hard",
                "children": [
                    {"title": "漏斗分析", "description": "转化率拆解、流失节点定位", "difficulty": "medium"},
                    {"title": "留存分析", "description": "群组分析、次日/7日/30日留存", "difficulty": "hard"},
                    {"title": "归因分析", "description": "首次/末次/线性归因、Shapley值", "difficulty": "hard"},
                    {"title": "A/B测试", "description": "实验设计、样本量计算、显著性判定", "difficulty": "hard"},
                ]
            },
        ]
    },
}


@router.post("/paths/generate")
def generate_path(user_id: int = 1, career: str = ""):
    """AI生成两级学习路线：阶段（目录）→ 具体知识点"""
    db = SessionLocal()
    try:
        prof = db.query(Profile).filter(Profile.user_id == user_id).first()
        career_name = career or (prof.job_targets.split(",")[0] if prof and prof.job_targets else "软件工程师")
    except:
        career_name = career or "软件工程师"
    finally:
        db.close()

    # ── 尝试AI生成 ──
    data = _try_ai_generate(career_name)

    # ── 如果AI失败，查内置知识库 ──
    if data is None:
        kb = _KB.get(career_name)
        if kb:
            data = kb
        else:
            # 兜底：3章通用
            data = {
                "title": f"{career_name}学习路线",
                "description": "系统推荐的基础到进阶学习路径",
                "difficulty": "beginner",
                "nodes": [
                    {"title": "基础入门", "order_index": 0, "duration": "约7天", "difficulty": "easy",
                     "children": [{"title": f"{career_name}概述", "difficulty": "easy"}]},
                    {"title": "技能进阶", "order_index": 1, "duration": "约14天", "difficulty": "medium",
                     "children": [{"title": f"{career_name}核心技术", "difficulty": "medium"}]},
                    {"title": "实战项目", "order_index": 2, "duration": "约21天", "difficulty": "hard",
                     "children": [{"title": f"{career_name}项目实践", "difficulty": "hard"}]},
                ]
            }

    # ── 写数据库 ──
    db = SessionLocal()
    try:
        path_obj = LearningPath(
            user_id=user_id, career=career_name,
            title=data.get("title", f"{career_name}学习路线"),
            description=data.get("description", ""),
            difficulty=data.get("difficulty", "beginner"),
            total_nodes=0, is_active=1,
        )
        db.add(path_obj)
        db.flush()

        total_count = 0
        for nd in data.get("nodes", []):
            chapter = LearningNode(
                path_id=path_obj.id, parent_id=0, user_id=user_id,
                title=nd.get("title", ""), description=nd.get("description", ""),
                order_index=nd.get("order_index", 0), duration=nd.get("duration", "约7天"),
                difficulty=nd.get("difficulty", "medium"),
            )
            db.add(chapter)
            db.flush()

            # 子知识点
            for i, kp in enumerate(nd.get("children", [])):
                db.add(LearningNode(
                    path_id=path_obj.id, parent_id=chapter.id, user_id=user_id,
                    title=kp.get("title", ""), description=kp.get("description", ""),
                    order_index=i, duration="约30分钟",
                    difficulty=kp.get("difficulty", "medium"),
                ))
                total_count += 1

        path_obj.total_nodes = len(data.get("nodes", [])) + total_count
        db.commit()

        # ── 返回 ──
        nodes = db.query(LearningNode).filter(
            LearningNode.path_id == path_obj.id
        ).order_by(LearningNode.order_index).all()

        return {
            "id": path_obj.id,
            "title": data.get("title", ""),
            "description": data.get("description", ""),
            "difficulty": data.get("difficulty", "beginner"),
            "nodes": [
                {
                    "id": n.id, "title": n.title, "description": n.description,
                    "order_index": n.order_index, "parent_id": n.parent_id,
                    "duration": n.duration, "difficulty": n.difficulty, "status": n.status,
                }
                for n in nodes
            ],
        }
    finally:
        db.close()


def _try_ai_generate(career_name: str) -> dict | None:
    """尝试AI生成知识树，失败返回None"""
    try:
        from routers.llm import chat as _chat
        prompt = f"""你是一位资深职业培训师。为「{career_name}」设计一套完整的学习路线。
输出纯JSON（不要markdown代码块），要求：
- title: 路线标题
- description: 一句话介绍
- difficulty: beginner/intermediate/advanced
- nodes: 数组，每个元素包含 title/description/order_index/duration/difficulty/children

每个node的children数组包含具体知识点：{{"title":"知识点名","description":"一句话说明","difficulty":"easy/medium/hard"}}

示例结构：
{{"title":"{career_name}学习路线","description":"","difficulty":"beginner","nodes":[
  {{"title":"第一阶段","description":"","order_index":0,"duration":"约7天","difficulty":"easy","children":[
    {{"title":"第一个知识点","description":"","difficulty":"easy"}}
  ]}}
]}}

生成5-7个阶段，每阶段6-10个具体知识点。"""
        text = _chat(prompt, system="你是一位课程设计专家。只返回纯JSON。",
                     max_tokens=4000, temperature=0.7)
        if not text or not text.strip():
            return None
        text = text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            if text.endswith("```"):
                text = text[:-3]
        data = json.loads(text)
        if not isinstance(data, dict) or "nodes" not in data:
            return None
        # 校验：必须有至少一个节点包含 children（子知识点）
        has_children = any(
            isinstance(n, dict) and "children" in n and isinstance(n["children"], list) and len(n["children"]) > 0
            for n in data.get("nodes", [])
        )
        if not has_children:
            return None
        return data
    except Exception:
        return None


@router.get("/paths")
def get_paths(user_id: int = 1):
    db = SessionLocal()
    try:
        paths = db.query(LearningPath).filter(
            LearningPath.user_id == user_id
        ).order_by(LearningPath.created_at.desc()).all()
        return {
            "items": [
                {
                    "id": p.id,
                    "title": p.title,
                    "description": p.description,
                    "difficulty": p.difficulty,
                    "total_nodes": p.total_nodes,
                    "progress": p.progress,
                    "is_active": p.is_active,
                    "created_at": p.created_at.strftime("%Y-%m-%d") if p.created_at else "",
                }
                for p in paths
            ]
        }
    finally:
        db.close()


@router.get("/paths/{path_id}")
def get_path_detail(path_id: int):
    db = SessionLocal()
    try:
        path = db.query(LearningPath).filter(LearningPath.id == path_id).first()
        if not path:
            return {"error": "not found"}
        nodes = db.query(LearningNode).filter(
            LearningNode.path_id == path_id
        ).order_by(LearningNode.order_index).all()
        return {
            "id": path.id,
            "title": path.title,
            "description": path.description,
            "difficulty": path.difficulty,
            "progress": path.progress,
            "nodes": [
                {
                    "id": n.id,
                    "title": n.title,
                    "description": n.description,
                    "order_index": n.order_index,
                    "parent_id": n.parent_id,
                    "duration": n.duration,
                    "difficulty": n.difficulty,
                    "status": n.status,
                    "completed_at": n.completed_at.strftime("%Y-%m-%d") if n.completed_at else "",
                }
                for n in nodes
            ]
        }
    finally:
        db.close()


@router.post("/paths/create")
def create_path(user_id: int = 1, title: str = "", description: str = "", career: str = ""):
    db = SessionLocal()
    try:
        path = LearningPath(user_id=user_id, career=career or title, title=title or "学习路线",
            description=description or "", difficulty="beginner", total_nodes=0, is_active=1)
        db.add(path); db.commit()
        return {"id": path.id, "ok": True}
    finally:
        db.close()


@router.delete("/paths/{path_id}")
def delete_path(path_id: int):
    db = SessionLocal()
    try:
        db.query(LearningNode).filter(LearningNode.path_id == path_id).delete()
        db.query(LearningPath).filter(LearningPath.id == path_id).delete()
        db.commit()
        return {"ok": True}
    finally:
        db.close()


@router.post("/paths/{path_id}/nodes")
def add_node(path_id: int, title: str = "", description: str = "", parent_id: int = 0, user_id: int = 1):
    db = SessionLocal()
    try:
        path = db.query(LearningPath).filter(LearningPath.id == path_id).first()
        if not path: return {"ok": False, "error": "path not found"}
        nodes = db.query(LearningNode).filter(LearningNode.path_id == path_id).order_by(LearningNode.order_index.desc()).limit(1).all()
        max_order = nodes[0].order_index if nodes else -1
        node = LearningNode(path_id=path_id, user_id=user_id, title=title, description=description,
            parent_id=parent_id, order_index=max_order + 1, status="pending")
        db.add(node); path.total_nodes += 1; db.commit()
        return {"ok": True, "id": node.id, "title": node.title, "order_index": node.order_index}
    finally:
        db.close()


@router.delete("/nodes/{node_id}")
def delete_node(node_id: int):
    db = SessionLocal()
    try:
        node = db.query(LearningNode).filter(LearningNode.id == node_id).first()
        if not node: return {"ok": False, "error": "not found"}
        path = db.query(LearningPath).filter(LearningPath.id == node.path_id).first()
        db.delete(node)
        if path and path.total_nodes > 0: path.total_nodes -= 1
        db.commit()
        return {"ok": True}
    finally:
        db.close()


@router.post("/nodes/{node_id}/generate-doc")
def generate_node_doc(node_id: int, resource_id: int = 0):
    db = SessionLocal()
    try:
        node = db.query(LearningNode).filter(LearningNode.id == node_id).first()
        if not node: return {"ok": False, "error": "not found"}
        # 如果指定了resource_id，使用该资源的标题
        title = node.title
        if resource_id:
            res = db.query(LearningResource).filter(LearningResource.id == resource_id).first()
            if res:
                title = res.title
        prompt = f"为「{title}」生成详细学习笔记（500字以内markdown）：\n1. 核心概念\n2. 关键要点\n3. 实用技巧\n4. 常见问题"
        doc = chat(prompt, system="你是技术文档作者。回复简洁、结构清晰。", max_tokens=1500)
        if resource_id:
            # 更新已有资源的内容
            res = db.query(LearningResource).filter(LearningResource.id == resource_id).first()
            if res:
                res.content = doc
                db.commit()
                return {"ok": True, "title": res.title, "content": doc}
        # 没有 resource_id，创建新文档
        r = LearningResource(node_id=node_id, title=f"{node.title} 学习笔记", content=doc, resource_type="document")
        db.add(r); db.commit()
        return {"ok": True, "title": r.title, "content": doc}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        db.close()


@router.post("/paths/{path_id}/import-career")
def import_career_path(path_id: int, career: str = ""):
    db = SessionLocal()
    try:
        path = db.query(LearningPath).filter(LearningPath.id == path_id).first()
        if not path: return {"ok": False, "error": "path not found"}
        from routers.llm import chat as lm
        txt = lm(f"为「{career}」设计8-12个核心技能模块。返回JSON数组：[{{\"title\":\"模块名\",\"description\":\"一句话说明\"}}]",
                 system="只返回纯JSON。", max_tokens=2000, temperature=0.7).strip()
        if txt.startswith("```"): txt = txt.split("\n",1)[1]
        if txt.endswith("```"): txt = txt[:-3]
        nodes = json.loads(txt) if txt.startswith("[") else []
        if not isinstance(nodes, list): nodes = []
        for i, nd in enumerate(nodes):
            db.add(LearningNode(path_id=path_id, user_id=path.user_id or 1,
                title=nd.get("title",""), description=nd.get("description",""),
                order_index=i, status="pending"))
        path.total_nodes = len(nodes); db.commit()
        return {"ok": True, "count": len(nodes), "nodes": nodes}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        db.close()


@router.post("/nodes/{node_id}/chat")
def node_chat(node_id: int, question: str = ""):
    db = SessionLocal()
    try:
        node = db.query(LearningNode).filter(LearningNode.id == node_id).first()
        if not node: return {"ok": False, "error": "not found"}
        prompt = f"用户学习：{node.title}（{node.description}）\n提问：{question}\n中文200字内。"
        ans = chat(prompt, system="友好的AI学习助手。", max_tokens=500)
        return {"ok": True, "answer": ans}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        db.close()


@router.post("/nodes/{node_id}/progress")
def update_node_progress(node_id: int, status: str = "completed"):
    db = SessionLocal()
    try:
        node = db.query(LearningNode).filter(LearningNode.id == node_id).first()
        if not node:
            return {"ok": False, "error": "not found"}
        node.status = status
        if status == "completed":
            node.completed_at = datetime.utcnow()
            # 更新路线进度
            path = db.query(LearningPath).filter(LearningPath.id == node.path_id).first()
            if path:
                total = db.query(LearningNode).filter(
                    LearningNode.path_id == node.path_id
                ).count()
                done = db.query(LearningNode).filter(
                    LearningNode.path_id == node.path_id,
                    LearningNode.status == "completed"
                ).count()
                path.progress = round(done / total * 100, 1) if total > 0 else 0
        db.commit()
        return {"ok": True}
    finally:
        db.close()


# ═══════════════════════════════════════════
# 3.5 节点资源
# ═══════════════════════════════════════════
@router.get("/resources")
def get_resources(node_id: int = 0, user_id: int = 1):
    """获取节点的学习资源（卡片）"""
    db = SessionLocal()
    try:
        q = db.query(LearningResource)
        if node_id:
            q = q.filter(LearningResource.node_id == node_id)
        items = q.order_by(LearningResource.id).all()
        return {
            "items": [
                {
                    "id": r.id,
                    "node_id": r.node_id,
                    "title": r.title,
                    "resource_type": r.resource_type,
                    "url": r.url,
                    "content": r.content,
                }
                for r in items
            ]
        }
    finally:
        db.close()


@router.post("/resources")
def add_resource(
    node_id: int = Query(1),
    user_id: int = Query(1),
    title: str = Query(""),
    resource_type: str = Query("card"),
):
    """添加学习卡片到知识点"""
    db = SessionLocal()
    try:
        r = LearningResource(
            node_id=node_id,
            user_id=user_id,
            title=title or "学习卡片",
            resource_type=resource_type,
        )
        db.add(r)
        db.commit()
        db.refresh(r)
        return {"ok": True, "id": r.id, "title": r.title, "resource_type": r.resource_type}
    finally:
        db.close()


@router.delete("/resources/{rid}")
def delete_resource(rid: int):
    db = SessionLocal()
    try:
        r = db.query(LearningResource).filter(LearningResource.id == rid).first()
        if not r:
            return {"ok": False, "error": "not found"}
        db.delete(r)
        db.commit()
        return {"ok": True}
    finally:
        db.close()


# ═══════════════════════════════════════════
# 4. 笔记
# ═══════════════════════════════════════════
@router.get("/notes")
def get_notes(user_id: int = 1, node_id: int = 0):
    db = SessionLocal()
    try:
        q = db.query(LearningNote).filter(LearningNote.user_id == user_id)
        if node_id:
            q = q.filter(LearningNote.node_id == node_id)
        notes = q.order_by(LearningNote.created_at.desc()).all()
        return {
            "items": [
                {
                    "id": n.id,
                    "title": n.title,
                    "content": n.content,
                    "node_id": n.node_id,
                    "resource_id": n.resource_id,
                    "created_at": n.created_at.strftime("%Y-%m-%d %H:%M") if n.created_at else "",
                }
                for n in notes
            ]
        }
    finally:
        db.close()


@router.post("/notes")
def create_note(
    user_id: int = Query(1),
    node_id: int = Query(0),
    resource_id: int = Query(0),
    title: str = Query(""),
    content: str = Query(""),
    # JSON body support (preferred for rich text)
    body: dict = None,
):
    db = SessionLocal()
    try:
        # Merge: JSON body fields override query params
        uid = body.get("user_id", user_id) if body else user_id
        nid = body.get("node_id", node_id) if body else node_id
        rid = body.get("resource_id", resource_id) if body else resource_id
        ttl = body.get("title", title) if body else title
        ctt = body.get("content", content) if body else content

        note = LearningNote(
            user_id=uid, node_id=nid, resource_id=rid,
            title=ttl, content=ctt
        )
        db.add(note)
        db.commit()
        db.refresh(note)
        return {"ok": True, "id": note.id}
    finally:
        db.close()


@router.put("/notes/{note_id}")
def update_note(note_id: int, title: str = "", content: str = ""):
    db = SessionLocal()
    try:
        note = db.query(LearningNote).filter(LearningNote.id == note_id).first()
        if not note:
            return {"ok": False, "error": "not found"}
        if title:
            note.title = title
        if content:
            note.content = content
        db.commit()
        return {"ok": True}
    finally:
        db.close()


@router.delete("/notes/{note_id}")
def delete_note(note_id: int):
    db = SessionLocal()
    try:
        note = db.query(LearningNote).filter(LearningNote.id == note_id).first()
        if note:
            db.delete(note)
            db.commit()
        return {"ok": True}
    finally:
        db.close()


# ═══════════════════════════════════════════
# 5. 复习提醒
# ═══════════════════════════════════════════
@router.get("/reviews")
def get_reviews(user_id: int = 1):
    db = SessionLocal()
    try:
        items = db.query(ReviewSchedule).filter(
            ReviewSchedule.user_id == user_id
        ).order_by(ReviewSchedule.next_review_at.asc()).all()
        return {
            "items": [
                {
                    "id": r.id,
                    "title": r.title,
                    "weakness_id": r.weakness_id,
                    "review_interval": r.review_interval,
                    "next_review_at": r.next_review_at,
                    "reviewed_count": r.reviewed_count,
                    "last_reviewed_at": r.last_reviewed_at,
                }
                for r in items
            ]
        }
    finally:
        db.close()


@router.post("/reviews")
def create_review(user_id: int = 1, weakness_id: int = 0, title: str = "",
                  review_interval: int = 1, next_review_at: str = ""):
    db = SessionLocal()
    try:
        r = ReviewSchedule(
            user_id=user_id, weakness_id=weakness_id, title=title,
            review_interval=review_interval, next_review_at=next_review_at
        )
        db.add(r)
        db.commit()
        return {"ok": True}
    finally:
        db.close()


@router.post("/reviews/auto-create")
def auto_create_reviews(user_id: int = 1):
    """从所有未掌握的薄弱点自动创建复习提醒（跳过已存在的）"""
    db = SessionLocal()
    try:
        weaknesses = db.query(WeaknessItem).filter(
            WeaknessItem.user_id == user_id,
            WeaknessItem.mastered == 0
        ).all()
        existing = db.query(ReviewSchedule).filter(
            ReviewSchedule.user_id == user_id
        ).all()
        existing_titles = set(r.title for r in existing)

        now = datetime.utcnow()
        created = 0
        from datetime import timedelta
        for w in weaknesses:
            title = f"{w.name}复习"
            if title in existing_titles:
                continue
            interval = 3  # 默认3天后复习
            review = ReviewSchedule(
                user_id=user_id, weakness_id=w.id, title=title,
                review_interval=interval,
                next_review_at=(now + timedelta(days=interval)).strftime("%Y-%m-%d"),
                reviewed_count=0,
            )
            db.add(review)
            created += 1
        db.commit()
        return {"ok": True, "created": created}
    finally:
        db.close()


@router.post("/reviews/{rid}/complete")
def complete_review(rid: int):
    db = SessionLocal()
    try:
        r = db.query(ReviewSchedule).filter(ReviewSchedule.id == rid).first()
        if r:
            r.reviewed_count += 1
            from datetime import timedelta
            now = datetime.utcnow()
            r.last_reviewed_at = now.strftime("%Y-%m-%d %H:%M")
            next_dt = now + timedelta(days=r.review_interval)
            r.next_review_at = next_dt.strftime("%Y-%m-%d")
            db.commit()
            return {"ok": True}
        return {"ok": False, "error": "not found"}
    finally:
        db.close()


# ═══════════════════════════════════════════
# 6. 智能简历 + 匹配度
# ═══════════════════════════════════════════
@router.get("/resume")
def get_smart_resume(user_id: int = 1, career: str = ""):
    db = SessionLocal()
    try:
        q = db.query(SmartResume).filter(SmartResume.user_id == user_id)
        if career:
            q = q.filter(SmartResume.career == career)
        item = q.order_by(SmartResume.created_at.desc()).first()
        if item:
            return {
                "id": item.id,
                "career": item.career,
                "summary": item.summary,
                "skills_text": item.skills_text,
                "experience_text": item.experience_text,
                "education_text": item.education_text,
                "match_score": item.match_score,
                "created_at": item.created_at.strftime("%Y-%m-%d") if item.created_at else "",
            }
        return {}
    finally:
        db.close()


@router.get("/resume/list")
def list_smart_resumes(user_id: int = 1):
    """列出用户所有已生成的智能简历"""
    db = SessionLocal()
    try:
        items = db.query(SmartResume).filter(
            SmartResume.user_id == user_id
        ).order_by(SmartResume.created_at.desc()).all()
        return [{
            "id": r.id,
            "career": r.career,
            "summary": r.summary[:100] if r.summary else "",
            "skills_text": r.skills_text[:100] if r.skills_text else "",
            "match_score": r.match_score,
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M") if r.created_at else "",
        } for r in items]
    finally:
        db.close()


@router.post("/resume/generate")
def generate_resume(user_id: int = 1, career: str = ""):
    """AI根据画像生成简历内容"""
    db = SessionLocal()
    try:
        prof = db.query(Profile).filter(Profile.user_id == user_id).first()
        weaknesses = db.query(WeaknessItem).filter(
            WeaknessItem.user_id == user_id,
            WeaknessItem.mastered == 0
        ).all()
        sessions = db.query(InterviewSession).order_by(
            InterviewSession.created_at.desc()
        ).limit(10).all()
        avg_score = 0
        if sessions:
            scores = [s.average_score for s in sessions if s.average_score]
            avg_score = round(sum(scores) / len(scores), 1) if scores else 0

        prompt = f"""你是资深HR。请为用户生成面向「{career or (prof.job_targets if prof else '目标岗位')}」的简历内容。

用户画像：
- 学历：{prof.education if prof else '本科'}
- 专业：{prof.major if prof else ''}
- 技能：{prof.skills if prof else ''}
- 年级：{prof.grade if prof else ''}
- 面试平均分：{avg_score}
- 薄弱点：{', '.join([w.name for w in weaknesses[:5]]) if weaknesses else '暂无'}

请返回JSON格式（不要markdown代码块）：
{{
  "summary": "50字内的个人总结",
  "skills_text": "技能清单（含掌握程度），不同技能用｜分隔",
  "experience_text": "一段描述项目/实践经历的文字",
  "education_text": "教育背景描述",
  "match_score": 0-100的匹配度数字
}}"""
        text = chat(prompt, system="你是资深HR，简历内容实用、不提虚的。只返回JSON。",
                    max_tokens=1500)
        text = text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            if text.endswith("```"):
                text = text[:-3]
        data = json.loads(text)
    except:
        data = {
            "summary": f"具备{prof.major if prof else '相关'}专业背景，正在求职{career or '目标岗位'}方向",
            "skills_text": prof.skills if prof and prof.skills else "基础技能",
            "experience_text": "在校期间积极参与项目实践",
            "education_text": f"{prof.education if prof else '本科'} · {prof.major if prof else ''}",
            "match_score": 65,
        }

    sr = SmartResume(
        user_id=user_id,
        career=career or (prof.job_targets.split(",")[0] if prof and prof.job_targets else ""),
        summary=data.get("summary", ""),
        skills_text=data.get("skills_text", ""),
        experience_text=data.get("experience_text", ""),
        education_text=data.get("education_text", ""),
        match_score=data.get("match_score", 0),
    )
    db.add(sr)
    db.commit()
    return {"ok": True, "match_score": data.get("match_score", 0)}


@router.get("/match/{career}")
def get_match_score(user_id: int = 1, career: str = ""):
    """计算用户与某个岗位的匹配度"""
    if not career:
        return {"match_score": 0, "skill_gaps": [], "suggestion": ""}
    db = SessionLocal()
    try:
        prof = db.query(Profile).filter(Profile.user_id == user_id).first()
        if not prof:
            return {"match_score": 30, "skill_gaps": ["请先完善个人画像"], "suggestion": "完善资料后可获得准确匹配度"}
        weaknesses = db.query(WeaknessItem).filter(
            WeaknessItem.user_id == user_id,
            WeaknessItem.mastered == 0
        ).count()
        sessions = db.query(InterviewSession).filter(
            InterviewSession.job == career
        ).count()
        total_sessions = db.query(InterviewSession).count()
        avg_score = 0
        all_sessions = db.query(InterviewSession).order_by(InterviewSession.created_at.desc()).limit(5).all()
        if all_sessions:
            scores = [s.average_score for s in all_sessions if s.average_score]
            avg_score = round(sum(scores) / len(scores), 1) if scores else 0

        # 计算匹配度
        has_career = 20 if career in (prof.job_targets or "") else 10
        has_interview = min(20, sessions * 5)
        score_base = min(20, int(avg_score * 0.2)) if avg_score else 10
        weak_penalty = max(0, 20 - weaknesses * 3)
        has_skills = 10 if prof.skills else 0
        has_experience = 10 if prof.experience else 0
        match_score = min(99, has_career + has_interview + score_base + weak_penalty + has_skills + has_experience)

        prompts = [
            "掌握核心技能，建议多投同类型岗位",
            "整体匹配，建议强化薄弱环节",
            "基础匹配，建议补足技能后再投递",
            "匹配度较低，建议作为保底选项",
        ]
        suggestion = prompts[0] if match_score >= 80 else prompts[1] if match_score >= 60 else prompts[2] if match_score >= 40 else prompts[3]

        return {
            "match_score": match_score,
            "skill_gaps": [w.name for w in db.query(WeaknessItem).filter(
                WeaknessItem.user_id == user_id,
                WeaknessItem.mastered == 0
            ).limit(3).all()] if weaknesses > 0 else [],
            "suggestion": suggestion,
            "details": {
                "career_match": has_career,
                "interview_experience": has_interview,
                "score_performance": score_base,
                "weakness_penalty": weak_penalty,
                "skills_match": has_skills,
                "experience_match": has_experience,
            }
        }
    finally:
        db.close()


# ═══════════════════════════════════════════
# 7. 学习轨迹 — 学习打卡 + 成长地图
# ═══════════════════════════════════════════
@router.get("/trajectory")
def get_trajectory(user_id: int = 1, days: int = 30):
    """返回学习轨迹：热力图/薄弱点攻克进度/已通关路线"""
    db = SessionLocal()
    try:
        from datetime import timedelta, date
        from collections import defaultdict
        from datetime import datetime as dt2
        now = datetime.utcnow()
        since = now - timedelta(days=days)

        # ── 1. 学习打卡热力图（过去84天每日活动计数）──
        heatmap_days = 84
        heat_since = now - timedelta(days=heatmap_days)

        activity_dates = []

        for s in db.query(InterviewSession).filter(
            InterviewSession.created_at >= heat_since
        ).all():
            if s.created_at:
                activity_dates.append(s.created_at)

        for e in db.query(ExamRecord).filter(
            ExamRecord.created_at >= heat_since
        ).all():
            if e.created_at:
                activity_dates.append(e.created_at)

        for n in db.query(LearningNode).filter(
            LearningNode.user_id == user_id,
            LearningNode.status == "completed",
            LearningNode.completed_at >= heat_since,
        ).all():
            if n.completed_at:
                activity_dates.append(n.completed_at)

        for r in db.query(ReviewSchedule).filter(
            ReviewSchedule.user_id == user_id
        ).all():
            if r.last_reviewed_at:
                try:
                    rd = dt2.strptime(r.last_reviewed_at[:10], "%Y-%m-%d")
                    if rd >= (now - timedelta(days=heatmap_days)):
                        activity_dates.append(rd)
                except:
                    pass

        for xm in db.query(XiaoJuMessage).filter(
            XiaoJuMessage.created_at >= heat_since
        ).all():
            if xm.created_at:
                activity_dates.append(xm.created_at)

        heat_counts = defaultdict(int)
        for ad in activity_dates:
            key = ad.strftime("%Y-%m-%d")
            heat_counts[key] += 1

        heatmap = []
        for i in range(heatmap_days):
            d = (heat_since + timedelta(days=i))
            heatmap.append({"date": d.strftime("%Y-%m-%d"), "count": heat_counts.get(d.strftime("%Y-%m-%d"), 0), "dow": d.weekday()})

        # 连续学习天数
        streak = 0
        check = now.date()
        for _ in range(365):
            if heat_counts.get(check.strftime("%Y-%m-%d"), 0) > 0:
                streak += 1
                check -= timedelta(days=1)
            else:
                break

        # ── 2. 薄弱点攻克进度 ──
        weaknesses = db.query(WeaknessItem).filter(
            WeaknessItem.user_id == user_id,
            WeaknessItem.mastered != 2,
        ).order_by(WeaknessItem.score.asc()).limit(20).all()

        weakness_progress = []
        for w in weaknesses:
            review_count = 0
            try:
                for r in db.query(ReviewSchedule).filter(
                    ReviewSchedule.weakness_id == w.id
                ).all():
                    review_count += r.reviewed_count or 0
            except:
                pass
            weakness_progress.append({
                "id": w.id,
                "name": w.name,
                "score": w.score or 0,
                "mastered": w.mastered or 0,
                "category": w.category or "interview",
                "detected_count": w.detected_count or 1,
                "review_count": review_count,
                "created_at": w.created_at.strftime("%Y-%m-%d") if w.created_at else "",
            })

        # ── 3. 已通关路线图 ──
        paths = db.query(LearningPath).filter(
            LearningPath.user_id == user_id,
            LearningPath.is_active == 1
        ).all()

        path_progress = []
        for p in paths:
            total = db.query(LearningNode).filter(
                LearningNode.path_id == p.id,
                LearningNode.parent_id != 0
            ).count()
            completed = db.query(LearningNode).filter(
                LearningNode.path_id == p.id,
                LearningNode.parent_id != 0,
                LearningNode.status == "completed"
            ).count()
            if total > 0:
                path_progress.append({
                    "id": p.id,
                    "career": p.career or p.title or "未命名",
                    "total": total,
                    "completed": completed,
                    "progress": round(completed / total * 100, 1),
                })

        # ── 4. 保留活动时间线 ──
        events = []
        for s in db.query(InterviewSession).filter(
            InterviewSession.created_at >= since
        ).order_by(InterviewSession.created_at.desc()).all():
            events.append({
                "type": "interview",
                "title": f"完成「{s.job or '面试'}」模拟面试",
                "score": s.average_score,
                "time": s.created_at.strftime("%m-%d %H:%M") if s.created_at else "",
            })
        for e in db.query(ExamRecord).filter(
            ExamRecord.created_at >= since
        ).order_by(ExamRecord.created_at.desc()).all():
            events.append({
                "type": "exam",
                "title": f"完成「{e.career or '笔试'}」{e.mode or ''}",
                "score": e.accuracy,
                "time": e.created_at.strftime("%m-%d %H:%M") if e.created_at else "",
            })
        for n in db.query(LearningNode).filter(
            LearningNode.user_id == user_id,
            LearningNode.status == "completed",
            LearningNode.completed_at >= since,
        ).all():
            events.append({
                "type": "node",
                "title": f"完成学习节点「{n.title}」",
                "score": None,
                "time": n.completed_at.strftime("%m-%d %H:%M") if n.completed_at else "",
            })
        try:
            since_s = since.strftime("%Y-%m-%d %H:%M")
            for r in db.query(ReviewSchedule).filter(
                ReviewSchedule.user_id == user_id
            ).all():
                lr = r.last_reviewed_at
                if lr and lr >= since_s:
                    events.append({
                        "type": "review",
                        "title": f"完成复习「{r.title}」",
                        "score": None,
                        "time": lr,
                    })
        except:
            pass
        events.sort(key=lambda x: x["time"], reverse=True)

        return {
            "heatmap": heatmap,
            "streak": streak,
            "weakness_progress": weakness_progress,
            "path_progress": path_progress,
            "events": events[:20],
        }
    finally:
        db.close()


# ═══════════════════════════════════════════
# 8. 知识点对话（学习助手）
# ═══════════════════════════════════════════
@router.get("/chat")
def chat_about_knowledge(context: str = "", question: str = ""):
    """回答用户关于知识点的提问"""
    try:
        from routers.llm import chat
        prompt = f"用户正在学习：{context}\n\n用户提问：{question}\n\n请用中文回答，简洁易懂，控制在200字以内。如果涉及代码，给出简短示例。"
        answer = chat(prompt, system="你是友好的AI学习助手，帮助大学生理解和掌握知识点。回答简洁、准确、带示例。", max_tokens=500)
        return {"answer": answer}
    except:
        return {"answer": f"关于「{context}」的问题「{question}」，建议查看节点内的学习文档或搜索相关视频巩固理解。"}


# ═══════════════════════════════════════════
# 8.5 聊天持久化 + 共享记忆
# ═══════════════════════════════════════════

@router.get("/chat/{node_id}/history")
def get_chat_history(node_id: int, user_id: int = 1):
    """读取某知识点的聊天历史"""
    db = SessionLocal()
    try:
        session = db.query(XiaoJuSession).filter(
            XiaoJuSession.node_id == node_id,
            XiaoJuSession.user_id == user_id
        ).first()
        if not session:
            return {"messages": [], "session_id": None, "count": 0, "summary": ""}
        msgs = db.query(XiaoJuMessage).filter(
            XiaoJuMessage.session_id == session.id
        ).order_by(XiaoJuMessage.id).all()
        return {
            "messages": [{"role": m.role, "content": m.content} for m in msgs],
            "session_id": session.id,
            "count": len(msgs),
            "summary": session.context_summary or "",
            "is_archived": session.is_archived,
        }
    finally:
        db.close()


@router.post("/chat/{node_id}/save")
def save_chat_message(node_id: int, role: str = "user", content: str = "", user_id: int = 1):
    """保存一条聊天消息"""
    db = SessionLocal()
    try:
        session = db.query(XiaoJuSession).filter(
            XiaoJuSession.node_id == node_id,
            XiaoJuSession.user_id == user_id
        ).first()
        if not session:
            node = db.query(LearningNode).filter(LearningNode.id == node_id).first()
            session = XiaoJuSession(
                user_id=user_id,
                node_id=node_id,
                topic=node.title if node else "学习问答",
                message_count=0
            )
            db.add(session)
            db.flush()
        msg = XiaoJuMessage(session_id=session.id, role=role, content=content)
        db.add(msg)
        session.message_count = (session.message_count or 0) + 1
        session.updated_at = datetime.utcnow()
        db.commit()
        return {"ok": True, "session_id": session.id, "count": session.message_count}
    finally:
        db.close()


@router.post("/chat/{node_id}/archive")
def archive_chat(node_id: int, user_id: int = 1):
    """聊天达到上限 → 自动打包为知识卡片"""
    db = SessionLocal()
    try:
        session = db.query(XiaoJuSession).filter(
            XiaoJuSession.node_id == node_id,
            XiaoJuSession.user_id == user_id
        ).first()
        if not session or (session.message_count or 0) < 4:
            return {"ok": False, "error": "not enough messages"}

        msgs = db.query(XiaoJuMessage).filter(
            XiaoJuMessage.session_id == session.id
        ).order_by(XiaoJuMessage.id).all()

        # 构建对话文本
        conv_lines = []
        for m in msgs:
            who = "用户" if m.role == "user" else "小橘"
            conv_lines.append(f"{who}：{m.content}")
        conv_text = "\n".join(conv_lines)

        # AI生成摘要文档
        from routers.llm import chat as lm_chat
        prompt = f"以下是一段学习对话，请整理成结构化的知识点摘要文档（markdown格式，300字以内，包含核心问题和解答要点）：\n\n{conv_text}"
        summary = lm_chat(prompt, system="你是学习助手，将对话整理成整洁的结构化笔记。", max_tokens=800)

        # 保存为学习资源（知识卡片）
        res = LearningResource(
            node_id=node_id,
            user_id=user_id,
            title=f"💬 AI对话总结 - {session.topic}",
            content=summary,
            resource_type="document",
        )
        db.add(res)
        db.flush()

        # 同时保存到 XIAOJU_MEMORY（共享记忆）
        memory = XiaoJuMemory(
            user_id=user_id,
            key=f"chat_summary_node_{node_id}",
            value=summary,
            memory_type="learning",
        )
        db.add(memory)

        # 标记会话已归档
        session.is_archived = 1
        session.context_summary = summary[:500]
        db.commit()

        return {"ok": True, "resource_id": res.id, "title": res.title}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        db.close()


# ═══════════════════════════════════════════
# 9. 学习资源搜索（面试准备用）
# ═══════════════════════════════════════════
@router.get("/search-resources")
def search_resources(keyword: str = "", user_id: int = 1):
    """
    Search learning resources by keyword in title (case-insensitive).
    Returns all resources whose title contains the keyword.
    Used by the interview prep tab to find learning content for weak points.
    """
    db = SessionLocal()
    try:
        q = db.query(LearningResource).filter(LearningResource.user_id == user_id)
        if keyword.strip():
            q = q.filter(LearningResource.title.ilike(f"%{keyword.strip()}%"))
        resources = q.order_by(LearningResource.id).all()
        return {
            "items": [
                {
                    "id": r.id,
                    "title": r.title,
                    "resource_type": r.resource_type,
                    "url": r.url or "",
                    "content": r.content or "",
                    "node_id": r.node_id,
                }
                for r in resources
            ]
        }
    finally:
        db.close()


# ═══════════════════════════════════════════
# 10. 面试备战 — 记录卡片 + 薄弱点学习
# ═══════════════════════════════════════════

@router.get("/interview/sessions")
def get_interview_sessions(user_id: int = 1):
    """获取面试记录列表（用于面试备战卡片）"""
    db = SessionLocal()
    try:
        from models import InterviewSession
        sessions = db.query(InterviewSession).order_by(InterviewSession.created_at.desc()).limit(30).all()
        items = []
        for s in sessions:
            weaknesses = _json_loads(s.weaknesses_json, [])
            dims = _json_loads(s.dimensions_json, {})
            items.append({
                "id": s.id,
                "job": s.job or "模拟面试",
                "score": s.average_score or 0,
                "mode": s.mode or "basic",
                "question_count": s.total_questions or 0,
                "weaknesses": weaknesses[:4],
                "dimensions": dims,
                "created_at": s.created_at.strftime("%m-%d %H:%M") if s.created_at else "",
            })
        return {"items": items}
    finally:
        db.close()


@router.get("/interview/{session_id}/study")
def get_interview_study(session_id: int, user_id: int = 1):
    """获取某次面试的薄弱点 + 匹配的学习资源"""
    db = SessionLocal()
    try:
        from models import InterviewSession, LearningResource
        session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
        if not session:
            return {"error": "not found"}

        weaknesses = _json_loads(session.weaknesses_json, [])
        suggestions = _json_loads(session.suggestions_json, [])
        dims = _json_loads(session.dimensions_json, {})
        strengths = _json_loads(session.strengths_json, [])

        weak_items = []
        for w in weaknesses[:8]:
            name = w if isinstance(w, str) else (w.get("name") or w.get("item") or "")
            if not name:
                continue
            resources = db.query(LearningResource).filter(
                LearningResource.title.ilike(f"%{name}%")
            ).limit(3).all()
            weak_items.append({
                "name": name,
                "resources": [
                    {"id": r.id, "title": r.title, "content": r.content or "", "type": r.resource_type}
                    for r in resources
                ],
            })

        return {
            "session": {
                "id": session.id,
                "job": session.job or "",
                "score": session.average_score or 0,
                "mode": session.mode or "",
                "question_count": session.total_questions or 0,
                "dimensions": dims,
                "strengths": strengths,
                "suggestions": suggestions,
                "created_at": session.created_at.strftime("%m-%d %H:%M") if session.created_at else "",
            },
            "weak_items": weak_items,
        }
    finally:
        db.close()


@router.post("/study/generate-doc")
def generate_study_doc(context: str = ""):
    """为薄弱点生成学习文档（不存库，直接返回）"""
    if not context:
        return {"ok": False, "error": "missing context"}
    try:
        from routers.llm import chat as _chat
        prompt = f"为知识点「{context}」生成详细学习笔记（markdown格式，300字以内）：\n1. 核心概念\n2. 关键要点\n3. 实用技巧\n4. 常见问题"
        doc = _chat(prompt, system="你是学习辅助专家。输出简洁、结构清晰的Markdown。", max_tokens=1000)
        return {"ok": True, "content": doc}
    except Exception as e:
        return {"ok": False, "error": str(e)}