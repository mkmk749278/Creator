// print phrase times for a scene: node _tools/cuet.js <scene> <line> "phrase" ...
const fs = require("fs"); global.window = global;
eval(fs.readFileSync(process.argv[2] + "/cues.js", "utf8")); eval(fs.readFileSync("_shared/kav.js", "utf8"));
const id = process.argv[3]; console.log("D", window.CUES.duration, window.CUES.cues[id]);
for (const p of process.argv.slice(4)) console.log(p, window.at(id, p).toFixed(2));
