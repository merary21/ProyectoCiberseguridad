/* ============================================================
   auth.js - Interactividad de las páginas de login y registro
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

    // Mostrar / ocultar contraseña
    document.querySelectorAll('.input-toggle').forEach((btn) => {
        btn.addEventListener('click', () => {
            const input = document.getElementById(btn.getAttribute('data-target'));
            if (!input) return;

            const mostrando = input.type === 'text';
            input.type = mostrando ? 'password' : 'text';
            btn.classList.toggle('is-visible', !mostrando);
            btn.setAttribute('aria-label', mostrando ? 'Mostrar contraseña' : 'Ocultar contraseña');
        });
    });

    // Medidor de fuerza de contraseña
    const passwordInput = document.getElementById('password');
    const strengthBox = document.getElementById('passwordStrength');

    if (passwordInput && strengthBox) {
        const bars = strengthBox.querySelectorAll('.strength-bars span');
        const label = strengthBox.querySelector('.strength-label');
        const niveles = ['', 'Débil', 'Media', 'Fuerte', 'Muy fuerte'];
        const clases = ['', 'weak', 'medium', 'strong', 'very-strong'];

        passwordInput.addEventListener('input', () => {
            const valor = passwordInput.value;
            let score = 0;

            if (valor.length >= 8) score++;
            if (/[a-z]/.test(valor) && /[A-Z]/.test(valor)) score++;
            if (/\d/.test(valor)) score++;
            if (/[^A-Za-z0-9]/.test(valor)) score++;
            if (!valor.length) score = 0;

            strengthBox.className = 'password-strength' + (clases[score] ? ' ' + clases[score] : '');
            bars.forEach((bar, i) => bar.classList.toggle('active', i < score));
            label.textContent = valor.length ? niveles[score] : '';
        });
    }

    // Coincidencia entre contraseña y confirmación
    const confirmInput = document.getElementById('confirmar_password');
    const matchHint = document.getElementById('matchHint');

    if (passwordInput && confirmInput && matchHint) {
        const verificarCoincidencia = () => {
            if (!confirmInput.value) {
                matchHint.textContent = '';
                matchHint.className = 'field-hint';
                return;
            }
            const coincide = confirmInput.value === passwordInput.value;
            matchHint.textContent = coincide ? 'Las contraseñas coinciden' : 'Las contraseñas no coinciden';
            matchHint.className = 'field-hint ' + (coincide ? 'ok' : 'error');
        };

        confirmInput.addEventListener('input', verificarCoincidencia);
        passwordInput.addEventListener('input', verificarCoincidencia);
    }

    // Validación visual del correo al salir del campo
    document.querySelectorAll('input[type="email"]').forEach((emailInput) => {
        emailInput.addEventListener('blur', () => {
            if (!emailInput.value) {
                emailInput.classList.remove('field-valid', 'field-invalid');
                return;
            }
            const valido = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailInput.value);
            emailInput.classList.toggle('field-valid', valido);
            emailInput.classList.toggle('field-invalid', !valido);
        });

        emailInput.addEventListener('input', () => {
            emailInput.classList.remove('field-valid', 'field-invalid');
        });
    });

    // Brillo que sigue al cursor en el panel de marca
    const brand = document.querySelector('.auth-brand');
    if (brand) {
        brand.addEventListener('mousemove', (e) => {
            const rect = brand.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width) * 100;
            const y = ((e.clientY - rect.top) / rect.height) * 100;
            brand.style.setProperty('--mx', `${x}%`);
            brand.style.setProperty('--my', `${y}%`);
            brand.classList.add('glow-active');
        });

        brand.addEventListener('mouseleave', () => {
            brand.classList.remove('glow-active');
        });
    }
});
