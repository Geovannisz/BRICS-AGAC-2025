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
 * Fetches the number of unique registered participants and updates the counter on the page.
 */
async function updateRegistrationCount() {
    const url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSDhHAo69dtSs8Snd2wPwlw70K3k9Hvg2Z9nMAG-s3L8bjAjpamz1aUdDdMinSOgS0r9E264eVWrkz7/pub?gid=899626177&single=true&output=csv';
    const registrationCountSpan = document.getElementById('registration-count');

    if (!registrationCountSpan) {
        // This is expected on pages without the counter, so we don't log an error.
        return;
    }

    // A robust CSV parser to be used locally within this function.
    function parseCSV(text) {
        const lines = text.trim().split(/\r?\n/);
        if (lines.length < 2) return [];
        const headers = lines[0].split(',').map(h => h.trim().replace(/^"|"$/g, ''));
        return lines.slice(1).map(line => {
            if (!line.trim()) return null;
            const obj = {};
            const values = [];
            let current = '';
            let inQuotes = false;
            for (let i = 0; i < line.length; i++) {
                const char = line[i];
                if (char === '"' && (i === 0 || line[i-1] === ',' || line[i+1] === ',' || i === line.length - 1)) {
                    inQuotes = !inQuotes;
                    continue;
                }
                if (char === ',' && !inQuotes) {
                    values.push(current);
                    current = '';
                } else {
                    current += char;
                }
            }
            values.push(current);
            headers.forEach((header, i) => {
                obj[header] = (values[i] || '').trim().replace(/^"|"$/g, '');
            });
            return obj;
        }).filter(Boolean);
    }

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`CSV fetch error: ${response.status}`);
        }
        const csvText = await response.text();
        const allAttendees = parseCSV(csvText).map(row => ({
            timestamp: row['Carimbo de data/hora'] || '',
            name: row['Name'] || ''
        }));

        // De-duplicate attendees, keeping the latest entry for each name
        const uniqueAttendeesMap = new Map();
        allAttendees.forEach(attendee => {
            const nameKey = attendee.name.trim().toLowerCase();
            if (!nameKey) return;

            const existing = uniqueAttendeesMap.get(nameKey);
            if (!existing) {
                uniqueAttendeesMap.set(nameKey, attendee);
            } else {
                 const parseDate = (dateStr) => {
                    if (!dateStr || !dateStr.includes(' ')) return new Date(0);
                    const [datePart, timePart] = dateStr.split(' ');
                    const [day, month, year] = datePart.split('/');
                    if (!year || !month || !day) return new Date(0);
                    return new Date(`${year}-${month}-${day}T${timePart}`);
                };
                if (parseDate(attendee.timestamp) > parseDate(existing.timestamp)) {
                    uniqueAttendeesMap.set(nameKey, attendee);
                }
            }
        });

        registrationCountSpan.textContent = uniqueAttendeesMap.size;

    } catch (error) {
        console.error('Error fetching registration data:', error);
        registrationCountSpan.textContent = '??'; // Display error indicator
    }
}
