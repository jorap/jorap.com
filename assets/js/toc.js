// Table of Contents scroll offset handler
document.addEventListener('DOMContentLoaded', function () {
    // Check if table of contents exists on the page
    const tableOfContent = document.querySelector('.table-of-content');

    // Only proceed if the table of content element exists
    if (tableOfContent) {
        // Get all links in the table of contents
        const tocLinks = document.querySelectorAll('.table-of-content a');

        // Add click event listeners to each link
        tocLinks.forEach(link => {
            link.addEventListener('click', function (e) {
                e.preventDefault();

                // Get the target element from the href attribute
                const targetId = this.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);

                if (targetElement) {
                    // Calculate header height - get the actual header element
                    const header = document.querySelector('.header.sticky');
                    const headerHeight = header ? header.offsetHeight : 0;

                    // Calculate the element's position relative to the viewport
                    const elementPosition = targetElement.getBoundingClientRect().top;
                    // Calculate the absolute position and adjust for header height
                    const offsetPosition = elementPosition + window.pageYOffset - headerHeight - 20; // 20px additional padding

                    // Smooth scroll to the element
                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }
});