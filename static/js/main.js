/**
 * AI Urban Design Planner - JavaScript principal
 */

// Message d'alerte auto-hide
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide des alertes après 5 secondes
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        // Ne pas auto-hide les alertes de danger
        if (!alert.classList.contains('alert-danger')) {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });
    
    // Confirmation avant suppression
    const deleteButtons = document.querySelectorAll('a[href*="/supprimer/"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Êtes-vous sûr de vouloir supprimer ce projet ?')) {
                e.preventDefault();
            }
        });
    });
});

// Fonction pour copier le prompt dans le presse-papiers
function copyToClipboard(text, buttonElement) {
    navigator.clipboard.writeText(text).then(() => {
        const originalText = buttonElement.innerHTML;
        buttonElement.innerHTML = '<i class="bi bi-check"></i> Copié!';
        setTimeout(() => {
            buttonElement.innerHTML = originalText;
        }, 2000);
    }).catch(() => {
        alert('Erreur lors de la copie');
    });
}

// Format des nombres
function formatNumber(num) {
    return new Intl.NumberFormat('fr-FR').format(num);
}

// Validation des formulaires Bootstrap
(function() {
    'use strict';
    window.addEventListener('load', function() {
        var forms = document.querySelectorAll('.needs-validation');
        var validation = Array.prototype.filter.call(forms, function(form) {
            form.addEventListener('submit', function(event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);
})();
