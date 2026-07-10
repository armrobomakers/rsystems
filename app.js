const yearNode = document.getElementById("year");

if (yearNode) {
  yearNode.textContent = "© 2024 R Systems";
}

const revealNodes = document.querySelectorAll(".reveal");

if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      }
    },
    {
      threshold: 0.15,
      rootMargin: "0px 0px -8% 0px",
    },
  );

  revealNodes.forEach((node) => observer.observe(node));
} else {
  revealNodes.forEach((node) => node.classList.add("visible"));
}

const topbar = document.querySelector(".topbar");
const menuToggle = document.querySelector(".menu-toggle");
const mobileMenu = document.getElementById("mobile-menu");

if (topbar) {
  const setMenuOpen = (open) => {
    topbar.classList.toggle("is-menu-open", open);
    if (menuToggle) {
      menuToggle.setAttribute("aria-expanded", open ? "true" : "false");
    }
    if (mobileMenu) {
      mobileMenu.setAttribute("aria-hidden", open ? "false" : "true");
    }
  };

  if (menuToggle) {
    menuToggle.addEventListener("click", () => {
      setMenuOpen(!topbar.classList.contains("is-menu-open"));
    });
  }

  if (mobileMenu) {
    mobileMenu.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => setMenuOpen(false));
    });
  }

  let ticking = false;
  let hidden = false;

  const updateTopbar = () => {
    const currentY = window.scrollY;
    const isCompact = window.innerWidth <= 900;
    hidden = !isCompact && currentY > 24 && !topbar.classList.contains("is-menu-open");

    document.body.classList.toggle("is-header-hidden", hidden);
    ticking = false;
  };

  window.addEventListener(
    "scroll",
    () => {
      if (!ticking) {
        window.requestAnimationFrame(updateTopbar);
        ticking = true;
      }
    },
    { passive: true },
  );

  window.addEventListener("resize", () => {
    if (window.innerWidth > 900) {
      setMenuOpen(false);
    }
    updateTopbar();
  });

  updateTopbar();
}
