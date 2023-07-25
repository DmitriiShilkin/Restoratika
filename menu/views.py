from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

from .filters import DishFilter
from .forms import MenuSectionForm, DishForm, DishSortForm
from .models import MenuSection, Dish


# Create your views here.
# Представление для просмотра всех категорий
class MenuSectionListView(ListView):
    model = MenuSection
    ordering = 'name'
    template_name = 'menu/sections.html'
    context_object_name = 'sections'
    paginate_by = 20


# Представление для просмотра и редактирования категории
class MenuSectionDetailView(UpdateView):
    # используемая форма
    form_class = MenuSectionForm
    # используемая модель
    model = MenuSection
    # имя шаблона, в соответствии с которым информация будет отображаться на странице
    template_name = 'menu/section.html'
    # контекстное имя объекта для использования в шаблоне
    context_object_name = 'section'
    success_url = reverse_lazy('sections_list')


# Представление для создания категории
class MenuSectionCreateView(CreateView):
    # используемая форма
    form_class = MenuSectionForm
    # используемая модель
    model = MenuSection
    # имя шаблона, в соответствии с которым информация будет отображаться на странице
    template_name = 'menu/section_create.html'
    success_url = reverse_lazy('sections_list')


# Представление, удаляющее категорию
class MenuSectionDeleteView(DeleteView):
    model = MenuSection
    template_name = 'menu/section_delete.html'
    success_url = reverse_lazy('sections_list')


# Представление для просмотра всех товаров
class DishListView(ListView):
    model = Dish
    template_name = 'menu/dishes.html'
    context_object_name = 'dishes'
    paginate_by = 20
    ordering = 'name'

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()

        # Применяем выбранную сортировку
        self.sortform = DishSortForm(self.request.GET)
        if self.sortform.is_valid():
            if self.sortform.cleaned_data['ordering']:
                queryset = queryset.order_by(self.sortform.cleaned_data['ordering'])

        # Используем наш класс фильтрации.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = DishFilter(self.request.GET, queryset)
        self.in_stock = DishFilter(self.request.GET, queryset.filter(is_in_stop_list='False'))
        self.stop_list = DishFilter(self.request.GET, queryset.filter(is_in_stop_list='True'))
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        context['sortform'] = self.sortform
        context['in_stock'] = self.in_stock.qs
        context['stop_list'] = self.stop_list.qs

        return context

    # изменение цены у товара в представлении списком
    def post(self, request, *args, **kwargs):
        # если пост-запрос не пустой
        if request.POST:
            # получаем последний элемент из QueryDict
            for element in request.POST.items():
                d = element
            # находим товар в БД с названием из запроса
            dish = Dish.objects.get(pk=d[0])
            new_price = float(d[1])
            if dish.price != new_price:
                # устанавливаем новую цену
                dish.price = abs(new_price)
                dish.save()

        return redirect('/dishes/')


# Представление для просмотра и редактирования товара
class DishDetailView(UpdateView):
    # используемая форма
    form_class = DishForm
    # используемая модель
    model = Dish
    # имя шаблона, в соответствии с которым информация будет отображаться на странице
    template_name = 'menu/dish.html'
    # контекстное имя объекта для использования в шаблоне
    context_object_name = 'dish'
    success_url = reverse_lazy('dishes_list')


# Представление для создания товара
class DishCreateView(CreateView):
    # используемая форма
    form_class = DishForm
    # используемая модель
    model = Dish
    # имя шаблона, в соответствии с которым информация будет отображаться на странице
    template_name = 'menu/dish_create.html'
    success_url = reverse_lazy('dishes_list')


# Представление, удаляющее товар
class DishDeleteView(DeleteView):
    model = Dish
    template_name = 'menu/dish_delete.html'
    success_url = reverse_lazy('dishes_list')


# Представление добавления товара в стоп-лист
def add_stop_list_view(request, pk):
    # получаем активное блюдо
    dish = Dish.objects.get(id=pk)

    # добавляем в стоп-лист
    dish.is_in_stop_list = True
    dish.save()

    return redirect('/dishes/')


# Представление удаления товара из стоп-листа
def del_stop_list_view(request, pk):
    # получаем активное блюдо
    dish = Dish.objects.get(id=pk)

    # добавляем в стоп-лист
    dish.is_in_stop_list = False
    dish.save()

    return redirect('/dishes/')


# Представление для просмотра всех товаров в наличии
class DishInstockView(ListView):
    model = Dish
    template_name = 'menu/dishes.html'
    context_object_name = 'dishes'
    paginate_by = 20
    ordering = 'name'

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()

        # Применяем выбранную сортировку
        self.sortform = DishSortForm(self.request.GET)
        if self.sortform.is_valid():
            if self.sortform.cleaned_data['ordering']:
                queryset = queryset.order_by(self.sortform.cleaned_data['ordering'])

        # Используем наш класс фильтрации.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = DishFilter(self.request.GET, queryset.filter(is_in_stop_list='False'))
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        context['sortform'] = self.sortform

        return context

    # изменение цены у товара в представлении списком
    def post(self, request, *args, **kwargs):
        # если пост-запрос не пустой
        if request.POST:
            # получаем последний элемент из QueryDict
            for element in request.POST.items():
                d = element
            # находим товар в БД с названием из запроса
            dish = Dish.objects.get(pk=d[0])
            new_price = float(d[1])
            if dish.price != new_price:
                # устанавливаем новую цену
                dish.price = abs(new_price)
                dish.save()

        return redirect('/dishes/instock/')


# Представление для просмотра всех товаров в стоп-листе
class DishStoplistView(ListView):
    model = Dish
    template_name = 'menu/dishes.html'
    context_object_name = 'dishes'
    paginate_by = 20
    ordering = 'name'

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()

        # Применяем выбранную сортировку
        self.sortform = DishSortForm(self.request.GET)
        if self.sortform.is_valid():
            if self.sortform.cleaned_data['ordering']:
                queryset = queryset.order_by(self.sortform.cleaned_data['ordering'])

        # Используем наш класс фильтрации.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = DishFilter(self.request.GET, queryset.filter(is_in_stop_list='True'))
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        context['sortform'] = self.sortform

        return context

    # изменение цены у товара в представлении списком
    def post(self, request, *args, **kwargs):
        # если пост-запрос не пустой
        if request.POST:
            # получаем последний элемент из QueryDict
            for element in request.POST.items():
                d = element
            # находим товар в БД с названием из запроса
            dish = Dish.objects.get(pk=d[0])
            new_price = float(d[1])
            if dish.price != new_price:
                # устанавливаем новую цену
                dish.price = abs(new_price)
                dish.save()

        return redirect('/dishes/stoplist')
