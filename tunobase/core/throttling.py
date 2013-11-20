'''
Created on 12 Nov 2013

@author: michael
'''
from django.utils import timezone, dateparse

def add_to_throttle(request, throttle_key, timestamp):
    if throttle_key in request.session:
        old_session = request.session[throttle_key]
        old_session.append(timestamp.strftime('%Y-%m-%d %H:%M:%S'))
        request.session[throttle_key] = old_session
    else:
        request.session[throttle_key] = [timestamp.strftime('%Y-%m-%d %H:%M:%S')]
        
def check_throttle_exists(request, throttle_key):
    return throttle_key in request.session
        
def check_throttle(request, throttle_key, lockout_duration,
                   num_allowed_in_lockout):
    try:
        oldest_timestamp = timezone.make_aware(
            dateparse.parse_datetime(request.session[throttle_key][-num_allowed_in_lockout]),
            timezone.utc
        )
        return oldest_timestamp > (timezone.now() - lockout_duration)
    except IndexError:
        pass
        
    return False