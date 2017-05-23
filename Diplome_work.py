# from tgdm import tqdm
import requests
import json
import time


def get_params():
    AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
    VERSION = '5.64'
    APP_ID = 5947968  # Your app_id here
    access_token = "d13e692be69592b09fd22c77a590dd34e186e6d696daa88d6d981e1b4e296b14acb377e82dcbc81dc0f22"  # token
    params = {'access_token': access_token,
              'v': VERSION,
              }
    return params


def print_process():
    print('.')


def get_user_friends_id(params):
    print_process()
    response = requests.get('https://api.vk.com/method/friends.get', params)
    friends_list = response.json()
    return friends_list


def get_user_groups(params):
    print_process()
    response = requests.get('https://api.vk.com/method/groups.get', params)
    groups_list = response.json()
    return groups_list


def get_group_members_id(params):
    print_process()
    response = requests.get('https://api.vk.com/method/groups.getMembers', params)
    members_list = response.json()
    return members_list


def get_users_is_members(params, friends_list):
    final_list = []
    x = 0
    y = 250
    all_params = params['user_ids'].split(', ')
    while all_params[x:y]:
        params['user_ids'] = str(friends_list['response']['items'][x:y])[1:-1]
        x = y
        y += 250
        # time.sleep(1)
        print_process()
        response = requests.get('https://api.vk.com/method/groups.isMember', params)
        is_members = response.json()
        for member in is_members['response']:
            final_list.append(member)
    return final_list


def get_group_without_user_friends(params, groups_list, friends_list):
    user_is_along = []
    try:
        for group in groups_list['response']['items']:
            params['group_id'] = group['id']
            params['user_ids'] = str(friends_list['response']['items'])[1:-1]
            members_group = get_users_is_members(params, friends_list)
            for member in members_group:
                flag = False
                if member['member'] == 1:
                    flag = True
                    break
            if not flag:
                params['group_id'] = group['id']
                try:
                    str_dict = {'name': group['name'],
                                'gid': group['id'],
                                'members_count': get_group_members_id(params)['response']['count']}
                except:
                    print('except')
                user_is_along.append(str_dict)
            time.sleep(1)
        return user_is_along
    except:
        print('except')


def save_json(data):
    with open('list.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    params = get_params()
    params['user_id'] = 5030613
    friends_list = get_user_friends_id(params)
    params['extended'] = 1
    groups_list = get_user_groups(params)

    data = get_group_without_user_friends(params, groups_list, friends_list)
    save_json(data)

main()
