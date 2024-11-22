import os
from pathlib import Path
import numpy as np
import pandas as pd
from tqdm import tqdm
from PIL import Image

numSubj = 82
new_size = (512, 512)
currentDir = Path(os.getcwd())
datasetDir = str(Path(currentDir, 'Patients_CT'))

# Reading labels
hemorrhage_diagnosis_df = pd.read_csv(
    Path(currentDir, 'hemorrhage_diagnosis.csv')
)
hemorrhage_diagnosis_array = hemorrhage_diagnosis_df.to_numpy()

# reading images
AllCTscans = np.zeros([hemorrhage_diagnosis_array.shape[0],
                       new_size[0], new_size[1]], dtype=np.uint8)
Allsegment = np.zeros([hemorrhage_diagnosis_array.shape[0],
                       new_size[0], new_size[1]], dtype=np.uint8)

train_path = Path('train')
image_path = train_path / 'image'
label_path = train_path / 'label'
if not train_path.exists():
    train_path.mkdir()
    image_path.mkdir()
    label_path.mkdir()

counterI = 0
for sNo in tqdm(range(49, numSubj + 49)):  # Adjusted patient range
    datasetDirSubj = Path(datasetDir, "{0:0=3d}".format(sNo))

    # Only check the 'brain' subfolder for images
    brain_folder = Path(datasetDirSubj, 'brain')
    
    # Skip if the brain folder doesn't exist for the current subject
    if not brain_folder.exists():
        continue

    idx = hemorrhage_diagnosis_array[:, 0] == sNo
    sliceNos = hemorrhage_diagnosis_array[idx, 1]
    NoHemorrhage = hemorrhage_diagnosis_array[idx, 7]
    for sliceI in range(0, sliceNos.size):
        img_path = brain_folder / (str(sliceNos[sliceI]) + '.jpg')
        
        # Check if the image exists before processing
        if os.path.exists(img_path):
            # Open image and resize
            img = Image.open(img_path)
            img_resized = img.resize(new_size)
            img_array = np.array(img_resized)
            AllCTscans[counterI] = img_array
            img_resized.save(image_path / (str(counterI) + '.png'))

            # Saving the segmentation for a given slice
            segment_path = brain_folder / (str(sliceNos[sliceI]) + '_HGE_Seg.jpg')
            if os.path.exists(str(segment_path)):
                img = Image.open(segment_path)
                img_resized = img.resize(new_size)
                img_array = np.array(img_resized)
                # Thresholding to convert to binary image
                img_array = np.where(img_array > 128, 255, 0)
                # Ensure the image array is in uint8 format before saving
                Image.fromarray(img_array.astype(np.uint8)).save(label_path / (str(counterI) + '.png'))
            else:
                img_array = np.zeros([new_size[0], new_size[1]], dtype=np.uint8)
                Image.fromarray(img_array).save(label_path / (str(counterI) + '.png'))

            Allsegment[counterI] = img_array
            counterI += 1
