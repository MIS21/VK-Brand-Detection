import requests
import random


def search_users(params):
    url = 'https://api.vk.com/method/users.search'
    response = requests.get(url, params=params)
    return response.json()


def get_random_users(n, params):
    users = []
    response = search_users(params)

    if 'response' in response and 'items' in response['response']:
        all_users = [user['id'] for user in response['response']['items'] if
                     not user['is_closed'] or user['can_access_closed']]

        # Если общее количество пользователей меньше, чем n, вернем всех
        if len(all_users) <= n:
            return all_users

        # Иначе выбираем n случайных пользователей
        return random.sample(all_users, n)
    else:
        print("Ошибка при поиске пользователей или неожиданный формат ответа.")
        return []


def start_search(search_params):
    random_users = get_random_users(10, search_params)
    for user in random_users:
        print(f"ID: {user['id']}, Name: {user.get('first_name', 'Unknown')} {user.get('last_name', 'Unknown')}")


