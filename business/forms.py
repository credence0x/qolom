from django import forms
from business.models import BusinessQueue
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist

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

def get_choice():        
    ALL_CHOICES = []
    a = 1000
    c = 1 
    for x in range(a):
        ALL_CHOICES.append((str(c),str(c)))
        c += 1
    return ALL_CHOICES

class BusinessMenuForm(forms.Form):                           
    name            = forms.CharField(max_length=250,
                                  
                                  widget=forms.TextInput(
                                      attrs={'placeholder':'Name',
                                             'class':'pp'}))
    
    price           = forms.IntegerField(
                                  label='Price (NGN)',
                                  widget=forms.NumberInput(
                                      attrs={'placeholder':'Price Per Unit (NGN)',
                                             'class':'pp',
                                             'min':1}))
    
    units_available = forms.ChoiceField(choices = get_choice(),
                                        widget=forms.Select(
                                      attrs={
                                             'class':'pp'}))



class RefundForm(forms.Form):                           
    password    = forms.CharField(max_length=250,
                                  widget=forms.PasswordInput(
                                      attrs={'placeholder':'password',
                                             'class':'forms'}))
    
    
BANK_CHOICES = [
('044', 'Access Bank '),
('035',	'ALAT by Wema'),
('023', 'Citibank Nigeria'),
('063' ,'Diamond Bank Plc'),
('050' ,'Ecobank Nigeria'),
('084' ,'Enterprise Bank Plc'),
('070' ,'Fidelity Bank Plc'),
('011',	'First Bank of Nigeria Plc'),
('214',	'First City Monument Bank ( FCMB )'),
('058',	'Guaranty Trust Bank Plc'),
('030',	'Heritage Banking Company Ltd'),
('082',	'Keystone Bank Ltd'),
('014', 'Mainstreet Bank '),
('076',	'Skye Bank Plc'),
('221',	'Stanbic IBTC Plc'),
('068', 'Standard Chartered Bank'),
('232',	'Sterling Bank Plc'),#check
('032',	'Union Bank Nigeria Plc'),
('033',	'United Bank for Africa Plc'),
('215',	'Unity Bank Plc'),
('035',	'WEMA Bank Plc'),
('057',	'Zenith Bank '),
]
class BankForm(forms.Form):                           
    account_number   = forms.CharField(max_length=250,
                          label='Account Number',
                          widget=forms.TextInput(
                              attrs={'placeholder':'',
                                     'class':'forms'}))
    
    bank = forms.ChoiceField(choices = BANK_CHOICES,
                             widget=forms.Select(
                              attrs={
                                     'class':'forms'}))
    
    




class LineForm(forms.Form):
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
                           attrs={
                               'placeholder':'Instruction (e.g Please be available before you\'re third)',
                                 'class': 'forms'}))
    

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(LineForm, self).__init__(*args, **kwargs)
    
    def clean_name(self):
        cd1 = self.cleaned_data.get('name')
        cd2 = slugify(cd1)
        try:
            self.user.business_signup
            business = self.user.business_signup
            all_associated_lines = Business_line.objects.filter(business=business) 
            for line in all_associated_lines:
                if cd2 == line.slug:
                    raise forms.ValidationError('Your business already has a line with this name')
        except ObjectDoesNotExist:
            pass
        return cd1


    
        
class RemoveForm(forms.Form):
    remove = forms.CharField(max_length=250,
                             widget=forms.HiddenInput(
                           attrs={'id': 'remove'}))
    
class JoinLineForm(forms.Form):
    join = forms.CharField(max_length=250,
                           widget=forms.HiddenInput(
                               attrs={'id': 'join'}))
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
        
    def __init__(self, user, line, *args, **kwargs):
        self.user = user
        self.this_line = line
        super(EditLineForm, self).__init__(*args, **kwargs)
    
    def clean_name(self):
        cd1 = self.cleaned_data.get('name')
        cd2 = slugify(cd1)
        try:
            self.user.business_signup
            business = self.user.business_signup
            all_associated_lines = Business_line.objects.filter(business=business) 
            for line in all_associated_lines:
                if cd2 == line.slug and line != self.this_line :
                    raise forms.ValidationError('Your business already has a line with this name')
        except ObjectDoesNotExist:
            pass
        return cd1
    
    
        

        
class DaysOpenForm(forms.Form):
    
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
    
    
    
    
    
    
    
        

        

    

















    
    
