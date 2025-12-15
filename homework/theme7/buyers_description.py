def read_csv_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None