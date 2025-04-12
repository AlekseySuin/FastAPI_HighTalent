# Степень реализации проекта:
:white_check_mark: Использовать FastAPI как основной фреймворк.</br>
:white_check_mark: Работа с БД через SQLAlchemy или SQLModel.</br>
:white_check_mark: Использовать PostgreSQL.</br>
:white_check_mark: Использовать Alembic для миграций.</br>
:white_check_mark: Приложение должно быть обернуто в Docker.</br>
:white_check_mark: Использовать docker-compose для запуска всех компонентов.</br>
:white_check_mark: Структура проекта должна быть модульной: routers/, models/, schemas/, services/, и т.п.</br>
:white_check_mark: Код должен быть легко расширяемым.</br>
:negative_squared_cross_mark: Приветствуется: логгирование, покрытие базовых сценариев тестами (на pytest).</br>

# О чем проект?
REST API сервис для бронирование столиков в ресторане. Сервис позволяет создавать, просматривать и удалять брони.

# Как запустить проект?
## 1. Клонируйте проект

git clone (https://github.com/AlekseySuin/DjangoStripe)
cd ваш-репозиторий


## 2. Запуск с помощью Docker

а) Убедитесь, что Docker установлен
Убедитесь, что у вас установлены Docker и Docker Compose. Если нет, установите их:

[Установка Docker](https://docs.docker.com/get-started/get-docker/)

[Установка Docker Compose](https://docs.docker.com/compose/install/)

б) Сборка и запуск контейнеров
```
docker-compose up --build
```
После завершения сборки ваш проект будет доступен по адресу:
```
http://localhost:8000/
```
