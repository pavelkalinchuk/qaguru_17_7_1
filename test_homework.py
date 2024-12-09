import csv
import io
from zipfile import ZipFile
from openpyxl import load_workbook
from pypdf import PdfReader


# Читаем csv-файл расположенный в архиве и выполняем проверки содержимого
def test_csv(make_zip):
    with ZipFile("resources/archive.zip", 'r') as zfile_csv:
        # Открываем CSV-файл внутри архива
        with zfile_csv.open("../tmp/test.csv") as csv_file:
            # Создаем объект CSV-ридера
            csv_reader = csv.reader(io.TextIOWrapper(csv_file, encoding='utf-8'))
            # Читаем строки из CSV-файла и записываем в список
            csv_content = []
            for row in csv_reader:
                csv_content.append(row)
            assert csv_content, "Файл пустой!"
            assert len(csv_content) == 3, "Количество строк не соответствует ожидаемому"
            assert "Фамилия; Имя; Отчество; Пол; Возраст" in csv_content[0]


# Читаем xlsx-файл расположенный в архиве и выполняем проверки содержимого.
def test_xlsx():
    with ZipFile("resources/archive.zip", 'r') as zfile_xlsx:
        # Открываем xlsx-файл внутри архива
        with zfile_xlsx.open("../tmp/book.xlsx") as xlsx_file:
            file_content = io.BytesIO(xlsx_file.read())
            workbook = load_workbook(file_content)
            sheet = workbook.active
            assert sheet['A1'].value == "Ячейка А1"
            assert sheet['C10'].value == "Ячейка С10"


def test_pdf():
    with ZipFile("resources/archive.zip", 'r') as zfile_pdf:
        # Открываем pdf-файл внутри архива
        with zfile_pdf.open("../tmp/ranger.pdf") as pdf_file:
            reader = PdfReader(pdf_file)
            assert "Доброго дня господа" in reader.pages[0].extract_text()
            assert len(reader.pages) == 9
