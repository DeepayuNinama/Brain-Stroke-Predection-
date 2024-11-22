import os

datasetDir = 'Patients_CT - Copy'  # Adjust the path if needed
print("Listing patient folders:")
for patient_folder in os.listdir(datasetDir):
    print(patient_folder)
