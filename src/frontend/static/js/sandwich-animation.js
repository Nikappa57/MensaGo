// Function to add random sizes and slightly different animations to sandwiches
document.addEventListener('DOMContentLoaded', function() {
    const sandwiches = document.querySelectorAll('.sandwich-bubble');
    
    sandwiches.forEach(sandwich => {
        // Random size between 64px and 128px
        const size = Math.floor(Math.random() * 64) + 64;
        sandwich.style.width = `${size}px`;
        sandwich.style.height = `${size}px`;
        
        // Random horizontal position
        const posX = Math.floor(Math.random() * 90) + 5; // between 5% and 95%
        sandwich.style.left = `${posX}%`;
        
        // Random animation delay
        const delay = Math.random() * 1;
        sandwich.style.animationDelay = `${delay}s`;
        
        // Random animation duration between 6s and 12s
        const duration = Math.random() * 6 + 6;
        sandwich.style.animationDuration = `${duration}s`;
        
        // Random initial rotation
        const rotation = Math.floor(Math.random() * 360);
        sandwich.style.transform = `rotate(${rotation}deg)`;
    });
});
