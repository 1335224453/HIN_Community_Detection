import matplotlib.pyplot as plt
import networkx as nx
from community import community_louvain



# loading DBLP from file
full_dblp_graph = nx.read_gexf('data/small_paper_dblp_graph.gexf')

# initialize community_label_id attribute to node, default value = -1
nx.set_node_attributes(full_dblp_graph, '-1', 'community_label_id')

def get_paper_only_graph():
    paper_only_dblp_graph = nx.Graph()

    for (p, d) in full_dblp_graph.node(data=True):
        if d['node_type'] == 'paper':
            paper_only_dblp_graph.add_node(p)

    for s, t, a in full_dblp_graph.edges(data=True):
        if s in paper_only_dblp_graph.nodes() and t in paper_only_dblp_graph.nodes():
            paper_only_dblp_graph.add_edge(s, t, weight=a['weight'])

    return paper_only_dblp_graph


paper_only_dblp_graph = get_paper_only_graph()
partitions = community_louvain.best_partition(paper_only_dblp_graph)

for node, community_id in partitions.items():
    full_dblp_graph.node[node]['community_label_id'] = community_id


#assign_possible_community_label_id_to_node
def assign_possible_community_label_id_to_node(target_node):

    neighbors = full_dblp_graph.neighbors(target_node)

    possible_community_id_list = {}

    for neighbor_node_id in neighbors:
        if full_dblp_graph.node[neighbor_node_id]['node_type'] == 'paper':
            community_label_id = full_dblp_graph.node[neighbor_node_id]['community_label_id']
            if community_label_id in possible_community_id_list:
                possible_community_id_list[community_label_id] += 1
            else:
                possible_community_id_list.update({community_label_id: 1})

    possible_community_id = sorted(possible_community_id_list.items(),
                                   key=lambda value: value[1], reverse=True)[:1][0][0]
    full_dblp_graph.node[target_node]['community_label_id'] = possible_community_id


for (p, d) in full_dblp_graph.node(data=True):
    if d['node_type'] == 'author':
        assign_possible_community_label_id_to_node(p)
    if d['node_type'] == 'venue':
        assign_possible_community_label_id_to_node(p)


nx.write_gexf(full_dblp_graph, 'data/labelled_dblp_graph.gexf', encoding="utf-8")
