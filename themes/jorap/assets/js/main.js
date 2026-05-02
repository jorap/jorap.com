// main script
(function () {
  "use strict";

  // Dropdown Menu Toggler For Mobile and Tablet
  // ----------------------------------------
  const dropdownTriggers = document.querySelectorAll(".nav-dropdown-trigger");

  const setDropdownExpanded = (navItem, expanded) => {
    const btn = navItem?.querySelector(".nav-dropdown-trigger");
    if (btn) btn.setAttribute("aria-expanded", expanded ? "true" : "false");
  };

  const closeAllDropdowns = () => {
    document.querySelectorAll(".nav-dropdown.active").forEach((item) => {
      item.classList.remove("active");
      setDropdownExpanded(item, false);
    });
  };

  document.addEventListener("click", (e) => {
    if (!e.target.closest(".nav-dropdown")) {
      closeAllDropdowns();
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    closeAllDropdowns();
  });

  dropdownTriggers.forEach((toggler) => {
    toggler?.addEventListener("click", (e) => {
      e.preventDefault();
      const navItem = e.target.closest(".nav-item");
      if (!navItem) return;

      const isOpen = navItem.classList.contains("active");
      if (isOpen) {
        navItem.classList.remove("active");
        setDropdownExpanded(navItem, false);
        return;
      }

      document.querySelectorAll(".nav-dropdown.active").forEach((item) => {
        if (item !== navItem) {
          item.classList.remove("active");
          setDropdownExpanded(item, false);
        }
      });
      navItem.classList.add("active");
      setDropdownExpanded(navItem, true);
    });
  });

  // Testimonial Slider
  // ----------------------------------------
  const testimonialRoot = document.querySelector(".testimonial-slider");
  if (testimonialRoot) {
    new Swiper(".testimonial-slider", {
      spaceBetween: 24,
      loop: true,
      pagination: {
        el: ".testimonial-slider-pagination",
        type: "bullets",
        clickable: true,
      },
      breakpoints: {
        768: {
          slidesPerView: 2,
        },
        992: {
          slidesPerView: 3,
        },
      },
    });
  }
})();
