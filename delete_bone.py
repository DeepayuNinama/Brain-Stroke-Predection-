import os
import shutil
from pathlib import Path

# Set the path to the Patients_CT directory
currentDir = Path(os.getcwd())
datasetDir = Path(currentDir, 'Patients_CT')

# Define the patient number range
start_patient = 49
end_patient = 130

# Loop through each patient folder from 049 to 130
for sNo in range(start_patient, end_patient + 1):
    # Create the path to the current patient's folder (e.g., '049', '050', etc.)
    patient_folder = datasetDir / f"{sNo:0=3d}"
    
    # Check if the patient folder exists
    if patient_folder.exists():
        # Define the path to the 'bone' folder within the patient's folder
        bone_folder = patient_folder / 'bone'
        
        # If the 'bone' folder exists, delete it
        if bone_folder.exists() and bone_folder.is_dir():
            try:
                # First, delete all contents of the 'bone' folder
                for root, dirs, files in os.walk(bone_folder, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))  # Delete files
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))  # Delete subdirectories
                
                # After deleting all files and subdirectories, delete the 'bone' folder itself
                os.rmdir(bone_folder)
                print(f"Deleted: {bone_folder}")
            except Exception as e:
                print(f"Error deleting {bone_folder}: {e}")
        else:
            print(f"No 'bone' folder found for patient {sNo:0=3d}")
    else:
        print(f"Patient folder {sNo:0=3d} not found.")
