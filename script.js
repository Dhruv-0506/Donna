document.getElementById('research-button').addEventListener('click', function() {
    const formContainer = document.querySelector('.form-container');
    const loadingContainer = document.getElementById('loading-container');
    const outputContainer = document.getElementById('output-container');
    const outputContent = document.getElementById('output-content');

    // Hide form and show loader
    formContainer.classList.add('hidden');
    loadingContainer.classList.remove('hidden');
    outputContainer.classList.add('hidden');

    // Simulate a backend process (e.g., an API call to your LLM)
    setTimeout(() => {
        // This is where you would fetch the data from your backend
        const researchData = `
Company: Stark Industries
LinkedIn: https://www.linkedin.com/company/stark-industries
Products/Services: Advanced weaponry, renewable energy, arc reactor technology.
Territories: Global
Positioning Pitch: "Pioneering technology for a better, safer future. Stark Industries delivers cutting-edge solutions that redefine what's possible."

---

Solutions to Position:
- Arc Reactor for sustainable energy solutions.
- Iron Man suit technology for advanced defense applications.

Opportunity Name: Global Energy Crisis Solution
        `;

        // Hide loader and display output
        loadingContainer.classList.add('hidden');
        outputContent.innerText = researchData;
        outputContainer.classList.remove('hidden');
    }, 3000); // Simulate a 3-second loading time
});
