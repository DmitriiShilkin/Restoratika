import datetime

from django_filters import FilterSet, DateFilter
# from django_filters import CharFilter

from django.forms import DateInput
# from django.forms import Select

from .models import Application

# from .models import STATUSES


# Создаем свой набор фильтров для модели Application.
class ApplicationFilter(FilterSet):

    # задаем значение по умолчанию для фильтра, оно будет храниться в initial
    def __init__(self, data=None, *args, **kwargs):
        # if filterset is bound, use initial values as defaults
        if data is not None:
            # get a mutable copy of the QueryDict
            data = data.copy()

            for name, f in self.base_filters.items():
                initial = f.extra.get('initial')

                # filter param is either missing or empty, use initial as default
                if not data.get(name) and initial:
                    data[name] = initial

        super().__init__(data, *args, **kwargs)

    # поиск по статусу
    # status = CharFilter(widget=Select(choices=STATUSES), label='Статус', lookup_expr='exact')
    # поиск по дате бронирования (указанной клиентом)
    date = DateFilter(widget=DateInput(attrs={'type': 'date'}),
                      label='',
                      lookup_expr='exact',
                      initial=datetime.datetime.today().date()
                      )

    class Meta:
        # В Meta классе мы должны указать Django модель, в которой будем фильтровать записи.
        model = Application
        # В fields мы описываем по каким полям модели будет производиться фильтрация.
        fields = [
            # 'status',
            'date'
        ]
