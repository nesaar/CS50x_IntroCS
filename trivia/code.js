document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.btn').addEventListener('OnClick', function(e) {
        alert('hello, ');
        e.preventDefault();
    });
});