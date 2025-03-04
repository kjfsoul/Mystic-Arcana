
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
