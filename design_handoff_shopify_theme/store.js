/* SANTAVILA · Tienda · interacciones */
(function () {
  // Reveal/entrance is handled in CSS (clock-driven animation), so it can
  // never leave content hidden in environments where IntersectionObserver
  // or class-toggled transitions misbehave.

  // ---- Header state (transparent over hero -> solid) ----
  const hdr = document.querySelector(".hdr");
  const hero = document.querySelector("[data-hero]");
  if (hdr && !hero) {
    // Light pages (PDP/Collection grids without a hero): always solid.
    hdr.classList.add("hdr--solid");
  } else if (hdr && hero) {
    const onScroll = () => {
      const trigger = Math.max(hero.offsetHeight - 90, 60);
      if (window.scrollY > trigger) {
        hdr.classList.add("hdr--solid");
        hdr.classList.remove("hdr--over");
      } else {
        hdr.classList.remove("hdr--solid");
        hdr.classList.add("hdr--over");
      }
    };
    hdr.classList.add("hdr--over");
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    window.addEventListener("load", () => requestAnimationFrame(onScroll));
  }

  // ---- Mobile menu ----
  const burger = document.querySelector("[data-burger]");
  const mnav = document.querySelector(".mnav");
  const mclose = document.querySelector("[data-mclose]");
  if (burger && mnav) {
    const open = () => { mnav.classList.add("open"); document.body.style.overflow = "hidden"; };
    const close = () => { mnav.classList.remove("open"); document.body.style.overflow = ""; };
    burger.addEventListener("click", open);
    mclose && mclose.addEventListener("click", close);
    mnav.querySelectorAll("a").forEach((a) => a.addEventListener("click", close));
  }

  // ---- Subtle hero parallax ----
  const heroImg = document.querySelector("[data-hero] image-slot");
  if (heroImg && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    window.addEventListener("scroll", () => {
      const y = Math.min(window.scrollY, window.innerHeight);
      heroImg.style.transform = "translateY(" + y * 0.18 + "px) scale(1.06)";
    }, { passive: true });
  }
})();
