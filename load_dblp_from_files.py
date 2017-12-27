import networkx as nx
import numpy as np
import random

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


doc_topic_portion_output_file_path = 'data/dblp/doc_topic_portions.txt'

theta_portions = {}

# cal_cos_sim
def cal_cos_sim(source_doc_id, target_doc_id):
    dot_product = np.dot(source_doc_id, target_doc_id)
    norm_a = np.linalg.norm(source_doc_id)
    norm_b = np.linalg.norm(target_doc_id)
    return dot_product / (norm_a * norm_b)

def read_LDA_theta_doc_topic_portion():
    dataFile = open(doc_topic_portion_output_file_path, 'r', encoding='utf-8')
    number_of_topic = 0
    for lineIndex, line in enumerate(dataFile):
        if line.startswith('number_of_topic='):
            number_of_topic = int(line.split('=')[1])
        else:
            splits = line.split('\t')
            doc_id = int(splits[0])

            theta_portion = []
            for topic_index in range(1, number_of_topic + 1):
                portion_splits = splits[topic_index].split(':')
                theta_portion.append(float(portion_splits[1]))

            theta_portions.update({doc_id: np.array(theta_portion)})


    print('Fetching total topics -> [{}], theta portions -> [{}]'.format(number_of_topic,
                                                                         len(theta_portions)))


read_LDA_theta_doc_topic_portion()

# params

author_file_path = 'data/dblp/authors.txt'
paper_file_path = 'data/dblp/papers.txt'
venue_file_path = 'data/dblp/venues.txt'

author_paper_maps_file_path = 'data/dblp/author_paper_maps.txt'
paper_paper_maps_file_path = 'data/dblp/paper_paper_maps.txt'
paper_venue_maps_file_path = 'data/dblp/paper_venue_maps.txt'

author_dict = file_to_dict(author_file_path)
paper_dict = file_to_dict(paper_file_path)
paper_author_maps_dict = file_to_reverse_dict(author_paper_maps_file_path)
paper_paper_maps_dict = file_to_dict(paper_paper_maps_file_path)
paper_venue_maps_dict = file_to_dict(paper_venue_maps_file_path)

limited_paper_node_count = 1000000
node_count = 0

def get_sim_weight_between_2_paper(source_paper_id, target_paper_id):
    sim_weight = 0
    if int(source_paper_id) in theta_portions \
            and int(target_paper_id) in theta_portions:
        sim_weight = cal_cos_sim(theta_portions[int(source_paper_id)],
                                 theta_portions[int(target_paper_id)])
    else:
        print(source_paper_id, target_paper_id)
        sim_weight = random.uniform(0, 1)
    return sim_weight

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


def create_edge_of_paper_and_author(paper_id):

    if paper_id in paper_author_maps_dict:

        author_list = paper_author_maps_dict[paper_id]

        for author_id in author_list:

            if author_id in author_dict:
                add_node_to_dblp_graph(author_id, 'author')

                dblpGraph.add_edge('author_{}'.format(author_id),
                                   'paper_{}'.format(paper_id),
                                   relation_type='write')


for index, paper_paper_map in enumerate(paper_paper_maps_dict):

    if limited_paper_node_count > node_count:

        source_paper_id = paper_paper_map

        if source_paper_id in paper_dict.keys() \
                and int(source_paper_id) in theta_portions:

            set_of_citing_paper_ids = paper_paper_maps_dict[source_paper_id]

            if len(set_of_citing_paper_ids) > 0:

                node_count += 1
                add_node_to_dblp_graph(source_paper_id, 'paper')

                #mapping paper-venue relation
                create_edge_of_paper_and_venue(source_paper_id)

                #mapping author-paper relation
                create_edge_of_paper_and_author(source_paper_id)

                for target_paper_id in set_of_citing_paper_ids:

                    if target_paper_id in paper_dict.keys() \
                            and int(target_paper_id) in theta_portions.keys():

                        add_node_to_dblp_graph(target_paper_id, 'paper')

                        # mapping paper-venue relation
                        create_edge_of_paper_and_venue(target_paper_id)

                        # mapping author-paper relation
                        create_edge_of_paper_and_author(source_paper_id)

                        #calculating similarity between 2 papers
                        sim_weight = get_sim_weight_between_2_paper(source_paper_id,
                                                                    target_paper_id)

                        dblpGraph.add_edge('paper_{}'.format(source_paper_id),
                                           'paper_{}'.format(target_paper_id),
                                           relation_type='refer_to',
                                           weight=sim_weight)

            else:
                print(source_paper_id)
    else:
        break

print(len(dblpGraph.nodes()))
print(len(dblpGraph.edges()))

nx.write_gexf(dblpGraph, 'data/small_paper_dblp_graph.gexf', encoding="utf-8")
