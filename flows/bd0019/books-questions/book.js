(function () {
  var book = document.getElementById('book');
  var pages = Array.prototype.slice.call(document.querySelectorAll('.page'));
  var dots = Array.prototype.slice.call(document.querySelectorAll('.dots i'));
  var cur = 0;
  function mark(i) { cur = i; dots.forEach(function (d, j) { d.classList.toggle('on', j === i); }); }
  mark(0);
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) mark(pages.indexOf(e.target)); });
    }, { root: book, threshold: 0.55 });
    pages.forEach(function (p) { io.observe(p); });
  }
  var smooth = !(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  function go(i) {
    i = Math.max(0, Math.min(pages.length - 1, i));
    pages[i].scrollIntoView({ behavior: smooth ? 'smooth' : 'auto', block: 'start' });
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowDown' || e.key === 'ArrowRight' || e.key === 'PageDown') { e.preventDefault(); go(cur + 1); }
    else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); go(cur - 1); }
  });
  try { book.focus({ preventScroll: true }); } catch (e) {}
})();
