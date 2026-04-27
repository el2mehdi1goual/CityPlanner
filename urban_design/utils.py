"""
Utilitaires pour la génération de propositions d'aménagement urbain
"""
import math

def generer_proposition_amenagement(projet):
    """
    Génère une proposition d'aménagement basée sur les paramètres du projet
    
    Args:
        projet: Instance de ProjetUrbain
    
    Returns:
        dict: Dictionnaire contenant les détails de la proposition
    """
    
    # Calcul des paramètres de base
    nombre_logements = projet.nombre_familles
    population_totale = projet.population_totale
    
    # Calcul du nombre d'équipements selon les règles
    nombre_ecoles = max(1, math.ceil(population_totale / 500))
    nombre_centres_sante = max(1, math.ceil(population_totale / 1000))
    nombre_marches = max(1, math.ceil(population_totale / 800))
    
    # Calcul de la surface des espaces verts selon la priorité
    if projet.priorite == 'espaces_verts':
        pourcentage_espaces_verts = 0.15
    elif projet.priorite == 'équilibré':
        pourcentage_espaces_verts = 0.10
    else:  # logements ou services_publics
        pourcentage_espaces_verts = 0.07
    
    surface_espaces_verts = projet.surface_terrain * pourcentage_espaces_verts
    
    # Surface des routes
    surface_routes = projet.surface_terrain * 0.20
    
    # Génération de la description textuelle
    description = generer_description_proposition(
        projet,
        nombre_logements,
        population_totale,
        nombre_ecoles,
        nombre_centres_sante,
        nombre_marches,
        surface_espaces_verts,
        surface_routes
    )
    
    return {
        'nombre_logements': nombre_logements,
        'nombre_ecoles': nombre_ecoles,
        'nombre_centres_sante': nombre_centres_sante,
        'nombre_marches': nombre_marches,
        'surface_espaces_verts': round(surface_espaces_verts, 2),
        'surface_routes': round(surface_routes, 2),
        'description': description,
    }


def generer_description_proposition(projet, logements, population, ecoles, centres_sante, marches, espaces_verts, routes):
    """
    Génère une description textuelle claire de la proposition
    
    Args:
        projet: Instance de ProjetUrbain
        logements: Nombre de logements
        population: Population totale estimée
        ecoles: Nombre d'écoles
        centres_sante: Nombre de centres de santé
        marches: Nombre de marchés
        espaces_verts: Surface des espaces verts
        routes: Surface des routes
    
    Returns:
        str: Description formatée
    """
    
    priorite_texte = dict(projet._meta.get_field('priorite').choices).get(projet.priorite)
    budget_texte = dict(projet._meta.get_field('niveau_budget').choices).get(projet.niveau_budget)
    
    description = f"""
PROPOSITION D'AMÉNAGEMENT URBAIN
{'=' * 50}

Projet: {projet.titre}
Date de création: {projet.date_creation.strftime('%d/%m/%Y')}

CARACTÉRISTIQUES DU PROJET:
- Nombre de familles: {projet.nombre_familles}
- Taille moyenne des familles: {projet.taille_moyenne_famille} personnes
- Population estimée: {population} habitants
- Superficie du terrain: {projet.surface_terrain} hectares
- Niveau de budget: {budget_texte}
- Priorité d'aménagement: {priorite_texte}

PROPOSITION D'AMÉNAGEMENT:
- Nombre de logements: {logements} unités
- Nombre d'écoles: {ecoles}
- Nombre de centres de santé: {centres_sante}
- Nombre de marchés: {marches}
- Surface des espaces verts: {espaces_verts} hectares ({(espaces_verts/projet.surface_terrain)*100:.1f}% du terrain)
- Surface des routes: {routes} hectares ({(routes/projet.surface_terrain)*100:.1f}% du terrain)

RECOMMANDATIONS:
- Cette proposition respecte les standards internationaux de planification urbaine
- Les équipements publics sont dimensionnés selon les normes (1 école/500 hab., 1 centre de santé/1000 hab., 1 marché/800 hab.)
- La priorité "{priorite_texte}" a été prise en compte dans la répartition des espaces
- Cette proposition requiert un budget "{budget_texte}" pour la mise en œuvre
- Les espaces verts couvrent une part importante du terrain pour assurer la qualité de vie

PROCHAINES ÉTAPES:
1. Valider cette proposition avec les parties prenantes
2. Générer une visualisation graphique du quartier
3. Élaborer un plan détaillé de mise en œuvre
4. Évaluer l'impact environnemental et social
"""
    
    return description.strip()


def generer_prompt_image(proposition):
    """
    Génère un prompt textuel pour une API de génération d'images basé sur la proposition
    
    Args:
        proposition: Instance de PropositionAmenagement
    
    Returns:
        str: Prompt prêt pour une API d'image (ex: Midjourney, DALL-E, Stable Diffusion)
    """
    
    projet = proposition.projet
    
    prompt = f"""Generate a realistic top-view urban neighborhood master plan for {proposition.nombre_logements} families 
({proposition.nombre_logements * projet.taille_moyenne_famille} people total), including:
- {proposition.nombre_logements} residential housing blocks with varied architecture
- {proposition.nombre_ecoles} school building(s) with playground areas
- {proposition.nombre_centres_sante} health center(s)
- {proposition.nombre_marches} local market area(s)
- {proposition.surface_espaces_verts:.1f} hectares of green spaces with parks, trees, and recreational areas
- Well-planned road network with {proposition.surface_routes:.1f} hectares of streets and pathways
- Public gathering spaces and community centers
- Sustainable design with modern infrastructure
- Organized, human-centered urban layout
- Natural lighting and ventilation
- Professional urban planning style, high detail, 4K quality"""
    
    return prompt.strip()
