// Tokenization Frontend JavaScript
console.log('Tokenization Frontend Loaded');

// API Base URL - works with both Python and Rust backends
const API_BASE = '/api';

// Function to fetch components from the backend API
async function fetchComponents() {
    try {
        const response = await fetch(`${API_BASE}/components`);
        const data = await response.json();
        console.log('Components:', data);
        displayComponents(data);
        return data;
    } catch (error) {
        console.error('Error fetching components:', error);
        displayError('Failed to fetch components: ' + error.message);
    }
}

// Function to fetch components by type
async function fetchComponentsByType(type) {
    try {
        const response = await fetch(`${API_BASE}/components/${encodeURIComponent(type)}`);
        const data = await response.json();
        console.log(`Components for type ${type}:`, data);
        displayComponents(data);
        return data;
    } catch (error) {
        console.error(`Error fetching components for type ${type}:`, error);
        displayError(`Failed to fetch components for type ${type}: ` + error.message);
    }
}

// Function to display components in the UI
function displayComponents(apiResponse) {
    const container = document.getElementById('components-container');
    
    if (!apiResponse.success) {
        displayError(apiResponse.message || 'Failed to fetch components');
        return;
    }
    
    if (!apiResponse.data || apiResponse.data.length === 0) {
        container.innerHTML = '<div class="loading">No components found</div>';
        return;
    }
    
    let html = '';
    apiResponse.data.forEach(component => {
        html += `
            <div class="component">
                <h3>${component.main_type} - ${component.sub_type}</h3>
                <div class="component-type">
                    <strong>Main Type:</strong> ${component.main_type}
                </div>
                <div class="component-subtype">
                    <strong>Sub Type:</strong> ${component.sub_type}
                </div>
                <div class="component-details">
                    <strong>Components:</strong> ${component.components}
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

// Function to display errors in the UI
function displayError(message) {
    const container = document.getElementById('components-container');
    container.innerHTML = `<div class="error">${message}</div>`;
}

// Initialize the app
document.addEventListener('DOMContentLoaded', async () => {
    console.log('App initialized');
    // Fetch all components when the app loads
    await fetchComponents();
    
    // Add event listeners for filtering
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(button => {
        button.addEventListener('click', async () => {
            const type = button.getAttribute('data-type');
            if (type === 'all') {
                await fetchComponents();
            } else {
                await fetchComponentsByType(type);
            }
        });
    });
});