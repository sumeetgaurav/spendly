// main.js — students will add JavaScript here as features are built

document.addEventListener('DOMContentLoaded', function () {
    var modal = document.getElementById('how-it-works-modal');
    var openBtn = document.getElementById('how-it-works-btn');
    var iframe = document.getElementById('how-it-works-iframe');

    if (!modal || !openBtn || !iframe) return;

    function openModal() {
        iframe.src = iframe.getAttribute('data-src') + '?autoplay=1';
        modal.classList.add('is-open');
        document.body.classList.add('modal-open');
    }

    function closeModal() {
        modal.classList.remove('is-open');
        document.body.classList.remove('modal-open');
        iframe.src = '';
    }

    openBtn.addEventListener('click', openModal);

    modal.querySelectorAll('[data-modal-close]').forEach(function (el) {
        el.addEventListener('click', closeModal);
    });
});
