documents = [
    {"type": "passport", "number": "2287 876234", "name": "Василий Гулкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "18086", "name": "Аристарх Павлов"},
    {"type": "passport", "number": "10006", "name": "Аристарх Павлов"}
]

directories = {
    "1": ["2287 876234", "11-2"],
    "2": ["18086"],
    "3": ["10006"]
}

def get_owner_by_document_number(doc_number):
    """Возвращает владельца документа по номеру или сообщение об ошибке."""
    for doc in documents:
        if doc["number"] == doc_number:
            return doc["name"]
    return "владелец не найден"

def main():
    while True:
        command = input("Введите команду: ").strip().lower()
        if command == "q":
            break
        elif command == "p":
            doc_number = input("Введите номер документа: ").strip()
            owner = get_owner_by_document_number(doc_number)
            print(f"Владелец документа: {owner}")
        else:
            print("Неизвестная команда")

if __name__ == "__main__":
    main()