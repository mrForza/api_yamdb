# api_yamdb
**yamdb** — это платформа для публикации произведений. Сервис позволяет добавлять, модифицировать и удалять различные жанры, категории, произведения, отзывы и комментарии к ним по средствам API

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:mrForza/api_yamdb.git
```

```
cd api_yamdb
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

Запустить проект:

```
python manage.py runserver
```

## Примеры некоторых запросов к API:
Получение категорий: [GET /api/v1/categories/](http://127.0.0.1:8000/api/v1/categories/)

Добавление категории: [POST /api/v1/categories/](http://127.0.0.1:8000/api/v1/categories/)

Удаление категории: [DELETE /api/v1/categories/{slug}/](http://127.0.0.1:8000/api/v1/categories/{slug}/)

Получение жанров: [GET /api/v1/genres/](http://127.0.0.1:8000/api/v1/genres/)

Добавление жанра: [POST /api/v1/genres/](http://127.0.0.1:8000/api/v1/genres/)

Удаление жанра: [DELETE /api/v1/genres/{slug}/](http://127.0.0.1:8000/api/v1/genres/{slug}/)

Список сообществ: [GET /api/v1/groups/](http://127.0.0.1:8000/api/v1/groups/)

Информация о сообществе: [GET /api/v1/groups/{id}/](http://127.0.0.1:8000/api/v1/groups/{id}/)

Подписки: [GET /api/v1/follow/](http://127.0.0.1:8000/api/v1/follow/)

Подписка: [POST /api/v1/follow/](http://127.0.0.1:8000/api/v1/follow/)


## Использованные технологии:
* Python
* Django Rest Framework
* Django ORM
* REST API

## Авторы:
**[Viacheslav Korablev](https://github.com/VK73-dev/)**

**[Roman Gromov](https://github.com/mrForza)**

**[Lubov Skutina](https://github.com/LubovSkutina)**

