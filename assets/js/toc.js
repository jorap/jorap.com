// Unified anchor link handler for the entire site
document.addEventListener('DOMContentLoaded', function () {
    // Function to get the current header height dynamically
    function getHeaderOffset() {
        const header = document.querySelector('.header.sticky');
        if (header) {
            // Get the actual header height including padding and content
            const headerHeight = header.offsetHeight;
            // Add some extra padding for better visual spacing
            return headerHeight + 20;
        }
        // Fallback if header not found
        return 100;
    }

    // Handle all anchor links on the page
    function handleAnchorLinks() {
        // Get all anchor links that point to elements on the same page
        const anchorLinks = document.querySelectorAll('a[href^="#"]:not([href="#"])');

        anchorLinks.forEach(link => {
            link.addEventListener('click', function (e) {
                const targetId = this.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);

                if (targetElement) {
                    e.preventDefault();

                    // Calculate offset dynamically based on current header height
                    const offset = getHeaderOffset();
                    window.scrollTo({
                        top: targetElement.offsetTop - offset,
                        behavior: 'smooth'
                    });

                    // Update URL hash without triggering scroll
                    if (history.pushState) {
                        history.pushState(null, null, '#' + targetId);
                    } else {
                        // Fallback for older browsers
                        location.hash = '#' + targetId;
                    }
                }
            });
        });
    }

    // Handle anchor links in table of contents specifically
    function handleTocSpecificFeatures() {
        const tableOfContent = document.querySelector('.table-of-content');

        if (tableOfContent) {
            const tocLinks = tableOfContent.querySelectorAll('a[href^="#"]');

            // Get mobile TOC elements for blog pages
            const mobileTocContent = document.querySelector('.mobile-toc-content');
            const tocChevron = document.getElementById('toc-chevron');

            // Add additional TOC-specific functionality
            tocLinks.forEach(link => {
                link.addEventListener('click', function () {
                    // Remove bold from all TOC links
                    tocLinks.forEach(l => l.classList.remove('font-bold'));
                    // Make clicked link bold
                    this.classList.add('font-bold');

                    // On mobile, close the TOC after clicking a link (blog-specific)
                    if (window.innerWidth < 1024 && mobileTocContent) {
                        mobileTocContent.classList.add('hidden');
                        if (tocChevron) tocChevron.classList.remove('rotate-180');
                    }
                });
            });
        }
    }

    // Initialize both handlers
    handleAnchorLinks();
    handleTocSpecificFeatures();

    // Handle direct anchor navigation on page load with dynamic offset
    if (window.location.hash) {
        setTimeout(() => {
            const targetElement = document.getElementById(window.location.hash.substring(1));
            if (targetElement) {
                const offset = getHeaderOffset();
                window.scrollTo({
                    top: targetElement.offsetTop - offset,
                    behavior: 'smooth'
                });
            }
        }, 100);
    }

    // Handle window resize to recalculate offsets if needed
    let resizeTimeout;
    window.addEventListener('resize', function () {
        // Debounce resize events
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            // If there's a hash in the URL, re-scroll to maintain correct position
            if (window.location.hash) {
                const targetElement = document.getElementById(window.location.hash.substring(1));
                if (targetElement) {
                    const offset = getHeaderOffset();
                    window.scrollTo({
                        top: targetElement.offsetTop - offset,
                        behavior: 'smooth'
                    });
                }
            }
        }, 150);
    });
});