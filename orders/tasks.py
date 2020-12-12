from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail
from .models import Order

@shared_task
def order_created(order_id):
	order = Order.objects.get(id=order_id)
	subject = f"Order number {order.id}"
	message = f"Dear {order.first_name},\n\nYou have successfully placed an order.\nYour order id is {order.id}"
	
	mail_sent = send_mail(subject, message,'150223109@kocaeli.edu.tr',[order.email])

	return mail_sent
