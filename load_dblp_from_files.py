import networkx as nx


dblpGraph = nx.Graph()

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

# params
author_file_path = 'data/dblp/authors.txt'
paper_file_path = 'data/dblp/papers.txt'
venue_file_path = 'data/dblp/venues.txt'

author_paper_maps_file_path = 'data/dblp/author_paper_maps.txt'
paper_paper_maps_file_path = 'data/dblp/paper_paper_maps.txt'
paper_venue_maps_file_path = 'data/dblp/paper_venue_maps.txt'

paper_dict = file_to_dict(paper_file_path)
paper_paper_maps_dict = file_to_dict(paper_paper_maps_file_path)
paper_venue_maps_dict = file_to_dict(paper_venue_maps_file_path)

limited_paper_node_count = 100

node_count = 0

def add_node_to_dblp_graph(node_id, node_type_value):
    if not dblpGraph.has_node('{}_{}'.format(node_type_value, node_id)):
        dblpGraph.add_node('{}_{}'.format(node_type_value, node_id), node_type=node_type_value)

def create_edge_of_paper_and_venue(paper_id):
    if paper_id in paper_venue_maps_dict:
        venue_id = paper_venue_maps_dict[paper_id][0]

        add_node_to_dblp_graph(venue_id, 'venue')

        dblpGraph.add_edge('paper_{}'.format(paper_id),
                           'venue_{}'.format(venue_id),
                           relation_type='publish_to')


for index, paper_paper_map in enumerate(paper_paper_maps_dict):

    if limited_paper_node_count > node_count:

        source_paper_id = paper_paper_map

        if source_paper_id in paper_dict.keys():

            set_of_citing_paper_ids = paper_paper_maps_dict[source_paper_id]

            if len(set_of_citing_paper_ids) > 0:

                node_count += 1
                add_node_to_dblp_graph(source_paper_id, 'paper')
                #create_edge_of_paper_and_venue(source_paper_id)

                for target_paper_id in set_of_citing_paper_ids:

                    if target_paper_id in paper_dict.keys():
                        add_node_to_dblp_graph(target_paper_id, 'paper')
                        #create_edge_of_paper_and_venue(target_paper_id)
                        dblpGraph.add_edge('paper_{}'.format(source_paper_id),
                                           'paper_{}'.format(target_paper_id),
                                           relation_type='refer_to')
            else:
                print(source_paper_id)
    else:
        break

print(len(dblpGraph.nodes()))
print(len(dblpGraph.edges()))

nx.write_gexf(dblpGraph, 'data/small_paper_dblp_graph.gexf', encoding="utf-8")
