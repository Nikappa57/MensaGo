document.addEventListener('DOMContentLoaded', function() {
    // Navbar active section functionality
    function updateActiveNavLink() {
        // Select only section navigation links, exclude profile/login buttons
        const navLinks = document.querySelectorAll('.navbar-nav .nav-link[href^="#"]:not(.profile-btn):not(.login-btn)');
        
        if (navLinks.length === 0) return; // Skip if no nav links found
        
        // Get all target sections based on nav links
        const sections = Array.from(navLinks).map(link => {
            const targetId = link.getAttribute('href').substring(1); // Remove #
            return document.getElementById(targetId);
        }).filter(section => section !== null);
        
        if (sections.length === 0) return; // Skip if no sections found
        
        let currentSection = '';
        const scrollPosition = window.scrollY + 100; // Offset for fixed navbar
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                currentSection = section.getAttribute('id');
            }
        });
        
        // Update active class ONLY on section navigation links
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${currentSection}`) {
                link.classList.add('active');
            }
        });
    }
    
    // Smooth scrolling for navbar links
    function setupSmoothScrolling() {
        const navLinks = document.querySelectorAll('.navbar-nav .nav-link[href^="#"]');
        
        navLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const targetId = this.getAttribute('href');
                const targetSection = document.querySelector(targetId);
                
                if (targetSection) {
                    const navbarHeight = 80; // Fixed navbar height
                    const targetPosition = targetSection.offsetTop - navbarHeight;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }
    
    // Initialize navbar functionality
    updateActiveNavLink();
    setupSmoothScrolling();
    
    // Update active link on scroll
    window.addEventListener('scroll', updateActiveNavLink);
});