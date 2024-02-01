import numpy as np

import torch
import transformers
import scipy
from transformer_utils.logit_lens import make_lens_hooks
from transformer_utils.logit_lens.layer_names import make_layer_names

def postprocess_logits(layer_logits):
    layer_preds = layer_logits.argmax(axis=-1)

    layer_probs = scipy.special.softmax(layer_logits, axis=-1)

    return layer_preds, layer_probs

def collect_logits(model, input_ids, layer_names, decoder_layer_names):
    model._last_resid = None

    with torch.no_grad():
        out = model(input_ids)
    del out
    model._last_resid = None

    layer_logits = np.concatenate(
        [model._layer_logits[name] for name in layer_names],
        axis=0,
    )

    return layer_logits, layer_names


model_large = transformers.AutoModelForCausalLM.from_pretrained('roneneldan/TinyStories-33M')
model_small = transformers.AutoModelForCausalLM.from_pretrained('roneneldan/TinyStories-2Layers-33M')
tokenizer = transformers.AutoTokenizer.from_pretrained('roneneldan/TinyStories-33M')


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_large.to(device)
model_small.to(device)
test_text_from_gpt4="""Once upon a time, in a small, old house, lived a little boy named Tom and his cat, Whiskers. The house was very old, so old that everyone in the town called it the "ancient house." Tom loved his ancient house very much."""


def text_to_input_ids(text):
    toks = tokenizer.encode(text)
    return torch.as_tensor(toks).view(1, -1).cuda()

input_ids = text_to_input_ids(test_text_from_gpt4)
input_ids = input_ids.to(device)




block_step=1
include_input=True
force_include_output=True
decoder_layer_names = ['final_layernorm', 'lm_head']
verbose = True
include_subblocks = True

def get_logits(model, input_ids):

    layer_names = make_layer_names(
        model,
        block_step=block_step,
        include_input=include_input,
        force_include_output=force_include_output,
        include_subblocks=include_subblocks,
        decoder_layer_names=decoder_layer_names
    )
    start_ix=0
    end_ix=input_ids.shape[1] - 1 #,#len(input_ids) - 1

    make_lens_hooks(model, start_ix=start_ix, end_ix=end_ix, layer_names=layer_names,
                    decoder_layer_names=decoder_layer_names,
                        verbose=verbose)
                        
    layer_logits, layer_names = collect_logits(
        model, input_ids, layer_names=layer_names, decoder_layer_names=decoder_layer_names,
    )

    layer_preds, layer_probs = postprocess_logits(layer_logits)
    return layer_logits, layer_names, layer_preds, layer_probs

import torch
import torch.nn.functional as F

def print_and_return_next_token_small_model_correct(small_model_incorrect_predictions, large_model_correct_predictions, previous_string, predicted_next_token_large,actual_next_token,predicted_next_token_small,probs_small,probs_large, top_preds_small, top_preds_large, i, accumulated_string, difference_threshold=.3,prob_incorrect_threshold=.1,prob_correct_threshold=.9):
    if predicted_next_token_large == actual_next_token and predicted_next_token_small != actual_next_token:
        prob_small = probs_small[i, top_preds_small[i]].item()
        prob_large = probs_large[i, top_preds_large[i]].item()
        prob_large_for_small_pred = probs_large[i, top_preds_small[i]].item()


        if ( (prob_large - prob_small) > difference_threshold):
            if prob_large_for_small_pred < prob_correct_threshold and prob_large > prob_correct_threshold:
                small_model_incorrect_predictions.append(predicted_next_token_small)
                large_model_correct_predictions.append(predicted_next_token_large)
                previous_string.append(accumulated_string.strip()[-20:])
                print(f"\n\nContext: {accumulated_string.strip()}")
                print(f"Small Model Predicted: '{predicted_next_token_small}' (Prob: {prob_small:.4f}), Large Model Correctly Predicted: '{predicted_next_token_large}' (Prob: {prob_large})")
                print(f"Probability assigned by Large Model to Small Model's prediction: {prob_large_for_small_pred:.4f}")
                print()
    return (small_model_incorrect_predictions, large_model_correct_predictions, previous_string)


def print_and_return_next_token_large_model_correct(small_model_incorrect_predictions, large_model_correct_predictions, previous_string, predicted_next_token_large,actual_next_token,predicted_next_token_small,probs_small,probs_large, top_preds_small, top_preds_large, i, accumulated_string, difference_threshold=.3,prob_incorrect_threshold=.1,prob_correct_threshold=.9):
    if predicted_next_token_small == actual_next_token and predicted_next_token_large != actual_next_token:
        prob_small = probs_small[i, top_preds_small[i]].item()
        prob_large = probs_large[i, top_preds_large[i]].item()
        prob_small_for_large_pred = probs_small[i, top_preds_large[i]].item()

        if ((prob_small - prob_large) > difference_threshold):
            if prob_small_for_large_pred < prob_incorrect_threshold and prob_small > prob_correct_threshold:
                print(f"\n\n\nSMALL BETTER THAN BIG!\nContext: {accumulated_string.strip()}")
                print(f"Large Model Predicted: '{predicted_next_token_large}' (Prob: {prob_large:.4f}), Small Model Correctly Predicted: '{predicted_next_token_small}' (Prob: {prob_small})")
                print(f"Probability assigned by Small Model to Large Model's prediction: {prob_small_for_large_pred:.4f}")
                print("END SMALL BETTER THAN BIG!")
                print()
    return (small_model_incorrect_predictions, large_model_correct_predictions, previous_string)


def compare_and_print_predictions_with_context_and_probs(layer_logits_small, layer_logits_large, input_ids, tokenizer):
    last_layer_logits_small = torch.tensor(layer_logits_small[-1])
    last_layer_logits_large = torch.tensor(layer_logits_large[-1])

    top_preds_small = torch.argmax(last_layer_logits_small, dim=-1)
    top_preds_large = torch.argmax(last_layer_logits_large, dim=-1)

    # Convert logits to probabilities using softmax
    probs_small = F.softmax(last_layer_logits_small, dim=-1)
    probs_large = F.softmax(last_layer_logits_large, dim=-1)

    num_tokens = min(input_ids.shape[1] - 1, top_preds_small.shape[0], top_preds_large.shape[0])
    accumulated_string = ""

    small_model_incorrect_predictions = []
    large_model_correct_predictions = []
    previous_string = []
    for i in range(num_tokens):  # Iterate only over the valid range
        current_token = tokenizer.decode(input_ids[0, i])
        accumulated_string += current_token + " "
        actual_next_token = tokenizer.decode(input_ids[0, i+1])
        predicted_next_token_small = tokenizer.decode(top_preds_small[i].item())
        predicted_next_token_large = tokenizer.decode(top_preds_large[i].item())
        is_uninteresting_token = False
        if actual_next_token=="\n" or actual_next_token == "." or actual_next_token == "," or actual_next_token == "'s":
            is_uninteresting_token = True
        if predicted_next_token_small=="\n" or predicted_next_token_small == "." or predicted_next_token_small == "," or predicted_next_token_small == "'s":
            is_uninteresting_token = True
        if predicted_next_token_large=="\n" or predicted_next_token_large == "." or predicted_next_token_large == "," or predicted_next_token_large == "'s":
            is_uninteresting_token = True
        if current_token.lower() == " once" and actual_next_token.lower() == " upon":
            is_uninteresting_token = True

        if is_uninteresting_token:
            continue


        print_and_return_next_token_small_model_correct(small_model_incorrect_predictions, large_model_correct_predictions, previous_string, predicted_next_token_large,actual_next_token,predicted_next_token_small,probs_small,probs_large,top_preds_small, top_preds_large, i, accumulated_string)
        (small_model_incorrect_predictions, large_model_correct_predictions, previous_string) = print_and_return_next_token_large_model_correct(small_model_incorrect_predictions, large_model_correct_predictions, previous_string, predicted_next_token_large,actual_next_token,predicted_next_token_small,probs_small,probs_large,top_preds_small, top_preds_large, i, accumulated_string)
    return (
        small_model_incorrect_predictions,
        large_model_correct_predictions,
        previous_string
    )

# Usage

examples = ["Alice was so tired when she got back home so she went straight to bed. ",
"Lily likes cats and dogs. She asked her mom for a dog and her mom said no, so instead she asked",
"Alice and Jack walked up the street and met a girl in a red dress. The girl said to them, \"Hi, I'm Jane. What are your names?\" Alice said, \"I'm Alice and this is Jack.\"",
"Jack and Lily saw a rainbow after a rainy day. They were amazed by the colors. Jack said, \"Look, Lily. A rainbow has red, orange, yellow, green, blue, and purple!\"",
"Jack and Lily liked to watch the moon at night. They noticed that the moon changed its shape every night. Sometimes the moon was big and round, and sometimes it was small and thin.",
"Jack told Mary, \"If you give me your banana, I'll give you my apple\". Mary gave Jack her Banana so he could give her the apple.",
"On weekends Jack went to visit his grandmother whereas on weekdays he would go to school. Last weekend, when Jack was on his way to his grandmother's house,"]


def print_better_predictions(examples,n_examples):
    all_incorrect_predictions = []
    all_correct_predictions = []
    all_previous_strings = []
    for example in examples[0:n_examples]:
        print("")
        print("")
        print("")
        print("")
        print("new example")
        print("")
        input_ids = text_to_input_ids(example)
        input_ids = input_ids.to(device)
        print("example")
        print(example)
        start_ix=0
        end_ix=input_ids.shape[1] - 1#,#len(input_ids) - 1

        layer_logits_small, layer_names_small, layer_preds_small, layer_probs_small = get_logits(model_small, input_ids)
        layer_logits_large, layer_names_large, layer_preds_large, layer_probs_large = get_logits(model_large, input_ids)
        (
            small_model_incorrect_predictions,
            large_model_correct_predictions,
            previous_string
        ) = compare_and_print_predictions_with_context_and_probs(layer_logits_small, layer_logits_large, input_ids, tokenizer)
        all_incorrect_predictions.extend(small_model_incorrect_predictions)
        all_correct_predictions.extend(large_model_correct_predictions)
        all_previous_strings.extend(previous_string)
    return (
        all_incorrect_predictions,
        all_correct_predictions,
        all_previous_strings
    )

if __name__ == "__main__":
    print_better_predictions(examples)
