import requests
import csv

# Function to get event details from the API
def get_event_details(event_id):
    url = f"https://d29dxerjsp82wz.cloudfront.net/api/v3/event/live/{event_id}.json"  # Replace with the actual URL pattern
    print(f'fetching {event_id}')
    response = requests.get(url)
    
    if response.status_code == 200:
        print('response 200')
        return response.json()
    else:
        print(f"Failed to fetch data for event ID {event_id}: {response.status_code}")
        return None

# Function to process event data and write to CSV
def write_csv_file(event_ids, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['ufc_event_id', 'ufc_fight_id', 'event_name', 'event_date', 'fighter_1_name', 'fighter_1_id', 'fighter_2_name', 'fighter_2_id', 'winner', 'winner_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for event_id in event_ids:
            data = get_event_details(event_id)
            if data:
                event_details = data.get('LiveEventDetail', {})
                event_name = event_details.get('Name', 'N/A')
                event_date = event_details.get('StartTime', 'N/A')
                
                for fight in event_details.get('FightCard', []):
                    fight_id = fight.get('FightId', {})
                    competitor_1 = fight.get('Fighters', [{}])[0]
                    competitor_2 = fight.get('Fighters', [{}])[1] if len(fight.get('Fighters', [])) > 1 else {}

                    fighter_1_name = f"{competitor_1.get('Name', {}).get('FirstName', 'N/A')} {competitor_1.get('Name', {}).get('LastName', 'N/A')}"
                    fighter_2_name = f"{competitor_2.get('Name', {}).get('FirstName', 'N/A')} {competitor_2.get('Name', {}).get('LastName', 'N/A')}"
                    fighter_1_id = competitor_1.get('FighterId', {})
                    fighter_2_id = competitor_2.get('FighterId', {})


                    if competitor_1.get('Outcome', {}).get('Outcome', '') == 'Win':
                        winner = fighter_1_name
                        winner_id = fighter_1_id
                    elif competitor_2.get('Outcome', {}).get('Outcome', '') == 'Win':
                        winner = fighter_2_name
                        winner_id = fighter_2_id
                    else:
                        winner = 'Draw'
                        winner_id = None

                    writer.writerow({
                        'ufc_event_id': event_id,
                        'ufc_fight_id': fight_id,
                        'event_name': event_name,
                        'event_date': event_date,
                        'fighter_1_name': fighter_1_name,
                        'fighter_1_id': fighter_1_id,
                        'fighter_2_name': fighter_2_name,
                        'fighter_2_id': fighter_2_id,
                        'winner': winner,
                        'winner_id': winner_id
                    })

# Main function
def main():
    start_event_id = 1144
    end_event_id = 1213
    output_file = './ufc_fight_winner.csv'

    event_ids = range(start_event_id, end_event_id + 1)
    
    # Write CSV file
    write_csv_file(event_ids, output_file)
    
    print(f"Data from events {start_event_id} to {end_event_id} has been successfully written to {output_file}")

if __name__ == "__main__":
    main()
