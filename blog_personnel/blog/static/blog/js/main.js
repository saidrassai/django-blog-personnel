// Main JavaScript file for the blog application

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Add active class to current nav item
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (href === '/' && currentPath === '/')) {
            link.classList.add('active');
        }
    });

    // Add form validation styling
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });

    // Enhance textareas for article content (if applicable)
    const contentTextarea = document.getElementById('id_content');
    if (contentTextarea) {
        contentTextarea.setAttribute('rows', '10');
        contentTextarea.classList.add('content-editor');
    }
});

// Function to confirm deletion
function confirmDelete(event) {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cet élément ?')) {
        event.preventDefault();
    }
}

// Attach confirm delete to delete buttons
document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('a[href*="delete"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', confirmDelete);
    });
});