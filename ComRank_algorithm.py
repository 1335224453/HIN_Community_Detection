import matplotlib.pyplot as plt
import networkx as nx
from community import community_louvain

k = 5

# params
author_file_path = 'data/dblp/authors.txt'

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

author_dict = file_to_dict(author_file_path)

# loading DBLP from file
full_com_labelled_dblp_graph = nx.read_gexf('data/labelled_dblp_graph.gexf')

node_communitie_tuples = nx.get_node_attributes(full_com_labelled_dblp_graph, 'community_label_id')

communities = {}
community_counts = {}

for node_communitie_tuple in node_communitie_tuples:
    node_id = node_communitie_tuple
    com_label_id = node_communitie_tuples[node_communitie_tuple]
    if com_label_id in communities:
        communities[com_label_id].append(node_id)
        community_counts[com_label_id]+=1
    else:
        communities.update({com_label_id: [node_id]})
        community_counts.update({com_label_id:1})

community_counts = sorted(community_counts.items(),key=lambda v : v[1], reverse=True)[:k]

for com_tuple in community_counts:

    author_in_com_list = {}

    top_com_label_id = com_tuple[0]

    print('Community id -> {}'.format(top_com_label_id))

    total_author_2_paper_link = 0

    for node_id in communities[top_com_label_id]:
        if full_com_labelled_dblp_graph.node[node_id]['node_type'] == 'author':
            author_degree = nx.degree(full_com_labelled_dblp_graph, node_id)
            total_author_2_paper_link+=author_degree
            author_in_com_list.update({node_id: author_degree})

    author_in_com_list = sorted(author_in_com_list.items(), key=lambda v: v[1], reverse=True)[:10]
    for author_tuple in author_in_com_list:
        author_node_id = author_tuple[0]
        author_name = author_dict[author_node_id.replace('author_', '')]
        print('{} -> {}'.format(author_name, author_tuple[1] / total_author_2_paper_link))

    print('-----')