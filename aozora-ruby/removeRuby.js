document.querySelectorAll('ruby').forEach(e => {
    const rb = e.querySelector('rb');
    e.outerHTML = rb.innerHTML;
});