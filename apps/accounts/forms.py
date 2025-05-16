from django import forms
from django.contrib.auth.models import User
from .models import Profile, Address


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label="نام")
    last_name = forms.CharField(max_length=30, required=False, label="نام خانوادگی")
    email = forms.EmailField(required=False, label="ایمیل")
    
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'postal_code', 'city', 'avatar']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        
        # Update user fields
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()
        
        if commit:
            profile.save()
        
        return profile


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'title', 'recipient_name', 'phone', 'address', 'postal_code', 
            'city', 'address_type', 'is_default'
        ]