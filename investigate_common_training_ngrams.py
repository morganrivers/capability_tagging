import nltk
from nltk.tokenize import word_tokenize
from collections import Counter
import pandas as pd
from datasets import load_dataset
import os
from nltk.util import ngrams
SAMPLE_FILE = 'random_sample_1000.csv'
SAMPLE_SIZE = 1000
RANDOM_SEED = 44

# Define groups of interchangeable tokens
interchangeable_groups = {
    "lily": ["timmy", "james", "timmy","billy","anna","ben","tim","tom","benny","sarah","sara", "sue", "sam", "lucy", "max", "susie", "jack", "ben", "milly","ann","jay","chloe","cathy","jamie"],
    "a": ["an"],
    "she": ["he"],
    "her": ["his"],
    "mommy": ["daddy"],
    "mom": ["dad"],
    "girl": ["boy"],
    "little": ["big"],
    "bunny": ["dog","cat","bird","fish","dragon","bear","owl","caterpillar","butterfly"],
    "red": ["orange","yellow","blue","purple","green","black","white"],
}

def load_or_create_sample_dataset(filename):
    if os.path.exists(filename):
        print(f"Loading dataset from {filename}")
        return pd.read_csv(filename)
    else:
        dataset = load_dataset('roneneldan/TinyStories', data_files="data/train-00000-of-00004-2d5a1467fff1081b.parquet")
        sample = dataset['train'].shuffle(seed=RANDOM_SEED).select(range(SAMPLE_SIZE))
        df_sample = pd.DataFrame(sample['text'], columns=['text'])
        df_sample['text'] = df_sample['text'].str.lower()
        df_sample.to_csv(filename, index=False)
        return df_sample

# Function to replace tokens with their group representative
def replace_with_representative(token, groups):
    for rep, group in groups.items():
        if token in group:
            return rep
    return token

def shared_word_count(ngram1, ngram2):
    """Count the max length of shared words between two n-grams."""
    return len(ngram1.intersection(ngram2))

def remove_duplicate_ngrams(ngrams_list,ngram_length):
    """Group n-grams based on the number of shared words."""
    grouped_ngrams = {}
    for ngram in ngrams_list:
        # Check if ngram can be grouped with an existing group
        added = False
        for key in grouped_ngrams.keys():
            if shared_word_count(ngram, key) >= ngram_length//2:
                grouped_ngrams[key].append(ngram)
                added = True
                break
        if not added:
            grouped_ngrams[ngram] = [ngram]
    return grouped_ngrams

def print_phrases(phrases):
    for phrase in phrases:
        print("count: "+ str(phrase[1])+" | "+" ".join(phrase[0]))

def print_all_samples_with_phrase_in_it(search_text):
    print("")
    print("search_text: "+search_text)
    print("")
    for text in df_sample['text']:
        tokens = word_tokenize(text)
        if search_text in " ".join(tokens):
            print("")
            print(" ".join(tokens))
            print("")
    print("")

# # Main function
# def main():
# Load or create sample dataset
df_sample = load_or_create_sample_dataset(SAMPLE_FILE)

token_counts = Counter()

# # Tokenize and process the text
# all_tokens = []
# for text in df_sample['text']:
#     tokens = tokenizer.tokenize(text.lower())
#     replaced_tokens = [replace_with_representative(token, interchangeable_groups) for token in tokens]
#     all_tokens.extend(replaced_tokens)

all_tokens = []
for text in df_sample['text']:
    tokens = word_tokenize(text)
    all_tokens.extend(tokens)
    token_counts.update(tokens)

all_tokens_replaced = [replace_with_representative(token, interchangeable_groups) for token in all_tokens]

unigram_counts = Counter(ngrams(all_tokens_replaced, 1))

bigram_counts = Counter(ngrams(all_tokens_replaced, 2))
trigram_counts = Counter(ngrams(all_tokens_replaced, 3))
quadgram_counts = Counter(ngrams(all_tokens_replaced, 4))
most_common_bigrams = bigram_counts.most_common(300)
most_common_trigrams = trigram_counts.most_common(300)
most_common_quadgrams = trigram_counts.most_common(300)
# pd.DataFrame(most_common_bigrams, columns=['Bigram', 'Frequency']).to_csv(BIGRAMS_FILE, index=False)
print("")
print("")
print("")
print("")
print("")
print("UNIGRAM 300")
print(unigram_counts.most_common(300))
print("BIGRAM 300")
print(most_common_bigrams)
print("TRIGRAM 300")
print(most_common_trigrams)
print("QUADGRAM 300")
print(most_common_quadgrams)

# Find the 300 most common 8-token phrases
phrase_counts = Counter(ngrams(all_tokens_replaced, 8))
most_common_phrases = phrase_counts.most_common(500)
print("")
print("")
once_upon_phrases = []
girl_named_lily_phrases = []
happily_ever_after_phrases = []
play_phrases = []
upset_phrases = []
dialog_phrases = []
remaining_phrases = []
for phrase in most_common_phrases:
    if "once upon a time" in " ".join(phrase[0]):
        once_upon_phrases.append(phrase)
        continue
    if "girl named lily" in " ".join(phrase[0]) or "little girl" in " ".join(phrase[0]):
        girl_named_lily_phrases.append(phrase)
        continue
    if "happily ever after" in " ".join(phrase[0]):
        happily_ever_after_phrases.append(phrase)
        continue
    if "upset" in " ".join(phrase[0]):
        upset_phrases.append(phrase)
        continue
    if "play" in " ".join(phrase[0]):
        play_phrases.append(phrase)
        continue
    if "said , ``" in " ".join(phrase[0]) or ", '' she said" in " ".join(phrase[0]) or ", '' lily said" in " ".join(phrase[0]):
        dialog_phrases.append(phrase)
        continue

    remaining_phrases.append(phrase)
print("")
print("")
print("once_upon_phrases, length "+ str(len(once_upon_phrases)))
print_phrases(once_upon_phrases)
print("")
print("")
print("girl_named_lily_phrases, length "+str( len(girl_named_lily_phrases)))
print_phrases(girl_named_lily_phrases)
print("")
print("")
print("happily_ever_after_phrases, length "+str( len(happily_ever_after_phrases)))
print_phrases(happily_ever_after_phrases)
print("")
print("")
print("play_phrases, length "+str( len(play_phrases)))
print_phrases(play_phrases)
print("")
print("")
print("upset_phrases, length "+str( len(upset_phrases)))
print_phrases(upset_phrases)
print("")
print("")
print("dialog_phrases, length "+str( len(dialog_phrases)))
print_phrases(dialog_phrases)
print("")
print("")
print("remaining_phrases, length "+str( len(remaining_phrases)))
print_phrases(remaining_phrases)
print("")
print("")


# print_all_samples_with_phrase_in_it("do you understand")
# print_all_samples_with_phrase_in_it("hide and seek")
# print_all_samples_with_phrase_in_it("and said , `` do n't")
# print_all_samples_with_phrase_in_it("said , `` yes , but")

# grouped_phrases = remove_duplicate_ngrams([ngram for ngram, count in phrase_counts.most_common(300)],ngram_length=10)
# print("\nGrouped Phrases:")
# for group, members in grouped_phrases.items():
#     print(f"Shared Words: {len(group)}, Group: {members}")

# if __name__ == "__main__":
#     main()