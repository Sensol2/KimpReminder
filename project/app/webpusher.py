from django.contrib.auth import get_user_model

from webpush import send_user_notification

def episode_webpush():
    User = get_user_model()
    users = User.objects.all()

    for user in users:
        payload = {"head": "Welcome!", "body": "Hello World"}
        send_user_notification(user=user, payload=payload, ttl=1000)