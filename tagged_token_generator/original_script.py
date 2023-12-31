import random

# Function to generate reasoning tests by varying specific phrases, names, and word order
def generate_reasoning_test(template, name_options, relationship_options):
    """
    Generates a reasoning test by varying character names and relationships.
    
    Args:
    template (str): The template string with placeholders for names and relationships.
    name_options (list of str): List of possible names to use in the template.
    relationship_options (list of str): List of possible relationships to use in the template.
    
    Returns:
    str: A generated reasoning test string.
    """
    # Randomly choose a name and a relationship from the provided options
    name = random.choice(name_options)
    relationship = random.choice(relationship_options)

    # Replace placeholders in the template with the chosen name and relationship
    test = template.replace("{name}", name).replace("{relationship}", relationship)
    return test

# Example usage
template = "{name} likes cats and dogs. She asked her {relationship} for a dog and her {relationship} said no, so instead she asked for a "
name_options = ["Lily", "Emma", "Sophie", "Olivia"]
relationship_options = ["mom", "dad", "grandma", "grandpa"]

# Generate a reasoning test
generated_test = generate_reasoning_test(template, name_options, relationship_options)
print(generated_test)
