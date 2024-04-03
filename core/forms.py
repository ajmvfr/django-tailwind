from django import forms

class LoginForm(forms.Form):
    # username = forms.CharField(label="Username", max_length=100)
    email = forms.EmailField(label="E-mail", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    
    
    
# class OTPForm(forms.Form):
#     otp = forms.CharField(label="OTP", max_length=6)
    

class OTPForm(forms.Form):
    otp = forms.CharField(label="OTP", max_length=6)
    