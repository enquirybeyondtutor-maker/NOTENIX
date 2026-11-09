// Render every $...$ / $$...$$ in the exam-engine content (all exams) with KaTeX (as MathText does) and report errors.
// Run from frontend/:  node ../backend/exam_content/_katex_check.js
const fs = require("fs");
const path = require("path");
const katex = require(path.resolve("node_modules/katex"));

const MATH = /\$\$([\s\S]+?)\$\$|\$(?![\s$])((?:\\.|[^$\\\n])+?)(?<!\s)\$(?!\d)/g;
const dir = path.resolve(__dirname);
const files = [];
(function scan(d) { for (const e of fs.readdirSync(d, { withFileTypes: true })) { if (e.isDirectory()) scan(path.join(d, e.name)); else if (e.name.endsWith(".json")) files.push(path.join(d, e.name)); } })(dir);
let n = 0, bad = 0;
function walk(v, where) {
  if (typeof v === "string") {
    for (const m of v.matchAll(MATH)) {
      n++;
      try { katex.renderToString(m[1] ?? m[2], { throwOnError: true, displayMode: m[1] != null }); }
      catch (e) { bad++; console.log(`${where}: ${e.message.split("\n")[0]}  in  ${(m[1] ?? m[2]).slice(0, 60)}`); }
    }
  } else if (Array.isArray(v)) v.forEach((x, i) => walk(x, where));
  else if (v && typeof v === "object") for (const [k, x] of Object.entries(v)) walk(x, v.id ? `${v.id}.${k}` : where);
}
for (const f of files) walk(JSON.parse(fs.readFileSync(f, "utf8")), path.relative(dir, f));
console.log(`${n} maths expressions checked, ${bad} problems`);
