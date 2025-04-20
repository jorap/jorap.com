// main script
(function () {
  "use strict";

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
    }
  });

  dropdownMenuToggler.forEach((toggler) => {
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
