# импорт стандартных форм Джанго
from django import forms
# импорт метода для локализации полей формы
from django.utils.translation import gettext_lazy as _

from .models import MenuSection, Dish


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

    menu_section = forms.ModelChoiceField(
        queryset=MenuSection.objects.all(),
        empty_label='Не выбрано',
        label='Раздел меню'
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
            'weight',
            'price',
            'discount',
            'quantity',
            'menu_section',
        ]

        # описания полей для отображения в форме
        labels = {
            'name': _('Название'),
            'description': _('Описание'),
            'picture': _('Иконка'),
            'weight': _('Вес, гр.'),
            'price': _('Цена, руб.'),
            'discount': _('Скидка, %'),
            'quantity': _('Количество, шт.'),
        }
