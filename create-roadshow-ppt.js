const pptxgen = require("pptxgenjs");
const fs = require("fs");

const C = {
  PRIMARY: "2563EB", PRIMARY_DARK: "1E3A5F", PRIMARY_LIGHT: "EFF6FF",
  TEXT: "1E293B", TEXT_MUTED: "64748B",
  ACCENT: "F97316", ACCENT_LIGHT: "FFF7ED",
  WHITE: "FFFFFF", BORDER: "BFDBFE", LINE: "F1F5F9",
  DARK_TEXT: "94A3B8",
};
const F = { CN: "Microsoft YaHei", EN: "Arial" };
const S = { TITLE: 36, SUB: 18, H2: 22, BODY: 14, SMALL: 12, STAT: 44 };

const SC = "/Users/wendao/qitu-job-assistant/screenshots";
const AS = "/Users/wendao/qitu-job-assistant/frontend/src/assets";

function ex(f) { return fs.existsSync(f); }
function addImg(slide, file, x, y, fitW, fitH, opts) {
  if (!ex(file)) return;
  slide.addImage({ path: file, x, y, w: fitW, h: fitH, sizing: { type: "contain", w: fitW, h: fitH }, ...(opts || {}) });
}
function shadow(b, o, p) {
  return { type: "outer", color: "000000", blur: b||3, offset: o||1, angle: 135, opacity: p||0.08 };
}
function addT(slide, text, x, y, w, h, opts) {
  slide.addText(text, { x, y, w, h, fontFace: F.CN, ...opts });
}
function addFooter(slide, txt) {
  addT(slide, txt || "启途  |  3分钟路演", 0.6, 5.28, 4, 0.25, { fontSize: 9, color: C.TEXT_MUTED });
}
function addHeader(slide, title) {
  slide.addShape("rect", { x: 0, y: 0, w: 10, h: 0.04, fill: { color: C.PRIMARY } });
  slide.addShape("rect", { x: 0.6, y: 0.35, w: 0.04, h: 0.42, fill: { color: C.PRIMARY } });
  addT(slide, title, 0.85, 0.3, 8, 0.55, { fontSize: S.H2, bold: true, color: C.TEXT });
}

// Numbered circle helper (professional replacement for emoji)
function addNumCircle(slide, num, x, y, size) {
  const r = size || 0.4;
  slide.addShape("ellipse", { x, y, w: r, h: r, fill: { color: C.PRIMARY } });
  addT(slide, String(num), x, y, r, r, {
    fontSize: r * 36, bold: true, color: C.WHITE, align: "center", valign: "middle", fontFace: F.EN,
  });
}

const pres = new pptxgen();
pres.defineLayout({ name: "C16", width: 10, height: 5.625 });
pres.layout = "C16";
pres.author = "启途团队";
pres.title = "启途 — AI求职教育平台";

// ==================== SLIDE 1: COVER ====================
{
  const s = pres.addSlide();
  s.background = { color: C.PRIMARY_DARK };

  s.addShape("rect", { x: 7.2, y: -1.0, w: 4, h: 4, fill: { color: "25496D" }, rotation: 45 });
  s.addShape("ellipse", { x: 8.5, y: 3.8, w: 2.5, h: 2.5, fill: { color: "25496D" } });
  s.addShape("rect", { x: -0.8, y: 4.2, w: 2.5, h: 2, fill: { color: "25496D" }, rotation: -25 });

  s.addShape("rect", { x: 0.8, y: 1.5, w: 0.06, h: 1.3, fill: { color: C.ACCENT } });

  addT(s, "启 途", 1.1, 1.3, 5, 1.0, { fontSize: 50, bold: true, color: C.WHITE, fontFace: F.EN });
  addT(s, "AI求职教育平台", 1.1, 2.2, 5, 0.5, { fontSize: 22, color: "93C5FD" });
  addT(s, "一个人 + AI智能体团队，从零构建的全栈AI求职平台", 1.1, 2.9, 6.5, 0.4, { fontSize: 14, color: C.DARK_TEXT });

  s.addShape("rect", { x: 0, y: 4.7, w: 10, h: 0.925, fill: { color: "0F2A45" } });
  addT(s, "团队成员：曾怡嫚（组长）| 申梓淼 | 牛保康", 0.8, 4.85, 6, 0.3, { fontSize: 12, color: C.DARK_TEXT });
  addT(s, "AI+X Vibe Coding实验班（一期）", 0.8, 5.15, 5, 0.3, { fontSize: 11, color: "6B8CAE" });

  // Cat aligned with bottom bar boundary
  addImg(s, `${AS}/xiaoju-on-banner-lg.png`, 6.5, 3.6, 2.5, 1.32);
}

// ==================== SLIDE 2: PROBLEM & SCENE ====================
{
  const s = pres.addSlide();
  s.background = { color: C.WHITE };
  addHeader(s, "真实问题与场景");

  // Left: screenshot
  s.addShape("rect", { x: 0.6, y: 1.1, w: 4.2, h: 3.0, fill: { color: C.PRIMARY_LIGHT }, rectRadius: 0.1, shadow: shadow() });
  addImg(s, `${SC}/04-career-explore.png`, 0.65, 1.15, 4.1, 2.9);

  // Right: 3 pain point cards with numbers (no leading zero)
  const pains = [
    { n: "1", t: "方向迷茫", d: "很多大一学生不清楚所学专业未来能从事什么岗位，也不了解不同职业方向的具体要求和路径，缺乏明确的规划。" },
    { n: "2", t: "面试零经验", d: "校园内缺少真实面试场景的训练机会，学生面对面试官时容易紧张无措，缺乏有效的应对技巧和实战经验。" },
    { n: "3", t: "简历不会写", d: "大多数学生不知道如何提炼个人优势、撰写有竞争力的简历，求职第一关就难以迈出，影响后续信心。" },
  ];

  const cardX = 5.2, cardW = 4.4, cardH = 1.05, gapY = 1.08;
  pains.forEach((p, i) => {
    const cy = 0.95 + i * gapY;
    // Card bg
    s.addShape("roundRect", {
      x: cardX, y: cy, w: cardW, h: cardH,
      fill: { color: i === 1 ? C.ACCENT_LIGHT : C.PRIMARY_LIGHT },
      line: { color: C.BORDER, width: 0.8 }, rectRadius: 0.08,
    });
    // Number circle
    s.addShape("ellipse", { x: cardX + 0.12, y: cy + 0.22, w: 0.35, h: 0.35, fill: { color: C.PRIMARY } });
    addT(s, p.n, cardX + 0.12, cy + 0.22, 0.35, 0.35, {
      fontSize: 15, bold: true, color: C.WHITE, align: "center", valign: "middle", fontFace: F.EN,
    });
    // Title
    addT(s, p.t, cardX + 0.65, cy + 0.15, 3.5, 0.28, { fontSize: 14, bold: true, color: C.TEXT });
    // Description - bigger area
    addT(s, p.d, cardX + 0.65, cy + 0.48, 3.55, 0.5, { fontSize: 9.5, color: C.TEXT_MUTED, lineSpacingMultiple: 1.15, valign: "top" });
  });

  // Target users bar - moved down to avoid overlap
  s.addShape("rect", { x: 0.6, y: 4.3, w: 8.8, h: 0.75, fill: { color: "F8FAFC" }, rectRadius: 0.08 });
  addT(s, "👥 目标用户：在校大学生（尤其大一新生）— 面临职业规划起步难、求职准备无从下手", 0.85, 4.42, 8.3, 0.5, { fontSize: 12, color: C.TEXT, lineSpacingMultiple: 1.3 });

  addFooter(s);
}

// ==================== SLIDE 3: SOLUTION & FEATURES ====================
{
  const s = pres.addSlide();
  s.background = { color: C.WHITE };
  addHeader(s, "解决方案与成果展示");

  // 3 feature cards with more text, fewer screenshots
  const features = [
    {
      img: `${SC}/05-interview-sim.png`,
      t: "AI面试模拟",
      d: "支持标准面试、压力面试、项目深挖三种模式，AI根据岗位要求和简历内容动态出题。对话过程全程记录，面试结束后自动生成评估报告，分析回答质量、表达能力和知识薄弱点，并提供针对性改进建议。",
    },
    {
      img: `${SC}/04-career-explore.png`,
      t: "智能职业探索",
      d: "输入专业和兴趣方向，AI自动匹配合适岗位，展示职业详情、薪资范围、能力要求。提供三级职业图谱（行业→岗位→细分方向），并为每个岗位自动生成包含证书推荐、学习资源和任务清单的成长路径。",
    },
    {
      img: `${SC}/06-exam-practice.png`,
      t: "AI笔试练习",
      d: "支持行业→岗位→题型三层筛选，AI智能出题涵盖选择题、编程题等多种题型。限时作答，提交后自动批改并输出考点统计报告，答错题目自动收录至错题本，支持「待回顾/已掌握」标记和反复练习。",
    },
  ];

  const cardW = 2.72, cardH = 3.6, gapX = 0.32, startX = 0.6, startY = 1.05;

  features.forEach((f, idx) => {
    const cx = startX + (cardW + gapX) * idx;

    s.addShape("roundRect", {
      x: cx, y: startY, w: cardW, h: cardH,
      fill: { color: C.WHITE }, line: { color: C.BORDER, width: 1 },
      rectRadius: 0.06, shadow: shadow(3, 1, 0.08),
    });

    // Screenshot
    s.addShape("rect", { x: cx + 0.1, y: startY + 0.1, w: cardW - 0.2, h: 1.2, fill: { color: C.PRIMARY_LIGHT }, rectRadius: 0.04 });
    addImg(s, f.img, cx + 0.12, startY + 0.12, cardW - 0.24, 1.16);

    // Divider
    s.addShape("rect", { x: cx + 0.3, y: startY + 1.4, w: cardW - 0.6, h: 0, line: { color: C.LINE, width: 0.8, dashType: "dash" } });

    // Title with accent bar
    s.addShape("rect", { x: cx + 0.12, y: startY + 1.55, w: 0.04, h: 0.35, fill: { color: C.PRIMARY } });
    addT(s, f.t, cx + 0.28, startY + 1.5, cardW - 0.4, 0.4, { fontSize: 14, bold: true, color: C.TEXT });

    // Description - much more text
    addT(s, f.d, cx + 0.12, startY + 1.95, cardW - 0.24, 1.5, { fontSize: 10, color: C.TEXT_MUTED, lineSpacingMultiple: 1.35, valign: "top" });
  });

  addFooter(s);
}

// ==================== SLIDE 4: AI COLLABORATION ====================
{
  const s = pres.addSlide();
  s.background = { color: C.PRIMARY_DARK };

  s.addShape("rect", { x: 0, y: 0, w: 10, h: 0.04, fill: { color: C.ACCENT } });
  addT(s, "AI协同开发模式", 0.8, 0.3, 6, 0.55, { fontSize: S.H2, bold: true, color: C.WHITE });

  // Human panel - professional title, no emoji
  s.addShape("roundRect", { x: 0.6, y: 1.1, w: 4.15, h: 3.5, fill: { color: "0F2A45" }, rectRadius: 0.08 });
  // Panel header with professional styling
  s.addShape("rect", { x: 0.6, y: 1.1, w: 4.15, h: 0.55, fill: { color: C.ACCENT }, rectRadius: 0.08 });
  s.addShape("rect", { x: 0.6, y: 1.5, w: 4.15, h: 0.08, fill: { color: C.ACCENT } }); // cover bottom corner
  // Redraw header area properly
  s.addShape("roundRect", { x: 0.6, y: 1.1, w: 4.15, h: 0.5, fill: { color: "C24A0A" }, rectRadius: 0.08 });
  // Overlay bottom corners with rounded rect
  s.addShape("rect", { x: 0.6, y: 1.45, w: 4.15, h: 0.15, fill: { color: "C24A0A" } });
  addT(s, "团队负责人", 0.85, 1.15, 3.5, 0.4, { fontSize: 15, bold: true, color: C.WHITE });

  // Use simple text bullet points with colored dots
  addT(s, [
    { text: "●", options: { fontSize: 10, color: C.ACCENT, lineSpacingMultiple: 1.6, fontFace: F.EN } },
    { text: " 需求分析与产品方向决策", options: { fontSize: 12, color: "93C5FD", lineSpacingMultiple: 1.6 } },
    { text: "\n●", options: { fontSize: 10, color: C.ACCENT, lineSpacingMultiple: 1.6, fontFace: F.EN } },
    { text: " 系统架构设计与技术选型", options: { fontSize: 12, color: "93C5FD", lineSpacingMultiple: 1.6 } },
    { text: "\n●", options: { fontSize: 10, color: C.ACCENT, lineSpacingMultiple: 1.6, fontFace: F.EN } },
    { text: " AI输出验证与方案修正", options: { fontSize: 12, color: "93C5FD", lineSpacingMultiple: 1.6 } },
    { text: "\n●", options: { fontSize: 10, color: C.ACCENT, lineSpacingMultiple: 1.6, fontFace: F.EN } },
    { text: " 界面视觉与交互体验把关", options: { fontSize: 12, color: "93C5FD", lineSpacingMultiple: 1.6 } },
    { text: "\n●", options: { fontSize: 10, color: C.ACCENT, lineSpacingMultiple: 1.6, fontFace: F.EN } },
    { text: " 功能测试验收与质量把控", options: { fontSize: 12, color: "93C5FD", lineSpacingMultiple: 1.6 } },
  ], 0.85, 1.85, 3.6, 2.6, { valign: "top" });

  // AI panel
  s.addShape("roundRect", { x: 5.25, y: 1.1, w: 4.15, h: 3.5, fill: { color: "0F2A45" }, rectRadius: 0.08 });
  s.addShape("roundRect", { x: 5.25, y: 1.1, w: 4.15, h: 0.5, fill: { color: C.PRIMARY }, rectRadius: 0.08 });
  s.addShape("rect", { x: 5.25, y: 1.45, w: 4.15, h: 0.15, fill: { color: C.PRIMARY } });
  addT(s, "AI编程助手", 5.5, 1.15, 3.5, 0.4, { fontSize: 15, bold: true, color: C.WHITE });

  addT(s, [
    { text: "●", options: { fontSize: 10, color: C.PRIMARY, lineSpacingMultiple: 1.6, fontFace: F.EN } },
    { text: " 代码编写与功能实现", options: { fontSize: 12, color: "93C5FD", lineSpacingMultiple: 1.6 } },
    { text: "\n●", options: { fontSize: 10, color: C.PRIMARY, lineSpacingMultiple: 1.6, fontFace: F.EN } },
    { text: " 代码审查与缺陷修复", options: { fontSize: 12, color: "93C5FD", lineSpacingMultiple: 1.6 } },
    { text: "\n●", options: { fontSize: 10, color: C.PRIMARY, lineSpacingMultiple: 1.6, fontFace: F.EN } },
    { text: " 技术方案建议与快速原型", options: { fontSize: 12, color: "93C5FD", lineSpacingMultiple: 1.6 } },
    { text: "\n●", options: { fontSize: 10, color: C.PRIMARY, lineSpacingMultiple: 1.6, fontFace: F.EN } },
    { text: " 自动化测试与文档编写", options: { fontSize: 12, color: "93C5FD", lineSpacingMultiple: 1.6 } },
    { text: "\n●", options: { fontSize: 10, color: C.PRIMARY, lineSpacingMultiple: 1.6, fontFace: F.EN } },
    { text: " 数据模型与接口开发", options: { fontSize: 12, color: "93C5FD", lineSpacingMultiple: 1.6 } },
  ], 5.5, 1.85, 3.6, 2.6, { valign: "top" });

  // Center connector
  s.addShape("ellipse", { x: 4.55, y: 2.55, w: 0.9, h: 0.9, fill: { color: C.PRIMARY } });
  addT(s, "⇄", 4.7, 2.65, 0.6, 0.6, { fontSize: 28, color: C.WHITE, align: "center", valign: "middle", fontFace: F.EN });

  // Tech stack
  s.addShape("rect", { x: 0.6, y: 4.8, w: 8.8, h: 0.45, fill: { color: "0F2A45" }, rectRadius: 0.06 });
  addT(s, "技术栈：Vue 3 + FastAPI + SQLite | AI引擎：小米MiMo大模型 | 一人+AI双脑开发", 0.85, 4.85, 8.3, 0.35, { fontSize: 11, color: C.DARK_TEXT, align: "center" });

  addFooter(s);
}

// ==================== SLIDE 5: VERIFICATION & TEAM ====================
{
  const s = pres.addSlide();
  s.background = { color: C.WHITE };
  addHeader(s, "验证、迭代与团队贡献");

  // Stats cards
  const stats = [
    { n: "36+", l: "职业方向覆盖", m: "互联网/金融/医疗等多行业" },
    { n: "3", l: "面试模拟模式", m: "标准/压力/项目深挖" },
    { n: "6", l: "核心功能模块", m: "全流程求职支持" },
    { n: "1", l: "人 + AI团队", m: "创新双脑开发模式" },
  ];

  stats.forEach((st, i) => {
    const sx = 0.6 + i * 2.27;
    s.addShape("roundRect", {
      x: sx, y: 1.1, w: 2.0, h: 1.6,
      fill: { color: i % 2 === 0 ? C.PRIMARY_LIGHT : C.WHITE },
      line: { color: C.BORDER, width: 0.8 }, rectRadius: 0.06,
    });
    addT(s, st.n, sx, 1.2, 2, 0.6, { fontSize: S.STAT, bold: true, color: C.PRIMARY, align: "center", fontFace: F.EN });
    addT(s, st.l, sx, 1.8, 2, 0.3, { fontSize: 13, bold: true, color: C.TEXT, align: "center" });
    addT(s, st.m, sx, 2.1, 2, 0.35, { fontSize: 10, color: C.TEXT_MUTED, align: "center" });
  });

  // Team
  s.addShape("rect", { x: 0.6, y: 2.95, w: 8.8, h: 1.55, fill: { color: "F8FAFC" }, rectRadius: 0.08 });
  addT(s, "团队分工", 0.85, 3.05, 4, 0.35, { fontSize: 14, bold: true, color: C.TEXT });
  addT(s, [
    { text: "曾怡嫚（组长）", options: { fontSize: 12, bold: true, color: C.TEXT } },
    { text: " — 整体架构设计、后端开发、AI引擎集成、产品方向决策", options: { fontSize: 12, color: C.TEXT } },
  ], 0.85, 3.42, 8, 0.28, {});
  addT(s, [
    { text: "申梓淼", options: { fontSize: 12, bold: true, color: C.TEXT_MUTED } },
    { text: " — 前端页面开发、功能测试与用户体验优化", options: { fontSize: 12, color: C.TEXT_MUTED } },
  ], 0.85, 3.72, 8, 0.28, {});
  addT(s, [
    { text: "牛保康", options: { fontSize: 12, bold: true, color: C.TEXT_MUTED } },
    { text: " — 数据处理、项目文档编写与测试支撑", options: { fontSize: 12, color: C.TEXT_MUTED } },
  ], 0.85, 4.02, 8, 0.28, {});

  // Process bar
  s.addShape("rect", { x: 0.6, y: 4.65, w: 8.8, h: 0.5, fill: { color: C.PRIMARY_LIGHT }, rectRadius: 0.06 });
  addT(s, "迭代过程：Git版本控制 | 模块逐个串通 | AI辅助测试验证 | 持续优化改进", 0.85, 4.73, 8.3, 0.35, { fontSize: 11, color: C.TEXT });

  addFooter(s);
}

// ==================== SLIDE 6: CLOSING ====================
{
  const s = pres.addSlide();
  s.background = { color: C.PRIMARY_DARK };

  s.addShape("ellipse", { x: -1.5, y: -1, w: 4, h: 4, fill: { color: "25496D" } });
  s.addShape("rect", { x: 7, y: 3.5, w: 4.5, h: 3, fill: { color: "25496D" }, rotation: 30 });

  addT(s, "启 途", 0, 1.0, 10, 0.9, { fontSize: 46, bold: true, color: C.WHITE, align: "center", fontFace: F.EN });
  addT(s, "AI求职教育平台", 0, 1.85, 10, 0.45, { fontSize: 20, color: "93C5FD", align: "center" });

  s.addShape("rect", { x: 3.5, y: 2.5, w: 3, h: 0.02, fill: { color: C.ACCENT } });

  addT(s, "我们希望下一步获得", 0, 2.8, 10, 0.4, { fontSize: 16, color: C.WHITE, align: "center" });
  addT(s, "企业场景对接 · 校内试用 · 实习就业面谈", 0, 3.2, 10, 0.5, { fontSize: 22, bold: true, color: C.ACCENT, align: "center" });
  addT(s, "让启途继续完善、真正落地", 0, 3.8, 10, 0.35, { fontSize: 14, color: C.DARK_TEXT, align: "center" });

  addT(s, "感谢各位老师聆听  恳请批评指正", 0, 4.5, 10, 0.4, { fontSize: 14, color: C.WHITE, align: "center" });

  // No cat image on closing slide - removed as requested

  addT(s, "团队成员：曾怡嫚 | 申梓淼 | 牛保康", 0.6, 5.2, 5, 0.25, { fontSize: 10, color: "6B8CAE" });
}

// ===== SAVE =====
const outPath = "/Users/wendao/Desktop/启途-结项路演PPT.pptx";
pres.writeFile({ fileName: outPath }).then(() => {
  console.log("✅ PPT saved: " + outPath);
}).catch(err => {
  console.error("❌ Error:", err);
});
