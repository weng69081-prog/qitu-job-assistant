const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.defineLayout({ name: "CUSTOM_16_9", width: 13.33, height: 7.5 });
pres.layout = "CUSTOM_16_9";
pres.author = "曾怡嫚 · AI+X Elite 20";
pres.title = "AI+X 学习之旅";
pres.subject = "面向工资编程队";

// ══════════════════════════════════
// 配色 — 简约创意模板风格
// ══════════════════════════════════
const C = {
  teal: "00C2B9",       // 主色 — 青绿
  tealDark: "154A4B",   // 深青
  tealMuted: "538B88",  // 灰青
  blue: "00B0F0",       // 湖蓝辅助
  green: "92D050",      // 淡绿辅助
  text: "091E21",       // 深色文字
  textDark: "01091E",   // 极深
  cream: "EEECE1",      // 米白底
  gray: "D9D9D9",       // 浅灰
  white: "FFFFFF",
  black: "333333",
};

const FONT = "Arial";

// ─── 辅助函数 ──────────────────────

/** 左侧装饰竖条（配合标题） */
function addTitleBar(slide, y, h = 0.6) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y, w: 0.06, h,
    fill: { color: C.teal },
  });
}

/** 页面标题（带左侧竖条） */
function addPageTitle(slide, title, subtitle = "") {
  addTitleBar(slide, 0.45, 0.65);
  slide.addText(title, {
    x: 0.75, y: 0.35, w: 10, h: 0.85,
    fontSize: 28, fontFace: FONT, color: C.text, bold: true,
    margin: 0, valign: "middle",
  });
  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.75, y: 1.05, w: 10, h: 0.4,
      fontSize: 12, fontFace: FONT, color: C.tealMuted,
      margin: 0,
    });
  }
}

/** 装饰小圆点 */
function addDot(slide, x, y, r = 0.15, color = C.teal) {
  slide.addShape(pres.shapes.OVAL, {
    x: x - r, y: y - r, w: r * 2, h: r * 2,
    fill: { color },
  });
}

/** 圆角卡片 */
function addCard(slide, x, y, w, h, color = C.white) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h,
    fill: { color },
    rectRadius: 0.08,
  });
}

/** 底栏装饰线 */
function addFooterLine(slide) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 6.9, w: 12.3, h: 0.008,
    fill: { color: C.gray },
  });
  slide.addText("AI+X Elite 20 · 面向工资编程队", {
    x: 0.5, y: 6.95, w: 12.3, h: 0.35,
    fontSize: 9, fontFace: FONT, color: C.gray,
    align: "right", margin: 0,
  });
}

// ════════════════════════════════════
//  第 1 页 · 封面
// ════════════════════════════════════

const s1 = pres.addSlide();
s1.background = { color: C.white };

// 左侧装饰 — 一条简洁的青绿色带
s1.addShape(pres.shapes.RECTANGLE, {
  x: 0.3, y: 0.3, w: 0.08, h: 6.9,
  fill: { color: C.teal },
});

// 顶部标题区
s1.addText("面向工资编程队", {
  x: 1.0, y: 0.5, w: 5.0, h: 0.5,
  fontSize: 13, fontFace: FONT, color: C.tealMuted,
  margin: 0,
});

// 主标题 — 大号
s1.addText("AI+X 学习之旅", {
  x: 1.0, y: 1.2, w: 7.0, h: 1.0,
  fontSize: 36, fontFace: FONT, color: C.text, bold: true,
  margin: 0,
});

s1.addText("从课堂到实战 · 从代码到能力", {
  x: 1.0, y: 2.2, w: 7.0, h: 0.5,
  fontSize: 14, fontFace: FONT, color: C.tealMuted,
  margin: 0,
});

// 分割线
s1.addShape(pres.shapes.RECTANGLE, {
  x: 1.0, y: 2.85, w: 3.5, h: 0.03,
  fill: { color: C.teal },
});

// 装饰性圆点
addDot(s1, 1.0, 2.85, 0.06, C.teal);
addDot(s1, 4.5, 2.85, 0.06, C.blue);

// 描述文字
s1.addText([
  { text: "AI + X 实验班 Elite 20", options: { fontSize: 12, color: C.text, bold: true } },
], {
  x: 1.0, y: 3.2, w: 7.0, h: 1.2,
  fontFace: FONT, lineSpacingMultiple: 1.6, margin: 0,
});

// 右侧装饰元素 — 大圆环
s1.addShape(pres.shapes.OVAL, {
  x: 8.5, y: 0.8, w: 4.5, h: 4.5,
  fill: { color: C.teal, transparency: 92 },
});
s1.addShape(pres.shapes.OVAL, {
  x: 9.5, y: 1.8, w: 2.5, h: 2.5,
  fill: { color: C.teal, transparency: 88 },
});

// 装饰小圆
s1.addShape(pres.shapes.OVAL, {
  x: 10.0, y: 4.8, w: 0.8, h: 0.8,
  fill: { color: C.teal, transparency: 85 },
});
s1.addShape(pres.shapes.OVAL, {
  x: 8.0, y: 5.5, w: 0.5, h: 0.5,
  fill: { color: C.blue, transparency: 80 },
});

// 底部署名
s1.addText("曾怡嫚 · AI+X Elite 20 · 面向工资编程队", {
  x: 1.0, y: 6.5, w: 8.0, h: 0.4,
  fontSize: 10, fontFace: FONT, color: C.gray,
  margin: 0,
});
addFooterLine(s1);


// ════════════════════════════════════
//  第 2 页 · AI+X 三层能力理念
// ════════════════════════════════════

const s2 = pres.addSlide();
s2.background = { color: C.white };
addPageTitle(s2, "AI+X 三层能力理念", "AI 不是工具，是思维方式的延伸");

// 三层卡片
const layers = [
  { title: "L1 · 建模能力 Modeling", subtitle: "🌍 理解世界", desc: "快速理解并结构化\n任何领域的能力\n从混沌中提取模式", color: C.teal },
  { title: "L2 · 协同能力 Collaboration", subtitle: "🔧 改变世界", desc: "借助 AI 工具\n将复杂问题\n转化为具体结果的能力", color: C.blue },
  { title: "L3 · 反馈能力 Feedback", subtitle: "🔄 进化自己", desc: "从结果中获取洞察\n驱动持续进化的能力\n经验+闭环反馈=知识", color: C.green },
];

layers.forEach((layer, idx) => {
  const cx = 0.6 + idx * 4.1;
  const cy = 2.2;

  // 卡片背景
  addCard(s2, cx, cy, 3.7, 4.0);
  
  // 顶部色条
  s2.addShape(pres.shapes.RECTANGLE, {
    x: cx, y: cy, w: 3.7, h: 0.06,
    fill: { color: layer.color },
  });

  // 层级编号
  s2.addText(`0${idx + 1}`, {
    x: cx + 0.3, y: cy + 0.25, w: 1.5, h: 0.7,
    fontSize: 36, fontFace: FONT, color: layer.color, bold: true,
    margin: 0,
  });

  // 标题
  s2.addText(layer.title, {
    x: cx + 0.3, y: cy + 0.85, w: 3.0, h: 0.45,
    fontSize: 15, fontFace: FONT, color: C.text, bold: true,
    margin: 0,
  });

  // 副标题（目标）
  s2.addText(layer.subtitle, {
    x: cx + 0.3, y: cy + 1.3, w: 3.0, h: 0.4,
    fontSize: 12, fontFace: FONT, color: layer.color,
    margin: 0,
  });

  // 描述
  s2.addText(layer.desc, {
    x: cx + 0.3, y: cy + 1.8, w: 3.1, h: 2.0,
    fontSize: 11, fontFace: FONT, color: C.tealMuted,
    lineSpacingMultiple: 1.6, margin: 0,
  });

  // 小装饰点
  addDot(s2, cx + 0.15, cy + 0.15, 0.05, layer.color);
});

// 底部总结
s2.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 0.6, y: 6.3, w: 12.1, h: 0.4,
  fill: { color: C.teal, transparency: 90 },
  rectRadius: 0.08,
});
s2.addText("🌟 核心观点：建模 → 协同 → 反馈，教育的下一站不在答案里，在闭环里", {
  x: 0.8, y: 6.3, w: 11.5, h: 0.4,
  fontSize: 10, fontFace: FONT, color: C.tealDark, italic: true,
  margin: 0, valign: "middle",
});
addFooterLine(s2);


// ════════════════════════════════════
//  第 3 页 · KSTAR 架构
// ════════════════════════════════════

const s3 = pres.addSlide();
s3.background = { color: C.white };
addPageTitle(s3, "KSTAR 架构", "情境 · 任务 · 行动 · 结果 — 学习发生在闭环反馈中");

// 五张卡片围绕中心排列，全部保持在页面上半区（不碰底部引用）
const kstarItems = [
  { label: "K", title: "Knowledge", desc: "先验知识与经验\n学习的基础存量", x: 1.8, y: 1.6 },
  { label: "S", title: "Situation", desc: "当前情境\n理解所处的环境与条件", x: 5.0, y: 1.2 },
  { label: "T", title: "Task", desc: "要完成的任务\n明确的行动目标", x: 9.4, y: 1.6 },
  { label: "A", title: "Action", desc: "行动（实际/预期）\nÂ = 预期动作\nA = 实际执行", x: 8.0, y: 4.4 },
  { label: "R", title: "Result", desc: "结果（实际/预期）\nR̂ = 预期结果\nR = 实际结果", x: 2.5, y: 4.4 },
];
const CARD_W = 2.6;
const CARD_H = 1.9;

kstarItems.forEach(item => {
  addCard(s3, item.x, item.y, CARD_W, CARD_H);
  // 左侧色条
  s3.addShape(pres.shapes.RECTANGLE, {
    x: item.x, y: item.y, w: 0.05, h: CARD_H,
    fill: { color: C.teal },
  });
  // 大字母
  s3.addText(item.label, {
    x: item.x + 0.2, y: item.y + 0.1, w: 0.7, h: 0.7,
    fontSize: 30, fontFace: FONT, color: C.teal, bold: true,
    margin: 0,
  });
  // 标题
  s3.addText(item.title, {
    x: item.x + 0.9, y: item.y + 0.2, w: 1.5, h: 0.35,
    fontSize: 12, fontFace: FONT, color: C.text, bold: true,
    margin: 0, valign: "middle",
  });
  // 描述
  s3.addText(item.desc, {
    x: item.x + 0.2, y: item.y + 0.8, w: 2.2, h: 0.9,
    fontSize: 10, fontFace: FONT, color: C.tealMuted,
    lineSpacingMultiple: 1.5, margin: 0,
  });
});

// 中心圆圈
s3.addShape(pres.shapes.OVAL, {
  x: 5.4, y: 3.2, w: 1.6, h: 1.6,
  fill: { color: C.teal, transparency: 85 },
});
s3.addShape(pres.shapes.OVAL, {
  x: 5.8, y: 3.6, w: 0.8, h: 0.8,
  fill: { color: C.teal },
});
s3.addText("✦", {
  x: 5.8, y: 3.6, w: 0.8, h: 0.8,
  fontSize: 24, color: C.white, fontFace: FONT, bold: true,
  align: "center", valign: "middle", margin: 0,
});

// 底部引用（与卡片底部不重叠）
s3.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 0.6, y: 6.3, w: 12.1, h: 0.4,
  fill: { color: C.teal, transparency: 90 },
  rectRadius: 0.08,
});
s3.addText("📖 核心公式：学习 = ΔR = 实际结果 − 预期结果  |  经验 − 反馈 = 噪音 · 经验 + 闭环反馈 = 知识", {
  x: 0.8, y: 6.3, w: 11.5, h: 0.4,
  fontSize: 10, fontFace: FONT, color: C.tealDark, italic: true,
  margin: 0, valign: "middle",
});
addFooterLine(s3);


// ════════════════════════════════════
//  第 4 页 · 老师的教学方法
// ════════════════════════════════════

const s4 = pres.addSlide();
s4.background = { color: C.white };
addPageTitle(s4, "AI+X 教学方法", "三大训练法 · 从听课到实战");

const methods = [
  { num: "01", title: "数字留痕", desc: "GitHub 协作记录\n代码即作品、过程即成果\n让每一行代码都被看见", icon: "📝" },
  { num: "02", title: "工具赋能", desc: "Hermes Agent 助教\nClaude Code 结对编程\nAI 工具链贯穿全过程", icon: "🛠" },
  { num: "03", title: "竞争成长", desc: "C2S 挑战任务\n强者带人·弱者自驱\n让每个人都找到自己的节奏", icon: "⚡" },
];

methods.forEach((m, idx) => {
  const mx = 0.9 + idx * 3.85;
  const my = 2.2;

  // 卡片
  addCard(s4, mx, my, 3.2, 4.1);

  // 顶部色条
  s4.addShape(pres.shapes.RECTANGLE, {
    x: mx, y: my, w: 3.2, h: 0.05,
    fill: { color: idx === 0 ? C.teal : idx === 1 ? C.blue : C.tealDark },
  });

  // 编号大号
  s4.addText(m.num, {
    x: mx + 0.2, y: my + 0.2, w: 1.5, h: 0.7,
    fontSize: 32, fontFace: FONT, color: C.teal, bold: true,
    margin: 0,
  });

  // Icon + 标题
  s4.addText(`${m.icon} ${m.title}`, {
    x: mx + 0.2, y: my + 0.85, w: 2.8, h: 0.5,
    fontSize: 14, fontFace: FONT, color: C.text, bold: true,
    margin: 0,
  });

  // 分割线
  s4.addShape(pres.shapes.RECTANGLE, {
    x: mx + 0.2, y: my + 1.4, w: 2.8, h: 0.008,
    fill: { color: C.gray },
  });

  // 描述
  s4.addText(m.desc, {
    x: mx + 0.2, y: my + 1.55, w: 2.8, h: 2.0,
    fontSize: 11, fontFace: FONT, color: C.tealMuted,
    lineSpacingMultiple: 1.7, margin: 0,
  });

  // 底部小装饰
  addDot(s4, mx + 2.55, my + 3.85, 0.04, idx === 0 ? C.teal : C.gray);
});

addFooterLine(s4);

// ════════════════════════════════════
//  第 5 页 · AI 编程工具对比：三款 Agent
// ════════════════════════════════════

const s4b = pres.addSlide();
s4b.background = { color: C.white };
addPageTitle(s4b, "AI 编程工具对比", "三款自主编码 Agent 的定位与选择");

// 三列卡片 — 每个工具一列
const tools = [
  {
    name: "Hermes Agent", icon: "🤖",
    items: [
      { label: "角色定位", value: "全能 AI 助手\n工作流编排+工具管理" },
      { label: "核心能力", value: "任务拆解与编排\n多工具自动调用\n持久记忆与技能管理" },
      { label: "交互方式", value: "自然语言对话\n自主执行+人工确认" },
      { label: "最佳场景", value: "复杂多步骤工作流\n跨工具协同任务\n日常开发全流程" },
    ],
    bar: C.tealDark,
  },
  {
    name: "Claude Code", icon: "🐙",
    items: [
      { label: "角色定位", value: "结对编程搭档\n深度代码开发与调试" },
      { label: "核心能力", value: "多文件代码重构\n深度调试与排查\n复杂 Git 操作" },
      { label: "交互方式", value: "终端内对话式编程\n所见即所得的代码操作" },
      { label: "最佳场景", value: "大范围代码重构\n疑难 Bug 排查\n复杂多文件修改" },
    ],
    bar: C.blue,
  },
  {
    name: "OpenCode", icon: "⚡",
    items: [
      { label: "角色定位", value: "快速编码代理\n原型开发与验证" },
      { label: "核心能力", value: "快速原型生成\n单文件代码编写\n测试用例生成" },
      { label: "交互方式", value: "终端内对话式编程\n轻量快速响应" },
      { label: "最佳场景", value: "快速原型验证\n独立功能开发\n单元测试编写" },
    ],
    bar: C.green,
  },
];

tools.forEach((tool, idx) => {
  const cx = 0.6 + idx * 4.1;
  const cy = 2.0;

  // 卡片背景
  addCard(s4b, cx, cy, 3.7, 4.8);

  // 顶部色条
  s4b.addShape(pres.shapes.RECTANGLE, {
    x: cx, y: cy, w: 3.7, h: 0.06,
    fill: { color: tool.bar },
  });

  // 工具名 + 图标
  s4b.addText(`${tool.icon}  ${tool.name}`, {
    x: cx + 0.2, y: cy + 0.2, w: 3.3, h: 0.5,
    fontSize: 14, fontFace: FONT, color: C.text, bold: true,
    margin: 0,
  });

  // 分隔线
  s4b.addShape(pres.shapes.RECTANGLE, {
    x: cx + 0.2, y: cy + 0.75, w: 3.3, h: 0.006,
    fill: { color: C.gray },
  });

  // 各项属性
  tool.items.forEach((item, i) => {
    const iy = cy + 0.9 + i * 0.95;

    // 标签
    s4b.addText(item.label, {
      x: cx + 0.2, y: iy, w: 1.0, h: 0.3,
      fontSize: 9, fontFace: FONT, color: tool.bar, bold: true,
      margin: 0,
    });

    // 值
    s4b.addText(item.value, {
      x: cx + 0.2, y: iy + 0.28, w: 3.3, h: 0.65,
      fontSize: 10, fontFace: FONT, color: C.tealMuted,
      lineSpacingMultiple: 1.4, margin: 0,
    });
  });
});

addFooterLine(s4b);

// ════════════════════════════════════
//  第 6 页 · GitHub 数字留痕
// ════════════════════════════════════

const s5 = pres.addSlide();
s5.background = { color: C.white };
addPageTitle(s5, "数字留痕", "\"数字留痕 + 作品展现 = 核心评估方式\"");

// 左：数字留痕的四种形式
addCard(s5, 0.6, 2.0, 5.8, 4.8);
s5.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 2.0, w: 0.05, h: 4.8,
  fill: { color: C.teal },
});

const traceTypes = [
  { icon: "💻", title: "GitHub 代码仓库", desc: "全过程中形成完整数字留痕" },
  { icon: "📄", title: "论文草稿与提交记录", desc: "学术成果的系统化沉淀" },
  { icon: "🎮", title: "Demo / 产品原型", desc: "可交互、可演示的作品" },
  { icon: "📋", title: "文档与过程记录", desc: "学习过程的完整轨迹" },
];

traceTypes.forEach((tt, idx) => {
  const ty = 2.3 + idx * 1.1;
  s5.addText(`${tt.icon} ${tt.title}`, {
    x: 1.0, y: ty, w: 5.0, h: 0.35,
    fontSize: 14, fontFace: FONT, color: C.text, bold: true,
    margin: 0,
  });
  s5.addText(tt.desc, {
    x: 1.0, y: ty + 0.35, w: 5.0, h: 0.5,
    fontSize: 11, fontFace: FONT, color: C.tealMuted,
    margin: 0,
  });
});

// 右：展示标准
addCard(s5, 6.8, 2.0, 5.8, 2.2);
s5.addShape(pres.shapes.RECTANGLE, {
  x: 6.8, y: 2.0, w: 0.05, h: 2.2,
  fill: { color: C.teal },
});
s5.addText("🌐 展示标准：必须走向国际平台", {
  x: 7.1, y: 2.15, w: 5.2, h: 0.4,
  fontSize: 13, fontFace: FONT, color: C.text, bold: true,
  margin: 0,
});
const platformItems = [
  "📕 论文发表（Workshop / Conference）",
  "🐙 开源平台（GitHub 等）",
  "🏆 国际挑战赛（AI4Math 等）",
];
s5.addText(platformItems.join("\n"), {
  x: 7.1, y: 2.6, w: 5.2, h: 1.4,
  fontSize: 11, fontFace: FONT, color: C.tealMuted,
  lineSpacingMultiple: 1.8, margin: 0,
});

// 右下：核心精神
addCard(s5, 6.8, 4.5, 5.8, 2.3);
s5.addShape(pres.shapes.RECTANGLE, {
  x: 6.8, y: 4.5, w: 0.05, h: 2.3,
  fill: { color: C.teal },
});
s5.addText("🎯 核心精神", {
  x: 7.1, y: 4.6, w: 5.2, h: 0.35,
  fontSize: 13, fontFace: FONT, color: C.text, bold: true,
  margin: 0,
});
s5.addText("不是做作业，而是：\n做作品 · 做成果 · 做可以被世界看到的东西", {
  x: 7.1, y: 5.0, w: 5.2, h: 1.0,
  fontSize: 12, fontFace: FONT, color: C.teal,
  lineSpacingMultiple: 1.6, margin: 0, italic: true,
});

addFooterLine(s5);


// ════════════════════════════════════
//  第 7 页 · Skill：可复用的程序性知识
// ════════════════════════════════════

const s6 = pres.addSlide();
s6.background = { color: C.white };
addPageTitle(s6, "Skill：可复用的程序性知识", "L4 抽象 → 可复用的 Workflow 或 Skill");

// 左：Skill 的定义
addCard(s6, 0.6, 2.0, 5.8, 2.5);
s6.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 2.0, w: 0.05, h: 2.5,
  fill: { color: C.teal },
});
s6.addText("❓ Skill 是什么？", {
  x: 0.9, y: 2.15, w: 5.2, h: 0.4,
  fontSize: 14, fontFace: FONT, color: C.text, bold: true,
  margin: 0,
});
s6.addText("Skill 是将「过程」固化为可复用的程序性知识。\n遇到同类任务时，Agent 动态连接 Skill，\n直接调用最佳方案，而非每次都从零开始。", {
  x: 0.9, y: 2.6, w: 5.2, h: 1.6,
  fontSize: 11, fontFace: FONT, color: C.tealMuted,
  lineSpacingMultiple: 1.7, margin: 0,
});

// 左下：在 L1-L5 中的位置
addCard(s6, 0.6, 4.8, 5.8, 2.0);
s6.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 4.8, w: 0.05, h: 2.0,
  fill: { color: C.blue },
});
s6.addText("📊 行为梯度中的位置", {
  x: 0.9, y: 4.95, w: 5.2, h: 0.35,
  fontSize: 13, fontFace: FONT, color: C.text, bold: true,
  margin: 0,
});
s6.addText("L1 模仿 → L2 解释 → L3 协作 → L4 抽象(→ Skill) → L5 传播\nSkill 是 L4 抽象到 L5 传播的关键桥梁——\n把经验变成可复用的资产，让他人也能调用", {
  x: 0.9, y: 5.4, w: 5.2, h: 1.2,
  fontSize: 10, fontFace: FONT, color: C.tealMuted,
  lineSpacingMultiple: 1.6, margin: 0,
});

// 右：Skill 驱动的架构
addCard(s6, 6.8, 2.0, 5.8, 2.5);
s6.addShape(pres.shapes.RECTANGLE, {
  x: 6.8, y: 2.0, w: 0.05, h: 2.5,
  fill: { color: C.teal },
});
s6.addText("⚙️ Skill 驱动的架构演进", {
  x: 7.1, y: 2.15, w: 5.2, h: 0.35,
  fontSize: 14, fontFace: FONT, color: C.text, bold: true,
  margin: 0,
});
s6.addText("相比传统固定流程（Computation Graph），\nSkill 模式通过 Agent 动态连接任务，\n利用对话交互实现灵活的工作流编排，\n大幅提升开发效率。", {
  x: 7.1, y: 2.6, w: 5.2, h: 1.6,
  fontSize: 11, fontFace: FONT, color: C.tealMuted,
  lineSpacingMultiple: 1.7, margin: 0,
});

// 右下：Meta Skill & 本体嵌入
addCard(s6, 6.8, 4.8, 5.8, 2.0);
s6.addShape(pres.shapes.RECTANGLE, {
  x: 6.8, y: 4.8, w: 0.05, h: 2.0,
  fill: { color: C.tealDark },
});
s6.addText("🧩 Meta Skill 与本体嵌入", {
  x: 7.1, y: 4.95, w: 5.2, h: 0.35,
  fontSize: 13, fontFace: FONT, color: C.text, bold: true,
  margin: 0,
});
s6.addText("• Meta Skill（如 Skill Creator）通过定义 Schema\n  自动生成特定任务的 Skill\n• 本体模型（Ontology）作为长期记忆\n  嵌入 Skill 中，沉淀领域知识", {
  x: 7.1, y: 5.35, w: 5.2, h: 1.3,
  fontSize: 10, fontFace: FONT, color: C.tealMuted,
  lineSpacingMultiple: 1.6, margin: 0,
});

addFooterLine(s6);

// ════════════════════════════════════
//  第 8 页 · 协作学习：行为梯度 L1 → L5
// ════════════════════════════════════

const s7 = pres.addSlide();
s7.background = { color: C.white };
addPageTitle(s7, "协作学习：行为梯度", "从个体模仿到网络传播，价值在被复用中规模化");

// 五级梯度 — 横向展示
const gradients = [
  { level: "L1", label: "模仿", en: "Copy", desc: "允许抄作业\n但必须标注来源\n并写下理解" },
  { level: "L2", label: "解释", en: "Explain", desc: "能够教别人\n复制 → 理解的传播" },
  { level: "L3", label: "协作", en: "Collaborate", desc: "团队分工\n记录协作轨迹" },
  { level: "L4", label: "抽象", en: "Abstract", desc: "过程→可复用的\nWorkflow 或 Skill" },
  { level: "L5", label: "传播", en: "Scale", desc: "作品被他人调用\n价值规模化" },
];

const arrowColors = [C.teal, C.blue, C.green, C.tealDark];
const itemW = 2.0;
const gap = 0.5;
const startX = 0.6;

gradients.forEach((g, idx) => {
  const gx = startX + idx * (itemW + gap);

  // 卡片
  addCard(s7, gx, 2.0, itemW, 4.5);

  // 顶部色条
  const barColor = idx < 2 ? C.teal : idx < 4 ? C.blue : C.tealDark;
  s7.addShape(pres.shapes.RECTANGLE, {
    x: gx, y: 2.0, w: itemW, h: 0.06,
    fill: { color: barColor },
  });

  // 级别大号
  s7.addText(g.level, {
    x: gx + 0.2, y: 2.2, w: 1.2, h: 0.5,
    fontSize: 22, fontFace: FONT, color: barColor, bold: true,
    margin: 0,
  });

  // 中文标签
  s7.addText(g.label, {
    x: gx + 0.2, y: 2.7, w: 1.6, h: 0.4,
    fontSize: 15, fontFace: FONT, color: C.text, bold: true,
    margin: 0,
  });

  // 英文标签
  s7.addText(g.en, {
    x: gx + 0.2, y: 3.1, w: 1.6, h: 0.3,
    fontSize: 10, fontFace: FONT, color: C.tealMuted, italic: true,
    margin: 0,
  });

  // 分割线
  s7.addShape(pres.shapes.RECTANGLE, {
    x: gx + 0.2, y: 3.55, w: 1.6, h: 0.006,
    fill: { color: C.gray },
  });

  // 描述
  s7.addText(g.desc, {
    x: gx + 0.2, y: 3.7, w: 1.6, h: 2.0,
    fontSize: 10, fontFace: FONT, color: C.tealMuted,
    lineSpacingMultiple: 1.6, margin: 0,
  });

  // 小圆点装饰
  addDot(s7, gx + 0.1, 2.0 + 0.1, 0.04, barColor);

  // 箭头（L1→L2→L3→L4→L5）
  if (idx < gradients.length - 1) {
    const arrowX = gx + itemW + 0.05;
    s7.addText("→", {
      x: arrowX, y: 2.0, w: 0.4, h: 4.5,
      fontSize: 18, fontFace: FONT, color: arrowColors[idx],
      align: "center", valign: "middle", margin: 0,
    });
  }
});

// 底部核心原则
s7.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 0.6, y: 6.3, w: 12.1, h: 0.4,
  fill: { color: C.teal, transparency: 90 },
  rectRadius: 0.08,
});
s7.addText("💡 核心原则：抄作业是输入，帮别人是输出，一起做是系统，而被复用才是价值", {
  x: 0.8, y: 6.3, w: 11.5, h: 0.4,
  fontSize: 10, fontFace: FONT, color: C.tealDark, italic: true,
  margin: 0, valign: "middle",
});
addFooterLine(s7);


// ════════════════════════════════════
//  第 8 页 · Richard 敏捷开发方法
// ════════════════════════════════════

const s8 = pres.addSlide();
s8.background = { color: C.white };
addPageTitle(s8, "AI 驱动的敏捷开发范式", "本体建模 → 设计工具 → 工作流管理 → MVP 验证 → 拿来主义");

// 五个步骤横排
const steps = [
  { num: "01", title: "本体建模", desc: "开发前先建立本体模型\n明确实体、关系与规则\nModel the World", color: C.teal },
  { num: "02", title: "Claude Design", desc: "原型→高保真HTML代码\n设计与开发一体化\n与 Claude Code 无缝对接", color: C.blue },
  { num: "03", title: "Linear", desc: "Agent 工作流管理\n任务拆解与跟踪\n透明化进度", color: C.green },
  { num: "04", title: "MVP 验证", desc: "最小可行产品先行\n验证闭环而非完美开发\n奥卡姆剃刀 · 快速迭代", color: C.tealDark },
  { num: "05", title: "代码黑盒", desc: "拿来主义 — 复用高星项目\n架构认知避免蒙眼开发\nLog 日志精准纠错", color: C.tealMuted },
];

steps.forEach((st, idx) => {
  const sx = 0.5 + idx * 2.55;
  const sy = 2.0;

  // 卡片
  addCard(s8, sx, sy, 2.3, 4.0);
  
  // 顶部色条
  s8.addShape(pres.shapes.RECTANGLE, {
    x: sx, y: sy, w: 2.3, h: 0.05,
    fill: { color: st.color },
  });

  // 编号
  s8.addText(st.num, {
    x: sx + 1.5, y: sy + 0.15, w: 0.6, h: 0.5,
    fontSize: 22, fontFace: FONT, color: st.color, bold: true,
    margin: 0, align: "right",
  });

  // 标题
  s8.addText(st.title, {
    x: sx + 0.2, y: sy + 0.7, w: 1.9, h: 0.4,
    fontSize: 14, fontFace: FONT, color: C.text, bold: true,
    margin: 0,
  });

  // 分割线
  s8.addShape(pres.shapes.RECTANGLE, {
    x: sx + 0.2, y: sy + 1.2, w: 1.9, h: 0.008,
    fill: { color: C.gray },
  });

  // 描述
  s8.addText(st.desc, {
    x: sx + 0.2, y: sy + 1.35, w: 1.9, h: 2.2,
    fontSize: 10, fontFace: FONT, color: C.tealMuted,
    lineSpacingMultiple: 1.6, margin: 0,
  });

  // 箭头（除了最后一个）
  if (idx < steps.length - 1) {
    s8.addText("→", {
      x: sx + 2.15, y: sy + 1.6, w: 0.5, h: 0.5,
      fontSize: 18, fontFace: FONT, color: C.teal,
      margin: 0, align: "center",
    });
  }
});

// 引用框
s8.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 0.6, y: 6.3, w: 12.1, h: 0.7,
  fill: { color: C.cream },
  rectRadius: 0.08,
});
s8.addText("\"拿来主义不是从零开始——优先在 GitHub 寻找高星开源项目，\n利用现有框架降低开发门槛\"", {
  x: 0.8, y: 6.35, w: 11.5, h: 0.55,
  fontSize: 12, fontFace: FONT, color: C.tealDark, italic: true,
  margin: 0, valign: "middle", align: "center",
});
addFooterLine(s8);


// ════════════════════════════════════
//  第 10 页 · 谢谢观看
// ════════════════════════════════════

const s9 = pres.addSlide();
s9.background = { color: C.white };

// 左侧装饰 — 一条简洁的青绿色带（呼应封面）
s9.addShape(pres.shapes.RECTANGLE, {
  x: 0.3, y: 0.3, w: 0.08, h: 6.9,
  fill: { color: C.teal },
});

// 谢谢观看
s9.addText("谢谢观看", {
  x: 1.0, y: 1.5, w: 6.0, h: 1.2,
  fontSize: 44, fontFace: FONT, color: C.text, bold: true,
  margin: 0,
});

s9.addText("A technically savvy presentation is important", {
  x: 1.0, y: 2.7, w: 6.0, h: 0.5,
  fontSize: 12, fontFace: FONT, color: C.tealMuted, italic: true,
  margin: 0,
});

// 分割线
s9.addShape(pres.shapes.RECTANGLE, {
  x: 1.0, y: 3.5, w: 3.5, h: 0.03,
  fill: { color: C.teal },
});
addDot(s9, 1.0, 3.5, 0.06, C.teal);
addDot(s9, 4.5, 3.5, 0.06, C.blue);

// 团队信息
s9.addText([
  { text: "面向工资编程队", options: { fontSize: 14, color: C.text, bold: true, breakLine: true } },
  { text: "AI+X Elite 20 · 面向工资编程队", options: { fontSize: 11, color: C.tealMuted, breakLine: true } },
  { text: "曾怡嫚 · 申梓淼 · 牛保康", options: { fontSize: 11, color: C.tealMuted } },
], {
  x: 1.0, y: 3.8, w: 6.0, h: 1.5,
  fontFace: FONT, lineSpacingMultiple: 1.6, margin: 0,
});

// 右侧装饰 — 大圆环（呼应封面）
s9.addShape(pres.shapes.OVAL, {
  x: 8.5, y: 0.8, w: 4.5, h: 4.5,
  fill: { color: C.teal, transparency: 92 },
});
s9.addShape(pres.shapes.OVAL, {
  x: 9.5, y: 1.8, w: 2.5, h: 2.5,
  fill: { color: C.teal, transparency: 88 },
});
s9.addShape(pres.shapes.OVAL, {
  x: 10.0, y: 4.8, w: 0.8, h: 0.8,
  fill: { color: C.teal, transparency: 85 },
});
s9.addShape(pres.shapes.OVAL, {
  x: 8.0, y: 5.5, w: 0.5, h: 0.5,
  fill: { color: C.blue, transparency: 80 },
});

s9.addText("曾怡嫚 · AI+X Elite 20 · 2025", {
  x: 1.0, y: 6.5, w: 6.0, h: 0.4,
  fontSize: 10, fontFace: FONT, color: C.gray,
  margin: 0,
});
addFooterLine(s9);


// ════════════════════════════════════
//  输出
// ════════════════════════════════════

const outPath = "/Users/wendao/Desktop/AI+X_学习之旅.pptx";
pres.writeFile({ fileName: outPath })
  .then(() => console.log("✅ PPT 生成成功！"))
  .catch(err => console.error("❌ 失败:", err));