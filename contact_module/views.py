from django.http import HttpResponseRedirect
from django.views.generic import ListView

from .forms import ContactUsModelForm
from django.views.generic.edit import CreateView


class ContactUsView(CreateView):
    form_class = ContactUsModelForm
    template_name = 'contact_module/contact.html'
    success_url = '/contact-us/'










