/* SANTAVILA · PDP interactions */
(function(){
  // Option selection (color swatch + size)
  document.querySelectorAll('[data-group]').forEach(function(g){
    g.querySelectorAll('.sw, .size').forEach(function(el){
      el.addEventListener('click', function(){
        g.querySelectorAll('.sw, .size').forEach(function(s){ s.classList.remove('on'); });
        el.classList.add('on');
        if (g.dataset.group==='color' && el.dataset.label){
          var v = document.querySelector('[data-color-val]'); if(v) v.textContent = el.dataset.label;
        }
        if (g.dataset.group==='size' && el.dataset.price){
          var add = document.querySelector('[data-add-price]'); if(add) add.textContent = el.dataset.price;
          var sb = document.querySelector('[data-sticky-price]'); if(sb) sb.textContent = el.dataset.price;
          var main = document.querySelector('[data-main-price]'); if(main) main.textContent = el.dataset.price;
        }
      });
    });
  });

  // Gallery
  var stage = document.querySelector('[data-stage]');
  document.querySelectorAll('.gthumb').forEach(function(t){
    t.addEventListener('click', function(){
      document.querySelectorAll('.gthumb').forEach(function(s){ s.classList.remove('on'); });
      t.classList.add('on');
    });
  });

  // QTY
  document.querySelectorAll('[data-qty]').forEach(function(q){
    var val = q.querySelector('span'); var n = 1;
    q.querySelectorAll('button').forEach(function(b){
      b.addEventListener('click', function(){
        n = Math.max(1, n + (b.dataset.dir==='up'?1:-1)); val.textContent = n;
      });
    });
  });

  // Accordions
  document.querySelectorAll('.acc__head').forEach(function(h){
    h.addEventListener('click', function(){
      var item = h.closest('.acc__item');
      var panel = item.querySelector('.acc__panel');
      var open = item.classList.contains('open');
      if (open){ item.classList.remove('open'); panel.style.maxHeight = 0; }
      else { item.classList.add('open'); panel.style.maxHeight = panel.scrollHeight + 'px'; }
    });
  });

  // Sticky add bar
  var bar = document.querySelector('.stickybar');
  var anchor = document.querySelector('[data-buy]');
  if (bar && anchor && 'IntersectionObserver' in window){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (e.boundingClientRect.top < 0 && !e.isIntersecting){ bar.classList.add('show'); }
        else if (e.isIntersecting){ bar.classList.remove('show'); }
      });
    }, { rootMargin:'-80px 0px 0px 0px', threshold:0 });
    io.observe(anchor);
  }

  // Size guide modal
  var modal = document.querySelector('.modal');
  document.querySelectorAll('[data-open-guide]').forEach(function(b){
    b.addEventListener('click', function(e){ e.preventDefault(); modal && modal.classList.add('open'); document.body.style.overflow='hidden'; });
  });
  if (modal){
    function close(){ modal.classList.remove('open'); document.body.style.overflow=''; }
    modal.querySelector('.modal__bg').addEventListener('click', close);
    modal.querySelector('.modal__close').addEventListener('click', close);
    document.addEventListener('keydown', function(e){ if(e.key==='Escape') close(); });
  }
})();
