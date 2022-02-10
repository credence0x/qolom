import django.dispatch


line_changed = django.dispatch.Signal(providing_args=["line_uniquefield"])
notify = django.dispatch.Signal(providing_args=["key","collected",'request'])
notify_business= django.dispatch.Signal(providing_args=["business"])
confirm_bank  = django.dispatch.Signal(providing_args=['user','request'])
