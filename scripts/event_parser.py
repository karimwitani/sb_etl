import requests
import csv

# URL of the API endpoint
event_id = 1144
url = f"https://d29dxerjsp82wz.cloudfront.net/api/v3/event/live/{event_id}.json"  # Replace with the actual URL

# Function to get the fight details
def get_fight_details():
    # Make a request to the API
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Extract the fight card details
        fight_card = data["LiveEventDetail"]["FightCard"]
        
        # List to store fight details
        fight_details = []
        
        for fight in fight_card:
            # Get fighter names
            fighter_1 = f"{fight['Fighters'][0]['Name']['FirstName']} {fight['Fighters'][0]['Name']['LastName']}"
            fighter_2 = f"{fight['Fighters'][1]['Name']['FirstName']} {fight['Fighters'][1]['Name']['LastName']}"
            
            # Determine the winner
            if fight['Fighters'][0]['Outcome']['Outcome'] == "Win":
                winner = fighter_1
            elif fight['Fighters'][1]['Outcome']['Outcome'] == "Win":
                winner = fighter_2
            else:
                winner = "Draw"
            
            # Append the details to the list
            fight_details.append({
                "fighter_1": fighter_1,
                "fighter_2": fighter_2,
                "winner": winner
            })
        
        return fight_details
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return []

# Get the fight details
fights = get_fight_details()

# Define the CSV file name
csv_file = f"event_winner_details_{event_id}.csv"

# Write the fight details to a CSV file
with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["fighter_1", "fighter_2", "winner"])
    writer.writeheader()
    writer.writerows(fights)

print(f"Fight details have been written to {csv_file}")
