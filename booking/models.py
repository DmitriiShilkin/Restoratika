import json
# импорт модуля даты и времени
from datetime import datetime, timedelta

from django.urls import reverse
# импорт стандартных моделей
from django.db import models

from django.db import transaction
# импорт валидаторов
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator

# возможные значения поля status в таблице Application
STATUSES = [
    ('NEW', 'Новая'),
    ('VAL', 'Проверяется'),
    ('CNF', 'Подтверждена'),
    ('CAN', 'Отменена'),
    ('FIN', 'Завершена'),
]

# параметр, который определяет интервал (в минутах), когда стол не может быть забронирован -/+ относительно
# действующей брони. Например, стол забронирован на 15:00, тогда интервал будет (13:30...16:30), крайние значения в
# в интервал не входят
INTERVAL = 90


# Модель для связи приложения с таблицей Hall базы данных
class Hall(models.Model):
    # поля таблицы, поле id создается автоматически, его указывать не нужно
    name = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=255, blank=True)

    # указываем, как будет отображаться название на странице
    def __str__(self):
        return self.name.title()


# Модель для связи приложения с таблицей Table базы данных
class Table(models.Model):
    # поля таблицы, поле id создается автоматически, его указывать не нужно
    number = models.CharField(max_length=10)
    description = models.CharField(max_length=128, blank=True)
    is_available = models.BooleanField(default=True)
    occupied = models.TextField(default=[])
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)

    # занимаем столик на указанную дату-время и преобразуем список в строку для записи в БД
    def set_occupied(self, date, time):
        dt = str(datetime.combine(date, time))
        # читаем новое (не кэшированное) значение из БД
        table = Table.objects.get(id=self.pk)
        occupied = table.occupied
        occupied_list = json.loads(occupied)
        if dt not in occupied_list:
            occupied_list.append(dt)
            self.occupied = json.dumps(occupied_list)
            self.save()

    # преобразуем строку из БД в список, освобождаем столик, делаем обратное преобразование
    def free_occupied(self, date, time):
        dt = str(datetime.combine(date, time))
        occupied_list = json.loads(self.occupied)
        if dt in occupied_list:
            occupied_list.remove(dt)
            self.occupied = json.dumps(occupied_list)
            self.save()

    # преобразуем строку из БД в список и проверяем занят ли стол на указанную дату-время
    def is_occupied(self, date, time):
        dt = datetime.combine(date, time)
        occupied_list = json.loads(self.occupied)
        minutes = -(INTERVAL - 5)
        while minutes < INTERVAL:
            new_dt = dt + timedelta(minutes=minutes)
            minutes += 5
            if str(new_dt) in occupied_list:
                return True
        return False

    # указываем, как будет отображаться номер на странице
    def __str__(self):
        return self.number


# Модель для связи приложения с таблицей Application базы данных
class Application(models.Model):
    # поля таблицы
    created_at = models.DateTimeField(auto_now_add=True)
    number_persons = models.IntegerField(default=2, validators=[MinValueValidator(1), MaxValueValidator(999)])
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=3, choices=STATUSES)
    comment = models.CharField(max_length=128, blank=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, default=1)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, default=1)
    client_name = models.CharField(max_length=64)
    client_phone = models.CharField(max_length=17)
    client_email = models.EmailField(max_length=32, validators=[EmailValidator])

    # функция reverse позволяет нам указывать не путь вида /booking/…, а название пути, которое мы задали
    # в файле urls.py для аргумента name
    def get_absolute_url(self):
        return reverse('app_detail', args=[str(self.pk)])
