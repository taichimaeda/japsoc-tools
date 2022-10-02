const res = [];
document.querySelectorAll('ruby').forEach(e => {
    const rb = e.querySelector('rb');
    const rt = e.querySelector('rt');
    res.push(`${rb.innerText}（${rt.innerText}）\n`);
});

const blob = new Blob(res, { type: "text/plain;charset=utf-8" });
const a = document.createElement('a');
a.href = URL.createObjectURL(blob);
a.download = 'temp';
document.body.appendChild(a);
a.click();