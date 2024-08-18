from django.utils import timezone
from celery import shared_task
from rest_framework.authtoken.models import Token
import logging
from datetime import timedelta
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


@shared_task
def deleteCookie():
    try:
        # Calculate the threshold date (1 day ago)
        threshold_date = timezone.now() - timedelta(days=5)

        # Filter tokens that are older than 1 day
        tokens_to_delete = Token.objects.filter(created__lt=threshold_date)

        # Log the number of tokens found
        logger.info(f"Found {tokens_to_delete.count()} tokens to delete.")

        # Delete the tokens
        tokens_to_delete.delete()

        logger.info("Tokens deleted successfully.")
    except Exception as e:
        logger.error(f"Error deleting tokens: {e}")


@shared_task
def send_welcome_email(user_email):
    print("inside send mail")
    subject = 'Welcome to Our Website'
    message = 'Thank you for registering with us. We are excited to have you!'
    # email_from = settings.DEFAULT_FROM_EMAIL  # or 'no-reply@yourdomain.com'
    email_from = 'testwelcom@elmassalla.com'  # or 'no-reply@yourdomain.com'
    recipient_list = [user_email]
    send_mail(subject, message, email_from, recipient_list)
