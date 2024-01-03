# Runs the tinystories 33million parameter model on the next token implied by a sampling of examples, and reports the results.
import torch
import pprint
from transformer_lens import HookedTransformer, utils
from generate_examples_for_capability import get_text_and_completion_once, get_templates
from tqdm import tqdm
tqdm._instances.clear()  # Clear any existing instances

# Disable tqdm globally
tqdm.pandas(disable=True)  # If you're using tqdm with pandas

model = HookedTransformer.from_pretrained("tiny-stories-33M").to(torch.float32)
#test="Hi Mommy! Today I learned that two plus two is"

#for i in range(100):
#    print(model.generate(test, max_new_tokens=100, temperature=0.7, prepend_bos=False))

def run_model_return_result(test,correct_completion,incorrect_completion):
    start_and_completion = model.generate(test, max_new_tokens=4, temperature=0, prepend_bos=False)
    model_completion = start_and_completion[len(test):].lower().strip()
    print("test with completion")
    print(test +"|"+model_completion)
    #print("first word completion")
    #print(model_completion.split(" ")[0])
    #print("seems correct test: "+correct_completion.lower().strip().split(" ")[0] +" in " + model_completion+ " or "+model_completion.split(" ")[0]+" in " +correct_completion.lower())
    seems_correct = correct_completion.lower().strip().split(" ")[0] in model_completion or model_completion.split(" ")[0] in correct_completion.lower().strip()
    seems_incorrect = incorrect_completion.lower().strip().split(" ")[0] in model_completion or model_completion.split(" ")[0] in incorrect_completion.lower().strip()
    #print("model_completion, correct completion")
    #print(model_completion + ", " +correct_completion)
    return seems_correct, seems_incorrect, model_completion

def run_model_and_evaluate(all_tests_this_template):
    all_tests_this_template = {}
    for evaluation_type, test_and_completion in tests.items():
        all_tests_this_template[evaluation_type] = test_and_completion
        #if evaluation_type = "start_exclusion":
        seems_correct, seems_incorrect, model_completion = run_model_return_result(test_and_completion["test"],test_and_completion["correct_completion"],test_and_completion["incorrect_completion"])
        all_tests_this_template[evaluation_type]["answered_correctly"] = seems_correct
        all_tests_this_template[evaluation_type]["answered_incorrectly"] = seems_incorrect
        all_tests_this_template[evaluation_type]["answer"] = model_completion
    return all_tests_this_template


def update_success_rate_dictionary(evaluation,success_rate_by_type):
    for key, item in evaluation.items():
        if "start_" in key:
            type = key[len("start_"):]
            if type not in success_rate_by_type:
                success_rate_by_type[type] = {'success': 0, 'failure':0, 'total': 0}

            success_rate_by_type[type]['total'] += 1
            if item['answered_correctly']:
                success_rate_by_type[type]['success'] += 1
            if item['answered_incorrectly']:
                success_rate_by_type[type]['failure'] += 1
    return success_rate_by_type

# Initialize a dictionary to store success rate data by type

# Calculate and print the success rate by type

def print_success_rate(success_rate_by_type):
    for type, data in success_rate_by_type.items():
        success_rate = (data['success'] / data['total']) * 100 if data['total'] > 0 else 0
        failure_rate = (data['failure'] / data['total']) * 100 if data['total'] > 0 else 0
        print(f"Success rate for {type}: {success_rate:.2f}% ({data['success']} / {data['total']})")
        print(f"Failure rate for {type}: {failure_rate:.2f}% ({data['failure']} / {data['total']})")

def determine_if_should_skip(templates_of_interest, template_exclusion_string):
    skip_this_one = False
    if templates_of_interest is not None:
        skip_this_one = True
        for template_string in templates_of_interest:
            if template_string in template_exclusion_string:
                skip_this_one = False
                print("template_string not to skip")
                print(template_string)
    return skip_this_one


templates = get_templates()

all_success_rates = []

templates_of_interest = None
#templates_of_interest = ["received two gifts: a"]

templates_can_look_at = []
for template in templates:
    if determine_if_should_skip(templates_of_interest, template["start_exclusion"]):
        continue
    templates_can_look_at.append(template)
    success_rate_by_type = {}
    #print("template:")
    #pprint.pprint(template)
    for i in range(1000):
        tests = get_text_and_completion_once(template)
        evaluation = run_model_and_evaluate(tests)
        success_rate_by_type = update_success_rate_dictionary(evaluation,success_rate_by_type)
    #print("")
    #print("template:")
    #pprint.pprint(template)

    all_success_rates.append(success_rate_by_type)

    #print_success_rate(success_rate_by_type)
    #print("")
    #print("")
    #print("")
    #break
for template,success_rates in zip(templates_can_look_at,all_success_rates):
    print("template")
    print(template["start_exclusion"])
    if determine_if_should_skip(templates_of_interest, template["start_exclusion"]):
        continue
    print("template:")
    pprint.pprint(template)
    print("")
    print_success_rate(success_rates)
    print("")
    print("")
    print("")

#for i in range(500):
#    tests = get_text_and_completion_once()

