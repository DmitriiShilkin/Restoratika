from django_filters import FilterSet, CharFilter, ModelChoiceFilter, ChoiceFilter

from django.forms import TextInput

from .models import Dish, MenuSection, Store

STOPLIST = [
    ('False', 'Да'),
    ('True', 'Нет'),
]


# Создаем свой набор фильтров для модели Dish.
class DishFilter(FilterSet):
    # поиск по наименованию
    name = CharFilter(widget=TextInput(attrs={'placeholder': 'Поиск'}),
                      label='Наименование',
                      lookup_expr='iregex'
                      )

    # поиск по складу
    store = ModelChoiceFilter(queryset=Store.objects.all(),
                              label='Склад',
                              empty_label='Все',
                              )

    # поиск по категории
    menu_section = ModelChoiceFilter(queryset=MenuSection.objects.all(),
                                     label='Категория',
                                     empty_label='Все',
                                     )
    # поиск по стоп-листу
    is_in_stop_list = ChoiceFilter(choices=STOPLIST,
                                   label='В наличии',
                                   empty_label='Все',
                                   lookup_expr='exact',
                                   )

    class Meta:
        # В Meta классе мы должны указать Django модель, в которой будем фильтровать записи.
        model = Dish
        # В fields мы описываем по каким полям модели будет производиться фильтрация.
        fields = [
            'store',
            'menu_section',
            'name',
            'is_in_stop_list',
        ]