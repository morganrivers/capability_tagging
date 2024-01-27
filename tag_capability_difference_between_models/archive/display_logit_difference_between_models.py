"""
Display a difference in logit value for next token prediction between a smaller model and a larger model.
Only significant logit differences that also are correct, confident predictions are displayed, where the smaller model
was notably incorrect in its predictions.
"""
# Runs the tinystories 33million parameter model on the next token implied by a sampling of examples, and reports the results.
import torch
import pprint
from transformer_lens import HookedTransformer, utils
from generate_examples_for_capability import get_text_and_completion_once, get_templates
from tqdm import tqdm
tqdm._instances.clear()  # Clear any existing instances

# Disable tqdm globally
tqdm.pandas(disable=True)  # If you're using tqdm with pandas


model_small = HookedTransformer.from_pretrained("tiny-stories-2layers-33M").to(torch.float32)
model_large = HookedTransformer.from_pretrained("tiny-stories-33M").to(torch.float32)
test="Hi Mommy! Today I learned that two plus two is"

for i in range(100):
    print("Small")
    print(model_small.generate(test, max_new_tokens=100, temperature=0, prepend_bos=False))
    print("Large")
    print(model_large.generate(test, max_new_tokens=100, temperature=0, prepend_bos=False))
