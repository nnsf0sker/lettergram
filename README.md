# Lettergram


Это тестовое задание на позицию стажёра-бекендера в Avito, реализованное [@nnsf0sker](github.com/nnsf0sker) в сентябре 2019.
Исходные условия можно посмотреть в файле avito_task.md. Данная реализация получила абсолютно уникальное, и ни на что не
похожее название "Lettergram" (на самом деле, лишь для удобства навигации и красоты структуры проекта).

Для реализации был выбран Python 3.7.0. В качестве API фреймворка был выбрал falcon, а в качестве локальной базы данных 
была выбрана MongoDB.


## Использование

Для любого сценария использования необходимо вначале клонировать репозиторий:

    git clone https://github.com/nnsf0sker/lettergram.git
    cd lettergram
    
И создать виртуальное окружение:

    pip install virtualenv
    virtualenv venv -p python3.7
    source venv/bin/activate

### Запуск всей системы в контейнерах:

    docker-compose build
    docker-compose up

### Разработка:

Установка зависимостей проекта:
    
    pip install -r requirements.txt

Контроль код-стайла:

    flake8 .
