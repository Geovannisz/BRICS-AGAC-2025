const fetch = require('node-fetch');

exports.handler = async function(event, context) {
    const sheetId = '1lBkYPPzjLCO8j5QQ-98Kh5vxv0I3BXpBQCqCNvWXjTg';
    const sheetName = 'Respostas ao formulário 1';
    // The API key is stored as a secure environment variable on the server.
    const apiKey = process.env.GOOGLE_SHEETS_API_KEY;
    // We only need to fetch a single column to get the count, which is more efficient.
    const url = `https://sheets.googleapis.com/v4/spreadsheets/${sheetId}/values/${encodeURIComponent(sheetName)}!A:A?key=${apiKey}`;

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

        // The first row is the header, so we subtract it from the count.
        const registrationCount = rows.length > 0 ? rows.length - 1 : 0;

        return {
            statusCode: 200,
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*' // Allow requests from any origin
            },
            body: JSON.stringify({ count: registrationCount })
        };
    } catch (error) {
        console.error('Error in serverless function:', error);
        return {
            statusCode: 500,
            body: JSON.stringify({ error: 'Failed to fetch registration count.' })
        };
    }
};