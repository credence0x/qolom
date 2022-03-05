import math
from django.conf import settings

def rounder(num, decimals=0):
    """
    round "num" to "decimal" decimal places 
    """
    multiplier = 10 ** decimals
    return math.floor(num*multiplier + 0.5) / multiplier
        

def get_fees(total):
    fees = (settings.ORDERING_FEES * total)
    fees = rounder(fees,2) # round fees to 2 decimal places
        
    if total > 2500:
        # additional N100 if take out is more than 2,500
        fees += 100
        
    # we collect not more than N2,500 in fees
    fees = min(fees,2500.0)
    