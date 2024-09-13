document.getElementById('callForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission

    const meetingLink = document.getElementById('meeting_link').value;
    const userId = document.getElementById('user_id').value;
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;

    // Send data to the server
    fetch('/add_call', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            meeting_link: meetingLink,
            user_id: userId,
            username: username,
            email: email
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.error); });
        }
        return response.json();
    })
    .then(data => {
        // Open the meeting link in a new tab
        window.open(data.redirect_url, '_blank');  // Redirect to the meeting link in a new tab

        // Display the carbon footprint and recommendations
        document.getElementById('footprint').innerText = `Carbon Footprint: ${data.carbon_footprint.carbon_emissions.toFixed(2)} kg CO2`;
        const recommendationsList = document.getElementById('recommendations');
        recommendationsList.innerHTML = ''; // Clear previous recommendations
        const li = document.createElement('li');
        li.innerText = data.recommendation.recommendation_text; // Display the recommendation
        recommendationsList.appendChild(li);
        document.getElementById('results').style.display = 'block'; // Show results section

        // Display a success message to the user
        alert('Call data submitted successfully!');
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        alert('An error occurred while submitting the data: ' + error.message);
    });
});
