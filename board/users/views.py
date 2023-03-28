from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from .forms import SignUpForm, ActivationForm
from .models import Token
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.contrib.sites.models import Site


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'users/signup.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        token = Token.objects.create(user=user)
        domain = Site.objects.get_current().domain
        url = reverse_lazy('activate', args=[user.pk])
        subject = _('Activate your account')
        message = render_to_string('users/activation_email.html', {
            'user': user,
            'token': token.value,
            'url': domain + url,
        })
        user.email_user(subject, message)
        messages.success(self.request, _('Activation code sent to your e-mail.'))
        return redirect(url)


class AccountActivationView(FormView):
    form_class = ActivationForm
    template_name = 'users/signup.html'
    model = get_user_model()

    def form_valid(self, form):
        token = form.cleaned_data['activation_code']
        user = get_object_or_404(self.model, pk=self.kwargs['pk'])
        saved_token = get_object_or_404(Token, user=user).value
        if token == saved_token:
            user.is_active = True
            user.save()
            messages.success(self.request, _('Account activated.'))
            return redirect(reverse_lazy('login'))
        else:
            messages.error(self.request, _('Activation code is incorrect.'))
            return HttpResponseRedirect(self.request.path_info)


