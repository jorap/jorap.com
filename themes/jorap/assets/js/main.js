// main script
(function () {
  "use strict";

  const syncDropdownAria = () => {
    document.querySelectorAll(".nav-dropdown").forEach((item) => {
      const toggler = item.querySelector(":scope > .nav-link");
      if (!toggler) return;
      toggler.setAttribute(
        "aria-expanded",
        item.classList.contains("active") ? "true" : "false",
      );
    });
  };

  // Mobile menu: sync aria-expanded, close after navigation, Escape
  const navToggle = document.getElementById("nav-toggle");
  const navMenu = document.getElementById("nav-menu");
  const navToggleLabel = document.getElementById("nav-toggle-label");
  if (navToggle && navMenu && navToggleLabel) {
    const syncNavOpen = () => {
      navToggleLabel.setAttribute(
        "aria-expanded",
        navToggle.checked ? "true" : "false",
      );
    };
    navToggle.addEventListener("change", syncNavOpen);
    syncNavOpen();

    navMenu.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        navToggle.checked = false;
        syncNavOpen();
      });
    });

    document.addEventListener("keydown", (e) => {
      if (e.key !== "Escape") return;
      if (navToggle.checked) {
        navToggle.checked = false;
        syncNavOpen();
      }
      document.querySelectorAll(".nav-dropdown.active").forEach((item) => {
        item.classList.remove("active");
      });
      syncDropdownAria();
    });
  }

  // Dropdown Menu Toggler For Mobile and Tablet
  // ----------------------------------------
  const dropdownMenuToggler = document.querySelectorAll(
    ".nav-dropdown > .nav-link",
  );

  // Close other active dropdowns when one is opened
  const closeOtherDropdowns = (currentItem) => {
    const activeItems = document.querySelectorAll(".nav-dropdown.active");
    activeItems.forEach((item) => {
      if (item !== currentItem && item.classList.contains("active")) {
        item.classList.remove("active");
      }
    });
  };

  // Close dropdown when clicking outside
  document.addEventListener("click", (e) => {
    if (!e.target.closest(".nav-dropdown")) {
      const activeItems = document.querySelectorAll(".nav-dropdown.active");
      activeItems.forEach((item) => {
        item.classList.remove("active");
      });
      syncDropdownAria();
    }
  });

  dropdownMenuToggler.forEach((toggler) => {
    toggler.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        toggler.click();
      }
    });

    toggler?.addEventListener("click", (e) => {
      e.preventDefault();
      const navItem = e.target.closest(".nav-item");

      // Toggle active class
      if (navItem.classList.contains("active")) {
        navItem.classList.remove("active");
      } else {
        closeOtherDropdowns(navItem);
        navItem.classList.add("active");
      }
      syncDropdownAria();
    });
  });

  // Testimonial Slider
  // ----------------------------------------
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
})();
