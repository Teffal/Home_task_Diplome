import requests
import json
import time


class UserVk:
    version = '5.64'
    access_token = ""  # token
    params = {'access_token': access_token, 'v': version}

    # ничальная иничиализация
    def __init__(self, user_id):
        self.params['user_id'] = user_id
        self.params['extended'] = 1

        # получение данных пользователя один раз при инициализаци экземпляра
        def get_data(url):
            while True:
                self.print_process()
                try:
                    response_list = requests.get(url, self.params).json()
                    _ = response_list['response']
                    break
                except KeyError:  # при возврате неверного ответа на запрос: ожидание 1с и отравка повторного запроса
                    time.sleep(1)
            return response_list

        self.friends_list = get_data('https://api.vk.com/method/friends.get')
        self.groups_list = get_data('https://api.vk.com/method/groups.get')

    # Показ процесса работы
    def print_process(self):
        print('.')

    # Отправка запроса
    def make_request(self, url):
        while True:
            self.print_process()
            try:
                response_list = requests.get(url, self.params).json()
                _ = response_list['response']
                break
            except KeyError:  # при возврате неверного ответа на запрос: ожидание 1с и отравка повторного запроса
                time.sleep(1)
                # print('Except, a new try.')
        return response_list

    # Является ли пользователь из списка друзей подписчиком группы
    def get_users_is_members(self):
        final_list = []
        x = 0
        y = 250
        all_params = self.params['user_ids'].split(', ')
        while all_params[x:y]:
            self.params['user_ids'] = str(self.friends_list['response']['items'][x:y])[1:-1]
            x = y
            y += 250
            members = self.make_request('https://api.vk.com/method/groups.isMember')
            for member in members['response']:
                final_list.append(member)
        return final_list

    # Является ли пользователь из списка друзей подписчиком группы
    def get_group_without_user_friends(self):
        user_is_along = []
        for group in self.groups_list['response']['items']:
            self.params['group_id'] = group['id']
            self.params['user_ids'] = str(self.friends_list['response']['items'])[1:-1]
            members_group = self.get_users_is_members()
            flag = False
            for member in members_group:
                if member['member'] == 1:
                    flag = True
                    break
            if not flag:
                self.params['group_id'] = group['id']
                str_dict = {'name': group['name'], 'gid': group['id'],
                            'members_count': self.make_request('https://api.vk.com/method/groups.getMembers')
                            ['response']['count']}
                user_is_along.append(str_dict)
        return user_is_along

    # Сохранение файла в json
    def save_json(self):
        with open('list2.json', 'w', encoding='utf-8') as f:
            data = self.get_group_without_user_friends()
            json.dump(data, f, ensure_ascii=False, indent=2)
            print(len(data))

u = UserVk(5030613)
u.save_json()
