// Renders every $...$ in the KS3 content with KaTeX (strict) and reports anything that fails.
// Run from the frontend folder so katex resolves: node ../backend/ks3_content/_katex_check.js
const fs = require("fs");
const path = require("path");
const katex = require("katex");

const root = __dirname;
let checked = 0, bad = 0;
for (const dir of ["tests", "notes"]) {
  for (const f of fs.readdirSync(path.join(root, dir))) {
    const data = JSON.parse(fs.readFileSync(path.join(root, dir, f), "utf8"));
    const texts = dir === "notes" ? [data.body] : data.questions.flatMap((q) => [q.question, q.explanation, ...q.options]);
    for (const t of texts) {
      for (const m of t.matchAll(/\$([^$]+)\$/g)) {
        checked++;
        try { katex.renderToString(m[1], { throwOnError: true }); }
        catch (e) { bad++; console.log(`${dir}/${f}: ${m[1]}  ->  ${e.message.slice(0, 90)}`); }
      }
      if ((t.match(/\$/g) || []).length % 2) { bad++; console.log(`${dir}/${f}: odd number of $ in: ${t.slice(0, 70)}`); }
    }
  }
}
console.log(`checked ${checked} formulas, ${bad} problems`);
process.exit(bad ? 1 : 0);
