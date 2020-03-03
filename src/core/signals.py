from django.db.models.signals import pre_delete, post_delete, post_save
from django.core.mail import EmailMessage
from django.dispatch import receiver
from django.template import Context
from django.template.loader import get_template
from src.settings import EMAIL_ADMIN
from .models import Product, Order


@receiver(pre_delete, sender=Product)
def product_pre_delete_receiver(sender, instance, **kwargs):
    instance.is_active = False


@receiver(post_delete, sender=Product)
def product_post_delete_receiver(sender, instance, **kwargs):
    instance.save()


@receiver(post_save, sender=Order)
def send_order_email_confirmation(sender, instance, **kwargs):
    order = instance
    message = get_template("emails/order_confirmation.html").render({'order': order.converted_data()})
    mail = EmailMessage(
        subject="Order confirmation",
        body=message,
        from_email=EMAIL_ADMIN,
        to=[order.email],
        reply_to=[EMAIL_ADMIN],
    )
    mail.content_subtype = "html"
    return mail.send()
