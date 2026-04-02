from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Involucrado, Logro, Riesgo, Costo, RolResponsabilidad, ReunionDocumento

# Custom validators

def validate_positive(value):
    if value <= 0:
        raise ValidationError('Value must be greater than zero.')


class InvolucradoForm(forms.ModelForm):
    class Meta:
        model = Involucrado
        fields = '__all__'


class LogroForm(forms.ModelForm):
    class Meta:
        model = Logro
        fields = '__all__'


class RiesgoForm(forms.ModelForm):
    class Meta:
        model = Riesgo
        fields = '__all__'


class CostoForm(forms.ModelForm):
    cost = forms.DecimalField(validators=[validate_positive])
    class Meta:
        model = Costo
        fields = '__all__'


class RolResponsabilidadForm(forms.ModelForm):
    class Meta:
        model = RolResponsabilidad
        fields = '__all__'


class ReunionDocumentoForm(forms.ModelForm):
    date = forms.DateField(initial=timezone.now)  # DateField for dates
    class Meta:
        model = ReunionDocumento
        fields = '__all__'


class StrongPasswordField(forms.CharField):
    def clean(self, value):
        super().clean(value)
        if len(value) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        if not any(char.isdigit() for char in value):
            raise ValidationError('Password must contain at least one digit.')
        if not any(char.isalpha() for char in value):
            raise ValidationError('Password must contain at least one letter.')
        return value


class CustomUserCreationForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = StrongPasswordField()
    confirm_password = StrongPasswordField()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError('Passwords do not match.')

        return cleaned_data
