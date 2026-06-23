"""
笔试专项练习模块 — 后端路由（重构版）
提供笔试题目获取、答案提交、错题管理、收藏管理、统计数据、AI出题等功能
"""

from fastapi import APIRouter, Query, Body
from database import SessionLocal
from models import ExamQuestion, WrongQuestion, SavedQuestion, ExamRecord
from sqlalchemy import desc, func
import json
import random
import os
import httpx
import asyncio
from datetime import datetime

router = APIRouter(prefix="/api/exam", tags=["笔试专项练习"])

# ═══════════════════════════════════════════════════════════════
# 岗位-考点映射
# ═══════════════════════════════════════════════════════════════

GENERAL_KNOWLEDGE_POINTS = [
    "逻辑思维",
    "沟通表达",
    "综合素养",
]

CAREER_KNOWLEDGE_MAP = {
    "前端开发工程师": {
        "professional": ["JavaScript核心", "Vue.js", "React", "CSS进阶", "性能优化", "工程化", "网络安全", "浏览器原理", "场景题", "TypeScript"]
    },
    "后端开发工程师": {
        "professional": ["数据库", "缓存", "API设计", "消息队列", "分布式", "认证授权", "系统设计", "性能优化", "Docker/K8s", "场景题"]
    },
    "产品经理": {
        "professional": ["需求分析", "产品设计", "数据分析", "项目管理", "竞品分析", "PRD写作", "用户增长", "用户研究"]
    },
    "数据分析师": {
        "professional": ["SQL", "统计学", "业务分析", "数据可视化", "实验设计", "工具"]
    },
    "算法工程师": {
        "professional": ["机器学习基础", "深度学习", "NLP/CV", "模型评估", "场景题"]
    },
    "Java开发工程师": {
        "professional": ["Java核心", "JVM", "Spring", "数据库", "场景题", "并发编程"]
    },
    "Python开发工程师": {
        "professional": ["Python基础", "Python进阶", "异步编程", "Web框架", "数据库", "测试"]
    },
    "测试开发工程师": {
        "professional": ["测试基础", "自动化", "性能测试", "CI/CD", "场景题"]
    },
    "UI/UX设计师": {
        "professional": ["设计基础", "交互设计", "设计原则", "用户体验", "设计系统", "工具", "场景题"]
    },
    "软件测试工程师": {
        "professional": ["测试基础理论", "SQL与数据库", "接口测试", "自动化测试", "Linux基础"]
    },
    "网络安全工程师": {
        "professional": ["网络安全基础", "密码学", "操作系统安全", "网络攻防", "漏洞分析"]
    },
    "运维工程师": {
        "professional": ["Linux系统", "网络基础", "Docker/K8s", "CI/CD", "监控告警"]
    },
    "运营专员": {
        "professional": ["内容运营", "用户运营", "数据分析", "活动策划", "新媒体"]
    },
    "市场营销": {
        "professional": ["市场分析", "营销策略", "数据分析", "品牌管理", "新媒体营销"]
    },
    "全栈开发工程师": {
        "professional": ["前端开发", "后端开发", "数据库", "DevOps", "全栈架构"]
    },
}

# 默认专业考点（适用于未明确定义的岗位）
DEFAULT_PROFESSIONAL_POINTS = ["编程语言(Java/Python/Go)", "数据库与SQL", "网络协议", "系统设计", "算法与数据结构"]

def get_career_knowledge(career: str):
    """获取岗位的完整考点（通用 + 专业）"""
    general = [
        {
            "name": kp,
            "types": ["single_choice", "multi_choice", "judge"],
            "difficulties": ["easy", "medium", "hard"]
        }
        for kp in GENERAL_KNOWLEDGE_POINTS
    ]
    if career in CAREER_KNOWLEDGE_MAP:
        prof_points = CAREER_KNOWLEDGE_MAP[career]["professional"]
    else:
        prof_points = DEFAULT_PROFESSIONAL_POINTS
    professional = [
        {
            "name": kp,
            "types": ["single_choice", "judge"],
            "difficulties": ["easy", "medium", "hard"]
        }
        for kp in prof_points
    ]
    return {
        "career": career,
        "general": general,
        "professional": professional,
    }


# ═══════════════════════════════════════════════════════════════
# 扩充题库（>= 150题）
# ═══════════════════════════════════════════════════════════════

EXPANDED_MOCK_QUESTIONS = [
    # ========== HTML/CSS（6题，前端开发工程师） ==========
    {"knowledge_point":"HTML/CSS","category":"专业","career":"前端开发工程师","difficulty":"easy","question_type":"single_choice","question":"HTML中，用于定义超链接的标签是？","options":[{"key":"A","value":"<link>"},{"key":"B","value":"<a>"},{"key":"C","value":"<href>"},{"key":"D","value":"<url>"}],"answer":"B","analysis":"<a>标签用于定义超链接，href属性指定链接目标。link标签用于链接外部资源。"},
    {"knowledge_point":"HTML/CSS","category":"专业","career":"前端开发工程师","difficulty":"easy","question_type":"single_choice","question":"CSS中，以下哪个属性可以实现水平居中？","options":[{"key":"A","value":"text-align:center"},{"key":"B","value":"align:center"},{"key":"C","value":"margin:center"},{"key":"D","value":"horizontal:center"}],"answer":"A","analysis":"text-align:center用于内联元素的水平居中。块级元素水平居中常用margin:0 auto。"},
    {"knowledge_point":"HTML/CSS","category":"专业","career":"前端开发工程师","difficulty":"easy","question_type":"judge","question":"判断：HTML5中，<header>标签只能出现在页面顶部。","options":[{"key":"对","value":"正确"},{"key":"错","value":"错误"}],"answer":"错","analysis":"<header>标签可以出现在文档的任何部分，如文章头部、章节头部等，不限于页面顶部。"},
    {"knowledge_point":"HTML/CSS","category":"专业","career":"前端开发工程师","difficulty":"medium","question_type":"single_choice","question":"CSS中，以下哪个选择器的优先级最高？","options":[{"key":"A","value":"#id"},{"key":"B","value":".class"},{"key":"C","value":"div"},{"key":"D","value":"*"}],"answer":"A","analysis":"CSS选择器优先级：!important>行内样式>ID选择器>类选择器>标签选择器>通配符选择器。"},
    {"knowledge_point":"HTML/CSS","category":"专业","career":"前端开发工程师","difficulty":"medium","question_type":"single_choice","question":"在Flex布局中，justify-content:center的作用是？","options":[{"key":"A","value":"垂直居中"},{"key":"B","value":"水平居中"},{"key":"C","value":"两端对齐"},{"key":"D","value":"换行"}],"answer":"B","analysis":"justify-content控制主轴方向的对齐方式，默认主轴为水平方向，所以center实现水平居中。垂直居中用align-items:center。"},
    {"knowledge_point":"HTML/CSS","category":"专业","career":"前端开发工程师","difficulty":"hard","question_type":"single_choice","question":"CSS中的box-sizing:border-box的作用是？","options":[{"key":"A","value":"使盒模型的宽度包含padding和border"},{"key":"B","value":"使盒模型的宽度只包含content"},{"key":"C","value":"使盒模型变为圆角"},{"key":"D","value":"设置盒模型为块级"}],"answer":"A","analysis":"border-box使元素的width/height包含content+padding+border，方便布局计算。"},

    # ========== JavaScript（6题，前端开发工程师） ==========
    {"knowledge_point":"JavaScript","category":"专业","career":"前端开发工程师","difficulty":"easy","question_type":"single_choice","question":"JavaScript中，typeof null的返回值是？","options":[{"key":"A","value":"\"null\""},{"key":"B","value":"\"object\""},{"key":"C","value":"\"undefined\""},{"key":"D","value":"\"number\""}],"answer":"B","analysis":"这是JavaScript的一个历史遗留bug，typeof null返回'object'。"},
    {"knowledge_point":"JavaScript","category":"专业","career":"前端开发工程师","difficulty":"easy","question_type":"single_choice","question":"以下哪个方法可以将字符串转换为整数？","options":[{"key":"A","value":"parseInt()"},{"key":"B","value":"parseFloat()"},{"key":"C","value":"toString()"},{"key":"D","value":"toFixed()"}],"answer":"A","analysis":"parseInt()将字符串解析为整数，parseFloat()解析为浮点数。"},
    {"knowledge_point":"JavaScript","category":"专业","career":"前端开发工程师","difficulty":"easy","question_type":"judge","question":"判断：JavaScript中，NaN === NaN的结果是true。","options":[{"key":"对","value":"正确"},{"key":"错","value":"错误"}],"answer":"错","analysis":"NaN不等于任何值，包括自身。判断NaN应使用isNaN()函数。"},
    {"knowledge_point":"JavaScript","category":"专业","career":"前端开发工程师","difficulty":"medium","question_type":"single_choice","question":"以下哪种方式可以实现JavaScript的异步编程？","options":[{"key":"A","value":"回调函数"},{"key":"B","value":"Promise"},{"key":"C","value":"async/await"},{"key":"D","value":"以上都是"}],"answer":"D","analysis":"回调函数、Promise、async/await都是JavaScript中实现异步编程的方式。"},
    {"knowledge_point":"JavaScript","category":"专业","career":"前端开发工程师","difficulty":"medium","question_type":"single_choice","question":"以下哪个是JavaScript ES6新增的变量声明方式？","options":[{"key":"A","value":"var"},{"key":"B","value":"let"},{"key":"C","value":"int"},{"key":"D","value":"String"}],"answer":"B","analysis":"ES6新增了let和const声明方式，let具有块级作用域。"},
    {"knowledge_point":"JavaScript","category":"专业","career":"前端开发工程师","difficulty":"hard","question_type":"single_choice","question":"闭包(Closure)是指？","options":[{"key":"A","value":"函数内部的变量不能被外部访问"},{"key":"B","value":"函数能够访问其外部函数作用域中的变量"},{"key":"C","value":"函数只能访问全局变量"},{"key":"D","value":"函数执行完毕后立即销毁"}],"answer":"B","analysis":"闭包是指内部函数可以访问外部函数作用域中变量的能力，即使外部函数已执行完毕。"},

    # ========== 前端框架(Vue/React)（5题，前端开发工程师） ==========
    {"knowledge_point":"前端框架(Vue/React)","category":"专业","career":"前端开发工程师","difficulty":"easy","question_type":"single_choice","question":"Vue.js中，用于响应式数据绑定的指令是？","options":[{"key":"A","value":"v-model"},{"key":"B","value":"v-bind"},{"key":"C","value":"v-for"},{"key":"D","value":"v-if"}],"answer":"A","analysis":"v-model实现表单元素和数据的双向绑定。v-bind实现单向数据绑定。"},
    {"knowledge_point":"前端框架(Vue/React)","category":"专业","career":"前端开发工程师","difficulty":"easy","question_type":"single_choice","question":"React中，用于管理组件状态的Hook是？","options":[{"key":"A","value":"useEffect"},{"key":"B","value":"useState"},{"key":"C","value":"useContext"},{"key":"D","value":"useReducer"}],"answer":"B","analysis":"useState是React中最基础的状态管理Hook，用于在函数组件中添加状态。"},
    {"knowledge_point":"前端框架(Vue/React)","category":"专业","career":"前端开发工程师","difficulty":"medium","question_type":"single_choice","question":"Vue中，以下哪个生命周期钩子在组件挂载后调用？","options":[{"key":"A","value":"created"},{"key":"B","value":"mounted"},{"key":"C","value":"updated"},{"key":"D","value":"beforeDestroy"}],"answer":"B","analysis":"mounted在组件挂载到DOM后调用，此时可以访问DOM元素。"},
    {"knowledge_point":"前端框架(Vue/React)","category":"专业","career":"前端开发工程师","difficulty":"medium","question_type":"judge","question":"判断：React中的虚拟DOM直接操作浏览器的真实DOM。","options":[{"key":"对","value":"正确"},{"key":"错","value":"错误"}],"answer":"错","analysis":"虚拟DOM是内存中的JS对象表示，通过Diff算法计算差异后再批量更新真实DOM。"},
    {"knowledge_point":"前端框架(Vue/React)","category":"专业","career":"前端开发工程师","difficulty":"hard","question_type":"single_choice","question":"React中，useEffect(fn, [])的依赖数组为空时，effect函数何时执行？","options":[{"key":"A","value":"每次渲染后都执行"},{"key":"B","value":"只在组件挂载时执行一次"},{"key":"C","value":"从不执行"},{"key":"D","value":"组件卸载时执行"}],"answer":"B","analysis":"空依赖数组表示effect不依赖任何变量，因此只在组件挂载时执行一次。"},

    # ========== 网络基础（6题，前端/运维通用） ==========
    {"knowledge_point":"网络基础","category":"专业","career":"前端开发工程师","difficulty":"easy","question_type":"single_choice","question":"HTTP状态码200表示什么？","options":[{"key":"A","value":"请求成功"},{"key":"B","value":"资源未找到"},{"key":"C","value":"服务器错误"},{"key":"D","value":"重定向"}],"answer":"A","analysis":"200 OK表示请求已成功处理。"},
    {"knowledge_point":"网络基础","category":"专业","career":"前端开发工程师","difficulty":"easy","question_type":"single_choice","question":"TCP/IP协议中，IP地址的作用是？","options":[{"key":"A","value":"标识网络中的设备"},{"key":"B","value":"标识应用程序"},{"key":"C","value":"加密数据传输"},{"key":"D","value":"压缩数据包"}],"answer":"A","analysis":"IP地址用于在网络中唯一标识一台主机或网络接口。"},
    {"knowledge_point":"网络基础","category":"专业","career":"前端开发工程师","difficulty":"easy","question_type":"judge","question":"判断：HTTPS使用的是SSL/TLS协议进行加密传输。","options":[{"key":"对","value":"正确"},{"key":"错","value":"错误"}],"answer":"对","analysis":"HTTPS = HTTP + SSL/TLS，通过SSL/TLS协议对通信数据进行加密。"},
    {"knowledge_point":"网络基础","category":"专业","career":"前端开发工程师","difficulty":"medium","question_type":"single_choice","question":"DNS的作用是？","options":[{"key":"A","value":"将域名解析为IP地址"},{"key":"B","value":"分配IP地址"},{"key":"C","value":"加密网络通信"},{"key":"D","value":"路由数据包"}],"answer":"A","analysis":"DNS（域名系统）将人类可读的域名转换为机器可读的IP地址。"},
    {"knowledge_point":"网络基础","category":"专业","career":"前端开发工程师","difficulty":"medium","question_type":"single_choice","question":"以下哪个是TCP协议的特点？","options":[{"key":"A","value":"面向连接"},{"key":"B","value":"不可靠传输"},{"key":"C","value":"无连接"},{"key":"D","value":"不保证顺序"}],"answer":"A","analysis":"TCP是面向连接的、可靠的传输层协议，保证数据顺序和完整性。"},
    {"knowledge_point":"网络基础","category":"专业","career":"前端开发工程师","difficulty":"hard","question_type":"single_choice","question":"OSI七层模型中，HTTP协议属于哪一层？","options":[{"key":"A","value":"传输层"},{"key":"B","value":"应用层"},{"key":"C","value":"网络层"},{"key":"D","value":"会话层"}],"answer":"B","analysis":"HTTP是应用层协议，在OSI模型中属于第7层（应用层）。"},

    # ========== 算法与数据结构（6题，通用专业） ==========
    {"knowledge_point":"算法与数据结构","category":"专业","career":"前端开发工程师","difficulty":"easy","question_type":"single_choice","question":"数组和链表相比，哪个的随机访问效率更高？","options":[{"key":"A","value":"数组"},{"key":"B","value":"链表"},{"key":"C","value":"两者一样"},{"key":"D","value":"取决于数据大小"}],"answer":"A","analysis":"数组支持O(1)随机访问，链表随机访问需要O(n)时间。"},
    {"knowledge_point":"算法与数据结构","category":"专业","career":"前端开发工程师","difficulty":"easy","question_type":"single_choice","question":"栈(Stack)的特点是？","options":[{"key":"A","value":"先进先出(FIFO)"},{"key":"B","value":"后进先出(LIFO)"},{"key":"C","value":"随机访问"},{"key":"D","value":"双端操作"}],"answer":"B","analysis":"栈是一种后进先出（LIFO）的数据结构，类似叠盘子。"},
    {"knowledge_point":"算法与数据结构","category":"专业","career":"前端开发工程师","difficulty":"medium","question_type":"single_choice","question":"二分查找的时间复杂度是？","options":[{"key":"A","value":"O(n)"},{"key":"B","value":"O(log n)"},{"key":"C","value":"O(n²)"},{"key":"D","value":"O(n log n)"}],"answer":"B","analysis":"二分查找每次将搜索范围减半，时间复杂度为O(log n)。"},
    {"knowledge_point":"算法与数据结构","category":"专业","career":"前端开发工程师","difficulty":"medium","question_type":"judge","question":"判断：哈希表的查找时间复杂度总是O(1)。","options":[{"key":"对","value":"正确"},{"key":"错","value":"错误"}],"answer":"错","analysis":"哈希表理想情况下是O(1)，但发生哈希冲突时可能退化为O(n)。"},
    {"knowledge_point":"算法与数据结构","category":"专业","career":"前端开发工程师","difficulty":"hard","question_type":"single_choice","question":"快速排序的平均时间复杂度是？","options":[{"key":"A","value":"O(n)"},{"key":"B","value":"O(n log n)"},{"key":"C","value":"O(n²)"},{"key":"D","value":"O(log n)"}],"answer":"B","analysis":"快速排序平均时间复杂度为O(n log n)，最坏情况为O(n²)。"},
    {"knowledge_point":"算法与数据结构","category":"专业","career":"前端开发工程师","difficulty":"hard","question_type":"single_choice","question":"图的深度优先遍历(DFS)通常使用什么数据结构辅助实现？","options":[{"key":"A","value":"栈"},{"key":"B","value":"队列"},{"key":"C","value":"数组"},{"key":"D","value":"堆"}],"answer":"A","analysis":"DFS常使用栈（递归本质也是栈），BFS使用队列。"},

    # ========== 编程语言(Java/Python/Go)（6题，后端开发工程师） ==========
    {"knowledge_point":"编程语言(Java/Python/Go)","category":"专业","career":"后端开发工程师","difficulty":"easy","question_type":"single_choice","question":"Python中，以下哪个关键字用于定义函数？","options":[{"key":"A","value":"def"},{"key":"B","value":"func"},{"key":"C","value":"define"},{"key":"D","value":"function"}],"answer":"A","analysis":"Python使用def关键字定义函数。"},
    {"knowledge_point":"编程语言(Java/Python/Go)","category":"专业","career":"后端开发工程师","difficulty":"easy","question_type":"single_choice","question":"Java中，以下哪个关键字用于继承？","options":[{"key":"A","value":"extends"},{"key":"B","value":"implements"},{"key":"C","value":"inherit"},{"key":"D","value":"super"}],"answer":"A","analysis":"Java中使用extends关键字表示类的继承关系，implements用于实现接口。"},
    {"knowledge_point":"编程语言(Java/Python/Go)","category":"专业","career":"后端开发工程师","difficulty":"easy","question_type":"judge","question":"判断：Go语言中的goroutine是比线程更轻量的并发执行单元。","options":[{"key":"对","value":"正确"},{"key":"错","value":"错误"}],"answer":"对","analysis":"goroutine由Go运行时管理，栈空间初始仅几KB，比系统线程轻量得多。"},
    {"knowledge_point":"编程语言(Java/Python/Go)","category":"专业","career":"后端开发工程师","difficulty":"medium","question_type":"single_choice","question":"Java中，以下哪个是面向对象的四大特性之一？","options":[{"key":"A","value":"封装"},{"key":"B","value":"编译"},{"key":"C","value":"解释"},{"key":"D","value":"链接"}],"answer":"A","analysis":"面向对象四大特性：封装、继承、多态、抽象。"},
    {"knowledge_point":"编程语言(Java/Python/Go)","category":"专业","career":"后端开发工程师","difficulty":"medium","question_type":"single_choice","question":"Python中，列表推导式[x**2 for x in range(5)]的结果是？","options":[{"key":"A","value":"[0,1,4,9,16]"},{"key":"B","value":"[1,4,9,16,25]"},{"key":"C","value":"[0,2,4,6,8]"},{"key":"D","value":"[0,1,2,3,4]"}],"answer":"A","analysis":"range(5)生成0,1,2,3,4，平方后得到[0,1,4,9,16]。"},
    {"knowledge_point":"编程语言(Java/Python/Go)","category":"专业","career":"后端开发工程师","difficulty":"hard","question_type":"single_choice","question":"Java中，关于volatile关键字的说法正确的是？","options":[{"key":"A","value":"保证原子性"},{"key":"B","value":"保证可见性"},{"key":"C","value":"保证有序性和原子性"},{"key":"D","value":"保证可见性和有序性，不保证原子性"}],"answer":"D","analysis":"volatile保证变量的可见性和禁止指令重排序，但不保证复合操作的原子性。"},

    # ========== 数据库与SQL（6题，后端/数据分析通用） ==========
    {"knowledge_point":"数据库与SQL","category":"专业","career":"后端开发工程师","difficulty":"easy","question_type":"single_choice","question":"SQL中，用于从表中查询数据的语句是？","options":[{"key":"A","value":"INSERT"},{"key":"B","value":"UPDATE"},{"key":"C","value":"SELECT"},{"key":"D","value":"DELETE"}],"answer":"C","analysis":"SELECT语句用于从数据库中查询数据。"},
    {"knowledge_point":"数据库与SQL","category":"专业","career":"后端开发工程师","difficulty":"easy","question_type":"single_choice","question":"关系型数据库中，主键(PRIMARY KEY)的作用是？","options":[{"key":"A","value":"唯一标识一条记录"},{"key":"B","value":"加速查询速度"},{"key":"C","value":"建立表间关联"},{"key":"D","value":"存储大文本数据"}],"answer":"A","analysis":"主键唯一标识表中的每一行记录，不能为空且必须唯一。"},
    {"knowledge_point":"数据库与SQL","category":"专业","career":"后端开发工程师","difficulty":"easy","question_type":"judge","question":"判断：SQL中的NULL表示空字符串。","options":[{"key":"对","value":"正确"},{"key":"错","value":"错误"}],"answer":"错","analysis":"NULL表示缺失或未知的值，不等于空字符串或0。"},
    {"knowledge_point":"数据库与SQL","category":"专业","career":"后端开发工程师","difficulty":"medium","question_type":"single_choice","question":"SQL中的JOIN操作用于？","options":[{"key":"A","value":"合并两个查询的结果"},{"key":"B","value":"根据关联条件连接两个表"},{"key":"C","value":"对查询结果排序"},{"key":"D","value":"对查询结果分组"}],"answer":"B","analysis":"JOIN用于根据两个表之间的关联条件连接数据。"},
    {"knowledge_point":"数据库与SQL","category":"专业","career":"后端开发工程师","difficulty":"medium","question_type":"single_choice","question":"以下哪个是关系型数据库？","options":[{"key":"A","value":"Redis"},{"key":"B","value":"MongoDB"},{"key":"C","value":"MySQL"},{"key":"D","value":"Elasticsearch"}],"answer":"C","analysis":"MySQL是关系型数据库，Redis是键值存储，MongoDB是文档数据库，Elasticsearch是搜索引擎。"},
    {"knowledge_point":"数据库与SQL","category":"专业","career":"后端开发工程师","difficulty":"hard","question_type":"single_choice","question":"数据库事务的ACID特性中，'I'代表什么？","options":[{"key":"A","value":"Integrity（完整性）"},{"key":"B","value":"Isolation（隔离性）"},{"key":"C","value":"Index（索引）"},{"key":"D","value":"Inherit（继承）"}],"answer":"B","analysis":"ACID：原子性(Atomicity)、一致性(Consistency)、隔离性(Isolation)、持久性(Durability)。"},

    # ========== 网络协议（5题，后端开发工程师） ==========
    {"knowledge_point":"网络协议","category":"专业","career":"后端开发工程师","difficulty":"easy","question_type":"single_choice","question":"TCP三次握手中的第二次握手发送的是什么？","options":[{"key":"A","value":"SYN"},{"key":"B","value":"SYN+ACK"},{"key":"C","value":"ACK"},{"key":"D","value":"FIN"}],"answer":"B","analysis":"第二次握手：服务器发送SYN+ACK包，表示收到客户端的SYN并同意建立连接。"},
    {"knowledge_point":"网络协议","category":"专业","career":"后端开发工程师","difficulty":"easy","question_type":"single_choice","question":"HTTP协议默认端口号是？","options":[{"key":"A","value":"21"},{"key":"B","value":"80"},{"key":"C","value":"443"},{"key":"D","value":"8080"}],"answer":"B","analysis":"HTTP默认端口80，HTTPS默认端口443。"},
    {"knowledge_point":"网络协议","category":"专业","career":"后端开发工程师","difficulty":"medium","question_type":"single_choice","question":"以下哪个协议是可靠的传输层协议？","options":[{"key":"A","value":"UDP"},{"key":"B","value":"TCP"},{"key":"C","value":"IP"},{"key":"D","value":"HTTP"}],"answer":"B","analysis":"TCP提供可靠的、面向连接的传输服务，UDP是不可靠的无连接协议。"},
    {"knowledge_point":"网络协议","category":"专业","career":"后端开发工程师","difficulty":"medium","question_type":"judge","question":"判断：WebSocket协议建立在HTTP协议之上。","options":[{"key":"对","value":"正确"},{"key":"错","value":"错误"}],"answer":"对","analysis":"WebSocket通过HTTP的Upgrade握手建立连接，之后切换到WebSocket协议进行全双工通信。"},
    {"knowledge_point":"网络协议","category":"专业","career":"后端开发工程师","difficulty":"hard","question_type":"single_choice","question":"HTTP/2相比HTTP/1.1的主要改进不包括？","options":[{"key":"A","value":"多路复用"},{"key":"B","value":"头部压缩"},{"key":"C","value":"服务器推送"},{"key":"D","value":"明文传输"}],"answer":"D","analysis":"HTTP/2引入了多路复用、头部压缩(HPACK)和服务器推送等特性，且通常基于TLS加密。"},

    # ========== 系统设计（5题，后端开发工程师） ==========
    {"knowledge_point":"系统设计","category":"专业","career":"后端开发工程师","difficulty":"easy","question_type":"single_choice","question":"以下哪个是微服务架构的特点？","options":[{"key":"A","value":"单体部署"},{"key":"B","value":"服务独立部署和扩展"},{"key":"C","value":"共享数据库"},{"key":"D","value":"所有代码在同一个项目中"}],"answer":"B","analysis":"微服务架构将应用拆分为独立部署的服务，每个服务可独立扩展和维护。"},
    {"knowledge_point":"系统设计","category":"专业","career":"后端开发工程师","difficulty":"easy","question_type":"judge","question":"判断：负载均衡可以解决单点故障问题。","options":[{"key":"对","value":"正确"},{"key":"错","value":"错误"}],"answer":"对","analysis":"负载均衡将流量分发到多个后端服务器，即使某台服务器故障，其他服务器仍可继续服务。"},
    {"knowledge_point":"系统设计","category":"专业","career":"后端开发工程师","difficulty":"medium","question_type":"single_choice","question":"缓存穿透是指？","options":[{"key":"A","value":"缓存数据过期"},{"key":"B","value":"请求的数据在缓存和数据库中都不存在"},{"key":"C","value":"缓存雪崩"},{"key":"D","value":"缓存击穿"}],"answer":"B","analysis":"缓存穿透指请求的数据在缓存和数据库中都不存在，导致请求直接打到数据库。"},
    {"knowledge_point":"系统设计","category":"专业","career":"后端开发工程师","difficulty":"medium","question_type":"single_choice","question":"消息队列的主要作用不包括？","options":[{"key":"A","value":"异步解耦"},{"key":"B","value":"流量削峰"},{"key":"C","value":"数据持久化"},{"key":"D","value":"替代数据库"}],"answer":"D","analysis":"消息队列用于异步解耦和流量削峰，不能替代数据库的持久化存储功能。"},
    {"knowledge_point":"系统设计","category":"专业","career":"后端开发工程师","difficulty":"hard","question_type":"single_choice","question":"在分布式系统中，CAP定理中的'P'代表什么？","options":[{"key":"A","value":"Performance（性能）"},{"key":"B","value":"Partition Tolerance（分区容错性）"},{"key":"C","value":"Persistence（持久性）"},{"key":"D","value":"Parallel（并行）"}],"answer":"B","analysis":"CAP定理：一致性(Consistency)、可用性(Availability)、分区容错性(Partition Tolerance)，三者不可兼得。"},

    # ========== 测试基础理论（5题，软件测试工程师） ==========
    {"knowledge_point":"测试基础理论","category":"专业","career":"软件测试工程师","difficulty":"easy","question_type":"single_choice","question":"软件测试中，黑盒测试的依据是？","options":[{"key":"A","value":"源代码"},{"key":"B","value":"需求规格说明"},{"key":"C","value":"程序内部结构"},{"key":"D","value":"算法逻辑"}],"answer":"B","analysis":"黑盒测试基于需求规格说明，不关注内部实现。"},
    {"knowledge_point":"测试基础理论","category":"专业","career":"软件测试工程师","difficulty":"easy","question_type":"single_choice","question":"以下哪个不是测试用例的组成部分？","options":[{"key":"A","value":"测试输入"},{"key":"B","value":"预期结果"},{"key":"C","value":"代码实现"},{"key":"D","value":"测试步骤"}],"answer":"C","analysis":"测试用例包括测试输入、执行步骤、预期结果等，不包括代码实现。"},
    {"knowledge_point":"测试基础理论","category":"专业","career":"软件测试工程师","difficulty":"medium","question_type":"single_choice","question":"边界值分析属于哪种测试方法？","options":[{"key":"A","value":"白盒测试"},{"key":"B","value":"黑盒测试"},{"key":"C","value":"静态测试"},{"key":"D","value":"集成测试"}],"answer":"B","analysis":"边界值分析是黑盒测试的一种常用方法，关注输入域的边界值。"},
    {"knowledge_point":"测试基础理论","category":"专业","career":"软件测试工程师","difficulty":"medium","question_type":"judge","question":"判断：回归测试的目的是验证修改后的代码没有引入新的缺陷。","options":[{"key":"对","value":"正确"},{"key":"错","value":"错误"}],"answer":"对","analysis":"回归测试确保代码变更后原有功能仍然正常工作，没有引入回归缺陷。"},
    {"knowledge_point":"测试基础理论","category":"专业","career":"软件测试工程师","difficulty":"hard","question_type":"single_choice","question":"以下哪个测试级别最早介入？","options":[{"key":"A","value":"系统测试"},{"key":"B","value":"集成测试"},{"key":"C","value":"单元测试"},{"key":"D","value":"验收测试"}],"answer":"C","analysis":"单元测试是测试金字塔的最底层，最早进行，针对最小可测试单元。"},

    # ========== SQL与数据库（共享，数据分析师） ==========
    {"knowledge_point":"SQL与数据库","category":"专业","career":"数据分析师","difficulty":"easy","question_type":"single_choice","question":"SQL中，用于删除数据的语句是？","options":[{"key":"A","value":"DELETE"},{"key":"B","value":"DROP"},{"key":"C","value":"TRUNCATE"},{"key":"D","value":"REMOVE"}],"answer":"A","analysis":"DELETE用于删除表中的数据行，DROP用于删除表结构，TRUNCATE清空表数据。"},
    {"knowledge_point":"SQL与数据库","category":"专业","career":"数据分析师","difficulty":"easy","question_type":"single_choice","question":"SQL中，GROUP BY子句通常与哪个聚合函数一起使用？","options":[{"key":"A","value":"COUNT"},{"key":"B","value":"LENGTH"},{"key":"C","value":"CONCAT"},{"key":"D","value":"REPLACE"}],"answer":"A","analysis":"GROUP BY常与COUNT、SUM、AVG、MAX、MIN等聚合函数配合使用。"},
    {"knowledge_point":"SQL与数据库","category":"专业","career":"数据分析师","difficulty":"medium","question_type":"single_choice","question":"SQL中，SELECT DISTINCT的作用是？","options":[{"key":"A","value":"去除查询结果中的重复行"},{"key":"B","value":"按某列排序"},{"key":"C","value":"筛选特定行"},{"key":"D","value":"连接两个表"}],"answer":"A","analysis":"DISTINCT关键字用于返回唯一不同的值，去除重复行。"},
    {"knowledge_point":"SQL与数据库","category":"专业","career":"数据分析师","difficulty":"medium","question_type":"single_choice","question":"以下SQL语句中，哪个用于创建索引？","options":[{"key":"A","value":"CREATE INDEX"},{"key":"B","value":"CREATE TABLE"},{"key":"C","value":"ALTER INDEX"},{"key":"D","value":"ADD INDEX"}],"answer":"A","analysis":"使用CREATE INDEX语句创建索引，用于加速查询。"},
    {"knowledge_point":"SQL与数据库","category":"专业","career":"数据分析师","difficulty":"hard","question_type":"single_choice","question":"数据库三范式中的第二范式(2NF)要求？","options":[{"key":"A","value":"属性不可再分"},{"key":"B","value":"消除非主属性对主键的部分依赖"},{"key":"C","value":"消除非主属性对主键的传递依赖"},{"key":"D","value":"消除多值依赖"}],"answer":"B","analysis":"1NF要求属性原子性，2NF要求消除部分依赖，3NF要求消除传递依赖。"},

    # ========== 统计学基础（5题，数据分析师） ==========
    {"knowledge_point":"统计学基础","category":"专业","career":"数据分析师","difficulty":"easy","question_type":"single_choice","question":"以下哪个统计量能反映数据的集中趋势？","options":[{"key":"A","value":"均值"},{"key":"B","value":"方差"},{"key":"C","value":"标准差"},{"key":"D","value":"极差"}],"answer":"A","analysis":"均值、中位数、众数反映集中趋势；方差、标准差、极差反映离散程度。"},
    {"knowledge_point":"统计学基础","category":"专业","career":"数据分析师","difficulty":"easy","question_type":"single_choice","question":"概率P(A|B)表示什么？","options":[{"key":"A","value":"A和B同时发生的概率"},{"key":"B","value":"在B发生的条件下A发生的概率"},{"key":"C","value":"A或B发生的概率"},{"key":"D","value":"B发生的概率"}],"answer":"B","analysis":"P(A|B)是条件概率，表示事件B发生的情况下事件A发生的概率。"},
    {"knowledge_point":"统计学基础","category":"专业","career":"数据分析师","difficulty":"medium","question_type":"single_choice","question":"正态分布的特征不包括？","options":[{"key":"A","value":"对称分布"},{"key":"B","value":"均值等于中位数"},{"key":"C","value":"偏态分布"},{"key":"D","value":"钟形曲线"}],"answer":"C","analysis":"正态分布是对称的钟形曲线，不是偏态分布。偏态分布是左偏或右偏的。"},
    {"knowledge_point":"统计学基础","category":"专业","career":"数据分析师","difficulty":"medium","question_type":"judge","question":"判断：相关系数r=0表示两个变量之间没有线性关系。","options":[{"key":"对","value":"正确"},{"key":"错","value":"错误"}],"answer":"对","analysis":"皮尔逊相关系数衡量线性相关程度，r=0表示不存在线性相关，但可能存在其他非线性关系。"},
    {"knowledge_point":"统计学基础","category":"专业","career":"数据分析师","difficulty":"hard","question_type":"single_choice","question":"在假设检验中，第一类错误(Type I Error)是指？","options":[{"key":"A","value":"接受错误的原假设"},{"key":"B","value":"拒绝正确的原假设"},{"key":"C","value":"样本量不足"},{"key":"D","value":"置信区间过宽"}],"answer":"B","analysis":"第一类错误（α错误）是拒绝了实际上正确的原假设（假阳性）。"},

    # ========== 测试相关：接口测试（5题，软件测试工程师） ==========
    {"knowledge_point":"接口测试","category":"专业","career":"软件测试工程师","difficulty":"easy","question_type":"single_choice","question":"接口测试中，RESTful API的GET请求通常用于？","options":[{"key":"A","value":"获取资源"},{"key":"B","value":"创建资源"},{"key":"C","value":"更新资源"},{"key":"D","value":"删除资源"}],"answer":"A","analysis":"GET用于获取资源，POST用于创建，PUT/PATCH用于更新，DELETE用于删除。"},
    {"knowledge_point":"接口测试","category":"专业","career":"软件测试工程师","difficulty":"easy","question_type":"single_choice","question":"HTTP状态码403表示？","options":[{"key":"A","value":"未授权"},{"key":"B","value":"禁止访问"},{"key":"C","value":"资源未找到"},{"key":"D","value":"请求超时"}],"answer":"B","analysis":"403 Forbidden表示服务器理解请求但拒绝执行，通常由于权限不足。"},
    {"knowledge_point":"接口测试","category":"专业","career":"软件测试工程师","difficulty":"medium","question_type":"single_choice","question":"Postman中，设置环境变量的目的是？","options":[{"key":"A","value":"美化界面"},{"key":"B","value":"在不同环境间切换配置"},{"key":"C","value":"记录请求日志"},{"key":"D","value":"生成测试报告"}],"answer":"B","analysis":"Postman环境变量用于在不同环境（如开发、测试、生产）间切换API配置。"},
    {"knowledge_point":"接口测试","category":"专业","career":"软件测试工程师","difficulty":"medium","question_type":"judge","question":"判断：接口测试只需要验证返回的HTTP状态码。","options":[{"key":"对","value":"正确"},{"key":"错","value":"错误"}],"answer":"错","analysis":"接口测试需要验证状态码、响应体内容、响应头、性能等多个维度。"},
    {"knowledge_point":"接口测试","category":"专业","career":"软件测试工程师","difficulty":"hard","question_type":"single_choice","question":"在接口测试中，幂等性是指？","options":[{"key":"A","value":"接口返回结果总是相同"},{"key":"B","value":"多次执行同一操作的结果相同"},{"key":"C","value":"接口响应时间一致"},{"key":"D","value":"接口只能被调用一次"}],"answer":"B","analysis":"幂等性指无论执行多少次，结果都与执行一次相同。GET、PUT、DELETE通常是幂等的。"},

    # ========== 自动化测试（5题，软件测试工程师） ==========
    {"knowledge_point":"自动化测试","category":"专业","career":"软件测试工程师","difficulty":"easy","question_type":"single_choice","question":"Selenium是用于什么测试的工具？","options":[{"key":"A","value":"接口测试"},{"key":"B","value":"UI自动化测试"},{"key":"C","value":"性能测试"},{"key":"D","value":"安全测试"}],"answer":"B","analysis":"Selenium是一个用于Web应用程序UI自动化测试的工具。"},
    {"knowledge_point":"自动化测试","category":"专业","career":"软件测试工程师","difficulty":"easy","question_type":"single_choice","question":"常用的Python自动化测试框架是？","options":[{"key":"A","value":"JUnit"},{"key":"B","value":"pytest"},{"key":"C","value":"Mocha"},{"key":"D","value":"Jasmine"}],"answer":"B","analysis":"pytest是Python最流行的测试框架，JUnit是Java的，Mocha和Jasmine是JavaScript的。"},
    {"knowledge_point":"自动化测试","category":"专业","career":"软件测试工程师","difficulty":"medium","question_type":"single_choice","question":"Page Object模式的主要目的是？","options":[{"key":"A","value":"提高测试速度"},{"key":"B","value":"分离测试逻辑和页面元素"},{"key":"C","value":"减少测试用例数"},{"key":"D","value":"自动生成测试数据"}],"answer":"B","analysis":"Page Object模式将页面元素和操作封装成类，使测试逻辑与页面实现解耦。"},
    {"knowledge_point":"自动化测试","category":"专业","career":"软件测试工程师","difficulty":"medium","question_type":"single_choice","question":"持续集成中，自动化测试通常在哪个阶段执行？","options":[{"key":"A","value":"代码编写前"},{"key":"B","value":"代码提交后自动触发"},{"key":"C","value":"版本发布后"},{"key":"D","value":"项目结束后"}],"answer":"B","analysis":"持续集成中，代码提交后自动触发构建和测试流程，快速反馈问题。"},
    {"knowledge_point":"自动化测试","category":"专业","career":"软件测试工程师","difficulty":"hard","question_type":"single_choice","question":"以下哪种测试不适合自动化？","options":[{"key":"A","value":"回归测试"},{"key":"B","value":"探索性测试"},{"key":"C","value":"冒烟测试"},{"key":"D","value":"数据驱动测试"}],"answer":"B","analysis":"探索性测试依赖测试人员的直觉和经验，需要灵活的探索，不适合自动化。"},

    # ========== Linux基础（5题，软件测试工程师） ==========
    {"knowledge_point":"Linux基础","category":"专业","career":"软件测试工程师","difficulty":"easy","question_type":"single_choice","question":"Linux中，查看当前目录下文件列表的命令是？","options":[{"key":"A","value":"ls"},{"key":"B","value":"cd"},{"key":"C","value":"pwd"},{"key":"D","value":"cat"}],"answer":"A","analysis":"ls命令列出当前目录的文件和子目录。"},
    {"knowledge_point":"Linux基础","category":"专业","career":"软件测试工程师","difficulty":"easy","question_type":"single_choice","question":"Linux中，用于创建新目录的命令是？","options":[{"key":"A","value":"mkdir"},{"key":"B","value":"touch"},{"key":"C","value":"rmdir"},{"key":"D","value":"rm"}],"answer":"A","analysis":"mkdir（make directory）用于创建新目录。"},
    {"knowledge_point":"Linux基础","category":"专业","career":"软件测试工程师","difficulty":"medium","question_type":"single_choice","question":"Linux中，修改文件权限的命令是？","options":[{"key":"A","value":"chmod"},{"key":"B","value":"chown"},{"key":"C","value":"chgrp"},{"key":"D","value":"umask"}],"answer":"A","analysis":"chmod用于修改文件或目录的权限位。"},
    {"knowledge_point":"Linux基础","category":"专业","career":"软件测试工程师","difficulty":"medium","question_type":"judge","question":"判断：Linux中，使用'|'符号可以实现管道操作，将前一个命令的输出作为后一个命令的输入。","options":[{"key":"对","value":"正确"},{"key":"错","value":"错误"}],"answer":"对","analysis":"管道符|将一个命令的标准输出连接到另一个命令的标准输入。"},
    {"knowledge_point":"Linux基础","category":"专业","career":"软件测试工程师","difficulty":"hard","question_type":"single_choice","question":"Linux中，查看进程信息的命令是？","options":[{"key":"A","value":"ps"},{"key":"B","value":"ls"},{"key":"C","value":"du"},{"key":"D","value":"df"}],"answer":"A","analysis":"ps命令显示当前进程的快照信息。"},

    # ========== Python数据分析（5题，数据分析师） ==========
    {"knowledge_point":"Python数据分析","category":"专业","career":"数据分析师","difficulty":"easy","question_type":"single_choice","question":"Python数据分析中最常用的数据处理库是？","options":[{"key":"A","value":"NumPy"},{"key":"B","value":"Pandas"},{"key":"C","value":"Matplotlib"},{"key":"D","value":"Scikit-learn"}],"answer":"B","analysis":"Pandas是Python中最常用的数据处理和分析库，提供DataFrame等数据结构。"},
    {"knowledge_point":"Python数据分析","category":"专业","career":"数据分析师","difficulty":"easy","question_type":"single_choice","question":"Pandas中，读取CSV文件的函数是？","options":[{"key":"A","value":"pd.read_csv()"},{"key":"B","value":"pd.read_excel()"},{"key":"C","value":"pd.read_json()"},{"key":"D","value":"pd.open()"}],"answer":"A","analysis":"pd.read_csv()用于读取CSV格式的数据文件。"},
    {"knowledge_point":"Python数据分析","category":"专业","career":"数据分析师","difficulty":"medium","question_type":"single_choice","question":"Pandas中，用于处理缺失值的函数是？","options":[{"key":"A","value":"dropna()"},{"key":"B","value":"sortna()"},{"key":"C","value":"cleanna()"},{"key":"D","value":"removena()"}],"answer":"A","analysis":"dropna()删除含有缺失值的行或列，fillna()用指定值填充缺失值。"},
    {"knowledge_point":"Python数据分析","category":"专业","career":"数据分析师","difficulty":"medium","question_type":"judge","question":"判断：Matplotlib是Python中用于数据可视化的库。","options":[{"key":"对","value":"正确"},{"key":"错","value":"错误"}],"answer":"对","analysis":"Matplotlib是Python最基础和最广泛使用的数据可视化库。"},
    {"knowledge_point":"Python数据分析","category":"专业","career":"数据分析师","difficulty":"hard","question_type":"single_choice","question":"以下哪个是Scikit-learn中用于划分训练集和测试集的函数？","options":[{"key":"A","value":"train_test_split"},{"key":"B","value":"cross_val_score"},{"key":"C","value":"GridSearchCV"},{"key":"D","value":"StandardScaler"}],"answer":"A","analysis":"train_test_split用于将数据集随机划分为训练集和测试集。"},

    # ========== 业务分析思维（5题，数据分析师） ==========
    {"knowledge_point":"业务分析思维","category":"专业","career":"数据分析师","difficulty":"easy","question_type":"single_choice","question":"数据分析中的'漏斗分析'常用于？","options":[{"key":"A","value":"分析用户转化路径"},{"key":"B","value":"预测未来趋势"},{"key":"C","value":"分类用户群体"},{"key":"D","value":"计算运营成本"}],"answer":"A","analysis":"漏斗分析通过追踪用户在各个环节的转化率，分析流失点和优化机会。"},
    {"knowledge_point":"业务分析思维","category":"专业","career":"数据分析师","difficulty":"easy","question_type":"single_choice","question":"A/B测试的目的是？","options":[{"key":"A","value":"比较两个版本的性能差异"},{"key":"B","value":"测试软件兼容性"},{"key":"C","value":"检查代码Bug"},{"key":"D","value":"自动化测试"}],"answer":"A","analysis":"A/B测试通过对比实验评估两个或多个版本的差异效果。"},
    {"knowledge_point":"业务分析思维","category":"专业","career":"数据分析师","difficulty":"medium","question_type":"single_choice","question":"RFM模型中，'F'代表什么？","options":[{"key":"A","value":"Frequency（消费频率）"},{"key":"B","value":"Feature（特征）"},{"key":"C","value":"Factor（因素）"},{"key":"D","value":"Format（格式）"}],"answer":"A","analysis":"RFM：Recency（最近消费时间）、Frequency（消费频率）、Monetary（消费金额）。"},
    {"knowledge_point":"业务分析思维","category":"专业","career":"数据分析师","difficulty":"medium","question_type":"judge","question":"判断：数据指标的波动越大越有分析价值。","options":[{"key":"对","value":"正确"},{"key":"错","value":"错误"}],"answer":"错","analysis":"指标波动大可能意味着数据不稳定或异常，需要区分有效波动和噪声。"},
    {"knowledge_point":"业务分析思维","category":"专业","career":"数据分析师","difficulty":"hard","question_type":"single_choice","question":"以下哪个是衡量用户粘性的核心指标？","options":[{"key":"A","value":"DAU/MAU"},{"key":"B","value":"ARPU"},{"key":"C","value":"CAC"},{"key":"D","value":"LTV"}],"answer":"A","analysis":"DAU/MAU（日活跃用户/月活跃用户）反映用户回访频率，是衡量用户粘性的核心指标。"},

    # ========== Excel（5题，数据分析师） ==========
    {"knowledge_point":"Excel","category":"专业","career":"数据分析师","difficulty":"easy","question_type":"single_choice","question":"Excel中，用于查询和引用数据的函数是？","options":[{"key":"A","value":"VLOOKUP"},{"key":"B","value":"SUM"},{"key":"C","value":"AVERAGE"},{"key":"D","value":"COUNT"}],"answer":"A","analysis":"VLOOKUP用于在表格中按列查找并返回匹配行的值。"},
    {"knowledge_point":"Excel","category":"专业","career":"数据分析师","difficulty":"easy","question_type":"single_choice","question":"Excel中，数据透视表的主要作用是？","options":[{"key":"A","value":"快速汇总和分析大量数据"},{"key":"B","value":"制作图表"},{"key":"C","value":"编写函数"},{"key":"D","value":"格式化单元格"}],"answer":"A","analysis":"数据透视表用于对大量数据进行快速汇总、交叉分析和报表生成。"},
    {"knowledge_point":"Excel","category":"专业","career":"数据分析师","difficulty":"medium","question_type":"single_choice","question":"Excel中，条件格式的功能是？","options":[{"key":"A","value":"根据条件自动设置单元格格式"},{"key":"B","value":"筛选数据"},{"key":"C","value":"排序数据"},{"key":"D","value":"合并单元格"}],"answer":"A","analysis":"条件格式根据指定条件自动应用格式（如颜色、图标），便于数据可视化。"},
    {"knowledge_point":"Excel","category":"专业","career":"数据分析师","difficulty":"medium","question_type":"judge","question":"判断：Excel中的$A$1是绝对引用，无论公式如何复制引用的单元格不变。","options":[{"key":"对","value":"正确"},{"key":"错","value":"错误"}],"answer":"对","analysis":"绝对引用使用$符号，行号和列号固定不变，复制公式时不会改变。"},
    {"knowledge_point":"Excel","category":"专业","career":"数据分析师","difficulty":"hard","question_type":"single_choice","question":"Excel中，INDEX和MATCH函数组合使用相比VLOOKUP的优势是？","options":[{"key":"A","value":"可以向左查找"},{"key":"B","value":"只能向右查找"},{"key":"C","value":"只能查找数字"},{"key":"D","value":"速度更慢"}],"answer":"A","analysis":"VLOOKUP只能向右查找，而INDEX+MATCH组合可以向左查找，更灵活。"},

    # ========== 网络安全基础（5题，网络安全工程师） ==========
    {"knowledge_point":"网络安全基础","category":"专业","career":"网络安全工程师","difficulty":"easy","question_type":"single_choice","question":"以下哪个是常见的网络攻击类型？","options":[{"key":"A","value":"SQL注入"},{"key":"B","value":"数据备份"},{"key":"C","value":"代码编译"},{"key":"D","value":"负载均衡"}],"answer":"A","analysis":"SQL注入是通过在输入中插入SQL代码来攻击数据库的常见网络攻击方式。"},
    {"knowledge_point":"网络安全基础","category":"专业","career":"网络安全工程师","difficulty":"easy","question_type":"single_choice","question":"防火墙的主要功能是？","options":[{"key":"A","value":"监控和过滤网络流量"},{"key":"B","value":"加速网络速度"},{"key":"C","value":"存储网络数据"},{"key":"D","value":"加密通信内容"}],"answer":"A","analysis":"防火墙根据预设规则监控和过滤进出的网络流量，阻止未经授权的访问。"},
    {"knowledge_point":"网络安全基础","category":"专业","career":"网络安全工程师","difficulty":"medium","question_type":"single_choice","question":"DDoS攻击的目标是？","options":[{"key":"A","value":"窃取用户数据"},{"key":"B","value":"耗尽目标资源使其无法服务"},{"key":"C","value":"修改系统配置"},{"key":"D","value":"植入病毒"}],"answer":"B","analysis":"DDoS（分布式拒绝服务）攻击通过大量请求耗尽目标系统资源，导致正常用户无法访问。"},
    {"knowledge_point":"网络安全基础","category":"专业","career":"网络安全工程师","difficulty":"medium","question_type":"judge","question":"判断：HTTPS可以完全防止中间人攻击。","options":[{"key":"对","value":"正确"},{"key":"错","value":"错误"}],"answer":"错","analysis":"HTTPS大大增加了中间人攻击的难度，但不能完全防止（如证书劫持等）。"},
    {"knowledge_point":"网络安全基础","category":"专业","career":"网络安全工程师","difficulty":"hard","question_type":"single_choice","question":"OWASP Top 10中排名第一的安全风险通常是？","options":[{"key":"A","value":"注入攻击"},{"key":"B","value":"XSS"},{"key":"C","value":"失效的身份验证"},{"key":"D","value":"敏感数据泄露"}],"answer":"A","analysis":"OWASP Top 10中，注入攻击（如SQL注入）长期占据首位。"},

    # ========== 密码学（5题，网络安全工程师） ==========
    {"knowledge_point":"密码学","category":"专业","career":"网络安全工程师","difficulty":"easy","question_type":"single_choice","question":"对称加密和非对称加密的主要区别是？","options":[{"key":"A","value":"使用相同或不同的密钥"},{"key":"B","value":"加密速度不同"},{"key":"C","value":"密钥长度不同"},{"key":"D","value":"以上都是"}],"answer":"A","analysis":"对称加密使用同一密钥加解密，非对称加密使用公钥和私钥对。"},
    {"knowledge_point":"密码学","category":"专业","career":"网络安全工程师","difficulty":"easy","question_type":"single_choice","question":"以下哪个是常见的对称加密算法？","options":[{"key":"A","value":"AES"},{"key":"B","value":"RSA"},{"key":"C","value":"DSA"},{"key":"D","value":"ECDSA"}],"answer":"A","analysis":"AES是高级加密标准，是一种对称加密算法。RSA、DSA、ECDSA是非对称加密。"},
    {"knowledge_point":"密码学","category":"专业","career":"网络安全工程师","difficulty":"medium","question_type":"single_choice","question":"哈希算法的主要特点不包括？","options":[{"key":"A","value":"不可逆"},{"key":"B","value":"定长输出"},{"key":"C","value":"可解密"},{"key":"D","value":"抗碰撞"}],"answer":"C","analysis":"哈希算法是单向的，不可逆，无法从哈希值还原原始数据。"},
    {"knowledge_point":"密码学","category":"专业","career":"网络安全工程师","difficulty":"medium","question_type":"single_choice","question":"数字签名的主要作用是？","options":[{"key":"A","value":"加密数据"},{"key":"B","value":"验证身份和完整性"},{"key":"C","value":"压缩数据"},{"key":"D","value":"加速传输"}],"answer":"B","analysis":"数字签名用于验证发送者身份和消息的完整性，不可否认。"},
    {"knowledge_point":"密码学","category":"专业","career":"网络安全工程师","difficulty":"hard","question_type":"single_choice","question":"RSA算法的安全性基于？","options":[{"key":"A","value":"大整数分解的困难性"},{"key":"B","value":"离散对数问题"},{"key":"C","value":"椭圆曲线问题"},{"key":"D","value":"哈希碰撞"}],"answer":"A","analysis":"RSA的安全性基于大整数因子分解的数学难题。"},

    # ========== 产品设计（5题，产品经理） ==========
    {"knowledge_point":"产品设计","category":"专业","career":"产品经理","difficulty":"easy","question_type":"single_choice","question":"MVP(Minimum Viable Product)的概念是指？","options":[{"key":"A","value":"功能最全的产品"},{"key":"B","value":"具备核心功能的最小化可行产品"},{"key":"C","value":"最便宜的产品"},{"key":"D","value":"代码最精简的产品"}],"answer":"B","analysis":"MVP是最小可行产品，用最少的功能验证核心假设和用户需求。"},
    {"knowledge_point":"产品设计","category":"专业","career":"产品经理","difficulty":"easy","question_type":"single_choice","question":"产品需求文档(PRD)的主要受众是？","options":[{"key":"A","value":"最终用户"},{"key":"B","value":"开发和测试团队"},{"key":"C","value":"投资人"},{"key":"D","value":"销售团队"}],"answer":"B","analysis":"PRD面向开发和测试团队，描述产品功能和需求细节。"},
    {"knowledge_point":"产品设计","category":"专业","career":"产品经理","difficulty":"medium","question_type":"single_choice","question":"Kano模型中，\"基本型需求\"的特点是？","options":[{"key":"A","value":"不满足时用户非常不满，满足时用户不会特别满意"},{"key":"B","value":"满足时用户非常满意，不满足时用户无所谓"},{"key":"C","value":"满足和不满都不会影响用户满意度"},{"key":"D","value":"与用户满意度成线性关系"}],"answer":"A","analysis":"基本型需求（如手机能打电话）是必须的，不满足则极大不满，满足也不会增加满意度。"},
    {"knowledge_point":"产品设计","category":"专业","career":"产品经理","difficulty":"medium","question_type":"judge","question":"判断：用户故事(User Story)的标准格式是'作为...，我想要...，以便...'。","options":[{"key":"对","value":"正确"},{"key":"错","value":"错误"}],"answer":"对","analysis":"用户故事标准格式：As a [角色], I want [功能], so that [价值]。"},
    {"knowledge_point":"产品设计","category":"专业","career":"产品经理","difficulty":"hard","question_type":"single_choice","question":"以下哪个工具通常用于产品路线图的规划？","options":[{"key":"A","value":"Jira"},{"key":"B","value":"Photoshop"},{"key":"C","value":"MySQL"},{"key":"D","value":"Postman"}],"answer":"A","analysis":"Jira是常用的项目管理和产品路线图工具，支持敏捷开发和需求跟踪。"},

    # ========== 机器学习（5题，算法工程师） ==========
    {"knowledge_point":"机器学习","category":"专业","career":"算法工程师","difficulty":"easy","question_type":"single_choice","question":"以下哪个是监督学习算法？","options":[{"key":"A","value":"K-means聚类"},{"key":"B","value":"线性回归"},{"key":"C","value":"PCA"},{"key":"D","value":"Apriori"}],"answer":"B","analysis":"线性回归是有标签数据的监督学习算法。K-means、PCA、Apriori是无监督学习。"},
    {"knowledge_point":"机器学习","category":"专业","career":"算法工程师","difficulty":"easy","question_type":"single_choice","question":"过拟合是指？","options":[{"key":"A","value":"模型在训练集上表现差"},{"key":"B","value":"模型在训练集上表现好但在测试集上表现差"},{"key":"C","value":"模型训练时间过长"},{"key":"D","value":"模型参数太少"}],"answer":"B","analysis":"过拟合指模型过度学习训练数据特征，导致泛化能力下降。"},
    {"knowledge_point":"机器学习","category":"专业","career":"算法工程师","difficulty":"medium","question_type":"single_choice","question":"在分类任务中，混淆矩阵的横轴通常表示？","options":[{"key":"A","value":"真实类别"},{"key":"B","value":"预测类别"},{"key":"C","value":"样本数量"},{"key":"D","value":"特征数量"}],"answer":"A","analysis":"混淆矩阵中，行通常表示真实类别，列表示预测类别。"},
    {"knowledge_point":"机器学习","category":"专业","career":"算法工程师","difficulty":"medium","question_type":"single_choice","question":"决策树中，信息增益是依据哪个指标计算的？","options":[{"key":"A","value":"熵"},{"key":"B","value":"方差"},{"key":"C","value":"均值"},{"key":"D","value":"标准差"}],"answer":"A","analysis":"信息增益基于熵的减少量来选择最优划分特征。"},
    {"knowledge_point":"机器学习","category":"专业","career":"算法工程师","difficulty":"hard","question_type":"single_choice","question":"随机森林属于哪种集成学习方法？","options":[{"key":"A","value":"Bagging"},{"key":"B","value":"Boosting"},{"key":"C","value":"Stacking"},{"key":"D","value":"Voting"}],"answer":"A","analysis":"随机森林是基于Bagging思想的集成方法，对多个决策树的结果进行投票。"},

    # ========== 深度学习（5题，算法工程师） ==========
    {"knowledge_point":"深度学习","category":"专业","career":"算法工程师","difficulty":"easy","question_type":"single_choice","question":"以下哪个是深度学习中的激活函数？","options":[{"key":"A","value":"ReLU"},{"key":"B","value":"K-means"},{"key":"C","value":"PCA"},{"key":"D","value":"SVM"}],"answer":"A","analysis":"ReLU（修正线性单元）是深度学习中常用的激活函数。"},
    {"knowledge_point":"深度学习","category":"专业","career":"算法工程师","difficulty":"easy","question_type":"single_choice","question":"卷积神经网络(CNN)主要用于处理什么类型的数据？","options":[{"key":"A","value":"图像数据"},{"key":"B","value":"文本数据"},{"key":"C","value":"音频数据"},{"key":"D","value":"表格数据"}],"answer":"A","analysis":"CNN通过卷积操作提取图像的空间特征，广泛应用于计算机视觉领域。"},
    {"knowledge_point":"深度学习","category":"专业","career":"算法工程师","difficulty":"medium","question_type":"single_choice","question":"在RNN中，梯度消失问题的常用解决方案是？","options":[{"key":"A","value":"LSTM/GRU"},{"key":"B","value":"Dropout"},{"key":"C","value":"Batch Normalization"},{"key":"D","value":"数据增强"}],"answer":"A","analysis":"LSTM（长短期记忆网络）和GRU通过门控机制有效缓解梯度消失问题。"},
    {"knowledge_point":"深度学习","category":"专业","career":"算法工程师","difficulty":"medium","question_type":"judge","question":"判断：深度学习模型的层数越多，模型的性能一定越好。","options":[{"key":"对","value":"正确"},{"key":"错","value":"错误"}],"answer":"错","analysis":"层数过多可能导致过拟合、梯度消失/爆炸等问题，不一定提升性能。"},
    {"knowledge_point":"深度学习","category":"专业","career":"算法工程师","difficulty":"hard","question_type":"single_choice","question":"Transformer架构中，自注意力机制(Self-Attention)的计算复杂度是？","options":[{"key":"A","value":"O(n)"},{"key":"B","value":"O(n²)"},{"key":"C","value":"O(n log n)"},{"key":"D","value":"O(1)"}],"answer":"B","analysis":"标准自注意力的计算复杂度为O(n²)，其中n是序列长度。"},

    # ========== 数据结构（算法工程师共享，复用前文） ==========
    # 这里加一个算法工程师专属的题目
    {"knowledge_point":"数据结构","category":"专业","career":"算法工程师","difficulty":"easy","question_type":"single_choice","question":"二叉树的前序遍历顺序是？","options":[{"key":"A","value":"根-左-右"},{"key":"B","value":"左-根-右"},{"key":"C","value":"左-右-根"},{"key":"D","value":"根-右-左"}],"answer":"A","analysis":"前序遍历：先访问根节点，再遍历左子树，最后遍历右子树。"},
    {"knowledge_point":"数据结构","category":"专业","career":"算法工程师","difficulty":"medium","question_type":"single_choice","question":"平衡二叉树(AVL)的平衡因子范围是？","options":[{"key":"A","value":"[-1, 1]"},{"key":"B","value":"[-2, 2]"},{"key":"C","value":"[0, 1]"},{"key":"D","value":"[-1, 0]"}],"answer":"A","analysis":"AVL树的每个节点的左右子树高度差不超过1（即-1, 0, 1）。"},
    {"knowledge_point":"数据结构","category":"专业","career":"算法工程师","difficulty":"hard","question_type":"single_choice","question":"哈希冲突的解决方法不包括？","options":[{"key":"A","value":"链地址法"},{"key":"B","value":"开放地址法"},{"key":"C","value":"再哈希法"},{"key":"D","value":"冒泡排序"}],"answer":"D","analysis":"链地址法、开放地址法、再哈希法是常见的哈希冲突处理方法，冒泡排序是排序算法。"},

    # ========== 数学基础（5题，算法工程师） ==========
    {"knowledge_point":"数学基础","category":"专业","career":"算法工程师","difficulty":"easy","question_type":"single_choice","question":"矩阵的转置操作是指？","options":[{"key":"A","value":"将矩阵的行和列互换"},{"key":"B","value":"将矩阵的元素取相反数"},{"key":"C","value":"将矩阵旋转90度"},{"key":"D","value":"计算矩阵的逆"}],"answer":"A","analysis":"矩阵转置将行变为列，列变为行。"},
    {"knowledge_point":"数学基础","category":"专业","career":"算法工程师","difficulty":"easy","question_type":"single_choice","question":"概率论中，所有可能事件概率之和为？","options":[{"key":"A","value":"0"},{"key":"B","value":"1"},{"key":"C","value":"100"},{"key":"D","value":"无穷大"}],"answer":"B","analysis":"根据概率公理，样本空间中所有事件的概率之和为1。"},
    {"knowledge_point":"数学基础","category":"专业","career":"算法工程师","difficulty":"medium","question_type":"single_choice","question":"梯度下降法中的学习率过大会导致？","options":[{"key":"A","value":"收敛速度加快"},{"key":"B","value":"可能无法收敛"},{"key":"C","value":"模型更准确"},{"key":"D","value":"过拟合"}],"answer":"B","analysis":"学习率过大可能导致参数在最优值附近震荡甚至发散，无法收敛。"},
    {"knowledge_point":"数学基础","category":"专业","career":"算法工程师","difficulty":"medium","question_type":"judge","question":"判断：两个向量正交的点积为0。","options":[{"key":"对","value":"正确"},{"key":"错","value":"错误"}],"answer":"对","analysis":"正交向量的点积为0，这是正交的定义。"},
    {"knowledge_point":"数学基础","category":"专业","career":"算法工程师","difficulty":"hard","question_type":"single_choice","question":"拉格朗日乘数法用于解决什么类型的优化问题？","options":[{"key":"A","value":"无约束优化"},{"key":"B","value":"有等式约束的优化"},{"key":"C","value":"有不等式约束的优化"},{"key":"D","value":"离散优化"}],"answer":"B","analysis":"拉格朗日乘数法将有等式约束的优化问题转化为无约束问题进行求解。"},

    # ========== Docker/K8s（5题，运维工程师） ==========
    {"knowledge_point":"Docker/K8s","category":"专业","career":"运维工程师","difficulty":"easy","question_type":"single_choice","question":"Docker的核心概念不包括以下哪个？","options":[{"key":"A","value":"镜像(Image)"},{"key":"B","value":"容器(Container)"},{"key":"C","value":"仓库(Repository)"},{"key":"D","value":"虚拟机(VM)"}],"answer":"D","analysis":"Docker三大核心概念：镜像、容器、仓库。虚拟机是传统虚拟化技术，非Docker核心概念。"},
    {"knowledge_point":"Docker/K8s","category":"专业","career":"运维工程师","difficulty":"easy","question_type":"single_choice","question":"Kubernetes中，用于管理Pod副本数的资源对象是？","options":[{"key":"A","value":"Deployment"},{"key":"B","value":"Service"},{"key":"C","value":"ConfigMap"},{"key":"D","value":"Ingress"}],"answer":"A","analysis":"Deployment负责管理Pod副本数，支持滚动更新和回滚。"},
    {"knowledge_point":"Docker/K8s","category":"专业","career":"运维工程师","difficulty":"medium","question_type":"single_choice","question":"Dockerfile中的CMD和ENTRYPOINT的区别是？","options":[{"key":"A","value":"没有区别"},{"key":"B","value":"CMD可以被覆盖，ENTRYPOINT默认不可被覆盖"},{"key":"C","value":"ENTRYPOINT可以被覆盖，CMD不可被覆盖"},{"key":"D","value":"CMD用于构建阶段，ENTRYPOINT用于运行阶段"}],"answer":"B","analysis":"CMD提供默认命令并可被docker run参数覆盖，ENTRYPOINT设置容器主命令。"},
    {"knowledge_point":"Docker/K8s","category":"专业","career":"运维工程师","difficulty":"medium","question_type":"judge","question":"判断：Kubernetes中，Pod是调度的最小单元。","options":[{"key":"对","value":"正确"},{"key":"错","value":"错误"}],"answer":"对","analysis":"Pod是Kubernetes中最小的可调度和管理的计算单元。"},
    {"knowledge_point":"Docker/K8s","category":"专业","career":"运维工程师","difficulty":"hard","question_type":"single_choice","question":"Kubernetes中，Service的类型不包括？","options":[{"key":"A","value":"ClusterIP"},{"key":"B","value":"NodePort"},{"key":"C","value":"LoadBalancer"},{"key":"D","value":"StorageClass"}],"answer":"D","analysis":"Service类型：ClusterIP、NodePort、LoadBalancer、ExternalName。StorageClass是存储相关资源。"},

    # ========== CI/CD（5题，运维工程师） ==========
    {"knowledge_point":"CI/CD","category":"专业","career":"运维工程师","difficulty":"easy","question_type":"single_choice","question":"CI/CD中的'CI'代表什么？","options":[{"key":"A","value":"Continuous Integration"},{"key":"B","value":"Computer Interface"},{"key":"C","value":"Code Inspection"},{"key":"D","value":"Configuration Item"}],"answer":"A","analysis":"CI/CD：Continuous Integration（持续集成）/ Continuous Deployment（持续部署）。"},
    {"knowledge_point":"CI/CD","category":"专业","career":"运维工程师","difficulty":"easy","question_type":"single_choice","question":"以下哪个是流行的CI/CD工具？","options":[{"key":"A","value":"Jenkins"},{"key":"B","value":"Photoshop"},{"key":"C","value":"MySQL"},{"key":"D","value":"Redis"}],"answer":"A","analysis":"Jenkins是开源的自动化CI/CD工具，支持构建、测试和部署流水线。"},
    {"knowledge_point":"CI/CD","category":"专业","career":"运维工程师","difficulty":"medium","question_type":"single_choice","question":"GitLab CI中，.gitlab-ci.yml文件的作用是？","options":[{"key":"A","value":"配置CI/CD流水线"},{"key":"B","value":"配置数据库连接"},{"key":"C","value":"配置服务器参数"},{"key":"D","value":"配置文件存储"}],"answer":"A","analysis":".gitlab-ci.yml是GitLab CI/CD的配置文件，定义流水线的阶段、作业和触发条件。"},
    {"knowledge_point":"CI/CD","category":"专业","career":"运维工程师","difficulty":"medium","question_type":"single_choice","question":"在CI/CD流水线中，'构建(Build)'阶段通常不包括？","options":[{"key":"A","value":"编译源代码"},{"key":"B","value":"运行单元测试"},{"key":"C","value":"部署到生产环境"},{"key":"D","value":"打包成可部署的制品"}],"answer":"C","analysis":"部署到生产环境通常属于CD阶段，构建阶段包括编译、测试和打包。"},
    {"knowledge_point":"CI/CD","category":"专业","career":"运维工程师","difficulty":"hard","question_type":"single_choice","question":"蓝绿部署(Blue-Green Deployment)的最大优点是？","options":[{"key":"A","value":"零停机部署和快速回滚"},{"key":"B","value":"节省服务器资源"},{"key":"C","value":"不需要自动化工具"},{"key":"D","value":"不需要测试"}],"answer":"A","analysis":"蓝绿部署通过维护两套环境实现零停机切换和快速回滚。"},

    # ========== 设计基础（5题，UI/UX设计师） ==========
    {"knowledge_point":"设计基础","category":"专业","career":"UI/UX设计师","difficulty":"easy","question_type":"single_choice","question":"色彩构成中，三原色是指？","options":[{"key":"A","value":"红黄蓝"},{"key":"B","value":"红绿蓝"},{"key":"C","value":"青品黄"},{"key":"D","value":"黑白灰"}],"answer":"A","analysis":"绘画/设计中的三原色是红(Red)、黄(Yellow)、蓝(Blue)。RGB是光的三原色。"},
    {"knowledge_point":"设计基础","category":"专业","career":"UI/UX设计师","difficulty":"easy","question_type":"single_choice","question":"以下哪个是排版设计的基本要素？","options":[{"key":"A","value":"字体的选择"},{"key":"B","value":"数据库设计"},{"key":"C","value":"网络协议"},{"key":"D","value":"算法复杂度"}],"answer":"A","analysis":"排版设计涉及字体、字号、行距、字距等基本要素。"},
    {"knowledge_point":"设计基础","category":"专业","career":"UI/UX设计师","difficulty":"medium","question_type":"single_choice","question":"菲茨定律(Fitts's Law)在UI设计中的启示是？","options":[{"key":"A","value":"重要操作元素应足够大且靠近用户"},{"key":"B","value":"颜色越丰富越好"},{"key":"C","value":"动画越多越好"},{"key":"D","value":"字体越小越好"}],"answer":"A","analysis":"菲茨定律指出，目标的大小和距离影响操作效率，重要元素应大而近。"},
    {"knowledge_point":"设计基础","category":"专业","career":"UI/UX设计师","difficulty":"medium","question_type":"judge","question":"判断：在UI设计中，使用过多的字体和颜色可以增强视觉层次感。","options":[{"key":"对","value":"正确"},{"key":"错","value":"错误"}],"answer":"错","analysis":"过多的字体和颜色会导致视觉混乱，好的设计通常控制字体和颜色数量。"},
    {"knowledge_point":"设计基础","category":"专业","career":"UI/UX设计师","difficulty":"hard","question_type":"single_choice","question":"格式塔原理(Gestalt Principles)中，\"接近性\"原理是指？","options":[{"key":"A","value":"距离相近的元素被视为一组"},{"key":"B","value":"相似的形状被视为一组"},{"key":"C","value":"闭合的图形被视为整体"},{"key":"D","value":"连续的线条被视为整体"}],"answer":"A","analysis":"接近性原理：物理位置相近的元素被感知为属于同一组。"},

    # ========== 内容运营（5题，运营专员） ==========
    {"knowledge_point":"内容运营","category":"专业","career":"运营专员","difficulty":"easy","question_type":"single_choice","question":"内容运营的核心目标包括？","options":[{"key":"A","value":"生产优质内容并触达目标用户"},{"key":"B","value":"编写代码"},{"key":"C","value":"设计数据库"},{"key":"D","value":"配置服务器"}],"answer":"A","analysis":"内容运营通过内容生产、分发和优化来吸引和留住用户。"},
    {"knowledge_point":"内容运营","category":"专业","career":"运营专员","difficulty":"easy","question_type":"single_choice","question":"公众号推文的标题在内容运营中属于哪个环节？","options":[{"key":"A","value":"内容分发"},{"key":"B","value":"内容生产"},{"key":"C","value":"数据复盘"},{"key":"D","value":"用户互动"}],"answer":"B","analysis":"标题写作属于内容生产环节的一部分。"},
    {"knowledge_point":"内容运营","category":"专业","career":"运营专员","difficulty":"medium","question_type":"single_choice","question":"内容运营中，'打开率'衡量的是？","options":[{"key":"A","value":"看到内容后点击阅读的用户比例"},{"key":"B","value":"分享内容的用户比例"},{"key":"C","value":"收藏内容的用户比例"},{"key":"D","value":"点赞的用户比例"}],"answer":"A","analysis":"打开率=阅读人数/推送到达人数，反映标题和封面图的吸引力。"},
    {"knowledge_point":"内容运营","category":"专业","career":"运营专员","difficulty":"medium","question_type":"single_choice","question":"SEO中的关键词密度一般建议控制在什么范围？","options":[{"key":"A","value":"2%-8%"},{"key":"B","value":"20%-30%"},{"key":"C","value":"50%以上"},{"key":"D","value":"越低越好"}],"answer":"A","analysis":"合理的关键词密度通常在2%-8%之间，过高可能被搜索引擎判定为作弊。"},
    {"knowledge_point":"内容运营","category":"专业","career":"运营专员","difficulty":"hard","question_type":"single_choice","question":"内容运营的AARRR模型中，第一个'A'代表什么？","options":[{"key":"A","value":"Acquisition（获取）"},{"key":"B","value":"Activation（激活）"},{"key":"C","value":"Retention（留存）"},{"key":"D","value":"Revenue（收入）"}],"answer":"A","analysis":"AARRR海盗模型：Acquisition获取→Activation激活→Retention留存→Revenue变现→Referral推荐。"},

    # ========== 市场营销（5题，市场营销） ==========
    {"knowledge_point":"市场分析","category":"专业","career":"市场营销","difficulty":"easy","question_type":"single_choice","question":"PEST分析中的'P'代表什么？","options":[{"key":"A","value":"Political（政治因素）"},{"key":"B","value":"Price（价格）"},{"key":"C","value":"Product（产品）"},{"key":"D","value":"Promotion（促销）"}],"answer":"A","analysis":"PEST：Political（政治）、Economic（经济）、Social（社会）、Technological（技术）。"},
    {"knowledge_point":"市场分析","category":"专业","career":"市场营销","difficulty":"easy","question_type":"single_choice","question":"4P营销理论不包括以下哪个？","options":[{"key":"A","value":"Product（产品）"},{"key":"B","value":"Price（价格）"},{"key":"C","value":"Place（渠道）"},{"key":"D","value":"People（人员）"}],"answer":"D","analysis":"4P：Product、Price、Place、Promotion。People是7P中的扩展。"},
    {"knowledge_point":"市场分析","category":"专业","career":"市场营销","difficulty":"medium","question_type":"single_choice","question":"STP营销战略中的'S'代表什么？","options":[{"key":"A","value":"Segmentation（市场细分）"},{"key":"B","value":"Strategy（战略）"},{"key":"C","value":"Sales（销售）"},{"key":"D","value":"Service（服务）"}],"answer":"A","analysis":"STP：Segmentation（细分）、Targeting（目标）、Positioning（定位）。"},
    {"knowledge_point":"市场分析","category":"专业","career":"市场营销","difficulty":"medium","question_type":"single_choice","question":"在品牌管理中，品牌资产(Brand Equity)的核心维度不包括？","options":[{"key":"A","value":"品牌知名度"},{"key":"B","value":"品牌联想"},{"key":"C","value":"生产成本"},{"key":"D","value":"品牌忠诚度"}],"answer":"C","analysis":"品牌资产的核心维度包括品牌知名度、品牌联想、品牌忠诚度和感知质量。"},
    {"knowledge_point":"市场分析","category":"专业","career":"市场营销","difficulty":"hard","question_type":"single_choice","question":"净推荐值(NPS)的计算方式是？","options":[{"key":"A","value":"推荐者比例-贬损者比例"},{"key":"B","value":"推荐者比例+贬损者比例"},{"key":"C","value":"推荐者比例×贬损者比例"},{"key":"D","value":"推荐者比例÷贬损者比例"}],"answer":"A","analysis":"NPS = %推荐者(9-10分) - %贬损者(0-6分)。"},

    # ========== 后端开发（5题，全栈开发工程师） ==========
    {"knowledge_point":"后端开发","category":"专业","career":"全栈开发工程师","difficulty":"easy","question_type":"single_choice","question":"RESTful API中，POST请求通常用于？","options":[{"key":"A","value":"创建新资源"},{"key":"B","value":"获取资源"},{"key":"C","value":"删除资源"},{"key":"D","value":"查询资源"}],"answer":"A","analysis":"POST用于创建新资源，GET用于获取资源，DELETE用于删除。"},
    {"knowledge_point":"后端开发","category":"专业","career":"全栈开发工程师","difficulty":"easy","question_type":"single_choice","question":"ORM(Object-Relational Mapping)的主要作用是？","options":[{"key":"A","value":"将对象映射到数据库表"},{"key":"B","value":"加速页面加载"},{"key":"C","value":"压缩图片"},{"key":"D","value":"管理前端路由"}],"answer":"A","analysis":"ORM将编程语言中的对象模型映射到关系数据库的表结构。"},
    {"knowledge_point":"后端开发","category":"专业","career":"全栈开发工程师","difficulty":"medium","question_type":"single_choice","question":"JWT(JSON Web Token)通常用于？","options":[{"key":"A","value":"用户身份认证"},{"key":"B","value":"数据库查询"},{"key":"C","value":"文件上传"},{"key":"D","value":"日志记录"}],"answer":"A","analysis":"JWT是一种紧凑的、自包含的令牌格式，常用于用户身份认证和信息交换。"},
    {"knowledge_point":"后端开发","category":"专业","career":"全栈开发工程师","difficulty":"medium","question_type":"judge","question":"判断：GraphQL相比REST API的一个优势是客户端可以精确控制返回的字段。","options":[{"key":"对","value":"正确"},{"key":"错","value":"错误"}],"answer":"对","analysis":"GraphQL允许客户端在请求中指定所需的字段，避免过度获取或获取不足。"},
    {"knowledge_point":"后端开发","category":"专业","career":"全栈开发工程师","difficulty":"hard","question_type":"single_choice","question":"在微服务架构中，服务间通信的常用方式不包括？","options":[{"key":"A","value":"HTTP/REST"},{"key":"B","value":"gRPC"},{"key":"C","value":"消息队列"},{"key":"D","value":"共享数据库"}],"answer":"D","analysis":"微服务间推荐通过API或消息队列通信，共享数据库会导致紧耦合。"},

    # ========== DevOps（5题，全栈开发工程师） ==========
    {"knowledge_point":"DevOps","category":"专业","career":"全栈开发工程师","difficulty":"easy","question_type":"single_choice","question":"DevOps文化强调的是什么？","options":[{"key":"A","value":"开发和运维的协作"},{"key":"B","value":"只关注开发效率"},{"key":"C","value":"只关注运维稳定性"},{"key":"D","value":"减少测试环节"}],"answer":"A","analysis":"DevOps强调开发(Dev)和运维(Ops)团队的协作与整合。"},
    {"knowledge_point":"DevOps","category":"专业","career":"全栈开发工程师","difficulty":"easy","question_type":"single_choice","question":"基础设施即代码(IaC)的工具是？","options":[{"key":"A","value":"Terraform"},{"key":"B","value":"Jenkins"},{"key":"C","value":"Git"},{"key":"D","value":"Docker"}],"answer":"A","analysis":"Terraform是基础设施即代码工具，用代码定义和管理基础设施。Jenkins是CI/CD工具。"},
    {"knowledge_point":"DevOps","category":"专业","career":"全栈开发工程师","difficulty":"medium","question_type":"single_choice","question":"Prometheus在云原生架构中的主要用途是？","options":[{"key":"A","value":"监控和告警"},{"key":"B","value":"日志收集"},{"key":"C","value":"服务发现"},{"key":"D","value":"容器编排"}],"answer":"A","analysis":"Prometheus是开源的系统监控和告警工具，是CNCF的毕业项目。"},
    {"knowledge_point":"DevOps","category":"专业","career":"全栈开发工程师","difficulty":"medium","question_type":"judge","question":"判断：GitOps是一种以Git仓库为单一信源的运维模式。","options":[{"key":"对","value":"正确"},{"key":"错","value":"错误"}],"answer":"对","analysis":"GitOps将Git仓库作为系统的单一事实来源，所有变更通过Git管理。"},
    {"knowledge_point":"DevOps","category":"专业","career":"全栈开发工程师","difficulty":"hard","question_type":"single_choice","question":"SRE(站点可靠性工程)中，SLA、SLI、SLO的关系是？","options":[{"key":"A","value":"SLO定义目标，SLI是实际指标，SLA是服务承诺"},{"key":"B","value":"SLA定义目标，SLO是实际指标，SLI是服务承诺"},{"key":"C","value":"SLI定义目标，SLO是实际指标，SLA是服务承诺"},{"key":"D","value":"三者没有关系"}],"answer":"A","analysis":"SLI(服务指标)是实际度量值，SLO(服务目标)是目标值，SLA(服务协议)是违约承诺。"},

    # ========== 前端基础（6题，UI/UX设计师） ==========
    {"knowledge_point":"前端基础","category":"专业","career":"UI/UX设计师","difficulty":"easy","question_type":"single_choice","question":"HTML中的<div>标签默认是哪种显示类型？","options":[{"key":"A","value":"块级元素(block)"},{"key":"B","value":"行内元素(inline)"},{"key":"C","value":"行内块级(inline-block)"},{"key":"D","value":"弹性布局(flex)"}],"answer":"A","analysis":"<div>是块级元素，默认占满整行宽度。"},
    {"knowledge_point":"前端基础","category":"专业","career":"UI/UX设计师","difficulty":"easy","question_type":"single_choice","question":"CSS中，哪个单位是相对于父元素字体大小的？","options":[{"key":"A","value":"em"},{"key":"B","value":"rem"},{"key":"C","value":"px"},{"key":"D","value":"vh"}],"answer":"A","analysis":"em相对于父元素的字体大小，rem相对于根(html)元素的字体大小。"},
    {"knowledge_point":"前端基础","category":"专业","career":"UI/UX设计师","difficulty":"medium","question_type":"single_choice","question":"响应式设计中，媒体查询(@media)的常用断点判断依据是？","options":[{"key":"A","value":"屏幕宽度"},{"key":"B","value":"屏幕高度"},{"key":"C","value":"浏览器版本"},{"key":"D","value":"操作系统类型"}],"answer":"A","analysis":"媒体查询常用min-width/max-width基于屏幕宽度设置不同样式。"},
    {"knowledge_point":"前端基础","category":"专业","career":"UI/UX设计师","difficulty":"medium","question_type":"judge","question":"判断：CSS Grid布局可以同时控制行和列的排列。","options":[{"key":"对","value":"正确"},{"key":"错","value":"错误"}],"answer":"对","analysis":"CSS Grid是二维布局系统，可以同时控制行和列。"},
    {"knowledge_point":"前端基础","category":"专业","career":"UI/UX设计师","difficulty":"hard","question_type":"single_choice","question":"CSS中，z-index属性只在什么情况下生效？","options":[{"key":"A","value":"元素设置了position属性（非static）"},{"key":"B","value":"元素是块级元素"},{"key":"C","value":"元素设置了float"},{"key":"D","value":"元素是行内元素"}],"answer":"A","analysis":"z-index只对设置了position（relative/absolute/fixed/sticky）的元素生效。"},
    {"knowledge_point":"前端基础","category":"专业","career":"UI/UX设计师","difficulty":"hard","question_type":"single_choice","question":"Flex布局中，align-self属性可以覆盖哪个父容器属性的设置？","options":[{"key":"A","value":"justify-content"},{"key":"B","value":"align-items"},{"key":"C","value":"flex-wrap"},{"key":"D","value":"flex-direction"}],"answer":"B","analysis":"align-self允许单个项目覆盖父容器align-items设置的对齐方式。"},

    # ========== 交互设计（5题，UI/UX设计师） ==========
    {"knowledge_point":"交互设计","category":"专业","career":"UI/UX设计师","difficulty":"easy","question_type":"single_choice","question":"用户流程图(User Flow)的主要目的是？","options":[{"key":"A","value":"展示用户完成任务的步骤"},{"key":"B","value":"展示代码逻辑"},{"key":"C","value":"展示数据库结构"},{"key":"D","value":"展示网络拓扑"}],"answer":"A","analysis":"用户流程图可视化用户完成特定任务时的操作路径和决策点。"},
    {"knowledge_point":"交互设计","category":"专业","career":"UI/UX设计师","difficulty":"easy","question_type":"single_choice","question":"低保真原型(Low-fidelity Prototype)的特点是？","options":[{"key":"A","value":"快速制作，用于测试基本概念"},{"key":"B","value":"高保真视觉效果"},{"key":"C","value":"包含真实数据"},{"key":"D","value":"已实现全部交互"}],"answer":"A","analysis":"低保真原型快速、低成本，用于早期测试设计概念和布局。"},
    {"knowledge_point":"交互设计","category":"专业","career":"UI/UX设计师","difficulty":"medium","question_type":"single_choice","question":"希克定律(Hick's Law)在交互设计中的应用是？","options":[{"key":"A","value":"减少用户的选择数量以提高决策效率"},{"key":"B","value":"增加动画效果"},{"key":"C","value":"使用更多颜色"},{"key":"D","value":"增加功能复杂度"}],"answer":"A","analysis":"希克定律指出选项越多，决策时间越长，设计中应减少不必要的选择。"},
    {"knowledge_point":"交互设计","category":"专业","career":"UI/UX设计师","difficulty":"medium","question_type":"single_choice","question":"尼尔森可用性启发式(Nielsen's Heuristics)中，'一致性'原则指的是？","options":[{"key":"A","value":"系统内的术语和操作保持一致"},{"key":"B","value":"所有页面使用相同颜色"},{"key":"C","value":"所有按钮大小相同"},{"key":"D","value":"所有文本字体相同"}],"answer":"A","analysis":"一致性原则要求同一系统中的词语、情境和操作保持一致，降低用户学习成本。"},
    {"knowledge_point":"交互设计","category":"专业","career":"UI/UX设计师","difficulty":"hard","question_type":"single_choice","question":"在进行用户可用性测试时，应该让用户？","options":[{"key":"A","value":"按照提示完成任务并观察行为"},{"key":"B","value":"自由探索系统并观察"},{"key":"C","value":"由测试人员引导完成"},{"key":"D","value":"阅读说明书后再操作"}],"answer":"A","analysis":"可用性测试通常给用户具体任务，观察其操作过程，记录问题和反馈。"},

    # ========== Linux系统（5题，运维工程师） ==========
    {"knowledge_point":"Linux系统","category":"专业","career":"运维工程师","difficulty":"easy","question_type":"single_choice","question":"Linux中，查看系统磁盘使用情况的命令是？","options":[{"key":"A","value":"df"},{"key":"B","value":"du"},{"key":"C","value":"free"},{"key":"D","value":"top"}],"answer":"A","analysis":"df显示文件系统的磁盘空间使用情况，du显示目录/文件占用空间。"},
    {"knowledge_point":"Linux系统","category":"专业","career":"运维工程师","difficulty":"easy","question_type":"single_choice","question":"Linux系统中，root用户的UID是？","options":[{"key":"A","value":"0"},{"key":"B","value":"1"},{"key":"C","value":"1000"},{"key":"D","value":"-1"}],"answer":"A","analysis":"root用户的UID为0，是系统最高权限用户。"},
    {"knowledge_point":"Linux系统","category":"专业","career":"运维工程师","difficulty":"medium","question_type":"single_choice","question":"Linux中，用于查看系统日志的命令是？","options":[{"key":"A","value":"journalctl"},{"key":"B","value":"lsblk"},{"key":"C","value":"fdisk"},{"key":"D","value":"mount"}],"answer":"A","analysis":"journalctl用于查看systemd日志，是Linux系统日志管理的主要工具。"},
    {"knowledge_point":"Linux系统","category":"专业","career":"运维工程师","difficulty":"medium","question_type":"judge","question":"判断：systemd是Linux的初始化系统和服务管理器。","options":[{"key":"对","value":"正确"},{"key":"错","value":"错误"}],"answer":"对","analysis":"systemd是大多数现代Linux发行版的初始化系统和服务管理器。"},
    {"knowledge_point":"Linux系统","category":"专业","career":"运维工程师","difficulty":"hard","question_type":"single_choice","question":"Linux中，cron表达式\"0 2 * * *\"的含义是？","options":[{"key":"A","value":"每天凌晨2点执行"},{"key":"B","value":"每小时的第2分钟执行"},{"key":"C","value":"每周2执行"},{"key":"D","value":"每月2号执行"}],"answer":"A","analysis":"cron格式：分 时 日 月 周，0 2 * * *表示每天2:00执行。"},

    # ========== 监控告警（5题，运维工程师） ==========
    {"knowledge_point":"监控告警","category":"专业","career":"运维工程师","difficulty":"easy","question_type":"single_choice","question":"以下哪个是系统监控的黄金信号(Golden Signals)之一？","options":[{"key":"A","value":"延迟(Latency)"},{"key":"B","value":"代码行数"},{"key":"C","value":"开发效率"},{"key":"D","value":"用户满意度"}],"answer":"A","analysis":"Google SRE提出的四大黄金信号：延迟、流量、错误数、饱和度。"},
    {"knowledge_point":"监控告警","category":"专业","career":"运维工程师","difficulty":"easy","question_type":"single_choice","question":"Grafana的主要用途是？","options":[{"key":"A","value":"数据可视化和监控仪表盘"},{"key":"B","value":"日志收集"},{"key":"C","value":"包管理"},{"key":"D","value":"代码编译"}],"answer":"A","analysis":"Grafana是开源的数据可视化和监控分析平台，常用于创建监控仪表盘。"},
    {"knowledge_point":"监控告警","category":"专业","career":"运维工程师","difficulty":"medium","question_type":"single_choice","question":"告警的'抑制(Inhibition)'机制是指？","options":[{"key":"A","value":"当某告警触发时阻止其他关联告警"},{"key":"B","value":"忽略所有告警"},{"key":"C","value":"增加告警频率"},{"key":"D","value":"删除历史告警"}],"answer":"A","analysis":"告警抑制是指当某告警触发时，阻止某些其他告警的通知，减少告警风暴。"},
    {"knowledge_point":"监控告警","category":"专业","career":"运维工程师","difficulty":"medium","question_type":"single_choice","question":"以下哪个是日志管理的常用工具？","options":[{"key":"A","value":"ELK Stack"},{"key":"B","value":"Docker"},{"key":"C","value":"Kubernetes"},{"key":"D","value":"Ansible"}],"answer":"A","analysis":"ELK Stack（Elasticsearch、Logstash、Kibana）是常用的日志管理方案。"},
    {"knowledge_point":"监控告警","category":"专业","career":"运维工程师","difficulty":"hard","question_type":"single_choice","question":"Prometheus的告警规则中，'for'字段的作用是？","options":[{"key":"A","value":"指定告警持续多长时间后才触发"},{"key":"B","value":"指定告警的频率"},{"key":"C","value":"指定告警接收人"},{"key":"D","value":"指定告警级别"}],"answer":"A","analysis":"'for'字段定义告警条件满足后持续多长时间才真正触发告警，用于避免抖动。"},

    # ========== 数据结构（共享，算法工程师额外） ==========
    {"knowledge_point":"数据结构","category":"专业","career":"算法工程师","difficulty":"hard","question_type":"single_choice","question":"红黑树的主要特性不包括？","options":[{"key":"A","value":"根节点是黑色"},{"key":"B","value":"红色节点的子节点都是黑色"},{"key":"C","value":"叶子节点都是红色"},{"key":"D","value":"从任一节点到叶子节点的黑色节点数相同"}],"answer":"C","analysis":"红黑树的叶子节点（NIL）是黑色的，不是红色的。"},
    {"knowledge_point":"数据结构","category":"专业","career":"算法工程师","difficulty":"hard","question_type":"single_choice","question":"B+树在数据库中常用于？","options":[{"key":"A","value":"索引结构"},{"key":"B","value":"数据缓存"},{"key":"C","value":"连接池"},{"key":"D","value":"事务管理"}],"answer":"A","analysis":"B+树是关系型数据库中广泛使用的索引数据结构，支持高效的范围查询。"},

    # ========== 编程能力（5题，算法工程师） ==========
    {"knowledge_point":"编程能力","category":"专业","career":"算法工程师","difficulty":"easy","question_type":"single_choice","question":"以下哪个排序算法的时间复杂度最优？","options":[{"key":"A","value":"冒泡排序"},{"key":"B","value":"插入排序"},{"key":"C","value":"归并排序"},{"key":"D","value":"选择排序"}],"answer":"C","analysis":"归并排序平均和最坏情况都是O(n log n)，冒泡、插入、选择排序最坏O(n²)。"},
    {"knowledge_point":"编程能力","category":"专业","career":"算法工程师","difficulty":"easy","question_type":"single_choice","question":"递归算法的核心要素是？","options":[{"key":"A","value":"终止条件和递归调用"},{"key":"B","value":"循环和条件判断"},{"key":"C","value":"变量和数组"},{"key":"D","value":"类和对象"}],"answer":"A","analysis":"递归必须包含终止条件（基本情况）和递归调用（向终止条件推进）。"},
    {"knowledge_point":"编程能力","category":"专业","career":"算法工程师","difficulty":"medium","question_type":"single_choice","question":"动态规划(Dynamic Programming)的适用条件是？","options":[{"key":"A","value":"最优子结构和重叠子问题"},{"key":"B","value":"随机输入"},{"key":"C","value":"只有小规模数据"},{"key":"D","value":"递归实现"}],"answer":"A","analysis":"动态规划适用于具有最优子结构和重叠子问题性质的问题。"},
    {"knowledge_point":"编程能力","category":"专业","career":"算法工程师","difficulty":"medium","question_type":"single_choice","question":"斐波那契数列的时间复杂度优化从O(2^n)到O(n)通常使用？","options":[{"key":"A","value":"记忆化搜索/动态规划"},{"key":"B","value":"递归"},{"key":"C","value":"分治"},{"key":"D","value":"贪心"}],"answer":"A","analysis":"使用记忆化搜索或动态规划避免重复计算，将指数级复杂度降为线性。"},
    {"knowledge_point":"编程能力","category":"专业","career":"算法工程师","difficulty":"hard","question_type":"single_choice","question":"以下哪个问题适合用贪心算法求解？","options":[{"key":"A","value":"0-1背包问题"},{"key":"B","value":"最短路径(Dijkstra)"},{"key":"C","value":"旅行商问题"},{"key":"D","value":"八皇后问题"}],"answer":"B","analysis":"Dijkstra最短路径算法是贪心算法的典型应用。0-1背包和TSP需要DP或回溯。"},

    # ========== 用户运营（5题，运营专员） ==========
    {"knowledge_point":"用户运营","category":"专业","career":"运营专员","difficulty":"easy","question_type":"single_choice","question":"用户运营中，新用户引导(Onboarding)的目的是？","options":[{"key":"A","value":"帮助用户快速了解产品核心价值"},{"key":"B","value":"增加服务器负载"},{"key":"C","value":"收集用户密码"},{"key":"D","value":"发送广告"}],"answer":"A","analysis":"新用户引导帮助用户在最短时间内体验到产品的核心价值(Aha Moment)。"},
    {"knowledge_point":"用户运营","category":"专业","career":"运营专员","difficulty":"easy","question_type":"single_choice","question":"用户分层中，RFM模型常用于？","options":[{"key":"A","value":"衡量用户价值"},{"key":"B","value":"计算服务器成本"},{"key":"C","value":"评估代码质量"},{"key":"D","value":"测试软件性能"}],"answer":"A","analysis":"RFM模型根据用户最近消费、频率和金额进行分层，评估用户价值。"},
    {"knowledge_point":"用户运营","category":"专业","career":"运营专员","difficulty":"medium","question_type":"single_choice","question":"用户留存率的计算公式通常为？","options":[{"key":"A","value":"第N天回访用户/首日新增用户"},{"key":"B","value":"总用户数/1"},{"key":"C","value":"付费用户/总用户"},{"key":"D","value":"活跃用户/注册用户"}],"answer":"A","analysis":"留存率=第N天仍活跃的用户数/该批新增用户总数。"},
    {"knowledge_point":"用户运营","category":"专业","career":"运营专员","difficulty":"medium","question_type":"single_choice","question":"在社群运营中，'KOL'是指？","options":[{"key":"A","value":"关键意见领袖"},{"key":"B","value":"关键绩效指标"},{"key":"C","value":"知识图谱"},{"key":"D","value":"关键操作日志"}],"answer":"A","analysis":"KOL（Key Opinion Leader）指在特定领域有影响力和话语权的人。"},
    {"knowledge_point":"用户运营","category":"专业","career":"运营专员","difficulty":"hard","question_type":"single_choice","question":"AARRR模型中，'Referral'阶段的核心目标是？","options":[{"key":"A","value":"激励用户邀请新用户"},{"key":"B","value":"提高客单价"},{"key":"C","value":"降低获客成本"},{"key":"D","value":"提升用户活跃度"}],"answer":"A","analysis":"Referral（推荐/自传播）阶段通过激励机制促使用户主动邀请其他人使用产品。"},

    # ========== 数据分析（通用专业，补充） ==========
    {"knowledge_point":"数据分析","category":"专业","career":"产品经理","difficulty":"easy","question_type":"single_choice","question":"产品数据分析中，DAU是指？","options":[{"key":"A","value":"日活跃用户数"},{"key":"B","value":"月活跃用户数"},{"key":"C","value":"用户平均收入"},{"key":"D","value":"客户获取成本"}],"answer":"A","analysis":"DAU（Daily Active Users）日活跃用户数，衡量产品每日使用人数。"},
    {"knowledge_point":"数据分析","category":"专业","career":"产品经理","difficulty":"easy","question_type":"single_choice","question":"漏斗分析中，相邻两个环节之间的转化率下降过多通常表明？","options":[{"key":"A","value":"该环节存在问题需要优化"},{"key":"B","value":"用户数量太少"},{"key":"C","value":"数据统计错误"},{"key":"D","value":"产品太受欢迎"}],"answer":"A","analysis":"转化率骤降说明该环节可能存在用户体验问题或障碍。"},
    {"knowledge_point":"数据分析","category":"专业","career":"产品经理","difficulty":"medium","question_type":"single_choice","question":"产品数据分析中，`留存率`和`流失率`的关系是？","options":[{"key":"A","value":"流失率=1-留存率"},{"key":"B","value":"留存率=1-流失率"},{"key":"C","value":"二者无关系"},{"key":"D","value":"二者相等"}],"answer":"A","analysis":"流失率=1-留存率，二者此消彼长。"},
    {"knowledge_point":"数据分析","category":"专业","career":"产品经理","difficulty":"medium","question_type":"single_choice","question":"同比和环比的区别是？","options":[{"key":"A","value":"同比与去年同期比较，环比与上个月比较"},{"key":"B","value":"同比与上个月比较，环比与去年比较"},{"key":"C","value":"同比与竞争对手比较"},{"key":"D","value":"环比与行业平均值比较"}],"answer":"A","analysis":"同比是年度同期比较，消除季节性因素；环比是相邻周期比较，反映短期趋势。"},
    {"knowledge_point":"数据分析","category":"专业","career":"运营专员","difficulty":"hard","question_type":"single_choice","question":"某电商平台通过数据分析发现用户下单转化率持续下降，以下分析思路最合理的是？","options":[{"key":"A","value":"拆解各流量渠道的转化率，定位问题渠道"},{"key":"B","value":"直接增加广告投放"},{"key":"C","value":"降低商品价格"},{"key":"D","value":"关闭数据分析功能"}],"answer":"A","analysis":"通过拆解各渠道转化率可以定位问题所在，针对性优化，这是数据驱动决策的正确思路。"},

    # ========== 全栈架构（5题，全栈开发工程师） ==========
    {"knowledge_point":"全栈架构","category":"专业","career":"全栈开发工程师","difficulty":"easy","question_type":"single_choice","question":"MVC架构中，'M'代表什么？","options":[{"key":"A","value":"Model（模型）"},{"key":"B","value":"Module（模块）"},{"key":"C","value":"Memory（内存）"},{"key":"D","value":"Monitor（监控）"}],"answer":"A","analysis":"MVC：Model（数据模型）、View（视图）、Controller（控制器）。"},
    {"knowledge_point":"全栈架构","category":"专业","career":"全栈开发工程师","difficulty":"easy","question_type":"single_choice","question":"前端与后端分离架构的主要优势是？","options":[{"key":"A","value":"前后端可独立开发和部署"},{"key":"B","value":"减少代码量"},{"key":"C","value":"不需要数据库"},{"key":"D","value":"不需要网络"}],"answer":"A","analysis":"前后端分离通过API通信，使前后端可以独立开发、测试和部署。"},
    {"knowledge_point":"全栈架构","category":"专业","career":"全栈开发工程师","difficulty":"medium","question_type":"single_choice","question":"单页应用(SPA)的缺点是？","options":[{"key":"A","value":"首屏加载速度较慢"},{"key":"B","value":"无法使用JavaScript"},{"key":"C","value":"不支持移动端"},{"key":"D","value":"代码难以维护"}],"answer":"A","analysis":"SPA需要在首屏加载大量JS，可能导致首屏加载时间较长。"},
    {"knowledge_point":"全栈架构","category":"专业","career":"全栈开发工程师","difficulty":"medium","question_type":"judge","question":"判断：SSR(服务端渲染)可以改善SPA的SEO问题。","options":[{"key":"对","value":"正确"},{"key":"错","value":"错误"}],"answer":"对","analysis":"SSR在服务端生成完整HTML，搜索引擎爬虫可以直接获取内容，改善SEO。"},
    {"knowledge_point":"全栈架构","category":"专业","career":"全栈开发工程师","difficulty":"hard","question_type":"single_choice","question":"在微前端架构中，以下哪个不是常见的实现方式？","options":[{"key":"A","value":"iframe嵌套"},{"key":"B","value":"Web Components"},{"key":"C","value":"模块联邦(Module Federation)"},{"key":"D","value":"单体应用"}],"answer":"D","analysis":"微前端通过iframe、Web Components、Module Federation等方式集成，单体应用是反例。"},
]


# ═══════════════════════════════════════════════════════════════
# 辅助函数
# ═══════════════════════════════════════════════════════════════

def safe_json_loads(text, default=None):
    """安全解析JSON字符串"""
    if default is None:
        default = []
    try:
        return json.loads(text) if text else default
    except (json.JSONDecodeError, TypeError):
        return default


def get_mimo_api_key():
    """获取MiMo API密钥，自高优先级向低优先级：MIMO_API_KEY → LLM_API_KEY → API_KEY"""
    for k in ("MIMO_API_KEY", "LLM_API_KEY", "API_KEY"):
        v = os.getenv(k)
        if v:
            return v
    return ""


# ═══════════════════════════════════════════════════════════════
# AI出题函数
# ═══════════════════════════════════════════════════════════════

async def generate_ai_questions(career: str, knowledge_point: str, difficulty: str,
                                 question_type: str, count: int):
    """调用AI API生成笔试题目，写入数据库并返回"""
    prompt = f"""你是一个专业笔试题出题专家，请为"{career}"岗位生成{count}道关于"{knowledge_point}"的笔试题。

要求：
- 难度：{difficulty}
- 题型：{question_type}
- 如果是single_choice，提供4个选项(A/B/C/D)
- 如果是judge，选项为[对, 错]
- 如果是multi_choice，提供4-6个选项
- 所有题目必须有唯一正确答案，不模棱两可
- 答案解析必须写清楚"为什么正确选项是对的"以及"为什么错误选项是错的"
- 考察的知识点要是真实企业中该岗位会问到的内容
- 题目要有实际应用场景，而不是纯理论背诵

请严格按照以下JSON数组格式返回，不要包含任何其他内容（不要Markdown代码块，纯JSON）：
[
  {{
    "question": "题目内容（2-3行以内，清晰直白）",
    "options": [{{"key": "A", "value": "选项内容"}}, {{"key": "B", "value": "选项内容"}}, {{"key": "C", "value": "选项内容"}}, {{"key": "D", "value": "选项内容"}}],
    "answer": "正确答案（单个字母如A，或逗号分隔如A,B）",
    "analysis": "详细解析：先指出正确选项为什么对，再逐个说明错误选项为什么错，最后总结该知识点在实际开发中的应用",
    "knowledge_point": "{knowledge_point}",
    "difficulty": "{difficulty}",
    "question_type": "{question_type}"
  }}
]

注意：analysis必须足够详细，让考生看完后能完全理解该知识点，不要只写一句话。
"""

    from routers.llm import async_chat
    content = await async_chat(
        prompt,
        system="你是专业笔试题出题专家。输出必须是纯JSON数组，不要添加任何Markdown格式或额外文字。",
        temperature=0.7, max_tokens=4096,
    )

    if not content:
        return {"error": "AI API调用失败"}

    # 清理可能的 Markdown 代码块标记
    content = content.strip()
    if content.startswith("```json"):
        content = content[7:]
    if content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()

    try:
        questions_data = json.loads(content)
    except:
        return {"error": "AI返回格式解析失败"}

    if not isinstance(questions_data, list):
        questions_data = [questions_data]

    # 获取当前最大ID
    db = SessionLocal()
    try:
        max_id = db.query(func.max(ExamQuestion.id)).scalar() or 0
        next_id = max_id + 1

        saved_questions = []
        for i, q_data in enumerate(questions_data[:count]):
            q_career = career
            q_category = "专业" if career != "通用" else "通用"
            q_knowledge = q_data.get("knowledge_point", knowledge_point)

            eq = ExamQuestion(
                category=q_knowledge,
                difficulty=q_data.get("difficulty", difficulty),
                question_type=q_data.get("question_type", question_type),
                question=q_data.get("question", ""),
                options_json=json.dumps(q_data.get("options", []), ensure_ascii=False),
                answer=q_data.get("answer", ""),
                analysis=q_data.get("analysis", ""),
                source=q_career,
            )
            db.add(eq)
            db.flush()

            saved_questions.append({
                "id": eq.id,
                "knowledge_point": q_knowledge,
                "category": q_category,
                "career": q_career,
                "difficulty": eq.difficulty,
                "question_type": eq.question_type,
                "question": eq.question,
                "options": q_data.get("options", []),
                "answer": eq.answer,
                "analysis": eq.analysis,
            })

        db.commit()
        return {"questions": saved_questions, "source": "ai_generated"}

    except Exception as e:
        db.rollback()
        return {"error": f"保存AI生成题目失败: {str(e)}"}
    finally:
        db.close()


# ═══════════════════════════════════════════════════════════════
# 题库初始化
# ═══════════════════════════════════════════════════════════════

def init_database():
    """初始化题库（在路由器创建时自动调用）"""
    db = SessionLocal()
    try:
        count = db.query(func.count(ExamQuestion.id)).scalar()
        if count > 0:
            return

        # Try to load from seed_questions.json first (real interview questions)
        import os
        json_path = os.path.join(os.path.dirname(__file__), "../seed_questions.json")
        if os.path.exists(json_path):
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    questions = json.load(f)
                for q in questions:
                    eq = ExamQuestion(
                        category=q.get("knowledge_point", ""),
                        knowledge_point=q.get("knowledge_point", ""),
                        career=q.get("career", ""),
                        difficulty=q.get("difficulty", "medium"),
                        question_type=q.get("question_type", "single"),
                        question=q["question"],
                        options_json=json.dumps(q.get("options", []), ensure_ascii=False),
                        answer=q.get("answer", ""),
                        analysis=q.get("analysis", ""),
                        source=q.get("career", ""),
                    )
                    db.add(eq)
                db.commit()
                return
            except Exception:
                db.rollback()

        # Fallback to hardcoded questions (legacy)
        for q in EXPANDED_MOCK_QUESTIONS:
            eq = ExamQuestion(
                category=q["knowledge_point"],
                difficulty=q["difficulty"],
                question_type=q["question_type"],
                question=q["question"],
                options_json=json.dumps(q["options"], ensure_ascii=False),
                answer=q["answer"],
                analysis=q["analysis"],
                source=q["career"],
            )
            db.add(eq)
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()


# 自动初始化
init_database()


# ═══════════════════════════════════════════════════════════════
# 岗位-考点接口
# ═══════════════════════════════════════════════════════════════

@router.get("/career-knowledge")
def get_career_knowledge_endpoint(
    career: str = Query("", description="目标岗位"),
):
    """获取岗位的可用考点（通用+专业）"""
    if not career:
        return {"error": "请提供career参数"}
    return get_career_knowledge(career)


# ═══════════════════════════════════════════════════════════════
# 题目管理接口
# ═══════════════════════════════════════════════════════════════

@router.post("/seed")
def seed_exam_questions():
    """将扩充题库写入数据库（如已写入则跳过）"""
    db = SessionLocal()
    try:
        count = db.query(func.count(ExamQuestion.id)).scalar()
        if count >= len(EXPANDED_MOCK_QUESTIONS):
            return {"message": "题库已经初始化，无需重复导入", "total": count}

        for q in EXPANDED_MOCK_QUESTIONS:
            eq = ExamQuestion(
                category=q["knowledge_point"],
                difficulty=q["difficulty"],
                question_type=q["question_type"],
                question=q["question"],
                options_json=json.dumps(q["options"], ensure_ascii=False),
                answer=q["answer"],
                analysis=q["analysis"],
                source=q["career"],
            )
            db.add(eq)
        db.commit()
        total = len(EXPANDED_MOCK_QUESTIONS)
        return {"message": f"题库初始化成功，共导入{total}道题目", "total": total}
    except Exception as e:
        db.rollback()
        return {"error": f"题库初始化失败: {str(e)}"}
    finally:
        db.close()


@router.get("/questions")
def get_exam_questions(
    category: str = Query("", description="考点分类"),
    difficulty: str = Query("", description="难度: easy/medium/hard"),
    question_type: str = Query("", description="题型: single_choice/multi_choice/judge"),
    source: str = Query("", description="来源/岗位分类"),
    career: str = Query("", description="岗位名称筛选"),
    knowledge_point: str = Query("", description="具体考点筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
):
    """获取笔试题目（支持分页和筛选）"""
    db = SessionLocal()
    try:
        query = db.query(ExamQuestion)

        # 处理career筛选：如果传了career，匹配该岗位的考点范围
        if career:
            knowledge_map = get_career_knowledge(career)
            all_points = [kp["name"] for kp in knowledge_map["general"]]
            all_points += [kp["name"] for kp in knowledge_map["professional"]]
            query = query.filter(
                ExamQuestion.category.in_(all_points)
            ).filter(
                # career="通用" 或 匹配该岗位的题目
                ExamQuestion.source.in_([career, "通用"])
            )

        # 处理knowledge_point筛选
        if knowledge_point:
            query = query.filter(ExamQuestion.category == knowledge_point)

        # 兼容旧的category参数（当作knowledge_point使用）
        if category and not knowledge_point:
            query = query.filter(ExamQuestion.category == category)

        if difficulty:
            query = query.filter(ExamQuestion.difficulty == difficulty)
        if question_type:
            query = query.filter(ExamQuestion.question_type == question_type)
        if source:
            query = query.filter(ExamQuestion.source == source)

        total = query.count()
        items = query.order_by(ExamQuestion.id).offset((page - 1) * page_size).limit(page_size).all()

        result = []
        for q in items:
            result.append({
                "id": q.id,
                "knowledge_point": q.category,
                "category": "专业" if q.source and q.source != "通用" else "通用",
                "career": q.source or "通用",
                "difficulty": q.difficulty,
                "question_type": q.question_type,
                "question": q.question,
                "options": safe_json_loads(q.options_json),
                "answer": q.answer,
                "analysis": q.analysis,
                "created_at": q.created_at.strftime("%Y-%m-%d %H:%M") if q.created_at else "",
            })

        return {
            "questions": result,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
        }
    except Exception as e:
        return {"error": f"获取题目失败: {str(e)}"}
    finally:
        db.close()


@router.get("/generate")
def generate_exam_questions(
    career: str = Query("", description="目标岗位"),
    knowledge_point: str = Query("", description="具体考点"),
    difficulty: str = Query("", description="难度: easy/medium/hard"),
    question_type: str = Query("", description="题型: single_choice/judge/multi_choice"),
    count: int = Query(10, ge=1, le=50, description="题目数量"),
    mode: str = Query("专项练习", description="练习模式"),
    use_ai: bool = Query(False, description="强制仅使用AI出题"),
):
    """核心出题接口：先查题库，不足时AI补充。use_ai=true 直接AI出题"""
    db = SessionLocal()
    try:
        results = []

        # ── use_ai=true：直接AI出题，跳过本地题库 ──
        ai_mode = use_ai and bool(career)
        if ai_mode:
            import asyncio
            loop = asyncio.new_event_loop()
            try:
                ai_result = loop.run_until_complete(
                    generate_ai_questions(
                        career=career,
                        knowledge_point=knowledge_point or "综合知识",
                        difficulty=difficulty or "medium",
                        question_type=question_type or "single_choice",
                        count=count,
                    )
                )
                loop.close()
                if "questions" in ai_result:
                    results.extend([ExamQuestion(
                        id=q["id"],
                        category=q["knowledge_point"],
                        difficulty=q["difficulty"],
                        question_type=q["question_type"],
                        question=q["question"],
                        options_json=json.dumps(q["options"], ensure_ascii=False),
                        answer=q["answer"],
                        analysis=q["analysis"],
                        source=career,
                    ) for q in ai_result["questions"]])
                elif "error" in ai_result:
                    db.close()
                    return {"error": ai_result["error"]}
            except Exception as e:
                loop.close()
                db.close()
                return {"error": f"AI出题失败: {str(e)}"}

        # 1. 查本地题库匹配（非AI模式才执行）
        if not ai_mode and career and knowledge_point:
            query = db.query(ExamQuestion).filter(
                ExamQuestion.category == knowledge_point,
                ExamQuestion.difficulty == difficulty if difficulty else True,
                ExamQuestion.question_type == question_type if question_type else True,
            )
            # 匹配该岗位专属 或 通用题目
            query = query.filter(
                ExamQuestion.source.in_([career, "通用"])
            )
            local_questions = query.order_by(func.random()).limit(count).all()
            results.extend(local_questions)

        # 如果只传了career没有knowledge_point，从该岗位的考点中随机选
        elif not ai_mode and career and not knowledge_point:
            knowledge_map = get_career_knowledge(career)
            all_points = [kp["name"] for kp in knowledge_map["general"]]
            all_points += [kp["name"] for kp in knowledge_map["professional"]]
            query = db.query(ExamQuestion).filter(
                ExamQuestion.category.in_(all_points),
                ExamQuestion.source.in_([career, "通用"]),
            )
            if difficulty:
                query = query.filter(ExamQuestion.difficulty == difficulty)
            if question_type:
                query = query.filter(ExamQuestion.question_type == question_type)
            local_questions = query.order_by(func.random()).limit(count).all()
            results.extend(local_questions)

        # 如果没传career，按原有方式随机出题
        elif not ai_mode and not career:
            query = db.query(ExamQuestion)
            if knowledge_point:
                query = query.filter(ExamQuestion.category == knowledge_point)
            if difficulty:
                query = query.filter(ExamQuestion.difficulty == difficulty)
            if question_type:
                query = query.filter(ExamQuestion.question_type == question_type)
            local_questions = query.order_by(func.random()).limit(count).all()
            results.extend(local_questions)

        # 2. 如果本地题目不够，调用AI补充
        need_count = count - len(results)
        if need_count > 0 and career:
            # 如果没有传knowledge_point，取该岗位第一个考点或"综合知识"
            fallback_kp = knowledge_point or "综合知识"
            import asyncio
            loop = asyncio.new_event_loop()
            try:
                ai_result = loop.run_until_complete(
                    generate_ai_questions(
                        career=career,
                        knowledge_point=fallback_kp,
                        difficulty=difficulty or "medium",
                        question_type=question_type or "single_choice",
                        count=need_count,
                    )
                )
                loop.close()
                if "questions" in ai_result:
                    results.extend([ExamQuestion(
                        id=q["id"],
                        category=q["knowledge_point"],
                        difficulty=q["difficulty"],
                        question_type=q["question_type"],
                        question=q["question"],
                        options_json=json.dumps(q["options"], ensure_ascii=False),
                        answer=q["answer"],
                        analysis=q["analysis"],
                        source=career,
                    ) for q in ai_result["questions"]])
            except Exception:
                pass

        # 格式化输出
        formatted = []
        for q in results:
            formatted.append({
                "id": q.id,
                "knowledge_point": q.category,
                "category": "专业" if q.source and q.source != "通用" else "通用",
                "career": q.source or "通用",
                "difficulty": q.difficulty,
                "question_type": q.question_type,
                "question": q.question,
                "options": safe_json_loads(q.options_json),
                "answer": q.answer,
                "analysis": q.analysis,
            })

        # 随机打乱
        random.shuffle(formatted)

        return {
            "questions": formatted[:count],
            "total": len(formatted),
            "mode": mode,
            "career": career,
            "knowledge_point": knowledge_point,
        }
    except Exception as e:
        return {"error": f"出题失败: {str(e)}"}
    finally:
        db.close()


# ═══════════════════════════════════════════════════════════════
# AI出题补充接口
# ═══════════════════════════════════════════════════════════════

@router.post("/generate-ai")
async def generate_ai_endpoint(
    career: str = Body("", description="目标岗位"),
    knowledge_point: str = Body("", description="考点"),
    difficulty: str = Body("medium", description="难度"),
    question_type: str = Body("single_choice", description="题型"),
    count: int = Body(5, ge=1, le=20, description="题目数量"),
):
    """AI出题补充接口"""
    if not career or not knowledge_point:
        return {"error": "请提供career和knowledge_point参数"}
    return await generate_ai_questions(career, knowledge_point, difficulty, question_type, count)


# ═══════════════════════════════════════════════════════════════
# 提交答案接口
# ═══════════════════════════════════════════════════════════════

@router.post("/submit")
def submit_exam_answer(
    question_id: int = Body(..., description="题目ID"),
    user_answer: str = Body("", description="用户答案"),
    career: str = Body("", description="岗位名称"),
    category: str = Body("", description="分类（自动填充）"),
    difficulty: str = Body("medium", description="难度"),
    question_type: str = Body("single_choice", description="题型"),
    question: str = Body("", description="题目内容"),
    options_json: str = Body("[]", description="选项JSON"),
    analysis: str = Body("", description="答案解析"),
):
    """提交笔试答案，自动判断对错并记录错题（新增career字段）"""
    db = SessionLocal()
    try:
        # 先从数据库查找题目
        q = db.query(ExamQuestion).filter(ExamQuestion.id == question_id).first()
        if q:
            correct_answer = q.answer
            full_analysis = q.analysis
            cat = q.category
            diff = q.difficulty
            q_type = q.question_type
            q_text = q.question
            opts_json = q.options_json
            src = q.source or career
        else:
            correct_answer = ""
            full_analysis = analysis
            cat = category
            diff = difficulty
            q_type = question_type
            q_text = question
            opts_json = options_json
            src = career

        is_correct = (user_answer.strip() == correct_answer.strip())

        if not is_correct:
            existing = db.query(WrongQuestion).filter(
                WrongQuestion.question_id == question_id,
                WrongQuestion.question_type == "exam",
            ).first()

            if existing:
                existing.wrong_count += 1
                existing.user_answer = user_answer
                existing.last_wrong_at = datetime.utcnow()
                existing.mastered = 0
                if career:
                    existing.career = career
            else:
                wq = WrongQuestion(
                    question_id=question_id,
                    question_type="exam",
                    career=src,
                    category=cat,
                    difficulty=diff,
                    question=q_text,
                    user_answer=user_answer,
                    correct_answer=correct_answer,
                    options_json=opts_json,
                    analysis=full_analysis,
                    source=src,
                    wrong_count=1,
                    last_wrong_at=datetime.utcnow(),
                    mastered=0,
                )
                db.add(wq)
            db.commit()

        return {
            "is_correct": is_correct,
            "correct_answer": correct_answer,
            "analysis": full_analysis,
            "message": "回答正确" if is_correct else "回答错误，已记录到错题本",
        }
    except Exception as e:
        db.rollback()
        return {"error": f"提交答案失败: {str(e)}"}
    finally:
        db.close()


# ═══════════════════════════════════════════════════════════════
# 练习记录接口
# ═══════════════════════════════════════════════════════════════

@router.post("/record")
def save_exam_record(
    career: str = Body("", description="目标岗位"),
    mode: str = Body("专项练习", description="练习模式: 专项练习/模拟卷/错题重练"),
    answers: list = Body([], description="答题记录列表"),
    duration_seconds: int = Body(0, description="总用时(秒)"),
):
    """保存一次练习记录到ExamRecord表"""
    db = SessionLocal()
    try:
        total = len(answers)
        correct = sum(1 for a in answers if a.get("correct", False))
        wrong = total - correct
        accuracy = round(correct / total * 100, 1) if total > 0 else 0

        # 统计考点分布
        knowledge_stats = {}
        for a in answers:
            kp = a.get("knowledge_point", "未知")
            if kp not in knowledge_stats:
                knowledge_stats[kp] = {"total": 0, "correct": 0}
            knowledge_stats[kp]["total"] += 1
            if a.get("correct", False):
                knowledge_stats[kp]["correct"] += 1

        record = ExamRecord(
            career=career,
            mode=mode,
            total_questions=total,
            correct_count=correct,
            wrong_count=wrong,
            accuracy=accuracy,
            duration_seconds=duration_seconds,
            answers_json=json.dumps(answers, ensure_ascii=False),
            knowledge_json=json.dumps(knowledge_stats, ensure_ascii=False),
        )
        db.add(record)
        db.commit()
        db.refresh(record)

        # 根据薄弱知识点生成学习推荐
        weak_kps = []
        for kp, stats in knowledge_stats.items():
            if stats["correct"] / stats["total"] < 0.6:
                weak_kps.append(kp)

        learning_tags = set()
        for kp in weak_kps:
            if "算法" in kp or "数据结构" in kp:
                learning_tags.add("算法 刷题 LeetCode")
            if "数据库" in kp or "SQL" in kp:
                learning_tags.add("SQL 数据库 面试")
            if "前端" in kp or "HTML" in kp or "CSS" in kp or "JavaScript" in kp or "JS" in kp or "Vue" in kp or "React" in kp:
                learning_tags.add(f"前端开发 {career} 面试")
            if "Java" in kp or "Python" in kp or "编程" in kp:
                learning_tags.add(f"{kp} 编程题 刷题")
            if "网络" in kp or "HTTP" in kp:
                learning_tags.add("计算机网络 面试")
            if "系统" in kp or "设计" in kp:
                learning_tags.add("系统设计 面试")
            if "框架" in kp or "Spring" in kp or "MyBatis" in kp:
                learning_tags.add(f"{kp} 面试 高频题")
        if not learning_tags and career:
            learning_tags.add(f"{career} 笔试 面试")

        return {
            "id": record.id,
            "career": career,
            "mode": mode,
            "total_questions": total,
            "correct_count": correct,
            "wrong_count": wrong,
            "accuracy": accuracy,
            "duration_seconds": duration_seconds,
            "knowledge_stats": knowledge_stats,
            "learning_tags": list(learning_tags),
            "message": "练习记录已保存",
        }
    except Exception as e:
        db.rollback()
        return {"error": f"保存记录失败: {str(e)}"}
    finally:
        db.close()


@router.get("/records")
def get_exam_records(
    career: str = Query("", description="岗位筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
):
    """获取练习记录列表，支持按岗位筛选"""
    db = SessionLocal()
    try:
        query = db.query(ExamRecord)
        if career:
            query = query.filter(ExamRecord.career == career)

        total = query.count()
        items = query.order_by(desc(ExamRecord.created_at)).offset(
            (page - 1) * page_size
        ).limit(page_size).all()

        result = []
        for r in items:
            result.append({
                "id": r.id,
                "career": r.career,
                "mode": r.mode,
                "total_questions": r.total_questions,
                "correct_count": r.correct_count,
                "wrong_count": r.wrong_count,
                "accuracy": r.accuracy,
                "duration_seconds": r.duration_seconds,
                "created_at": r.created_at.strftime("%Y-%m-%d %H:%M") if r.created_at else "",
            })

        return {
            "records": result,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
        }
    except Exception as e:
        return {"error": f"获取记录列表失败: {str(e)}"}
    finally:
        db.close()


@router.get("/records/{record_id}")
def get_exam_record_detail(record_id: int):
    """获取单次练习报告详情"""
    db = SessionLocal()
    try:
        record = db.query(ExamRecord).filter(ExamRecord.id == record_id).first()
        if not record:
            return {"error": "记录不存在"}

        return {
            "id": record.id,
            "career": record.career,
            "mode": record.mode,
            "total_questions": record.total_questions,
            "correct_count": record.correct_count,
            "wrong_count": record.wrong_count,
            "accuracy": record.accuracy,
            "duration_seconds": record.duration_seconds,
            "answers": safe_json_loads(record.answers_json),
            "knowledge_stats": safe_json_loads(record.knowledge_json, default={}),
            "created_at": record.created_at.strftime("%Y-%m-%d %H:%M") if record.created_at else "",
        }
    except Exception as e:
        return {"error": f"获取记录详情失败: {str(e)}"}
    finally:
        db.close()


# ═══════════════════════════════════════════════════════════════
# 错题管理接口
# ═══════════════════════════════════════════════════════════════

@router.get("/wrong-questions")
def get_wrong_questions(
    category: str = Query("", description="分类筛选"),
    difficulty: str = Query("", description="难度筛选"),
    career: str = Query("", description="岗位筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
):
    """获取笔试题错题列表（新增career筛选）"""
    db = SessionLocal()
    try:
        query = db.query(WrongQuestion).filter(
            WrongQuestion.question_type == "exam"
        )
        if category:
            query = query.filter(WrongQuestion.category == category)
        if difficulty:
            query = query.filter(WrongQuestion.difficulty == difficulty)
        if career:
            query = query.filter(WrongQuestion.career == career)

        total = query.count()
        items = query.order_by(desc(WrongQuestion.last_wrong_at)).offset(
            (page - 1) * page_size
        ).limit(page_size).all()

        result = []
        for w in items:
            result.append({
                "id": w.id,
                "question_id": w.question_id,
                "career": w.career,
                "category": w.category,
                "difficulty": w.difficulty,
                "question": w.question,
                "user_answer": w.user_answer,
                "correct_answer": w.correct_answer,
                "options": safe_json_loads(w.options_json),
                "analysis": w.analysis,
                "source": w.source,
                "wrong_count": w.wrong_count,
                "last_wrong_at": w.last_wrong_at.strftime("%Y-%m-%d %H:%M") if w.last_wrong_at else "",
                "mastered": bool(w.mastered),
                "created_at": w.created_at.strftime("%Y-%m-%d %H:%M") if w.created_at else "",
            })

        return {
            "wrong_questions": result,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
        }
    except Exception as e:
        return {"error": f"获取错题列表失败: {str(e)}"}
    finally:
        db.close()


@router.delete("/wrong-questions/{wrong_id}")
def delete_wrong_question(wrong_id: int):
    """移除错题记录"""
    db = SessionLocal()
    try:
        wq = db.query(WrongQuestion).filter(WrongQuestion.id == wrong_id).first()
        if not wq:
            return {"error": "错题记录不存在"}
        db.delete(wq)
        db.commit()
        return {"message": "错题已移除"}
    except Exception as e:
        db.rollback()
        return {"error": f"删除错题失败: {str(e)}"}
    finally:
        db.close()


@router.put("/wrong-questions/{wrong_id}/master")
def mark_wrong_mastered(wrong_id: int):
    """标记错题为已掌握"""
    db = SessionLocal()
    try:
        wq = db.query(WrongQuestion).filter(WrongQuestion.id == wrong_id).first()
        if not wq:
            return {"error": "错题记录不存在"}
        wq.mastered = 1
        db.commit()
        return {"message": "已标记为掌握", "mastered": True}
    except Exception as e:
        db.rollback()
        return {"error": f"标记失败: {str(e)}"}
    finally:
        db.close()


@router.post("/wrong-questions/reanswer/{wrong_id}")
def reanswer_wrong_question(
    wrong_id: int,
    body: dict = Body(..., description="请求体，包含 user_answer 字段"),
):
    """重做错题：提交答案后如果正确则自动标记为已掌握"""
    user_answer = body.get("user_answer", "") if isinstance(body, dict) else ""
    db = SessionLocal()
    try:
        wq = db.query(WrongQuestion).filter(WrongQuestion.id == wrong_id).first()
        if not wq:
            return {"error": "错题记录不存在"}

        correct_answer = wq.correct_answer
        is_correct = (user_answer.strip() == correct_answer.strip())

        if is_correct:
            wq.mastered = 1
            wq.user_answer = user_answer
            db.commit()
            return {
                "is_correct": True,
                "correct_answer": correct_answer,
                "analysis": wq.analysis,
                "message": "回答正确！已自动标记为掌握",
                "mastered": True,
            }
        else:
            wq.wrong_count += 1
            wq.user_answer = user_answer
            wq.last_wrong_at = datetime.utcnow()
            db.commit()
            return {
                "is_correct": False,
                "correct_answer": correct_answer,
                "analysis": wq.analysis,
                "message": "回答错误，再接再厉",
                "mastered": False,
            }
    except Exception as e:
        db.rollback()
        return {"error": f"重做错题失败: {str(e)}"}
    finally:
        db.close()


# ═══════════════════════════════════════════════════════════════
# 收藏管理接口
# ═══════════════════════════════════════════════════════════════

@router.get("/saved-questions")
def get_saved_questions(
    category: str = Query("", description="分类筛选"),
    question_type: str = Query("", description="题型筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
):
    """获取收藏列表"""
    db = SessionLocal()
    try:
        query = db.query(SavedQuestion)
        if category:
            query = query.filter(SavedQuestion.category == category)
        if question_type:
            query = query.filter(SavedQuestion.question_type == question_type)

        total = query.count()
        items = query.order_by(desc(SavedQuestion.id)).offset(
            (page - 1) * page_size
        ).limit(page_size).all()

        result = []
        for s in items:
            result.append({
                "id": s.id,
                "question_id": s.question_id,
                "question_type": s.question_type,
                "career": s.career,
                "category": s.category,
                "difficulty": s.difficulty,
                "question": s.question,
                "options": safe_json_loads(s.options_json),
                "source": s.source,
                "note": s.note,
                "created_at": s.created_at.strftime("%Y-%m-%d %H:%M") if s.created_at else "",
            })

        return {
            "saved_questions": result,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
        }
    except Exception as e:
        return {"error": f"获取收藏列表失败: {str(e)}"}
    finally:
        db.close()


@router.post("/saved-questions")
def save_question(
    question_id: int = Body(0, description="题目ID"),
    career: str = Body("", description="关联岗位"),
    category: str = Body("", description="分类"),
    difficulty: str = Body("medium", description="难度"),
    question: str = Body("", description="题目内容"),
    options_json: str = Body("[]", description="选项JSON"),
    source: str = Body("", description="来源"),
    note: str = Body("", description="收藏备注"),
):
    """收藏题目"""
    db = SessionLocal()
    try:
        existing = db.query(SavedQuestion).filter(
            SavedQuestion.question_id == question_id,
            SavedQuestion.question_type == "exam",
        ).first()
        if existing:
            return {"message": "题目已收藏，无需重复收藏", "id": existing.id}

        sq = SavedQuestion(
            question_id=question_id,
            question_type="exam",
            career=career,
            category=category,
            difficulty=difficulty,
            question=question,
            options_json=options_json,
            source=source,
            note=note,
        )
        db.add(sq)
        db.commit()
        db.refresh(sq)
        return {"message": "收藏成功", "id": sq.id}
    except Exception as e:
        db.rollback()
        return {"error": f"收藏失败: {str(e)}"}
    finally:
        db.close()


@router.delete("/saved-questions/{saved_id}")
def delete_saved_question(saved_id: int):
    """取消收藏"""
    db = SessionLocal()
    try:
        sq = db.query(SavedQuestion).filter(SavedQuestion.id == saved_id).first()
        if not sq:
            return {"error": "收藏记录不存在"}
        db.delete(sq)
        db.commit()
        return {"message": "已取消收藏"}
    except Exception as e:
        db.rollback()
        return {"error": f"取消收藏失败: {str(e)}"}
    finally:
        db.close()


# ═══════════════════════════════════════════════════════════════
# 统计数据接口
# ═══════════════════════════════════════════════════════════════

@router.get("/stats")
def get_exam_stats():
    """获取笔试相关的统计数据"""
    db = SessionLocal()
    try:
        wrong_count = db.query(func.count(WrongQuestion.id)).filter(
            WrongQuestion.question_type == "exam"
        ).scalar()
        mastered_count = db.query(func.count(WrongQuestion.id)).filter(
            WrongQuestion.question_type == "exam",
            WrongQuestion.mastered == 1,
        ).scalar()
        not_mastered = wrong_count - mastered_count

        total_wrong_attempts = db.query(func.sum(WrongQuestion.wrong_count)).filter(
            WrongQuestion.question_type == "exam"
        ).scalar() or 0

        total_saved = db.query(func.count(SavedQuestion.id)).filter(
            SavedQuestion.question_type == "exam"
        ).scalar()

        from models import InterviewSession
        total_interview_sessions = db.query(func.count(InterviewSession.id)).scalar()

        estimated_correct = max(0, int(total_wrong_attempts * 0.6))
        total_exam_done_est = total_wrong_attempts + estimated_correct
        accuracy_rate = round(estimated_correct / total_exam_done_est * 100, 1) if total_exam_done_est > 0 else 0

        return {
            "total_exam_done": total_exam_done_est,
            "total_correct": estimated_correct,
            "total_wrong": total_wrong_attempts,
            "accuracy_rate": f"{accuracy_rate}%",
            "wrong_not_mastered": not_mastered,
            "wrong_mastered": mastered_count,
            "total_saved": total_saved,
            "total_interview_sessions": total_interview_sessions,
        }
    except Exception as e:
        return {"error": f"获取统计数据失败: {str(e)}"}
    finally:
        db.close()


# ══════════════════════════════════════════
# 笔试统计接口（数据可视化用）
# ══════════════════════════════════════════

@router.get("/stats/overview")
def exam_stats_overview():
    """基础数据卡片：总刷题数 / 平均正确率 / 连续打卡天数 / 累计练习时长"""
    db = SessionLocal()
    try:
        from datetime import date, timedelta
        records = db.query(ExamRecord).all()
        total_questions = sum(r.total_questions for r in records)
        avg_accuracy = round(sum(r.accuracy for r in records) / len(records), 1) if records else 0
        total_seconds = sum(r.duration_seconds for r in records)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60

        practice_dates = sorted(set(
            r.created_at.date() for r in records if r.created_at
        ), reverse=True)
        streak = 0
        today = date.today()
        check = today
        while check in practice_dates:
            streak += 1
            check -= timedelta(days=1)
        if streak == 0:
            check = today - timedelta(days=1)
            while check in practice_dates:
                streak += 1
                check -= timedelta(days=1)

        return {
            "total_questions": total_questions,
            "avg_accuracy": avg_accuracy,
            "streak_days": streak,
            "total_hours": hours,
            "total_minutes": minutes,
        }
    finally:
        db.close()


@router.get("/stats/trend")
def exam_stats_trend(days: int = Query(7, description="天数")):
    """刷题量趋势（折线图数据）"""
    db = SessionLocal()
    try:
        from datetime import date, timedelta
        today = date.today()
        dates = [today - timedelta(days=i) for i in range(days - 1, -1, -1)]
        trend = []
        for d in dates:
            day_records = [r for r in db.query(ExamRecord).all() if r.created_at and r.created_at.date() == d]
            q_count = sum(r.total_questions for r in day_records)
            correct = sum(r.correct_count for r in day_records)
            wrong = sum(r.wrong_count for r in day_records)
            acc = round(correct / (correct + wrong) * 100, 1) if (correct + wrong) > 0 else 0
            trend.append({
                "date": d.isoformat(),
                "questions": q_count,
                "correct": correct,
                "wrong": wrong,
                "accuracy": acc
            })
        return {"trend": trend}
    finally:
        db.close()


@router.get("/stats/radar")
def exam_stats_radar(career: str = Query("", description="岗位")):
    """能力雷达图：各知识点掌握程度"""
    db = SessionLocal()
    try:
        kp_map = {}
        records = db.query(ExamRecord).all()
        for r in records:
            if career and r.career != career:
                continue
            try:
                answers = json.loads(r.answers_json) if r.answers_json else []
            except:
                answers = []
            for a in answers:
                qid = a.get("id", 0)
                q = db.query(ExamQuestion).filter(ExamQuestion.id == qid).first()
                if q and q.knowledge_point:
                    if q.knowledge_point not in kp_map:
                        kp_map[q.knowledge_point] = {"total": 0, "correct": 0}
                    kp_map[q.knowledge_point]["total"] += 1
                    if a.get("correct"):
                        kp_map[q.knowledge_point]["correct"] += 1

        if career and career in CAREER_KNOWLEDGE_MAP:
            all_kps = CAREER_KNOWLEDGE_MAP[career]["professional"]
        else:
            all_kps = list(kp_map.keys())[:6] if kp_map else ["编程基础", "数据结构", "数据库", "网络", "算法", "系统设计"]

        radar = []
        for kp in all_kps:
            data = kp_map.get(kp, {"total": 0, "correct": 0})
            mastery = round(data["correct"] / data["total"] * 100, 1) if data["total"] > 0 else 0
            radar.append({"name": kp, "total": data["total"], "correct": data["correct"], "mastery": mastery})
        return {"radar": radar}
    finally:
        db.close()


@router.get("/stats/error-distribution")
def exam_stats_error_distribution(career: str = Query("", description="岗位")):
    """错题分布（柱状图）：各知识点错题数"""
    db = SessionLocal()
    try:
        kp_wrong = {}
        wrongs = db.query(WrongQuestion).filter(
            WrongQuestion.question_type == "exam"
        ).all()
        for w in wrongs:
            if career and w.career != career:
                continue
            q = db.query(ExamQuestion).filter(ExamQuestion.id == w.question_id).first()
            kp = q.knowledge_point if q else "其他"
            if kp not in kp_wrong:
                kp_wrong[kp] = 0
            kp_wrong[kp] += 1

        items = sorted(kp_wrong.items(), key=lambda x: -x[1])
        return {
            "distribution": [
                {"name": k, "count": v} for k, v in items
            ]
        }
    finally:
        db.close()


@router.get("/stats/time-distribution")
def exam_stats_time_distribution():
    """时段分析（饼图）：练习时段分布"""
    db = SessionLocal()
    try:
        slots = {"凌晨(0-6点)": 0, "上午(6-12点)": 0, "下午(12-18点)": 0, "晚上(18-24点)": 0}
        records = db.query(ExamRecord).all()
        for r in records:
            if r.created_at:
                h = r.created_at.hour
                if 0 <= h < 6:
                    slots["凌晨(0-6点)"] += r.total_questions
                elif 6 <= h < 12:
                    slots["上午(6-12点)"] += r.total_questions
                elif 12 <= h < 18:
                    slots["下午(12-18点)"] += r.total_questions
                else:
                    slots["晚上(18-24点)"] += r.total_questions
        return {
            "distribution": [
                {"name": k, "value": v} for k, v in slots.items() if v > 0
            ]
        }
    finally:
        db.close()


@router.get("/stats/growth")
def exam_stats_growth():
    """成长对比：本周 vs 上周"""
    db = SessionLocal()
    try:
        from datetime import date, timedelta
        today = date.today()
        monday = today - timedelta(days=today.weekday())
        last_monday = monday - timedelta(days=7)
        last_sunday = monday - timedelta(days=1)

        def sum_week(start, end):
            q = 0
            c = 0
            w = 0
            for r in db.query(ExamRecord).all():
                if r.created_at and start <= r.created_at.date() <= end:
                    q += r.total_questions
                    c += r.correct_count
                    w += r.wrong_count
            acc = round(c / (c + w) * 100, 1) if (c + w) > 0 else 0
            return {"questions": q, "correct": c, "wrong": w, "accuracy": acc}

        this_week = sum_week(monday, today)
        last_week = sum_week(last_monday, last_sunday)

        change_questions = this_week["questions"] - last_week["questions"]
        change_accuracy = round(this_week["accuracy"] - last_week["accuracy"], 1)

        return {
            "this_week": this_week,
            "last_week": last_week,
            "change": {
                "questions": change_questions,
                "questions_percent": round(change_questions / last_week["questions"] * 100, 1) if last_week["questions"] > 0 else 100,
                "accuracy": change_accuracy
            }
        }
    finally:
        db.close()