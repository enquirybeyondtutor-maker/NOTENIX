// Tell Bing (and Yahoo/DuckDuckGo/Yandex via IndexNow) about every page in the live sitemap.
// Run after a deploy that adds or changes public pages:  npm run indexnow
const HOST = "www.notenix.com";
const KEY = "e3fcd846394f4a20abada001d507e32a"; // served at /<KEY>.txt from public/

const xml = await (await fetch(`https://${HOST}/sitemap.xml`)).text();
const urlList = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);

const res = await fetch("https://api.indexnow.org/indexnow", {
  method: "POST",
  headers: { "Content-Type": "application/json; charset=utf-8" },
  body: JSON.stringify({ host: HOST, key: KEY, keyLocation: `https://${HOST}/${KEY}.txt`, urlList }),
});
console.log(`IndexNow: ${res.status} ${res.statusText} for ${urlList.length} URLs`);
if (res.status >= 400) process.exit(1);
