// document.getElementById('callForm').addEventListener('submit', function(event) {
//     event.preventDefault(); // Prevent default form submission

//     const meetingLink = document.getElementById('meeting_link').value;
//     const userId = document.getElementById('user_id').value;
//     const username = document.getElementById('username').value;
//     const email = document.getElementById('email').value;

//     // Send data to the server
//     fetch('/add_call', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({
//             meeting_link: meetingLink,
//             user_id: userId,
//             username: username,
//             email: email
//         })
//     })
//     .then(response => {
//         if (!response.ok) {
//             return response.json().then(err => { throw new Error(err.error); });
//         }
//         return response.json();
//     })
//     .then(data => {
//         // Open the meeting link in a new tab
//         window.open(data.redirect_url, '_blank');  // Redirect to the meeting link in a new tab

//         // Display the carbon footprint and recommendations
//         document.getElementById('footprint').innerText = `Carbon Footprint: ${data.carbon_footprint.carbon_emissions.toFixed(2)} kg CO2`;
//         const recommendationsList = document.getElementById('recommendations');
//         recommendationsList.innerHTML = ''; // Clear previous recommendations
//         const li = document.createElement('li');
//         li.innerText = data.recommendation.recommendation_text; // Display the recommendation
//         recommendationsList.appendChild(li);
//         document.getElementById('results').style.display = 'block'; // Show results section

//         // Display a success message to the user
//         alert('Call data submitted successfully!');
//     })
//     .catch(error => {
//         console.error('There was a problem with the fetch operation:', error);
//         alert('An error occurred while submitting the data: ' + error.message);
//     });
// });
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
        // Open the meeting link in a new tab
        window.open(data.redirect_url, '_blank');  // Redirect to the meeting link in a new tab

        // Start the real-time carbon footprint updates
        callDuration = 0;  // Reset call duration
        startRealTimeUpdates(data.call.id);  // Pass the call ID to start updates

        document.getElementById('results').style.display = 'block';  // Show results section
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
        .then(response => response.json())
        .then(data => {
            document.getElementById('footprint').innerText = `Carbon Footprint: ${data.carbon_footprint.carbon_emissions.toFixed(2)} kg CO2`;
            document.getElementById('energy_consumption').innerText = `Energy Consumption: ${data.carbon_footprint.energy_consumption.toFixed(2)} kWh`;

            const recommendationsList = document.getElementById('recommendations');
            recommendationsList.innerHTML = '';  // Clear previous recommendations
            const li = document.createElement('li');
            li.innerText = data.recommendation.recommendation_text;
            recommendationsList.appendChild(li);
        });
    }, 60000);  // Update every 1 minute
}

// Function to stop live updates (optional)
function stopRealTimeUpdates() {
    if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
    }
}
