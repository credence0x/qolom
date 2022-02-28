from django.utils import timezone
import datetime,ast
from django.core.exceptions import ObjectDoesNotExist
from .forms import SearchForm
from django.utils import timezone
from dateutil.parser import parse
from datetime import timedelta

def get_business(request):
    try:
        business_real = request.user.BusinessProfile
    except Exception:
        business_real = False
    return {
        'business_real': business_real
    }

def special_line(request):
    try:
        special_line = request.user.UserProfile.admin_special_line
        
    except Exception:
        special_line = False
    return {
        'special_line': special_line
    }
def ready_order(request):
    try:
        UserProfile = request.user.UserProfile
        card_information = ast.literal_eval(UserProfile.card_information)
        perma_form = SearchForm()

        loc_time = request.session.get('loc_time',False)
        if loc_time:
            time = timezone.now()- parse(request.session['loc_time'])
            if time > timedelta(seconds=3600):
                request.session['allow']=True
            else:
                request.session['allow']=False
        else:
            request.session['allow']=True
        
        
    except Exception:
        perma_form = False
        order_sent = False
        order_ready = False
        order_ready_exists = False
        more_than_one = False
        first_order_url = False
        UserProfile = False
        return {
        'order_sent': order_sent,
        'order_ready':order_ready,
        'order_ready_exists':order_ready_exists,
        'more_than_one': more_than_one,
        'first_order_url':first_order_url,
        'card_info':False,
        'perma_form':perma_form,
        'UserProfile':UserProfile
        
    }


    minus = timezone.now()- datetime.timedelta(days=3)  
    order_sent = UserProfile.all_orders.filter(is_active=True,
                                                    order_status='SENT',
                                                    created__gte=minus)
    order_ready = UserProfile.all_orders.filter(is_active=True,
                                                    order_status='READY',
                                                    created__gte=minus,
                                                    has_seen_notification=False
                                                    )
    order_ready_exists=order_ready.exists()
    more_than_one = False
    first_order_url = False
    if order_ready_exists:
        if len(order_ready)>1:
            more_than_one = True 
        else:
            first_order_url = order_ready[0].id
        
        
        
    
        
    return {
        'order_sent': order_sent,
        'order_ready':order_ready,
        'order_ready_exists':order_ready_exists,
        'more_than_one': more_than_one,
        'first_order_url':first_order_url,
        'card_info':card_information,
        'perma_form':perma_form,
        'UserProfile':UserProfile
        
    }
    
