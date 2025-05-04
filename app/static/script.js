document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('callForm');
    const resultsDiv = document.getElementById('results');
    let callInterval = null;
    let currentCallId = null;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = {
            user_id: document.getElementById('user_id').value,
            meeting_link: document.getElementById('meeting_link').value,
            username: document.getElementById('username').value,
            email: document.getElementById('email').value
        };

        try {
            const response = await fetch('/add_call', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to start call');
            }

            const data = await response.json();
            currentCallId = data.call_id;
            
            // Open meeting link
            window.open(data.redirect_url, '_blank');
            
            // Show results
            resultsDiv.style.display = 'block';
            updateResults(data.carbon_footprint, data.recommendations);
            
            // Start live updates
            startLiveUpdates(currentCallId);
            
        } catch (error) {
            alert(`Error: ${error.message}`);
            console.error('Call error:', error);
        }
    });

    function startLiveUpdates(callId) {
        let duration = 0;
        
        // Update every minute
        callInterval = setInterval(async () => {
            duration += 1;
            
            try {
                const response = await fetch(`/update_call/${callId}?duration=${duration}`);
                if (!response.ok) throw new Error('Update failed');
                
                const data = await response.json();
                updateResults(data.carbon_footprint, data.recommendations);
                
            } catch (error) {
                console.error('Update error:', error);
                stopLiveUpdates();
            }
        }, 60000); // 1 minute
    }

    function stopLiveUpdates() {
        if (callInterval) {
            clearInterval(callInterval);
            callInterval = null;
        }
    }

    function updateResults(footprint, recommendations) {
        document.getElementById('footprint').textContent = 
            `Carbon Footprint: ${footprint.carbon_emissions} kg CO2`;
        
        document.getElementById('energy_consumption').textContent = 
            `Energy Used: ${footprint.energy_consumption} kWh`;
        
        const recList = document.getElementById('recommendations');
        recList.innerHTML = '';
        
        recommendations.forEach(rec => {
            const li = document.createElement('li');
            li.textContent = rec;
            recList.appendChild(li);
        });
    }

    // Clean up on page exit
    window.addEventListener('beforeunload', () => {
        stopLiveUpdates();
    });
});