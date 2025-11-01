const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');

const app = express();
const PORT = 3030;

// Middleware
app.use(cors());
app.use(express.json());

// Serve static files from the frontend directory
app.use(express.static(path.join(__dirname, 'tokenize_frontend')));

// In-memory storage for components
let components = [];

// Function to parse CSV file
function parseCSV() {
    return new Promise((resolve, reject) => {
        const results = [];
        fs.createReadStream('tokenization_digital_wallet.csv')
            .pipe(csv())
            .on('data', (data) => {
                // Skip header row
                if (data['Main Type'] !== 'Main Type') {
                    results.push({
                        id: results.length + 1,
                        main_type: data['Main Type'] || '',
                        sub_type: data['Sub Type'] || '',
                        components: data['Components'] || ''
                    });
                }
            })
            .on('end', () => {
                resolve(results);
            })
            .on('error', (error) => {
                reject(error);
            });
    });
}

// Initialize components from CSV
async function initializeComponents() {
    try {
        components = await parseCSV();
        console.log(`Loaded ${components.length} components from CSV`);
    } catch (error) {
        console.error('Error parsing CSV:', error);
    }
}

// API Routes

// Get all components
app.get('/api/components', (req, res) => {
    res.json({
        success: true,
        data: components,
        message: null
    });
});

// Get components by main type
app.get('/api/components/:mainType', (req, res) => {
    const mainType = req.params.mainType;
    const filteredComponents = components.filter(c => c.main_type === mainType);
    
    res.json({
        success: true,
        data: filteredComponents,
        message: filteredComponents.length === 0 ? `No components found for type: ${mainType}` : null
    });
});

// Get components by main type and sub type
app.get('/api/components/:mainType/:subType', (req, res) => {
    const mainType = req.params.mainType;
    const subType = req.params.subType;
    const filteredComponents = components.filter(c => c.main_type === mainType && c.sub_type === subType);
    
    res.json({
        success: true,
        data: filteredComponents,
        message: filteredComponents.length === 0 ? `No components found for type: ${mainType} and subtype: ${subType}` : null
    });
});

// Serve index.html for all other routes (for SPA)
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'tokenize_frontend', 'index.html'));
});

// Initialize and start server
initializeComponents().then(() => {
    app.listen(PORT, () => {
        console.log(`Server is running on http://localhost:${PORT}`);
        console.log(`API endpoints available at http://localhost:${PORT}/api/components`);
    });
});