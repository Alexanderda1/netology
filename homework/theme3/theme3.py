from datetime import datetime


def parse_date(date_str):
    formats = [
        "%A, %B %d, %Y",  # The Moscow Times
        "%A, %d.%m.%y",  # The Guardian
        "%A, %d %B %Y"  # Daily News
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def main():
    while True:
        user_input = input("Введите дату (или 'quit' для выхода): ").strip()
        if user_input.lower() == 'quit':
            break

        parsed_date = parse_date(user_input)
        if parsed_date:
            print(parsed_date)
        else:
            print("Неверный формат даты. Попробуйте снова.")


if __name__ == "__main__":
    main()