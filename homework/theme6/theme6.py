import csv
import json


def load_purchases(filename):
    """Загружает данные о покупках из JSON файла."""
    purchases = {}

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                try:
                    data = json.loads(line)
                    user_id = data.get('user_id', '').strip()
                    category = data.get('category', '').strip()

                    # Пропускаем заголовок
                    if user_id and user_id != 'user_id' and category:
                        purchases[user_id] = category
                except json.JSONDecodeError:
                    continue

    return purchases


def create_funnel(visit_file, purchases, output_file):
    """Создает файл funnel.csv с визитами, в которых были покупки."""
    with open(visit_file, 'r', encoding='utf-8') as infile, \
            open(output_file, 'w', encoding='utf-8', newline='') as outfile:

        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=['user_id', 'source', 'category'])
        writer.writeheader()

        for row in reader:
            user_id = row['user_id'].strip()

            # Если есть покупка - записываем в funnel
            if user_id in purchases:
                writer.writerow({
                    'user_id': user_id,
                    'source': row['source'],
                    'category': purchases[user_id]
                })


def main():
    """Основная функция программы."""
    # Загружаем данные о покупках
    print("Загрузка данных о покупках...")
    purchases = load_purchases('purchase_log.txt')
    print(f"Загружено покупок: {len(purchases)}")

    # Создаем файл с воронкой
    print("Обработка визитов...")
    create_funnel('visit_log__1_.csv', purchases, 'funnel.csv')

    print("Готово! Результат записан в funnel.csv")


if __name__ == '__main__':
    main()