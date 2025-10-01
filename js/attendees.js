// js/attendees.js

document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM content loaded. Starting attendees script.");
    fetchAttendeeData();
});

// Function to parse CSV text into an array of objects, handling quoted fields.
function parseCSV(text) {
    console.log("1. Entering parseCSV function.");
    try {
        const lines = text.trim().split(/\r?\n/);
        if (lines.length < 2) {
            console.warn("CSV has less than 2 lines. No data to parse.");
            return [];
        }

        const headers = lines[0].split(',').map(h => h.trim().replace(/^"|"$/g, ''));
        console.log("Parsed headers:", headers);

        const rows = lines.slice(1).map(line => {
            if (!line.trim()) return null;

            const obj = {};
            const values = [];
            let current = '';
            let inQuotes = false;

            for (let i = 0; i < line.length; i++) {
                const char = line[i];
                if (char === '"' && (i === 0 || line[i - 1] === ',' || line[i + 1] === ',' || i === line.length - 1)) {
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

        console.log(`2. Successfully parsed ${rows.length} rows.`);
        if (rows.length > 0) {
            console.log("Sample of first parsed row:", rows[0]);
        }
        return rows;
    } catch (error) {
        console.error("Error during CSV parsing:", error);
        return []; // Return empty array on error
    }
}

async function fetchAttendeeData() {
    console.log("3. Entering fetchAttendeeData function.");
    const url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSDhHAo69dtSs8Snd2wPwlw70K3k9Hvg2Z9nMAG-s3L8bjAjpamz1aUdDdMinSOgS0r9E264eVWrkz7/pub?gid=899626177&single=true&output=csv';
    const tbody = document.getElementById('attendees-tbody');

    if (!tbody) {
        console.error('CRITICAL: Attendees table body not found. Cannot proceed.');
        return;
    }

    try {
        console.log("4. Fetching data from URL:", url);
        const response = await fetch(url);
        console.log(`5. Fetch response status: ${response.status}`);
        if (!response.ok) {
            throw new Error(`CSV fetch error: ${response.status}`);
        }
        const csvText = await response.text();
        console.log("6. Successfully fetched CSV text. Length:", csvText.length);

        const attendees = parseCSV(csvText).map(row => ({
            timestamp: row['Timestamp'] || '',
            name: row['Full Name'] || '',
            institution: row['University/Institution'] || '',
            occupation: row['Student Status/Degree or Occupation'] || ''
        }));
        console.log(`7. Mapped CSV data to ${attendees.length} attendee objects.`);
        if (attendees.length > 0) {
            console.log("Sample of first mapped attendee object:", attendees[0]);
        }

        console.log("8. Calling rendering functions...");
        populateTable(attendees);
        setupSearch(attendees);
        setupSorting();
        createCharts(attendees);
        console.log("9. All rendering functions called.");

    } catch (error) {
        console.error('CRITICAL ERROR in fetchAttendeeData:', error);
        tbody.innerHTML = `<tr><td colspan="4" class="text-center">Error loading data. Please check the console for details.</td></tr>`;
    }
}

function populateTable(attendees) {
    console.log("...Populating table with", attendees.length, "attendees.");
    const tbody = document.getElementById('attendees-tbody');
    tbody.innerHTML = '';

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
    console.log("...Setting up search functionality.");
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
    console.log("...Setting up sorting functionality.");
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
    console.log("...Creating charts.");
    if (attendees.length === 0) return;
    const lang = localStorage.getItem('brics-agac-lang') || 'en';

    if (window.institutionsChart) window.institutionsChart.destroy();
    if (window.occupationChart) window.occupationChart.destroy();

    const institutionsCanvas = document.getElementById('institutions-chart');
    const occupationCanvas = document.getElementById('occupation-chart');
    if (!institutionsCanvas || !occupationCanvas) {
        console.error("CRITICAL: Chart canvas element not found.");
        return;
    }

    const institutionsCtx = institutionsCanvas.getContext('2d');
    const occupationCtx = occupationCanvas.getContext('2d');

    // ... rest of chart logic
    const institutionsTitle = institutionsCanvas.getAttribute(`data-lang-${lang}-title`);
    const institutionsLabel = institutionsCanvas.getAttribute(`data-lang-${lang}-label`);

    const institutionCounts = attendees.map(a => a.institution).filter(Boolean).reduce((acc, inst) => {
        acc[inst] = (acc[inst] || 0) + 1;
        return acc;
    }, {});

    const sortedInstitutions = Object.entries(institutionCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10)
        .reverse();

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
            scales: { x: { beginAtZero: true } }
        }
    });

    const occupationTitle = occupationCanvas.getAttribute(`data-lang-${lang}-title`);

    const occupationCounts = attendees.map(a => a.occupation).filter(Boolean).reduce((acc, occ) => {
        acc[occ] = (acc[occ] || 0) + 1;
        return acc;
    }, {});

    window.occupationChart = new Chart(occupationCtx, {
        type: 'pie',
        data: {
            labels: Object.keys(occupationCounts),
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
}