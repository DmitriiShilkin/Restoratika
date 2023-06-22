from datetime import datetime

from django.urls import reverse
# импорт стандартных моделей
from django.db import models
# импорт валидаторов
from django.core.validators import MinValueValidator

# возможные значения поля position в таблице Staff
STAFF = [
    ('DIR', 'Директор'),
    ('ADM', 'Администратор'),
    ('MNR', 'Менеджер'),
    ('CAS', 'Кассир'),
    ('CUR', 'Курьер'),
]


# Модель таблицы с разделами меню
class MenuSection(models.Model):
    # поля таблицы, поле id создается автоматически, его указывать не нужно
    # название раздела
    name = models.CharField(max_length=32, unique=True)
    # описание
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name.title()


# Модель таблицы с данными о персонале
class Staff(models.Model):
    # поля таблицы, поле id создается автоматически, его указывать не нужно
    # Фамилия, Имя, Отчество
    full_name = models.CharField(max_length=64)
    # должность
    position = models.CharField(max_length=3, choices=STAFF, default='CAS')
    # номер трудового договора
    contract = models.CharField(max_length=32, unique=True)


# Модель таблицы с данными о блюдах
class Dish(models.Model):
    # поля таблицы, поле id создается автоматически, его указывать не нужно
    # название блюда
    name = models.CharField(max_length=128, unique=True)
    # описание блюда
    description = models.CharField(max_length=255, blank=True, null=True)
    # цена блюда
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    # находится в стоп-листе?
    stop_list = models.BooleanField(default=False)
    # внешний ключ на таблицу с разделами меню
    menu_section = models.ForeignKey(MenuSection, on_delete=models.CASCADE)


# Модель таблицы с данными о заказах
class Order(models.Model):
    # поля таблицы, поле id создается автоматически, его указывать не нужно
    # время поступления заказа
    time_in = models.DateTimeField(auto_now_add=True)
    # время готовности заказа
    time_out = models.DateTimeField(blank=True, null=True)
    # общая стоимость заказа
    cost = models.FloatField(validators=[MinValueValidator(0.0)])
    # на вынос?
    take_away = models.BooleanField(default=False)
    # завершен?
    complete = models.BooleanField(default=False)
    # внешний ключ на исполнителя заказа
    staff = models.ForeignKey(MenuSection, on_delete=models.CASCADE)
    dish = models.ManyToManyField(Dish, through='DishOrder', related_name='order')

    # функция reverse позволяет нам указывать не путь вида /booking/…, а название пути, которое мы задали
    # в файле urls.py для аргумента name
    def get_absolute_url(self):
        return reverse('order_detail', args=[str(self.pk)])

    # фиксируем время завершения заказа
    def finish_order(self):
        self.time_out = datetime.now()
        self.complete = True
        self.save()

    # возвращает время выполнения заказа в минутах
    def get_duration(self):
        if self.complete:
            return (self.time_out - self.time_in).total_seconds() // 60
        else:
            return (datetime.now() - self.time_in).total_seconds() // 60


# Модель для вспомогательной таблицы Блюда-Заказы
class DishOrder(models.Model):
    # поля таблицы, поле id создается автоматически, его указывать не нужно
    # количество блюд в заказе
    amount = models.IntegerField(validators=[MinValueValidator(0)], default=1)
    # внешний ключ на таблицу блюд
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    # внешний ключ на таблицу заказов
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    # считаем стоимость блюда в заказе
    def dish_cost(self):
        dish_price = self.dish.price
        return dish_price * self.amount
