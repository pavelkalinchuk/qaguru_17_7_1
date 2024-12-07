import csv
import io
import os
from zipfile import ZipFile

current_directory_path = os.path.dirname(__file__)
resources_directory_path = os.path.join(current_directory_path, "resources")
tmp_directory_path = os.path.join(current_directory_path, "tmp")
archive_file = os.path.join(resources_directory_path, "archive.zip")

with ZipFile(archive_file, 'w') as zfile:
    # Проходим по всем файлам в директории
    for root, dirs, files in os.walk(tmp_directory_path):
        for file in files:
            # Полный путь к файлу
            file_path = os.path.join(root, file)
            # # Добавляем файл в архив
            zfile.write(file_path, os.path.relpath(file_path, resources_directory_path))
    print(zfile.namelist())


# Читаем csv-файл расположенный в архиве
def test_csv():
    with ZipFile(archive_file, 'r') as zfile:
        # Открываем CSV-файл внутри архива
        with zfile.open("../tmp/test.csv") as csv_file:
            # Создаем объект CSV-ридера
            csv_reader = csv.reader(io.TextIOWrapper(csv_file, encoding='utf-8'))
            # Читаем строки из CSV-файла и записываем в список
            csv_content = []
            for row in csv_reader:
                csv_content.append(row)
            assert csv_content, "Файл пустой!"
            assert len(csv_content) == 3, "Количество строк не соответствует ожидаемому"
            assert "Фамилия; Имя; Отчество; Пол; Возраст" in csv_content[0]
