import json
import glob
import os

def load_teams():
    all_teams = []
    path = "assets/teams/*.json"
    
    files = glob.glob(path)
    
    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                
                if isinstance(data, list):
                    all_teams.extend(data)
                else:
                    all_teams.append(data)
                    
        except Exception as e:
            print(f"Error loading {file_path}: {e}")

    if not all_teams:
        print("Warning: No teams loaded!")
        
    return all_teams