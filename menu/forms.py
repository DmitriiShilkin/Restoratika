# импорт стандартных форм Джанго
from django import forms
from django.forms import NumberInput
# импорт метода для локализации полей формы
from django.utils.translation import gettext_lazy as _

from .models import MenuSection, Dish, Store


# форма для создания разделов меню
class MenuSectionForm(forms.ModelForm):

    # Удаляем двоеточие у Label
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix

    class Meta:
        # наша модель
        model = MenuSection
        # поля, которые будут выводиться в форму, в порядке указания в списке
        fields = [
            'name',
            'description'
        ]

        # описания полей для отображения в форме
        labels = {
            'name': _('Название'),
            'description': _('Описание'),
        }


# форма для создания блюд
class DishForm(forms.ModelForm):

    store = forms.ModelChoiceField(
        queryset=Store.objects.all(),
        empty_label='Не выбрано',
        label='Склад списания'
    )

    menu_section = forms.ModelMultipleChoiceField(
        queryset=MenuSection.objects.all(),
        # empty_label='Не выбрано',
        label='Категория'
    )

    price = forms.FloatField(widget=NumberInput(
        attrs={'type': 'text', 'id': 'price', 'oninput': 'limit_input(7, id)'}),
        min_value=0.01,
        label='Цена, руб.',
    )

    discount = forms.FloatField(widget=NumberInput(
        attrs={'type': 'text', 'id': 'discount', 'oninput': 'limit_input(5, id)'}),
        label='Скидка, %',
        initial=0.0
    )

    discount_rub = forms.FloatField(widget=NumberInput(
        attrs={'type': 'text', 'id': 'discount_rub', 'oninput': 'limit_input(5, id)'}),
        label='Скидка, руб.',
        initial=0.0
    )

    increment = forms.FloatField(widget=NumberInput(
        attrs={'type': 'text', 'id': 'increment', 'oninput': 'limit_input(5, id)'}),
        label='Надбавка, %',
        initial=0.0
    )

    increment_rub = forms.FloatField(widget=NumberInput(
        attrs={'type': 'text', 'id': 'increment_rub', 'oninput': 'limit_input(5, id)'}),
        label='Надбавка, руб.',
        initial=0.0
    )

    # Удаляем двоеточие у Label
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix

    class Meta:
        # наша модель
        model = Dish
        # поля, которые будут выводиться в форму, в порядке указания в списке
        fields = [
            'name',
            'description',
            'picture',
            # 'weight',
            'price',
            # 'cost',
            # 'quantity',
            'store',
            'menu_section',
            'sticker',
            'discount',
            'discount_rub',
            'increment',
            'increment_rub',
            'is_in_POS',
            'is_in_delivery',
        ]

        # описания полей для отображения в форме
        labels = {
            'name': _('Наименование'),
            'description': _('Описание'),
            'picture': _('Фото'),
            # 'weight': _('Вес, гр.'),
            # 'cost': _('Себестоимость, руб.'),
            # 'quantity': _('Количество, шт.'),
            'sticker': _('Наклейка на карточке'),
            'is_in_POS': _('в POS:'),
            'is_in_delivery': _('на сайте доставки:'),
        }


class DishSortForm(forms.Form):
    SORT = [
        ('name', 'По алфавиту'),
        ('price_discount', 'По стоимости'),
    ]
    ordering = forms.ChoiceField(label='Порядок', choices=SORT, required=False)
