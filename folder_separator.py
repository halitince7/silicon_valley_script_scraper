import os
import shutil
import re

def create_season_folders():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    scripts_dir = os.path.join(current_dir, 'scripts')
    
    # Create a dictionary to store season numbers and their corresponding files
    season_files = {}
    
    # Iterate through all files in the scripts directory
    for filename in os.listdir(scripts_dir):
        if filename.endswith('.txt'):
            # Extract season number using regex
            match = re.match(r's(\d+)e\d+\.txt', filename)
            if match:
                season_num = match.group(1)
                if season_num not in season_files:
                    season_files[season_num] = []
                season_files[season_num].append(filename)
    
    # Create folders and move files
    for season_num, files in season_files.items():
        # Create season folder
        season_folder = os.path.join(scripts_dir, f's{season_num}')
        os.makedirs(season_folder, exist_ok=True)
        
        # Move files to season folder
        for file in files:
            src = os.path.join(scripts_dir, file)
            dst = os.path.join(season_folder, file)
            shutil.move(src, dst)
            print(f"Moved {file} to {season_folder}")

if __name__ == "__main__":
    create_season_folders()
    print("Folder organization completed!")
