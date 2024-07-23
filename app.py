from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse
import codecs
import json
import uuid

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')  # Разрешаем доступ с любого домена
        self.end_headers()
        tasks = read_tasks()
        self.wfile.write(tasks.encode('utf-8'))

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')  # Разрешаем доступ с любого домена
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')  # Разрешаем методы GET, POST, OPTIONS
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')  # Разрешаем заголовок Content-Type
        self.end_headers()

        if self.headers['Content-Length']:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            decoded_data = urllib.parse.unquote(post_data.decode('utf-8'))
            # print(decoded_data)
            # json_data = convert_str_to_json(decoded_data)
            json_data = json.loads(decoded_data)
            print(f"Получен запрос с параметрами {json_data}")
            save_task(json_data)

            response = f"{json.dumps(json_data)}"
            print(f"Отправляю ответ {response}")
            self.wfile.write(response.encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')  # Разрешаем доступ с любого домена
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')  # Разрешаем методы GET, POST, OPTIONS
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')  # Разрешаем заголовок Content-Type
        self.end_headers()

'''
Сохраняет задачу в файл
task: str. Задание, которое надо записать в файл
'''
def save_task(task):
  id = uuid.uuid1()
  current_task = task.get('task')

  file = codecs.open(r"D:\Informatik\Practik\notes\tasks.json", "r+", "utf-8")
  file_json = json.load(file)
  file_json['tasks'].append({"id": str(id), "task": str(current_task)})
  file.write('')
  file.close()
  
  file = codecs.open(r"D:\Informatik\Practik\notes\tasks.json", "w", "utf-8")
  file.write(json.dumps(file_json, ensure_ascii=False))
  file.close()
  print(f"Coхраняю в файл параметры {task}")


def convert_str_to_json(str):
  data = {}
  for item in str.split(';'):
    key, value = item.split('=')
    data[key] = value
  return data

def read_tasks():
  f = codecs.open(r"D:\Informatik\Practik\notes\tasks.json", "rb", "utf-8")
  tasks = f.read()
  f.close() 

  return tasks

server_address = ('', 8000)
httpd = HTTPServer(server_address, MyHandler)

print("Starting server on port 8000...")
httpd.serve_forever()