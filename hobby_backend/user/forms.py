from django import forms
from .models import CustomUser

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = "__all__"

    def clean_username(self):
        username = self.cleaned_data.get("username", None)
        if username:  # Проверяем, что username не None
            username = username.strip()
            if CustomUser.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Пользователь с таким username уже существует.")
        return username  # Возвращаем None, если пусто

