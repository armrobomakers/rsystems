const yearNode = document.getElementById("year");

if (yearNode) {
  yearNode.textContent = "\u00A9 2024 R Systems";
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

document
  .querySelectorAll(".orb, .grain, .hero-benefits i, .meta-icon, .service-icon, .panel-scene, .case-visual, .avatar, .status-dot")
  .forEach((node) => {
    node.setAttribute("aria-hidden", "true");
  });

if (topbar) {
  let isMenuOpen = false;
  let ticking = false;
  let lastScrollY = window.scrollY;
  let headerHidden = false;
  let previousBodyOverflow = "";

  const setMenuOpen = (open, { returnFocus = false } = {}) => {
    if (open === isMenuOpen) {
      if (!open && returnFocus && menuToggle) {
        menuToggle.focus({ preventScroll: true });
      }
      return;
    }

    isMenuOpen = open;
    topbar.classList.toggle("is-menu-open", open);
    document.body.classList.toggle("is-menu-open", open);

    if (open) {
      previousBodyOverflow = document.body.style.overflow;
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = previousBodyOverflow;
    }

    if (menuToggle) {
      menuToggle.setAttribute("aria-expanded", open ? "true" : "false");
    }

    if (mobileMenu) {
      mobileMenu.setAttribute("aria-hidden", open ? "false" : "true");
      mobileMenu.toggleAttribute("inert", !open);
    }

    if (!open && returnFocus && menuToggle) {
      menuToggle.focus({ preventScroll: true });
    }

    if (open) {
      document.body.classList.remove("is-header-hidden");
    }
  };

  if (menuToggle) {
    menuToggle.addEventListener("click", () => {
      setMenuOpen(!isMenuOpen);
    });
  }

  if (mobileMenu) {
    mobileMenu.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        setMenuOpen(false);
        window.setTimeout(() => {
          menuToggle?.focus({ preventScroll: true });
        }, 0);
      });
    });
  }

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      setMenuOpen(false, { returnFocus: true });
    }
  });

  document.addEventListener("click", (event) => {
    if (isMenuOpen && !topbar.contains(event.target)) {
      setMenuOpen(false, { returnFocus: true });
    }
  });

  const updateTopbar = () => {
    const currentY = window.scrollY;
    const isCompact = window.innerWidth <= 900;

    if (isCompact || isMenuOpen || currentY <= 36) {
      headerHidden = false;
    } else if (currentY > lastScrollY + 8 && currentY > 96) {
      headerHidden = true;
    } else if (currentY < lastScrollY - 6) {
      headerHidden = false;
    }

    document.body.classList.toggle("is-header-hidden", headerHidden);
    lastScrollY = currentY;
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
      setMenuOpen(false, { returnFocus: true });
    }

    lastScrollY = window.scrollY;
    updateTopbar();
  });

  updateTopbar();
}
