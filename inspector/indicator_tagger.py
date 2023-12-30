import pandas as pd
import random

# Function to update the indicators for each node based on the token generation
def update_indicators(row, activated_nodes, tags):
    """
    Updates the indicators for a node based on the activated nodes and tags in a token generation.
    
    :param row: A row from the DataFrame representing a node.
    :param activated_nodes: List of nodes activated in the current token generation.
    :param tags: List of tags associated with the current token generation.
    :return: Updated row with the 'Indicators' column modified.
    """
    if row['Node ID'] in activated_nodes:
        for tag in tags:
            row['Indicators'][tag] = row['Indicators'].get(tag, 0) + 1
    return row

def artificially_activate_nodes(tags, nodes, core_nodes_per_tag, correlation_factor, fraction_nodes_selected_each_tag, max_num_tags_to_select):
    # selected_tags = random.sample(tags, random.randint(1, num_tags))
    # max_num_tags_to_select = random.randint(1, num_tags)

    # randomly select max_num_tags_to_select of the available tags as active in the model for this generation 
    # if correlation is 1, then the core nodes will be active for these tags
    # only 
    selected_tags = random.sample(tags,max_num_tags_to_select) 

    all_core_nodes_this_generation = []
    selected_nodes = []

    # For each tag, select correlation fraction core nodes and 1-correlation other nodes
    for tag in selected_tags:
        core_nodes = core_nodes_per_tag[tag]
        if tag == "tag3":
            print("tag")
            print(tag)
            print("core_nodes expected")
            print(core_nodes)

        # if correlation 1, all of them. If correlation 0, fraction_nodes_selected_each_tag * core nodes

        # int(len(core_nodes) * fraction_nodes_selected_each_tag) # correlation 0
        # len(core_nodes) # correlation 1

        # test:
        
        # In [12]: correlation = 1
        # In [14]: fraction_nodes_selected_each_tag = 0.25
        # In [16]: len_core_nodes = 100
        # In [18]: int((1-correlation)* len_core_nodes * fraction_nodes_selected_each_tag + correlation *len_core_nodes)
        # Out[18]: 100
        # In [19]: correlation = 0
        # In [20]: int((1-correlation)* len_core_nodes * fraction_nodes_selected_each_tag + correlation *len_core_nodes)
        # Out[20]: 25
        # In [21]: correlation = .5
        # In [22]: int((1-correlation)* len_core_nodes * fraction_nodes_selected_each_tag + correlation *len_core_nodes)
        # Out[22]: 62
        # In [24]: (25/100+1)/2
        # Out[24]: 0.625
        
        num_core_nodes_to_add = int((1-correlation_factor)* len(core_nodes) * fraction_nodes_selected_each_tag + correlation_factor *len(core_nodes))
        core_nodes_that_are_used = random.sample(core_nodes, num_core_nodes_to_add)
        if correlation_factor == 1:
            assert(len(core_nodes_that_are_used) == len(core_nodes))
            assert(set(core_nodes_that_are_used) == set(core_nodes))

        ancillary_nodes = [node for node in nodes if node not in core_nodes_that_are_used]

        # if correlation 1, none of them.
        # if correlation 0, fraction_nodes_selected_each_tag.ancillary nodes
        num_ancillary_nodes_to_add = int(len(ancillary_nodes) * (1-correlation_factor)*fraction_nodes_selected_each_tag)  
        
        ancillary_nodes_used = random.sample(ancillary_nodes, num_ancillary_nodes_to_add)
        # print("core_nodes_that_are_used")
        # print(core_nodes_that_are_used)
        if correlation_factor == 1:
            assert len(ancillary_nodes_used) == 0
        selected_nodes.extend(core_nodes_that_are_used)
        selected_nodes.extend(ancillary_nodes_used)
        # if correlation is 1, then all core nodes are added and no ancillary are added.
        # If correlation 0, then a completely random subset of nodes will be added.

        # print("selected_nodes actual")
        # print(selected_nodes)
        # print("")
        all_core_nodes_this_generation.extend(core_nodes) # all the core nodes for all the two selected tags


    # for a single generation, some set of nodes are active. 
    # Above, we've looped over the available tags and artificially activated the nodes that should be active. 
    # Sometimes, these nodes may overlap.
    # A given generation always highlights some set of nodes (double counted nodes are not doubly activated)
    # So, remove duplicated activated nodes.
    print("selected_nodes")
    print(selected_nodes)
    selected_nodes = list(set(selected_nodes))
    all_core_nodes_this_generation = list(set(all_core_nodes_this_generation))

    #if correlation is 1, a given tag must have exactly and only the core nodes for that tag.
    if correlation_factor == 1:
        # print("selected_nodes core nodes")
        # print(selected_nodes)
        # print(all_core_nodes_this_generation)
        assert set(selected_nodes) == set(all_core_nodes_this_generation)


    return selected_nodes, selected_tags

def generate_token_generations_with_correlation(num_generations, nodes, num_tags, tags, correlation_factor=0.7):
    """
    Generates dummy data for token generations with correlation between tags and nodes.
    Each token generation includes a random subset of nodes and a random subset of tags.
    Tags are more likely to activate similar nodes (correlation).

    :param num_generations: Number of token generations to create.
    :param nodes: List of node IDs.
    :param num_tags: Number of tags available.
    :param tags: List of tag names.
    :param correlation_factor: Factor to determine how strong the correlation between tags and nodes should be.
    :return: List of tuples, each containing a list of nodes and a list of tags for a token generation.
    """
    token_generations = []
    
    # Assign core nodes for each tag ()
    # num_nodes_in_core_nodes = random.randint(1, len(nodes)//30) # between 1 and 1/30 of the nodes are in the core nodes 
    # core_nodes_per_tag = {tag: random.sample(nodes, random.randint(1, len(nodes)//30)) for tag in tags}
    fraction_nodes_selected_each_tag = 1/30
    max_num_tags_to_select = 2 #random.randint(1, num_tags)
    
    num_nodes_activated_per_tag = 10

    # number_to_divide_num_nodes_by_to_get_num_core_nodes = int(1/fraction_nodes_selected_each_tag)
    core_nodes_per_tag = {tag: random.sample(nodes, num_nodes_activated_per_tag) for tag in tags} # randomly assign 2 nodes to eacn tag.
    print("core_nodes_per_tag")
    print(core_nodes_per_tag)
    print("generating values for all "+str(num_tags) +" tags")
    for _ in range(num_generations):
        nodes_activated_in_token_generation, tags_for_token = artificially_activate_nodes(tags, nodes, core_nodes_per_tag, correlation_factor, fraction_nodes_selected_each_tag, max_num_tags_to_select)
        token_generations.append((nodes_activated_in_token_generation, tags_for_token))
        if "tag3" in tags_for_token:
            print("tag 3 nodes activated")
            print(nodes_activated_in_token_generation)
    return token_generations

def populate_indicator_column(nodes_df,token_generations_correlated):
    # Reset and update the DataFrame's 'Indicators' column
    nodes_df['Indicators'] = [{} for _ in range(len(nodes_df))]
    for nodes, tags in token_generations_correlated:
        # print("nodes")
        # print(nodes)
        # print("tag")
        # print(tags)
        nodes_df = nodes_df.apply(lambda row: update_indicators(row, nodes, tags), axis=1)

    return nodes_df

def main(save_csv = True, load_csv = True, nodes_df = None):
    if load_csv:
        nodes_df = pd.read_csv('data/nodes_df.csv',index_col=False)

    num_tags = 100

    # Sample tags for demonstration
    sample_tags = []
    for i in range(num_tags):
        sample_tags.append("tag"+str(i))
    # Number of token generations
    num_token_generations = 1000

    # Generate dummy data for 100 token generations with some correlation
    token_generations_correlated = generate_token_generations_with_correlation(num_generations=num_token_generations, nodes=list(nodes_df['Node ID']), num_tags=len(sample_tags), tags=sample_tags, correlation_factor=.7)
    nodes_df = populate_indicator_column(nodes_df,token_generations_correlated)

    if save_csv:
        nodes_df.to_csv("data/nodes_df.csv", index=False)
    else:
        return nodes_df

if __name__ == '__main__':
    main()