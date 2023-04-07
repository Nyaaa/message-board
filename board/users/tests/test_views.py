from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from users.models import Token


class ViewTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = get_user_model().objects.create_user(username='user1', password='12345')
        cls.new_user_data = {'username': 'user2', 'email': 'test@localhost',
                             'password1': '321321ewq', 'password2': '321321ewq'}

    def testSignUp(self):
        response = self.client.post(reverse('signup'), follow=True,
                                    data=self.new_user_data)
        user = get_user_model().objects.filter(username='user2')
        self.assertRedirects(response, reverse('activate', args=[user[0].pk]),
                             status_code=302, target_status_code=200,
                             fetch_redirect_response=True)
        self.assertTrue(user.exists())
        self.assertFalse(user[0].is_active)

    def testTokenCorrect(self):
        self.client.post(reverse('signup'), data=self.new_user_data)
        user = get_user_model().objects.get(username='user2')
        token = Token.objects.filter(user=user.pk)
        self.assertTrue(token.exists())
        token_val = token[0].value
        response = self.client.post(reverse('activate', args=[user.pk]), follow=True,
                                    data={'activation_code': token_val})
        self.assertRedirects(response, reverse('login'),
                             status_code=302, target_status_code=200,
                             fetch_redirect_response=True)
        user.refresh_from_db()
        self.assertTrue(user.is_active)

    def testTokenIncorrect(self):
        self.client.post(reverse('signup'), data=self.new_user_data)
        user = get_user_model().objects.get(username='user2')
        response = self.client.post(reverse('activate', args=[user.pk]), follow=True,
                                    data={'activation_code': 000})
        self.assertRedirects(response, reverse('activate', args=[user.pk]),
                             status_code=302, target_status_code=200,
                             fetch_redirect_response=True)
        user.refresh_from_db()
        self.assertFalse(user.is_active)

    def testProfileTimezone(self):
        self.client.login(username='user1', password='12345')
        self.client.post(reverse('profile'), data={'timezone': 'Europe/Berlin'})
        self.assertEqual(self.client.session['django_timezone'], 'Europe/Berlin')

    def testNewsletterSubscribe(self):
        self.client.login(username='user1', password='12345')
        user = get_user_model().objects.get(username='user1')
        self.assertFalse(user.subscriber)
        self.client.post(reverse('profile'), data={'newsletter': 'on'})
        user.refresh_from_db()
        self.assertTrue(user.subscriber)

    def testNewsletterUnsubscribe(self):
        self.client.login(username='user1', password='12345')
        user = get_user_model().objects.get(username='user1')
        user.subscriber = True
        user.save()
        self.client.post(reverse('profile'), data={'newsletter': 'off'})
        user.refresh_from_db()
        self.assertFalse(user.subscriber)
