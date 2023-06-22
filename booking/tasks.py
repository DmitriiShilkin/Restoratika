import json
import requests

from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


# отправка уведомления в telegram
def telegram_notification(booking_date, booking_time, client_name, client_phone, num_of_person):
    token = settings.TELBOT_TOKEN
    chat_id = settings.CHAT_ID
    message = f"Поступила новая заявка на бронирование столика!\n" \
              f"Дата:  {booking_date} в {booking_time}\n" \
              f"Гостей: {num_of_person} чел.\n" \
              f"Имя: {client_name} тел. {client_phone}"
    print(requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}").json())


# Отправка уведомления на почту клиента о подтверждении брони
def confirmed_email_notification(name, date, time, client_email):
    # указываем какой шаблон брать за основу и преобразовываем его в строку для отправки подписчику
    html_context = render_to_string(
        'mail/confirmed.html',
        {
            'name': name,
            'date': date,
            'time': time
        }
    )

    msg = EmailMultiAlternatives(
        # тема письма
        subject='Подтверждение брони',
        # тело пустое, потому что мы используем шаблон
        body='',
        # адрес отправителя
        from_email=settings.DEFAULT_FROM_EMAIL,
        # список адресатов
        to=[client_email],
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send(fail_silently=False)


# Отправка уведомления на почту клиента об отмене брони
def canceled_email_notification(name, date, time, client_email):
    # указываем какой шаблон брать за основу и преобразовываем его в строку для отправки подписчику
    html_context = render_to_string(
        'mail/canceled.html',
        {
            'name': name,
            'date': date,
            'time': time
        }
    )

    msg = EmailMultiAlternatives(
        # тема письма
        subject='Отмена брони',
        # тело пустое, потому что мы используем шаблон
        body='',
        # адрес отправителя
        from_email=settings.DEFAULT_FROM_EMAIL,
        # список адресатов
        to=[client_email],
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send(fail_silently=False)


# Создание задачи в Райде
def create_task(date: str, time: str, persons: int, name: str, phone: str, email: str, number: int, comment: str,
                hall: str, table: str):
    url = f"{settings.RAIDA_API_URL}/api/tasks/{settings.RAIDA_NODE_ID}/{settings.RAIDA_PROCESS_ID}"
    headers = {"Authorization": f"Bearer {settings.RAIDA_TOKEN}"}
    data = {
        "node_id": settings.RAIDA_NODE_ID,
        "process_id": settings.RAIDA_PROCESS_ID,
        "title": "application",
        "description": "Заявка на бронирование столика",
        "status_id": settings.RAIDA_NEW_STATUS_ID,
        "custom_fields": {
            "cf_date": str(date),
            "cf_time": str(time),
            "cf_number_persons": persons,
            "cf_comment": comment,
            "cf_client_name": name,
            "cf_client_phone": phone,
            "cf_client_email": email,
            "cf_app_number": number,
            "cf_hall": str(hall),
            "cf_table": str(table),
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = json.loads(response.text)

    # print(response)
    # print(result)

    return result.get("data")


# Обновление статуса и номера столика в задаче Райды
def update_task(table: str, status_id: str, task_id: str):
    url = f"{settings.RAIDA_API_URL}/api/tasks/{settings.RAIDA_NODE_ID}/{task_id}"
    headers = {"Authorization": f"Bearer {settings.RAIDA_TOKEN}"}
    data = {
        "status_id": status_id,
        "custom_fields": {
            "cf_table": str(table),
        }
    }

    response = requests.patch(url, headers=headers, data=json.dumps(data))
    result = json.loads(response.text)

    # print(response)
    # print(result)

    return result.get("data")


# Получение id задачи из Райды
def get_task_id(pk: int):
    url = f"{settings.RAIDA_API_URL}/api/tasks/{settings.RAIDA_NODE_ID}"
    headers = {"Authorization": f"Bearer {settings.RAIDA_TOKEN}"}

    response = requests.get(url, headers=headers)
    result = json.loads(response.text)

    for task in result.get('data'):
        if task.get('custom_fields').get('cf_app_number') == pk:
            return task.get('id')


# Получение id статуса из Райды
def get_status_id(status: str):
    url = f"{settings.RAIDA_API_URL}/api/statuses/{settings.RAIDA_NODE_ID}"
    headers = {"Authorization": f"Bearer {settings.RAIDA_TOKEN}"}

    response = requests.get(url, headers=headers)
    result = json.loads(response.text)

    for st in result.get('data'):
        if st.get('name') == status:
            return st.get('id')
