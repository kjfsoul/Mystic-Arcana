
// Initialize smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    if (this.getAttribute('href') !== '#') {
      e.preventDefault();
      
      const targetId = this.getAttribute('href');
      const targetElement = document.querySelector(targetId);
      
      if (targetElement) {
        window.scrollTo({
          top: targetElement.offsetTop - 80,
          behavior: 'smooth'
        });
      }
    }
  });
});

// Parallax effect for background elements
window.addEventListener('scroll', function() {
  const scrollPosition = window.pageYOffset;
  document.querySelector('.twinkling').style.transform = `translateY(${scrollPosition * 0.3}px)`;
});

// Add mouse-follow subtle glow effect
const body = document.querySelector('body');
let glowElement = document.createElement('div');
glowElement.classList.add('mouse-glow');
glowElement.style.position = 'fixed';
glowElement.style.width = '300px';
glowElement.style.height = '300px';
glowElement.style.borderRadius = '50%';
glowElement.style.background = 'radial-gradient(circle, rgba(139, 92, 246, 0.1) 0%, rgba(0, 0, 0, 0) 70%)';
glowElement.style.pointerEvents = 'none';
glowElement.style.zIndex = '2';
glowElement.style.transform = 'translate(-50%, -50%)';
body.appendChild(glowElement);

document.addEventListener('mousemove', (e) => {
  glowElement.style.left = `${e.clientX}px`;
  glowElement.style.top = `${e.clientY}px`;
});

// Card hover effects
const contentCards = document.querySelectorAll('.content-card, .blog-card, .product-card');
contentCards.forEach(card => {
  card.addEventListener('mouseenter', function() {
    this.style.transform = 'translateY(-8px)';
  });
  
  card.addEventListener('mouseleave', function() {
    this.style.transform = 'translateY(0)';
  });
});

// Add stellar particle effect to hero section (stars that twinkle)
const createStars = () => {
  const header = document.querySelector('header');
  
  for (let i = 0; i < 20; i++) {
    const star = document.createElement('div');
    star.classList.add('twinkling-star');
    
    const size = Math.random() * 4 + 1;
    star.style.width = `${size}px`;
    star.style.height = `${size}px`;
    star.style.background = 'white';
    star.style.position = 'absolute';
    star.style.borderRadius = '50%';
    star.style.opacity = Math.random() * 0.5 + 0.3;
    
    star.style.left = `${Math.random() * 100}%`;
    star.style.top = `${Math.random() * 100}%`;
    
    // Add twinkling animation
    star.style.animation = `twinkle ${Math.random() * 3 + 2}s infinite alternate`;
    
    header.appendChild(star);
  }
  
  // Add twinkle keyframes
  const style = document.createElement('style');
  style.innerHTML = `
    @keyframes twinkle {
      0% { opacity: 0.3; }
      100% { opacity: 0.8; }
    }
  `;
  document.head.appendChild(style);
};

createStars();

// Lazy load images with fade-in effect as they enter viewport
document.addEventListener('DOMContentLoaded', () => {
  const lazyImages = document.querySelectorAll('.blog-image-1, .blog-image-2, .blog-image-3');
  
  if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.style.opacity = 1;
          imageObserver.unobserve(img);
        }
      });
    });
    
    lazyImages.forEach(img => {
      img.style.opacity = 0;
      img.style.transition = 'opacity 0.8s ease-in-out';
      imageObserver.observe(img);
    });
  }
});

// Animate content cards as they enter viewport
document.addEventListener('DOMContentLoaded', () => {
  const animatedElements = document.querySelectorAll('.content-card, .blog-card, .product-card');
  
  if ('IntersectionObserver' in window) {
    const elementObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const element = entry.target;
          element.style.opacity = 1;
          element.style.transform = 'translateY(0)';
          elementObserver.unobserve(element);
        }
      });
    }, { threshold: 0.1 });
    
    animatedElements.forEach(element => {
      element.style.opacity = 0;
      element.style.transform = 'translateY(20px)';
      element.style.transition = 'opacity 0.8s ease-out, transform 0.8s ease-out';
      elementObserver.observe(element);
    });
  }
});

// Mobile menu toggle (for smaller screens)
document.addEventListener('DOMContentLoaded', () => {
  // Add mobile menu button if it doesn't exist yet
  const nav = document.querySelector('nav .container');
  if (window.innerWidth < 768 && !document.querySelector('.mobile-menu-btn')) {
    const mobileMenuBtn = document.createElement('button');
    mobileMenuBtn.classList.add('mobile-menu-btn');
    mobileMenuBtn.innerHTML = '<i class="fas fa-bars text-white text-xl"></i>';
    mobileMenuBtn.style.display = 'block';
    mobileMenuBtn.style.position = 'absolute';
    mobileMenuBtn.style.right = '1rem';
    mobileMenuBtn.style.top = '1rem';
    mobileMenuBtn.style.background = 'transparent';
    mobileMenuBtn.style.border = 'none';
    mobileMenuBtn.style.cursor = 'pointer';
    
    nav.appendChild(mobileMenuBtn);
    
    // Toggle menu visibility
    mobileMenuBtn.addEventListener('click', () => {
      const navLinks = document.querySelector('nav .space-x-6');
      if (navLinks.style.display === 'none' || navLinks.style.display === '') {
        navLinks.style.display = 'flex';
        navLinks.style.flexDirection = 'column';
        navLinks.style.alignItems = 'center';
        mobileMenuBtn.innerHTML = '<i class="fas fa-times text-white text-xl"></i>';
      } else {
        navLinks.style.display = 'none';
        mobileMenuBtn.innerHTML = '<i class="fas fa-bars text-white text-xl"></i>';
      }
    });
  }
});
