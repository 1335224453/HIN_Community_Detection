import os
from pathlib import Path

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


paper_file_path = 'data/dblp/papers.txt'
paper_abstract_content_file_path = 'E:\\Python_Projects\\TopRPathSim\data\\dblp\\paper_content_maps.txt'
new_paper_abstract_content_file_path = 'E:\\Python_Projects\\TopRPathSim\\data\\dblp\\new_paper_content_maps.txt'
new_paper_abstract_content_file = open(new_paper_abstract_content_file_path, 'w', encoding='utf-8')

corpus_folder_path = 'E:\\Neo4J\\document_content\\preprocessed_text'

paper_dict = file_to_dict(paper_file_path)
paper_abstract_content_dict = file_to_dict(paper_abstract_content_file_path)


paper_not_found_in_file = []
found_paper_in_corpus = []
existed_paper_in_corpus = []

for paper_id in paper_dict:
    if paper_id not in paper_abstract_content_dict:
        paper_not_found_in_file.append(paper_id)

print(len(paper_not_found_in_file))

for file in os.listdir(corpus_folder_path):
    if file.endswith(".txt"):
        filePath = os.path.join(corpus_folder_path, file)
        paper_id = file.replace('.txt', '')
        if paper_id in paper_not_found_in_file:
            found_paper_in_corpus.append(paper_id)
            contents = Path(filePath).read_text().replace('\n', '')
            print('{} -> {}'.format(paper_id, contents))
            new_paper_abstract_content_file.write('{}\t{}\n'.format(paper_id, contents))

        # if paper_id in paper_not_found_in_file:
        #     found_paper_in_corpus.append(paper_id)

print(len(found_paper_in_corpus))
new_paper_abstract_content_file.close()