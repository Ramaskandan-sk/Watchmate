// Main JavaScript file for Watchmate

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss flash messages after 5 seconds
    setTimeout(function() {
        const flashMessages = document.querySelectorAll('.alert-dismissible');
        flashMessages.forEach(function(message) {
            const bsAlert = new bootstrap.Alert(message);
            bsAlert.close();
        });
    }, 5000);
    
    // Initialize animations without demo triggers for now
    // We'll implement that separately

    // Initialize tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltipTriggerList.length > 0) {
        const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    }
    
    // Category filter handling
    const filterButtons = document.querySelectorAll('.filter-btn');
    
    if (filterButtons.length > 0) {
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                const category = this.getAttribute('data-category');
                window.location.href = category ? 
                    `/dashboard?category=${category}` : 
                    '/dashboard';
            });
        });
    }
    
    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    
    if (forms.length > 0) {
        Array.prototype.slice.call(forms).forEach(function(form) {
            form.addEventListener('submit', function(event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }

    // Image path preview on add/edit forms
    const imageUrlInput = document.getElementById('image_url');
    const imagePreview = document.getElementById('image-preview');
    
    if (imageUrlInput && imagePreview) {
        // Initial preview
        updateImagePreview();
        
        // Update on input change
        imageUrlInput.addEventListener('input', updateImagePreview);
        
        function updateImagePreview() {
            const imageUrl = imageUrlInput.value.trim();
            
            if (!imageUrl) {
                imagePreview.style.display = 'none';
                return;
            }
            
            // Determine if it's a URL or local path
            let displayUrl;
            if (imageUrl.match(/^https?:\/\//i)) {
                displayUrl = imageUrl;
            } else {
                // Handle local path
                // Remove leading slash if present
                const cleanPath = imageUrl.replace(/^\//, '');
                displayUrl = `/static/${cleanPath}`;
            }
            
            imagePreview.src = displayUrl;
            imagePreview.style.display = 'block';
            
            // Handle load errors
            imagePreview.onerror = function() {
                // Use a placeholder SVG
                this.src = 'data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22286%22%20height%3D%22180%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%20286%20180%22%20preserveAspectRatio%3D%22none%22%3E%3Cdefs%3E%3Cstyle%20type%3D%22text%2Fcss%22%3E%23holder_17a3f093956%20text%20%7B%20fill%3A%23AAAAAA%3Bfont-weight%3Abold%3Bfont-family%3AArial%2C%20Helvetica%2C%20Open%20Sans%2C%20sans-serif%2C%20monospace%3Bfont-size%3A14pt%20%7D%20%3C%2Fstyle%3E%3C%2Fdefs%3E%3Cg%20id%3D%22holder_17a3f093956%22%3E%3Crect%20width%3D%22286%22%20height%3D%22180%22%20fill%3D%22%23282c34%22%3E%3C%2Frect%3E%3Cg%3E%3Ctext%20x%3D%22108.5%22%20y%3D%2297.1%22%3EImage%20Preview%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fsvg%3E';
                this.onerror = null;
            };
        }
    }

    // Add hover animations
    const cards = document.querySelectorAll('.watchlist-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('card-hover');
        });
        
        card.addEventListener('mouseleave', function() {
            this.classList.remove('card-hover');
        });
    });
});