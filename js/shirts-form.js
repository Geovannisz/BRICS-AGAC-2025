document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('shirts-order-form');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            // Validate Full Name
            const fullName = document.getElementById('fullName').value.trim();
            if (fullName === '') {
                alert('Please enter your full name.');
                return;
            }

            // Validate Email
            const email = document.getElementById('email').value.trim();
            if (email === '') {
                alert('Please enter your email address.');
                return;
            }
            // Basic email format validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                alert('Please enter a valid email address.');
                return;
            }

            // Validate that at least one shirt is selected
            let totalQuantity = 0;
            const quantityInputs = form.querySelectorAll('input[type="number"]');
            quantityInputs.forEach(input => {
                totalQuantity += parseInt(input.value, 10);
            });

            if (totalQuantity === 0) {
                alert('You must select at least one shirt.');
                return;
            }

            form.submit();
        });
    }
});
