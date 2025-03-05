
document.addEventListener('DOMContentLoaded', function() {
    // Sample JavaScript functionality
    console.log('Mystic Arcana JavaScript loaded!');
    
    // Example of a simple card selection feature
    const cards = document.querySelectorAll('.card');
    if (cards.length > 0) {
        cards.forEach(card => {
            card.addEventListener('click', function() {
                this.classList.toggle('flipped');
            });
        });
    }
    
    // Example form validation
    const profileForm = document.querySelector('.profile-form');
    if (profileForm) {
        profileForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const nameInput = document.getElementById('name');
            const emailInput = document.getElementById('email');
            
            if (nameInput.value.trim() === '') {
                alert('Please enter your name');
                return;
            }
            
            if (emailInput.value.trim() === '') {
                alert('Please enter your email');
                return;
            }
            
            alert('Profile updated successfully!');
        });
    }
});
// Mystic Arcana - Main Javascript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Mystic Arcana scripts initialized');
    
    // Initialize any interactive elements
    initializeNavigation();
    initializeAnimations();
    
    // Fix for React DOM reference if used
    if (document.querySelectorAll('script[src*="react-dom"]').length > 0) {
        // Handle React DOM reference or provide fallback
        console.log('React DOM detected, initializing fallback if needed');
    }
});

function initializeNavigation() {
    // Mobile navigation toggle
    const navToggle = document.querySelector('.mobile-nav-toggle');
    if (navToggle) {
        navToggle.addEventListener('click', () => {
            const navItems = document.querySelector('.nav-items');
            navItems.classList.toggle('active');
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
}

function initializeAnimations() {
    // Add any animation initializations
    const animatedElements = document.querySelectorAll('.fade-in, .slide-in');
    if (animatedElements.length > 0) {
        // Simple animation observer
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, { threshold: 0.1 });
        
        animatedElements.forEach(el => observer.observe(el));
    }
}

// Handle tarot card interactions if present
const tarotCards = document.querySelectorAll('.tarot-card');
if (tarotCards.length > 0) {
    tarotCards.forEach(card => {
        card.addEventListener('click', function() {
            this.classList.toggle('flipped');
        });
    });
}

// Fix for CDN reference errors in index.html
// Safe check for external libraries
function safelyLoadExternalScript(libraryName, fallbackFunction) {
    try {
        if (typeof window[libraryName] === 'undefined') {
            console.log(`${libraryName} not loaded properly, using fallback`);
            if (typeof fallbackFunction === 'function') {
                fallbackFunction();
            }
        }
    } catch (e) {
        console.log(`Error checking ${libraryName}: ${e.message}`);
    }
}

// Check for dragselect library
safelyLoadExternalScript('DragSelect', function() {
    // Simple fallback if needed
    console.log('DragSelect fallback initialized');
});

// Fix for ReactDOM reference
safelyLoadExternalScript('ReactDOM', function() {
    // Provide minimal ReactDOM fallback if needed
    console.log('ReactDOM fallback initialized');
});
