import pyotp
from datetime import datetime, timedelta

def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'

def send_otp(request):
    #totp means time based one time password
    # totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    totp = pyotp.TOTP(pyotp.random_base32(), interval=120)
    
    otp = totp.now() # get one time password
    
    #store otp variable in session
    request.session['otp_secret_key'] = totp.secret
    
    valid_date = datetime.now() + timedelta(minutes=1)
    request.session['otp_valid_date'] = str(valid_date)
    
    print (f"your one-time-passord is: {otp}")
    