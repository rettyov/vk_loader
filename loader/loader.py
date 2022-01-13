from tqdm import tqdm


def get_type(vk, link):
    screen_name = link.rsplit('/')[-1]
    return vk.utils.resolveScreenName(screen_name=screen_name)


def get_data(vk, links):
    data = []
    for link in tqdm(links, desc='Processing links...', leave=False):
        type_link_request = get_type(vk, link)

        if not type_link_request:
            continue

        if type_link_request['type'] == 'group':
            return []

        if type_link_request['type'] == 'user':
            link_data = {
                'link': link,
                'id': type_link_request['object_id']
            }
            data.append(link_data)
    return data
