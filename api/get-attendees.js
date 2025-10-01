const fetch = require('node-fetch');

exports.handler = async function(event, context) {
    const sheetId = '1lBkYPPzjLCO8j5QQ-98Kh5vxv0I3BXpBQCqCNvWXjTg';
    const sheetName = 'Respostas ao formulário 1';
    // The API key is stored as a secure environment variable on the server.
    const apiKey = process.env.GOOGLE_SHEETS_API_KEY;
    const url = `https://sheets.googleapis.com/v4/spreadsheets/${sheetId}/values/${encodeURIComponent(sheetName)}?key=${apiKey}`;

    try {
        const response = await fetch(url);
        if (!response.ok) {
            return {
                statusCode: response.status,
                body: JSON.stringify({ error: `Google Sheets API error: ${response.statusText}` })
            };
        }
        const data = await response.json();
        const rows = data.values || [];

        // Remove header row and map to a clean array of objects with only the required fields.
        const attendees = rows.slice(1).map(row => ({
            timestamp: row[0] || '',
            name: row[1] || '',
            institution: row[4] || '', // Corrected column index for Institution
            occupation: row[5] || ''  // Corrected column index for Occupation
        }));

        return {
            statusCode: 200,
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*' // Allow requests from any origin
            },
            body: JSON.stringify(attendees)
        };
    } catch (error) {
        console.error('Error in serverless function:', error);
        return {
            statusCode: 500,
            body: JSON.stringify({ error: 'Failed to fetch data from Google Sheet.' })
        };
    }
};