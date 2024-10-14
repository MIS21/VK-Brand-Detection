import requests
import os
import json


def get_photos(user_id, access_token, count=5):
    url = 'https://api.vk.com/method/photos.get'
    params = {
        'owner_id': user_id,
        'album_id': 'profile',  # Фотографии профиля
        'extended': '1',
        'count': count,
        'access_token': access_token,
        'v': '5.131'
    }
    response = requests.get(url, params=params)
    return response.json()


def download_photo(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Изображение сохранено как {filename}")
    else:
        print(f"Не удалось загрузить {url}")


def start_downloading(ids, access_token, count=5):

    for user_id in ids:
        # Получаем информацию о фотографиях
        photos_data = get_photos(user_id, access_token, count)

        if 'response' in photos_data and 'items' in photos_data['response']:
            if not os.path.exists('vk_photos'):
                os.makedirs('vk_photos')

            for i, photo in enumerate(photos_data['response']['items']):
                # Выбираем самый большой размер фото
                max_size_photo = max(photo['sizes'], key=lambda x: x['width'])
                photo_url = max_size_photo['url']
                # Формируем имя файла
                file_extension = photo_url.split('.')[-1].split('?')[0]
                filename = f'vk_photos/{user_id}photo_{i + 1}.{file_extension}'
                download_photo(photo_url, filename)
        else:
            print("Не удалось загрузить фото")


