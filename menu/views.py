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
        self.form = DishSortForm(self.request.GET)
        if self.form.is_valid():
            if self.form.cleaned_data['ordering']:
                queryset = queryset.order_by(self.form.cleaned_data['ordering'])

        # Используем наш класс фильтрации.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = DishFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        context['form'] = self.form
        return context


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
