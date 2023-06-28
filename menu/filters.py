from django_filters import FilterSet, CharFilter, ModelChoiceFilter, ChoiceFilter

from django.forms import Select, TextInput

from .models import Dish, MenuSection

STOPLIST = [
    ('True', 'В стоп-листе'),
    ('False', 'Не в стоп-листе'),
]


# Создаем свой набор фильтров для модели Dish.
class DishFilter(FilterSet):
    # поиск по имени
    name = CharFilter(widget=TextInput(attrs={'placeholder': 'Название'}),
                      label='',
                      lookup_expr='icontains'
                      )
    # поиск по разделу меню
    menu_section = ModelChoiceFilter(queryset=MenuSection.objects.all(),
                                     label='',
                                     empty_label='Все разделы меню',
                                     )
    # поиск по стоп-листу
    is_in_stop_list = ChoiceFilter(choices=STOPLIST,
                                   label='',
                                   empty_label='Все блюда',
                                   lookup_expr='exact',
                                   )

    class Meta:
        # В Meta классе мы должны указать Django модель, в которой будем фильтровать записи.
        model = Dish
        # В fields мы описываем по каким полям модели будет производиться фильтрация.
        fields = [
            'name',
            'menu_section',
            'is_in_stop_list',
        ]
