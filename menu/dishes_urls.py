from django.urls import path

# импортируем наши представления
from .views import (DishListView, DishDetailView, DishCreateView, DishDeleteView,
                    add_stop_list_view, del_stop_list_view,
                    DishInstockView, DishStoplistView)

urlpatterns = [
    # связываем представления с URL-адресами страниц
    path('', DishListView.as_view(), name='dishes_list'),
    path('<int:pk>', DishDetailView.as_view(), name='dish_detail'),
    path('create/', DishCreateView.as_view(), name='dish_create'),
    path('<int:pk>/delete/', DishDeleteView.as_view(), name='dish_delete'),
    path('<int:pk>/addsl/', add_stop_list_view, name='dish_addsl'),
    path('<int:pk>/delsl/', del_stop_list_view, name='dish_delsl'),
    path('instock/', DishInstockView.as_view(), name='dishes_instock'),
    path('stoplist/', DishStoplistView.as_view(), name='dishes_stoplist'),
]
