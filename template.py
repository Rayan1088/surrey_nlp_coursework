import os 
from pathlib import Path

list_of_files = [

    f"notebooks/01_EDA.ipynb",
    f"notebooks/02_data_preprocessing.ipynb",
    f"notebooks/model_training.ipynb",
    f"notebooks/model_evaluation.ipynb",
    f"models_checkpoints/",
    f"artifacts/",
    f"src/__init__.py",
    f"src/exception.py",
    f"src/logger.py",
    f"src/utils.py",
    f"src/prediction_pipeline.py",
    "app.py",
    "requirements.txt",
    "setup.py",
    "config.yaml",
    "test.py" ]

for file_path in list_of_files:
    
    if file_path.endswith("/"):
        os.makedirs(file_path, exist_ok=True)
        print(f"{file_path} is already exists")
        continue
    
    file_path = Path(file_path) 
    filedir, filename = os.path.split(file_path)

    if filedir!= "":
        os.makedirs(filedir, exist_ok=True)
    
    if (not os.path.exists(file_path)) or (os.path.getsize(file_path)==0):
        with open(file_path, 'w') as file:
            pass
        print(f"{filename} is created in {filedir}")
    else:
        print(f"{filename} is already exists in {filedir} and has some content. Skipping creation.")