from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from urllib.parse import urlparse, parse_qs


class TaskManager:

    def __init__(self, filename='tasks.txt'):
        self.filename = filename
        self.tasks = []
        self.next_id = 1
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8-sig') as f:
                    data = json.load(f)
                    self.tasks = data.get('tasks', [])
                    self.next_id = data.get('next_id', 1)
                print(f"Загружено задач: {len(self.tasks)}")
            except Exception as e:
                print(f"Ошибка при загрузке задач: {e}")
                self.tasks = []
                self.next_id = 1

    def save_tasks(self):
        try:
            with open(self.filename, 'w', encoding='utf-8-sig') as f:
                data = {
                    'tasks': self.tasks,
                    'next_id': self.next_id
                }
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка при сохранении задач: {e}")

    def create_task(self, title, priority):
        task = {
            'id': self.next_id,
            'title': title,
            'priority': priority,
            'isDone': False
        }
        self.tasks.append(task)
        self.next_id += 1
        self.save_tasks()
        return task

    def get_all_tasks(self):
        return self.tasks

    def complete_task(self, task_id):
        for task in self.tasks:
            if task['id'] == task_id:
                task['isDone'] = True
                self.save_tasks()
                return True
        return False


class TaskRequestHandler(BaseHTTPRequestHandler):

    task_manager = TaskManager()

    def _set_headers(self, status_code=200, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.end_headers()

    def _send_json_response(self, data, status_code=200):
        self._set_headers(status_code)
        response = json.dumps(data, ensure_ascii=False)
        self.wfile.write(response.encode('utf-8'))

    def _read_request_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            body = self.rfile.read(content_length)
            return json.loads(body.decode('utf-8'))
        return None

    def do_GET(self):
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/tasks':
            tasks = self.task_manager.get_all_tasks()
            self._send_json_response(tasks)
        else:
            self._set_headers(404)
            self.wfile.write(b'Not Found')

    def do_POST(self):
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/tasks':
            try:
                data = self._read_request_body()

                if not data or 'title' not in data or 'priority' not in data:
                    self._send_json_response(
                        {'error': 'Missing required fields: title, priority'},
                        400
                    )
                    return

                title = data['title']
                priority = data['priority']

                if priority not in ['low', 'normal', 'high']:
                    self._send_json_response(
                        {'error': 'Invalid priority. Must be: low, normal, or high'},
                        400
                    )
                    return

                task = self.task_manager.create_task(title, priority)
                self._send_json_response(task, 201)

            except json.JSONDecodeError:
                self._send_json_response({'error': 'Invalid JSON'}, 400)
            except Exception as e:
                self._send_json_response({'error': str(e)}, 500)

        elif parsed_path.path.startswith('/tasks/') and parsed_path.path.endswith('/complete'):
            try:
                parts = parsed_path.path.split('/')
                if len(parts) == 4:
                    task_id = int(parts[2])

                    if self.task_manager.complete_task(task_id):
                        self._set_headers(200)
                        self.wfile.write(b'')
                    else:
                        self._set_headers(404)
                        self.wfile.write(b'Task not found')
                else:
                    self._set_headers(400)
                    self.wfile.write(b'Invalid path')
            except ValueError:
                self._set_headers(400)
                self.wfile.write(b'Invalid task ID')
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(str(e).encode('utf-8'))

        else:
            self._set_headers(404)
            self.wfile.write(b'Not Found')

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")


def run_server(host='localhost', port=8000):
    server_address = (host, port)
    httpd = HTTPServer(server_address, TaskRequestHandler)
    print(f"Сервер запущен на http://{host}:{port}")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nОстановка сервера...")
        httpd.shutdown()


if __name__ == '__main__':
    run_server()