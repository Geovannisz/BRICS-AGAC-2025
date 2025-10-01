// js/attendees.js

document.addEventListener('DOMContentLoaded', function() {
    fetchAttendeeData();
});

async function fetchAttendeeData() {
    const url = '/api/get-attendees'; // Use the secure serverless function
    const tbody = document.getElementById('attendees-tbody');

    if (!tbody) {
        console.error('Attendees table body not found.');
        return;
    }

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        const attendees = await response.json();

        populateTable(attendees);
        setupSearch(attendees);
        setupSorting(); // No change needed here, as it works on the DOM
        createCharts(attendees);

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
            <td>${attendee.timestamp || ''}</td>
            <td>${attendee.name || ''}</td>
            <td>${attendee.institution || ''}</td>
            <td>${attendee.occupation || ''}</td>
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
            // Search through the values of the attendee object
            return Object.values(attendee).some(value =>
                value.toLowerCase().includes(searchTerm)
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

    // Destroy existing charts if they exist to prevent canvas reuse issues
    if (window.institutionsChart) {
        window.institutionsChart.destroy();
    }
    if (window.occupationChart) {
        window.occupationChart.destroy();
    }

    // Chart 1: Top 10 Institutions (Horizontal Bar)
    const institutionsCanvas = document.getElementById('institutions-chart');
    const institutionsCtx = institutionsCanvas.getContext('2d');
    const institutionsTitle = institutionsCanvas.getAttribute(`data-lang-${lang}-title`);
    const institutionsLabel = institutionsCanvas.getAttribute(`data-lang-${lang}-label`);

    const institutions = attendees.map(attendee => attendee.institution).filter(Boolean);
    const institutionCounts = institutions.reduce((acc, inst) => {
        acc[inst] = (acc[inst] || 0) + 1;
        return acc;
    }, {});

    const sortedInstitutions = Object.entries(institutionCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10)
        .reverse(); // Reverse to show the highest value at the top

    const institutionLabels = sortedInstitutions.map(item => item[0]);
    const institutionData = sortedInstitutions.map(item => item[1]);

    window.institutionsChart = new Chart(institutionsCtx, {
        type: 'bar',
        data: {
            labels: institutionLabels,
            datasets: [{
                label: institutionsLabel,
                data: institutionData,
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: institutionsTitle
                }
            },
            scales: {
                x: {
                    beginAtZero: true
                }
            }
        }
    });

    // Chart 2: Distribution by Occupation
    const occupationCanvas = document.getElementById('occupation-chart');
    const occupationCtx = occupationCanvas.getContext('2d');
    const occupationTitle = occupationCanvas.getAttribute(`data-lang-${lang}-title`);

    const occupations = attendees.map(attendee => attendee.occupation).filter(Boolean);
    const occupationCounts = occupations.reduce((acc, occ) => {
        acc[occ] = (acc[occ] || 0) + 1;
        return acc;
    }, {});

    const occupationLabels = Object.keys(occupationCounts);
    const occupationData = Object.values(occupationCounts);

    window.occupationChart = new Chart(occupationCtx, {
        type: 'pie',
        data: {
            labels: occupationLabels,
            datasets: [{
                data: occupationData,
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
            plugins: {
                title: {
                    display: true,
                    text: occupationTitle
                }
            }
        }
    });
}