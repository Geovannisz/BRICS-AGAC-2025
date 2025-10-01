// js/script.js

// Function to set the language of the page
function setLanguage(lang) {
    // --- Translate standard text content ---
    const elements = document.querySelectorAll('[data-lang-en]');
    elements.forEach(el => {
        const text = el.getAttribute(`data-lang-${lang}`);
        if (text !== null) {
            el.innerHTML = text;
        }
    });

    // --- Translate placeholder attributes ---
    const placeholders = document.querySelectorAll('[data-lang-en-placeholder]');
    placeholders.forEach(el => {
        const placeholderText = el.getAttribute(`data-lang-${lang}-placeholder`);
        if (placeholderText !== null) {
            el.placeholder = placeholderText;
        }
    });

    // --- Translate title attribute ---
    const pageTitle = document.querySelector('title[data-lang-en]');
    if (pageTitle) {
        const titleText = pageTitle.getAttribute(`data-lang-${lang}`);
        if (titleText !== null) {
            document.title = titleText;
        }
    }


    // --- Update UI state ---
    // Update active state on language switcher
    document.getElementById('lang-switcher-en').style.fontWeight = (lang === 'en') ? 'bold' : 'normal';
    document.getElementById('lang-switcher-pt').style.fontWeight = (lang === 'pt') ? 'bold' : 'normal';

    // Save preference to localStorage
    localStorage.setItem('brics-agac-lang', lang);

}

document.addEventListener('DOMContentLoaded', function() {
    // --- Page Load Animation Trigger ---
    // Add 'page-loaded' class to body to trigger CSS transition
    document.body.classList.add('page-loaded');

    console.log("BRICS-AGAC 2025 Website Loaded");

    // --- Language Switcher Logic ---
    const savedLang = localStorage.getItem('brics-agac-lang') || 'en';
    setLanguage(savedLang);

    document.getElementById('lang-switcher-en').addEventListener('click', function(e) {
        e.preventDefault();
        setLanguage('en');
    });

    document.getElementById('lang-switcher-pt').addEventListener('click', function(e) {
        e.preventDefault();
        setLanguage('pt');
    });


    // --- Original Nav Link Activation ---
    // Activate current nav link based on URL
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const currentPath = window.location.pathname.split("/").pop() || "index.html";

    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        // Avoid adding 'active' to language switchers and ensure href exists
        if (href && !link.classList.contains('lang-switcher')) {
            const linkPath = href.split("/").pop();
            if (linkPath === currentPath) {
                link.classList.add('active');
            }
        }
    });

    // Optional: Smooth scroll for anchor links (if any are added later)
    // document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    //     anchor.addEventListener('click', function (e) {
    //         e.preventDefault();
    //         document.querySelector(this.getAttribute('href')).scrollIntoView({
    //             behavior: 'smooth'
    //         });
    //     });
    // });

    // --- Copy to Clipboard Functionality ---
    const copyButtons = document.querySelectorAll('.copy-btn');
    copyButtons.forEach(button => {
        const copyIcon = button.querySelector('.fa-copy');
        const checkIcon = button.querySelector('.fa-check');

        // Hide check icon by default if it's not already handled by CSS
        if (checkIcon) {
            checkIcon.style.display = 'none';
        }

        button.addEventListener('click', function(e) {
            e.preventDefault();
            const valueToCopy = this.dataset.copyValue;

            if (!valueToCopy || !navigator.clipboard) {
                console.error('Clipboard API not available or no value to copy.');
                return;
            }

            navigator.clipboard.writeText(valueToCopy).then(() => {
                // Success feedback
                if (copyIcon) copyIcon.style.display = 'none';
                if (checkIcon) checkIcon.style.display = 'inline-block';

                // Revert icon after a few seconds
                setTimeout(() => {
                    if (copyIcon) copyIcon.style.display = 'inline-block';
                    if (checkIcon) checkIcon.style.display = 'none';
                }, 2000);

            }).catch(err => {
                console.error('Failed to copy text: ', err);
                // Optional: show an error tooltip or message
            });
        });
    });

    // --- Registration Counter ---
    updateRegistrationCount();

    // --- Scroll Animation ---
    const scrollObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target); // Stop observing once visible
            }
        });
    }, {
        threshold: 0.1 // Trigger when 10% of the element is visible
    });

    const elementsToAnimate = document.querySelectorAll('.fade-in-on-scroll');
    elementsToAnimate.forEach(element => {
        scrollObserver.observe(element);
    });


    // --- Button Mouse-aware Spotlight Effect ---
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mousemove', e => {
            const rect = button.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            button.style.setProperty('--mouse-x', `${x}px`);
            button.style.setProperty('--mouse-y', `${y}px`);
        });
    });
});

/**
 * Fetches the number of registered participants by calling a secure serverless function.
 */
async function updateRegistrationCount() {
    const url = '/api/get-registration-count'; // Use the secure serverless function
    const registrationCountSpan = document.getElementById('registration-count');

    if (!registrationCountSpan) {
        console.log('Registration count element not found on this page.');
        return;
    }

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        const data = await response.json();
        registrationCountSpan.textContent = data.count;

    } catch (error) {
        console.error('Error fetching registration data:', error);
        registrationCountSpan.textContent = '??'; // Display error indicator
    }
}
