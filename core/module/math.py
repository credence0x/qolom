import math
from django.conf import settings

def rounder(num, decimals=0):
    """
    round "num" to "decimal" decimal places 
    """
    multiplier = 10 ** decimals
    return math.floor(num*multiplier + 0.5) / multiplier
        

def get_fees(total):
    assert total > 0 
    fees = (settings.ORDERING_FEES * total)
    fees = rounder(fees,2) # round fees to 2 decimal places
        
    if total > 2500:
        # additional N100 if take out is more than 2,500
        fees += 100
        
    # we collect not more than N2,500 in fees
    fees = min(fees,2500.0)
    return fees

def safe_total(old_total):
    "Converts value (Naira) to kobo equivalent"
    assert old_total > 0 
    kobo = 100
    total = old_total * kobo
    assert ((total> old_total))
    return total
    