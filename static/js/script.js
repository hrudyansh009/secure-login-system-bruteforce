// Theme initialization
(function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
})();

document.addEventListener('DOMContentLoaded', function () {
    const themeToggle = document.getElementById('theme-toggle');
    const sunIcon = document.getElementById('sun-icon');
    const moonIcon = document.getElementById('moon-icon');

    if (themeToggle) {
        updateThemeIcons();

        themeToggle.addEventListener('click', function () {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcons();

            themeToggle.style.transform = 'scale(0.9)';
            setTimeout(() => {
                themeToggle.style.transform = '';
            }, 100);
        });
    }

    function updateThemeIcons() {
        const currentTheme = document.documentElement.getAttribute('data-theme');

        if (sunIcon && moonIcon) {
            if (currentTheme === 'dark') {
                sunIcon.classList.remove('hidden');
                moonIcon.classList.add('hidden');
            } else {
                sunIcon.classList.add('hidden');
                moonIcon.classList.remove('hidden');
            }
        }
    }
});

// Flash messages
document.addEventListener('DOMContentLoaded', function () {
    const flashMessages = document.querySelectorAll('.alert');

    flashMessages.forEach(function (message) {
        setTimeout(function () {
            message.style.opacity = '0';
            message.style.transform = 'translateX(100px)';

            setTimeout(function () {
                message.remove();
            }, 400);
        }, 5000);
    });
});

// Password strength
document.addEventListener('DOMContentLoaded', function () {
    const passwordField = document.getElementById('password');

    if (passwordField) {
        passwordField.addEventListener('input', function () {
            const password = this.value;
            const strength = calculatePasswordStrength(password);
        });
    }
});

function calculatePasswordStrength(password) {
    let strength = 0;

    if (password.length >= 8) strength++;
    if (password.length >= 12) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^a-zA-Z0-9]/.test(password)) strength++;

    return strength;
}

// Button ripple
document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll('.btn');

    buttons.forEach(function (button) {
        button.addEventListener('click', function (e) {
            const ripple = document.createElement('span');
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255, 255, 255, 0.5)';
            ripple.style.width = ripple.style.height = '100px';
            ripple.style.left = e.clientX - this.offsetLeft - 50 + 'px';
            ripple.style.top = e.clientY - this.offsetTop - 50 + 'px';
            ripple.style.pointerEvents = 'none';
            ripple.style.transform = 'scale(0)';
            ripple.style.animation = 'ripple 0.6s ease-out';

            this.appendChild(ripple);

            setTimeout(function () {
                ripple.remove();
            }, 600);
        });
    });

    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
});

// Input interactions
document.addEventListener('DOMContentLoaded', function () {
    const inputs = document.querySelectorAll('.form-control');

    inputs.forEach(function (input) {
        input.addEventListener('focus', function () {
            this.closest('.form-group')?.classList.add('focused');
        });

        input.addEventListener('blur', function () {
            this.closest('.form-group')?.classList.remove('focused');
        });

        if (input.value) {
            input.classList.add('has-value');
        }

        input.addEventListener('input', function () {
            if (this.value) {
                this.classList.add('has-value');
            } else {
                this.classList.remove('has-value');
            }
        });
    });
});

// Loading states
document.addEventListener('DOMContentLoaded', function () {
    const forms = document.querySelectorAll('form');

    forms.forEach(function (form) {
        form.addEventListener('submit', function () {
            const submitButton = form.querySelector('button[type="submit"]');

            if (submitButton && !submitButton.disabled) {
                submitButton.disabled = true;
                const originalContent = submitButton.innerHTML;

                submitButton.innerHTML = '<span class="spinner"></span> Processing...';

                setTimeout(function () {
                    if (submitButton.disabled) {
                        submitButton.disabled = false;
                        submitButton.innerHTML = originalContent;
                    }
                }, 10000);
            }
        });
    });
});

// Page transitions
document.addEventListener('DOMContentLoaded', function () {
    document.body.style.opacity = '0';

    setTimeout(function () {
        document.body.style.transition = 'opacity 0.3s ease-in';
        document.body.style.opacity = '1';
    }, 10);
});

// Dashboard animations
document.addEventListener('DOMContentLoaded', function () {
    const cards = document.querySelectorAll('.dashboard-card');

    const observer = new IntersectionObserver(
        function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                    observer.unobserve(entry.target);
                }
            });
        },
        {
            threshold: 0.1,
        }
    );

    cards.forEach(function (card) {
        observer.observe(card);
    });
});

// Accessibility
document.addEventListener('DOMContentLoaded', function () {
    const themeToggle = document.getElementById('theme-toggle');

    if (themeToggle) {
        themeToggle.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    }

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Tab') {
            document.body.classList.add('keyboard-navigation');
        }
    });

    document.addEventListener('mousedown', function () {
        document.body.classList.remove('keyboard-navigation');
    });
});

// Console message
console.log(
    '%c🔐 Secure Login System',
    'font-size: 20px; font-weight: bold; color: #6366f1;'
);
console.log(
    '%cBuilt with security in mind | Enhanced UI/UX',
    'font-size: 12px; color: #94a3b8;'
);
console.log(
    '%c💡 Tip: Press the sun/moon icon to toggle light/dark mode!',
    'font-size: 11px; color: #14b8a6;'
);
