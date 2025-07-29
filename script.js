// script.js

document.getElementById('research-button').addEventListener('click', function() {
    const formContainer = document.querySelector('.form-container');
    const loadingContainer = document.getElementById('loading-container');
    const outputContainer = document.getElementById('output-container');
    const outputContent = document.getElementById('output-content');
    const researchButton = document.getElementById('research-button');

    // --- 1. Collect all data from the form ---
    const researchInputs = {
        name: document.getElementById('name').value,
        linkedinUrl: document.getElementById('linkedin').value,
        repCompanyUrl: document.getElementById('company-url-1').value, // URL for the rep's company
        productsServices: document.getElementById('products-services').value,
        territories: document.getElementById('territories').value,
        pitch: document.getElementById('pitch').value,
        targetCompanyUrl: document.getElementById('company-url-2').value, // URL for the target company
        solutions: document.getElementById('solutions').value,
        opportunityName: document.getElementById('opportunity').value,
    };

    // --- 2. Show loader and disable button ---
    formContainer.classList.add('hidden');
    researchButton.classList.add('hidden'); // Hide the button as well
    loadingContainer.classList.remove('hidden');
    outputContainer.classList.add('hidden'); // Ensure output is hidden

    // --- 3. Send data to your backend API ---
    // Make sure your backend is running. For local testing, this will be http://localhost:8080
    // When deployed, this will be your serverless application's URL.
    const backendUrl = 'https://serverless.on-demand.io/apps/donnaprototype/research'; 

    fetch(backendUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(researchInputs),
    })
    .then(response => {
        if (!response.ok) {
            // Handle HTTP errors like 500, 404 etc.
            throw new Error(`Network response was not ok: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        // --- 4. Receive the dossier and display it ---
        loadingContainer.classList.add('hidden');
        
        // The backend sends a 'dossier' key.
        // Using innerHTML to render Markdown formatting (like bold, lists) from the AI.
        // NOTE: This is safe here because we trust the source (our AI backend).
        // For untrusted sources, you would use a library to sanitize the HTML.
        outputContent.innerHTML = data.dossier.replace(/\n/g, '<br>'); // A simple way to respect line breaks
        
        outputContainer.classList.remove('hidden');
    })
    .catch(error => {
        // --- 5. Handle any errors ---
        console.error('Error during fetch operation:', error);
        loadingContainer.classList.add('hidden');
        
        // Display a user-friendly error message
        outputContent.innerHTML = `
            <h2>An Error Occurred</h2>
            <p>Could not retrieve the research dossier. Please check the console for details and ensure the backend server is running.</p>
            <p><strong>Error:</strong> ${error.message}</p>
        `;
        outputContainer.classList.remove('hidden');
    });
});
