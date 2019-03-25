from django import forms
from registration.forms import RegistrationForm

# class PasswordChangeCustomForm(PasswordChangeForm):
#     def __init__(self, user, *args, **kwargs):
#         super(forms.PasswordChangeForm, self).__init__(user,*args, **kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs['class'] = 'form-control'

class UserCreationCustomForm(RegistrationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationCustomForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'