# import asyncio
# from aiohttp import ClientSession
import json
import requests

from django.conf import settings


# отправка уведомления в telegram
def telegram_notification(booking_id, booking_date, booking_time, client_name, client_phone, num_of_person):
    data = {
        "event_code": "First_Restoratika_test",
        "user_identifier": settings.USER_IDENTIFIER,
        "project_identifier": settings.PROJECT_IDENTIFIER,
        "message_recipients": [
            {
                "telegram_chat_id": -1001917100200
            }
        ],
        "parameters": {
            "c_booking_date": booking_date.strftime('%d.%m.%Y'),
            "c_booking_id": booking_id,
            "c_booking_time": booking_time.strftime('%H:%M'),
            "c_client_name": client_name,
            "c_client_phone": client_phone,
            "c_num_of_person": num_of_person
        }
    }
    requests.post('https://notification.skroy.ru/notification', json=data)


# Отправка уведомления на почту клиента о подтверждении брони
def confirmed_email_notification(client_name, booking_date, booking_time, client_email):
    data = {
        "event_code": "resto_confirm_booking",
        "user_identifier": settings.USER_IDENTIFIER,
        "project_identifier": settings.PROJECT_IDENTIFIER,
        "message_recipients":
            [
                {
                    "email": client_email
                }
            ],
        "parameters": {
            "c_booking_date": booking_date.strftime('%d.%m.%Y'),
            "c_booking_time": booking_time.strftime('%H:%M'),
            "c_client_name": client_name
            }
    }
    requests.post('https://notification.skroy.ru/notification', json=data)


# Отправка уведомления на почту клиента об отмене брони
def canceled_email_notification(client_name, booking_date, booking_time, client_email):
    data = {
        "event_code": "resto_cancel_booking",
        "user_identifier": settings.USER_IDENTIFIER,
        "project_identifier": settings.PROJECT_IDENTIFIER,
        "message_recipients":
            [
                {
                    "email": client_email
                }
            ],
        "parameters": {
            "c_booking_date": booking_date.strftime('%d.%m.%Y'),
            "c_booking_time": booking_time.strftime('%H:%M'),
            "c_client_name": client_name
            }
    }
    requests.post('https://notification.skroy.ru/notification', json=data)


# Создание задачи в Райде
def create_task(date, time, persons: int, name: str, phone: str, email: str, number: int, comment: str,
                hall: int, table: int, created_at, status_id: str):
    url = f"{settings.RAIDA_API_URL}/api/tasks/{settings.RAIDA_NODE_ID}/{settings.RAIDA_PROCESS_ID}"
    headers = {"Authorization": f"Bearer {settings.RAIDA_TOKEN}"}
    data = {
        "node_id": settings.RAIDA_NODE_ID,
        "process_id": settings.RAIDA_PROCESS_ID,
        "title": "application",
        "description": "Заявка на бронирование столика",
        "status_id": status_id,
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
            "cf_created_at": str(created_at)
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = json.loads(response.text)
    # future = asyncio.ensure_future(asyncio.sleep(1, result=result.get("data")))

    return result


# Обновление статуса и номера столика в задаче Райды
def update_task(date, time, persons: int, name: str, phone: str, email: str, number: int, comment: str,
                hall: int, table: int, created_at, status_id: str, task_id: str):
    url = f"{settings.RAIDA_API_URL}/api/tasks/{settings.RAIDA_NODE_ID}/{task_id}"
    headers = {"Authorization": f"Bearer {settings.RAIDA_TOKEN}"}
    data = {
        "status_id": status_id,
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
            "cf_created_at": str(created_at)
        }
    }

    response = requests.patch(url, headers=headers, data=json.dumps(data))
    result = json.loads(response.text)
    # future = asyncio.ensure_future(asyncio.sleep(1, result=result.get("data")))

    return result.get("data")


# async def aupdate_task():
#     task = asyncio.create_task(update_task(app.date,
#                         app.time, app.number_persons, app.client_name, app.client_phone, app.client_email,
#                         app.pk, app.comment, app.hall, app.table, status_id, task_id))
#     await task


# Получение id задачи из Райды
def get_task_id(pk: int, created_at):
    url = f"{settings.RAIDA_API_URL}/api/tasks/{settings.RAIDA_NODE_ID}"
    headers = {"Authorization": f"Bearer {settings.RAIDA_TOKEN}"}

    response = requests.get(url, headers=headers)
    result = json.loads(response.text)

    for task in result.get('data'):
        if task.get('custom_fields').get('cf_app_number') == pk \
                and task.get('custom_fields').get('cf_created_at') == str(created_at):
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
