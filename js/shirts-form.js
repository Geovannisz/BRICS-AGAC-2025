document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('shirts-order-form');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            const fullName = document.getElementById('fullName').value.trim();
            if (fullName === '') {
                alert('Please enter your full name.');
                return;
            }

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
