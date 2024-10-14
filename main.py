from fastapi import FastAPI, Query
from typing import List, Dict, Any
import uvicorn
from ultralytics import YOLO
from collections import defaultdict
from user_search import get_random_users
from vk_download import start_downloading

app = FastAPI()

# Загружаем модель YOLO один раз при запуске приложения
model = YOLO('best.pt')


@app.get("/search")
async def search_users(
        sex: int = Query(..., description="1 for Female, 2 for Male"),
        age_from: int = Query(..., description="Minimum age"),
        age_to: int = Query(..., description="Maximum age"),
        city: int = Query(..., description="City ID, e.g., 1 for Moscow"),
        count: int = Query(10, description="Number of users to search for"),
        photos: int = Query(5, description="Number of photos to download per user"),
        access_token: str = Query(..., description="VK API access token")
):
    # Формируем параметры для поиска
    search_params = {
        'count': 1000,  # VK API limit, you might want to handle pagination if more are needed
        'sex': sex,
        'age_from': age_from,
        'age_to': age_to,
        'city': city,
        'has_photo': 1,  # Only users with photos
        'fields': 'is_closed, can_access_closed',
        'access_token': access_token,
        'v': '5.131'
    }

    # Получаем случайных пользователей
    users = get_random_users(count, search_params)

    # Скачиваем фотографии пользователей
    start_downloading(users, access_token, photos)

    brand_count = defaultdict(int)

    # Выполняем предсказание на изображениях
    results = model('vk_photos', verbose=False)

    # Обрабатываем результаты и считаем бренды
    for result in results:
        brands_detected = set()
        for box in result.boxes:
            brands_detected.add(result.names[int(box.cls)])
        for brand in brands_detected:
            brand_count[brand] += 1

    return {"brands_detected": dict(brand_count)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
