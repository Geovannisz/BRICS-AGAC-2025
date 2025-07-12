document.addEventListener('DOMContentLoaded', () => {
    const hotelCards = document.querySelectorAll('.hotel-card');

    hotelCards.forEach(card => {
        const mainImageContainer = card.querySelector('.main-image-container');
        const mainImage = card.querySelector('.main-image');
        const thumbnails = card.querySelectorAll('.thumbnail');
        let currentIndex = 0;
        let intervalId = null;

        function updateMainImage(index) {
            // Not found
            if (index < 0 || index >= thumbnails.length) {
                return;
            }

            mainImage.src = thumbnails[index].src.replace('thumbnail', 'main');
            thumbnails.forEach((thumb, i) => {
                thumb.classList.toggle('active', i === index);
            });
            currentIndex = index;
        }

        function startCarousel() {
            // Clear any existing interval
            if (intervalId) {
                clearInterval(intervalId);
            }
            intervalId = setInterval(() => {
                const nextIndex = (currentIndex + 1) % thumbnails.length;
                updateMainImage(nextIndex);
            }, 4000);
        }

        function stopCarousel() {
            clearInterval(intervalId);
            intervalId = null;
        }

        thumbnails.forEach((thumbnail, index) => {
            thumbnail.addEventListener('click', () => {
                updateMainImage(index);
                // When the user manually selects an image, we stop the automatic carousel
                stopCarousel();
            });
        });

        // Stop carousel on mouse enter
        mainImageContainer.addEventListener('mouseenter', stopCarousel);

        // Restart carousel on mouse leave
        mainImageContainer.addEventListener('mouseleave', startCarousel);

        // Start the carousel initially
        startCarousel();
    });
});
