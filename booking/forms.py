# импорт модуля даты и времени
from datetime import datetime
# импорт стандартных форм Джанго
from django import forms
# импорт ошибки валидации из исключений
from django.core.exceptions import ValidationError
# импорт поля ввода даты
from django.forms import DateInput, TimeInput, EmailInput, TextInput, NumberInput
# импорт метода для локализации полей формы
from django.utils.translation import gettext_lazy as _

# импорт нашей модели
from .models import Application

HOURS_STATES = [
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
    ('13', '13'),
    ('14', '14'),
    ('15', '15'),
    ('16', '16'),
    ('17', '17'),
    ('18', '18'),
    ('19', '19'),
    ('20', '20'),
    ('21', '21'),
    ('22', '22'),
    ('23', '23'),
    ('0', '24')
]

MINUTES_STATES = [
    ('0', '0'),
    ('5', '5'),
    ('10', '10'),
    ('15', '15'),
    ('20', '20'),
    ('25', '25'),
    ('30', '30'),
    ('35', '35'),
    ('40', '40'),
    ('45', '45'),
    ('50', '50'),
    ('55', '55')
]

GUESTS_STATES = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10')
]


# форма для ввода данных о бронировании менеджером
class ApplicationForm(forms.ModelForm):

    #Удаляем двоеточие у Label
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix
        if self.instance.time:
            self.fields['hours'].initial = self.instance.time.hour
            self.fields['minutes'].initial = self.instance.time.minute
        if self.instance.number_persons:
            if self.instance.number_persons <= 10:
                self.fields['guest_num'].initial = self.instance.number_persons

    # поля с проверками минимальной длины, виджетом выбора даты, времени и описанием для отображения в форме
    client_phone = forms.CharField(min_length=11, max_length=13, label='Телефон')
    date = forms.DateField(widget=DateInput(
        attrs={'type': 'date', 'class': 'my_class'}),
        label='',
        initial=datetime.today().date()
    )
    client_email = forms.EmailField(widget=EmailInput(attrs={'type': 'email'}), label='E-mail', required=False)
    hours = forms.ChoiceField(widget=forms.RadioSelect, choices=HOURS_STATES, label='Часы')
    minutes = forms.ChoiceField(widget=forms.RadioSelect, choices=MINUTES_STATES, label='Минуты')
    guest_num = forms.ChoiceField(widget=forms.RadioSelect, choices=GUESTS_STATES, label='', required=False)
    number_persons = forms.IntegerField(widget=NumberInput(
        attrs={'type': 'text', 'class': 'my_class', 'id': 'number_field', 'oninput': 'limit_input()'}),
        label='Количество гостей',
        initial=2,
    )

    class Meta:
        # наша модель
        model = Application
        # поля, которые будут выводиться в форму, в порядке указания в списке
        fields = [
            'client_name',
            'client_phone',
            'client_email',
            # 'hall',
            'comment',
            'number_persons',
            'guest_num',
            'date',
            'hours',
            'minutes',
            'table'
        ]

        # описания полей для отображения в форме
        labels = {
            'client_name': _('Имя'),
            # 'hall': _('Зал'),
            'table': _(''),
            'number_persons': _(''),
            'comment': _('Комментарий'),
        }

    def clean(self):
        cleaned_data = super().clean()

        # получаем введенное имя
        name = cleaned_data.get("client_name")
        # убираем пробелы и дефисы и нижние подчеркивания, чтобы можно было выполнить дальнейшую проверку
        for i in name:
            name = name.replace('-', '')
            name = name.replace('_', '')
            name = name.replace(' ', '')

        # проверяем имя на наличие цифр и спец. символов
        if not name.isalpha():
            raise ValidationError(
                "Имя может содержать только буквы, пробелы, дефисы и нижние подчеркивания!"
            )

        # получаем введенный номер телефона
        phone = cleaned_data.get("client_phone")

        if '+' in phone[1:]:
            raise ValidationError(
                "Знак '+' может быть только в начале номера!"
            )

        # убираем "+", чтобы можно было выполнить дальнейшую проверку
        for i in phone:
            phone = phone.replace('+', '')

        # проверяем номер телефона на наличие букв и спец. символов
        if not phone.isdigit():
            raise ValidationError(
                "В номере телефона допустимы только цифры и знак '+'!"
            )

        # проверка атуальности даты и времени бронирования
        # получаем введенную дату бронирования
        date = cleaned_data.get("date")
        # получаем введенное время бронирования
        # time_ = cleaned_data.get("time")
        hours = cleaned_data.get("hours")
        minutes = cleaned_data.get("minutes")
        time_str = f'{hours}:{minutes}:00'
        # преобразуем строку в time-объект
        time = datetime.strptime(time_str, '%H:%M:%S').time()
        # объединяем дату и время
        date_and_time = datetime.combine(date, time)
        # сравниваем введенные дату и время с текущими датой и временем
        if date_and_time <= datetime.now():
            raise ValidationError(
                "Дата бронирования не может быть раньше текущей!"
            )

        # получаем введенное количество гостей
        number_persons = cleaned_data.get("number_persons")
        guest_num = cleaned_data.get("guest_num")
        # проверяем, из какой переменной взять количество гостей для сохранения в БД
        # значения от 1 до 10 включ. хранятся в guest_num, а больше 10 - в number_persons
        persons = number_persons if guest_num == '' else guest_num

        self.cleaned_data["number_persons"] = persons
        self.instance.time = time

        # получаем выбранный столик
        table = cleaned_data.get("table")

        # если он занят, то выводим ошибку
        if not (table == self.instance.table and date == self.instance.date and time == self.instance.time) and\
                table.is_occupied(date, time):
            raise ValidationError(
                "Выбранный столик уже забронирован!"
            )

        return cleaned_data


# форма для ввода данных о бронировании клиентом
class ApplicationClientForm(forms.ModelForm):

    #Удаляем двоеточие у Label
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix

    client_name = forms.CharField(widget=TextInput(
        attrs={'type': 'text', 'class': 'my_class', 'placeholder': 'Имя'}),
        label='',
    )
    # поля с проверками минимальной длины, виджетом выбора даты, времени и описанием для отображения в форме
    client_phone = forms.CharField(widget=TextInput(
        attrs={'type': 'text', 'class': 'my_class', 'placeholder': 'Телефон'}),
        label='',
        min_length=11,
        max_length=17,
    )

    date = forms.DateField(widget=DateInput(
        attrs={'type': 'date', 'class': 'my_class'}),
        label='Дата и время визита',
    )
    time = forms.CharField(widget=TextInput(
        attrs={'type': 'text', 'class': 'my_class'}),
        label=' ',
    )
    client_email = forms.EmailField(widget=EmailInput(
        attrs={'type': 'email', 'class': 'my_class', 'placeholder': 'E-mail'}),
        label='',
    )
    comment = forms.CharField(widget=TextInput(
        attrs={'type': 'text', 'class': 'my_class', 'placeholder': 'Комментарий'}),
        label='',
        required=False,
    )

    number_persons = forms.IntegerField(widget=NumberInput(
        attrs={'type': 'text', 'class': 'my_class', 'id': 'number_field', 'oninput': 'limit_input()'}),
        label='',
        initial=2,
    )

    agreement = forms.BooleanField(label='Даю согласие на обработку моих персональных данных', required=True)

    class Meta:
        # наша модель
        model = Application
        # поля, которые будут выводиться в форму, в порядке указания в списке
        fields = [
            'client_name',
            'client_phone',
            'date',
            'time',
            'client_email',
            'comment',
            'number_persons',
            'agreement',
         ]

    def clean(self):
        cleaned_data = super().clean()

        # получаем введенное имя
        name = cleaned_data.get("client_name")
        # убираем пробелы и дефисы и нижние подчеркивания, чтобы можно было выполнить дальнейшую проверку
        for i in name:
            name = name.replace('-', '')
            name = name.replace('_', '')
            name = name.replace(' ', '')

        # проверяем имя на наличие цифр и спец. символов
        if not name.isalpha():
            raise ValidationError(
                "Имя может содержать только буквы, пробелы, дефисы и нижние подчеркивания!"
            )

        # получаем введенный номер телефона
        phone = cleaned_data.get("client_phone")

        if '+' in phone[1:]:
            raise ValidationError(
                "Знак '+' может быть только в начале номера!"
            )

        new_phone = phone

        # убираем "+", "-", "(", ")" и " ", чтобы можно было выполнить дальнейшую проверку
        for i in phone:
            phone = phone.replace('+', '')
            phone = phone.replace('-', '')
            phone = phone.replace('(', '')
            phone = phone.replace(')', '')
            phone = phone.replace(' ', '')

        # проверяем номер телефона на наличие букв и спец. символов
        if not phone.isdigit():
            raise ValidationError(
                "В номере телефона допустимы только цифры, пробелы и знаки '+', '-', '(', ')'!"
            )

        # оставляем в номере только знак "плюс", если он есть
        for i in new_phone:
            new_phone = new_phone.replace('-', '')
            new_phone = new_phone.replace('(', '')
            new_phone = new_phone.replace(')', '')
            new_phone = new_phone.replace(' ', '')

        self.cleaned_data["client_phone"] = new_phone

        # проверка атуальности даты и времени бронирования
        # получаем введенную дату бронирования
        date = cleaned_data.get("date")
        # получаем введенное время бронирования
        time = cleaned_data.get("time")
        time_str = f'{time}:00'
        # преобразуем строку в time-объект
        time = datetime.strptime(time_str, '%H:%M:%S').time()
        # объединяем дату и время
        date_and_time = datetime.combine(date, time)
        # сравниваем введенные дату и время с текущими датой и временем
        if date_and_time <= datetime.now():
            raise ValidationError(
                "Дата бронирования не может быть раньше текущей!"
            )
        self.cleaned_data["time"] = time

        return cleaned_data


# class ApplicationUpdateForm(forms.ModelForm):
#
#     # Удаляем двоеточие у Label
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.label_suffix = ""  # Removes : as label suffix
#
#     class Meta:
#         # наша модель
#         model = Application
#         # поля, которые будут выводиться в форму, в порядке указания в списке
#         fields = [
#             # 'hall',
#             'table'
#         ]
#
#         # описания полей для отображения в форме
#         labels = {
#             # 'hall': _('Зал'),
#             'table': _(''),
#         }
#
#     def clean(self):
#         cleaned_data = super().clean()
#
#         app = Application.objects.get(id=self.instance.pk)
#
#         # получаем выбранный столик
#         table = cleaned_data.get("table")
#         # если он занят, то выводим ошибку
#         if table.is_occupied(app.date, app.time):
#             raise ValidationError(
#                 "Выбранный столик уже забронирован!"
#             )
#
#         return cleaned_data

# ApplicationForm.base_fields['table'] = forms.ModelChoiceField(
#     widget=forms.Select,
#     queryset=Table.objects.filter(is_occupied=False),
#     label='',
#     empty_label='Выбрать стол'
# )
#
#
# ApplicationUpdateForm.base_fields['table'] = forms.ModelChoiceField(
#     widget=forms.Select,
#     queryset=Table.objects.filter(is_occupied=False),
#     label='',
#     empty_label='Занят'
# )
