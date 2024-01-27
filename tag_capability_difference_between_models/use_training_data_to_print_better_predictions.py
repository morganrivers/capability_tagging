import pandas as pd
from datasets import load_dataset
import os
from display_better_predicted_logits import print_better_predictions

SAMPLE_SIZE = 1000
RANDOM_SEED = 44
SAMPLE_FILE = 'random_sample_1000.csv'

def load_or_create_sample_dataset(filename):
    if os.path.exists(filename):
        print(f"Loading dataset from {filename}")
        return pd.read_csv(filename)
    else:
        #dataset = load_dataset('roneneldan/TinyStories', data_files="data/train-00000-of-00004-2d5a1467fff1081b.parquet")
        dataset = load_dataset('roneneldan/TinyStories', data_files="data/validation-00000-of-00001-869c898b519ad725.parquet")
        breakpoint()
        sample = dataset['train'].shuffle(seed=RANDOM_SEED).select(range(SAMPLE_SIZE))
        df_sample = pd.DataFrame(sample['text'], columns=['text'])
        df_sample['text'] = df_sample['text'].str.lower()
        df_sample.to_csv(filename, index=False)
        return df_sample

df_sample = load_or_create_sample_dataset(SAMPLE_FILE)
SAMPLE_FILE = 'random_sample_1000.csv'
SAMPLE_SIZE = 1000
RANDOM_SEED = 44

all_examples = []
for text in df_sample['text']:
    all_examples.append(text)
(
    all_incorrect_predictions,
    all_correct_predictions,
    all_previous_strings
) = print_better_predictions(all_examples,100)
"""
# Combine the lists into a list of tuples
combined = list(zip(all_incorrect_predictions, all_correct_predictions, all_previous_strings))

# Sort the list of tuples by different criteria and print out the results as requested

# Printout 1: Sorted by all_incorrect_predictions (index 2, 0, 1)
combined.sort(key=lambda x: x[0])  # Sorting by the first element of the tuple
print("\n\n\nPrintout 1:")
for i in combined:
    print(i)

# Printout 2: Sorted by all_correct_predictions (index 1, 2, 0)
combined.sort(key=lambda x: x[1])  # Sorting by the second element of the tuple
print("\n\n\nPrintout 2:")
for i in combined:
    print(i)

# Printout 3: Sorted by all_previous_strings (index 1, 2, 0)
combined.sort(key=lambda x: x[2])  # Sorting by the third element of the tuple
print("\n\nPrintout 3:")
for i in combined:
    print(i)
"""
