# api_final_yatube
**Yatube** — это платформа для блогов. Реализованы следующие возможности:
- Добавление произведений, категорий и жанров (только администратор)
- Аутентифицированные пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от 1-до 10
- Из пользовательских оценок формируется рейтинг. На одно произведение пользователь может оставить только один отзыв.
- Аутентифицированные пользователи могут оставлять комментарии к отзывам.
  
## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:VK73-dev/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Загрузить данные из csv файлов в БД:
```
python manage.py import_csv
```

Запустить проект:

```
python manage.py runserver
```

## Примеры запросов к API:
Получение публикаций: [GET /api/v1/posts/](http://127.0.0.1:8000/api/v1/posts/)

Получение публикации: [GET /api/v1/posts/{id}/](http://127.0.0.1:8000/api/v1/posts/{id}/)

Создание публикации: [POST /api/v1/posts/](http://127.0.0.1:8000/api/v1/posts/)
```
{
"text": "string",
"image": "string",
"group": 0
}
```

Получение комментариев: [GET /api/v1/posts/{post_id}/comments/](http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/)

Получение комментария: [GET /api/v1/posts/{post_id}/comments/{id}/](http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/{id}/)

Создание комментария: [POST /api/v1/posts/{post_id}/comments/](http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/)
```
{
"text": "string"
}
```

Список сообществ: [GET /api/v1/groups/](http://127.0.0.1:8000/api/v1/groups/)

Информация о сообществе: [GET /api/v1/groups/{id}/](http://127.0.0.1:8000/api/v1/groups/{id}/)

Подписки: [GET /api/v1/follow/](http://127.0.0.1:8000/api/v1/follow/)

Подписка: [POST /api/v1/follow/](http://127.0.0.1:8000/api/v1/follow/)
```
{
"following": "string"
}
```
## Использованные технологии:
* Django ORM
* REST API
* DRF

## Авторы:
- **Роман Громов**
- **[Viacheslav Korablev](https://github.com/VK73-dev/)**
- **Любовь Скутина**

