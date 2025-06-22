// PDF to Markdown Web Interface Scripts

document.addEventListener('DOMContentLoaded', function() {
    // Toggle configuration form
    const configToggle = document.getElementById('config-toggle');
    const configForm = document.getElementById('config-form');

    if (configToggle && configForm) {
        configToggle.addEventListener('click', function() {
            configForm.classList.toggle('show');
            configToggle.textContent = configForm.classList.contains('show') 
                ? 'Hide Advanced Configuration' 
                : 'Show Advanced Configuration';
        });
    }

    // Form validation
    const convertForm = document.getElementById('convert-form');
    if (convertForm) {
        convertForm.addEventListener('submit', function(event) {
            const fileInput = document.getElementById('pdf-file');
            if (fileInput && fileInput.files.length === 0) {
                event.preventDefault();
                showAlert('Please select a PDF file to convert.', 'error');
            }
        });
    }

    // Alert messages
    function showAlert(message, type) {
        const alertContainer = document.getElementById('alert-container');
        if (!alertContainer) return;

        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.textContent = message;

        alertContainer.innerHTML = '';
        alertContainer.appendChild(alertDiv);

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }

    // Handle URL parameters for alerts
    const urlParams = new URLSearchParams(window.location.search);
    const success = urlParams.get('success');
    const error = urlParams.get('error');

    if (success) {
        showAlert(decodeURIComponent(success), 'success');
    } else if (error) {
        showAlert(decodeURIComponent(error), 'error');
    }
});
