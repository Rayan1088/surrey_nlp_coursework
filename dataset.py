import pandas as pd

splits = {'train': 'data/train-00000-of-00001.parquet', 'validation': 'data/validation-00000-of-00001.parquet', 'test': 'data/test-00000-of-00001.parquet'}

train_path = "data/train.csv"
test_path = "data/test.csv"
val_path = "data/validation.csv"

# Load and save train dataset
df_train = pd.read_parquet("hf://datasets/surrey-nlp/BESSTIE-CW-26/" + splits["train"])
print(df_train.head())
df_train.to_csv(train_path, index=False)

# Load and save test dataset
df_test = pd.read_parquet("hf://datasets/surrey-nlp/BESSTIE-CW-26/" + splits["test"])
df_test.to_csv(test_path, index=False)

# Load and save validation dataset
df_val = pd.read_parquet("hf://datasets/surrey-nlp/BESSTIE-CW-26/" + splits["validation"])
df_val.to_csv(val_path, index=False)