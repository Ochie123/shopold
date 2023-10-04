from django import forms
from django.core.mail import send_mail 
import logging
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

from crispy_forms import bootstrap, helper, layout

from categories.models import Category
from products.models import Tag
from .models import Product
from products.models import SearchTerm
User = get_user_model()

logger = logging.getLogger(__name__)

class ContactForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)
    email = forms.EmailField(label='Your email', max_length=100) 
    message = forms.CharField(max_length=600, widget=forms.Textarea)
    
    def send_mail(self):
        logger.info("Sending email to customer service")
        subject = "Site message"
        message = f"From: {self.cleaned_data['name']} <{self.cleaned_data['email']}>\n{self.cleaned_data['message']}"
        sender_email = self.cleaned_data['email']  # Use the user's email as the sender
        recipient_list = ['sales@svgcraft.co']  # Your domain email address
        send_mail(
            subject,
            message,
            sender_email,
            recipient_list,
            fail_silently=False,
    )

class SearchsForm(forms.Form): 
    query = forms.CharField(
    label=u'Enter a keyword to search for',
    widget=forms.TextInput(attrs={'size': 32}) 
    )


class ProductFilterForm(forms.Form):

    category = forms.ModelChoiceField(
        label=_("Category"),
        required=False,
        queryset=Category.objects.annotate(
            product_count=models.Count("category_products")
        ).filter(product_count__gt=0),
    )


###Search
class SearchForm(forms.ModelForm): 
    class Meta:
        model = SearchTerm
        fields='__all__'

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs) 
        default_text = 'Search' 
        self.fields['q'].widget.attrs['value'] = default_text 
        self.fields['q'].widget.attrs['onfocus'] = "if (this.value=='" + default_text + "')this.value = ''" 
    
    include = ('q',)