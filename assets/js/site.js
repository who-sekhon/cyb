const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

const revealNodes = document.querySelectorAll("[data-reveal]");

if (!prefersReducedMotion && "IntersectionObserver" in window && revealNodes.length > 0) {
  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          revealObserver.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.15,
    },
  );

  revealNodes.forEach((node) => revealObserver.observe(node));
} else {
  revealNodes.forEach((node) => node.classList.add("is-visible"));
}

const progressBar = document.querySelector("[data-progress-bar]");

if (progressBar) {
  const updateProgressBar = () => {
    const scrollTop = window.scrollY;
    const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
    const progress = maxScroll > 0 ? (scrollTop / maxScroll) * 100 : 0;
    progressBar.style.width = `${Math.min(progress, 100)}%`;
  };

  updateProgressBar();
  window.addEventListener("scroll", updateProgressBar, { passive: true });
  window.addEventListener("resize", updateProgressBar);
}

const tocLinks = Array.from(document.querySelectorAll(".toc-list a"));
const sections = Array.from(document.querySelectorAll("[data-section]"));

if ("IntersectionObserver" in window && tocLinks.length > 0 && sections.length > 0) {
  const linkMap = new Map(
    tocLinks.map((link) => [link.getAttribute("href")?.replace("#", ""), link]),
  );

  const sectionObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) {
          return;
        }

        const id = entry.target.getAttribute("id");
        tocLinks.forEach((link) => link.classList.remove("is-active"));
        linkMap.get(id)?.classList.add("is-active");
      });
    },
    {
      rootMargin: "-28% 0px -55% 0px",
      threshold: 0.05,
    },
  );

  sections.forEach((section) => sectionObserver.observe(section));
}

const lightbox = document.querySelector("[data-lightbox]");
const lightboxImage = document.querySelector("[data-lightbox-image]");
const lightboxCaption = document.querySelector("[data-lightbox-caption]");
const lightboxTriggers = Array.from(document.querySelectorAll("[data-lightbox-src]"));
const lightboxCloseButtons = Array.from(document.querySelectorAll("[data-lightbox-close]"));

if (lightbox && lightboxImage && lightboxCaption && lightboxTriggers.length > 0) {
  let lastFocusedElement = null;

  const closeLightbox = () => {
    lightbox.hidden = true;
    document.body.style.overflow = "";
    if (lastFocusedElement instanceof HTMLElement) {
      lastFocusedElement.focus();
    }
  };

  const openLightbox = (trigger) => {
    const src = trigger.getAttribute("data-lightbox-src");
    const caption = trigger.getAttribute("data-lightbox-alt") ?? "";

    if (!src) {
      return;
    }

    lastFocusedElement = trigger;
    lightboxImage.src = src;
    lightboxImage.alt = caption;
    lightboxCaption.textContent = caption;
    lightbox.hidden = false;
    document.body.style.overflow = "hidden";
    lightbox.querySelector(".lightbox-close")?.focus();
  };

  lightboxTriggers.forEach((trigger) => {
    trigger.addEventListener("click", () => openLightbox(trigger));
  });

  lightboxCloseButtons.forEach((button) => {
    button.addEventListener("click", closeLightbox);
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !lightbox.hidden) {
      closeLightbox();
    }
  });
}
