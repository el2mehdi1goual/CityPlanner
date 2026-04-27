from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import ProjetUrbain, PropositionAmenagement, ImageGeneree, HistoriqueProjet
from .forms import ProjetUrbainForm, RegisterForm, LoginForm
from .utils import generer_proposition_amenagement, generer_prompt_image


# ===== VUE AUTHENTIFICATION =====

def register_view(request):
    """Vue d'inscription"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Ce nom d\'utilisateur est déjà pris')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                login(request, user)
                return redirect('dashboard')
    else:
        form = RegisterForm()
    
    return render(request, 'urban_design/register.html', {'form': form})


def login_view(request):
    """Vue de connexion"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, 'Identifiants invalides')
    else:
        form = LoginForm()
    
    return render(request, 'urban_design/login.html', {'form': form})


def logout_view(request):
    """Vue de déconnexion"""
    logout(request)
    return redirect('login')


# ===== VUE DASHBOARD =====

@login_required(login_url='login')
def dashboard_view(request):
    """Vue du tableau de bord"""
    user = request.user
    
    # Récupération des statistiques
    total_projets = ProjetUrbain.objects.filter(utilisateur=user).count()
    total_propositions = PropositionAmenagement.objects.filter(
        projet__utilisateur=user
    ).count()
    
    # Les 5 derniers projets
    derniers_projets = ProjetUrbain.objects.filter(utilisateur=user)[:5]
    
    context = {
        'total_projets': total_projets,
        'total_propositions': total_propositions,
        'derniers_projets': derniers_projets,
    }
    
    return render(request, 'urban_design/dashboard.html', context)


# ===== VUES PROJETS =====

@login_required(login_url='login')
def projet_list_view(request):
    """Affiche la liste des projets de l'utilisateur"""
    projets = ProjetUrbain.objects.filter(utilisateur=request.user)
    return render(request, 'urban_design/projet_list.html', {'projets': projets})


@login_required(login_url='login')
def projet_create_view(request):
    """Crée un nouveau projet"""
    if request.method == 'POST':
        form = ProjetUrbainForm(request.POST)
        if form.is_valid():
            projet = form.save(commit=False)
            projet.utilisateur = request.user
            projet.save()
            
            # Ajouter une entrée dans l'historique
            HistoriqueProjet.objects.create(
                projet=projet,
                action='creation',
                description=f'Projet "{projet.titre}" créé'
            )
            
            return redirect('projet_detail', pk=projet.pk)
    else:
        form = ProjetUrbainForm()
    
    return render(request, 'urban_design/projet_form.html', {'form': form, 'titre': 'Créer un nouveau projet'})


@login_required(login_url='login')
def projet_detail_view(request, pk):
    """Affiche les détails d'un projet"""
    projet = get_object_or_404(ProjetUrbain, pk=pk, utilisateur=request.user)
    proposition = PropositionAmenagement.objects.filter(projet=projet).first()
    images = ImageGeneree.objects.filter(projet=projet)
    historique = HistoriqueProjet.objects.filter(projet=projet)
    
    context = {
        'projet': projet,
        'proposition': proposition,
        'images': images,
        'historique': historique,
    }
    
    return render(request, 'urban_design/projet_detail.html', context)


@login_required(login_url='login')
def projet_update_view(request, pk):
    """Met à jour un projet"""
    projet = get_object_or_404(ProjetUrbain, pk=pk, utilisateur=request.user)
    
    if request.method == 'POST':
        form = ProjetUrbainForm(request.POST, instance=projet)
        if form.is_valid():
            projet = form.save()
            
            # Ajouter une entrée dans l'historique
            HistoriqueProjet.objects.create(
                projet=projet,
                action='modification',
                description=f'Projet "{projet.titre}" modifié'
            )
            
            return redirect('projet_detail', pk=projet.pk)
    else:
        form = ProjetUrbainForm(instance=projet)
    
    return render(request, 'urban_design/projet_form.html', {'form': form, 'titre': 'Modifier le projet', 'projet': projet})


@login_required(login_url='login')
def projet_delete_view(request, pk):
    """Supprime un projet"""
    projet = get_object_or_404(ProjetUrbain, pk=pk, utilisateur=request.user)
    
    if request.method == 'POST':
        # Ajouter une entrée dans l'historique avant suppression
        titre_projet = projet.titre
        HistoriqueProjet.objects.create(
            projet=projet,
            action='suppression',
            description=f'Projet "{titre_projet}" supprimé'
        )
        projet.delete()
        return redirect('projet_list')
    
    return render(request, 'urban_design/confirm_delete.html', {'projet': projet})


# ===== VUES GÉNÉRATION DE PROPOSITION =====

@login_required(login_url='login')
@require_http_methods(["POST"])
def generer_proposition_view(request, pk):
    """Génère ou regénère une proposition d'aménagement"""
    projet = get_object_or_404(ProjetUrbain, pk=pk, utilisateur=request.user)
    
    # Générer la proposition
    donnees_proposition = generer_proposition_amenagement(projet)
    
    # Vérifier si une proposition existe déjà
    proposition = PropositionAmenagement.objects.filter(projet=projet).first()
    
    if proposition:
        # Regénérer la proposition existante
        proposition.nombre_logements = donnees_proposition['nombre_logements']
        proposition.nombre_ecoles = donnees_proposition['nombre_ecoles']
        proposition.nombre_centres_sante = donnees_proposition['nombre_centres_sante']
        proposition.nombre_marches = donnees_proposition['nombre_marches']
        proposition.surface_espaces_verts = donnees_proposition['surface_espaces_verts']
        proposition.surface_routes = donnees_proposition['surface_routes']
        proposition.description = donnees_proposition['description']
        proposition.save()
        
        action = 'proposition_regeneree'
        message = 'Proposition regénérée avec succès'
    else:
        # Créer une nouvelle proposition
        proposition = PropositionAmenagement.objects.create(
            projet=projet,
            **donnees_proposition
        )
        
        action = 'proposition_generee'
        message = 'Proposition générée avec succès'
    
    # Ajouter une entrée dans l'historique
    HistoriqueProjet.objects.create(
        projet=projet,
        action=action,
        description=f'{dict(HistoriqueProjet._meta.get_field("action").choices).get(action)}'
    )
    
    return redirect('projet_detail', pk=projet.pk)


# ===== VUES GÉNÉRATION DE PROMPT IMAGE =====

@login_required(login_url='login')
@require_http_methods(["POST"])
def generer_prompt_image_view(request, pk):
    """Génère un prompt pour une image"""
    projet = get_object_or_404(ProjetUrbain, pk=pk, utilisateur=request.user)
    
    # Vérifier qu'une proposition existe
    proposition = PropositionAmenagement.objects.filter(projet=projet).first()
    if not proposition:
        # Générer une proposition d'abord
        donnees_proposition = generer_proposition_amenagement(projet)
        proposition = PropositionAmenagement.objects.create(
            projet=projet,
            **donnees_proposition
        )
        
        HistoriqueProjet.objects.create(
            projet=projet,
            action='proposition_generee',
            description='Proposition générée automatiquement'
        )
    
    # Générer le prompt
    prompt = generer_prompt_image(proposition)
    
    # Sauvegarder l'image générée
    image = ImageGeneree.objects.create(
        projet=projet,
        prompt=prompt
    )
    
    # Ajouter une entrée dans l'historique
    HistoriqueProjet.objects.create(
        projet=projet,
        action='prompt_genere',
        description='Prompt image généré'
    )
    
    return redirect('projet_detail', pk=projet.pk)


# ===== PAGE ERREUR =====

def page_not_found_view(request, exception):
    """Vue pour les pages non trouvées"""
    return render(request, 'urban_design/404.html', status=404)


def server_error_view(request):
    """Vue pour les erreurs serveur"""
    return render(request, 'urban_design/500.html', status=500)
