import matplotlib.pyplot as plt
import networkx as nx
from community import community_louvain

import time

start_time = time.time()


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

def file_to_dict(file_name):
    result = dict()
    f = open(file_name, 'r', encoding='utf-8')
    for line in f:
        splited = line.rstrip().split('\t')
        if splited[0] in result:
            result[splited[0]].append(splited[1])
        else:
            result.update({splited[0]: [splited[1]]})
    f.close()
    return result


def file_to_reverse_dict(file_name):
    result = dict()
    f = open(file_name, 'r', encoding='utf-8')
    for line in f:
        splited = line.rstrip().split('\t')
        if splited[1] in result:
            result[splited[1]].append(splited[0])
        else:
            result.update({splited[1]: [splited[0]]})
    f.close()
    return result

author_file_path = 'data/dblp/authors.txt'
author_paper_file_path = 'data/dblp/author_paper_maps.txt'
author_dict = file_to_dict(author_file_path)
paper_author_maps_dict = file_to_reverse_dict(author_paper_file_path)
author_paper_maps_dict = file_to_dict(author_paper_file_path)

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

print(len(partition.values()))

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
node_labels = {}
drawed_node_list = []
not_dominated_node_list = []
drawed_edge_list = []

def find_top_10_authors():
    tmp = {}
    top_authors = []
    for author in author_paper_maps_dict:
        tmp.update({author:len(author_paper_maps_dict[author])})
    tmp = sorted(tmp.items(),key=lambda value: value[1], reverse=True)[:50]
    for top_author in tmp:
        top_authors.append(top_author[0])
    return top_authors

top_10_authors = find_top_10_authors()
print(top_10_authors)

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

added_author_nodes = []

for index, dominated_community_id in enumerate(sorted_partition_list):
    if count <= 3:
        #color = '#{:06x}'.format(random.randint(0, 256 ** 3))
        color = defined_color[index]
        for index, labelled_value in enumerate(partition.values()):
            if labelled_value == dominated_community_id[0]:
                drawed_node_value = get_node_at_index(index)
                #print(g.nodes(data=True)[drawed_node_value])
                current_community_nodes = []
                if g.nodes(data=True)[drawed_node_value]['node_type'] == 'paper':

                    paper_id = drawed_node_value.replace('paper_', '')
                    if paper_id in paper_author_maps_dict:
                        first_author_id = paper_author_maps_dict[paper_id][0]
                        if first_author_id in top_10_authors and first_author_id not in added_author_nodes:
                            added_author_nodes.append(first_author_id)
                            first_author_name = author_dict[first_author_id][0]
                            print(first_author_name)
                            node_labels.update({drawed_node_value:first_author_name})
                        #print(first_author_name)

                    current_community_nodes.append(drawed_node_value)
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
                       node_size=200, alpha=0.4)

nx.draw_networkx_labels(drawedGraph,
                        pos,
                        font_size=15,
                        labels=node_labels)

# nx.draw_networkx_nodes(g,
#                        pos,
#                        nodelist=not_dominated_node_list,
#                        node_color='#e0e0eb',
#                        node_size=300, alpha=0.2)

# nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)
edge_labels = nx.get_edge_attributes(drawedGraph, 'relation_type')
nx.draw_networkx_edges(drawedGraph, pos, edgelist=drawedGraph.edges(),width=1,alpha=1)

plt.show()

# your code
elapsed_time = time.time() - start_time
print(elapsed_time)