from django import forms
from django.contrib.auth.models import User
from .models import ProjetUrbain


class RegisterForm(forms.Form):
    """Formulaire d'inscription"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom d\'utilisateur'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmer le mot de passe'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password != password_confirm:
            raise forms.ValidationError('Les mots de passe ne correspondent pas')
        
        return cleaned_data


class LoginForm(forms.Form):
    """Formulaire de connexion"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom d\'utilisateur'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
    )


class ProjetUrbainForm(forms.ModelForm):
    """Formulaire pour créer/modifier un projet urbain"""
    
    class Meta:
        model = ProjetUrbain
        fields = ['titre', 'description', 'nombre_familles', 'taille_moyenne_famille', 
                  'surface_terrain', 'niveau_budget', 'priorite']
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre du projet'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description du projet (optionnel)',
                'rows': 3
            }),
            'nombre_familles': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de familles',
                'min': '1'
            }),
            'taille_moyenne_famille': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Taille moyenne des familles',
                'min': '1'
            }),
            'surface_terrain': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Superficie du terrain (hectares)',
                'min': '0.1',
                'step': '0.1'
            }),
            'niveau_budget': forms.Select(attrs={
                'class': 'form-select'
            }),
            'priorite': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        labels = {
            'titre': 'Titre du projet',
            'description': 'Description',
            'nombre_familles': 'Nombre de familles',
            'taille_moyenne_famille': 'Taille moyenne des familles',
            'surface_terrain': 'Superficie du terrain (hectares)',
            'niveau_budget': 'Niveau du budget',
            'priorite': 'Priorité d\'aménagement'
        }
