from django.utils import timezone
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

STATUSES = [
    ('NEW', 'Новый'),
    ('CCK', 'Готовится'),
    ('ASM', 'На сборке'),
    ('DEL', 'Передан в доставку'),
    ('FIN', 'Закрыт'),
]

STICKERS = [
    ('NEW', 'Новинка'),
    ('SAL', 'Скидка'),
    ('TOP', 'Топ продаж'),
    ('ETY', 'Без отметки'),
]


# функция получения пути для сохранения фотографий, чтобы было понятно, к какому товару они относятся
def get_image_path(instance, file):
    return f'pictures/dish-{instance.name}/{file}'


# Модель таблицы с категориями
class MenuSection(models.Model):
    # поля таблицы, поле id создается автоматически, его указывать не нужно
    # название
    name = models.CharField(max_length=32, unique=True)
    # описание
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


# Модель таблицы с данными о персонале
class Staff(models.Model):
    # поля таблицы, поле id создается автоматически, его указывать не нужно
    # Фамилия, Имя, Отчество
    full_name = models.CharField(max_length=64)
    # должность
    position = models.CharField(max_length=3, choices=STAFF, default='CAS')
    # номер трудового договора
    contract = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.full_name


# Модель таблицы со складами
class Store(models.Model):
    # поля таблицы, поле id создается автоматически, его указывать не нужно
    # название
    name = models.CharField(max_length=32, unique=True)
    # описание
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


# Модель таблицы с данными о товарах
class Dish(models.Model):
    # поля таблицы, поле id создается автоматически, его указывать не нужно
    # наименование
    name = models.CharField(max_length=255, unique=True)
    # описание
    description = models.CharField(max_length=255, blank=True)
    # картинка
    picture = models.ImageField(upload_to=get_image_path, blank=True)
    # вес
    # weight = models.IntegerField(validators=[MinValueValidator(0)])
    # цена до скидки
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    # цена после скидки
    price_discount = models.FloatField(validators=[MinValueValidator(0.0)], editable=False)
    # себестоимость
    # cost = models.FloatField(validators=[MinValueValidator(0.0)])
    # наценка
    # margin = models.FloatField(validators=[MinValueValidator(0.0)], editable=False)
    # скидка в процентах
    discount = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    # скидка в рублях
    discount_rub = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    # надбавка в процентах
    increment = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    # надбавка в рублях
    increment_rub = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    # наклейка
    sticker = models.CharField(max_length=3, choices=STICKERS, default='NEW')
    # отображается в POS?
    is_in_POS = models.BooleanField(default=True)
    # отображается на сайте доставки?
    is_in_delivery = models.BooleanField(default=False)
    # находится в стоп-листе?
    is_in_stop_list = models.BooleanField(default=False)
    # отмечен для групповых операций?
    is_checked = models.BooleanField(default=False)
    # количество
    quantity = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    # внешний ключ на таблицу с категориями
    menu_section = models.ManyToManyField(MenuSection, related_name='dish')
    # внешний ключ на таблицу со складами
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    @property
    def picture_url(self):
        if self.picture and hasattr(self.picture, 'url'):
            return self.picture.url

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.price_discount = self.price * (1 - self.discount / 100 + self.increment / 100) - self.discount_rub \
                              + self.increment_rub
        if self.price_discount < 0:
            self.price_discount = 0
        # try:
        #     self.margin = (self.price_discount - self.cost) / self.cost * 100
        # except ZeroDivisionError:
        #     self.margin = 0

        super().save(*args, **kwargs)


# Модель таблицы с данными о заказах
class Order(models.Model):
    # поля таблицы, поле id создается автоматически, его указывать не нужно
    # время поступления
    time_in = models.DateTimeField(default=timezone.now, editable=False)
    # время готовности
    time_out = models.DateTimeField(blank=True)
    # общая стоимость
    cost = models.FloatField(validators=[MinValueValidator(0.0)])
    # на вынос?
    is_take_away = models.BooleanField(default=False)
    # завершен?
    is_complete = models.BooleanField(default=False)
    # оплачен?
    is_paid = models.BooleanField(default=False)
    # статус
    status = models.CharField(max_length=3, choices=STATUSES, default='NEW')
    # внешний ключ на исполнителя заказа
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    # внешний ключ на промежуточную таблицу товары-заказы
    dish = models.ManyToManyField(Dish, through='DishOrder', related_name='order')

    # функция reverse позволяет нам указывать не путь вида /booking/…, а название пути, которое мы задали
    # в файле urls.py для аргумента name
    def get_absolute_url(self):
        return reverse('order_detail', args=[str(self.pk)])

    # фиксируем время завершения заказа
    def finish_order(self):
        self.time_out = timezone.now()
        self.is_complete = True
        self.is_paid = True
        self.save()

    # возвращает время выполнения заказа в минутах
    def get_duration(self):
        if self.is_complete:
            return (self.time_out - self.time_in).total_seconds() // 60
        else:
            return (timezone.now() - self.time_in).total_seconds() // 60


# Модель для вспомогательной таблицы Товары-Заказы
class DishOrder(models.Model):
    # поля таблицы, поле id создается автоматически, его указывать не нужно
    # количество товаров в заказе
    amount = models.IntegerField(validators=[MinValueValidator(0)], default=1)
    # внешний ключ на таблицу товаров
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    # внешний ключ на таблицу заказов
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    # считаем стоимость товара в заказе
    def dish_cost(self):
        dish_price = self.dish.price_discount
        return dish_price * self.amount
