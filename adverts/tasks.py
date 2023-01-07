from celery import shared_task
import time
from adverts.models import Advert, Feedback, AdvertFeedback, NotificationMail
from django.core.mail import EmailMultiAlternatives
from datetime import datetime, timedelta
from django.template.loader import render_to_string
from django.contrib.auth.models import User

@shared_task
def week_notification():
    initial_date = datetime.today() - timedelta(days=7)
    adverts = Advert.objects.all(pub_time__gt=initial_date.isoformat())
    for advert in adverts:
        receivers = User.objects.exclude(user=advert.user)
        for receiver in receivers:
            html_content = render_to_string(
                'receivers_list_create.html',
                {'advert': advert, 'receiver': receiver}
            )
            text_body = ""
            for advert in adverts:
                text_body = text_body+f'{advert.title} \n http://127.0.0.1:8000{advert.get_absolute_url()} \n \n'
            msg = EmailMultiAlternatives(
                subject='Рассылка по подписке за неделю',
                body=text_body,
                from_email='romanags@yandex.ru',
                to=[receiver.user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

@shared_task
def feedback_pub_notification(oid):
    feedback = Feedback.objects.get(pk=oid)
    advertfeedback = AdvertFeedback.objects.get(feedback=feedback)
    advert = Advert.objects.get(pk=advertfeedback.advert.id)
    receivers = User.objects.exclude(username=feedback.user)
    for receiver in receivers:

        mail = NotificationMail(
            username = receiver.username,
            title = 'Оповещение об отклике',
            text = f'На ваше объявление {advert.title} пользователь {feedback.user} сделал отклик',
            first_name = receiver.first_name,
            last_name = receiver.last_name,
            link = feedback.get_absolute_url()
        )
        mail.save()

        html_content = render_to_string(
            'notification/notification_create.html',
            {'mail': mail}
        )

        msg = EmailMultiAlternatives(
            subject=f'{mail.title}',
            body=f'{mail.text}',
            from_email='romanags@yandex.ru',
            to=[receiver.email],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()

@shared_task
def feedback_del_notification(oid):
    feedback = Feedback.objects.get(pk=oid)
    advertfeedback = AdvertFeedback.objects.get(feedback=feedback)
    advert = Advert.objects.get(pk=advertfeedback.advert.id)
    receiver = User.objects.get(username=feedback.user)
    mail = NotificationMail(
        username = receiver.username,
        title = 'Оповещение об удалении отклика',
        text = f'Ваш отклик на объявление {advert.title} был удален пользователь',
        first_name = receiver.first_name,
        last_name = receiver.last_name,
        link = feedback.get_absolute_url()
    )
    mail.save()

    html_content = render_to_string(
        'notification/notification_create.html',
        {'mail': mail}
    )

@shared_task
def feedback_acc_notification(oid):
    feedback = Feedback.objects.get(pk=oid)
    advertfeedback = AdvertFeedback.objects.get(feedback=feedback)
    advert = Advert.objects.get(pk=advertfeedback.advert.id)
    receiver = User.objects.get(username=feedback.user)
    mail = NotificationMail(
        username = receiver.username,
        title = 'Оповещение о принятии отклика',
        text = f'Ваш отклик на объявление {advert.title} был принят',
        first_name = receiver.first_name,
        last_name = receiver.last_name,
        link = feedback.get_absolute_url()
    )
    mail.save()

    html_content = render_to_string(
        'notification/notification_create.html',
        {'mail': mail}
    )

    msg = EmailMultiAlternatives(
        subject=f'{mail.title}',
        body=f'{mail.text}',
        from_email='romanags@yandex.ru',
        to=[receiver.email],
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()

@shared_task
def feedback_rej_notification(oid):
    feedback = Feedback.objects.get(pk=oid)
    advertfeedback = AdvertFeedback.objects.get(feedback=feedback)
    advert = Advert.objects.get(pk=advertfeedback.advert.id)
    receiver = User.objects.get(username=feedback.user)
    mail = NotificationMail(
        username = receiver.username,
        title = 'Оповещение об отклонении отклика',
        text = f'Ваш отклик на объявление {advert.title} был отклонён',
        first_name = receiver.first_name,
        last_name = receiver.last_name,
        link = feedback.get_absolute_url()
    )
    mail.save()

    html_content = render_to_string(
        'notification/notification_create.html',
        {'mail': mail}
    )

    msg = EmailMultiAlternatives(
        subject=f'{mail.title}',
        body=f'{mail.text}',
        from_email='romanags@yandex.ru',
        to=[receiver.email],
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def advert_pub_notification(oid):
    advert = Advert.objects.get(pk=oid)
    receivers = User.objects.exclude(username=advert.user)
    for receiver in receivers:

        mail = NotificationMail(
            username = receiver.username,
            title = 'Новое объявление на портале Доска объявлений',
            text = f'Пользователь {advert.user.username} сделал новое объявление',
            first_name = receiver.first_name,
            last_name = receiver.last_name,
            link = advert.get_absolute_url()
        )
        mail.save()

        html_content = render_to_string(
            'notification/notification_create.html',
            {'mail': mail}
        )

        msg = EmailMultiAlternatives(
            subject=f'{mail.title}',
            body=f'{mail.text}',
            from_email='romanags@yandex.ru',
            to=[receiver.email],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()
