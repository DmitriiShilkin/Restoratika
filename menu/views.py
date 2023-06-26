from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

from .forms import MenuSectionForm, DishForm
from .models import MenuSection, Dish


# Create your views here.
# Представление для просмотра всех разделов меню
class MenuSectionListView(ListView):
    model = MenuSection
    ordering = 'name'
    template_name = 'menu/sections.html'
    context_object_name = 'sections'
    paginate_by = 10


# Представление для просмотра и редактирования раздела меню
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


# Представление для создания раздела меню
class MenuSectionCreateView(CreateView):
    # используемая форма
    form_class = MenuSectionForm
    # используемая модель
    model = MenuSection
    # имя шаблона, в соответствии с которым информация будет отображаться на странице
    template_name = 'menu/section_create.html'
    success_url = reverse_lazy('sections_list')


# Представление, удаляющее раздел меню
class MenuSectionDeleteView(DeleteView):
    model = MenuSection
    template_name = 'menu/section_delete.html'
    success_url = reverse_lazy('sections_list')


# Представление для просмотра всех блюд
class DishListView(ListView):
    model = Dish
    ordering = 'name'
    template_name = 'menu/dishes.html'
    context_object_name = 'dishes'
    paginate_by = 10


# Представление для просмотра и редактирования блюда
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


# Представление для создания блюда
class DishCreateView(CreateView):
    # используемая форма
    form_class = DishForm
    # используемая модель
    model = Dish
    # имя шаблона, в соответствии с которым информация будет отображаться на странице
    template_name = 'menu/dish_create.html'
    success_url = reverse_lazy('dishes_list')


# Представление, удаляющее блюдо
class DishDeleteView(DeleteView):
    model = Dish
    template_name = 'menu/dish_delete.html'
    success_url = reverse_lazy('dishes_list')


# Представление добавления блюда в стоп-лист
def add_stop_list_view(request, pk):
    # получаем активное блюдо
    dish = Dish.objects.get(id=pk)

    # добавляем в стоп-лист
    dish.is_in_stop_list = True
    dish.save()

    return redirect('/dishes/')


# Представление удаления блюда из стоп-листа
def del_stop_list_view(request, pk):
    # получаем активное блюдо
    dish = Dish.objects.get(id=pk)

    # добавляем в стоп-лист
    dish.is_in_stop_list = False
    dish.save()

    return redirect('/dishes/')
