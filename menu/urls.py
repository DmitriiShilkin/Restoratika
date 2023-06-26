from django.urls import path

# импортируем наши представления
from .views import (MenuSectionListView, MenuSectionDetailView, MenuSectionCreateView, MenuSectionDeleteView)

urlpatterns = [
    # связываем представления с URL-адресами страниц
    path('', MenuSectionListView.as_view(), name='sections_list'),
    path('<int:pk>', MenuSectionDetailView.as_view(), name='section_detail'),
    path('create/', MenuSectionCreateView.as_view(), name='section_create'),
    path('<int:pk>/delete/', MenuSectionDeleteView.as_view(), name='section_delete'),
]
