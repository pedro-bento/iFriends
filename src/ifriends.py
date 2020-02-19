import networkx as nx
import matplotlib.pyplot as plt
import web_scrapper
import sys

def get_relations_from_args():
    if len(sys.argv) is 3:
        relations = web_scrapper.get_relations(sys.argv[1], sys.argv[2])
        del sys.argv # minimize password trace
    elif len(sys.argv) is 2:
        relations = web_scrapper.load_relations_from_json(sys.argv[1])
    else:
        sys.exit("Incorrect arguments format, use:\npython3 ifriends.py \"username\" \"password\"\npython3 ifriends.py \"file_path\"")
    return relations

def create_graph_from_relations(relations):
    G = nx.Graph()
    nodes = [user for user in relations]
    G.add_nodes_from(nodes)
    edges = {(user, friend) for user in relations for friend in relations[user]}
    G.add_edges_from(edges)
    return G

def show_graph(G):
    nx.draw_networkx(G, pos = nx.kamada_kawai_layout(G), with_labels = False, node_size = 100)
    plt.show()

show_graph(create_graph_from_relations(get_relations_from_args()))
