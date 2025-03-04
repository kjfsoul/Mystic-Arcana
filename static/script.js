
// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        window.scrollTo({
          top: targetElement.offsetTop - 100,
          behavior: 'smooth'
        });
      }
    });
  });
  
  // Flash messages auto-hide
  const flashMessages = document.querySelectorAll('.flash-message');
  if (flashMessages.length > 0) {
    flashMessages.forEach(message => {
      setTimeout(() => {
        message.style.opacity = '0';
        setTimeout(() => {
          message.style.display = 'none';
        }, 500);
      }, 5000);
    });
  }
  
  // Add active class to current navigation link
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(link => {
    const linkPath = link.getAttribute('href');
    if (linkPath && currentPath.includes(linkPath) && linkPath !== '/') {
      link.classList.add('bg-purple-900', 'bg-opacity-50', 'text-white');
    }
  });
});
