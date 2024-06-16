import sys
import os

# Указываем путь к каталогу вашего проекта
path = '/home/manticore1111/FastApi'
if path not in sys.path:
    sys.path.append(path)

# Установите переменную окружения для конфигурации вашего приложения
os.environ['PYTHONPATH'] = path

# Импортируйте ваше приложение
from main import app  # Убедитесь, что 'main' — это файл, содержащий ваше FastAPI приложение

# Это указывается как application в веб-интерфейсе PythonAnywhere
application = app
