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
#venue_file_path = 'data/dblp/venues.txt'
author_paper_maps_file_path = 'data/dblp/author_paper_maps.txt'
#paper_venue_maps_file_path = 'data/dblp/paper_venue_maps.txt'

author_dict = file_to_dict(author_file_path)
#venue_dict = file_to_dict(venue_file_path)
author_paper_maps = file_to_dict(author_paper_maps_file_path)
#paper_venue_maps = file_to_dict(paper_venue_maps_file_path)
#venue_paper_maps = file_to_reverse_dict(paper_venue_maps_file_path)

total_link_count = 0
author_paper_count_dict = {}

for author_id in author_paper_maps:
    total_link_count += len(author_paper_maps[author_id])
    author_paper_count_dict.update({author_id: len(author_paper_maps[author_id])})

author_paper_count_dict = sorted(author_paper_count_dict.items(),key=lambda value : value[1], reverse=True)[:10]

for tuple in author_paper_count_dict:
    author_name = author_dict[tuple[0]][0]
    ranking_score = round(tuple[1] / total_link_count, 8)
    print('{}\t{}'.format(author_name, ranking_score))

