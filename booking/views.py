from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
# from django.shortcuts import redirect
# импорт стандартных дженериков-представлений из Джанго
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy

# импорт библиотек для работы с API, не используются
# from rest_framework.response import Response
# from rest_framework.views import APIView

# импорт нашей модели
from .models import Application, Table
# импорт нашей формы
from .forms import ApplicationForm, ApplicationUpdateForm
# импорт нашего фильтра
from .filters import ApplicationFilter
# импорт задач по рассылке уведомлений
from .tasks import telegram_notification
# from .tasks import confirmed_email_notification, canceled_email_notification
# импорт задач по работе с Райда
from .tasks import create_task
from .tasks import update_task, get_task_id, get_status_id
# импорт сериалайзера, не используется
# from .serializers import ApplicationSerializer


def get_free_tables(app):
    free_tables = []
    tables = Table.objects.all()
    for table in tables:
        if not table.is_occupied(app.date, app.time):
            free_tables += table
    return free_tables

# Представление для отображения списком всех заявок
class ApplicationsList(ListView):
    # используемая модель
    model = Application
    # сортировка списка по полю в порядке от новых к старым
    ordering = '-created_at'
    # имя шаблона, в соответствии с которым информация будет отображаться на странице
    template_name = 'booking/apps.html'
    # контекстное имя объекта для использования в шаблоне
    context_object_name = 'apps'
    # максимальное количество записей, выводимых на одной странице
    paginate_by = 10

    # переопределяем функцию получения списка заявок
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = ApplicationFilter(self.request.GET, queryset)
        self.new = Application.objects.filter(status='NEW')
        self.check = Application.objects.filter(status='VAL')
        self.new_val = Application.objects.filter(Q(status='NEW') | Q(status='VAL'))
        self.confirmed = ApplicationFilter(self.request.GET, queryset.filter(status='CNF'))
        self.archive = ApplicationFilter(self.request.GET, queryset.filter(Q(status='CAN') | Q(status='FIN')))

        # Возвращаем из функции отфильтрованный список заявок
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        context['new'] = self.new
        context['check'] = self.check
        context['new_val'] = self.new_val
        context['confirmed'] = self.confirmed.qs
        context['archive'] = self.archive.qs

        return context


# Представление для просмотра заявки, изменения её статуса и выбора столика
class ApplicationDetail(UpdateView):
    # используемая форма
    form_class = ApplicationUpdateForm
    # используемая модель
    model = Application
    # имя шаблона, в соответствии с которым информация будет отображаться на странице
    template_name = 'booking/app.html'
    # контекстное имя объекта для использования в шаблоне
    context_object_name = 'app'
    success_url = reverse_lazy('apps_list')

    def form_valid(self, form):
        # получаем данные из формы до сохранения
        app = form.save(commit=False)

        # присваиваем статус "Подтверждена"
        if app.status not in ['CNF', 'CAN', 'FIN']:
            app.status = 'CNF'

            # Если столик выбран, то занимаем его
            if app.table.id != 1:
                app.table.set_occupied(app.date, app.time)
                app.table.save()

            # получаем id статуса и задачи из Райды
            status_id = get_status_id(app.status)
            task_id = get_task_id(app.pk)
            # обновляем задачу в Райде
            # update_task(app.table, status_id, task_id)

            # отправляем уведомление о подтверждении брони клиенту
            # confirmed_email_notification(app.client_name, app.date, app.time, app.client_email)

        # сохраняем данные из формы в нашу БД
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Application.objects.all()
        new = ApplicationFilter(self.request.GET, queryset.filter(status='NEW'))
        # Добавляем в контекст объект фильтрации.
        context['new'] = new.qs

        return context


# Представление для ввода данных в форму
class ApplicationCreate(CreateView):
    # используемая форма
    form_class = ApplicationForm
    # используемая модель
    model = Application
    # имя шаблона, в соответствии с которым информация будет отображаться на странице
    template_name = 'booking/app_create.html'
    success_url = reverse_lazy('app_success')

    # метод валидации данных в форме
    def form_valid(self, form):
        # получаем данные из формы до сохранения
        app = form.save(commit=False)
        # вызываем метод super, для сохранения данных из формы в БД и чтобы у заявки появился pk
        result = super().form_valid(form)

        # если выбран столик, то сохраняем его
        if app.table.id != 1:
            app.table.save()

        # создаем задачу в Райде
        # create_task(app.date, app.time, app.number_persons, app.client_name, app.client_phone, app.client_email,
        #             app.pk, app.comment, app.hall, app.table)

        # уведомление о новых заявках в телеграм (чат менеджеров)
        # telegram_notification(app.date, app.time, app.client_name, app.client_phone, app.number_persons)

        # сохраняем данные из формы в нашу БД
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Application.objects.all()
        new = ApplicationFilter(self.request.GET, queryset.filter(status='NEW'))
        # Добавляем в контекст объект фильтрации.
        context['new'] = new.qs

        return context


# Представление-заглушка для стартовой страницы
def startpage(request):
    # Сохраняем нашу фильтрацию в объекте класса,
    # чтобы потом добавить в контекст и использовать в шаблоне.
    queryset = Application.objects.all()
    new = ApplicationFilter(request.GET, queryset.filter(status='NEW'))
    context = {
        'new': new.qs
    }

    return render(request, "index.html", context)


# Представление для отмены заявки
def application_cancel(request, pk):
    # получаем активную заявку
    app = Application.objects.get(id=pk)

    # присваиваем статус "Отменена"
    if app.status not in ['CAN', 'FIN']:
        app.status = 'CAN'

        # Если столик занят, то освобождаем его
        if app.table.id != 1:
            app.table.free_occupied(app.date, app.time)
            app.table.save()

        # сохраняем изменения в заявке
        app.save()

        # получаем id статуса и задачи из Райды
        status_id = get_status_id(app.status)
        task_id = get_task_id(app.pk)
        # обновляем задачу в Райде
        # update_task(app.table, status_id, task_id)

        # отправляем уведомление об отмене брони клиенту
        # canceled_email_notification(app.client_name, app.date, app.time, app.client_email)

        queryset = Application.objects.all()
        new = ApplicationFilter(request.GET, queryset.filter(status='NEW'))
        context = {
            'new': new.qs,
            'app': app
        }

        return render(request, 'booking/app_canceled.html', context)

    return redirect('app_detail', pk=app.id)


# Представление переключения статуса заявки на "Проверяется"
def application_validate(request, pk):
    # получаем активную заявку
    app = Application.objects.get(id=pk)
    # queryset = Application.objects.all()
    # new = ApplicationFilter(request.GET, queryset.filter(status='NEW'))

    # присваиваем статус "Проверяется"
    if app.status == 'NEW':
        app.status = 'VAL'
        app.save()

        # получаем id статуса и задачи из Райды
        status_id = get_status_id(app.status)
        task_id = get_task_id(app.pk)
        # обновляем задачу в Райде
        # update_task(app.table, status_id, task_id)

    # context = {
    #     'new': new.qs,
    #     'app': app
    # }

    # return render(request, 'booking/app.html', context)
    return redirect('app_detail', pk=app.id)


# Представление завершения заявки
def application_finish(request, pk):
    # получаем активную заявку
    app = Application.objects.get(id=pk)

    # присваиваем статус "Завершена"
    if app.status == 'CNF':
        app.status = 'FIN'

        # Если столик занят, то освобождаем его
        if app.table.number != 1:
            app.table.free_occupied(app.date, app.time)
            app.table.save()

        # сохраняем изменения в заявке
        app.save()

        # получаем id статуса и задачи из Райды
        status_id = get_status_id(app.status)
        task_id = get_task_id(app.pk)
        # обновляем задачу в Райде
        # update_task(app.table, status_id, task_id)

        queryset = Application.objects.all()
        new = ApplicationFilter(request.GET, queryset.filter(status='NEW'))
        context = {
            'new': new.qs,
            'app': app
        }

        return render(request, 'booking/app_finished.html', context)

    return redirect('app_detail', pk=app.id)


# Представление для отображения новых заявок
class ApplicationsNewList(ApplicationsList):

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = ApplicationFilter(self.request.GET, queryset.filter(status='NEW'))
        # Возвращаем из функции отфильтрованный список заявок
        return self.filterset.qs


# Представление для отображения подтвержденных заявок
class ApplicationsConfirmedList(ApplicationsList):

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = ApplicationFilter(self.request.GET, queryset.filter(status='CNF'))
        # Возвращаем из функции отфильтрованный список заявок
        return self.filterset.qs


# Представление для отображения архивных заявок
class ApplicationsArchiveList(ApplicationsList):

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = ApplicationFilter(self.request.GET, queryset.filter(Q(status='CAN') | Q(status='FIN')))
        # Возвращаем из функции отфильтрованный список заявок
        return self.filterset.qs


# Представление для сериализации данных из таблицы Application. Не используется
# class GetApplicationInfo(APIView):
#
#     def get(self, request):
#         # Получаем набор всех записей из таблицы Application
#         queryset = Application.objects.all()
#         # Сериализуем извлечённый набор записей
#         serializer_for_queryset = ApplicationSerializer(
#             instance=queryset, # Передаём набор записей
#             many=True # Указываем, что на вход подаётся именно набор записей
#         )
#         return Response(serializer_for_queryset.data)
