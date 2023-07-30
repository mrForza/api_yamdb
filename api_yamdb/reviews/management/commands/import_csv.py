import csv
import os
from typing import List

from django.core.management.base import BaseCommand, CommandError
from django.shortcuts import get_object_or_404
from django.db import models
from reviews import models

from api_yamdb.settings import BASE_DIR


class Command(BaseCommand):
    '''Выполняет загрузку данных из csv файлов в БД'''
    help = 'Load project data for current api project'

    CSV_FILES = [
        ['users.csv', models.User],
        ['category.csv', models.Category],
        ['genre.csv', models.Genre],
        ['titles.csv', models.Title],
        ['review.csv', models.Review],
        ['comments.csv', models.Comment],
    ]

    FOREIGN_FIELD_NAMES = {
        'review': models.Review,
        'author': models.User,
        'title': models.Title,
        'genre': models.Genre,
        'category': models.Category,
    }

    def add_arguments(self, parser):
        """Регистрация параметра, который позволяет задать альтернативный путь
        к директории с csv файлами"""
        parser.add_argument('data_dir', nargs='?', type=str)

    def handle(self, *args, **options):
        """Метод, выполняющий основную логику по загрузке данных.
        Точка входа выполнения команды"""
        data_dir = options['data_dir']
        if not data_dir:
            data_dir = os.path.join(BASE_DIR, 'static', 'data')
        for csv_file, model in self.CSV_FILES:
            absolute_path = os.path.join(data_dir, csv_file)
            print(f'Load {absolute_path}')
            self.process_file(absolute_path, model)
        self.add_genres_titles(os.path.join(data_dir, 'genre_title.csv'))

    def process_file(self, csv_file_path: str, model):
        """Открывает csv файл на чтение и построчно читает данные"""
        model_fields = [f.name for f in model._meta.fields]
        with open(csv_file_path, 'rt', encoding="utf8") as f:
            # Открываем csv файл как таблицу Exel
            csv_reader = csv.reader(f, dialect='excel')
            # Читаем первую строку как список колонок
            csv_field_names = next(csv_reader)
            # Корректируем имена колонок для последующей загрузки
            self.adjust_csv_field_names(csv_field_names)
            # Проверяем наличие всех колонок/полей в модели
            self.validate_field_names(csv_field_names, model_fields)
            # Вычитываем построчно все данные из файла
            for row in csv_reader:
                self.save_row_to_db(model, row, csv_field_names)

    def adjust_csv_field_names(self, csv_field_names: List[str]):
        """Конвертирует имена колонок из csv файла в название полей в модели"""
        for i, _ in enumerate(csv_field_names):
            csv_field_names[i] = csv_field_names[i].lower()
            csv_field_names[i] = csv_field_names[i].replace('_id', '')

    def validate_field_names(
        self, csv_field_names: List[str],
        model_field_names: List[str]
    ):
        """Проверяет наличие колонок из csv файла в списке полей модели."""
        for csv_field_name in csv_field_names:
            if csv_field_name not in model_field_names:
                raise CommandError(
                    f"{csv_field_name} field doesn't exist "
                    "in {Model} Model"
                )

    def save_row_to_db(self, target_model, row, field_names):
        """Переносит данные из csv строки в модель,
        а также разрешает ссылки по внешним ключам."""
        try:
            new_records = target_model()
            for i, field_value in enumerate(row):
                field_name = field_names[i]
                if field_name in self.FOREIGN_FIELD_NAMES.keys():
                    foreign_model = self.FOREIGN_FIELD_NAMES[field_names[i]]
                    field_value = get_object_or_404(
                        foreign_model,
                        id=field_value
                    )
                setattr(new_records, field_name, field_value)
            new_records.save()
        except Exception as e:
            raise CommandError(f'Failed to save row {row} to database.', e)

    def add_genres_titles(self, file_path: str):
        """Связывает данные жанров с произведениями."""
        with open(file_path, 'rt', encoding="utf8") as f:
            dict_reader = csv.DictReader(f)
            for row in dict_reader:
                try:
                    title = get_object_or_404(
                        models.Title,
                        id=int(row['title_id'])
                    )
                    genre = get_object_or_404(
                        models.Genre,
                        id=int(row['genre_id'])
                    )
                    title.genre.add(genre)
                    title.save()
                except Exception as error:
                    raise CommandError(
                        f'Failed add genre to title by using row: {row}',
                        error
                    )
