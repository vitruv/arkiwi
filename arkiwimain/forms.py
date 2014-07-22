# -*- coding: utf-8 -*-
from django import forms
from djangular.forms.angular_model import NgModelFormMixin
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.views.generic import TemplateView

class ImageUploadForm(NgModelFormMixin, forms.Form):

    """Image upload form."""

    name = forms.CharField()
    architect = forms.CharField()
    image = forms.ImageField()


class ContactFormView(TemplateView):
    template = 'djangulartests.html'

    def get_context_data(self, **kwargs):
        context = super(ContactFormView, self).get_context_data(**kwargs)
        context.update(contact_form=ContactForm())
        return context

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(ContactFormView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest('Expected an XMLHttpRequest')
        in_data = json.loads(request.body)
        bound_contact_form = CheckoutForm(data={'subject': in_data.get('subject')})
        # now validate ‘bound_contact_form’ and use it as in normal Django

    def __init__(self, *args, **kwargs):
        kwargs.update(scope_prefix='my_prefix')
        super(ContactForm, self).__init__(*args, **kwargs)