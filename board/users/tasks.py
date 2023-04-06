from users.models import Token
from boardapp.models import Post
from django.utils import timezone
from django.db.models import Count
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.contrib.sites.models import Site


def delete_old():
    Token.delete_old()


def newsletter():
    time = timezone.now() - timezone.timedelta(days=7)
    posts = Post.objects.filter(date__gte=time).annotate(Count('comment')).order_by('-comment__count')[0:5]
    users = get_user_model().objects.filter(subscriber=True).exclude(email='')
    subject = 'MessageBoard: Top posts this week'
    domain = Site.objects.get_current().domain
    for user in users:
        body = render_to_string('newsletter_email.html', {
            'posts': posts,
            'user': user,
            'domain': domain,
        })
        message = EmailMultiAlternatives(subject=subject, to=(user,))
        message.attach_alternative(body, "text/html")
        message.send()

