import matplotlib.pyplot as plt
import networkx as nx
import random
import pandas as pd
import matplotlib.colors as mcolors


def remove_isolated_nodes(nodes_df, edges_df):
    # Identify nodes that are involved in edges
    involved_nodes = set(edges_df['Source']).union(set(edges_df['Target']))

    # Filter the nodes dataframe to keep only nodes that have edges
    filtered_nodes_df = nodes_df[nodes_df['Node ID'].isin(involved_nodes)]

    return filtered_nodes_df

def create_label_dictionary(nodes_df):
    return {row["Node ID"]: row["Name"] for _, row in nodes_df.iterrows()}

def create_position_dictionary(nodes_df):
    pos = {}
    for _, row in nodes_df.iterrows():
        if row["Type"] == "Head":
            pos[row["Node ID"]] = (row["Layer"] * 2, -int(row["Name"].split()[-1]))
        else:
            pos[row["Node ID"]] = (row["Layer"] * 2 + 1, -int(row["Name"].split()[-1]))
    return pos

def build_graph_from_dataframes(nodes_df, edges_df):
    G = nx.DiGraph()
    color_map = plt.cm.get_cmap("rainbow")
    for _, row in nodes_df.iterrows():
        G.add_node(row["Node ID"], color=color_map(row["Correlation"]))
    for _, row in edges_df.iterrows():
        G.add_edge(row["Source"], row["Target"])
    return G

def draw_graph(G, pos, labels, nodes_df):
    plt.figure(figsize=(15, 10))
    ax = plt.gca()

    # Keep track of colors used for nodes
    node_colors = []

    for node_type in ["Head", "Feature"]:
        nodelist = [
            node
            for node, data in G.nodes(data=True)
            if not nodes_df[nodes_df["Node ID"] == node].empty
            and nodes_df[nodes_df["Node ID"] == node]["Type"].iloc[0] == node_type
        ]

        node_shapes = "o" if node_type == "Head" else "s"
        colors = [
            data["color"] for node, data in G.nodes(data=True) if node in nodelist
        ]
        node_colors.extend(colors)

        nx.draw_networkx_nodes(
            G,
            pos,
            nodelist=nodelist,
            node_shape=node_shapes,
            node_size=2000,
            node_color=colors,
            ax=ax
        )

    nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=20, ax=ax)
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, ax=ax)
    
    # Create a colorbar
    sm = plt.cm.ScalarMappable(cmap=plt.cm.rainbow, norm=plt.Normalize(vmin=0, vmax=1))
    sm.set_array([])
    plt.colorbar(sm, ax=ax, orientation='vertical')

    plt.title("Flow Chart with Custom Node Shapes, Colors, and Labels")
    plt.show()

def main(load_csv=True,nodes_df=None,edges_df=None):
    if load_csv:
        nodes_df = pd.read_csv('data/nodes_df.csv',index_col=False)
        edges_df = pd.read_csv('data/edges_df.csv',index_col=False)

    # Main execution
    nodes_df = remove_isolated_nodes(nodes_df, edges_df)
    labels = create_label_dictionary(nodes_df)
    pos = create_position_dictionary(nodes_df)
    G = build_graph_from_dataframes(nodes_df, edges_df)
    draw_graph(G, pos, labels, nodes_df)

if __name__ == '__main__':
    main()
