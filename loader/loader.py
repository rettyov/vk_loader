from tqdm import tqdm
from vk_api import ApiError


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
            link_data = get_user_data(vk, link_data)
            data.append(link_data)

    return data


def get_profile_desc(vk, user_id):
    fields = (''
              + 'verified, '
              + 'sex, '
              + 'bdate, '
              + 'city, '
              + 'country, '
              + 'home_town, '
              + 'photo_max, '
              + 'has_mobile, '
              + 'contacts, '
              + 'site, '
              + 'education, '
              + 'universities, '
              + 'schools, '
              + 'status, '
              + 'last_seen, '
              + 'followers_count, '
              + 'counters, '
              + 'occupation, '
              + 'nickname, '
              + 'relatives, '
              + 'relation, '
              + 'personal, '
              + 'connections, '
              + 'exports, '
              + 'wall_comments, '
              + 'activities, '
              + 'interests, '
              + 'music, '
              + 'movies, '
              + 'tv, '
              + 'books, '
              + 'games, '
              + 'about, '
              + 'quotes, '
              + 'can_post, '
              + 'can_see_all_posts, '
              + 'can_see_audio, '
              + 'can_write_private_message, '
              + 'timezone, '
              + 'screen_name'
              )
    return vk.users.get(user_ids=user_id, fields=fields)[0]


def add_profile_desc(link_data, profile_data):
    for (k, v) in profile_data.items():
        link_data[k] = v
    return link_data


def get_user_friends(vk, user_id):
    try:
        return vk.friends.get(user_id=user_id)
    except ApiError:
        return {}


def add_user_friends(link_data, user_friends):
    if 'counters' in link_data:
        link_data['counters']['friends'] = user_friends
    else:
        link_data['counters'] = {'friends': user_friends}
    return link_data


def get_user_followers(vk, user_id):
    try:
        return vk.users.getFollowers(user_id=user_id)
    except ApiError:
        return {}


def add_user_followers(link_data, user_followers):
    if 'counters' in link_data:
        link_data['counters']['followers'] = user_followers
    else:
        link_data['counters'] = {'followers': user_followers}
    return link_data


def get_user_gifts(vk, user_id):
    try:
        return vk.gifts.get(user_id=user_id)
    except ApiError:
        return {}


def add_user_gifts(link_data, user_gifts):
    if 'counters' in link_data:
        link_data['counters']['gifts'] = user_gifts
    else:
        link_data['counters'] = {'gifts': user_gifts}
    return link_data


def get_user_groups(vk, user_id):
    try:
        return vk.groups.get(user_id=user_id)
    except ApiError:
        return {}


def get_group_desc(vk, group_ids):
    if not group_ids:
        return {}

    try:
        return vk.groups.getById(group_ids=','.join(map(str, group_ids)))
    except ApiError:
        return {}


def add_user_groups(link_data, user_groups, group_desc):
    user_groups['items'] = group_desc
    if 'counters' in link_data:
        link_data['counters']['pages'] = user_groups
    else:
        link_data['counters'] = {'pages': user_groups}
    return link_data


def get_user_videos(vk, user_id):
    try:
        return vk.video.get(owner_id=user_id, extended=1)
    except ApiError:
        return {}


def add_user_videos(link_data, user_videos):
    if 'counters' in link_data:
        link_data['counters']['videos'] = user_videos
    else:
        link_data['counters'] = {'videos': user_videos}
    return link_data


def get_user_photos(vk, user_id):
    try:
        return vk.photos.getAll(owner_id=user_id, extended=1)
    except ApiError:
        return {}


def get_photo_comments(vk, user_id, user_photos):
    if not user_photos:
        return []

    data = []
    for photo in user_photos['items']:
        try:
            comments = vk.photos.getComments(owner_id=user_id, photo_id=photo['id'], need_likes=1)
        except ApiError:
            comments = []
        data.append(comments)
    return data


def add_user_photos(link_data, user_photos, photo_comments):
    if user_photos:
        for i in range(len(user_photos['items'])):
            user_photos['items'][i]['comments'] = photo_comments[i]

    if 'counters' in link_data:
        link_data['counters']['photos'] = user_photos
    else:
        link_data['counters'] = {'photos': user_photos}
    return link_data


def get_user_posts(vk, user_id):
    try:
        return vk.wall.get(owner_id=user_id, extended=1)
    except ApiError:
        return {}


def get_post_comments(vk, user_id, user_posts):
    if not user_posts:
        return []

    data = []
    for post in user_posts['items']:
        try:
            comments = vk.wall.getComments(owner_id=user_id, post_id=post['id'], need_likes=1)
        except ApiError:
            comments = []
        data.append(comments)
    return data


def add_user_posts(link_data, user_posts, post_comments):
    if user_posts:
        for i in range(len(user_posts['items'])):
            user_posts['items'][i]['comments'] = post_comments[i]

    if 'counters' in link_data:
        link_data['counters']['posts'] = user_posts
    else:
        link_data['counters'] = {'posts': user_posts}
    return link_data


def get_user_data(vk, link_data):
    # Profile
    profile_data = get_profile_desc(vk, link_data['id'])
    link_data = add_profile_desc(link_data, profile_data)
    # Friends
    user_friends = get_user_friends(vk, link_data['id'])
    link_data = add_user_friends(link_data, user_friends)
    # Followers
    user_followers = get_user_followers(vk, link_data['id'])
    link_data = add_user_followers(link_data, user_followers)
    # Gifts
    user_gifts = get_user_gifts(vk, link_data['id'])
    link_data = add_user_gifts(link_data, user_gifts)
    # Groups
    user_groups = get_user_groups(vk, link_data['id'])
    group_desc = get_group_desc(vk, user_groups)
    link_data = add_user_groups(link_data, user_groups, group_desc)
    # Videos
    user_videos = get_user_videos(vk, link_data['id'])
    link_data = add_user_videos(link_data, user_videos)
    # Photos
    user_photos = get_user_photos(vk, link_data['id'])
    photo_comments = get_photo_comments(vk, link_data['id'], user_photos)
    link_data = add_user_photos(link_data, user_photos, photo_comments)
    # Wall
    user_posts = get_user_posts(vk, link_data['id'])
    post_comments = get_post_comments(vk, link_data['id'], user_posts)
    link_data = add_user_posts(link_data, user_posts, post_comments)

    return link_data
