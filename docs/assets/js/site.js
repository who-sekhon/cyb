const revealNodes = document.querySelectorAll("[data-reveal]");

if ("IntersectionObserver" in window && revealNodes.length > 0) {
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
