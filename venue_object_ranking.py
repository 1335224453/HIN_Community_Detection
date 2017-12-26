
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

venue_file_path = 'data/dblp/venues.txt'
paper_venue_maps_file_path = 'data/dblp/paper_venue_maps.txt'
venue_dict = file_to_dict(venue_file_path)
venue_paper_maps = file_to_reverse_dict(paper_venue_maps_file_path)

venue_paper_dict_score = {}
total_link_count = 0

for venue_id in venue_paper_maps:
    total_link_count+=len(venue_paper_maps[venue_id])
    venue_paper_dict_score.update({venue_dict[venue_id][0]:len(venue_paper_maps[venue_id])})

#sorting
venue_paper_dict_score = sorted(venue_paper_dict_score.items(),
                                key=lambda value: value[1], reverse=True)

for tuple in venue_paper_dict_score:
    print('{} -> {}'.format(tuple[0], tuple[1] / total_link_count))