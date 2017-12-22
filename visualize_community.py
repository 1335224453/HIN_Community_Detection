import matplotlib.pyplot as plt
import networkx as nx
from community import community_louvain


def community_layout(g, partition):
    """
    Compute the layout for a modular graph.


    Arguments:
    ----------
    g -- networkx.Graph or networkx.DiGraph instance
        graph to plot

    partition -- dict mapping int node -> int community
        graph partitions


    Returns:
    --------
    pos -- dict mapping int node -> (float x, float y)
        node positions

    """

    pos_communities = _position_communities(g, partition, scale=3.)

    pos_nodes = _position_nodes(g, partition, scale=1.)

    # combine positions
    pos = dict()
    for node in g.nodes():
        pos[node] = pos_communities[node] + pos_nodes[node]

    return pos


def _position_communities(g, partition, **kwargs):
    # create a weighted graph, in which each node corresponds to a community,
    # and each edge weight to the number of edges between communities
    between_community_edges = _find_between_community_edges(g, partition)

    communities = set(partition.values())
    hypergraph = nx.DiGraph()
    hypergraph.add_nodes_from(communities)
    for (ci, cj), edges in between_community_edges.items():
        hypergraph.add_edge(ci, cj, weight=len(edges))

    # find layout for communities
    pos_communities = nx.spring_layout(hypergraph, **kwargs)

    # set node positions to position of community
    pos = dict()
    for node, community in partition.items():
        pos[node] = pos_communities[community]

    return pos


def _find_between_community_edges(g, partition):
    edges = dict()

    for (ni, nj) in g.edges():
        ci = partition[ni]
        cj = partition[nj]

        if ci != cj:
            try:
                edges[(ci, cj)] += [(ni, nj)]
            except KeyError:
                edges[(ci, cj)] = [(ni, nj)]

    return edges


def _position_nodes(g, partition, **kwargs):
    """
    Positions nodes within communities.
    """

    communities = dict()
    for node, community in partition.items():
        try:
            communities[community] += [node]
        except KeyError:
            communities[community] = [node]

    pos = dict()
    for ci, nodes in communities.items():
        subgraph = g.subgraph(nodes)
        pos_subgraph = nx.spring_layout(subgraph, **kwargs)
        pos.update(pos_subgraph)

    return pos

plt.figure(figsize=(12, 12))
plt.axis('off')
#g = nx.read_gexf('data/small_dblp_graph.gexf')
g = nx.read_gexf('data/small_paper_dblp_graph.gexf')
#g = nx.karate_club_graph()
partition_list = {}
# g = nx.karate_club_graph()
partition = community_louvain.best_partition(g)

color_partition_id_maps = []
color_maps = []

for value in partition.values():
    if value not in partition_list:
        partition_list.update({value: 1})
    else:
        partition_list[value] += 1

# for partition_id in partition_list:
#     color = 'white'
#     color_partition_id_maps.append(color)

sorted_partition_list = sorted(partition_list.items(), key=lambda value: value[1], reverse=True)

count = 0


color_maps = []
drawed_node_list = []
not_dominated_node_list = []
drawed_edge_list = []


def get_node_at_index(index):
    for node_index, node_value in enumerate(g.nodes()):
        if index == node_index:
            return node_value


defined_color = []
defined_color.append('red')
defined_color.append('green')
defined_color.append('blue')
defined_color.append('#9933ff')
defined_color.append('#990099')
defined_color.append('#669900')

for index, dominated_community_id in enumerate(sorted_partition_list):
    if count <= 3:
        #color = '#{:06x}'.format(random.randint(0, 256 ** 3))
        color = defined_color[index]
        for index, labelled_value in enumerate(partition.values()):
            if labelled_value == dominated_community_id[0]:
                drawed_node_value = get_node_at_index(index)
                #print(g.nodes(data=True)[drawed_node_value])
                if g.nodes(data=True)[drawed_node_value]['node_type'] == 'paper':
                    drawed_node_list.append(drawed_node_value)
                    color_maps.append(color)
        count += 1
    else:
        break

for (p, d) in g.nodes(data=True):
    if p not in drawed_node_list:
        not_dominated_node_list.append(p)

#print(drawed_node_list)

for s, t, a in g.edges(data=True):
    if s in drawed_node_list and t in drawed_node_list:
        drawed_edge_list.append((s, t))

drawedGraph = nx.Graph()
drawedGraph.add_nodes_from(drawed_node_list)
drawedGraph.add_edges_from(drawed_edge_list)

# print(partition)
#

# drawing node
pos = nx.spring_layout(drawedGraph)  # positions for all nodes
nx.draw_networkx_nodes(drawedGraph,
                       pos,
                       nodelist=drawed_node_list,
                       node_color=color_maps,
                       node_size=500, alpha=0.3)

# nx.draw_networkx_nodes(g,
#                        pos,
#                        nodelist=not_dominated_node_list,
#                        node_color='#e0e0eb',
#                        node_size=300, alpha=0.2)

# nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)
edge_labels = nx.get_edge_attributes(drawedGraph, 'relation_type')
nx.draw_networkx_edges(drawedGraph, pos, edgelist=drawedGraph.edges(),width=1,alpha=1)

plt.show()
