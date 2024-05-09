import subprocess
import os
import time

# Define the notebook paths

notebook1_path = 'D:\\Final Project\\Text\\Final Output\\Final_project.ipynb'
notebook2_path = 'D:\\Final Project\\Text\\Final Output\\TestEmotionDetector.ipynb'



# Execute Notebook 1
subprocess.Popen(['jupyter', 'nbconvert', '--execute', '--to', 'notebook', notebook1_path])

# Execute Notebook 2
subprocess.Popen(['jupyter', 'nbconvert', '--execute', '--to', 'notebook', notebook2_path])

# Wait for a few seconds before exiting (adjust as needed)
time.sleep(10)
