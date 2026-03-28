/**
 * Login Page — Interactivity & Micro-interactions
 */

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('login-form');
    const toggleBtn = document.getElementById('toggle-password');
    const passwordInput = document.getElementById('password');
    const usernameInput = document.getElementById('username');
    const loginBtn = document.getElementById('login-btn');

    // ---- Password visibility toggle ----
    if (toggleBtn && passwordInput) {
        const eyeIcon = toggleBtn.querySelector('.eye-icon');
        const eyeOffIcon = toggleBtn.querySelector('.eye-off-icon');

        toggleBtn.addEventListener('click', () => {
            const isPassword = passwordInput.type === 'password';
            passwordInput.type = isPassword ? 'text' : 'password';

            if (eyeIcon && eyeOffIcon) {
                eyeIcon.style.display = isPassword ? 'none' : 'block';
                eyeOffIcon.style.display = isPassword ? 'block' : 'none';
            }
        });
    }

    // ---- Input focus ripple effect ----
    const inputGroups = document.querySelectorAll('.input-group');
    inputGroups.forEach(group => {
        const input = group.querySelector('input');
        if (!input) return;

        input.addEventListener('focus', () => {
            group.classList.add('focused');
        });

        input.addEventListener('blur', () => {
            group.classList.remove('focused');
            // Add filled class if input has value
            if (input.value.trim()) {
                group.classList.add('filled');
            } else {
                group.classList.remove('filled');
            }
        });

        // Initialize filled state
        if (input.value.trim()) {
            group.classList.add('filled');
        }
    });

    // ---- Form submit loading state ----
    if (form && loginBtn) {
        form.addEventListener('submit', (e) => {
            const username = usernameInput ? usernameInput.value.trim() : '';
            const password = passwordInput ? passwordInput.value.trim() : '';

            // Basic client-side validation
            if (!username || !password) {
                e.preventDefault();
                if (!username && usernameInput) {
                    shakeInput(document.getElementById('username-group'));
                }
                if (!password && passwordInput) {
                    shakeInput(document.getElementById('password-group'));
                }
                return;
            }

            // Show loading state
            const btnText = loginBtn.querySelector('.btn-text');
            const btnLoader = loginBtn.querySelector('.btn-loader');
            if (btnText) btnText.style.display = 'none';
            if (btnLoader) btnLoader.style.display = 'inline-flex';
            loginBtn.disabled = true;
        });
    }

    // ---- Shake animation for validation ----
    function shakeInput(element) {
        if (!element) return;
        element.style.animation = 'none';
        // Trigger reflow
        void element.offsetHeight;
        element.style.animation = 'shake 0.5s cubic-bezier(0.36, 0.07, 0.19, 0.97)';

        const input = element.querySelector('input');
        if (input) {
            input.style.borderColor = 'var(--error-color)';
            input.style.boxShadow = '0 0 0 3px rgba(248, 113, 113, 0.15)';

            setTimeout(() => {
                input.style.borderColor = '';
                input.style.boxShadow = '';
            }, 2000);
        }
    }

    // Add shake keyframes dynamically
    const style = document.createElement('style');
    style.textContent = `
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-4px); }
            20%, 40%, 60%, 80% { transform: translateX(4px); }
        }
    `;
    document.head.appendChild(style);

    // ---- Auto-focus username field ----
    if (usernameInput && !usernameInput.value) {
        setTimeout(() => usernameInput.focus(), 600);
    }
});
