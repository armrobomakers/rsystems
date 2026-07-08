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

if (topbar) {
  let lastY = window.scrollY;
  let ticking = false;

  const updateTopbar = () => {
    const currentY = window.scrollY;
    const scrolled = currentY > 24;
    const directionDown = currentY > lastY;

    document.body.classList.toggle("is-scrolled", scrolled);
    document.body.classList.toggle("is-scrolling-down", directionDown && scrolled);

    lastY = currentY;
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

  updateTopbar();
}
