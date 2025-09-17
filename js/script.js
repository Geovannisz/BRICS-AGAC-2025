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
        // Avoid adding 'active' to language switchers
        if (!link.classList.contains('lang-switcher')) {
            const linkPath = link.getAttribute('href').split("/").pop();
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
    document.body.addEventListener('click', function(e) {
        if (e.target.classList.contains('copy-btn')) {
            const valueToCopy = e.target.getAttribute('data-copy-value');
            const feedbackElement = e.target.querySelector('.copy-feedback');

            navigator.clipboard.writeText(valueToCopy).then(() => {
                // Show feedback
                if (feedbackElement) {
                    feedbackElement.classList.add('visible');
                    // Hide feedback after 2 seconds
                    setTimeout(() => {
                        feedbackElement.classList.remove('visible');
                    }, 2000);
                }
            }).catch(err => {
                console.error('Failed to copy text: ', err);
                // Optionally, provide error feedback to the user
                if (feedbackElement) {
                    feedbackElement.textContent = 'Failed!';
                    feedbackElement.style.color = 'red';
                    feedbackElement.classList.add('visible');
                    setTimeout(() => {
                        feedbackElement.classList.remove('visible');
                        // Reset text and color
                        feedbackElement.textContent = 'Copied!';
                        feedbackElement.style.color = 'green';
                    }, 2000);
                }
            });
        }
    });
});