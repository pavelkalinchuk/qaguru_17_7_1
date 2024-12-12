import pytest
import os
from zipfile import ZipFile


@pytest.fixture(scope="session", autouse=True)
# Создаём архив 'archive.zip' с файлами из каталога 'tmp' и помещаем в каталог 'resources'
def make_zip():
    if not os.path.exists("resources"):  # Проверям, если данной папки нет, то создаём её
        os.mkdir("resources")
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

    yield

    # Удаляем созданный ZIP-архив
    if os.path.exists("resources/archive.zip"):
        if os.path.isfile("resources/archive.zip"):
            os.remove("resources/archive.zip")
