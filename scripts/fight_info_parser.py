import requests
import csv
import json
import os
import pandas as pd


# Function to get the fight details
def get_fighter_details(json_file_path):
    print(json_file_path)
    with open(json_file_path, 'r') as fh:
        data = json.load(fh)
    
    # Extract the fight card details
    fight_card = data["LiveEventDetail"]["FightCard"]
    
    # List to store fight details
    fighter_details = []
    
    for fight in fight_card:
        # Get fighter names
        fighter_1_name = f"{fight['Fighters'][0]['Name']['FirstName']} {fight['Fighters'][0]['Name']['LastName']}"
        fighter_2_name = f"{fight['Fighters'][1]['Name']['FirstName']} {fight['Fighters'][1]['Name']['LastName']}"
        fighter_1_id = fight['Fighters'][0]['FighterId']
        fighter_2_id = fight['Fighters'][1]['FighterId']
        
        # Append the details to the list
        fighter_details.append({
            "fighter_name": fighter_1_name,
            "fighter_id": fighter_1_id,
        })
        fighter_details.append({
            "fighter_name": fighter_2_name,
            "fighter_id": fighter_2_id,
        })
    
    return fighter_details

# Get the fight details
fighters = get_fighter_details("/Users/karim/Developer/repos/reddit-topic-scraping/sports-betting/dropzone/ufc/1/ufc_data_1-1.json")

# fighter_details_full = []
# base_dir = "/Users/karim/Developer/repos/reddit-topic-scraping/sports-betting/dropzone/ufc/"
# for folder in os.listdir(base_dir):
#     for file in os.listdir(f"{base_dir}{folder}"):
#         fighter_details = get_fighter_details(f"{base_dir}{folder}/{file}")
#         fighter_details_full.extend(fighter_details)


# print(fighters)
# # Write the fight details to a CSV file
# with open("./fighter_details.csv", mode='w', newline='') as file:
#     writer = csv.DictWriter(file, fieldnames=["fighter_name", "fighter_id"])
#     writer.writeheader()
#     writer.writerows(fighter_details_full)

df = pd.read_csv("./fighter_details.csv")
print(len(df))
df  = df.drop_duplicates()
print(len(df))
df.to_csv("./fighter_details.csv", index=False)

# print(f"Fight details have been written to ./fighter_details.csv")
