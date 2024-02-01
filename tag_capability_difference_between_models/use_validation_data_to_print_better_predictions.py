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
RANDOM_SEED = 42

all_examples = []
for text in df_sample['text']:
    all_examples.append(text)
(
    all_incorrect_predictions,
    all_correct_predictions,
    all_previous_strings
) = print_better_predictions(all_examples,100)
