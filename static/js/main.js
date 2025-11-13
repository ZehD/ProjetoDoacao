// Funções utilitárias JavaScript

// Fechar mensagens flash automaticamente após 5 segundos
document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });
});

// Validação de formulários
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;

    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.style.borderColor = '#f44336';
        } else {
            field.style.borderColor = '';
        }
    });

    return isValid;
}

// Formatação de números
function formatNumber(num, decimals = 2) {
    return parseFloat(num).toFixed(decimals);
}

// Confirmação antes de ações destrutivas
function confirmAction(message) {
    return confirm(message || 'Tem certeza que deseja continuar?');
}
