# импорт стандартных форм Джанго
from django import forms
# импорт метода для локализации полей формы
from django.utils.translation import gettext_lazy as _

from .models import MenuSection, Dish, Store


# форма для создания разделов меню
class MenuSectionForm(forms.ModelForm):

    #Удаляем двоеточие у Label
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

    menu_section = forms.ModelChoiceField(
        queryset=MenuSection.objects.all(),
        empty_label='Не выбрано',
        label='Категория'
    )

    #Удаляем двоеточие у Label
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
            'cost',
            'discount',
            'quantity',
            'store',
            'menu_section',
            'sticker',
            'is_in_POS',
            'is_in_delivery',
        ]

        # описания полей для отображения в форме
        labels = {
            'name': _('Наименование'),
            'description': _('Описание'),
            'picture': _('Фото'),
            # 'weight': _('Вес, гр.'),
            'price': _('Цена, руб.'),
            'cost': _('Себестоимость, руб.'),
            'discount': _('Скидка, %'),
            'quantity': _('Количество, шт.'),
            'sticker': _('Наклейка на карточке'),
            'is_in_POS': _('Показывать эту позицию в POS:'),
            'is_in_delivery': _('Показывать эту позицию на сайте доставки:'),
        }


class DishSortForm(forms.Form):
    SORT = [
        ('name', 'По алфавиту'),
        ('price_discount', 'По стоимости'),
    ]
    ordering = forms.ChoiceField(label='Порядок', choices=SORT, required=False)
