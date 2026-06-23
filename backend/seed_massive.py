"""大量填充演示数据（修正字段名版）"""
from database import SessionLocal, engine, Base
from models import (
    User, Profile, InterviewSession, ExamRecord, WeaknessItem,
    LearningPath, LearningNode, LearningResource, LearningNote,
    ReviewSchedule, SmartResume, ExamQuestion, WrongQuestion,
    SavedQuestion
)
from datetime import datetime, timedelta
import json, hashlib, secrets, random

now = datetime.utcnow()
uid = 1


def hash_pw(password: str, salt: str = "") -> tuple:
    if not salt:
        salt = secrets.token_hex(8)
    h = hashlib.sha256((password + salt).encode()).hexdigest()
    return h, salt


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 清空重来
        for t in [LearningNode, LearningResource, LearningNote, ReviewSchedule,
                  SmartResume, WeaknessItem, InterviewSession, ExamRecord,
                  ExamQuestion, WrongQuestion, SavedQuestion]:
            db.query(t).delete()
        db.query(Profile).delete()
        db.query(User).delete()
        db.commit()

        # 创建demo用户
        h, s = hash_pw("demo")
        user = User(username="demo", password_hash=h+":"+s, nickname="小明")
        db.add(user)
        db.flush()
        uid = user.id

        prof = Profile(user_id=uid, education="本科", major="计算机科学与技术",
                       city="北京", skills="Java, Python, JavaScript, SQL, Vue",
                       grade="大一", job_targets="前端开发工程师",
                       experience="学校ACM社团项目开发", interests="Web开发、算法")
        db.add(prof)

        # ═══ 面试记录 10条 ═══
        for i, (job, avg, weak) in enumerate([
            ("前端开发", 72, ["JavaScript异步编程不熟", "CSS布局不够灵活"]),
            ("Java开发", 65, ["Java集合框架理解不深", "多线程编程薄弱"]),
            ("前端开发", 78, ["Vue响应式原理不熟", "性能优化经验不足"]),
            ("Python开发", 82, ["算法题不够熟练", "数据库优化经验少"]),
            ("全栈开发", 70, ["前后端联调经验不足", "部署流程不熟"]),
            ("前端开发", 85, ["TypeScript泛型不熟", "Webpack配置不深"]),
            ("Java开发", 68, ["微服务架构不熟", "Redis使用经验少"]),
            ("数据分析", 75, ["SQL优化不够", "可视化工具不熟"]),
            ("算法工程师", 60, ["动态规划薄弱", "机器学习理论不深"]),
            ("产品经理", 80, ["PRD文档规范不够", "数据分析思维不足"]),
        ]):
            dims = random.choice([
                {"专业知识":72,"代码能力":68,"算法思维":65,"项目经验":60,"语言表达":78,"沟通协作":80,"学习能力":85,"职业素养":75},
                {"专业知识":65,"代码能力":70,"算法思维":60,"项目经验":55,"语言表达":78,"沟通协作":80,"学习能力":85,"职业素养":75},
                {"专业知识":80,"代码能力":85,"算法思维":75,"项目经验":70,"语言表达":82,"沟通协作":78,"学习能力":90,"职业素养":80},
            ])
            db.add(InterviewSession(
                job=job, category="计算机类", average_score=avg,
                highest_score=avg+12, lowest_score=avg-8,
                total_questions=random.randint(4,7),
                dimensions_json=json.dumps(dims),
                weaknesses_json=json.dumps(weak),
                strengths_json=json.dumps(["学习能力强","态度积极","逻辑清晰"]),
                suggestions_json=json.dumps(["多练习项目实战","加强基础理论知识"]),
                answers_json="[]", created_at=now-timedelta(days=random.randint(1,30))
            ))

        # ═══ 笔试题库 10条 ═══
        for cat, q, opts, ans, diff in [
            ("Java","JVM垃圾回收的算法有哪些？",["标记-清除","复制算法","标记-整理","以上都是"],"D","中等"),
            ("Java","Spring Boot自动配置的原理？",["@EnableAutoConfiguration","@SpringBootApplication","条件注解","以上都是"],"D","困难"),
            ("Java","HashMap和ConcurrentHashMap的区别？",["线程安全","性能差异","底层结构不同","以上都对"],"D","中等"),
            ("前端","React Hooks和Vue Composition API的区别？",["设计理念不同","语法不同","响应式原理不同","以上都是"],"D","困难"),
            ("前端","CSS中flex:1代表什么？",["flex-grow:1","flex:1 1 0%","flex:1 0 auto","flex:0 1 auto"],"B","简单"),
            ("数据库","MySQL的MVCC机制是什么？",["多版本并发控制","乐观锁","悲观锁","读写分离"],"A","困难"),
            ("数据库","B+树索引和哈希索引的区别？",["范围查询能力","等值查询效率","存储结构不同","以上都是"],"D","中等"),
            ("算法","LRU缓存如何实现？",["HashMap+双向链表","数组","队列","栈"],"A","中等"),
            ("网络","HTTPS的TLS握手过程中非对称加密的作用？",["传输对称密钥","加密数据","身份认证","A和C"],"D","困难"),
            ("网络","HTTP/2相比HTTP/1.1的改进？",["多路复用","头部压缩","服务端推送","以上都是"],"D","中等"),
            ("Python","Python装饰器的作用？",["增强函数功能","修改函数结构","替代函数","删除函数"],"A","简单"),
            ("Python","GIL对Python多线程的影响？",["限制并行执行","无影响","提高性能","替代线程"],"A","中等"),
        ]:
            db.add(ExamQuestion(
                category=cat, question=q,
                options_json=json.dumps([{"label":chr(65+i),"text":o} for i,o in enumerate(opts)]),
                answer=ans, difficulty=diff
            ))

        # ═══ 错题本 15条 ═══
        for q, ua, ca, wc, cat in [
            ("Java中HashMap的底层数据结构是？","数组","数组+链表+红黑树",3,"Java"),
            ("Vue3的Composition API与Options API的区别？","语法不同","Composition API更适合逻辑复用和TypeScript支持",2,"前端"),
            ("TCP三次握手的详细过程？","SYN-SYN-ACK","SYN→SYN-ACK→ACK，分别对应seq=x,seq=y+ack=x+1,seq=x+1+ack=y+1",4,"网络"),
            ("SQL中INNER JOIN和LEFT JOIN的区别？","INNER只返回匹配行","INNER JOIN只返回两表匹配的行，LEFT JOIN返回左表所有行+右表匹配行",2,"数据库"),
            ("什么是JVM的垃圾回收机制？","自动回收无用对象","通过标记-清除/复制/标记-整理算法自动回收堆中不再被引用的对象",5,"Java"),
            ("CSS中Flex布局和Grid布局的区别？","一个一维一个二维","Flex是一维布局（行或列），Grid是二维布局（行列同时控制）",1,"前端"),
            ("HTTPS的SSL/TLS握手过程？","加密通信","ClientHello→ServerHello+证书→密钥交换→ChangeCipherSpec→加密通信",3,"网络"),
            ("React中useEffect的清理函数什么时候执行？","组件卸载时","组件卸载时和依赖变化前执行",2,"前端"),
            ("MySQL索引为什么会失效？","查询数据量太大","使用LIKE前导模糊查询、函数运算导致索引失效",3,"数据库"),
            ("快速排序的最坏时间复杂度？","O(n)","O(n²)，当每次选择的基准元素都是最大或最小时",2,"算法"),
            ("HTTP状态码304的含义？","重定向","未修改（Not Modified），告诉客户端使用缓存",1,"网络"),
            ("Vue中v-if和v-show的区别？","都隐藏元素","v-if销毁/创建元素，v-show切换display属性",2,"前端"),
            ("Python中列表和元组的区别？","都可以修改","列表(list)可变，元组(tuple)不可变",1,"Python"),
            ("什么是跨域问题？","接口调用失败","不同源（协议/域名/端口不同）之间的请求被浏览器拦截",3,"前端"),
            ("Spring中@Autowired和@Resource的区别？","用法相同","@Autowired按类型注入，@Resource按名称注入",2,"Java"),
        ]:
            db.add(WrongQuestion(
                question_type="exam", category=cat, question=q,
                user_answer=ua, correct_answer=ca, wrong_count=wc,
                last_wrong_at=now-timedelta(days=random.randint(1,14)), source="exam"
            ))

        # ═══ 收藏题 12条 ═══
        saved_items = [
            ("Java集合框架面试题汇总","Java","文章"),
            ("Vue3响应式原理详解","前端","视频"),
            ("SQL优化实战50例","数据库","文章"),
            ("设计模式全解（23种）","架构","视频"),
            ("计算机网络面试必问","网络","文章"),
            ("算法刷题指南（LeetCode分类）","算法","文章"),
            ("系统设计入门教程","架构","视频"),
            ("Python异步编程完全指南","Python","文章"),
            ("Git工作流最佳实践","工具","文章"),
            ("Docker从入门到精通","运维","视频"),
            ("微服务架构设计原理","架构","文章"),
            ("Redis缓存实战指南","数据库","视频"),
        ]
        for title, cat, qtype in saved_items:
            db.add(SavedQuestion(
                question_type="exam", career="前端开发", category=cat,
                question=title, note="收藏以便复习",
                created_at=now-timedelta(days=random.randint(1,60))
            ))

        # ═══ 笔试记录 8条 ═══
        for mode, total, correct, acc in [
            ("专项练习",10,6,65),("模拟卷",15,11,72),("专项练习",8,7,88),
            ("模拟卷",20,14,70),("Java专项",12,9,75),("前端专项",10,8,80),
            ("真题模拟",25,17,68),("数据结构专项",15,10,67),
        ]:
            db.add(ExamRecord(
                career="前端开发", mode=mode, total_questions=total,
                correct_count=correct, wrong_count=total-correct, accuracy=acc,
                duration_seconds=random.randint(1200,3600), answers_json="[]",
                knowledge_json=json.dumps({"Java":70,"前端":75,"数据库":60}),
                created_at=now-timedelta(days=random.randint(1,40))
            ))

        # ═══ 薄弱点 10条 ═══
        for nm, sc, cat in [
            ("JavaScript异步编程",45,"interview"),("CSS布局",50,"interview"),
            ("Vue响应式原理",40,"interview"),("Java集合框架",50,"exam"),
            ("多线程编程",35,"exam"),("SQL优化",55,"exam"),
            ("算法动态规划",30,"exam"),("Webpack配置",45,"exam"),
            ("TypeScript泛型",40,"exam"),("微服务架构",38,"interview"),
        ]:
            db.add(WeaknessItem(user_id=uid, name=nm, score=sc, category=cat,
                               source=cat, career="前端开发", detected_count=random.randint(2,6)))

        # ═══ 学习路线 3条 ═══
        paths = [
            ("前端开发","前端开发入门到实战","从前端基础知识到项目实战的完整学习路径","beginner",5,20),
            ("Java开发","Java后端从零到就业","Java基础→SSM→微服务的系统学习","beginner",6,10),
            ("算法","算法与数据结构精进","LeetCode面试算法系统训练","intermediate",5,5),
        ]
        nodes_data = {
            "前端开发入门到实战": [
                ("HTML/CSS基础","掌握网页结构搭建和样式设计",0,"约7天","easy","completed"),
                ("JavaScript核心","理解变量、函数、DOM操作等JS基础",1,"约14天","easy","in_progress"),
                ("Vue框架入门","学习组件化开发、路由、状态管理",2,"约21天","medium","pending"),
                ("前端工程化","Webpack、Vite、ESLint等工具链",3,"约10天","hard","pending"),
                ("实战项目","完成一个完整的前端项目",4,"约30天","hard","pending"),
            ],
            "Java后端从零到就业": [
                ("Java基础核心","面向对象、集合、IO、异常处理",0,"约14天","easy","completed"),
                ("数据库与SQL","MySQL设计、索引、事务、优化",1,"约14天","easy","in_progress"),
                ("Spring Boot实战","REST API、MyBatis、JPA",2,"约21天","medium","pending"),
                ("微服务与中间件","Redis、RabbitMQ、Docker",3,"约21天","hard","pending"),
                ("项目实战","电商/社交类后端完整开发",4,"约30天","hard","pending"),
                ("面试冲刺","简历指导、面经刷题、模拟面试",5,"约14天","hard","pending"),
            ],
            "算法与数据结构精进": [
                ("线性表与字符串","数组、链表、栈、队列基础",0,"约7天","easy","completed"),
                ("树与图","二叉树遍历、图搜索、最短路径",1,"约10天","medium","in_progress"),
                ("动态规划","背包问题、区间DP、状态压缩",2,"约14天","hard","pending"),
                ("排序与查找","十大排序、二分查找变种",3,"约7天","medium","pending"),
                ("高频面试150题","LeetCode热题分类精刷",4,"约21天","hard","pending"),
            ],
        }
        for career, title, desc, diff, total, prog in paths:
            path = LearningPath(user_id=uid, career=career, title=title, description=desc,
                               difficulty=diff, total_nodes=total, progress=prog, is_active=1)
            db.add(path)
            db.flush()
            for nd in nodes_data.get(title, []):
                db.add(LearningNode(path_id=path.id, user_id=uid, title=nd[0],
                    description=nd[1], order_index=nd[2], duration=nd[3],
                    difficulty=nd[4], status=nd[5],
                    completed_at=now-timedelta(days=15) if nd[5]=="completed" else None))

        # ═══ 学习资源 20条 ═══
        for title, url, rtype in [
            ("MDN Web文档","https://developer.mozilla.org/zh-CN/","article"),
            ("Vue3官方文档","https://vuejs.org/","article"),
            ("现代JavaScript教程","https://zh.javascript.info/","article"),
            ("React官方文档","https://react.dev/","article"),
            ("JavaGuide面试指南","https://javaguide.cn/","article"),
            ("Spring官方文档","https://spring.io/docs","article"),
            ("MySQL官方手册","https://dev.mysql.com/doc/","article"),
            ("LeetCode题库","https://leetcode.cn/","exercise"),
            ("代码随想录","https://programmercarl.com/","article"),
            ("小林Coding图解网络","https://xiaolincoding.com/","article"),
            ("阮一峰ES6教程","https://es6.ruanyifeng.com/","article"),
            ("Webpack官方文档","https://webpack.js.org/","article"),
            ("Docker从入门到实践","https://yeasy.gitbook.io/docker_practice/","article"),
            ("Python官方文档","https://docs.python.org/zh-cn/3/","article"),
            ("廖雪峰Python教程","https://www.liaoxuefeng.com/wiki/1016959663602400","article"),
            ("尚硅谷Java入门视频","https://www.bilibili.com/video/BV1Kb411W75N","video"),
            ("Vue3+TypeScript实战项目","https://www.bilibili.com/video/BV1dS4y1y7vd","video"),
            ("数据结构与算法基础","https://www.bilibili.com/video/BV1Cz411B7mC","video"),
            ("Python数据分析入门","https://www.bilibili.com/video/BV1q4411N7uC","video"),
            ("设计模式精讲视频","https://www.bilibili.com/","video"),
        ]:
            db.add(LearningResource(node_id=1, user_id=uid, title=title,
                   resource_type=rtype, url=url, is_done=random.choice([0,1])))

        # ═══ 学习笔记 10条 ═══
        for title, content in [
            ("Vue3响应式原理解析","Vue3使用Proxy代理对象实现响应式，比Vue2的defineProperty更强大，支持数组和新增属性的响应式。"),
            ("Java集合框架总结","Collection（List/Set/Queue）和Map两大类。ArrayList底层数组，LinkedList双向链表，HashMap数组+链表+红黑树。"),
            ("HTTP状态码速记","2xx成功、3xx重定向、4xx客户端错误、5xx服务端错误。记住301永久重定向/302临时/304缓存/401未授权/403禁止/404未找到/500内部错误/502网关错误。"),
            ("CSS居中完全指南","水平居中：text-align:center/margin:0 auto/flex/absolute+transform。垂直居中：flex align-items/absolute+transform/grid。"),
            ("MySQL索引优化笔记","联合索引最左前缀原则，避免%前缀模糊查询，索引列不做函数运算，回表查询尽量用覆盖索引。"),
            ("Redis面试重点","五种数据类型String/Hash/List/Set/ZSet，过期策略定期删除+惰性删除，持久化RDB+AOF，哨兵+集群高可用。"),
            ("JavaScript闭包理解","闭包=函数+它声明时的词法环境。用途：数据私有化、回调函数、高阶函数、模块模式。注意内存泄漏问题。"),
            ("Docker常用命令","docker pull/run/ps/exec/stop/rm/images/build，docker-compose up/down。制作Dockerfile注意层级缓存。"),
            ("Git工作流总结","feature分支开发→develop合并→release分支→master。常用git merge/rebase/reset/stash/cherry-pick。"),
            ("Spring Boot自动配置","@SpringBootApplication=@Configuration+@EnableAutoConfiguration+@ComponentScan。自动配置基于条件注解@Conditional。"),
        ]:
            db.add(LearningNote(user_id=uid, title=title, content=content,
                              created_at=now-timedelta(days=random.randint(1,60))))

        # ═══ 复习计划 6条 ═══
        for title, cat in [
            ("Vue3核心知识复习","前端框架"),("Java集合框架","Java基础"),
            ("MySQL索引优化","数据库"),("HTTP/TCP协议","计算机网络"),
            ("排序算法汇总","算法"),("设计模式复习","架构设计"),
        ]:
            db.add(ReviewSchedule(user_id=uid, title=title, reviewed_count=random.randint(1,5),
                                next_review_at=(now+timedelta(days=random.randint(1,14))).strftime("%Y-%m-%d"),
                                last_reviewed_at=(now-timedelta(days=random.randint(1,20))).strftime("%Y-%m-%d")))

        # ═══ 智能简历 3条 ═══
        for career, summary in [
            ("前端开发工程师","精通Vue3/React框架，有多个完整项目经验，熟悉前端工程化和性能优化。"),
            ("Java后端开发","熟练掌握Spring Boot/MyBatis框架，了解微服务架构和Redis缓存。"),
            ("全栈开发","前后端全栈能力，Vue3+Spring Boot技术栈，有项目从零到部署的经验。"),
        ]:
            db.add(SmartResume(user_id=uid, career=career, summary=summary,
                             skills_text="Vue3, React, Java, Python, MySQL, Docker",
                             education_text="郑州西亚斯学院 · 计算机科学与技术 · 本科",
                             match_score=random.randint(65, 92)))

        db.commit()
        print(f"✅ 大量演示数据填充完成！用户: demo / demo")

        # 统计
        for t_name, t_obj in [("面试记录",InterviewSession),("笔试题",ExamQuestion),
                              ("错题",WrongQuestion),("收藏",SavedQuestion),
                              ("笔试记录",ExamRecord),("薄弱点",WeaknessItem),
                              ("学习路线",LearningPath),("学习资源",LearningResource),
                              ("学习笔记",LearningNote),("复习计划",ReviewSchedule),
                              ("智能简历",SmartResume)]:
            c = db.query(t_obj).count()
            print(f"  {t_name}: {c}条")

    except Exception as e:
        db.rollback()
        print(f"❌ {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
