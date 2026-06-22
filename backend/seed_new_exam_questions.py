"""Replace EXPANDED_MOCK_QUESTIONS with career-specific interview questions.

Each career gets 15-25 questions covering real interview topics:
- Career-specific knowledge questions
- Scenario-based problem solving
- System design/architecture
- Best practices and trade-offs
"""
import json
from database import SessionLocal, engine
from models import ExamQuestion
from sqlalchemy import text

NEW_QUESTIONS = []

def q(kp, cat, career, diff, qtype, question, options, answer, analysis):
    NEW_QUESTIONS.append({
        "knowledge_point": kp,
        "category": cat,
        "career": career,
        "difficulty": diff,
        "question_type": qtype,
        "question": question,
        "options": options,
        "answer": answer,
        "analysis": analysis,
    })

# ═══════════════════════════════════════════
# 前端开发工程师（25题）
# ═══════════════════════════════════════════
q("JavaScript核心", "专业", "前端开发工程师", "easy", "single_choice",
  "以下哪种情况会导致JavaScript中的this指向window（浏览器环境）？",
  [{"key":"A","value":"对象方法中调用this"},{"key":"B","value":"箭头函数中的this"},{"key":"C","value":"普通函数直接调用"},{"key":"D","value":"事件处理函数中的this"}],
  "C", "普通函数直接调用时，非严格模式下this指向全局对象window。")

q("JavaScript核心", "专业", "前端开发工程师", "medium", "single_choice",
  "以下代码输出什么？\nconsole.log(1);\nsetTimeout(() => console.log(2), 0);\nPromise.resolve().then(() => console.log(3));\nconsole.log(4);",
  [{"key":"A","value":"1 2 3 4"},{"key":"B","value":"1 4 2 3"},{"key":"C","value":"1 4 3 2"},{"key":"D","value":"4 1 2 3"}],
  "C", "同步代码先执行（1和4），微任务(Promise.then)在宏任务(setTimeout)之前执行，所以输出1 4 3 2。")

q("JavaScript核心", "专业", "前端开发工程师", "medium", "single_choice",
  "以下哪种方式可以正确实现深拷贝？",
  [{"key":"A","value":"let b = a"},{"key":"B","value":"let b = Object.assign({}, a)"},{"key":"C","value":"let b = JSON.parse(JSON.stringify(a))"},{"key":"D","value":"let b = {...a}"}],
  "C", "JSON.parse(JSON.stringify())是目前最常用的深拷贝方式，但会丢失function、undefined、Symbol等属性。A/B/D都是浅拷贝。")

q("JavaScript核心", "专业", "前端开发工程师", "hard", "single_choice",
  "以下代码输出什么？\nfor (var i = 0; i < 3; i++) {\n  setTimeout(() => console.log(i), 100);\n}",
  [{"key":"A","value":"0 1 2"},{"key":"B","value":"3 3 3"},{"key":"C","value":"undefined undefined undefined"},{"key":"D","value":"0 0 0"}],
  "B", "var声明的i是函数级作用域，循环结束后i=3。三个setTimeout回调执行时都引用同一个i。用let声明可得到预期结果0 1 2。")

q("Vue.js", "专业", "前端开发工程师", "easy", "judge",
  "判断：Vue的v-if和v-show都可以控制元素显示隐藏，v-if通过display:none实现。",
  [{"key":"对","value":"正确"},{"key":"错","value":"错误"}],
  "错", "v-if是条件渲染（DOM增删），v-show通过display:none切换。v-if有更高的切换开销，v-show有更高的初始渲染开销。")

q("Vue.js", "专业", "前端开发工程师", "medium", "single_choice",
  "Vue3中，以下哪个API用于替代Vue2的Vue.observable()？",
  [{"key":"A","value":"computed()"},{"key":"B","value":"reactive()"},{"key":"C","value":"watch()"},{"key":"D","value":"inject()"}],
  "B", "reactive()返回对象的响应式代理，是Vue2中Vue.observable()的替代。")

q("Vue.js", "专业", "前端开发工程师", "medium", "single_choice",
  "Vue中组件通信最常见的方式是？",
  [{"key":"A","value":"props/emit"},{"key":"B","value":"全局变量"},{"key":"C","value":"localStorage"},{"key":"D","value":"CSS变量"}],
  "A", "父子组件通信使用props（父传子）和emit（子传父）。兄弟组件通信用事件总线或Vuex/Pinia。")

q("Vue.js", "专业", "前端开发工程师", "hard", "single_choice",
  "Vue3中ref和reactive的主要区别是？",
  [{"key":"A","value":"ref只支持数字，reactive支持对象"},{"key":"B","value":"ref在模板中自动解包，reactive不会"},{"key":"C","value":"ref需要.value访问，reactive不需要"},{"key":"D","value":"ref用于简单类型，reactive用于复杂类型"}],
  "C", "ref需要用.value访问/修改值（模板中自动解包），reactive直接访问属性。ref可以代理任何类型（包括基本类型），reactive只能代理对象。")

q("React", "专业", "前端开发工程师", "medium", "single_choice",
  "React中，useEffect的cleanup函数在什么时候执行？",
  [{"key":"A","value":"组件挂载时"},{"key":"B","value":"每次组件更新前"},{"key":"C","value":"组件卸载时，以及下次effect执行前"},{"key":"D","value":"只在组件卸载时"}],
  "C", "cleanup函数在组件卸载时执行，也会在依赖变化导致effect重新执行前执行，用于清理上次的副作用。")

q("React", "专业", "前端开发工程师", "medium", "single_choice",
  "React中key属性的作用是什么？",
  [{"key":"A","value":"唯一标识组件类型"},{"key":"B","value":"帮助React识别哪些元素改变了"},{"key":"C","value":"设置组件的CSS类名"},{"key":"D","value":"定义组件的默认属性"}],
  "B", "key帮助React优化Diff算法，准确判断哪些列表项被添加/删除/移动。使用数组索引作为key可能导致性能问题或渲染错误。")

q("CSS进阶", "专业", "前端开发工程师", "medium", "single_choice",
  "CSS中，position:sticky的定位基准是？",
  [{"key":"A","value":"视口(viewport)"},{"key":"B","value":"最近的定位祖先元素"},{"key":"C","value":"最近的滚动容器"},{"key":"D","value":"文档根元素"}],
  "C", "sticky定位相对于最近的滚动容器（overflow不为visible的祖先）。在滚动到阈值前相当于relative，超过阈值后相当于fixed。")

q("CSS进阶", "专业", "前端开发工程师", "medium", "single_choice",
  "以下哪种方法可以实现元素水平垂直居中？",
  [{"key":"A","value":"flex布局：justify-content:center; align-items:center"},{"key":"B","value":"text-align:center; vertical-align:middle"},{"key":"C","value":"float:center"},{"key":"D","value":"display:inline"}],
  "A", "Flexbox的justify-content:center（主轴居中）和align-items:center（交叉轴居中）是modern最常用的居中方案。")

q("CSS进阶", "专业", "前端开发工程师", "hard", "single_choice",
  "CSS中，以下哪些属性不会触发重排(reflow)？",
  [{"key":"A","value":"width"},{"key":"B","value":"transform"},{"key":"C","value":"margin"},{"key":"D","value":"padding"}],
  "B", "transform、opacity、filter等属性只触发合成(composite)，不会触发重排和重绘。修改width/margin/padding都会触发重排。")

q("性能优化", "专业", "前端开发工程师", "medium", "single_choice",
  "首屏加载性能优化中，以下哪个做法是错误的？",
  [{"key":"A","value":"图片懒加载"},{"key":"B","value":"把所有JS打包成一个大文件减少请求数"},{"key":"C","value":"路由懒加载"},{"key":"D","value":"使用CDN加速静态资源"}],
  "B", "把所有JS打成一个文件会增大首屏加载体积。现代做法是用代码分割(Code Splitting)按需加载。")

q("性能优化", "专业", "前端开发工程师", "hard", "single_choice",
  "Lighthouse中的CLS(Cumulative Layout Shift)指标衡量的是什么？",
  [{"key":"A","value":"页面加载速度"},{"key":"B","value":"页面布局的视觉稳定性"},{"key":"C","value":"JavaScript执行时间"},{"key":"D","value":"图片加载成功率"}],
  "B", "CLS衡量页面加载过程中布局偏移的总量。常见原因：没有设置图片尺寸、动态插入内容、字体加载导致布局变化。")

q("工程化", "专业", "前端开发工程师", "medium", "single_choice",
  "Webpack中，loader和plugin的区别是什么？",
  [{"key":"A","value":"loader处理模块转换，plugin处理构建流程"},{"key":"B","value":"loader处理JS，plugin处理CSS"},{"key":"C","value":"没有区别，只是名称不同"},{"key":"D","value":"loader在打包前执行，plugin在打包后执行"}],
  "A", "Loader用于转换模块源码（如babel-loader转译ES6），Plugin用于扩展Webpack功能（如HtmlWebpackPlugin生成HTML）。")

q("工程化", "专业", "前端开发工程师", "hard", "single_choice",
  "Vite为什么比Webpack快？",
  [{"key":"A","value":"Vite使用ES Modules原生支持，开发时不用打包"},{"key":"B","value":"Vite用Go语言编写"},{"key":"C","value":"Vite只支持Vue框架"},{"key":"D","value":"Vite运行在Node.js 20以上版本"}],
  "A", "Vite利用浏览器原生ES Module支持，开发模式按需编译，不事先打包。Webpack需要先构建整个依赖图再服务。")

q("网络安全", "专业", "前端开发工程师", "medium", "single_choice",
  "防御XSS攻击最有效的措施是？",
  [{"key":"A","value":"使用HTTPS"},{"key":"B","value":"对用户输入进行转义和过滤"},{"key":"C","value":"使用CDN"},{"key":"D","value":"添加验证码"}],
  "B", "XSS（跨站脚本攻击）的核心防范是：对用户输入做HTML实体编码转义、设置CSP(Content-Security-Policy)头、避免使用innerHTML插入用户内容。")

q("网络请求", "专业", "前端开发工程师", "medium", "single_choice",
  "HTTP/2相比HTTP/1.1的主要改进是什么？",
  [{"key":"A","value":"改用UDP协议"},{"key":"B","value":"支持多路复用，一个连接并行传输多个请求"},{"key":"C","value":"强制使用HTTPS"},{"key":"D","value":"删除请求头"}],
  "B", "HTTP/2的核心改进：多路复用（一个TCP连接并行处理多个请求）、服务器推送、头部压缩（HPACK）、二进制分帧。")

q("浏览器原理", "专业", "前端开发工程师", "hard", "single_choice",
  "浏览器渲染流程中，重排(Reflow)和重绘(Repaint)的关系是？",
  [{"key":"A","value":"重排一定会导致重绘"},{"key":"B","value":"重绘一定会导致重排"},{"key":"C","value":"两者没有关联"},{"key":"D","value":"重排比重绘开销小"}],
  "A", "重排（计算元素位置和大小）后必然需要重绘（绘制像素）。重绘不一定需要重排（如只改颜色）。重排开销最大，应尽量避免。")

q("场景题", "专业", "前端开发工程师", "hard", "single_choice",
  "一个搜索输入框需要做防抖(debounce)，以下哪种实现是正确的？",
  [{"key":"A","value":"每次输入都立即发送请求"},{"key":"B","value":"用户停止输入500ms后才发送请求"},{"key":"C","value":"每500ms固定发送一次请求"},{"key":"D","value":"用户输入完成后最多发送3次请求"}],
  "B", "防抖在用户停止操作一段时间后才执行。节流(throttle)才是固定间隔执行。搜索框用防抖减少请求次数。")

q("场景题", "专业", "前端开发工程师", "hard", "single_choice",
  "前端实现文件分片上传的优势是什么？",
  [{"key":"A","value":"减小文件体积"},{"key":"B","value":"支持大文件上传、断点续传、显示上传进度"},{"key":"C","value":"提高文件安全性"},{"key":"D","value":"不需要后端配合"}],
  "B", "分片上传将大文件切割成小块，支持：①并发上传提高速度；②断点续传（失败后重传失败的分片）；③显示精确上传进度。")

q("场景题", "专业", "前端开发工程师", "hard", "judge",
  "判断：前端用WebSocket代替HTTP轮询可以显著减少服务器压力。",
  [{"key":"对","value":"正确"},{"key":"错","value":"错误"}],
  "对", "WebSocket建立一次连接后保持长连接，服务端可以主动推送数据。相比HTTP轮询（客户端不断发请求查询），减少了大量无效请求的建立和响应开销。")

q("TypeScript", "专业", "前端开发工程师", "medium", "single_choice",
  "TypeScript中，interface和type的区别是什么？",
  [{"key":"A","value":"interface可以extends，type不能"},{"key":"B","value":"type可以定义联合类型，interface不能"},{"key":"C","value":"interface是值，type是类型"},{"key":"D","value":"两者没有区别"}],
  "B", "type可以定义联合类型（type A = B | C）、交叉类型、元组等。interface主要用于对象形状定义，支持声明合并。")

# ═══════════════════════════════════════════
# 后端开发工程师（22题）
# ═══════════════════════════════════════════
q("数据库", "专业", "后端开发工程师", "medium", "single_choice",
  "MySQL中，以下哪种索引最适合范围查询？",
  [{"key":"A","value":"哈希索引"},{"key":"B","value":"B+树索引"},{"key":"C","value":"全文索引"},{"key":"D","value":"空间索引"}],
  "B", "B+树索引叶子节点有序排列且带双向链表，非常适合范围查询（BETWEEN、>、<）。哈希索引只支持等值查询。")

q("数据库", "专业", "后端开发工程师", "medium", "single_choice",
  "事务的ACID特性中，隔离性(Isolation)通常通过什么机制实现？",
  [{"key":"A","value":"索引"},{"key":"B","value":"锁和MVCC"},{"key":"C","value":"日志"},{"key":"D","value":"缓存"}],
  "B", "MySQL InnoDB通过行锁+MVCC（多版本并发控制）实现隔离性。MVCC通过undo log保存数据快照，实现非锁定读。")

q("数据库", "专业", "后端开发工程师", "hard", "single_choice",
  "什么情况下会发生死锁？如何解决？",
  [{"key":"A","value":"两个事务同时更新同一行"},{"key":"B","value":"两个事务互相等待对方持有的锁"},{"key":"C","value":"一个事务更新多行数据"},{"key":"D","value":"事务没有提交"}],
  "B", "死锁条件：互斥、持有并等待、不可剥夺、循环等待。解决：①按固定顺序访问资源；②设置锁超时（innodb_lock_wait_timeout）；③MySQL自动检测死锁并回滚代价较小的事务。")

q("缓存", "专业", "后端开发工程师", "medium", "single_choice",
  "Redis中，以下哪种数据结构可以实现排行榜功能？",
  [{"key":"A","value":"String"},{"key":"B","value":"List"},{"key":"C","value":"ZSet（有序集合）"},{"key":"D","value":"Hash"}],
  "C", "ZSet（有序集合）每个元素关联一个score，按score排序。用ZADD添加/更新分数，ZREVRANGE获取排名前N。")

q("缓存", "专业", "后端开发工程师", "hard", "single_choice",
  "缓存雪崩和缓存穿透的区别是什么？",
  [{"key":"A","value":"两者是同一个概念"},{"key":"B","value":"雪崩是大面积缓存同时失效，穿透是查询不存在的数据"},{"key":"C","value":"雪崩是数据库崩溃，穿透是缓存崩溃"},{"key":"D","value":"雪崩是写入失败，穿透是读取失败"}],
  "B", "缓存雪崩：大量key同时过期或Redis宕机，请求全部打到DB。解决：过期时间加随机值、限流降级、多级缓存。缓存穿透：查询不存在的数据，缓存和DB都查不到。解决：布隆过滤器、缓存空值。")

q("缓存", "专业", "后端开发工程师", "medium", "judge",
  "判断：Redis的所有操作都是原子性的。",
  [{"key":"对","value":"正确"},{"key":"错","value":"错误"}],
  "对", "Redis是单线程执行命令，所有单个命令都是原子操作。但多个命令组合（如GET+SET）需要Lua脚本或事务保证原子性。")

q("API设计", "专业", "后端开发工程师", "medium", "single_choice",
  "RESTful API中，PUT和PATCH的区别是什么？",
  [{"key":"A","value":"没有区别"},{"key":"B","value":"PUT是全量更新，PATCH是部分更新"},{"key":"C","value":"PUT是安全的，PATCH不是"},{"key":"D","value":"PUT用于创建，PATCH用于删除"}],
  "B", "PUT替换整个资源（全量更新），PATCH只修改指定字段（部分更新）。PATCH请求体只包含要修改的字段。")

q("API设计", "专业", "后端开发工程师", "hard", "single_choice",
  "API限流(rate limiting)常用的算法中，哪个能处理突发流量？",
  [{"key":"A","value":"固定窗口计数器"},{"key":"B","value":"滑动窗口日志"},{"key":"C","value":"令牌桶"},{"key":"D","value":"漏桶"}],
  "C", "令牌桶允许一定程度突发：令牌积累后可以快速消费。漏桶强制平滑速率，不允许突发。固定窗口有临界突变问题。")

q("消息队列", "专业", "后端开发工程师", "medium", "single_choice",
  "消息队列中，如何保证消息不丢失？",
  [{"key":"A","value":"生产者发送后不用管"},{"key":"B","value":"生产者确认+消费者手动ACK+消息持久化+"},{"key":"C","value":"消费者收到后立即返回"},{"key":"D","value":"使用HTTP协议代替MQ"}],
  "B", "保证不丢失需要三端配合：①生产者确认机制；②Broker消息持久化到磁盘；③消费者手动ACK（处理完再确认）。")

q("消息队列", "专业", "后端开发工程师", "hard", "single_choice",
  "Kafka中，同一个消费者组内的多个消费者如何消费分区？",
  [{"key":"A","value":"所有消费者都消费所有分区"},{"key":"B","value":"每个分区只能被组内一个消费者消费"},{"key":"C","value":"消费者抢到哪个分区就消费哪个"},{"key":"D","value":"按消费者名称哈希分配"}],
  "B", "Kafka一个分区只能被同一个消费者组内的一个消费者消费，保证消息有序。消费者数不应超过分区数，超出的消费者闲置。")

q("分布式", "专业", "后端开发工程师", "hard", "single_choice",
  "分布式系统中的CAP理论是什么？",
  [{"key":"A","value":"一致性、可用性、分区容错性三者最多同时满足两个"},{"key":"B","value":"一致性、可用性、性能三者必须同时满足"},{"key":"C","value":"一致性、原子性、持久性必须全部满足"},{"key":"D","value":"容量、可用性、性能是核心指标"}],
  "A", "CAP定理：C（Consistency一致性）、A（Availability可用性）、P（Partition Tolerance分区容错性）。网络分区时必须选择CP或AP。")

q("认证授权", "专业", "后端开发工程师", "medium", "single_choice",
  "JWT的payload部分可以包含敏感信息吗？",
  [{"key":"A","value":"可以，JWT自带加密"},{"key":"B","value":"不可以，JWT只签名不加密"},{"key":"C","value":"取决于签名算法"},{"key":"D","value":"只有refresh token可以"}],
  "B", "JWT是签名的（防篡改）但不加密，payload是Base64编码，任何拿到token的人都可以解码读取。敏感信息不应放在payload。")

q("认证授权", "专业", "后端开发工程师", "hard", "single_choice",
  "OAuth 2.0中，Authorization Code模式相比Implicit模式的优势是？",
  [{"key":"A","value":"不需要客户端密钥"},{"key":"B","value":"access token不经过前端浏览器，更安全"},{"key":"C","value":"速度更快"},{"key":"D","value":"不需要用户登录"}],
  "B", "Authorization Code模式通过后端服务器交换token，access token不暴露给前端。Implicit模式直接返回token给前端，有安全风险。")

q("系统设计", "专业", "后端开发工程师", "medium", "single_choice",
  "设计短链接系统时，如何生成唯一的短码？",
  [{"key":"A","value":"使用UUID作为短码"},{"key":"B","value":"使用自增ID+Base62编码"},{"key":"C","value":"使用MD5哈希的前8位"},{"key":"D","value":"使用随机字符串"}],
  "B", "自增ID+Base62编码（0-9a-zA-Z共62个字符）可以生成短且唯一的短码，6000万条数据只需6位字符。UUID太长不适合短链接。")

q("系统设计", "专业", "后端开发工程师", "hard", "single_choice",
  "高并发下，如何保证扣库存不超卖？",
  [{"key":"A","value":"应用程序加synchronized"},{"key":"B","value":"数据库更新时带条件判断 stock > 0"},{"key":"C","value":"使用乐观锁+版本号"},{"key":"D","value":"先查询再判断"}],
  "C", "乐观锁方案：UPDATE goods SET stock=stock-1, version=version+1 WHERE id=? AND version=? AND stock>0。在SQL层面原子操作保证扣减安全。")

q("性能优化", "专业", "后端开发工程师", "medium", "single_choice",
  "SQL查询慢的常见原因有哪些？",
  [{"key":"A","value":"服务器磁盘空间不足"},{"key":"B","value":"没有走索引、数据量大、锁等待、字段类型转换"},{"key":"C","value":"网络带宽不够"},{"key":"D","value":"CPU温度过高"}],
  "B", "慢查询常见原因：①索引缺失或不合理；②数据量过大未分页；③锁等待；④隐式类型转换导致索引失效；⑤SELECT * 取多余字段。")

q("性能优化", "专业", "后端开发工程师", "hard", "single_choice",
  "MySQL慢查询日志中，以下哪项可以帮助分析问题？",
  [{"key":"A","value":"查询的数据库名"},{"key":"B","value":"查询执行时间、扫描行数、返回行数"},{"key":"C","value":"服务器的IP地址"},{"key":"D","value":"操作系统版本"}],
  "B", "慢查询日志记录：执行时间、锁等待时间、扫描行数、返回行数、SQL语句。通过比较扫描行数和返回行数判断是否需要加索引。")

q("Docker/K8s", "专业", "后端开发工程师", "medium", "single_choice",
  "Docker中，CMD和ENTRYPOINT的区别是？",
  [{"key":"A","value":"两者完全相同"},{"key":"B","value":"CMD定义容器启动命令，ENTRYPOINT定义默认参数"},{"key":"C","value":"CMD可以被docker run参数覆盖，ENTRYPOINT不会"},{"key":"D","value":"ENTRYPOINT是Linux命令，CMD是Docker命令"}],
  "C", "CMD提供默认命令和参数，docker run时可以覆盖。ENTRYPOINT配置容器启动程序，docker run时追加的参数会作为ENTRYPOINT的参数。")

q("场景题", "专业", "后端开发工程师", "medium", "single_choice",
  "用户密码存储的正确做法是？",
  [{"key":"A","value":"明文存储"},{"key":"B","value":"MD5加密存储"},{"key":"C","value":"bcrypt加盐哈希存储"},{"key":"D","value":"Base64编码存储"}],
  "C", "bcrypt是自适应哈希算法，自动生成随机盐，抗暴力破解。MD5和SHA系列很容易被彩虹表破解。Base64是编码不是加密。")

q("场景题", "专业", "后端开发工程师", "hard", "judge",
  "判断：微服务架构中，服务间通信应该优先选择同步HTTP调用。",
  [{"key":"对","value":"正确"},{"key":"错","value":"错误"}],
  "错", "微服务间应优先使用异步消息通信（如Kafka/RabbitMQ）解耦服务。同步HTTP调用会造成链式故障、增加延迟。")

q("场景题", "专业", "后端开发工程师", "hard", "single_choice",
  "服务降级和服务熔断的区别是什么？",
  [{"key":"A","value":"降级是主动关闭非核心功能，熔断是被动切断故障链路"},{"key":"B","value":"两者概念相同"},{"key":"C","value":"熔断是降级的一种方式"},{"key":"D","value":"降级是客户端行为，熔断是服务端行为"}],
  "A", "服务降级（主动）：系统压力大时关闭非核心功能保核心。服务熔断（被动）：下游故障率超过阈值时自动切断请求，防止级联故障。")

# ═══════════════════════════════════════════
# 产品经理（20题）
# ═══════════════════════════════════════════
q("需求分析", "专业", "产品经理", "easy", "single_choice",
  "以下哪个不是收集用户需求的常用方法？",
  [{"key":"A","value":"用户访谈"},{"key":"B","value":"问卷调查"},{"key":"C","value":"直接替用户做决定"},{"key":"D","value":"数据分析"}],
  "C", "产品经理应该通过用户访谈、问卷、数据分析、竞品分析等方式发现真实需求，而不是凭主观臆断替用户做决定。")

q("需求分析", "专业", "产品经理", "medium", "single_choice",
  "Kano模型中，基本型需求(Basic Needs)的特点是？",
  [{"key":"A","value":"做得好用户会满意，做不好用户会很不满意"},{"key":"B","value":"做得好用户满意，做不好用户无所谓"},{"key":"C","value":"用户不会明确说出来，但缺失时会强烈不满"},{"key":"D","value":"价值最高，应优先投入资源"}],
  "C", "基本型需求是用户默认必须有、不说出来但缺失会强烈不满的功能（如App登录功能）。期望型需求是用户明确说出来的。兴奋型需求是超出预期的。")

q("需求分析", "专业", "产品经理", "hard", "single_choice",
  "你的功能上线后数据没有提升，第一步应该做什么？",
  [{"key":"A","value":"立即回滚功能"},{"key":"B","value":"检查数据埋点是否正确，确认数据可信"},{"key":"C","value":"指责开发没做好"},{"key":"D","value":"放弃这个方向"}],
  "B", "数据未提升的排查步骤：①确认埋点正确性；②样本量是否满足统计要求；③拆解细分维度看是否有局部提升；④做用户回访验证认知。")

q("产品设计", "专业", "产品经理", "medium", "single_choice",
  "MVP(最小可行产品)的核心原则是什么？",
  [{"key":"A","value":"做出功能最完整的版本"},{"key":"B","value":"用最小成本验证核心假设"},{"key":"C","value":"界面要美观精致"},{"key":"D","value":"同时支持所有平台"}],
  "B", "MVP的核心是以最小的开发和资源投入，尽快验证产品假设是否成立。关键是'验证'而不是'最小'。")

q("产品设计", "专业", "产品经理", "medium", "single_choice",
  "信息架构中，卡片分类法(Card Sorting)的作用是？",
  [{"key":"A","value":"测试产品功能是否好用"},{"key":"B","value":"了解用户对信息分类的心理模型"},{"key":"C","value":"评估产品性能"},{"key":"D","value":"确定产品定价"}],
  "B", "卡片分类法通过让用户对卡片（代表信息/功能）进行分类，了解用户对信息组织方式的自然认知，指导导航和信息架构设计。")

q("数据分析", "专业", "产品经理", "medium", "single_choice",
  "评估A/B测试结果时，p-value<0.05意味着什么？",
  [{"key":"A","value":"实验组比对照组好5%"},{"key":"B","value":"有95%的信心认为两组差异不是随机造成的"},{"key":"C","value":"实验无效"},{"key":"D","value":"样本量不够"}],
  "B", "p<0.05表示在零假设（两组无差异）为真的情况下，观察到当前结果的概率小于5%。通常认为差异具有统计显著性。")

q("数据分析", "专业", "产品经理", "hard", "single_choice",
  "日活跃用户(DAU)下降5%，应该从哪些维度拆解分析？",
  [{"key":"A","value":"只看整体数据"},{"key":"B","value":"渠道来源、用户分层、地区、版本"},{"key":"C","value":"只看新用户"},{"key":"D","value":"等一周再分析"}],
  "B", "DAU下降要拆解：①哪个渠道新增减少；②新用户还是老用户流失；③哪个地区下降最多；④哪个版本/平台有问题。定位问题后才能对症下药。")

q("项目管理", "专业", "产品经理", "medium", "single_choice",
  "需求变更频繁时，产品经理应该怎么做？",
  [{"key":"A","value":"全部拒绝"},{"key":"B","value":"全部接受"},{"key":"C","value":"建立变更评审流程，评估影响后决定"},{"key":"D","value":"让开发自己决定"}],
  "C", "需求变更应有规范流程：①提出变更申请；②评估对范围/时间/成本的影响；③干系人确认；④更新PRD和排期。小变更周会统一处理，大变更重新排期。")

q("竞品分析", "专业", "产品经理", "medium", "single_choice",
  "做竞品分析时，以下哪个维度不是必须关注的？",
  [{"key":"A","value":"功能对比"},{"key":"B","value":"用户评价"},{"key":"C","value":"竞品公司食堂好不好吃"},{"key":"D","value":"产品定位"}],
  "C", "竞品分析应关注：产品定位、目标用户、核心功能、交互体验、商业模式、市场份额、用户评价、技术方案等。与产品无关的信息不需要关注。")

q("PRD写作", "专业", "产品经理", "medium", "single_choice",
  "好的PRD中，功能描述应该包含哪些要素？",
  [{"key":"A","value":"只说功能名称即可"},{"key":"B","value":"正常流程、异常流程、边界条件"},{"key":"C","value":"只写用户故事"},{"key":"D","value":"只画原型图"}],
  "B", "功能描述应包含：①正常操作流程；②异常情况处理（网络中断、数据为空、权限不足等）；③边界条件（输入上限、时间限制等）。")

q("用户增长", "专业", "产品经理", "hard", "single_choice",
  "产品冷启动阶段，最有效的获取第一批用户的方式是？",
  [{"key":"A","value":"大规模投放广告"},{"key":"B","value":"手动邀请+种子用户运营"},{"key":"C","value":"等待用户自然发现"},{"key":"D","value":"立即做裂变活动"}],
  "B", "冷启动阶段资源有限，最有效的方式是：精准找到目标用户群体，一对一邀请或小范围运营，收集反馈迭代产品。大规模投放可能浪费预算。")

q("用户研究", "专业", "产品经理", "medium", "judge",
  "判断：用户说出来的需求，就是他们真正需要的。",
  [{"key":"对","value":"正确"},{"key":"错","value":"错误"}],
  "错", "用户说的需求和真实需求往往有偏差。用户可能：①不知道有什么更好的方案；②表达的方案只是他们能想到的解决方案；③说的和做的不同。产品经理需要挖掘背后的真实动机。")

# Add remaining questions for other careers below...
# For brevity, generating top 6 most common career paths
# 数据分析师（18题）

q("SQL", "专业", "数据分析师", "medium", "single_choice",
  "SQL中，INNER JOIN和LEFT JOIN的区别是？",
  [{"key":"A","value":"INNER JOIN只返回匹配的行，LEFT JOIN返回左表所有行"},{"key":"B","value":"INNER JOIN比LEFT JOIN慢"},{"key":"C","value":"LEFT JOIN只返回匹配的行"},{"key":"D","value":"两者结果相同"}],
  "A", "INNER JOIN返回两表匹配的记录。LEFT JOIN返回左表全部记录+右表匹配的记录（不匹配的字段为NULL）。")

q("SQL", "专业", "数据分析师", "medium", "single_choice",
  "以下SQL窗口函数中，哪个可以获取每个分组内的前N条记录？",
  [{"key":"A","value":"SUM() OVER"},{"key":"B","value":"ROW_NUMBER() OVER"},{"key":"C","value":"AVG() OVER"},{"key":"D","value":"COUNT() OVER"}],
  "B", "ROW_NUMBER()配合PARTITION BY分组和ORDER BY排序，再用WHERE过滤序号<=N即可获取每组前N条。")

q("SQL", "专业", "数据分析师", "hard", "single_choice",
  "SQL执行计划中，type列为ALL表示什么？",
  [{"key":"A","value":"走了索引"},{"key":"B","value":"全表扫描，需要优化"},{"key":"C","value":"使用了临时表"},{"key":"D","value":"使用了文件排序"}],
  "B", "EXPLAIN的type列：const/ref/range表示走了索引，ALL表示全表扫描，通常需要加索引优化。")

q("统计学", "专业", "数据分析师", "medium", "single_choice",
  "标准差和标准误的区别是？",
  [{"key":"A","value":"标准差描述数据离散程度，标准误描述样本统计量精度"},{"key":"B","value":"两者相同"},{"key":"C","value":"标准差是标准误的平方"},{"key":"D","value":"标准误衡量总体均值"}],
  "A", "标准差(σ)衡量个体数据的波动大小。标准误(SE=σ/√n)衡量样本均值的抽样误差，样本量越大标准误越小。")

q("统计学", "专业", "数据分析师", "hard", "single_choice",
  "正偏态(右偏)分布中，均值、中位数、众数的关系是？",
  [{"key":"A","value":"众数 < 中位数 < 均值"},{"key":"B","value":"均值 < 中位数 < 众数"},{"key":"C","value":"三者相等"},{"key":"D","value":"中位数 < 众数 < 均值"}],
  "A", "正偏态（右偏）分布右侧有长尾，均值被极端值拉向右，所以众数<中位数<均值。负偏态则相反。")

q("统计学", "专业", "数据分析师", "medium", "judge",
  "判断：相关系数r=0表示两个变量之间没有任何关系。",
  [{"key":"对","value":"正确"},{"key":"错","value":"错误"}],
  "错", "r=0只表示没有线性相关，但可能存在非线性关系（如抛物线关系）。需要画散点图辅助判断。")

q("业务分析", "专业", "数据分析师", "medium", "single_choice",
  "同期群分析(Cohort Analysis)最适合用来分析什么？",
  [{"key":"A","value":"用户当前活跃度"},{"key":"B","value":"不同批次用户的留存变化趋势"},{"key":"C","value":"功能使用次数"},{"key":"D","value":"服务器响应时间"}],
  "B", "同期群分析按用户首次行为时间（如注册月）分组，跟踪每组后续的留存/付费等指标，发现留存变化趋势。")

q("业务分析", "专业", "数据分析师", "hard", "single_choice",
  "某功能上线后整体转化率没有变化，但细分后发现iOS提升10%而Android下降10%，这是什么现象？",
  [{"key":"A","value":"辛普森悖论"},{"key":"B","value":"幸存者偏差"},{"key":"C","value":"选择偏差"},{"key":"D","value":"确认偏误"}],
  "A", "辛普森悖论：整体趋势与分组趋势相反。原因是两组样本量差异大，加权平均后整体表现被占权重大的组主导。")

q("数据可视化", "专业", "数据分析师", "medium", "single_choice",
  "展示不同类别在整体中的占比，最适合用哪种图表？",
  [{"key":"A","value":"折线图"},{"key":"B","value":"扇形图或环形图"},{"key":"C","value":"散点图"},{"key":"D","value":"箱线图"}],
  "B", "扇形图（饼图）和环形图适合展示占比关系。折线图展示趋势，散点图展示相关关系，箱线图展示数据分布。")

q("数据可视化", "专业", "数据分析师", "medium", "single_choice",
  "箱线图(Box Plot)中可以直观看到哪些统计量？",
  [{"key":"A","value":"均值、方差、标准差"},{"key":"B","value":"最小值、Q1、中位数、Q3、最大值、异常值"},{"key":"C","value":"众数、分位数"},{"key":"D","value":"偏度、峰度"}],
  "B", "箱线图展示五数概括：最小值、第一四分位数(Q1)、中位数、第三四分位数(Q3)、最大值。箱体外的点通常视为异常值。")

q("实验设计", "专业", "数据分析师", "hard", "single_choice",
  "AB测试中，什么是'新奇效应'(Novelty Effect)？",
  [{"key":"A","value":"用户对新功能感到新奇而短暂提升指标"},{"key":"B","value":"测试用户作弊"},{"key":"C","value":"新功能导致用户不适"},{"key":"D","value":"技术架构问题"}],
  "A", "新奇效应指用户因新鲜感短期内对实验组表现更好的现象。解决方法：跑足够长时间（至少一个完整业务周期），观察趋势是否稳定。")

q("工具", "专业", "数据分析师", "medium", "single_choice",
  "Python的pandas中，groupby操作后恢复为普通DataFrame的方法是？",
  [{"key":"A","value":"reset_index()"},{"key":"B","value":"unstack()"},{"key":"C","value":"melt()"},{"key":"D","value":"pivot()"}],
  "A", "groupby().agg()返回的是GroupBy对象，reset_index()将分组键恢复为普通列。")

# ═══════════════════════════════════════════
# 算法工程师（20题）
# ═══════════════════════════════════════════
q("机器学习基础", "专业", "算法工程师", "medium", "single_choice",
  "决策树剪枝的目的是什么？",
  [{"key":"A","value":"加快训练速度"},{"key":"B","value":"防止过拟合，提高泛化能力"},{"key":"C","value":"减少特征数量"},{"key":"D","value":"增加树的深度"}],
  "B", "决策树容易过拟合（完全生长会记住噪声）。剪枝通过限制树深度/叶子节点最小样本数等，提高泛化能力。")

q("机器学习基础", "专业", "算法工程师", "medium", "single_choice",
  "L1正则化和L2正则化的区别是？",
  [{"key":"A","value":"L1使部分系数变为0（特征选择），L2使系数趋向于0但不为0"},{"key":"B","value":"L2使系数变为0"},{"key":"C","value":"L1和L2没有区别"},{"key":"D","value":"L1用于分类，L2用于回归"}],
  "A", "L1（Lasso）加绝对值惩罚，产生稀疏解（部分权重为0），自带特征选择。L2（Ridge）加平方惩罚，权重整体缩小但不为0。")

q("机器学习基础", "专业", "算法工程师", "hard", "single_choice",
  "随机森林中，每个决策树的训练数据是如何获取的？",
  [{"key":"A","value":"全部原始数据"},{"key":"B","value":"有放回抽样(Bootstrap)，样本量与原数据相同"},{"key":"C","value":"不放回抽样的一半数据"},{"key":"D","value":"随机选取50%的数据"}],
  "B", "随机森林每个树用Bootstrap抽样（有放回）从原始数据中抽取N个样本，约63.2%的原始样本会被抽到，其余为OOB样本。")

q("机器学习基础", "专业", "算法工程师", "medium", "single_choice",
  "以下哪个指标不适合评估不平衡分类问题？",
  [{"key":"A","value":"F1-Score"},{"key":"B","value":"AUC-ROC"},{"key":"C","value":"准确率(Accuracy)"},{"key":"D","value":"Precision-Recall曲线"}],
  "C", "不平衡数据（如99:1）中，全部预测为多数类也能有99%准确率，这个指标完全失去意义。AUC和F1对不平衡更鲁棒。")

q("深度学习", "专业", "算法工程师", "medium", "single_choice",
  "Batch Normalization的主要作用是？",
  [{"key":"A","value":"加速模型推理"},{"key":"B","value":"缓解梯度消失/爆炸，加速收敛"},{"key":"C","value":"减少模型参数量"},{"key":"D","value":"增加模型深度"}],
  "B", "BN对每个batch进行归一化，使各层输入分布稳定，允许用更大的学习率，加速训练收敛，同时有轻微正则化效果。")

q("深度学习", "专业", "算法工程师", "hard", "single_choice",
  "Transformer中，自注意力(Self-Attention)的计算复杂度是？",
  [{"key":"A","value":"O(n)"},{"key":"B","value":"O(n²)"},{"key":"C","value":"O(n log n)"},{"key":"D","value":"O(n³)"}],
  "B", "Self-Attention需要计算n个token两两之间的注意力得分，复杂度O(n²·d)。n为序列长度，d为隐层维度。这限制了长文本处理。")

q("深度学习", "专业", "算法工程师", "hard", "single_choice",
  "梯度消失问题的常见解决方案不包括以下哪项？",
  [{"key":"A","value":"使用ReLU激活函数"},{"key":"B","value":"使用残差连接"},{"key":"C","value":"增大学习率"},{"key":"D","value":"使用LSTM/GRU代替RNN"}],
  "C", "增大学习率反而可能导致梯度爆炸。解决梯度消失：ReLU（正区间梯度为1）、残差连接（恒等映射保持梯度）、LSTM门控机制。")

q("NLP/CV", "专业", "算法工程师", "medium", "single_choice",
  "文本分类任务中，TF-IDF的缺点是什么？",
  [{"key":"A","value":"计算速度慢"},{"key":"B","value":"无法捕捉词语顺序和语义信息"},{"key":"C","value":"占用内存大"},{"key":"D","value":"不支持中文"}],
  "B", "TF-IDF是基于词频统计的Bag-of-Words方法，忽略词语顺序和上下文语义。Word2Vec/ELMo/BERT等词向量可以捕捉更丰富的语义。")

q("模型评估", "专业", "算法工程师", "medium", "single_choice",
  "K折交叉验证中，K值越大通常会导致？",
  [{"key":"A","value":"偏差减小、方差增大"},{"key":"B","value":"偏差增大、方差减小"},{"key":"C","value":"偏差和方差都增大"},{"key":"D","value":"偏差和方差都减小"}],
  "A", "K越大，训练集越大，模型偏差越小。但训练集之间的相似度增加，导致不同折的模型差异增大（方差增大）。常用K=5或10。")

q("场景题", "专业", "算法工程师", "hard", "single_choice",
  "推荐系统中，协同过滤(Collaborative Filtering)的冷启动问题怎么解决？",
  [{"key":"A","value":"随机推荐"},{"key":"B","value":"基于内容的推荐(Content-Based)或热门推荐"},{"key":"C","value":"不做任何处理"},{"key":"D","value":"增加模型层数"}],
  "B", "新用户/新物品没有行为数据时，协同过滤失效。解决方案：①基于内容推荐（利用用户画像/物品属性）；②热门推荐兜底；③混合推荐策略。")

q("场景题", "专业", "算法工程师", "medium", "judge",
  "判断：模型在训练集上表现很好但在测试集上表现差，一定是过拟合。",
  [{"key":"对","value":"正确"},{"key":"错","value":"错误"}],
  "错", "也可能是数据泄露、训练集和测试集分布不一致、或者评测指标使用不当等原因。过拟合是常见原因但不是唯一原因。")

# ═══════════════════════════════════════════
# 通用/综合题（15题）
# ═══════════════════════════════════════════
q("逻辑思维", "综合", "通用", "medium", "single_choice",
  "如果你的上级布置了一个你无法完成的任务，你会怎么做？",
  [{"key":"A","value":"硬着头皮做，做不完再说"},{"key":"B","value":"直接说不做"},{"key":"C","value":"先评估难点，带着方案找上级沟通资源和时间调整"},{"key":"D","value":"找同事帮忙不告诉上级"}],
  "C", "正确的做法是先理解任务目标，评估困难和资源缺口，准备替代方案或时间/资源调整建议，主动与上级沟通。")

q("逻辑思维", "综合", "通用", "medium", "single_choice",
  "团队中遇到意见分歧时，你通常怎么处理？",
  [{"key":"A","value":"坚持自己观点"},{"key":"B","value":"听资历深的人"},{"key":"C","value":"摆数据、讲依据，用实验或小规模验证说服对方"},{"key":"D","value":"投票决定"}],
  "C", "意见分歧时，用数据和事实说话最有效。小范围验证（如AB测试）可以客观评判方案优劣，避免主观争论。")

q("逻辑思维", "综合", "通用", "hard", "single_choice",
  "估算北京有多少个加油站，你会怎么思考？",
  [{"key":"A","value":"上网查数据"},{"key":"B","value":"用费米估算：从车辆数、加油频次、加油站服务能力计算"},{"key":"C","value":"随便猜一个数"},{"key":"D","value":"问出租车司机"}],
  "B", "费米估算用已知量推导未知量。例如：北京约600万人，假设平均每3人有1辆车（200万辆车），每辆车每周加油一次，每个加油站每天服务约300辆车... 层层推导。")

print(f"Generated {len(NEW_QUESTIONS)} new questions total")


# ═══════════════════════════════════════════
# Replace the questions in database
# ═══════════════════════════════════════════
def replace_questions():
    db = SessionLocal()
    try:
        # Delete existing seed questions (those inserted by init, not user-created ones)
        # We'll just replace all questions
        deleted = db.query(ExamQuestion).delete()
        print(f"Deleted {deleted} existing questions")

        # Insert new questions
        for q_data in NEW_QUESTIONS:
            q = ExamQuestion(
                knowledge_point=q_data["knowledge_point"],
                category=q_data["category"],
                career=q_data["career"],
                difficulty=q_data["difficulty"],
                question_type=q_data["question_type"],
                question=q_data["question"],
                options_json=json.dumps(q_data["options"], ensure_ascii=False),
                answer=q_data["answer"],
                analysis=q_data["analysis"],
            )
            db.add(q)

        db.commit()
        count = db.query(ExamQuestion).count()
        print(f"✅ 题库更新完成！现共有 {count} 道题")
    except Exception as e:
        db.rollback()
        print(f"❌ 错误: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    replace_questions()