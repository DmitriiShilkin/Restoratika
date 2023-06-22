from django.urls import path
from django.views.generic import TemplateView

# импортируем наши представления
from .views import (ApplicationsList, ApplicationDetail, ApplicationCreate,
                    application_cancel, application_validate, application_finish,
                    ApplicationsNewList, ApplicationsConfirmedList, ApplicationsArchiveList)

# from .views import GetApplicationInfo

urlpatterns = [
    # связываем представления с URL-адресами страниц
    path('', ApplicationsList.as_view(), name='apps_list'),
    path('<int:pk>', ApplicationDetail.as_view(), name='app_detail'),
    path('create/', ApplicationCreate.as_view(), name='app_create'),
    path('create/success/', ApplicationCreate.as_view(template_name='booking/app_success.html'), name='app_success'),
    path('<int:pk>/validate/', application_validate, name='app_validate'),
    path('<int:pk>/cancel/', application_cancel, name='app_cancel'),
    path('<int:pk>/finish/', application_finish, name='app_finish'),
    path('new/', ApplicationsNewList.as_view(), name='new'),
    path('confirmed/', ApplicationsConfirmedList.as_view(), name='confirmed'),
    path('archive/', ApplicationsArchiveList.as_view(), name='archive'),

    # путь для представления-сериализатора, не используется
    # path('api/applications/', GetApplicationInfo.as_view(), name='api_list'),
]
