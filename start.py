import os

print('Установка зависимостей')
os.system('pip install -r requirements.txt')
print('Собираем статику')
os.system('python manage.py collectstatic')
print('Выполняем миграции')
os.system('python manage.py migrate')
print('Запуск сервера')
os.system('python manage.py runserver')
