const pptxgen = require("pptxgenjs");
const fs = require("fs");

// ===== THEME =====
const C = {
  PRIMARY: "2563EB", PRIMARY_DARK: "1E3A5F", PRIMARY_LIGHT: "EFF6FF",
  TEXT: "1E293B", TEXT_MUTED: "64748B",
  ACCENT: "F97316", ACCENT_LIGHT: "FFF7ED",
  WHITE: "FFFFFF", BORDER: "BFDBFE", LINE: "F1F5F9",
  DARK_TEXT: "94A3B8",
};
const F = { CN: "Microsoft YaHei", EN: "Arial" };
const S = { TITLE: 36, SUB: 18, H2: 22, BODY: 14, SMALL: 12, STAT: 44 };
const L = { W: 10, H: 5.625, MX: 0.6, CW: 8.8 };

const SC = "/Users/wendao/qitu-job-assistant/screenshots";
const AS = "/Users/wendao/qitu-job-assistant/frontend/src/assets";

function ex(f) { return fs.existsSync(f); }

// Helper: add image preserving aspect ratio
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

const pres = new pptxgen();
pres.defineLayout({ name: "C16", width: 10, height: 5.625 });
pres.layout = "C16";
pres.author = "启途团队";
pres.title = "启途 — AI求职教育平台";

// ==================== SLIDE 1: COVER ====================
{
  const s = pres.addSlide();
  s.background = { color: C.PRIMARY_DARK };

  // Background geometric shapes
  s.addShape("rect", { x: 7.2, y: -1.0, w: 4, h: 4, fill: { color: "25496D" }, rotation: 45 });
  s.addShape("ellipse", { x: 8.5, y: 3.8, w: 2.5, h: 2.5, fill: { color: "25496D" } });
  s.addShape("rect", { x: -0.8, y: 4.2, w: 2.5, h: 2, fill: { color: "25496D" }, rotation: -25 });

  // Accent line
  s.addShape("rect", { x: 0.8, y: 1.5, w: 0.06, h: 1.3, fill: { color: C.ACCENT } });

  // Title
  addT(s, "启 途", 1.1, 1.3, 5, 1.0, { fontSize: 50, bold: true, color: C.WHITE, fontFace: F.EN });
  addT(s, "AI求职教育平台", 1.1, 2.2, 5, 0.5, { fontSize: 22, color: "93C5FD" });

  // Subtitle
  addT(s, "一个人 + AI智能体团队，从零构建的全栈AI求职平台", 1.1, 2.9, 6.5, 0.4, { fontSize: 14, color: C.DARK_TEXT });

  // Bottom bar
  s.addShape("rect", { x: 0, y: 4.7, w: 10, h: 0.925, fill: { color: "0F2A45" } });
  addT(s, "团队成员：曾怡嫚（组长）| 申梓淼 | 牛保康", 0.8, 4.85, 6, 0.3, { fontSize: 12, color: C.DARK_TEXT });
  addT(s, "AI+X Vibe Coding实验班（一期）", 0.8, 5.15, 5, 0.3, { fontSize: 11, color: "6B8CAE" });

  // Cat image - use xiaoju-full.jpg (1280x1280 square) - properly sized
  // Place at right side, use sizing: contain so it doesn't stretch
  addImg(s, `${AS}/xiaoju-full.jpg`, 6.5, 0.8, 3.2, 3.5);
}

// ==================== SLIDE 2: PROBLEM ====================
{
  const s = pres.addSlide();
  s.background = { color: C.WHITE };

  // Header
  s.addShape("rect", { x: 0, y: 0, w: 10, h: 0.04, fill: { color: C.PRIMARY } });
  s.addShape("rect", { x: 0.6, y: 0.35, w: 0.04, h: 0.42, fill: { color: C.PRIMARY } });
  addT(s, "真实问题与场景", 0.85, 0.3, 5, 0.55, { fontSize: S.H2, bold: true, color: C.TEXT });

  // Left: screenshot
  s.addShape("rect", { x: 0.6, y: 1.1, w: 4.2, h: 3.0, fill: { color: C.PRIMARY_LIGHT }, rectRadius: 0.1, shadow: shadow() });
  addImg(s, `${SC}/04-career-explore.png`, 0.65, 1.15, 4.1, 2.9);

  // Right: pain point cards
  const pains = [
    { icon: "🎯", t: "职业方向迷茫", d: "大一学生不知道\n自己适合什么岗位" },
    { icon: "🎤", t: "面试零经验", d: "没有实战机会\n面对面试官紧张无措" },
    { icon: "📄", t: "简历不会写", d: "不知道怎么写\n一份像样的简历" },
  ];

  pains.forEach((p, i) => {
    const cy = 1.1 + i * 1.03;
    s.addShape("roundRect", {
      x: 5.2, y: cy, w: 4.4, h: 0.88,
      fill: { color: i === 1 ? C.ACCENT_LIGHT : C.PRIMARY_LIGHT },
      line: { color: C.BORDER, width: 0.8 }, rectRadius: 0.08,
    });
    addT(s, p.icon, 5.35, cy + 0.15, 0.5, 0.55, { fontSize: 24, align: "center", valign: "middle" });
    addT(s, p.t, 5.95, cy + 0.08, 3.2, 0.35, { fontSize: 14, bold: true, color: C.TEXT });
    addT(s, p.d, 5.95, cy + 0.42, 3.2, 0.42, { fontSize: 11, color: C.TEXT_MUTED, lineSpacingMultiple: 1.2 });
  });

  // Target users bar
  s.addShape("rect", { x: 0.6, y: 4.3, w: 8.8, h: 0.85, fill: { color: "F8FAFC" }, rectRadius: 0.08 });
  addT(s, "👥 目标用户：在校大学生（尤其大一新生）— 面临职业规划起步难、求职准备无从下手", 0.85, 4.42, 8.3, 0.6, { fontSize: 12, color: C.TEXT, lineSpacingMultiple: 1.3 });

  addT(s, "启途  |  3分钟路演", 0.6, 5.28, 4, 0.25, { fontSize: 9, color: C.TEXT_MUTED });
}

// ==================== SLIDE 3: FEATURES ====================
{
  const s = pres.addSlide();
  s.background = { color: C.WHITE };

  s.addShape("rect", { x: 0, y: 0, w: 10, h: 0.04, fill: { color: C.PRIMARY } });
  s.addShape("rect", { x: 0.6, y: 0.35, w: 0.04, h: 0.42, fill: { color: C.PRIMARY } });
  addT(s, "解决方案与成果展示", 0.85, 0.3, 6, 0.55, { fontSize: S.H2, bold: true, color: C.TEXT });
  addT(s, "6大核心功能模块", 7.2, 0.35, 2.5, 0.4, { fontSize: 11, color: C.TEXT_MUTED, align: "right" });

  const features = [
    { img: `${SC}/04-career-explore.png`, t: "职业探索", d: "AI推荐+三级职业图谱\n成长路径+证书推荐" },
    { img: `${SC}/05-interview-sim.png`, t: "面试模拟", d: "对话式AI面试官\n三种模式+表情分析" },
    { img: `${SC}/06-exam-practice.png`, t: "笔试练习", d: "多题型AI出题\n限时作答+错题本" },
    { img: `${SC}/03-dashboard.png`, t: "首页仪表盘", d: "收藏汇总+快速导航\nAI助手小橘陪伴" },
    { img: `${SC}/07-delivery-assistant.png`, t: "投递助手", d: "AI匹配推荐\n全流程投递追踪" },
    { img: `${SC}/08-settings.png`, t: "简历优化", d: "AI智能润色\n针对岗位优化内容" },
  ];

  const cardW = 2.72, cardH = 2.85, gapX = 0.32, gapY = 0.2, startX = 0.6, startY = 1.05;

  features.forEach((f, idx) => {
    const col = idx % 3, row = Math.floor(idx / 3);
    const cx = startX + (cardW + gapX) * col;
    const cy = startY + (cardH + gapY) * row;

    s.addShape("roundRect", { x: cx, y: cy, w: cardW, h: cardH, fill: { color: C.WHITE }, line: { color: C.BORDER, width: 1 }, rectRadius: 0.06, shadow: shadow(3, 1, 0.08) });

    // Screenshot area - use contain sizing to prevent stretch
    s.addShape("rect", { x: cx + 0.1, y: cy + 0.1, w: cardW - 0.2, h: 1.35, fill: { color: C.PRIMARY_LIGHT }, rectRadius: 0.04 });
    addImg(s, f.img, cx + 0.12, cy + 0.12, cardW - 0.24, 1.31);

    // Divider
    s.addShape("rect", { x: cx + 0.3, y: cy + 1.55, w: cardW - 0.6, h: 0, line: { color: C.LINE, width: 0.8, dashType: "dash" } });

    // Title with accent bar
    s.addShape("rect", { x: cx + 0.12, y: cy + 1.7, w: 0.04, h: 0.35, fill: { color: C.PRIMARY } });
    addT(s, f.t, cx + 0.28, cy + 1.65, cardW - 0.4, 0.4, { fontSize: 13, bold: true, color: C.TEXT });
    addT(s, f.d, cx + 0.15, cy + 2.1, cardW - 0.3, 0.65, { fontSize: 10, color: C.TEXT_MUTED, lineSpacingMultiple: 1.2 });
  });

  addT(s, "启途  |  3分钟路演", 0.6, 5.28, 4, 0.25, { fontSize: 9, color: C.TEXT_MUTED });
}

// ==================== SLIDE 4: AI COLLAB ====================
{
  const s = pres.addSlide();
  s.background = { color: C.PRIMARY_DARK };

  s.addShape("rect", { x: 0, y: 0, w: 10, h: 0.04, fill: { color: C.ACCENT } });
  addT(s, "AI协同与双脑开发", 0.8, 0.3, 6, 0.55, { fontSize: S.H2, bold: true, color: C.WHITE });

  // Human panel
  s.addShape("roundRect", { x: 0.6, y: 1.1, w: 4.15, h: 3.5, fill: { color: "0F2A45" }, rectRadius: 0.08 });
  addT(s, "🧑‍💻  人（组长）", 0.85, 1.25, 3.5, 0.45, { fontSize: 16, bold: true, color: C.WHITE });
  addT(s, [
    { text: "• 需求分析与产品方向决策", options: { fontSize: 12, color: "93C5FD", lineSpacingMultiple: 1.5 } },
    { text: "\n• 架构设计与技术选型", options: { fontSize: 12, color: "93C5FD", lineSpacingMultiple: 1.5 } },
    { text: "\n• AI输出验证与修正", options: { fontSize: 12, color: "93C5FD", lineSpacingMultiple: 1.5 } },
    { text: "\n• 界面视觉与交互把关", options: { fontSize: 12, color: "93C5FD", lineSpacingMultiple: 1.5 } },
    { text: "\n• 测试验收与质量把控", options: { fontSize: 12, color: "93C5FD", lineSpacingMultiple: 1.5 } },
  ], 0.85, 1.85, 3.6, 2.5, { valign: "top" });

  // AI panel
  s.addShape("roundRect", { x: 5.25, y: 1.1, w: 4.15, h: 3.5, fill: { color: "0F2A45" }, rectRadius: 0.08 });
  addT(s, "🤖  AI助手（咪 / Claude Code）", 5.5, 1.25, 3.5, 0.45, { fontSize: 16, bold: true, color: C.WHITE });
  addT(s, [
    { text: "• 编码执行与功能实现", options: { fontSize: 12, color: "93C5FD", lineSpacingMultiple: 1.5 } },
    { text: "\n• 代码审查与Bug修复", options: { fontSize: 12, color: "93C5FD", lineSpacingMultiple: 1.5 } },
    { text: "\n• 方案建议与快速原型", options: { fontSize: 12, color: "93C5FD", lineSpacingMultiple: 1.5 } },
    { text: "\n• 文档编写与测试脚本", options: { fontSize: 12, color: "93C5FD", lineSpacingMultiple: 1.5 } },
    { text: "\n• 数据库设计与接口开发", options: { fontSize: 12, color: "93C5FD", lineSpacingMultiple: 1.5 } },
  ], 5.5, 1.85, 3.6, 2.5, { valign: "top" });

  // Center connector
  s.addShape("ellipse", { x: 4.55, y: 2.55, w: 0.9, h: 0.9, fill: { color: C.PRIMARY } });
  addT(s, "⇄", 4.7, 2.65, 0.6, 0.6, { fontSize: 28, color: C.WHITE, align: "center", valign: "middle", fontFace: F.EN });

  // Tech stack bar
  s.addShape("rect", { x: 0.6, y: 4.8, w: 8.8, h: 0.45, fill: { color: "0F2A45" }, rectRadius: 0.06 });
  addT(s, "技术栈：Vue 3 + FastAPI + SQLite | AI引擎：小米MiMo大模型 | 一人+AI双脑开发", 0.85, 4.85, 8.3, 0.35, { fontSize: 11, color: C.DARK_TEXT, align: "center" });

  addT(s, "启途  |  3分钟路演", 0.6, 5.28, 4, 0.25, { fontSize: 9, color: "6B8CAE" });
}

// ==================== SLIDE 5: VERIFICATION ====================
{
  const s = pres.addSlide();
  s.background = { color: C.WHITE };

  s.addShape("rect", { x: 0, y: 0, w: 10, h: 0.04, fill: { color: C.PRIMARY } });
  s.addShape("rect", { x: 0.6, y: 0.35, w: 0.04, h: 0.42, fill: { color: C.PRIMARY } });
  addT(s, "验证、迭代与团队贡献", 0.85, 0.3, 6, 0.55, { fontSize: S.H2, bold: true, color: C.TEXT });

  // Stats cards
  const stats = [
    { n: "36+", l: "职业方向覆盖", m: "互联网/金融/医疗等" },
    { n: "3", l: "面试模式", m: "标准/压力/项目深挖" },
    { n: "6", l: "功能模块", m: "全流程求职支持" },
    { n: "1", l: "人 + AI团队", m: "双脑开发模式" },
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

  // Team section
  s.addShape("rect", { x: 0.6, y: 2.95, w: 8.8, h: 1.55, fill: { color: "F8FAFC" }, rectRadius: 0.08 });
  addT(s, "👥 团队分工", 0.85, 3.05, 4, 0.35, { fontSize: 14, bold: true, color: C.TEXT });
  addT(s, "曾怡嫚（组长）— 整体架构、后端开发、AI集成、产品方向", 0.85, 3.42, 8, 0.28, { fontSize: 12, color: C.TEXT });
  addT(s, "申梓淼 — 前端页面开发与功能测试", 0.85, 3.72, 8, 0.28, { fontSize: 12, color: C.TEXT_MUTED });
  addT(s, "牛保康 — 数据处理与项目文档", 0.85, 4.02, 8, 0.28, { fontSize: 12, color: C.TEXT_MUTED });

  // Process bar
  s.addShape("rect", { x: 0.6, y: 4.65, w: 8.8, h: 0.5, fill: { color: C.PRIMARY_LIGHT }, rectRadius: 0.06 });
  addT(s, "🔄 迭代过程：Git版本控制 | 功能模块逐个串通 | AI辅助测试验证 | 持续优化改进", 0.85, 4.73, 8.3, 0.35, { fontSize: 11, color: C.TEXT });

  addT(s, "启途  |  3分钟路演", 0.6, 5.28, 4, 0.25, { fontSize: 9, color: C.TEXT_MUTED });
}

// ==================== SLIDE 6: CLOSING ====================
{
  const s = pres.addSlide();
  s.background = { color: C.PRIMARY_DARK };

  // Decorative
  s.addShape("ellipse", { x: -1.5, y: -1, w: 4, h: 4, fill: { color: "25496D" } });
  s.addShape("rect", { x: 7, y: 3.5, w: 4.5, h: 3, fill: { color: "25496D" }, rotation: 30 });

  // Center title
  addT(s, "启 途", 0, 1.0, 10, 0.9, { fontSize: 46, bold: true, color: C.WHITE, align: "center", fontFace: F.EN });
  addT(s, "AI求职教育平台", 0, 1.85, 10, 0.45, { fontSize: 20, color: "93C5FD", align: "center" });

  // Decorative line
  s.addShape("rect", { x: 3.5, y: 2.5, w: 3, h: 0.02, fill: { color: C.ACCENT } });

  // CTA
  addT(s, "我们希望下一步获得", 0, 2.8, 10, 0.4, { fontSize: 16, color: C.WHITE, align: "center" });
  addT(s, "企业场景对接 · 校内试用 · 实习就业面谈", 0, 3.2, 10, 0.5, { fontSize: 22, bold: true, color: C.ACCENT, align: "center" });
  addT(s, "让启途继续完善、真正落地", 0, 3.8, 10, 0.35, { fontSize: 14, color: C.DARK_TEXT, align: "center" });

  // Thanks
  addT(s, "感谢各位老师聆听  恳请批评指正", 0, 4.5, 10, 0.4, { fontSize: 14, color: C.WHITE, align: "center" });

  // Cat - use xiaoju-full.jpg, properly sized with contain
  addImg(s, `${AS}/xiaoju-full.jpg`, 8.0, 3.8, 1.6, 1.6);

  addT(s, "团队成员：曾怡嫚 | 申梓淼 | 牛保康", 0.6, 5.2, 5, 0.25, { fontSize: 10, color: "6B8CAE" });
}

// ===== SAVE =====
const outPath = "/Users/wendao/Desktop/启途-结项路演PPT.pptx";
pres.writeFile({ fileName: outPath }).then(() => {
  console.log("✅ PPT saved: " + outPath);
}).catch(err => {
  console.error("❌ Error:", err);
});
