from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.urls import reverse_lazy
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from .models import Comment


@receiver(post_save, sender=Comment)
def save_trigger(sender, instance, created, **kwargs):
    user = instance.post.author
    if created:
        subject = 'You got a new reply'
        domain = Site.objects.get_current().domain
        message = render_to_string('reply_email.html', {
            'user': user,
            'post': instance.post,
            'reply': instance.text,
            'url': domain + reverse_lazy('reply_accept', kwargs={'pk': instance.pk}),
        })
        user.email_user(subject, message)


@receiver(pre_save, sender=Comment)
def accept_trigger(sender, instance, **kwargs):
    user = instance.author
    orig = Comment.objects.get(id=instance.id)
    if getattr(instance, 'accepted') != getattr(orig, 'accepted'):
        subject = 'Your reply was accepted!'
        message = f'Your reply "{instance.text}" to post "{instance.post}" was accepted!'
        user.email_user(subject, message)


