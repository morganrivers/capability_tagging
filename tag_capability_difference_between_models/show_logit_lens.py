from transformer_utils.logit_lens import plot_logit_lens

import transformers
from transformer_lens import HookedTransformer, utils
import torch

model_for_generation = HookedTransformer.from_pretrained("tiny-stories-instruct-33M").to(torch.float32)

#test_text_from_gpt4="""Once upon a time, in a small, old house, lived a little boy named Tom and his cat, Whiskers. """
#test_text_from_gpt4="""Once upon a time, in a"""
#test_text_from_gpt4="""However, Jerry made a bit of a mess. The dough was all over the floor and their hands were sticky and messy. """

#Sam laughed and said, 
test_text_from_gpt4=""""No worries! I'll just clean this up and start again."
So, Sam and Jerry worked to clean the mess, and then"""
tokenizer = transformers.AutoTokenizer.from_pretrained('roneneldan/TinyStories-33M')

def text_to_input_ids(text):
    #    toks = model.tokenizer.encode(text)
    toks = tokenizer.encode(text)
    return torch.as_tensor(toks).view(1, -1).cuda()


input_ids = text_to_input_ids(test_text_from_gpt4)

model_copy = transformers.AutoModelForCausalLM.from_pretrained('roneneldan/TinyStories-33M')

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_copy.to(device)
input_ids = input_ids.to(device)

plot_logit_lens(model_copy, tokenizer, input_ids, start_ix=0, end_ix=1000)  # logits
