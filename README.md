
# Green Video Calls

Green Video Calls is an environmental awareness web application that calculates the carbon footprint of your video meetings in real-time. It provides personalized recommendations to reduce digital carbon emissions and promotes greener communication habits.


## Features

- #### Carbon Footprint Calculation
Computes emissions based on device type, internet speed, resolution, and call duration.

- #### Real-Time Tracking
Live monitoring of your ongoing call duration and emission impact.

- #### Eco-Friendly Suggestions
Personalized tips and recommendations to reduce your carbon output.

- #### Update Calls
Modify and re-calculate emissions for calls in progress or recently ended.


## Technologies Used

- #### Frontend:
HTML, CSS, JavaScript

- #### Backend:
Python Flask

SQLAlchemy

PostgreSQL 

- #### Others:
Internet speed test library

Device detection APIs

Webcam resolution checker 
##  Setup Instructions
1. #### Clone the repository
```bash
git clone https://github.com/your-username/green-video-calls.git
cd green-video-calls
```

2. #### Create a virtual environment and activate it
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```


3. #### Install dependencies
```bash
pip install -r requirements.txt
```


4. #### Run the application
```bash
python run.py
```


5. #### Open the frontend
Navigate to localhost:5000 in your browser.


## Sample flow

1. User submits video call details via a web form.

2. Backend calculates carbon emissions based on:

- Duration

- Internet speed

- Device specifications

- Webcam resolution

3. Recommendations are generated.

4. Real-time updates occur during the call.
## Demo


https://github.com/user-attachments/assets/0b149eec-ca97-4df3-b76b-1ac4c981d82a