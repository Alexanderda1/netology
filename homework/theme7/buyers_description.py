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


def get_verb_form(sex):
    if sex.lower() == 'male':
        return 'совершил'
    elif sex.lower() == 'female':
        return 'совершила'
    else:
        return 'совершило'


def translate_device(device_type):
    device_map = {
        'mobile': 'мобильного',
        'tablet': 'планшетного',
        'desktop': 'стационарного',
        'laptop': 'портативного'
    }
    return device_map.get(device_type.lower(), device_type)


def format_description(customer_data):
    name = customer_data['name']
    sex_description = translate_sex(customer_data['sex'])
    age = customer_data['age']
    verb = get_verb_form(customer_data['sex'])
    bill = customer_data['bill']
    device = translate_device(customer_data['device_type'])
    browser = customer_data['browser']
    region = customer_data['region']

    description = (
        f"Пользователь {name} {sex_description} пола, {age} лет "
        f"{verb} покупку на {bill} у.е. с {device} браузера {browser}. "
        f"Регион, из которого совершалась покупка: {region}."
    )

    return description


