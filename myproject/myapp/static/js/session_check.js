document.addEventListener('DOMContentLoaded', function () {
    const user = localStorage.getItem('user');

    if (!user) {
        if (window.location.pathname.includes('/myapp')) {
            window.location = '/';
        }
    } else {
        if (!window.location.pathname.includes('/myapp')) {
            window.location = '/myapp';
        }
    }

});