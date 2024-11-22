import os
import shutil
import pandas as pd
from pathlib import Path

# Set the path to the Patients_CT directory and Brain_Data_Organised directory
currentDir = Path(os.getcwd())
datasetDir = Path(currentDir, 'Patients_CT')
organisedDir = Path(currentDir, 'Brain_Data_Organised')

# Create the main directories for Normal and Stroke if they don't exist
normal_dir = organisedDir / 'Normal'
stroke_dir = organisedDir / 'Stroke'

if not normal_dir.exists():
    normal_dir.mkdir(parents=True)
if not stroke_dir.exists():
    stroke_dir.mkdir(parents=True)

# Read the patient demographics CSV file
demographics_df = pd.read_csv(Path(currentDir, 'patient_demographics.csv'))

# Loop through each row in the CSV file
for _, row in demographics_df.iterrows():
    patient_number = row['Patient Number']
    condition = row['Condition on file']
    
    # Create the path to the patient's folder (e.g., 049, 050, etc.)
    patient_folder = datasetDir / f"{patient_number:0=3d}"
    
    # Check if the patient folder exists
    if patient_folder.exists():
        brain_folder = patient_folder / 'brain'
        
        # Check if the 'brain' folder exists
        if brain_folder.exists():
            # Define the destination folder based on the 'Condition' column
            if condition == 'Normal CT':
                destination_folder = normal_dir
                image_range = range(1, 1552)  # Indices 1 to 1551
            else:
                destination_folder = stroke_dir
                image_range = range(1, 951)  # Indices 1 to 950
                
            # Copy the images from the brain folder to the destination folder based on the range
            images = list(brain_folder.glob('*.jpg'))  # Assuming images are in .jpg format
            
            for idx, img in enumerate(images, 1):
                if idx in image_range:
                    # Copy the image to the destination folder
                    shutil.copy(str(img), destination_folder / img.name)
            
            print(f"Copied patient {patient_number} images to {condition} folder.")
        else:
            print(f"Brain folder not found for patient {patient_number:0=3d}")
    else:
        print(f"Patient folder {patient_number:0=3d} not found.")
