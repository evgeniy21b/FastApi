import sys
import os

# Указываем путь к каталогу вашего проекта
path = '/home/manticore1111/FastApi'
if path not in sys.path:
    sys.path.append(path)

# Установка переменной окружения для PythonAnywhere
os.environ['PYTHONPATH'] = path

# Импорт вашего приложения FastAPI
from main import app

# Убедитесь, что приложение импортировано правильно
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
