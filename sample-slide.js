const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "小咪";

// ── 可爱配色 ──
const C = {
  bg: "FFF5F7",      // 粉白底
  primary: "FF8FAB", // 主粉
  secondary: "C084FC", // 紫
  accent: "FDE68A",  // 暖黄
  circle: "FFD6E0",  // 浅粉圆
  text: "4A1942",    // 深紫文字
  light: "FFE4EC",   // 浅粉
  white: "FFFFFF",
};

// ══════════════ 封面页 ══════════════
const slide = pres.addSlide();
slide.background = { color: C.bg };

// 装饰大圆（背景）
slide.addShape(pres.shapes.OVAL, {
  x: -1.5, y: -1.5, w: 4, h: 4,
  fill: { color: C.circle, transparency: 40 },
});
slide.addShape(pres.shapes.OVAL, {
  x: 7.5, y: 3.5, w: 3.5, h: 3.5,
  fill: { color: C.accent, transparency: 50 },
});

// 主标题卡片（白色圆角）
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 0.8, y: 0.8, w: 8.4, h: 1.2,
  fill: { color: C.white },
  shadow: { type: "outer", color: "FF8FAB", blur: 12, offset: 3, angle: 135, opacity: 0.15 },
  rectRadius: 0.15,
});

// 标题左侧装饰条
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.8, y: 0.8, w: 0.08, h: 1.2,
  fill: { color: C.primary },
});

slide.addText("✨ 我们的 AI 面试助手之旅", {
  x: 1.1, y: 0.85, w: 7.8, h: 1.1,
  fontSize: 28, fontFace: "Arial", color: C.text, bold: true,
  margin: 0, valign: "middle",
});

// 可爱小人 + 副标题区
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 0.8, y: 2.3, w: 8.4, h: 2.8,
  fill: { color: C.white },
  shadow: { type: "outer", color: "C084FC", blur: 10, offset: 2, angle: 135, opacity: 0.1 },
  rectRadius: 0.15,
});

slide.addText("🎯 多模态模拟面试评测智能体", {
  x: 1.2, y: 2.5, w: 7.5, h: 0.7,
  fontSize: 20, fontFace: "Arial", color: C.text,
  bold: true, margin: 0,
});

slide.addText([
  { text: "从零到一，构建一个完整的 AI 面试辅助系统", options: { breakLine: true, fontSize: 14, color: "888888" } },
  { text: "", options: { breakLine: true, fontSize: 8 } },
  { text: "💡 Vue 3 + FastAPI + SQLite + AI API", options: { fontSize: 13, color: C.primary, bold: true } },
], {
  x: 1.2, y: 3.3, w: 7.5, h: 1.5,
  fontFace: "Arial", margin: 0, valign: "top",
});

// 底部装饰小标签
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 0.8, y: 5.4, w: 8.4, h: 0.5,
  fill: { color: C.light },
  rectRadius: 0.1,
});

slide.addText("👤 曾怡嫚 · AI+X 实验班 P28 · 科大讯飞合作项目", {
  x: 1.2, y: 5.4, w: 7.8, h: 0.5,
  fontSize: 11, color: "999999", fontFace: "Arial",
  margin: 0, valign: "middle",
});

// 输出
pres.writeFile({ fileName: "/Users/wendao/interview-agent/sample-slide.pptx" })
  .then(() => console.log("✅ 样张生成成功！"));