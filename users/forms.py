from django import forms
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist

chars = ['1','2','3','4','5','6','7','8','9','0','~','@','$',
        '#','%','^','&','*','(',')','+','=','{','}',']','[',
        "'",';',':','/','>','<','?','/','.',',','\\','-','_','`']

class SearchForm(forms.Form):
    search = forms.CharField(max_length=2000,       
                             label=False,
                             widget=forms.TextInput(
                               attrs={'id':'search_for',
                                      'class': 'inputtext searchpad',
                                      'placeholder':'Search for places'}))



class GetLocationForm(forms.Form):
    country_code = forms.CharField(max_length=2000,widget=forms.HiddenInput())
    
    statin = forms.CharField(max_length=2000,widget=forms.HiddenInput())
    
    cty = forms.CharField(max_length=2000,widget=forms.HiddenInput())
    
    locaty = forms.CharField(max_length=2000,widget=forms.HiddenInput())
   
    
class SearchByLocationForm(forms.Form):
    s_b_l = forms.CharField(max_length=2000,
                                         label=False,
                                 widget=forms.TextInput(
                                   attrs={'class': 's_b_l inputtext searchpad',
                                            
                                          'placeholder':'Search by Location'}))
    
  

class EditProfileForm(forms.Form):
    country  = forms.CharField(max_length=250,
                               label=False,
                                  widget=forms.HiddenInput(
                                      attrs={'class':'forms',
                                             'id':'country'}))
    iso_code  = forms.CharField(max_length=250,
                                  widget=forms.HiddenInput(
                                      attrs={'class':'forms',
                                             'id':'iso_code'}))
                               
    first_name = forms.CharField(max_length=15,
                                  label=False,
                                  widget=forms.TextInput(
                                      attrs={'placeholder':'First Name',
                                             'class':'forms'})
                                  )
    last_name  = forms.CharField(max_length=30,
                                  label=False,
                                  widget=forms.TextInput(
                                      attrs={'placeholder':'Last Name',
                                             'class':'forms'}))
    timezone = forms.CharField(max_length=80,
                               label=False,
                           widget=forms.HiddenInput(
                           attrs={'placeholder':'Timezone',
                                  'id':'tz',
                                 'class': 'forms'}))


    password = forms.CharField(max_length=80,
                               label=False,
                               widget=forms.PasswordInput(
                                      attrs={'placeholder':'Enter password',
                                             'class':'forms'}))
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EditProfileForm, self).__init__(*args, **kwargs)
    
    
    def clean_password(self):
        cd = self.cleaned_data.get('password')
        person = self.user
        if not person.check_password(cd):
            raise forms.ValidationError('Invaid Password')
        return cd


UNIT_CHOICES =( 
    ("1", "1"),("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"),
    ("6", "6"),("7", "7"), ("8", "8"), ("9", "9"), ("10", "10"),
    ("11", "11"),("12", "12"), ("13", "13"), ("14", "14"), ("15", "15"),
    ("16", "16"),("17", "17"), ("18", "18"), ("19", "19"), ("20", "20"),
    ("21", "21"),("22", "22"), ("23", "23"), ("24", "24"), ("25", "25"),
    ("26", "26"),("27", "27"), ("28", "28"), ("29", "29"), ("30", "30"),
    ("31", "31"),("32", "32"), ("33", "33"), ("34", "34"), ("35", "35"),
    ("36", "36"),("37", "37"), ("38", "38"), ("39", "39"), ("40", "40"),
    ("41", "41"),("42", "42"), ("43", "43"), ("44", "44"), ("45", "45"),
    ("46", "46"),("47", "47"), ("48", "48"), ("49", "49"), ("50", "50"),
)

class UserMenuForm(forms.Form):
    
                               
    Item = forms.CharField(max_length=250,
                                  label=False,
                                  widget=forms.TextInput(
                                      attrs={'placeholder':'Item',
                                             'class':'forms'})
                                  )
    cost_per_unit  = forms.CharField(max_length=30,
                                  label=False,
                                  widget=forms.TextInput(
                                      attrs={'placeholder':'Cost Per Unit',
                                             'class':'forms'}))
    number_of_units = forms.ChoiceField(choices = UNIT_CHOICES)







class CheckKeyForm(forms.Form):
    key = forms.CharField(max_length=8,
                            label=False,
                            widget=forms.TextInput(
                              attrs={'placeholder':'Enter key',
                                     'class':'forms',
                                     }))

    




class EditLineForm(forms.Form):
    name = forms.CharField(max_length=50,
                           widget=forms.TextInput(
                           attrs={'placeholder':'Name of Line (e.g Coffee Line)',
                                 'class': 'forms'}))
    information = forms.CharField(max_length=250,
                                  required = False,
                           widget=forms.TextInput(
                           attrs={'placeholder':'Information (e.g Please wait in line to get coffee)',
                                 'class': 'forms'}))
    instruction = forms.CharField(max_length=250,
                                  required=False,
                           widget=forms.TextInput(
                           attrs={'placeholder':'Instruction (e.g Please be available before you\'re third)',
                                 'class': 'forms'}))
        
    monday = forms.BooleanField(required=False)
    mo_o = forms.TimeField(required=False,
                           widget=forms.TimeInput(
                           attrs={'class': 'time',
                                 'placeholder':' HH:MM',
                                  'type':'time'
                                 }))
    
    mo_c = forms.TimeField(required=False,
                           widget=forms.TimeInput(
                           attrs={'class': 'time',
                                 'placeholder':' HH:MM',
                                  'type':'time'}))
    
    tuesday = forms.BooleanField(required=False)
    tu_o = forms.TimeField(required=False,
                           widget=forms.TimeInput(
                           attrs={'class': 'time',
                                 'placeholder':' HH:MM',
                                  'type':'time'
                                 }))
    
    
    tu_c = forms.TimeField(required=False,
                           widget=forms.TimeInput(
                           attrs={'class': 'time',
                                 'placeholder':' HH:MM',
                                  'type':'time'}))
    wednesday = forms.BooleanField(required=False)
    we_o = forms.TimeField(required=False,
                           widget=forms.TimeInput(
                           attrs={'class': 'time',
                                 'placeholder':' HH:MM',
                                  'type':'time'
                                 }))
    
    we_c = forms.TimeField(required=False,
                           widget=forms.TimeInput(
                           attrs={'class': 'time',
                                 'placeholder':' HH:MM',
                                  'type':'time'}))
    thursday = forms.BooleanField(required=False)
    th_o = forms.TimeField(required=False,
                           widget=forms.TimeInput(
                           attrs={'class': 'time',
                                 'placeholder':' HH:MM',
                                  'type':'time'
                                 }))
    
    th_c = forms.TimeField(required=False,
                           widget=forms.TimeInput(
                           attrs={'class': 'time',
                                 'placeholder':' HH:MM',
                                  'type':'time'}))
    friday = forms.BooleanField(required=False)
    fr_o = forms.TimeField(required=False,
                           widget=forms.TimeInput(
                           attrs={'class': 'time',
                                 'placeholder':' HH:MM',
                                  'type':'time'
                                 }))
    
    fr_c = forms.TimeField(required=False,
                           widget=forms.TimeInput(
                           attrs={'class': 'time',
                                 'placeholder':' HH:MM',
                                  'type':'time'}))
    saturday = forms.BooleanField(required=False)
    sa_o = forms.TimeField(required=False,
                           widget=forms.TimeInput(
                           attrs={'class': 'time',
                                 'placeholder':' HH:MM',
                                  'type':'time'
                                 }))
    
    sa_c = forms.TimeField(required=False,
                           widget=forms.TimeInput(
                           attrs={'class': 'time',
                                 'placeholder':' HH:MM',
                                  'type':'time'}))
    sunday = forms.BooleanField(required=False)
    su_o = forms.TimeField(required=False,
                           widget=forms.TimeInput(
                           attrs={'class': 'time',
                                 'placeholder':' HH:MM',
                                  'type':'time'
                                 }))
    
    su_c = forms.TimeField(required=False,
                           widget=forms.TimeInput(
                           attrs={'class': 'time',
                                 'placeholder':' HH:MM',
                                  'type':'time'}))


        
    def __init__(self, user, line, *args, **kwargs):
        self.user = user
        self.this_line = line
        super(EditLineForm, self).__init__(*args, **kwargs)
    
    def clean_name(self):
        cd1 = self.cleaned_data.get('name')
        cd2 = slugify(cd1)
        
        try:
            self.user.BusinessProfile
            business = self.user.BusinessProfile
            all_associated_lines = Business_line.objects.filter(business=business) 
            for line in all_associated_lines:
                if cd2 == line.slug and line != self.this_line :
                    raise forms.ValidationError('Your business already has a line with this name')
        except ObjectDoesNotExist:
            pass
        
        return cd1





class CreateLineForm(forms.Form):
    name = forms.CharField(max_length=50,
                           widget=forms.TextInput(
                           attrs={'placeholder':'Name of Line (e.g Coffee Line)',
                                 'class': 'forms'}))
    information = forms.CharField(max_length=250,
                                  required = False,
                           widget=forms.TextInput(
                           attrs={'placeholder':'Information (e.g Please wait in line to get coffee)',
                                 'class': 'forms'}))
    instruction = forms.CharField(max_length=250,
                                  required=False,
                           widget=forms.TextInput(
                           attrs={'placeholder':'Instruction (e.g Please be available before you\'re third)',
                                 'class': 'forms'}))
        
    monday = forms.BooleanField(required=False)
    mo_o = forms.TimeField(required=False,
                           widget=forms.TimeInput(
                           attrs={'class': 'time',
                                 'placeholder':' HH:MM',
                                  'type':'time'
                                 }))
    
    mo_c = forms.TimeField(required=False,
                           widget=forms.TimeInput(
                           attrs={'class': 'time',
                                 'placeholder':' HH:MM',
                                  'type':'time'}))
    
    tuesday = forms.BooleanField(required=False)
    tu_o = forms.TimeField(required=False,
                           widget=forms.TimeInput(
                           attrs={'class': 'time',
                                 'placeholder':' HH:MM',
                                  'type':'time'
                                 }))
    
    
    tu_c = forms.TimeField(required=False,
                           widget=forms.TimeInput(
                           attrs={'class': 'time',
                                 'placeholder':' HH:MM',
                                  'type':'time'}))
    wednesday = forms.BooleanField(required=False)
    we_o = forms.TimeField(required=False,
                           widget=forms.TimeInput(
                           attrs={'class': 'time',
                                 'placeholder':' HH:MM',
                                  'type':'time'
                                 }))
    
    we_c = forms.TimeField(required=False,
                           widget=forms.TimeInput(
                           attrs={'class': 'time',
                                 'placeholder':' HH:MM',
                                  'type':'time'}))
    thursday = forms.BooleanField(required=False)
    th_o = forms.TimeField(required=False,
                           widget=forms.TimeInput(
                           attrs={'class': 'time',
                                 'placeholder':' HH:MM',
                                  'type':'time'
                                 }))
    
    th_c = forms.TimeField(required=False,
                           widget=forms.TimeInput(
                           attrs={'class': 'time',
                                 'placeholder':' HH:MM',
                                  'type':'time'}))
    friday = forms.BooleanField(required=False)
    fr_o = forms.TimeField(required=False,
                           widget=forms.TimeInput(
                           attrs={'class': 'time',
                                 'placeholder':' HH:MM',
                                  'type':'time'
                                 }))
    
    fr_c = forms.TimeField(required=False,
                           widget=forms.TimeInput(
                           attrs={'class': 'time',
                                 'placeholder':' HH:MM',
                                  'type':'time'}))
    saturday = forms.BooleanField(required=False)
    sa_o = forms.TimeField(required=False,
                           widget=forms.TimeInput(
                           attrs={'class': 'time',
                                 'placeholder':' HH:MM',
                                  'type':'time'
                                 }))
    
    sa_c = forms.TimeField(required=False,
                           widget=forms.TimeInput(
                           attrs={'class': 'time',
                                 'placeholder':' HH:MM',
                                  'type':'time'}))
    sunday = forms.BooleanField(required=False)
    su_o = forms.TimeField(required=False,
                           widget=forms.TimeInput(
                           attrs={'class': 'time',
                                 'placeholder':' HH:MM',
                                  'type':'time'
                                 }))
    
    su_c = forms.TimeField(required=False,
                           widget=forms.TimeInput(
                           attrs={'class': 'time',
                                 'placeholder':' HH:MM',
                                  'type':'time'}))


        
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CreateLineForm, self).__init__(*args, **kwargs)
    
    def clean_name(self):
        cd1 = self.cleaned_data.get('name')
        cd2 = slugify(cd1)
        try:
            self.user.BusinessProfile
            business = self.user.BusinessProfile
            all_associated_lines = Business_line.objects.filter(business=business) 
            for line in all_associated_lines:
                if cd2 == line.slug:
                    raise forms.ValidationError('Your business already has a line with this name')
        except ObjectDoesNotExist:
            pass
        return cd1
    
    
        

        

