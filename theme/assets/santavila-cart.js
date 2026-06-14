/* SANTAVILA · Aceptación obligatoria de políticas en el carrito.
   Bloquea "Finalizar compra" y el pago acelerado hasta marcar el checkbox.
   Robusto ante el re-render AJAX del carrito (página /cart + drawer). */
(function () {
  function bindAll() {
    document.querySelectorAll('[data-sv-cart-terms]').forEach(function (wrap) {
      var check = wrap.querySelector('.sv-cart-terms__check');
      var ctas = wrap.closest('.cart__ctas') || wrap.parentElement;
      if (!check || !ctas) return;
      var btn = ctas.querySelector('button[name="checkout"]');
      var accel = ctas.querySelector('.additional-checkout-buttons');
      if (!btn) return;
      function sync() {
        var ok = !!check.checked;
        btn.disabled = !ok;
        btn.setAttribute('aria-disabled', String(!ok));
        if (accel) {
          accel.style.pointerEvents = ok ? '' : 'none';
          accel.style.opacity = ok ? '' : '0.45';
          accel.setAttribute('aria-hidden', String(!ok));
        }
      }
      if (!check.dataset.svBound) {
        check.dataset.svBound = '1';
        check.addEventListener('change', sync);
      }
      sync();
    });
  }
  function run() { requestAnimationFrame(bindAll); }
  if (document.readyState !== 'loading') run(); else document.addEventListener('DOMContentLoaded', run);
  document.addEventListener('cart:update', run);
  var pending = false;
  try {
    new MutationObserver(function () {
      if (pending) return;
      pending = true;
      requestAnimationFrame(function () { pending = false; bindAll(); });
    }).observe(document.body, { childList: true, subtree: true });
  } catch (e) {}
})();
