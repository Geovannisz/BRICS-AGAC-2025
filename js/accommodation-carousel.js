document.addEventListener('DOMContentLoaded', () => {
    const hotelCards = document.querySelectorAll('.hotel-card');

    hotelCards.forEach(card => {
        const mainImage = card.querySelector('.main-image');
        const thumbnails = card.querySelectorAll('.thumbnail');
        let currentIndex = 0;
        let intervalId;

        function updateMainImage(index) {
            mainImage.src = thumbnails[index].src;
            thumbnails.forEach((thumb, i) => {
                thumb.classList.toggle('active', i === index);
            });
            currentIndex = index;
        }

        function startCarousel() {
            intervalId = setInterval(() => {
                let nextIndex = (currentIndex + 1) % thumbnails.length;
                updateMainImage(nextIndex);
            }, 4000);
        }

        function stopCarousel() {
            clearInterval(intervalId);
        }

        thumbnails.forEach((thumbnail, index) => {
            thumbnail.addEventListener('click', () => {
                stopCarousel();
                updateMainImage(index);
                startCarousel();
            });
        });

        card.addEventListener('mouseenter', stopCarousel);
        card.addEventListener('mouseleave', startCarousel);

        startCarousel();
    });
});
