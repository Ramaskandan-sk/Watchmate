// Animation functionality for Watchmate

document.addEventListener('DOMContentLoaded', function() {
    // Initialize loading animations system
    initLoadingAnimations();
    
    // Add page transition effect
    document.querySelector('main').classList.add('page-transition');
    
    // Initialize button hover animations
    initButtonAnimations();
    
    // Add card hover effects
    initCardAnimations();
    
    // Add demo triggers for filter buttons and navigation
    addDemoTriggers();
});

// Loading animations
function initLoadingAnimations() {
    // Create loading overlay if it doesn't exist
    if (!document.querySelector('.loading-overlay')) {
        createLoadingOverlay();
    }
    
    // Add loading animation to links that navigate to other pages
    const pageLinks = document.querySelectorAll('a[href]:not([href^="#"]):not([href^="javascript:"]):not([href^="mailto:"]):not([target="_blank"])');
    
    pageLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Only for internal links
            if (link.hostname === window.location.hostname) {
                // Determine the type of page we're going to
                let animationType = 'default';
                const href = link.getAttribute('href').toLowerCase();
                
                if (href.includes('movie') || link.innerText.toLowerCase().includes('movie')) {
                    animationType = 'movie';
                } else if (href.includes('anime') || link.innerText.toLowerCase().includes('anime')) {
                    animationType = 'anime';
                } else if (href.includes('series') || link.innerText.toLowerCase().includes('series')) {
                    animationType = 'series';
                }
                
                // Custom text based on where the user is going
                let loadingText = 'Loading...';
                if (href.includes('dashboard')) {
                    loadingText = 'Loading your watchlist...';
                } else if (href.includes('add')) {
                    loadingText = 'Preparing to add new content...';
                } else if (href.includes('profile')) {
                    loadingText = 'Loading your profile...';
                }
                
                showLoading(animationType, loadingText);
                
                // Let the animation show before navigating
                e.preventDefault();
                setTimeout(() => {
                    window.location.href = link.href;
                }, 800);
            }
        });
    });
    
    // Add loading animation to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Don't show loading for forms with data-no-loading attribute
            if (form.getAttribute('data-no-loading') === 'true') {
                return;
            }
            
            // Determine animation type based on form action or purpose
            let animationType = 'default';
            if (form.id === 'login-form' || form.id === 'signup-form') {
                animationType = 'default';
            } else if (form.querySelector('select[name="category"]')) {
                const categorySelect = form.querySelector('select[name="category"]');
                if (categorySelect.value) {
                    animationType = categorySelect.value.toLowerCase();
                }
            }
            
            // Custom loading text
            let loadingText = 'Processing...';
            if (form.id === 'login-form') {
                loadingText = 'Logging in...';
            } else if (form.id === 'signup-form') {
                loadingText = 'Creating your account...';
            } else if (form.action.includes('add')) {
                loadingText = 'Adding to your watchlist...';
            } else if (form.action.includes('edit')) {
                loadingText = 'Updating your item...';
            } else if (form.action.includes('delete')) {
                loadingText = 'Removing from watchlist...';
            }
            
            showLoading(animationType, loadingText);
        });
    });
    
    // Add animation for AJAX actions
    const importBtn = document.getElementById('importSubmitBtn');
    if (importBtn) {
        importBtn.addEventListener('click', function() {
            // Don't show if no file selected (handled by the import logic)
            const fileInput = document.getElementById('importFileInput');
            if (!fileInput.files || fileInput.files.length === 0) {
                return;
            }
            
            showLoading('default', 'Importing your watchlist...');
        });
    }
    
    // Hide loading overlay when page is fully loaded
    window.addEventListener('load', hideLoading);
}

// Create the loading overlay structure
function createLoadingOverlay() {
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';
    
    const characterContainer = document.createElement('div');
    characterContainer.className = 'loading-character';
    
    // Create all character types
    const characterTypes = ['movie', 'anime', 'series', 'default'];
    characterTypes.forEach(type => {
        const character = document.createElement('div');
        character.className = `character character-${type}`;
        character.style.display = 'none';
        characterContainer.appendChild(character);
    });
    
    const text = document.createElement('div');
    text.className = 'loading-text';
    text.innerHTML = 'Loading<span class="loading-dots"></span>';
    
    const spinner = document.createElement('div');
    spinner.className = 'loading-spinner';
    
    overlay.appendChild(characterContainer);
    overlay.appendChild(text);
    overlay.appendChild(spinner);
    
    document.body.appendChild(overlay);
}

// Show loading animation
function showLoading(type = 'default', message = 'Loading...') {
    const overlay = document.querySelector('.loading-overlay');
    if (!overlay) return;
    
    // Hide all characters first
    document.querySelectorAll('.character').forEach(char => {
        char.style.display = 'none';
    });
    
    // Show the appropriate character
    let characterType = type.toLowerCase();
    // Normalize the type if needed
    if (['movie', 'movies', 'film'].includes(characterType)) {
        characterType = 'movie';
    } else if (['anime', 'animation'].includes(characterType)) {
        characterType = 'anime';
    } else if (['series', 'tv', 'show'].includes(characterType)) {
        characterType = 'series';
    } else {
        characterType = 'default';
    }
    
    const character = document.querySelector(`.character-${characterType}`);
    if (character) {
        character.style.display = 'block';
    }
    
    // Set the message
    const loadingText = document.querySelector('.loading-text');
    if (loadingText) {
        // Keep the dots animation by preserving the span
        loadingText.innerHTML = message + '<span class="loading-dots"></span>';
    }
    
    // Show the overlay
    overlay.classList.add('active');
}

// Hide loading animation
function hideLoading() {
    const overlay = document.querySelector('.loading-overlay');
    if (overlay) {
        overlay.classList.remove('active');
    }
}

// Button animations
function initButtonAnimations() {
    // Add hover animations to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.classList.add('button-hover');
        });
        button.addEventListener('mouseleave', function() {
            this.classList.remove('button-hover');
        });
    });
}

// Card animations
function initCardAnimations() {
    // Add hover effect to cards
    const cards = document.querySelectorAll('.watchlist-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('card-hover');
        });
        card.addEventListener('mouseleave', function() {
            this.classList.remove('card-hover');
        });
    });
}

// Global function to manually trigger loading
function showLoadingAnimation(type, message) {
    showLoading(type, message);
}

// Global function to manually hide loading
function hideLoadingAnimation() {
    hideLoading();
}

// Add demo animation triggers
function addDemoTriggers() {
    // Add animation to filter buttons
    const filterButtons = document.querySelectorAll('.filter-btn');
    if (filterButtons.length > 0) {
        filterButtons.forEach(button => {
            // On click, show a quick animation
            button.addEventListener('click', function() {
                const category = this.getAttribute('data-category');
                let animationType = 'default';
                let message = 'Loading all items...';
                
                if (category === 'Movie') {
                    animationType = 'movie';
                    message = 'Loading movies...';
                } else if (category === 'Anime') {
                    animationType = 'anime';
                    message = 'Loading anime...';
                } else if (category === 'Series') {
                    animationType = 'series';
                    message = 'Loading series...';
                }
                
                showLoading(animationType, message);
            });
        });
    }
    
    // Add animation to the "Add New" button
    const addButton = document.querySelector('.btn-add');
    if (addButton) {
        addButton.addEventListener('click', function() {
            showLoading('default', 'Preparing to add new content...');
        });
    }
    
    // Add animation to the dashboard button
    const dashboardLink = document.querySelector('a[href="/dashboard"]');
    if (dashboardLink) {
        dashboardLink.addEventListener('click', function(e) {
            e.preventDefault();
            showLoading('default', 'Loading your watchlist...');
            setTimeout(() => {
                window.location.href = dashboardLink.href;
            }, 1000);
        });
    }
    
    // Add animation to the import button
    const importButton = document.querySelector('a[data-bs-target="#importModal"]');
    if (importButton) {
        importButton.addEventListener('click', function() {
            // Just a brief flash to show the animation
            showLoading('default', 'Loading import options...');
            setTimeout(hideLoading, 500);
        });
    }
    
    // Demo animation button for users to see all character types
    const demoButton = document.createElement('button');
    demoButton.className = 'btn btn-sm btn-secondary position-fixed demo-animations-btn';
    demoButton.style.bottom = '20px';
    demoButton.style.right = '20px';
    demoButton.style.zIndex = '1000';
    demoButton.innerHTML = '<i class="fas fa-magic me-1"></i> Demo Animations';
    
    demoButton.addEventListener('click', function() {
        // Cycle through all animation types
        const types = ['movie', 'anime', 'series', 'default'];
        let index = 0;
        
        function showNextAnimation() {
            if (index >= types.length) {
                hideLoading();
                return;
            }
            
            const type = types[index];
            let message = 'Loading...';
            
            switch(type) {
                case 'movie':
                    message = 'Loading movies...';
                    break;
                case 'anime':
                    message = 'Loading anime...';
                    break;
                case 'series':
                    message = 'Loading series...';
                    break;
                default:
                    message = 'Loading your content...';
            }
            
            showLoading(type, message);
            index++;
            setTimeout(showNextAnimation, 1500);
        }
        
        showNextAnimation();
    });
    
    document.body.appendChild(demoButton);
}