from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.urls import reverse_lazy
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import Comment


@receiver(post_save, sender=Comment)
def save_trigger(sender, instance, created, **kwargs):
    user = instance.post.author
    if created:
        to = user.email
        subject = 'You got a new reply'
        domain = Site.objects.get_current().domain
        body = render_to_string('reply_email.html', {
            'user': user,
            'post': instance.post,
            'reply': instance.text,
            'url': domain + reverse_lazy('reply_accept', kwargs={'pk': instance.pk}),
        })
        message = EmailMultiAlternatives(subject=subject,
                                         body='test',
                                         to=(to,))
        message.attach_alternative(body, "text/html")
        message.send()


@receiver(pre_save, sender=Comment)
def accept_trigger(sender, instance, **kwargs):
    if instance.pk:
        user = instance.author
        orig = Comment.objects.get(pk=instance.pk)
        if getattr(instance, 'accepted') != getattr(orig, 'accepted'):
            subject = 'Your reply was accepted!'
            message = f'Your reply "{instance.text}" to post "{instance.post}" was accepted!'
            user.email_user(subject, message)


