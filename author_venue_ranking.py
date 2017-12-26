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
venue_file_path = 'data/dblp/venues.txt'
author_paper_maps_file_path = 'data/dblp/author_paper_maps.txt'
paper_venue_maps_file_path = 'data/dblp/paper_venue_maps.txt'

author_dict = file_to_dict(author_file_path)
venue_dict = file_to_dict(venue_file_path)
author_paper_maps = file_to_dict(author_paper_maps_file_path)
paper_venue_maps = file_to_dict(paper_venue_maps_file_path)
venue_paper_maps = file_to_reverse_dict(paper_venue_maps_file_path)

venue_author_count_dict = {}

for author_id in author_dict:
    paper_list = author_paper_maps[author_id]
    for paper_of_author in paper_list:
        if paper_of_author in paper_venue_maps:
            submit_at_venue_id = paper_venue_maps[paper_of_author][0]
            if submit_at_venue_id in venue_author_count_dict:
                if author_id in venue_author_count_dict[submit_at_venue_id]:
                    venue_author_count_dict[submit_at_venue_id][author_id] += 1
                else:
                    venue_author_count_dict[submit_at_venue_id].update({author_id: 1})
            else:
                venue_author_count_dict.update({submit_at_venue_id: {author_id: 1}})


#target_venue_id = '8' #VBLD
target_venue_id = '158' #KDD
total_link_to_target_venue = len(venue_paper_maps[target_venue_id])
print(venue_dict[target_venue_id][0])
print('Total links -> {}'.format(total_link_to_target_venue))

target_venue_list = venue_author_count_dict[target_venue_id]
target_venue_list = sorted(target_venue_list.items(),
                                key=lambda value: value[1], reverse=True)

for index, author in enumerate(target_venue_list):
    if index < 10:
        author_name = author_dict[author[0]][0]
        print('{}) {} -> {}'.format(index, author_name, author[1] / total_link_to_target_venue))
    else:
        break