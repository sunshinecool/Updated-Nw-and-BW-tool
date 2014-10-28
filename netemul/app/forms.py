from django import forms
#from app.models import blog
from app.models import UserProfile
from app.models import PcDetails
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class form(forms.Form):
	username = forms.CharField(max_length=30)
	password = forms.CharField(widget=forms.PasswordInput())
        
        #class Meta:
            #model = User
            #fields = ('username','password')
    
#class PostForm(form.ModelForm)
#	title=forms.CharField()
#	body=forms.TextInput()
#	
#	class Meta:
#		model=Blog
#		fields=['title','body']



class UserForm(UserCreationForm):
    #password = forms.CharField(widget=forms.PasswordInput())
    CHOICES = (('1', 'Tester',), ('2', 'Analyzer',))
    Group = forms.ChoiceField(widget=forms.RadioSelect,choices=CHOICES)

    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email', 'password1','password2')
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email is already used")
        return data

class PcForm(forms.ModelForm):
	class Meta:
		model = PcDetails
		fields=['pc_name','pc_user','pc_ip','pc_password','pc_os']
