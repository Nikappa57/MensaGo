// JavaScript for authentication pages (login, register, etc.)

document.addEventListener('DOMContentLoaded', function() {
    // Profile picture preview functionality
    const propicInput = document.getElementById('id_propic');
    const profilePreview = document.getElementById('profile-preview');
    
    if (propicInput && profilePreview) {
        propicInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Verify it's an image
                if (!file.type.startsWith('image/')) {
                    alert('Per favore seleziona un file immagine valido.');
                    e.target.value = '';
                    return;
                }
                
                // Verify file size (max 5MB)
                if (file.size > 5 * 1024 * 1024) {
                    alert('Il file è troppo grande. Seleziona un\'immagine di massimo 5MB.');
                    e.target.value = '';
                    return;
                }
                
                const reader = new FileReader();
                reader.onload = function(e) {
                    profilePreview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            } else {
                // Reset preview if no file is selected
                // Get default image path from the img element's data attribute or fallback
                const defaultSrc = profilePreview.getAttribute('data-default-src') || '/static/imgs/profile_pics/default.jpg';
                profilePreview.src = defaultSrc;
            }
        });
    }
});
