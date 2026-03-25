// ─── Theme Toggle ─────────────────────────────────────────────────────────────
(function () {
  const KEY = 'urbanstore-theme';
  const saved = localStorage.getItem(KEY);
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const theme = saved || (prefersDark ? 'dark' : 'light');
  document.documentElement.setAttribute('data-theme', theme);
})();

document.addEventListener('DOMContentLoaded', function () {
  // Apply saved theme to body too
  const KEY = 'urbanstore-theme';
  const current = document.documentElement.getAttribute('data-theme') || 'light';
  document.body.setAttribute('data-theme', current);

  // Theme toggle button
  const toggleBtn = document.getElementById('themeToggle');
  if (toggleBtn) {
    updateToggleIcon(current, toggleBtn);
    toggleBtn.addEventListener('click', function () {
      const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
      const next = isDark ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      document.body.setAttribute('data-theme', next);
      localStorage.setItem(KEY, next);
      updateToggleIcon(next, toggleBtn);
    });
  }

  // Mobile nav
  const navToggle = document.getElementById('navToggle');
  const navMenu = document.querySelector('.nav-menu');
  if (navToggle && navMenu) {
    navToggle.addEventListener('click', function () {
      navMenu.classList.toggle('open');
    });
    document.addEventListener('click', function (e) {
      if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
        navMenu.classList.remove('open');
      }
    });
  }

  // Auto-dismiss alerts after 5s
  document.querySelectorAll('.alert').forEach(function (alert) {
    setTimeout(function () {
      alert.style.transition = 'opacity 0.4s, transform 0.4s';
      alert.style.opacity = '0';
      alert.style.transform = 'translateX(20px)';
      setTimeout(function () { alert.remove(); }, 400);
    }, 5000);
  });

  // Lazy load images (Intersection Observer)
  if ('IntersectionObserver' in window) {
    const imgs = document.querySelectorAll('img[data-src]');
    const obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.src = e.target.dataset.src;
          obs.unobserve(e.target);
        }
      });
    }, { rootMargin: '200px' });
    imgs.forEach(function (img) { obs.observe(img); });
  }

  // Filter form auto-submit on select change
  const filtroForm = document.getElementById('filtroForm');
  if (filtroForm) {
    filtroForm.querySelectorAll('select').forEach(function (sel) {
      sel.addEventListener('change', function () { filtroForm.submit(); });
    });
  }

  // Produto form image preview
  const urlInput = document.querySelector('input[name="imagem_url"]');
  if (urlInput) {
    const preview = document.getElementById('imgPreview');
    const previewWrap = document.getElementById('imgPreviewWrap');
    if (preview && previewWrap) {
      if (urlInput.value) {
        preview.src = urlInput.value;
        previewWrap.style.display = 'block';
      }
      let debounce;
      urlInput.addEventListener('input', function () {
        clearTimeout(debounce);
        debounce = setTimeout(function () {
          const url = urlInput.value.trim();
          if (url) {
            preview.src = url;
            previewWrap.style.display = 'block';
            preview.onerror = function () { previewWrap.style.display = 'none'; };
          } else {
            previewWrap.style.display = 'none';
          }
        }, 400);
      });
    }
  }
});

function updateToggleIcon(theme, btn) {
  btn.textContent = theme === 'dark' ? '☀️' : '🌙';
  btn.title = theme === 'dark' ? 'Mudar para modo claro' : 'Mudar para modo escuro';
}
