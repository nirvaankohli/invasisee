// API Configuration
const API_URL = window.location.origin;

// Utility function for making API requests
async function request(path, options = {}) {
    const config = {
        method: options.method || 'GET',
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        },
        credentials: 'include'
    };

    if (options.body) {
        config.body = JSON.stringify(options.body);
    }

    try {
        const response = await fetch(`${API_URL}${path}`, config);
        const text = await response.text();
        let data;
        
        try {
            data = text ? JSON.parse(text) : {};
        } catch {
            data = { raw: text };
        }

        if (!response.ok) {
            const message = data?.detail || data?.message || response.statusText;
            throw new Error(message);
        }

        return data;
    } catch (error) {
        throw error;
    }
}

// Auth API functions
async function register(username, password) {
    return request('/api/register', {
        method: 'POST',
        body: { username, password }
    });
}

async function login(username, password) {
    return request('/api/login', {
        method: 'POST',
        body: { username, password }
    });
}

async function getMe() {
    return request('/api/me');
}

async function logout() {
    return request('/api/logout', {
        method: 'POST'
    });
}

// Auth Panel Component
class AuthPanel {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        // Initialize with server-side user data if available
        this.user = window.INITIAL_USER || null;
        this.loading = false;
        this.error = '';
        
        this.init();
    }

    async init() {
        // Only fetch if we don't have initial user data
        if (!this.user) {
            await this.fetchMe();
        }
        this.render();
        this.attachEventListeners();
    }

    async fetchMe() {
        try {
            this.error = '';
            const data = await getMe();
            this.user = data;
        } catch {
            this.user = null;
        }
    }

    render() {
        if (!this.container) return;

        if (this.user) {
            this.container.innerHTML = `
                <div class="auth-container">
                    <h3 class="auth-title">Account</h3>
                    <div class="auth-logged-in">
                        <div class="auth-username">
                            Signed in as <span>${this.escapeHtml(this.user.username)}</span>
                        </div>
                        <button class="auth-btn auth-btn-logout" id="logout-btn" ${this.loading ? 'disabled' : ''}>
                            ${this.loading ? 'Working…' : 'Log out'}
                        </button>
                    </div>
                </div>
            `;
        } else {
            this.container.innerHTML = `
                <div class="auth-container">
                    <h3 class="auth-title">Account</h3>
                    <form class="auth-form" id="auth-form">
                        <input
                            class="auth-input"
                            type="text"
                            placeholder="Username"
                            id="username-input"
                            required
                            ${this.loading ? 'disabled' : ''}
                        />
                        <input
                            class="auth-input"
                            type="password"
                            placeholder="Password"
                            id="password-input"
                            required
                            ${this.loading ? 'disabled' : ''}
                        />
                        ${this.error ? `<div class="auth-error">${this.escapeHtml(this.error)}</div>` : ''}
                        <div class="auth-buttons">
                            <button type="submit" class="auth-btn auth-btn-login" ${this.loading ? 'disabled' : ''}>
                                ${this.loading ? 'Working…' : 'Log in'}
                            </button>
                            <button type="button" class="auth-btn auth-btn-register" id="register-btn" ${this.loading ? 'disabled' : ''}>
                                ${this.loading ? 'Working…' : 'Register'}
                            </button>
                        </div>
                    </form>
                </div>
            `;
        }

        this.attachEventListeners();
    }

    attachEventListeners() {
        if (!this.container) return;

        const form = document.getElementById('auth-form');
        const registerBtn = document.getElementById('register-btn');
        const logoutBtn = document.getElementById('logout-btn');

        if (form) {
            form.addEventListener('submit', (e) => this.handleLogin(e));
        }

        if (registerBtn) {
            registerBtn.addEventListener('click', () => this.handleRegister());
        }

        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => this.handleLogout());
        }
    }

    async handleLogin(e) {
        e.preventDefault();
        
        const username = document.getElementById('username-input').value;
        const password = document.getElementById('password-input').value;

        this.loading = true;
        this.error = '';
        this.render();

        try {
            await login(username, password);
            await this.fetchMe();
            this.render();
        } catch (err) {
            this.error = err.message || 'Login failed';
        } finally {
            this.loading = false;
            this.render();
        }
    }

    async handleRegister() {
        const username = document.getElementById('username-input').value;
        const password = document.getElementById('password-input').value;

        if (!username || !password) {
            this.error = 'Username and password are required';
            this.render();
            return;
        }

        this.loading = true;
        this.error = '';
        this.render();

        try {
            await register(username, password);
            // Auto login after register
            await login(username, password);
            await this.fetchMe();
            this.render();
        } catch (err) {
            this.error = err.message || 'Registration failed';
        } finally {
            this.loading = false;
            this.render();
        }
    }

    async handleLogout() {
        this.loading = true;
        this.error = '';
        this.render();

        try {
            await logout();
            this.user = null;
        } catch (err) {
            this.error = err.message || 'Logout failed';
        } finally {
            this.loading = false;
            this.render();
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Smooth scrolling for anchor links
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#' || !href) return;
            
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                const headerOffset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Set current year in footer
function setCurrentYear() {
    const yearElement = document.getElementById('current-year');
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Initialize auth panel
    const authPanel = new AuthPanel('auth-panel');
    
    // Initialize smooth scrolling
    initSmoothScroll();
    
    // Set current year
    setCurrentYear();
    
    // Add animation on scroll (optional enhancement)
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe elements with animate-fade-in class
    document.querySelectorAll('.animate-fade-in').forEach(el => {
        observer.observe(el);
    });
});
