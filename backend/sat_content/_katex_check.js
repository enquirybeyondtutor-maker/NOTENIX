// Render every $...$ / $$...$$ in the SAT forms with KaTeX (as MathText does) and report errors.
// Run from frontend/:  node ../backend/sat_content/_katex_check.js
const fs = require("fs");
const path = require("path");
const katex = require(path.resolve("node_modules/katex"));

const MATH = /\$\$([\s\S]+?)\$\$|\$(?![\s$])((?:\\.|[^$\\\n])+?)(?<!\s)\$(?!\d)/g;
const dir = path.resolve(__dirname);
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
for (const f of fs.readdirSync(dir).filter((f) => f.endsWith(".json"))) walk(JSON.parse(fs.readFileSync(path.join(dir, f), "utf8")), f);
console.log(`${n} maths expressions checked, ${bad} problems`);
