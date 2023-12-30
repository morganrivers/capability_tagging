import pandas as pd
import random
import matplotlib.pyplot as plt
import os

def initialize_dataframes():
    columns = ["Node ID", "Type", "Layer", "Name", "Correlation"]
    nodes_df = pd.DataFrame(columns=columns)
    edges_df = pd.DataFrame(columns=["Source", "Target"])
    return nodes_df, edges_df

def populate_dataframes(nodes_df, edges_df, num_layers=4, features_per_layer=30):
    color_map = plt.cm.get_cmap("rainbow")
    
    # Precompute the number of features for each layer
    num_features_per_layer = [random.randint(features_per_layer//2, features_per_layer) for _ in range(num_layers)]

    for layer in range(num_layers):
        num_features = num_features_per_layer[layer]
        num_attention_heads = random.randint(1, 4)

        for head in range(num_attention_heads):
            head_id = f"L{layer+1}H{head+1}"
            head_name = f"Custom Head {head+1}"
            correlation = random.random()
            nodes_df = nodes_df._append(
                {
                    "Node ID": head_id,
                    "Type": "Head",
                    "Layer": layer + 1,
                    "Name": head_name,
                    "Correlation": correlation,
                },
                ignore_index=True,
            )
            
        for feature in range(num_features):
            feature_id = f"L{layer+1}F{feature+1}"
            feature_name = f"Custom Feature {feature+1}"
            feature_correlation = random.random()
            nodes_df = nodes_df._append(
                {
                    "Node ID": feature_id,
                    "Type": "Feature",
                    "Layer": layer + 1,
                    "Name": feature_name,
                    "Correlation": feature_correlation,
                },
                ignore_index=True,
            )
            if random.random() < 0.5:
                edges_df = edges_df._append(
                    {"Source": head_id, "Target": feature_id}, ignore_index=True
                )

        if layer < num_layers - 1:
            next_layer_num_features = num_features_per_layer[layer + 1]
            for feature in range(num_features):
                current_feature_id = f"L{layer+1}F{feature+1}"
                for next_feature in range(next_layer_num_features):
                    next_feature_id = f"L{layer+2}F{next_feature+1}"
                    if random.random() < 0.2:
                        edges_df = edges_df._append(
                            {"Source": current_feature_id, "Target": next_feature_id},
                            ignore_index=True,
                        )

    return nodes_df, edges_df

def main(save_csv=True):
    nodes_df, edges_df = initialize_dataframes()
    nodes_df, edges_df = populate_dataframes(nodes_df, edges_df)
    if save_csv:
        if "data" not in os.listdir():
            os.mkdir("data")
        nodes_df.to_csv("data/nodes_df.csv", index=False)
        edges_df.to_csv("data/edges_df.csv", index=False)
    return nodes_df, edges_df
        
if __name__ == '__main__':
    main()