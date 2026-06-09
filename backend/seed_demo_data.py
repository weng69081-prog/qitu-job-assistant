"""Seed realistic demo interview sessions into the database."""
import json
import random
from datetime import datetime, timedelta
from database import SessionLocal
from models import InterviewSession

JOB_CAREERS = [
    ("前端开发工程师", "技术"),
    ("后端开发工程师", "技术"),
    ("产品经理", "产品"),
    ("数据分析师", "数据"),
    ("UI/UX设计师", "设计"),
    ("运营专员", "运营"),
    ("算法工程师", "技术"),
    ("Java开发工程师", "技术"),
    ("全栈开发工程师", "技术"),
    ("Python开发工程师", "技术"),
]

MODES = ["ai", "basic", "mock"]

# ─── Realistic Q&A pairs ───
QA_PAIRS = {
    "前端开发工程师": [
        {
            "q": "请解释一下Vue的响应式原理。",
            "a": "Vue2通过Object.defineProperty对data中的每个属性进行getter/setter拦截，在getter中收集依赖（Dep和Watcher），在setter中通知更新。Vue3改用Proxy代理整个对象，可以拦截更多操作（如新增属性、数组索引），性能更好且不需要递归遍历。"
        },
        {
            "q": "CSS中BFC是什么？如何触发？",
            "a": "BFC（块级格式化上下文）是一个独立的渲染区域，内外元素互不影响。触发条件：float不为none、overflow不为visible、display为inline-block/flex/grid、position为absolute/fixed。常用于清除浮动、防止margin合并。"
        },
        {
            "q": "讲一下JavaScript的事件循环机制。",
            "a": "JS是单线程，事件循环分三步：①执行栈中的同步代码；②遇到异步任务（setTimeout/Promise/请求）交给WebAPI处理；③异步任务完成后回调进入任务队列（宏任务/微任务）。每个宏任务执行完都会清空微任务队列。Promise.then是微任务，setTimeout是宏任务。"
        },
        {
            "q": "前端性能优化你有做过哪些？",
            "a": "我主要做了这几方面：①图片懒加载和WebP格式转换；②代码分割（Vue的defineAsyncComponent配合路由懒加载）；③CDN加速静态资源；④减少重排重绘（使用transform替代top/left动画、批量DOM操作）；⑤开启gzip压缩；⑥利用浏览器缓存策略（强缓存+协商缓存）。"
        },
        {
            "q": "跨域问题你是怎么解决的？",
            "a": "开发环境用Vite的proxy代理解决。生产环境主要有几种方案：①后端配CORS（设置Access-Control-Allow-Origin等响应头）；②Nginx反向代理同源转发；③JSONP（仅支持GET）；④postMessage跨窗口通信。实际项目中最常用CORS+Nginx组合。"
        }
    ],
    "后端开发工程师": [
        {
            "q": "谈谈你对RESTful API的理解。",
            "a": "RESTful是一种API设计风格，核心原则：资源导向URL、HTTP动词表示操作（GET查/POST增/PUT全量更新/PATCH部分更新/DELETE删）、无状态通信、统一接口。我设计时一般资源URL用复数名词，版本号放URL或Header，返回统一JSON格式。"
        },
        {
            "q": "数据库索引的原理和适用场景？",
            "a": "MySQL默认使用B+树索引，叶子节点存数据地址，非叶子节点存索引键。优点是范围查询快、磁盘IO少。适用场景：频繁WHERE查询的列、JOIN关联列、ORDER BY列。不适合：频繁增删改的表（维护索引成本高）、值重复率高的列（如性别）、小表。"
        },
        {
            "q": "你怎么理解微服务架构？",
            "a": "微服务是把一个大型单体应用拆成多个独立的小服务，每个服务有独立的数据库、独立部署、独立开发。优点是：①各个服务可以独立扩展；②技术栈可以不同；③故障隔离。缺点是：①分布式事务复杂；②服务间通信有网络开销；③运维成本高。"
        },
        {
            "q": "Redis常见的数据结构和应用场景？",
            "a": "String：缓存、计数器、分布式锁（SETNX）；Hash：存储对象属性；List：消息队列、最新消息列表（LPUSH+BRPOP）；Set：标签系统、去重、共同好友（交集）；ZSet：排行榜、延时队列（score做时间戳）；HyperLogLog：UV统计；Bitmap：签到统计。"
        },
        {
            "q": "JWT认证和Session认证有什么区别？",
            "a": "Session是服务端存储会话状态，客户端只存session_id。优点是服务端可以主动失效。JWT把用户信息编码在token里，服务端无状态。优点是跨服务共享认证方便、不需要存储。缺点是一旦签发不能主动失效（除非引入黑名单）。一般登录用JWT做access token+refresh token组合。"
        }
    ],
    "产品经理": [
        {
            "q": "你怎么做需求优先级排序？",
            "a": "我主要用RICE模型：Reach（影响人数）、Impact（影响程度）、Confidence（信心指数）、Effort（开发成本）。另外结合Kano模型区分基本型、期望型、兴奋型需求。紧急重要的先做（四象限法），同时和产品大方向对齐。"
        },
        {
            "q": "讲一个你做过的成功产品决策。",
            "a": "之前负责一个在线教育App，用户留存率偏低。我分析数据发现70%的用户在注册后3天内没完成首次课程，就流失了。我推动加了一个「新手引导任务」功能：首次完成课程送会员体验。上线后7日留存从12%提升到28%，转化率提升40%。"
        },
        {
            "q": "如何确定一个功能要不要做？",
            "a": "①用户价值：解决什么真实痛点？②商业价值：对营收/留存/活跃有什么帮助？③技术可行性：现有架构支持吗？④ROI评估：开发成本vs预期收益。先做MVP验证假设，用A/B测试确认效果。不做没有明确验收标准的功能。"
        },
        {
            "q": "PRD应该包含哪些核心内容？",
            "a": "①项目背景和目标（量化指标）；②用户故事和流程图；③功能详述（正常流程+异常流程）；④原型图或交互说明；⑤数据埋点需求；⑥验收标准；⑦排期和依赖。我习惯在PRD开头加一个变更记录表，方便追溯。"
        },
        {
            "q": "和开发团队沟通不畅怎么办？",
            "a": "①提前让开发参与需求评审（不是定稿了才通知）；②PRD写清楚边界条件和异常场景；③用开发听得懂的语言——不要只说'用户体验不好'，要说'这个接口返回慢1秒，用户等待时间加长'；④建立需求变更流程，小变动周会同步，大变动重新排期。"
        }
    ],
    "数据分析师": [
        {
            "q": "AB测试的流程和注意事项？",
            "a": "①确定实验假设和核心指标；②样本量估算（用功效分析）；③随机分组保证两组同质；④跑实验期间不中途查看结果避免窥探效应；⑤跑够时间（至少一个完整业务周期）；⑥用假设检验判断显著性。常见坑：多重比较问题、新奇效应、实验污染。"
        },
        {
            "q": "SQL中窗口函数的使用场景？",
            "a": "窗口函数在不合并行的情况下计算聚合值。常见场景：ROW_NUMBER()做分组排名、LAG/LEAD取前后行值对比、SUM() OVER做累计求和、RANK/DENSE_RANK做排行榜。比如'查每个部门工资前三的员工'，用ROW_NUMBER() PARTITION BY部门 ORDER BY工资 DESC就能搞定。"
        },
        {
            "q": "用户留存分析你怎么做？",
            "a": "①日报留存（次日/7日/30日留存率曲线）；②同期群分析（按注册月份分组看每月留存变化）；③按用户行为分层（核心活跃用户/沉默用户/流失用户）；④流失预警模型（用Logistic回归或生存分析预测哪些用户即将流失）。"
        }
    ],
    "UI/UX设计师": [
        {
            "q": "你设计一个产品的设计系统时从哪开始？",
            "a": "①梳理现有组件和样式，做设计审计；②定义设计原则（如简洁、一致、可访问）；③建立色彩/字体/间距/图标的基础规范；④提取原子组件（按钮、输入框、卡片）；⑤沉淀业务组件（表格、筛选器、弹窗）；⑥形成文档并同步开发走组件化。"
        },
        {
            "q": "怎么验证你的设计方案？",
            "a": "①可用性测试（找5个目标用户操作原型，观察卡点和误操作）；②A/B测试（上线两个版本看数据差异）；③启发式评估（专家对照尼尔森十大原则过一遍）；④热力图分析（看用户实际点击分布）。我最常用的是可用性测试+热力图。"
        },
        {
            "q": "低保真和高保真原型各在什么阶段用？",
            "a": "低保真（线框图）在早期探索阶段用，快速验证信息架构和页面布局，修改成本低。高保真在方案定稿后用，模拟真实交互效果，用于用户测试和向干系人演示。我不建议跳过低保真直接做高保真——改起来太痛苦。"
        }
    ],
    "运营专员": [
        {
            "q": "用户增长有哪些常用手段？",
            "a": "①ASO优化（应用商店搜索优化）；②社交裂变（分享有奖/拼团/砍价）；③内容营销（干货文章/短视频引流）；④付费投放（信息流/搜索广告）；⑤渠道合作（异业互换/联名活动）；⑥老带新（推荐奖励/邀请码）；⑦私域运营（社群/企微转化）。"
        },
        {
            "q": "你怎么看数据决定运营策略？",
            "a": "先建立核心指标体系（AARRR模型：获客→激活→留存→收入→推荐）。每日监控核心指标异动，发现下降立即多维度拆解（渠道/地区/用户分层）。例如留存下降3%，拆开看是新用户留存差还是老用户流失，再针对性调整策略。"
        },
        {
            "q": "策划一个活动的基本流程？",
            "a": "①明确目标（拉新/促活/转化/品牌）；②确定目标用户画像；③设计活动机制（奖品/规则/参与方式）；④输出活动方案和排期；⑤协调设计和开发；⑥上线前全链路测试；⑦上线后实时监控数据；⑧活动结束后复盘（数据复盘+用户反馈+改进方向）。"
        }
    ],
    "算法工程师": [
        {
            "q": "过拟合怎么解决？",
            "a": "①增加训练数据量（数据增强/迁移学习）；②降低模型复杂度（减少层数/特征选择）；③正则化（L1/L2正则化，Dropout）；④早停；⑤集成学习（Bagging/随机森林）；⑥交叉验证。实践中最好先检查是否数据泄露导致幻觉过拟合。"
        },
        {
            "q": "特征工程你一般怎么做？",
            "a": "①特征提取（文本TF-IDF/Word2Vec、图像CNN特征）；②特征构造（交叉特征、聚合特征、时间窗特征）；③特征选择（方差过滤/卡方检验/互信息/LASSO回归）；④特征缩放（标准化/归一化）。好的特征工程比调参更有效。"
        },
        {
            "q": "ROC曲线和AUC怎么理解？",
            "a": "ROC曲线以FPR（假正率）为X轴、TPR（真正率/召回率）为Y轴。AUC是ROC曲线下的面积，值越大模型区分正负样本的能力越强。AUC=0.5表示随机猜，AUC=1表示完美分类。正负样本不平衡时，AUC比准确率更稳定。"
        }
    ],
    "Java开发工程师": [
        {
            "q": "HashMap的底层实现原理？",
            "a": "JDK8中HashMap是数组+链表+红黑树。根据key的hashCode计算桶位置。哈希冲突时用链表（超过8个转红黑树）。put流程：计算hash→定位桶→遍历链表/树找key→找不到就插入。负载因子默认0.75，超过阈值（容量×0.75）就扩容到2倍。"
        },
        {
            "q": "Spring的IoC和AOP是怎么实现的？",
            "a": "IoC（控制反转）：Spring容器通过反射创建和管理Bean，开发者只需声明依赖，由容器注入。AOP（面向切面）：基于动态代理——实现接口的类用JDK动态代理，没实现接口的用CGLIB代理。典型应用：事务管理、日志记录、权限校验。"
        },
        {
            "q": "线程池的参数和拒绝策略？",
            "a": "核心参数：corePoolSize（核心线程数）、maxPoolSize（最大线程数）、keepAliveTime（空闲存活时间）、workQueue（任务队列）。拒绝策略：AbortPolicy（抛异常）、CallerRunsPolicy（调用者线程执行）、DiscardPolicy（丢弃）、DiscardOldestPolicy（丢弃最旧）。"
        }
    ],
    "全栈开发工程师": [
        {
            "q": "从输入URL到页面渲染，发生了什么？",
            "a": "①DNS解析域名→IP；②TCP三次握手建立连接；③发送HTTP请求；④服务器处理并返回响应；⑤浏览器解析HTML构建DOM树；⑥解析CSS构建CSSOM树；⑦合并成渲染树；⑧布局计算位置；⑨绘制像素到屏幕。现在还有HTTP/2多路复用和缓存策略优化这个过程。"
        },
        {
            "q": "你是怎么设计数据库表的？",
            "a": "①先理清业务实体和关系（1:1/1:N/N:M）；②设计E-R图；③确定主键（自增ID/UUID/雪花算法）；④考虑索引（高频查询字段加索引，联合索引覆盖更多查询）；⑤范式化到第三范式，必要时候反范式（用冗余换性能）。"
        },
        {
            "q": "用户登录流程你是怎么实现的？",
            "a": "前端提交账号密码→后端校验→校验通过生成JWT（含用户ID和过期时间）→返回给前端→前端存入localStorage→后续请求带Authorization header→中间件解析JWT并校验→放行或拒绝。密码存库时加盐哈希（bcrypt），不用明文。敏感操作需要二次验证。"
        }
    ],
    "Python开发工程师": [
        {
            "q": "Python的GIL是什么？怎么绕过？",
            "a": "GIL（全局解释器锁）确保同一时刻只有一个线程执行Python字节码。多线程在CPU密集型场景反而更慢。绕过：①IO密集型用多线程（GIL在IO等待时释放）；②CPU密集型用多进程（multiprocessing）；③用C扩展（numpy/cython）；④用asyncio做协程并发。"
        },
        {
            "q": "Django和Flask的区别，你什么时候选哪个？",
            "a": "Django大而全：内置ORM、Admin后台、认证系统、模板引擎，适合中大型项目。Flask轻量灵活：只有核心功能，扩展按需加，适合微服务和API项目。我个人偏好：快速原型用Flask，需要Admin管理后台用Django。"
        },
        {
            "q": "Python装饰器的原理和作用？",
            "a": "装饰器本质是接受函数并返回函数的可调用对象。@decorator等价于func=decorator(func)。常用于：日志记录、性能计时、权限校验、事务管理、缓存。带参数的装饰器需要包三层函数：外层接收参数→中间层接收函数→内层接收*args/**kwargs。"
        }
    ],
}

# ─── Realistic emotion patterns ───
def gen_emotions(interview_len_minutes=8):
    emotions = []
    patterns = [
        # Early interview: nervous -> calm -> confident
        {"emotion": "紧张", "confidence": 70},
        {"emotion": "平静", "confidence": 75},
        {"emotion": "自信", "confidence": 80},
        {"emotion": "平静", "confidence": 82},
        {"emotion": "自信", "confidence": 88},
    ]
    base_time = datetime(2025, 6, 1, 10, 0, 0).timestamp() * 1000
    for i, p in enumerate(patterns):
        emotions.append({
            "emotion": p["emotion"],
            "confidence": p["confidence"] + random.randint(-5, 5),
            "time": int(base_time + i * 60000) + random.randint(-10000, 10000),
            "round": i + 1,
            "details": {
                p["emotion"]: min(100, p["confidence"] + random.randint(-10, 10)),
                "开心": random.randint(40, 60),
                "困惑": random.randint(5, 20),
            }
        })
    return emotions

def gen_emotions_varied():
    """Generate varied emotion sets for different sessions."""
    templates = [
        # Confident throughout
        [("自信", 85), ("自信", 90), ("自信", 88), ("平静", 80), ("自信", 92)],
        # Started nervous, gained confidence
        [("紧张", 65), ("平静", 72), ("自信", 78), ("自信", 85), ("自信", 90)],
        # Calm and steady
        [("平静", 80), ("平静", 82), ("平静", 78), ("平静", 85), ("平静", 80)],
        # Mixed emotions
        [("紧张", 55), ("困惑", 60), ("平静", 70), ("自信", 75), ("自信", 80)],
        # Very positive
        [("开心", 88), ("自信", 90), ("开心", 92), ("自信", 88), ("开心", 95)],
    ]
    tmpl = random.choice(templates)
    emotions = []
    base_time = datetime(2025, 6, random.randint(1, 8), random.randint(9, 17), random.randint(0, 59)).timestamp() * 1000
    for i, (emotion, conf) in enumerate(tmpl):
        emotions.append({
            "emotion": emotion,
            "confidence": min(100, conf + random.randint(-8, 8)),
            "time": int(base_time + i * (60000 + random.randint(-15000, 15000))),
            "round": i + 1,
            "details": {
                emotion: min(100, conf + random.randint(-5, 15)),
                "开心": random.randint(30, 70),
                "困惑": random.randint(0, 25),
                "紧张": random.randint(0, 20),
            }
        })
    return emotions


def gen_session_data(job, category):
    """Generate a complete fake interview session."""
    qa_list = QA_PAIRS.get(job, QA_PAIRS["前端开发工程师"])
    selected = random.sample(qa_list, min(len(qa_list), random.randint(2, 5)))

    # Sort to make the order feel natural
    total_q = len(selected)

    # Generate per-question scores that vary
    base_score = random.randint(65, 92)
    per_q_scores = []
    for i in range(total_q):
        score = base_score + random.randint(-15, 10)
        per_q_scores.append(max(40, min(98, score)))

    overall = round(sum(per_q_scores) / len(per_q_scores))

    dimensions = {
        "专业知识掌握度": {"score": min(98, max(40, overall + random.randint(-10, 10))), "comment": random.choice(["基础扎实", "知识面广", "有深度", "继续加强", "回答充分"])},
        "语言表达与逻辑": {"score": min(98, max(40, overall + random.randint(-8, 8))), "comment": random.choice(["条理清晰", "逻辑严密", "表达流畅", "可以更简洁", "层次分明"])},
        "临场应变能力": {"score": min(98, max(40, overall + random.randint(-12, 5))), "comment": random.choice(["反应快", "思路开阔", "临场不慌", "稍显紧张", "应对得当"])},
        "岗位匹配度": {"score": min(98, max(40, overall + random.randint(-5, 12))), "comment": random.choice(["高度匹配", "方向一致", "潜力股", "合适人选", "有培养空间"])},
    }

    # Generate answers list (alternating assistant/user)
    answers = []
    for i, pair in enumerate(selected):
        answers.append({"role": "assistant", "content": pair["q"]})
        answers.append({"role": "user", "content": pair["a"]})

    avg_pq = round(sum(per_q_scores) / len(per_q_scores))

    strengths_pool = [
        "回答有深度，能结合项目经验", "逻辑思维清晰，层层递进",
        "对基础知识掌握扎实", "能主动思考问题的边界条件",
        "沟通表达简洁明了", "对技术趋势有跟进",
        "能提出自己的见解而非照本宣科", "对岗位职责理解清晰"
    ]
    weaknesses_pool = [
        "部分问题回答不够具体", "可以多结合真实案例",
        "对底层原理理解有待加强", "建议多关注行业最佳实践",
        "回答可以更结构化", "可以展示更多主动性",
        "表达可以更自信", "拓展知识的广度"
    ]

    strengths = random.sample(strengths_pool, random.randint(2, 3))
    weaknesses = random.sample(weaknesses_pool, random.randint(2, 3))
    suggestions = [
        "建议多练习系统设计类题目",
        "可以系统地梳理一下自己的项目经验",
        "建议关注行业前沿技术动态",
        "可以尝试用STAR法则组织项目经历描述",
        "多参加模拟面试，提升临场表现",
    ][:random.randint(2, 3)]

    emotions = gen_emotions_varied()

    # Timestamp within past week
    past_days = random.randint(0, 7)
    past_hours = random.randint(8, 22)
    created_at = datetime(2025, 6, 1, 10, 0, 0) - timedelta(days=past_days, hours=random.randint(0, 12))

    return {
        "job": job,
        "category": category,
        "mode": random.choice(MODES),
        "total_questions": total_q,
        "average_score": avg_pq,
        "highest_score": max(per_q_scores),
        "lowest_score": min(per_q_scores),
        "answers_json": json.dumps(answers, ensure_ascii=False),
        "dimensions_json": json.dumps(dimensions, ensure_ascii=False),
        "strengths_json": json.dumps(strengths, ensure_ascii=False),
        "weaknesses_json": json.dumps(weaknesses, ensure_ascii=False),
        "suggestions_json": json.dumps(suggestions, ensure_ascii=False),
        "emotions_json": json.dumps(emotions, ensure_ascii=False),
        "created_at": created_at,
    }


def seed():
    db = SessionLocal()
    # Delete existing demo sessions (keep any that are real)
    # We'll keep all existing ones and just add new ones

    count = 0
    for job, category in JOB_CAREERS:
        # 1-2 sessions per job
        for _ in range(random.randint(1, 2)):
            data = gen_session_data(job, category)
            session = InterviewSession(**data)
            db.add(session)
            count += 1
            print(f"  [{count}] {data['job']} | 总分{data['average_score']} | {data['total_questions']}题 | {data['created_at'].strftime('%m/%d %H:%M')}")

    db.commit()
    db.close()
    print(f"\n✅ 共插入 {count} 条面试记录！")
    print("刷新页面即可看到修改后的数据。")


if __name__ == "__main__":
    seed()