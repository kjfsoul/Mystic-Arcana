
// Set the countdown target time (example: 8 hours from now for the alignment)
const targetTime = new Date();
targetTime.setHours(targetTime.getHours() + 8);

// Update countdown every second
function updateCountdown() {
  const currentTime = new Date();
  const difference = targetTime - currentTime;
  
  // Calculate hours, minutes, seconds
  const hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
  const seconds = Math.floor((difference % (1000 * 60)) / 1000);
  
  // Update the HTML elements
  document.getElementById('hours').textContent = hours.toString().padStart(2, '0');
  document.getElementById('minutes').textContent = minutes.toString().padStart(2, '0');
  document.getElementById('seconds').textContent = seconds.toString().padStart(2, '0');
  
  // If countdown is finished
  if (difference < 0) {
    clearInterval(countdownInterval);
    document.getElementById('countdown').innerHTML = '<h3 class="text-2xl text-purple-400">The Planets Are Aligned!</h3>';
  }
}

// Initialize countdown
updateCountdown();
const countdownInterval = setInterval(updateCountdown, 1000);

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();
    
    const targetId = this.getAttribute('href');
    if (targetId === '#') return;
    
    const targetElement = document.querySelector(targetId);
    if (targetElement) {
      window.scrollTo({
        top: targetElement.offsetTop - 80,
        behavior: 'smooth'
      });
    }
  });
});

// Add parallax effect to stars background
window.addEventListener('scroll', function() {
  const scrollPosition = window.pageYOffset;
  document.querySelector('.twinkling').style.transform = `translateY(${scrollPosition * 0.3}px)`;
});

// Initialize AOS for scroll animations if available
if (typeof AOS !== 'undefined') {
  AOS.init({
    duration: 800,
    easing: 'ease-in-out'
  });
}

// Add animation to products on hover
const productCards = document.querySelectorAll('.product-card');
productCards.forEach(card => {
  card.addEventListener('mouseenter', function() {
    this.style.transform = 'translateY(-10px)';
    this.style.boxShadow = '0 20px 40px rgba(123, 31, 162, 0.4)';
  });
  
  card.addEventListener('mouseleave', function() {
    this.style.transform = 'translateY(0)';
    this.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.5)';
  });
});
