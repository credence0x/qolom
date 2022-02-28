from django import forms
from account.models import BusinessProfile, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.urls import reverse
from django.http import HttpResponseRedirect
chars = ['1','2','3','4','5','6','7','8','9','0','~','@','$',
        '#','%','^','&','*','(',')','+','=','{','}',']','[',
        "'",';',':','/','>','<','?','/','.',',','\\','-','_','`']
AGE_CHOICES =( (0, 'None'),
    (1, 1),(2, 2), (3, 3), (4, 4), (5, 5),
    (6, 6),(7, 7), (8, 8), (9, 9), (10, 10),
    (11, 11),(12, 12), (13, 13), (14, 14), (15, 15),
    (16, 16),(17, 17), (18, 18), (19, 19), (20, 20),
    (21, 21)
)

class CreateUserAccountForm(forms.Form):
    country    = forms.CharField(max_length=200,
                                  widget=forms.HiddenInput(attrs={
                                      'id':'country'}))

    iso_code = forms.CharField(max_length=2,
                                 widget=forms.HiddenInput(attrs={
                                      'id':'iso_code'}))
 
    first_name = forms.CharField(max_length=15,
                                  
                                  widget=forms.TextInput(
                                      attrs={
                                             'class':'forms'}))

    
    last_name  = forms.CharField(max_length=30,
                                 
                                  widget=forms.TextInput(
                                      attrs={
                                             'class':'forms'}))
    date_of_birth = forms.DateField(
                                  widget=forms.DateInput(
                                      attrs={
                                             'class':'forms'}))
    
    
    email    = forms.EmailField(max_length=250,
                                label ='E-mail',
                                widget=forms.EmailInput(
                                      attrs={
                                             'class':'forms'}))
    
    username =forms.CharField(max_length=80,
                              
                              widget=forms.TextInput(
                                      attrs={
                                             'id':'username',
                                             'class':'forms'}))
    
    password = forms.CharField(max_length=80,
                               
                               widget=forms.PasswordInput(
                                      attrs={
                                             'id':'password',
                                             'class':'forms'}))
    
    password2 = forms.CharField(max_length=80,
                                label='Confirm password',
                               widget=forms.PasswordInput(
                                      attrs={
                                             'id':'password2',
                                             'class':'forms'}))
    timezone = forms.CharField(max_length=100,
                               label ='Timezone',
                               required=False,
                           widget=forms.HiddenInput(
                           attrs={'id':'tz',
                                  'class':'forms'}))
    def clean_email(self):
        cd = self.cleaned_data.get('email')
        cd = cd.lower()
        user = User.objects.filter(email=cd).exists()
        if user:
            raise forms.ValidationError('This e-mail address is already registered to another account')
        return cd

    
    def clean_timezone(self):
        cd = self.cleaned_data.get('timezone')
        if cd == 'undefined':
            raise forms.ValidationError('We couldn\'t get your timezone. Please update browser or switch to another browser')
        return cd

    def clean_username(self):
        cd = self.cleaned_data.get('username')
        cd = cd.lower()
        if len(cd) < 6:
            raise forms.ValidationError("Username must contain up to 6 characters")
        if ' ' in cd:
            raise forms.ValidationError("A blank space can not be included as part of username")
        user = User.objects.filter(username=cd).exists()
        if user:
            raise forms.ValidationError('Username is already taken. Please choose another username')
        return cd

    def clean_password(self):
        cd = self.cleaned_data
        if len(cd['password']) < 8:
            raise forms.ValidationError("Password must contain up to 8 characters including a number or special character")
        a = False
        for at_least_one in chars:
            if at_least_one in cd['password']:
                a = True
        if not a:
            raise forms.ValidationError(
                "Password must contain a number or special character")
        return cd['password']

    def clean(self):
        cleaned_data = super(CreateUserAccountForm, self).clean()
        ab = self.cleaned_data.get('password')
        cd = self.cleaned_data.get('password2')
        if ab != cd:
            self.add_error('password',"Passwords did not match")
        return cleaned_data

    
    
    

class BusinessAccountForm(forms.Form):
    name     = forms.CharField(max_length=250,
                               label='Business Name',
                                  widget=forms.TextInput(
                                      attrs={
                                             'class':'forms',
                                             'id':'name'}))
    
    address   = forms.CharField(max_length=300,
                                label='Address(including state/region)',
                                widget=forms.TextInput(attrs={
                                    'class':'forms',
                                    'id':'address'
                                    }))
    
    email    = forms.EmailField(max_length=250,
                                label='E-mail',
                                widget=forms.EmailInput(
                                      attrs={
                                             'class':'forms',
                                             'id':'email'}))
    minimum_age = forms.ChoiceField(choices = AGE_CHOICES,
                             label="Minimun required age to use business",
                             widget=forms.Select(
                              attrs={
                                     'class':'forms'}))
    username = forms.CharField(max_length=80,
                               
                              widget=forms.TextInput(
                                      attrs={
                                             'class':'forms',
                                             'id':'username'}))
    password = forms.CharField(max_length=80,
                               
                               widget=forms.PasswordInput(
                                      attrs={
                                             'class':'forms',
                                             'id':'password'}))
    password2 = forms.CharField(max_length=80,
                                label='Confirm password',
                               widget=forms.PasswordInput(
                                      attrs={
                                             'class':'forms',
                                             'id':'password2'}))
    
    state      = forms.CharField(max_length=200,
                                 
                                  widget=forms.HiddenInput(attrs={
                                      'id':'state'}))
    country    = forms.CharField(max_length=200,
                                  widget=forms.HiddenInput(attrs={
                                      'id':'country'}))
    timezone = forms.CharField(max_length=100,
                               label ='Timezone',
                               required=False,
                           widget=forms.HiddenInput(
                           attrs={'id':'tz',
                                  'class':'forms'}))

    iso_code = forms.CharField(max_length=2,
                                 widget=forms.HiddenInput(attrs={
                                      'id':'iso_code'}))

    
    def clean_email(self):
        cd = self.cleaned_data.get('email')
        cd = cd.lower()
        user = User.objects.filter(email=cd).exists() 
        if user:
            raise forms.ValidationError('E-mail address is already registered to another account')
        return cd
    
    def clean(self):
        cleaned_data = super(BusinessAccountForm, self).clean()
        cd = self.cleaned_data.get('name')
        iso_code = self.cleaned_data.get('iso_code')
        exists = BusinessProfile.objects.filter(name__iexact=cd,iso_code=iso_code).exists()
        if exists:
            self.add_error('name','''A business with the name "{}" already exists in your country.'''.format(cd))
        ab = self.cleaned_data.get('password')
        cd = self.cleaned_data.get('password2')
        if ab != cd:
            self.add_error('password',"Passwords did not match")
        return cleaned_data
    
    def clean_timezone(self):
        cd = self.cleaned_data.get('timezone')
        if cd == 'undefined':
            raise forms.ValidationError('We couldn\'t get your timezone. Please update browser or switch to another browser')
        return cd

    def clean_username(self):
        cd = self.cleaned_data.get('username')
        cd = cd.lower()
        if len(cd) < 6:
            raise forms.ValidationError("Username must contain up to 6 characters")
        if ' ' in cd:
            raise forms.ValidationError("A blank space can not be included as part of username")
        user = User.objects.filter(username=cd).exists()
        if user:
            raise forms.ValidationError('Username is already taken. Please choose another username.')
        return cd

    def clean_password(self):
        cd = self.cleaned_data
        if len(cd['password']) < 8:
            raise forms.ValidationError("Password must contain up to 8 characters including a number or special character")
        a = False
        for at_least_one in chars:
            if at_least_one in cd['password']:
                a = True
        if not a:
            raise forms.ValidationError(
                "Password must contain a number or special character ")
        return cd['password']

   
    
    
class LoginForm(forms.Form):
    username  = forms.CharField(max_length=80,
                                label=False,
                              widget=forms.TextInput(
                                      attrs={'placeholder':'username or e-mail',
                                             'class':'forms'}))
    password  = forms.CharField(max_length=80,
                                label=False,
                              widget=forms.PasswordInput(
                                      attrs={'placeholder':'password',
                                             'class':'forms'}))
  
    def clean_username(self):
        cd = self.cleaned_data.get('username')
        cd = cd.lower()
        return cd


class EditBusinessProfileForm(forms.Form):
    remove_logo = forms.BooleanField(required=False,label='Select to  delete logo')
    dp       = forms.ImageField(label='',
                                help_text='',
                                required=False,
                                widget=forms.FileInput())
    name     = forms.CharField(max_length=250,
                               label='Business Name',
                                  widget=forms.TextInput(
                                      attrs={
                                             'class':'forms'}))
    
    address   = forms.CharField(max_length=300,
                                label='Address (including state/region)',
                                widget=forms.TextInput(attrs={
                                    
                                    'class':'forms',
                                    }))
    minimum_age = forms.ChoiceField(choices = AGE_CHOICES,
                             label="Minimun required age to use business",
                             widget=forms.Select(
                              attrs={
                                     'class':'forms'}))
   
    password = forms.CharField(max_length=80,
                               widget=forms.PasswordInput(
                                      attrs={
                                             'class':'forms'}))
    
    state      = forms.CharField(max_length=200,
                                  widget=forms.HiddenInput(attrs={
                                      'id':'state'}))
    country    = forms.CharField(max_length=200,
                                  widget=forms.HiddenInput(attrs={
                                      'id':'country'}))
    iso_code = forms.CharField(max_length=2,
                                 widget=forms.HiddenInput(attrs={
                                      'id':'iso_code'}))
    timezone = forms.CharField(max_length=80,
                               label=False,
                           widget=forms.HiddenInput(
                           attrs={
                                  'id':'tz',
                                 'class': 'forms'}))
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EditBusinessProfileForm, self).__init__(*args, **kwargs)

    def clean_dp(self):
        cd = self.cleaned_data.get('dp')
        if cd:
            filesize= cd.size
            if filesize > 52400:
                raise forms.ValidationError("Image size must be 50KB or less")
        return cd
        



    

    
    def clean_password(self):
        cd = self.cleaned_data.get('password')
        person = self.user
        if not person.check_password(cd):
            raise forms.ValidationError('Invalid Password')
        return cd
    def clean(self):
        cleaned_data = super(EditBusinessProfileForm, self).clean()
        person = self.user
        business = person.BusinessProfile
        cd = self.cleaned_data.get('name')
        iso_code = self.cleaned_data.get('iso_code')
        exists = BusinessProfile.objects.filter(name__iexact=cd,
                                                iso_code=iso_code).exists()
        if exists and cd!=business.name:
            self.add_error('name','''A business with the name "{}" already exists in your country.'''.format(cd))
        return cleaned_data      

    
    
class ChangePasswordForm(forms.Form):
    password = forms.CharField(max_length=250,
                               label=False,
                               widget=forms.PasswordInput(
                               attrs={'placeholder':'Current password',
                                      'class': 'forms'}))
    new_password = forms.CharField(max_length=250,
                                    label=False,
                               widget=forms.PasswordInput(
                               attrs={'placeholder':'New password',
                                      'class': 'forms'}))
    confirm_password = forms.CharField(max_length=250,
                                    label=False,
                               widget=forms.PasswordInput(
                               attrs={'placeholder':'Confirm new password',
                                      'class': 'forms'}))
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
    
    def clean_password(self):
        cd = self.cleaned_data.get('password')
        user = self.user
        if not user.check_password(cd):
            raise forms.ValidationError('Invaid Password')
        return cd
    
    def clean_new_password(self):
        cd = self.cleaned_data.get('new_password')
        if len(cd) < 8:
            raise forms.ValidationError("Password must contain up to 8 characters including a number or special character")
        a = False
        for at_least_one in chars:
            if at_least_one in cd:
                a = True
        if not a:
            raise forms.ValidationError(
                "Password must contain a number or special character")
        return cd

    def clean_confirm_password(self):
        ab = self.cleaned_data.get('new_password')
        cd = self.cleaned_data.get('confirm_password')
        if type(ab)==type(cd):
            if ab != cd:
                raise forms.ValidationError("Passwords did not match")
        return cd        

class DeleteBusinessLineForm(forms.Form):
    delete = forms.CharField(max_length=250,widget=forms.HiddenInput())

class new_passwordForm(forms.Form):
    password1 = forms.CharField(max_length=250,
                                    label=False,
                               widget=forms.PasswordInput(
                               attrs={'placeholder':'New password',
                                      'class': 'forms'}))
    password2 = forms.CharField(max_length=250,
                                    label=False,
                               widget=forms.PasswordInput(
                               attrs={'placeholder':'Confirm password',
                                      'class': 'forms'}))
    def clean_password1(self):
        cd = self.cleaned_data.get('password1')
        if len(cd) < 8:
            raise forms.ValidationError("Password must contain up to 8 characters including a number or special character")
        a = False
        for at_least_one in chars:
            if at_least_one in cd:
                a = True
        if not a:
            raise forms.ValidationError(
                "Password must contain a number or special character")
        return cd

    def clean(self):
        cleaned_data = super(new_passwordForm, self).clean()
        ab = self.cleaned_data.get('password1')
        cd = self.cleaned_data.get('password2')
        if ab != cd:
            raise forms.ValidationError("Passwords did not match")
        return cleaned_data
        

class PasswordResetForm(forms.Form):
    username = forms.CharField(max_length=80,
                               label = False,
                              widget=forms.TextInput(
                                      attrs={'placeholder':'username or e-mail',
                                             'class':'forms'}))
    def clean_username(self):
        cd = self.cleaned_data.get('username')
        cd = cd.lower()
        return cd
    


class ChangeEmailForm(forms.Form):
    email = forms.EmailField(max_length=250,
                                label=False,
                                widget=forms.EmailInput(
                                      attrs={'placeholder':'Enter valid e-mail address',
                                             'class':'forms',
                                             }))

    def clean_email(self):
        cd = self.cleaned_data.get('email')
        cd = cd.lower()
        user = User.objects.filter(email__iexact=cd).exists() 
        if user:
            raise forms.ValidationError('E-mail address is registered to an account')
        return cd




        
