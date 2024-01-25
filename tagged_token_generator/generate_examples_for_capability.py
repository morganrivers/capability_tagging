import random

def get_reasoning_test(exclusion_template, non_exclusion_templates, character_options, relationship_options, irrelevant_content_options, alternative_word_options, categories):
    """
    Generates a reasoning test by varying character names, relationships, irrelevant content, and the use of alternative words.
    This version uses multiple templates and ensures grammatical correctness, with category-specific pet names.
    
    Args:
    templates (list of dict): List of template strings with placeholders.
    character_options (list of dict): List of possible characters with name and pronoun to use in the templates.
    relationship_options (list of str): List of possible relationships to use in the templates.
    irrelevant_content_options (list of str): List of possible irrelevant content to insert in the templates.
    alternative_word_options (list of str): List of possible words to use for expressing alternatives.
    categories (list of dict): List of category information with singular and plural forms.
    
    Returns:
    str: A generated reasoning test string.
    """
    # Randomly choose a name, a relationship, irrelevant content, and an alternative word from the provided options
    character = random.choice(character_options)
    category_dict = random.choice(categories)
    category = category_dict["category"]
    category_plural = category_dict["category_plural"]
    example1, example2 = random.sample(category_dict["examples"], 2)  # Assuming 'examples' contains a list of example pets for the category

    # name = random.choice(name_options)
    name = character['name']
    pronoun = character['pronoun']
    relationship = random.choice(relationship_options)
    [irrelevant_content_1,irrelevant_content_2,irrelevant_content_3] = random.sample(irrelevant_content_options,3)
    alternative_word = random.choice(alternative_word_options)
    first_example_shown, second_example_shown = random.sample([example1,example2], 2)
    pronoun_capitalized = pronoun.capitalize()

    # Construct the test with logical sentence order and coherence

    test_exclusion = exclusion_template.format(name=name, pronoun=pronoun, relationship=relationship, irrelevant_content_1=irrelevant_content_1,irrelevant_content_2=irrelevant_content_2, irrelevant_content_3=irrelevant_content_3, alternative_word=alternative_word, category_plural=category_plural,category=category, example1=example1, example2=example2,first_example_shown=first_example_shown, second_example_shown=second_example_shown,pronoun_capitalized=pronoun_capitalized)
    print(f"exclusion: {test_exclusion}")
    all_tests = {}
    all_tests["start_exclusion"] = {"test":test_exclusion,"correct_completion":example2,"incorrect_completion":example1}
    for key, template in non_exclusion_templates.items():
        test_non_exclusion = template.format(name=name, pronoun=pronoun, relationship=relationship, irrelevant_content_1=irrelevant_content_1,irrelevant_content_2=irrelevant_content_2, irrelevant_content_3=irrelevant_content_3, alternative_word=alternative_word, category_plural=category_plural,category=category, example1=example1, example2=example2,first_example_shown=first_example_shown, second_example_shown=second_example_shown,pronoun_capitalized=pronoun_capitalized)
        # non_exclusion_text = generate_alternative_reasoning_test(template, character_options, relationship_options, irrelevant_content_options, alternative_word_options,categories)
        all_tests[key] = {"test":test_non_exclusion,"correct_completion":example2,"incorrect_completion":example1}
        print(f"{key}: {test_non_exclusion}")
    print("")
    print("")
    print("")

    return all_tests

# Example templates with correct grammar for each structure
templates = [
    {"start_exclusion": "{irrelevant_content_1} {name} really wanted a {first_example_shown} or a {second_example_shown}. {name} asked {relationship} for a {example1} and {relationship} said no, so instead {name} asked for a "},
    {"start_exclusion": "{name} wanted {category}. {name} liked both a {first_example_shown} and a {second_example_shown}. {name} asked {relationship} for a {example1} but they said no! So {name} got a ",
    "start_possession": "{name} wanted {category}. {name} liked both a {first_example_shown} and a {second_example_shown}. When {name} asked {relationship} for a {example2} and they said yes! So {name} got a ",
    "start_nonpossession": "{irrelevant_content_1} {name} wanted a {category}. {name} liked both a {first_example_shown} and maybe a {second_example_shown}. {irrelevant_content_2} When {name} asked {relationship} for a {example1} and was refused, {name} still didn't have a ",
    "correct completion exclusion": "{example2}","correct completion posession": "{example2}","correct completion possession": "{example2}"},
    {"start_exclusion": "{name} loved {category_plural}, especially a {first_example_shown}. {irrelevant_content_1} {name} also would love a {second_example_shown}. {irrelevant_content_2} {relationship} couldn't get {name} a {example1}. {irrelevant_content_3} {name} was happy about getting a ",
    "start_preference": "{name} loved {category_plural}, especially a {first_example_shown}. {irrelevant_content_1} {name} also would love a {second_example_shown}. {irrelevant_content_2} {relationship} was luckily able to get {name} a {example2}. {irrelevant_content_3} {name} was happy about getting a ",
    "correct completion exclusion": "{example2}","correct completion preference": "{example2}"},
    # {"start_exclusion": "{irrelevant_content_1} {name} always dreamed of having {category}. {name} fancied a {first_example_shown} and a {second_example_shown}. After being told no to a {example1} by {relationship}, {name} considered a ",
    # "correct completion exclusion": "{example2}","correct completion permanence": "{example2}","correct completion possession": "{example2}"},
    # {"start_exclusion": "{irrelevant_content_1} {name} was fond of {category_plural}, like a {first_example_shown} and a {second_example_shown}. {irrelevant_content_2} {relationship} said {name} was too young for a {example1}. {irrelevant_content_3} {alternative_word}, {name} then asked for a ",
    # "correct completion exclusion": "{example2}","correct completion permanence": "{example2}","correct completion possession": "{example2}"},
    # {"start_exclusion": "{irrelevant_content_1} It was {name}'s birthday. {name} had always wanted either a {first_example_shown} or a {second_example_shown}. {irrelevant_content_2} {relationship} had already denied a {example1}. {irrelevant_content_3} {alternative_word}, {name} hoped for a ",
    # "correct completion exclusion": "{example2}","correct completion permanence": "{example2}","correct completion possession": "{example2}"},
    # {"start_exclusion": "{irrelevant_content_1} {name} had a love for {category_plural}, particularly a {first_example_shown} and a {second_example_shown}. {irrelevant_content_2} {relationship} said no to a {example1}. {irrelevant_content_3} {alternative_word}, {name} pondered getting a ",
    # "correct completion exclusion": "{example2}","correct completion permanence": "{example2}","correct completion possession": "{example2}"},
    # {"start_exclusion": "{irrelevant_content_1} Having {category} was {name}'s wish. {name} admired both a {first_example_shown} and a {second_example_shown}. {irrelevant_content_2} {relationship} disapproved of a {example1}. {irrelevant_content_3} {alternative_word}, {name} shifted to asking for a ",
    # "correct completion exclusion": "{example2}","correct completion permanence": "{example2}","correct completion possession": "{example2}"},
    # {"start_exclusion": "{irrelevant_content_1} {name} asked {relationship} for a {example1}, but the answer was no. {irrelevant_content_2} {name} also liked the idea of a {example2}. {irrelevant_content_3} {alternative_word}, {name} began thinking about a ",
    # "correct completion exclusion": "{example2}","correct completion permanence": "{example2}","correct completion possession": "{example2}"},
    # {"start_exclusion": "{irrelevant_content_1} {name} thought a {first_example_shown} or a {second_example_shown} would be fun. {irrelevant_content_2} {relationship} thought a {example1} was too much for {name}. {irrelevant_content_3} {alternative_word}, {name} then contemplated a ",
    # "correct completion exclusion": "{example2}","correct completion permanence": "{example2}","correct completion possession": "{example2}"},
    # {"start_exclusion": "{irrelevant_content_1} For {name}, {category} was a big desire. {name} liked both a {first_example_shown} and a {second_example_shown}. {irrelevant_content_2} {relationship} rejected the idea of a {example1}. {irrelevant_content_3} {alternative_word}, {name} leaned towards a ",
    # "correct completion exclusion": "{example2}","correct completion permanence": "{example2}","correct completion possession": "{example2}"}

]
# templates_no_authority
more_interesting_examples = [
    {"start_exclusion": "{irrelevant_content_1} {name} had two {category_plural}, one {first_example_shown} and one {second_example_shown}. {irrelevant_content_2}But oh no! {pronoun_capitalized} lost the {example1}. {irrelevant_content_3} {name} thought, \"at least I still have the ",
    "start_possession": "{irrelevant_content_1} {name} had two {category_plural}, one {first_example_shown} and one {second_example_shown}. {irrelevant_content_2}But oh no! {pronoun_capitalized} lost the {example1}, but later found it again. {irrelevant_content_3} {name} thought, \"It's great I still have the ",
    "correct completion exclusion": "{example2}",
    "correct completion possession": "{example2}"},
    {"start_exclusion": "{irrelevant_content_1} For {name}'s birthday, {name} could choose either a {first_example_shown} or a {second_example_shown}. {irrelevant_content_2} {pronoun_capitalized} decided a {example1} was not what {pronoun} wanted. {irrelevant_content_3} So, on {name}'s birthday, {name} was smiling with {name}'s new ",
    "start_possession": "{irrelevant_content_1} For {name}'s birthday, {name} could choose either a {first_example_shown} or a {second_example_shown}. {irrelevant_content_2} {pronoun_capitalized} decided a {example2} was what {pronoun} wanted. {irrelevant_content_3} So, on {name}'s birthday, {name} was smiling with {name}'s new ",
    "start_preference": "{irrelevant_content_1} For {name}'s birthday, {name} could choose either a {first_example_shown} or a {second_example_shown}. {irrelevant_content_2} {pronoun_capitalized} decided a {example1} was great, but {pronoun} was more excited about {example2}. {irrelevant_content_3} So, on {name}'s birthday, {name} was smiling with {name}'s new ",
    "correct completion exclusion": "{example2}",
    "correct completion possession": "{example2}",
    "correct completion preference": "{example2}"},
    {"start_exclusion": "{irrelevant_content_1} In the kitchen, there were two {category_plural}, a {first_example_shown} and a {second_example_shown}. Mom lost {name}'s {example1}. {irrelevant_content_2} In {name}'s hand was the ",
    "start_possession": "{irrelevant_content_1} In the kitchen, there were two {category_plural}, a {first_example_shown} and a {second_example_shown}. Mom gave {name} the {example2}. {irrelevant_content_2} In {name}'s hand was the ",
    "correct completion exclusion": "{example2}",
    "correct completion posession": "{example2}"},
    {"start_exclusion": "{irrelevant_content_1} {name} had two {category_plural}, a {first_example_shown} and also a {second_example_shown}. {pronoun_capitalized} gave the {example1} to {name}'s friend. In {name}'s room, {name} still kept the ",
    "start_possession": "{irrelevant_content_1} {name} had two {category_plural}, a {first_example_shown} and also a {second_example_shown}. {pronoun_capitalized} gave the {example2} to {name}'s friend. In {name}'s friend's room, {name}'s friend had the ",
    "correct completion exclusion": "{example2}",
    "correct completion posession": "{example2}"}
]

more_generated_examples = [
    {"start_exclusion": "{irrelevant_content_1}Every night, {name} dreamed about {category_plural}. Sometimes {name} dreamed of a {first_example_shown}. {irrelevant_content_2} {name} also sometimes dreamed about a {second_example_shown}. One morning, {relationship} told {name} that the {example1} had turned real! {irrelevant_content_3}Excitedly, {name} looked for other {category_plural} and was excited to find the ",
    "start_existence": "{irrelevant_content_1}Every night, {name} dreamed about {category_plural}. Sometimes {name} dreamed of a {first_example_shown}. {irrelevant_content_2}{name} also sometimes dreamed about a {second_example_shown}. One morning, {relationship} told {name} that the {example2} had turned real! {irrelevant_content_3} Excitedly, {name} looked for {category_plural} and was excited to indeed find the ",
    "start_existence_negation": "{irrelevant_content_1}Every night, {name} dreamed about {category_plural}. Sometimes {name} dreamed of a {first_example_shown}. {irrelevant_content_2}{name} also sometimes dreamed about a {second_example_shown}. One morning, {relationship} told {name} that the {example2} had turned real! {irrelevant_content_3}Excitedly, {name} looked for {category_plural} but was disappointed to not find the ",
    "correct completion exclusion": "{example2}","correct completion existence": "{example2}"},
    {"start_exclusion": "{irrelevant_content_1} While exploring the attic, {name} found an old box with two {category_plural}. At first, {name} only saw a {first_example_shown}. But then {name} noticed there was a {second_example_shown} too! {irrelevant_content_2} {pronoun_capitalized} decided to give away the {example1}. {irrelevant_content_3} At bedtime, {name} felt happy having the ",
    "start_possession": "{irrelevant_content_1} While exploring the attic, {name} found an old box with two {category_plural}. At first, {name} only saw a {first_example_shown}. But then {name} noticed there was a {second_example_shown} too! {irrelevant_content_2} {pronoun_capitalized} decided to keep the {example2}. {irrelevant_content_3} At bedtime, {name} felt happy having the ",
    "start_possession2": "{irrelevant_content_1} While exploring the attic, {name} found an old box with two {category_plural}. At first, {name} only saw a {first_example_shown}. But then {name} noticed there was a {second_example_shown} too! {irrelevant_content_2} {pronoun_capitalized} decided to give away the {example2}. {irrelevant_content_3} At bedtime, {name} felt happy about giving away the ",
    "correct completion exclusion": "{example2}",
    "correct completion possession": "{example2}",
    "correct completion possession2": "{example2}"},
    {"start_exclusion": "{irrelevant_content_1} At the picnic, {name} got a {first_example_shown}. Later in the day, {name} found a {second_example_shown}. {irrelevant_content_2} {pronoun_capitalized} accidentally left the {example1} at the park. {irrelevant_content_3} Thankfully, at home, {name} still had the ",
    "start_possession": "{irrelevant_content_1} At the picnic, {name} got a {first_example_shown}. Later in the day, {name} found a {second_example_shown}. {irrelevant_content_2} {pronoun_capitalized} accidentally left the {example2} at the park. {irrelevant_content_3} Thankfully, at the park, {name} found the ",
    "correct completion exclusion": "{example2}",
    "correct completion possession": "{example2}"},
    {"start_exclusion": "{irrelevant_content_1} {name} received two gifts: a {first_example_shown} and a {second_example_shown}. {irrelevant_content_2} {irrelevant_content_3} {pronoun} didn't like the {example1} so {name}'s favorite was the ",
    "start_exlu_using_a": "{irrelevant_content_1} {name} received two gifts: a {first_example_shown} and a {second_example_shown}. {irrelevant_content_2} {irrelevant_content_3} {pronoun} didn't like a {example1} so {name}'s favorite was a ",
    "start_preference": "{irrelevant_content_1} {name} received two gifts: a {first_example_shown} and a {second_example_shown}. {irrelevant_content_2} {pronoun} always played with the {example2}. {irrelevant_content_3} {name}'s favorite was the ",
    "start_preference_balanced_count": "{irrelevant_content_1} {name} received two gifts: a {first_example_shown} and a {second_example_shown}. {pronoun_capitalized} always played with the {example2}, but {pronoun} was getting tired of the {example1}. {irrelevant_content_3} {name}'s favorite was the ",
    "start_preference_reverse_order": "{irrelevant_content_1} {irrelevant_content_2} {pronoun} always played with a {example2} {name} received two gifts: a {example2} and a {example1}. {irrelevant_content_2} {irrelevant_content_3} {name}'s favorite was the ",
    "correct completion exclusion": "{example2}",
    "correct completion preference": "{example2}"}
]
templates.extend(more_interesting_examples)
#templates.extend(more_interesting_examples)
templates.extend(more_generated_examples)
#templates.extend(more_generated_examples)
#templates.extend(more_generated_examples)


# Example usage with defined templates
name_options = ["Lily", "Emma", "Sophie", "Olivia"]
relationship_options = ["Mom", "Dad", "Grandma", "Grandpa"]
irrelevant_content_options = [
    "It was a sunny day.",
    "Their favorite show was about to start.",
    "The birds were singing outside the window.",
    "It was almost time for dinner.",
    "They were getting ready for bed.",
    "A gentle breeze was blowing through the trees.",
    "The clock struck three in the afternoon.",
    "The cat was napping in the sunny spot.",
    "They were baking cookies in the kitchen.",
    "It was their weekly trip to the library.",
    "The family was planning a weekend trip.",
    "The flowers in the garden were blooming.",
]
irrelevant_content_options.extend([
    "A colorful butterfly fluttered by the window.",
    "They found a shiny pebble on the sidewalk.",
    "A little bird was building a nest in the tree.",
    "The moon was playing hide and seek with the clouds.",
    "A rainbow appeared after the brief rain.",
    "The puppy was chasing its tail in the garden.",
    "They spotted a squirrel scampering up a tree.",
    "The stars were twinkling in the night sky.",
    "A frog was croaking at the pond.",
    "They were drawing pictures with bright crayons.",
    "The train chugged along the distant tracks.",
    "A kite was flying high in the sky.",
    "They had a picnic in the backyard.",
    "A duck family was swimming in the pond.",
    "The wind was playing with the leaves.",
    "They made a fort with cushions and blankets.",
    "A bee was buzzing around the flowers.",
    "The sun was setting, painting the sky orange and pink.",
    "They were playing hide and seek in the garden.",
    "A ladybug landed on a leaf near them.",
    "The ice cream truck played a melody down the street.",
    "They had a fun bubble bath with toy boats.",
    "A group of birds were chirping cheerfully.",
    "The snowflakes were gently falling outside.",
    "They built a sandcastle at the beach.",
    "A balloon was floating up into the sky.",
    "The fish in the aquarium were swimming peacefully.",
    "They were counting the stars at night.",
    "A caterpillar was crawling on a branch.",
    "The fireplace crackled cozily in the evening."
])
irrelevant_content_options.extend([""]*50)
irrelevant_content_options = ["","",""]
# Example character options with gender flipping
character_options = [
    {"name": "Aiden", "pronoun": "he"},
    {"name": "Mia", "pronoun": "she"},
    {"name": "Leo", "pronoun": "he"},
    {"name": "Zoe", "pronoun": "she"},
    {"name": "Eli", "pronoun": "he"},
    {"name": "Ava", "pronoun": "she"},
    {"name": "Theo", "pronoun": "he"},
    {"name": "Isla", "pronoun": "she"},
    {"name": "Lucas", "pronoun": "he"},
    {"name": "Ruby", "pronoun": "she"},
    {"name": "Oscar", "pronoun": "he"},
    {"name": "Grace", "pronoun": "she"},
    {"name": "Finn", "pronoun": "he"},
    {"name": "Chloe", "pronoun": "she"},
    {"name": "Archie", "pronoun": "he"},
    {"name": "Ella", "pronoun": "she"},
    {"name": "Sam", "pronoun": "he"},
    {"name": "Luna", "pronoun": "she"},
    {"name": "Miles", "pronoun": "he"},
    {"name": "Nora", "pronoun": "she"},
    {"name": "Isaac", "pronoun": "he"},
    {"name": "Sophia", "pronoun": "she"},
    {"name": "Jordan", "pronoun": "he"},
    {"name": "Charlie", "pronoun": "he"}
]
alternative_word_options = ["Because of the refusal", "Then", "So"]

categories = [
    {"category": "a fruit", "category_plural": "fruits", "examples": ["apple", "banana", "orange", "strawberry", "grape", "pear", "cherry", "watermelon", "peach", "kiwi"]},
    {"category": "a vegetable", "category_plural": "vegetables", "examples": ["carrot", "broccoli", "corn cob", "potato", "tomato", "cucumber"]},
    {"category": "a musical instrument", "category_plural": "musical instruments", "examples": ["piano", "guitar", "drum", "violin", "flute", "trumpet", "xylophone", "accordion", "harp", "ukulele"]},
    {"category": "a book", "category_plural": "books", "examples": ["fairy tale", "picture book", "adventure story", "animal book", "science book", "comic book", "bedtime story", "fantasy novel", "mystery book", "history book"]},
    {"category": "a type of vehicle", "category_plural": "vehicles", "examples": ["car", "bicycle", "train", "bus", "airplane", "ship", "scooter", "motorcycle", "tractor", "fire truck"]},
    {"category": "a playground equipment", "category_plural": "playground equipment", "examples": ["swing", "slide", "see-saw", "sandbox",  "balance beam", "playhouse"]},
    {"category": "a type of bug", "category_plural": "bugs", "examples": ["butterfly", "ladybug", "ant", "grasshopper", "bee", "spider", "dragonfly", "beetle", "caterpillar", "firefly"]},
    {"category": "a sea creature", "category_plural": "sea creatures", "examples": ["fish", "dolphin", "shark", "octopus", "seahorse", "whale", "jellyfish", "crab", "lobster", "starfish"]},
    {"category": "a bird", "category_plural": "birds", "examples": ["sparrow", "owl", "eagle", "parrot", "penguin", "flamingo", "peacock", "swan", "hummingbird", "woodpecker"]},
    {"category": "a piece of clothing", "category_plural": "clothes", "examples": ["t-shirt", "dress", "hat", "jacket", "sweater", "scarf"]},
    {"category": "a shape", "category_plural": "shapes", "examples": ["circle", "square", "triangle", "rectangle", "star", "heart", "oval", "diamond", "pentagon", "hexagon"]},
    {"category": "a type of cake", "category_plural": "cakes", "examples": ["chocolate cake", "vanilla cake", "strawberry cake", "lemon cake", "carrot cake", "cheesecake", "sponge cake", "red velvet cake", "ice cream cake", "fruit cake"]},
    {"category": "a type of sandwich", "category_plural": "sandwiches", "examples": ["peanut butter and jelly sandwich", "ham and cheese sandwich", "turkey sandwich", "grilled cheese sandwich", "tuna sandwich", "BLT", "chicken sandwich"]},
    {"category": "a type of ice cream", "category_plural": "ice creams", "examples": ["vanilla", "chocolate", "strawberry", "mint chocolate chip", "cookie dough", "rocky road", "butter pecan", "neapolitan", "cookies and cream", "pistachio"]},
    {"category": "a type of tree", "category_plural": "trees", "examples": ["maple tree","apple tree", "cherry tree"]},
    {"category": "a type of hat", "category_plural": "hats", "examples": ["baseball cap", "beanie", "cowboy hat", "sun hat", "beret", "fedora", "bucket hat", "witch hat", "helmet", "crown"]},
    {"category": "a type of shoe", "category_plural": "shoes", "examples": ["sneaker", "boot", "sandal", "loafer", "slipper", "running shoe", "ballet shoe", "hiking boot"]},
    {"category": "a type of bird", "category_plural": "birds", "examples": ["robin", "canary", "falcon", "duck", "goose", "pigeon", "hawk", "ostrich", "parakeet"]},
    {"category": "a type of fish", "category_plural": "fish", "examples": ["goldfish",  "tuna", "salmon", "catfish", "shark", "swordfish"]},
    {"category": "a type of pasta", "category_plural": "pastas", "examples": ["spaghetti", "macaroni", "lasagna", "ravioli"]},
    {"category": "a type of drink", "category_plural": "drinks", "examples": ["water", "juice", "milk", "lemonade", "iced tea", "hot chocolate", "smoothie", "soda", "shake", "coffee"]},
    {"category": "a type of dessert", "category_plural": "desserts", "examples": ["cupcake", "cookie", "brownie", "pie", "tin of pudding", "donut", "tart", "muffin"]},
    {"category": "a type of birdhouse", "category_plural": "birdhouses", "examples": ["wooden birdhouse", "painted birdhouse"]},
    {"category": "a type of cookie", "category_plural": "cookies", "examples": ["chocolate chip cookie", "oatmeal raisin cookie", "sugar cookie", "peanut butter cookie", "snickerdoodle", "gingerbread cookie", "white chocolate cookie", "lemon cookie"]}
]

def main():
    for _ in range(10):
        # print("templates")
        # print(templates)
        template_series = random.choice(templates)
        exclusion_template = None
        # print("template_series")
        # print(template_series)
        non_exclusion_templates = {}
        # Randomly choose a template from the provided list
        for key, value in template_series.items():
            # print("key, value")
            # print(f"{key}, {value}")
            if "start_exclusion" in key:
                exclusion_template = value
            elif "start" in key:
                non_exclusion_templates[key] = value
        # Generate a reasoning test with improved sentence structure
        get_reasoning_test(exclusion_template, non_exclusion_templates, character_options, relationship_options, irrelevant_content_options, alternative_word_options,categories)


# deception might be more like: having objects, and then understanding that when you lie, the object disappears

def get_text_and_completion_once(template_series=None):
    if template_series is None:
        template_series = random.choice(templates)
    exclusion_template = None
    # print("template_series")
    # print(template_series)
    non_exclusion_templates = {}
    # Randomly choose a template from the provided list
    for key, value in template_series.items():
        # print("key, value")
        # print(f"{key}, {value}")
        if "start_exclusion" in key:
            exclusion_template = value
        elif "start" in key:
            non_exclusion_templates[key] = value

    return get_reasoning_test(exclusion_template, non_exclusion_templates, character_options, relationship_options, irrelevant_content_options, alternative_word_options,categories)

def get_templates():
    return templates
