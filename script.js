document.getElementById('research-button').addEventListener('click', function() {
    const formContainer = document.querySelector('.form-container');
    const loadingContainer = document.getElementById('loading-container');
    const outputContainer = document.getElementById('output-container');
    const outputContent = document.getElementById('output-content');
    const researchButton = document.getElementById('research-button');

    // Collect all data from the form
    const researchInputs = {
        name: document.getElementById('name').value,
        linkedinUrl: document.getElementById('linkedin').value,
        repCompanyUrl: document.getElementById('company-url-1').value,
        productsServices: document.getElementById('products-services').value,
        territories: document.getElementById('territories').value,
        pitch: document.getElementById('pitch').value,
        targetCompanyUrl: document.getElementById('company-url-2').value,
        solutions: document.getElementById('solutions').value,
        opportunityName: document.getElementById('opportunity').value,
    };

    // Show loader and hide form
    formContainer.classList.add('hidden');
    researchButton.classList.add('hidden');
    loadingContainer.classList.remove('hidden');
    outputContainer.classList.add('hidden');

    // Define the backend URL as a root-relative path
    const backendUrl = '/research';

    // Send the data to the backend API
    fetch(backendUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(researchInputs),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        // Receive the dossier and display it
        loadingContainer.classList.add('hidden');
        
        if (data.dossier) {
            // A simple way to render Markdown-like line breaks and basic formatting
            let formattedDossier = data.dossier.replace(/\n/g, '<br>');
            outputContent.innerHTML = formattedDossier;
        } else {
             outputContent.innerHTML = "<h2>Error</h2><p>Received an empty response from the server.</p>";
        }
        
        outputContainer.classList.remove('hidden');
    })
    .catch(error => {
        // Handle any errors during the fetch operation
        console.error('Error during fetch operation:', error);
        loadingContainer.classList.add('hidden');
        
        // Display a user-friendly error message
        outputContent.innerHTML = `
            <h2>An Error Occurred</h2>
            <p>Could not retrieve the research dossier. Please check the browser console for details and ensure the backend is running correctly.</p>
            <p><strong>Error:</strong> ${error.message}</p>
        `;
        outputContainer.classList.remove('hidden');
    });
});
