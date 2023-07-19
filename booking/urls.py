from django.urls import path

# импортируем наши представления
from .views import (ApplicationsList, ApplicationDetail, ApplicationCreate,
                    application_cancel, application_validate, application_finish,
                    ApplicationCreateClient)

urlpatterns = [
    # связываем представления с URL-адресами страниц
    path('', ApplicationsList.as_view(), name='apps_list'),
    path('<int:pk>', ApplicationDetail.as_view(), name='app_detail'),
    path('create/', ApplicationCreate.as_view(), name='app_create'),
    path('create/success/', ApplicationCreate.as_view(template_name='booking/app_success.html'), name='app_success'),
    path('<int:pk>/validate/', application_validate, name='app_validate'),
    path('<int:pk>/cancel/', application_cancel, name='app_cancel'),
    path('<int:pk>/finish/', application_finish, name='app_finish'),
    path('createcl/', ApplicationCreateClient.as_view(), name='app_create_client'),
]
