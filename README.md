
Настройка окружения (в папке backend):
python -m venv venv

Активация (Linux/macOS): source venv/bin/activate
Активация (Windows): .\venv\Scripts\Activate.ps1

База данных и запуск:

python manage.py migrate
python manage.py createsuperuser  # создать админа
python manage.py runserver