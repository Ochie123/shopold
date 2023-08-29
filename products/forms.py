from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

from crispy_forms import bootstrap, helper, layout

from categories.models import Category

from .models import Product
from products.models import SearchTerm
User = get_user_model()

class ProductFilterForm(forms.Form):

    category = forms.ModelChoiceField(
        label=_("Category"),
        required=False,
        queryset=Category.objects.annotate(
            product_count=models.Count("category_products")
        ).filter(product_count__gt=0),
    )

class ProductSearchForm(forms.Form):
    q = forms.CharField(label=_("Search for"), required=False)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

        self.helper = helper.FormHelper()
        self.helper.form_action = self.request.path
        self.helper.form_method = "GET"
        self.helper.layout = layout.Layout(
            layout.Field("q", css_class="input-block-level"),
            layout.Submit("search", _("Search")),
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