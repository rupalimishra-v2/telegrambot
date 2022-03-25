def generate_group_data(group_link, current_date, current_time, text):
    group_data = [group_link, current_date, current_time, text]
    return group_data


def convert_list_into_list_of_lists(group_links, number_of_items):
    result = []
    for idx in range(0, number_of_items):
        result.append(group_links[idx::number_of_items])
    return result
