from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post, Category, PostCategory
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance,  **kwargs):
    subscribes = []
    for cat in instance.category.all():
        subscribes += Category.objects.get(category_name=cat.category_name).subscribes.all()
    for user in set(subscribes):
        html_content = render_to_string(
            'post_for_male.html', {'post': instance, 'user': user}
        )
        msg = EmailMultiAlternatives(
            subject=instance.title,
            body=f'Здравствуй, {user.username}. Новая статья в твоём любимом разделе!',  # это то же, что и message
            from_email='nikitaf73@yandex.ru',
            to=[user.email,],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()
