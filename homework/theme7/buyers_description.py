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


def parse_csv_line(line):
    parts = line.strip().split(',')

    if len(parts) < 7:
        return None

    customer_data = {
        'name': parts[0],
        'device_type': parts[1],
        'browser': parts[2],
        'sex': parts[3],
        'age': parts[4],
        'bill': parts[5],
        'region': parts[6]
    }

    return customer_data


def translate_sex(sex):
    if sex.lower() == 'male':
        return 'мужского'
    elif sex.lower() == 'female':
        return 'женского'
    else:
        return 'неопределенного'


