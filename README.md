# RashTest
Данный проект является реализацией интеграции приложения Django Payment App и платежной системы  Stripe.

# 1. Клонирование репозитория с GitHub.
* Python должен быть уже установлен. 
В терминале через команду  
```
git clone https://github.com/ZloyBaklan/RashTest.git
```
скопирйте репозиторий на свой компьютер.

* Правильно будет установить виртуальное окружение в директории проекта:
``` 
python -m venv venv 
```
Далее необходимо его активировать:
```
source venv/Scripts/activate 
```
Затем используйте pip для установки зависимостей:
```
pip install -r requirements.txt 
```

# 2. Подготовка(переменные окружения .env).
В директории payment_service необходимо создать .env файл в нем будут размещены:
```
DJANGO_SECRET_KEY = 'django-insecure--4!$a4k3a5riquz(vam8+*l378^#3kvunyvo5=-hg&7c!s7kf('
DEBUG = False
STRIPE_PUBLIC_KEY = 'Ваш публичный stripe ключ'
STRIPE_SECRET_KEY = 'Ваш секретный stripe ключ'
```
Stripe-ключи необходимо получить с [Stripe](https://stripe.com/),
после регистрации на сайте, в разделе [stripe/test/dashboard/](https://dashboard.stripe.com/test/dashboard)

# 3. Запуск проекта, создание админки.
Если вы еще не в директории payment_service, самое время через команду
```
cd 'payment_service' 
```
перейти в нужную директорию, не забудьте сделать и применить миграции:
```
python manage.py makemigrations
```
```
python manage.py migrate
```
Иногда миграции не "встают", поэтому добавьте к makemigrations items, затем повторите для orders, далее создаем админа:
```
python manage.py createsuperuser
```
сможете создать админа нашего приложения(с паролем и мейлом).

Далее с помощью команды 
```
python manage.py runserver 
```
вы сможете запустить проект на своей локальной машине(у меня к сожалению нет возможности размещения данного репозитория на удаленном сервере).

Затем перейдите по ссылке [Admin](http://127.0.0.1:8000/admin/) и у вас появится возможность зайти "внутрь" нашего проекта.

# 4. Подготовка к работе, промокоды, скидки и налоги.
Через интерфейс админки, создайте модели Discount, PromoCode и Tax, поскольку данные модели доступны для создания только через интерфейс админки(что логично, ведь это же "скидки и налоги") :)

Далее вы можете перейте на [Сайт](http://127.0.0.1:8000/), вы будете находиться на нем под логином админа.

# 5. Регистрация, объекты платежа, заказы.

Если вдруг вам захочется создать тестовый аккаунт, в шапке сайта есть кнопка "Регистрация", далее после заполнения формы вы сможете войти на сайт уже под "обычным" пользователем без staff статуса.

* Продукт(Item)
Я не стал ограничивать возможность создания продукта требованием авторизации, любой может создать продукт.
Так же любой может нажав кнопку "Buy Now", оказаться на странице товара, где заполнив email форму для связи и нажав checkout перенесется на stripesession, где уже неообходимо будет произвести оплату.

* !ВАЖНО(Цена на stripe все равно в долларах, так как метод оплаты через PaymentIntent "в разработке" (привязка к stripe key pair через данный метод). Однако, если при создании товара вы выберете рубли, то цена пересчитается по актуальному курсу ЦБРФ в доллары автоматически.)

* Заказ(Order)
При авторизации вам станет доступен "Заказ" и появится возможность добавления продукта в заказ с нужным количеством(выбирается через интерфейс на сайте). Вы можете добавлять существующие позиции в Заказ и совершить оплату через вкладку Order кнопка: Создать интент

Вас перенесет на страницу оплаты, где можно будет использовать один из созданных промокодов, так же будет учтен "налог" и будет выставлен счет на итоговую сумму.

# 6. Docker.

Планируется возможность развернуть приложение через docker с помощью команды 
```
docker-compose up -d --build
```


#### P.S. Данное задание было весьма интересное, буду ждать обратной связи, спасибо.
