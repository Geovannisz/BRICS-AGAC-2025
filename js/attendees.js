// js/attendees.js

document.addEventListener('DOMContentLoaded', function() {
    fetchAttendeeData();
});

// Function to parse CSV text into an array of objects, handling quoted fields.
function parseCSV(text) {
    const lines = text.trim().split(/\r?\n/);
    if (lines.length < 2) return []; // Return empty if no header or data

    const headers = lines[0].split(',').map(h => h.trim().replace(/^"|"$/g, ''));

    return lines.slice(1).map(line => {
        if (!line.trim()) return null; // Skip empty lines

        const obj = {};
        const values = [];
        let current = '';
        let inQuotes = false;

        // This parser iterates through the line, respecting quotes.
        for (let i = 0; i < line.length; i++) {
            const char = line[i];
            if (char === '"' && (line[i-1] === ',' || line[i+1] === ',' || i === 0 || i === line.length - 1)) {
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
    }).filter(Boolean); // Filter out nulls from empty lines
}


// Helper function to convert strings to Title Case, preserving specific acronyms.
function toTitleCase(str) {
    if (!str) return '';

    // List of known acronyms to preserve in uppercase.
    const acronyms = ['ECIEEM', 'UFPB', 'UFCG', 'UFJF', 'USP', 'UEFS', 'UEPB', 'IF', 'APA', 'CPM', 'GRE', 'UNOPAR'];
    // A small list of words to keep in lowercase.
    const exceptions = ['da', 'de', 'do', 'dos', 'e', 'o', 'a'];

    // If the entire string is a known acronym, return it in uppercase.
    if (acronyms.includes(str.toUpperCase().trim())) {
        return str.toUpperCase().trim();
    }

    return str.toLowerCase().split(' ').map(word => {
        // Handle parenthesized acronyms like (UFPB)
        if (word.startsWith('(') && word.endsWith(')')) {
            const acronym = word.slice(1, -1).toUpperCase();
            if (acronyms.includes(acronym)) {
                return `(${acronym})`;
            }
        }

        // Handle simple acronyms
        if (acronyms.includes(word.toUpperCase())) {
            return word.toUpperCase();
        }

        if (exceptions.includes(word)) {
            return word;
        }

        return word.charAt(0).toUpperCase() + word.slice(1);
    }).join(' ');
}

function normalizeData(attendee) {
    const institutionMap = {
        'UFPB': 'Universidade Federal da Paraíba (UFPB)',
        'Universidade Federal da Paraíba': 'Universidade Federal da Paraíba (UFPB)',
        'universidade federal da paraíba': 'Universidade Federal da Paraíba (UFPB)',
        'Universidade Federal da Paraíba-UFPB': 'Universidade Federal da Paraíba (UFPB)',
        'UFCG': 'Universidade Federal de Campina Grande (UFCG)',
        'Unversidade Federal de Campina Grande': 'Universidade Federal de Campina Grande (UFCG)',
        'Universidade Federal de Juiz de Fora': 'Universidade Federal de Juiz de Fora (UFJF)',
        'IF Sudeste MG': 'Instituto Federal do Sudeste de Minas Gerais',
        'INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DO SUDESTE DE MINAS GERAIS - Campus Juiz de Fora': 'Instituto Federal do Sudeste de Minas Gerais',
        'USP': 'Universidade de São Paulo (USP)',
        'IAG/USP': 'Universidade de São Paulo (USP)',
        'Instituto de Física da USP': 'Universidade de São Paulo (USP)',
        'UEFS': 'Universidade Estadual de Feira de Santana (UEFS)',
        'UEPB': 'Universidade Estadual da Paraíba (UEPB)',
        'Rural Federal University of Pernambuco': 'Universidade Federal Rural de Pernambuco (UFRPE)',
        'Associação Paraibana de Astronomia': 'Associação Paraibana de Astronomia (APA)',
        'ASSOCIAÇÃO PARAIBANA DE ASTRONOMIA (APA)': 'Associação Paraibana de Astronomia (APA)',
        'Associação Paraibana de Astronomia - APA': 'Associação Paraibana de Astronomia (APA)',
    };

    const occupationMap = {
        'student (aluno)': 'Student',
        'Estudante': 'Student',
        'Estudent': 'Student',
        'High school student': 'Student',
        'Undergraduate': 'Student',
        'Posdoc': 'Postdoc',
        'junior researcher': 'Researcher',
        'Astrônoma amadora/ Cientista cidadã': 'Amateur Astronomer',
        'Astrônomo amador mirim': 'Amateur Astronomer',
        'Entusiasta da astronomia': 'Amateur Astronomer',
        'Master': "Master's Student",
        'PhD': 'PhD Student',
        'Graduated': 'Student',
    };

    // First, map known variations to a standard name.
    const mappedInstitution = Object.keys(institutionMap).find(key =>
        attendee.institution.trim().toLowerCase().includes(key.toLowerCase())
    );
    attendee.institution = mappedInstitution ? institutionMap[mappedInstitution] : attendee.institution.trim();

    const mappedOccupation = Object.keys(occupationMap).find(key =>
        attendee.occupation.trim().toLowerCase() === key.toLowerCase()
    );
    attendee.occupation = mappedOccupation ? occupationMap[mappedOccupation] : attendee.occupation.trim();

    // Then, apply capitalization formatting.
    attendee.name = toTitleCase(attendee.name.trim());
    attendee.institution = toTitleCase(attendee.institution);

    return attendee;
}

async function fetchAttendeeData() {
    const url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSDhHAo69dtSs8Snd2wPwlw70K3k9Hvg2Z9nMAG-s3L8bjAjpamz1aUdDdMinSOgS0r9E264eVWrkz7/pub?gid=899626177&single=true&output=csv';
    const tbody = document.getElementById('attendees-tbody');

    if (!tbody) {
        console.error('Attendees table body not found.');
        return;
    }

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`CSV fetch error: ${response.status}`);
        }
        const csvText = await response.text();
        const allAttendees = parseCSV(csvText).map(row => ({
            timestamp: row['Carimbo de data/hora'] || '',
            name: row['Name'] || '',
            institution: row['University or Institution'] || '',
            occupation: row['Choose your degree or occupation:'] || ''
        })).map(normalizeData); // Apply normalization here

        // De-duplicate attendees, keeping the latest entry for each name
        const uniqueAttendeesMap = new Map();
        allAttendees.forEach(attendee => {
            const nameKey = attendee.name.trim().toLowerCase();
            if (!nameKey) return; // Skip entries with no name

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
        const uniqueAttendees = Array.from(uniqueAttendeesMap.values());

        populateTable(uniqueAttendees);
        setupSearch(uniqueAttendees);
        setupSorting();
        createCharts(uniqueAttendees);

    } catch (error) {
        console.error('Error fetching or processing attendee data:', error);
        tbody.innerHTML = `<tr><td colspan="4" class="text-center">Error loading data. Please try again later.</td></tr>`;
    }
}

function populateTable(attendees) {
    const tbody = document.getElementById('attendees-tbody');
    tbody.innerHTML = ''; // Clear existing data

    if (attendees.length === 0) {
        tbody.innerHTML = `<tr><td colspan="4" class="text-center">No attendees registered yet.</td></tr>`;
        return;
    }

    attendees.forEach(attendee => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${attendee.timestamp}</td>
            <td>${attendee.name}</td>
            <td>${attendee.institution}</td>
            <td>${attendee.occupation}</td>
        `;
        tbody.appendChild(tr);
    });
}

function setupSearch(allAttendees) {
    const searchInput = document.getElementById('search-input');
    if (!searchInput) return;

    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const filteredAttendees = allAttendees.filter(attendee => {
            return Object.values(attendee).some(value =>
                value && value.toLowerCase().includes(searchTerm)
            );
        });
        populateTable(filteredAttendees);
    });
}

function setupSorting() {
    const table = document.getElementById('attendees-table');
    if (!table) return;

    table.querySelectorAll('th').forEach((header, index) => {
        header.addEventListener('click', () => {
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            const isAscending = header.classList.contains('sort-asc');

            table.querySelectorAll('th').forEach(h => h.classList.remove('sort-asc', 'sort-desc'));

            rows.sort((a, b) => {
                const aText = a.children[index].textContent.trim();
                const bText = b.children[index].textContent.trim();
                return aText.localeCompare(bText, undefined, {numeric: true}) * (isAscending ? -1 : 1);
            });

            header.classList.toggle('sort-asc', !isAscending);
            header.classList.toggle('sort-desc', isAscending);

            tbody.innerHTML = '';
            rows.forEach(row => tbody.appendChild(row));
        });
    });
}

function createCharts(attendees) {
    if (attendees.length === 0) return;

    const lang = localStorage.getItem('brics-agac-lang') || 'en';

    // Translation map for occupations
    const occupationTranslations = {
        'Student': { en: 'Student', pt: 'Estudante' },
        'Professor': { en: 'Professor', pt: 'Professor(a)' },
        'Postdoc': { en: 'Postdoc', pt: 'Pós-Doutorando(a)' },
        'Researcher': { en: 'Researcher', pt: 'Pesquisador(a)' },
        "Master's Student": { en: "Master's Student", pt: "Mestrando(a)" },
        'PhD Student': { en: 'PhD Student', pt: 'Doutorando(a)' },
        'Amateur Astronomer': { en: 'Amateur Astronomer', pt: 'Astrônomo(a) Amador(a)' }
    };

    if (window.institutionsChart) window.institutionsChart.destroy();
    if (window.occupationChart) window.occupationChart.destroy();
    if (window.registrationsByWeekChart) window.registrationsByWeekChart.destroy();

    const institutionsCanvas = document.getElementById('institutions-chart');
    const occupationCanvas = document.getElementById('occupation-chart');
    const registrationsByWeekCanvas = document.getElementById('registrations-by-week-chart');
    if (!institutionsCanvas || !occupationCanvas || !registrationsByWeekCanvas) {
        console.error("A chart canvas element was not found.");
        return;
    }

    const institutionsCtx = institutionsCanvas.getContext('2d');
    const occupationCtx = occupationCanvas.getContext('2d');

    const institutionsTitle = institutionsCanvas.getAttribute(`data-lang-${lang}-title`);
    const institutionsLabel = institutionsCanvas.getAttribute(`data-lang-${lang}-label`);

    const institutionCounts = attendees
        .map(a => a.institution)
        .filter(Boolean) // Remove any null/undefined institutions
        .filter(inst => inst.trim().toLowerCase() !== 'institution') // Filter out generic "Institution"
        .reduce((acc, inst) => {
            acc[inst] = (acc[inst] || 0) + 1;
            return acc;
    }, {});

    // Sort ascending by count, then take the last 15 items.
    // This gives the Top 15, with the largest value at the end of the array.
    // For a horizontal bar chart, the last item is at the top.
    const sortedInstitutions = Object.entries(institutionCounts)
        .sort((a, b) => a[1] - b[1])
        .slice(-15);

    window.institutionsChart = new Chart(institutionsCtx, {
        type: 'bar',
        data: {
            labels: sortedInstitutions.map(item => item[0]),
            datasets: [{
                label: institutionsLabel,
                data: sortedInstitutions.map(item => item[1]),
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            plugins: { legend: { display: false }, title: { display: true, text: institutionsTitle } },
            scales: {
                x: {
                    beginAtZero: true
                },
                y: {
                    ticks: {
                        autoSkip: false
                    }
                }
            }
        }
    });

    const occupationTitle = occupationCanvas.getAttribute(`data-lang-${lang}-title`);

    const occupationCounts = attendees.map(a => a.occupation).filter(Boolean).reduce((acc, occ) => {
        acc[occ] = (acc[occ] || 0) + 1;
        return acc;
    }, {});

    const translatedLabels = Object.keys(occupationCounts).map(label => {
        return occupationTranslations[label] ? occupationTranslations[label][lang] || label : label;
    });

    window.occupationChart = new Chart(occupationCtx, {
        type: 'pie',
        data: {
            labels: translatedLabels,
            datasets: [{
                data: Object.values(occupationCounts),
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)', 'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)', 'rgba(75, 192, 192, 0.6)',
                    'rgba(153, 102, 255, 0.6)', 'rgba(255, 159, 64, 0.6)',
                    'rgba(255, 99, 132, 0.4)', 'rgba(54, 162, 235, 0.4)',
                    'rgba(255, 206, 86, 0.4)', 'rgba(75, 192, 192, 0.4)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: { title: { display: true, text: occupationTitle } }
        }
    });

    // Chart 3: Registrations by Week
    const registrationsByWeekCtx = registrationsByWeekCanvas.getContext('2d');
    const registrationsByWeekTitle = registrationsByWeekCanvas.getAttribute(`data-lang-${lang}-title`);
    const registrationsByWeekLabel = registrationsByWeekCanvas.getAttribute(`data-lang-${lang}-label`);

    const getWeek = (date) => {
        const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
        const dayNum = d.getUTCDay() || 7;
        d.setUTCDate(d.getUTCDate() + 4 - dayNum);
        const yearStart = new Date(Date.UTC(d.getUTCFullYear(),0,1));
        return Math.ceil((((d - yearStart) / 86400000) + 1)/7);
    };

    const weeklyCounts = attendees.reduce((acc, attendee) => {
        if (!attendee.timestamp) return acc;
        const [datePart] = attendee.timestamp.split(' ');
        const [day, month, year] = datePart.split('/');
        if (!year || !month || !day) return acc;
        const date = new Date(`${year}-${month}-${day}`);
        const week = `Week ${getWeek(date)}, ${year}`;
        acc[week] = (acc[week] || 0) + 1;
        return acc;
    }, {});

    const sortedWeeks = Object.keys(weeklyCounts).sort((a, b) => {
        const [, weekA, yearA] = a.match(/Week (\d+), (\d+)/);
        const [, weekB, yearB] = b.match(/Week (\d+), (\d+)/);
        return new Date(yearA, 0, 1 + (weekA - 1) * 7) - new Date(yearB, 0, 1 + (weekB - 1) * 7);
    });

    window.registrationsByWeekChart = new Chart(registrationsByWeekCtx, {
        type: 'line',
        data: {
            labels: sortedWeeks,
            datasets: [{
                label: registrationsByWeekLabel,
                data: sortedWeeks.map(week => weeklyCounts[week]),
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: registrationsByWeekTitle
                }
            }
        }
    });
}