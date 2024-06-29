import json
import csv
import os

# Function to read JSON file
def read_json_file(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
    return data

# Function to write CSV file
def write_csv_file(data_list, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['data_pull_date', 'meet_name', 'meet_date', 'competitor_1_name', 'competitor_1_odds', 'competitor_2_name', 'competitor_2_odds']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        
        for data in data_list:
            
            data_pull_date = data['data_pull_date']
            for event in data['betting_data']:
                try:
                    meet_name = event['meet_name']
                    meet_date = event['meet_date']
                    
                    for fight in event['fights']:
                        competitor_1 = fight.get('competitor_1', {})
                        competitor_2 = fight.get('competitor_2', {})

                        if (competitor_1.get('odds', '').lower() == 'suspended' or
                                competitor_2.get('odds', '').lower() == 'suspended'):
                            continue
                        competitor_1_name = fight['competitor_1']['name']
                        competitor_1_odds = fight['competitor_1']['odds']
                        competitor_2_name = fight['competitor_2']['name']
                        competitor_2_odds = fight['competitor_2']['odds']
                        
                        writer.writerow({
                            'data_pull_date': data_pull_date,
                            'meet_name': meet_name,
                            'meet_date': meet_date,
                            'competitor_1_name': competitor_1_name,
                            'competitor_1_odds': competitor_1_odds,
                            'competitor_2_name': competitor_2_name,
                            'competitor_2_odds': competitor_2_odds
                        })
                except Exception as e:
                    print(e)
                    print(data_pull_date)
                    print(event)


# Main function
def main():
    directory = "./betvictor_odds_json/"
    output_file = "./betvictor_odds_csv/betvictor_data_pull_full.csv"
 
    data_list = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            # Read JSON data from file
            data = read_json_file(file_path)
            data_list.append(data)

    # Write CSV file
    write_csv_file(data_list, output_file)
    
    print(f"Data from all JSON files in {directory} has been successfully written to {output_file}")

if __name__ == "__main__":
    main()
