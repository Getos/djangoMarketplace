from django.dispatch import receiver
from users.signals import send_email
from ecommerce.tasks import send_welcome_email


@receiver(send_email)
def delayed_sending_email(sender, **kwargs):
    print("singal recieved")
    send_welcome_email.delay(sender)
