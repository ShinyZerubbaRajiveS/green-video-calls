let callDuration = 0;  // Track the call duration in minutes
let intervalId = null; // For periodic updates

document.getElementById('callForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent default form submission

    const meetingLink = document.getElementById('meeting_link').value;
    const userId = document.getElementById('user_id').value;
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;

    // Send data to the server to start the call
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
        // Log the redirect_url for debugging
        console.log('Redirect URL:', data.redirect_url);

        // Check if the redirect_url is valid
        if (data.redirect_url) {
            window.open(/*data.redirect_url*/meetingLink, '_blank');  // Open the meeting link in a new tab
        } else {
            console.error('Redirect URL is not valid:', data.redirect_url);
            alert('Failed to open the meeting link. Please try again.');
        }

        // Start the real-time carbon footprint updates
        callDuration = 0;  // Reset call duration
        startRealTimeUpdates(data.call.id);  // Pass the call ID to start updates

        document.getElementById('results').style.display = 'block';  // Show results section
        updateFootprintDisplay(data.carbon_footprint);
        updateRecommendationsDisplay(data.recommendations);
        alert('Call started. Live carbon footprint calculations ongoing.');
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        alert('An error occurred while submitting the data: ' + error.message);
    });
});

function startRealTimeUpdates(callId) {
    // Update every 60 seconds (1 minute)
    intervalId = setInterval(() => {
        callDuration += 1;  // Increment call duration in minutes

        // Fetch updated carbon footprint from server
        fetch(`/update_call/${callId}?duration=${callDuration}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch updated data');
            }
            return response.json();
        })
        .then(data => {
            updateFootprintDisplay(data.carbon_footprint);
            updateRecommendationsDisplay(data.recommendations);

        })
        .catch(error => {
            console.error('Error fetching updated data:', error);
            stopRealTimeUpdates();  // Stop updates if there's an error
        });
    }, 60000);  // Update every 1 minute
}

function updateFootprintDisplay(footprint) {
    document.getElementById('footprint').innerText = `Carbon Footprint: ${footprint.carbon_emissions.toFixed(2)} kg CO2`;
    document.getElementById('energy_consumption').innerText = `Energy Consumption: ${footprint.energy_consumption.toFixed(2)} kWh`;
}

function updateRecommendationsDisplay(recommendations) {
    const recommendationsList = document.getElementById('recommendations');
    recommendationsList.innerHTML = '';  // Clear previous recommendations
    if (Array.isArray(recommendations)) {
        recommendations.forEach(rec => {
            const li = document.createElement('li');
            li.innerText = rec.recommendation_text;
            recommendationsList.appendChild(li);
        });
    } else {
        console.error('Recommendations data is not an array:', recommendations);
    }
}

// Function to stop live updates (optional)
function stopRealTimeUpdates() {
    if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
    }
}