import plotter as plotter
import indicator_tagger as indicator_tagger
import transformer_network as transformer_network

nodes_df, edges_df = transformer_network.main(save_csv=True)
nodes_df = indicator_tagger.main(save_csv=True, load_csv=False,nodes_df=nodes_df)

# You can plot if you want, but probably better to use the jupyter interactive widget instead
# plotter.main(load_csv=False, nodes_df=nodes_df, edges_df=edges_df)
