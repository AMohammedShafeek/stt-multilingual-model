# pyrefly: ignore [missing-import]
from datasets import load_dataset

dataset = load_dataset(
    "csv",
    data_files="dataset/metadata.csv"
)

print(dataset)

print("\nFirst Row:\n")

print(dataset["train"][0])