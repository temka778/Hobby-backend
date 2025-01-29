from django import forms
from .models import CustomUser

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = "__all__"

    def clean_username(self):
        """Преобразуем None в пустую строку"""
        username = self.cleaned_data.get("username", "")
        return username or ""
