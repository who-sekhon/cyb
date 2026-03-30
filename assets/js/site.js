const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const revealAllOnLoad = Boolean(window.location.hash);
const shouldAnimateReveal = document.body?.classList.contains("page-home");

const revealNodes = document.querySelectorAll("[data-reveal]");

if (
  shouldAnimateReveal &&
  !prefersReducedMotion &&
  !revealAllOnLoad &&
  "IntersectionObserver" in window &&
  revealNodes.length > 0
) {
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
const lightboxDialog = lightbox?.querySelector(".lightbox-dialog") ?? null;
const lightboxImage = document.querySelector("[data-lightbox-image]");
const lightboxCaption = document.querySelector("[data-lightbox-caption]");
const lightboxPrevButton = document.querySelector("[data-lightbox-prev]");
const lightboxNextButton = document.querySelector("[data-lightbox-next]");
const lightboxTriggers = Array.from(document.querySelectorAll("[data-lightbox-src]"));
const lightboxCloseButtons = Array.from(document.querySelectorAll("[data-lightbox-close]"));

if (
  lightbox instanceof HTMLElement &&
  lightboxDialog instanceof HTMLElement &&
  lightboxImage instanceof HTMLImageElement &&
  lightboxCaption instanceof HTMLElement &&
  lightboxTriggers.length > 0
) {
  let lastFocusedElement = null;
  let currentIndex = -1;

  const focusableSelector =
    'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';

  const getFocusableElements = () =>
    Array.from(lightboxDialog.querySelectorAll(focusableSelector)).filter(
      (element) => element instanceof HTMLElement && !element.hasAttribute("hidden"),
    );

  const renderFigure = (index) => {
    if (lightboxTriggers.length === 0) {
      return;
    }

    currentIndex = (index + lightboxTriggers.length) % lightboxTriggers.length;
    const trigger = lightboxTriggers[currentIndex];
    const src = trigger.getAttribute("data-lightbox-src");
    const caption = trigger.getAttribute("data-lightbox-alt") ?? "";

    if (!src) {
      return;
    }

    lightboxImage.src = src;
    lightboxImage.alt = caption;
    lightboxCaption.textContent = caption;

    if (lightboxPrevButton instanceof HTMLButtonElement) {
      lightboxPrevButton.disabled = lightboxTriggers.length < 2;
    }

    if (lightboxNextButton instanceof HTMLButtonElement) {
      lightboxNextButton.disabled = lightboxTriggers.length < 2;
    }
  };

  const closeLightbox = () => {
    lightbox.hidden = true;
    lightbox.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
    if (lastFocusedElement instanceof HTMLElement) {
      lastFocusedElement.focus();
    }
  };

  const openLightboxAt = (index) => {
    lastFocusedElement = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    renderFigure(index);
    lightbox.hidden = false;
    lightbox.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    lightboxDialog.focus();
  };

  const moveLightbox = (direction) => {
    if (lightboxTriggers.length < 2) {
      return;
    }
    renderFigure(currentIndex + direction);
  };

  const trapFocus = (event) => {
    if (event.key !== "Tab" || lightbox.hidden) {
      return;
    }

    const focusableElements = getFocusableElements();

    if (focusableElements.length === 0) {
      event.preventDefault();
      lightboxDialog.focus();
      return;
    }

    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];

    if (event.shiftKey && document.activeElement === firstElement) {
      event.preventDefault();
      lastElement.focus();
    } else if (!event.shiftKey && document.activeElement === lastElement) {
      event.preventDefault();
      firstElement.focus();
    }
  };

  lightboxTriggers.forEach((trigger, index) => {
    trigger.addEventListener("click", () => openLightboxAt(index));
  });

  lightboxCloseButtons.forEach((button) => {
    button.addEventListener("click", closeLightbox);
  });

  if (lightboxPrevButton instanceof HTMLButtonElement) {
    lightboxPrevButton.addEventListener("click", () => moveLightbox(-1));
  }

  if (lightboxNextButton instanceof HTMLButtonElement) {
    lightboxNextButton.addEventListener("click", () => moveLightbox(1));
  }

  document.addEventListener("keydown", (event) => {
    if (lightbox.hidden) {
      return;
    }

    if (event.key === "Escape") {
      closeLightbox();
      return;
    }

    if (event.key === "ArrowLeft") {
      moveLightbox(-1);
      return;
    }

    if (event.key === "ArrowRight") {
      moveLightbox(1);
      return;
    }

    trapFocus(event);
  });
}
