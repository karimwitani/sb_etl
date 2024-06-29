import requests
import csv

# Initialize an empty list to store the event details
event_details = []

# Loop through event IDs from 1180 to 1220
for event_id in range(1100, 2020):
    # Construct the full URL with the event ID
    url = f"https://d29dxerjsp82wz.cloudfront.net/api/v3/event/live/{event_id}.json"
    
    # Perform the GET request
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Extract the required fields
        event_id = data.get('LiveEventDetail', {}).get('EventId')
        event_name = data.get('LiveEventDetail', {}).get('Name')
        event_date = data['LiveEventDetail']['StartTime'].split('T')[0] if data.get('LiveEventDetail') else None
        
        # Append the extracted details to the list
        if event_id and event_name:
            event_details.append({
                'event_id': event_id,
                'event_name': event_name,
                'event_date': event_date
            })
    else:
        print(f"Failed to retrieve event ID {event_id}. Status code: {response.status_code}")

# Define the CSV file path
csv_file_path = 'event_details.csv'

# Write the event details to the CSV file
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['event_id', 'event_name','event_date'])
    writer.writeheader()
    writer.writerows(event_details)

print(f"Event details have been written to {csv_file_path}")
