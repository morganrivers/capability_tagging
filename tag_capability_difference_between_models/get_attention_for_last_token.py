import numpy as np
from transformers import AutoTokenizer, AutoModel, utils
from bertviz import model_view

from bertviz.util import format_special_chars, format_attention, num_layers, num_heads
utils.logging.set_verbosity_error()  # Suppress standard warnings
#model = HookedTransformer.from_pretrained("tiny-stories-33M").to(torch.float32)

#model_name = "microsoft/xtremedistil-l12-h384-uncased"  # Find popular HuggingFace models here: https://huggingface.co/models
model_name = "roneneldan/TinyStories-33M"  # Find popular HuggingFace models here: https://huggingface.co/models
#model_name = "Roneneldan/TinyStories-33M"  # Find popular HuggingFace models here: https://huggingface.co/models
#input_text = "Lily knows all the colors in the rainbow: red,"  
input_text = "Ben had beautiful white eyes." #He enjoyed it when the shiny teeth of the fish went through his hair"
model = AutoModel.from_pretrained(model_name, output_attentions=True)  # Configure model to return attention values
tokenizer = AutoTokenizer.from_pretrained(model_name)

from transformer_lens import HookedTransformer, utils
import torch
model_for_generation = HookedTransformer.from_pretrained("tiny-stories-instruct-33M").to(torch.float32)

def get_attn_data(input_text,tokenizer,model):
    inputs = tokenizer.encode(input_text, return_tensors='pt')  # Tokenize input text
    outputs = model(inputs)  # Run model
    attention = outputs[-1]  # Retrieve attention from model outputs
    tokens = tokenizer.convert_ids_to_tokens(inputs[0])  # Convert input ids to token strings
    attn_data = []
    if tokens is None:
        raise ValueError("'tokens' is required")
    n_heads = num_heads(attention)
    include_layers = list(range(num_layers(attention)))
    include_heads = list(range(n_heads))
    attention = format_attention(attention, include_layers, include_heads)
    attn_data.append(
        {
            'name': None,
            'attn': attention.tolist(),
            'left_text': tokens,
            'right_text': tokens
        }
    )
    return attn_data

def element_wise_average(lists):
    return [sum(elements) / len(elements) for elements in zip(*lists)]


def process_layers(layers_nested_list):
    attention_for_whole_context = []

    n_tokens_to_make_layers_for = len(layers_nested_list[0][0])
    print("n_tokens_to_make_layers_for")
    print(n_tokens_to_make_layers_for)
    for i in range(n_tokens_to_make_layers_for):
        layers = {}

        for j, layer in enumerate(layers_nested_list):
            layer_key = f'layer{j}'
            all_heads_last_lists = []
            layers[layer_key] = {}
            for k in range(len(layer)):
                head_key = f'head{k}'
                this_token_list = layer[k][i] # the list of attention for this token at index i, for layer k
                all_heads_last_lists.append(this_token_list)
                layers[layer_key][head_key] = this_token_list

            head_averages = element_wise_average(all_heads_last_lists)
            layers[layer_key]['head_averages'] = head_averages

        # Calculate layer_averages as the element-wise average of head_averages of all layers
        layers['layer_averages'] = element_wise_average([layers[layer]['head_averages'] for layer in layers])
        layers['layer123_averages'] = element_wise_average([layer['head_averages'] for layer in [layers["layer1"],layers["layer2"],layers["layer3"]]])

        attention_for_whole_context.append(layers)
    return attention_for_whole_context

#attn_data = get_attn_data(input_text,tokenizer,model)
#attn_all_tokens = process_layers(attn_data[0]['attn'])
#import pprint
#print(attn_last_token["layer1"])
#pprint.pprint(attn_last_token["layer1"])
#print(attn_last_token["layer1"].keys())
#print(attn_last_token["layer1"]["head1"])

# Mia was a three-year-old girl who had very beautiful, long, white hair. She enjoyed it very much, especially when the shiny teeth of the comb caught the light of the stars when it went through her


#import torch
#from transformer_lens import HookedTransformer, utils

#model = HookedTransformer.from_pretrained("tiny-stories-33M").to(torch.float32)
#test=input_text = "Mia had beautiful white hair. She enjoyed it when the shiny teeth of the comb went through her hair"


#for i in range(100):
#    print(model.generate(test, max_new_tokens=10, temperature=0.7, prepend_bos=False))


# get the attention on all the tokens of the input
#print(attn_data[0]['right_text'])



def color_sentence_with_brightness_and_bold(sentence, random_numbers):
    colored_sentence = ""
    max_number = max(random_numbers)
    for word, number in zip(sentence, random_numbers):
        # Scale the random number to range from 0 to 255 for the red color component
        red_brightness = int(number/max_number * 255)
        # Determine if the word should be bold
        bold_code = ";1" if number/max_number > 0.7 else ""
        # Construct the ANSI escape code for the color and boldness
        color_code = f"\033[38;2;{red_brightness};0;0{bold_code}m"
        # Color the word and reset the color afterwards
        colored_word = color_code + word + "\033[0m"
        colored_sentence += colored_word + " "
    return colored_sentence


def print_attention_for_sentence(sentence,attn_last_token):
    first_layer_avg_attention = attn_last_token["layer0"]["head_averages"]
    colored_sentence = color_sentence_with_brightness_and_bold(sentence,first_layer_avg_attention)
    print("layer 0 attention")
    print(colored_sentence)

    other_layers_avg_attention = attn_last_token["layer123_averages"]
    colored_sentence = color_sentence_with_brightness_and_bold(sentence,other_layers_avg_attention)
    print("layers 123 attention")
    print(colored_sentence)
    print("")
    layer2_avg_attention = attn_last_token["layer1"]["head_averages"]
    colored_sentence = color_sentence_with_brightness_and_bold(sentence,layer2_avg_attention)
    print("layer 1 attention")
    print(colored_sentence)

    layer3_avg_attention = attn_last_token["layer2"]["head_averages"]
    colored_sentence = color_sentence_with_brightness_and_bold(sentence,layer3_avg_attention)
    print("layer 2 attention")
    print(colored_sentence)

    layer4_avg_attention = attn_last_token["layer3"]["head_averages"]
    colored_sentence = color_sentence_with_brightness_and_bold(sentence,layer4_avg_attention)
    print("layer 3 attention")
    print(colored_sentence)

    """
    layer4_avg_attention = attn_last_token["layer3"]["head0"]
    colored_sentence = color_sentence_with_brightness_and_bold(sentence,layer4_avg_attention)
    print("layer 3 head 0 attention")
    print(colored_sentence)
    layer4_avg_attention = attn_last_token["layer3"]["head0"]
    colored_sentence = color_sentence_with_brightness_and_bold(sentence,layer4_avg_attention)
    print("layer 3 attention")
    print(colored_sentence)
    """
example=input_text
attn_data = get_attn_data(example,tokenizer,model)
attn_all_tokens = process_layers(attn_data[0]['attn'])
sentence = attn_data[0]['right_text']
sentence = format_special_chars(sentence)
print("len(sentence)")
print(len(sentence))
print("attention for last token")
print_attention_for_sentence(sentence,attn_all_tokens[-1])
print("attention for 2nd to last token")
print_attention_for_sentence(sentence,attn_all_tokens[-2])
print("attention for 5th to last token")
print_attention_for_sentence(sentence,attn_all_tokens[-5])
print(model_for_generation.generate(example, max_new_tokens=1, temperature=0, prepend_bos=True)[-100:])

"""
def build_and_print_tree(layers, tokens, threshold=0.3):
    def recurse_tree(node, layer, attention_product, prefix=""):
        if layer >= len(layers):
            return

        # Using the pre-calculated head averages for each layer
        avg_attention = layers[f"layer{layer}"]["head_averages"]

        for i, attn_weight in enumerate(avg_attention):
            new_attention_product = attention_product * attn_weight *2
            if new_attention_product > threshold:
                token_str = f"Token {i}: '{tokens[i]}'" if i < len(tokens) else f"Token {i}"
                print(f"{prefix}|- {token_str} (Layer {layer}, Attn: {attn_weight:.2f})")
                recurse_tree(i, layer + 1, new_attention_product, prefix + "  ")

    last_token_index = len(tokens) - 1  # Last token index
    last_token_str = tokens[last_token_index] if last_token_index < len(tokens) else f"Token {last_token_index}"
    print(f"Root: {last_token_str} (Last Token)")
    recurse_tree(last_token_index, 0, 1.0)
"""
import numpy as np
"""
def build_and_print_tree(
    layers, tokens, threshold=0.1, reducing_cost_of_depth_coeff=0.9
):
    def recurse_tree(node, current_layer, depth, attention_product, prefix=""):
        if depth >= len(tokens):  # Limit the recursion depth to the number of tokens
            return

        # every layer from this down needs to be looked at. We will sort descending all matches regardless of which layer the match comes from.
        # Collecting attention data for sorting at this depth and this particular branch
        attention_data = []
        for layer in range(current_layer, -1, -1):
            avg_attention = layers[f"layer{layer}"]["head_averages"]

            for token_index, attn_weight in enumerate(avg_attention):
                new_attention_product = np.power(
                    attention_product * attn_weight, reducing_cost_of_depth_coeff
                )
                if new_attention_product > threshold:
                    attention_data.append(
                        (token_index, layer, attn_weight, new_attention_product)
                    )

        # Sorting by attention weight in descending order
        attention_data.sort(key=lambda x: x[2], reverse=True)
        for (
            token_index,
            attended_layer,
            attn_weight,
            new_attention_product,
        ) in attention_data:
            token_str = f"Token {token_index}: '{tokens[token_index]}'"
            print(
                f"{prefix}|- {token_str} (Layer: {attended_layer}, Depth: {depth}, Attn: {attn_weight:.2f})"
            )
            recurse_tree(
                token_index, attended_layer, new_attention_product, prefix + "  "
            )

    last_token_index = len(tokens) - 1  # Last token index
    last_token_str = f"Token {last_token_index}: '{tokens[last_token_index]}'"
    print(f"Root: {last_token_str} (Last Token)")
    recurse_tree(
        node=last_token_index, current_layer=3, depth=0, attention_product=1
    )  # Start from the last layer and depth 0
"""
def build_and_print_tree(
    attn_all_tokens, tokens, threshold=0.1, reducing_cost_of_depth_coeff=0.9
):
    def recurse_tree(node, current_layer, depth, attention_product, prefix=""):
        if depth >= len(tokens):  # Limit the recursion depth to the number of tokens
            return

        # every layer from this down needs to be looked at. We will sort descending all matches regardless of which layer the match comes from.
        # Collecting attention data for sorting at this depth and this particular branch
        attention_data = []
        for layer in range(current_layer, -1, -1):
            layers = attn_all_tokens[node] # get just the attention for the token we're looking at. This applies the causal mask -- no looking at later tokens
            avg_attention = layers[f"layer{layer}"]["head_averages"]

            for token_index, attn_weight in enumerate(avg_attention):
                #new_attention_product = np.power(
                #    attention_product * attn_weight, reducing_cost_of_depth_coeff
                #)
                new_attention_product=attn_weight
                if new_attention_product > threshold:
                    if token_index == node:
                        continue # we want to skip attention to your own residual stream as that's uninteresting (if you don't do that, then you're using or copying other tokens somehow
                    if token_index == 0:
                        continue # the first token is usually just a place-holder for no attention, so we ignore it
                    if depth > 5:
                        continue # let's not get too deep now that we're always following strong attentions
                    attention_data.append(
                        (token_index, layer, attn_weight, new_attention_product)
                    )

        # Sorting by attention weight in descending order
        attention_data.sort(key=lambda x: x[2], reverse=True)
        for (
            token_index,
            attended_layer,
            attn_weight,
            new_attention_product,
        ) in attention_data:
            token_str = f"Token {token_index}: '{tokens[token_index]}'"
            print(
                f"{prefix}|- {token_str} (Layer: {attended_layer}, Depth: {depth}, Attn: {attn_weight:.2f})"
            )
            recurse_tree(
                token_index, attended_layer,depth + 1, new_attention_product, prefix + "  "
            )

    last_token_index = len(tokens) - 1  # Last token index
    last_token_str = f"Token {last_token_index}: '{tokens[last_token_index]}'"
    print(f"Root: {last_token_str} (Last Token)")
    recurse_tree(
        node=last_token_index, current_layer=3, depth=0, attention_product=1
    )  # Start from the last layer and depth 0

"""
interesting_examples = [\"""Once upon a time, there was a big race between two animals. A rabbit and a turtle wanted to see who was the fastest. The race started and the rabbit ran very fast. The turtle was slow, but he kept going. Suddenly, the rabbit got tired and slept. The turtle kept going and won the race! The turtle had a victory! 

The rabbit was very sad, but his friends were helpful. They told him to not give up and try again. The rabbit listened and practiced every day. Soon, he was ready for a new race. This time, he didn't stop and he didn't sleep. He ran and ran until he reached the finish line. He had a victory too! 

But the rabbit learned a lesson. He learned that being too confident can strike you down. He was happy that his friends were helpful and that he could try again. From that day on, the rabbit\""",\
\"""However, Jerry made a bit of a mess. The dough was all over the floor and their hands were sticky and messy. 

Sam laughed and said, "No worries! Let's just clean this up and start again." 

So, Sam and Jerry worked together to clean the mess, and then\""","Once upon a time, Lily asked for a cat. For Christmas, mom gave Lily a"]
"""
interesting_examples = ["Jack and Lily saw a rainbow after a rainy day. They were amazed by the colors. Jack said, \"Look, Lily. A rainbow has red,",\
""""What language do they speak in France?", Tom asked his mother.
"They speak""",\
"If I throw a ball up, eventually it will come back",\
"""No worries! Let's just clean this up and start again."
So, Sam and Jerry worked together to clean the mess, and then""",
"""No worries! I'll just clean this up and start again."
So, Sam and Jerry worked to clean the mess, and then""",
"""No worries! I'll just clean this up and start again."
So, Sam worked to clean the mess, and then"""
]

for example in interesting_examples:
    attn_data = get_attn_data(example,tokenizer,model)
    attn_all_tokens = process_layers(attn_data[0]['attn'])
    sentence = attn_data[0]['right_text']
    sentence = format_special_chars(sentence)
    print()
    print()
    print()
    print()
    print("attention for last token")
    print_attention_for_sentence(sentence,attn_all_tokens[-1])
    print()
    print("attention for 2nd to last token")
    print_attention_for_sentence(sentence,attn_all_tokens[-2])
    print()
    print("attention for 5th to last token")
    print_attention_for_sentence(sentence,attn_all_tokens[-5])

    print(model_for_generation.generate(example, max_new_tokens=1, temperature=0, prepend_bos=True)[-100:])
    build_and_print_tree(attn_all_tokens, sentence, threshold=.1,reducing_cost_of_depth_coeff=0.8)

