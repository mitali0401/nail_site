from django import forms
from django.contrib.auth.models import User
from .import models

class ContactForm(forms.ModelForm):
    class Meta:
        model = models.Contact
        fields = '__all__'
        widgets = {
            'name' : forms.TextInput(attrs = {'class':'form-control','placeholder':'Your Name'}),
            'email' : forms.EmailInput(attrs = {'class':'form-control','placeholder':'Your Email'}),
            'phone' : forms.TextInput(attrs = {'class':'form-control','placeholder':'your phone Number'}),
            'comment' : forms.TextInput(attrs = {'class':'form-control'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username' , 'email' , 'password' , 'first_name' , 'last_name')

    def __init__(self , *args , **kwargs):
        super(UserForm, self).__init__(*args , **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class OrderForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)
