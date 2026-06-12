function toggleMenu() {
  document.getElementById('mobileMenu').classList.toggle('open');
}

// Auto-dismiss flash messages after 4 seconds
document.querySelectorAll('.flash').forEach(el => {
  setTimeout(() => el.remove(), 4000);
});

// Smooth scroll to comments
document.querySelectorAll('a[href="#comments"]').forEach(a => {
  a.addEventListener('click', e => {
    e.preventDefault();
    document.getElementById('comments')?.scrollIntoView({ behavior: 'smooth' });
  });
});
