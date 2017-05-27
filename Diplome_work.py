import requests
import json
import time


# Формироваине параметров для запросов.
def get_params():
    # authorize_url = 'https://oauth.vk.com/authorize'
    version = '5.64'
    # app_id = 5947968
    access_token = ""  # token
    params = {'access_token': access_token,
              'v': version}
    return params


# Показ процесса работы
def print_process():
    print('.')


# Отправка запроса
def make_request(url, params):
    while True:
        print_process()
        try:
            response_list = requests.get(url, params).json()
            _ = response_list['response']
            break
        except KeyError:  # при возврате неверного ответа на запрос: ожидание 1с и отравка повторного запроса
            time.sleep(1)
            # print('Except, a new try.')
    return response_list


# Является ли пользователь из списка друзей подписчиком группы
def get_users_is_members(params, friends_list):
    final_list = []
    x = 0
    y = 250
    all_params = params['user_ids'].split(', ')
    while all_params[x:y]:
        params['user_ids'] = str(friends_list['response']['items'][x:y])[1:-1]
        x = y
        y += 250
        members = make_request('https://api.vk.com/method/groups.isMember', params)
        for member in members['response']:
            final_list.append(member)
    return final_list


# Является ли пользователь из списка друзей подписчиком группы
def get_group_without_user_friends(params, groups_list, friends_list):
    user_is_along = []
    for group in groups_list['response']['items']:
        params['group_id'] = group['id']
        params['user_ids'] = str(friends_list['response']['items'])[1:-1]
        members_group = get_users_is_members(params, friends_list)
        flag = False
        for member in members_group:
            if member['member'] == 1:
                flag = True
                break
        if not flag:
            params['group_id'] = group['id']
            str_dict = {'name': group['name'], 'gid': group['id'],
                        'members_count': make_request('https://api.vk.com/method/groups.getMembers',
                                                      params)['response']['count']}
            user_is_along.append(str_dict)
    return user_is_along


# Сохранение файла в json
def save_json(data):
    with open('list.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        print(len(data))


def main():
    params = get_params()
    params['user_id'] = 5030613
    friends_list = make_request('https://api.vk.com/method/friends.get', params)
    params['extended'] = 1
    groups_list = make_request('https://api.vk.com/method/groups.get', params)
    data = get_group_without_user_friends(params, groups_list, friends_list)
    save_json(data)

if __name__ == '__main__':
    main()
