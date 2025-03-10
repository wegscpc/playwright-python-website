"""Simple Flask application for testing."""
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Us</title>
    <style>
        /* CSS Custom Properties for theme consistency */
        :root {
            /* Colors */
            --color-primary: #1a1a1a;
            --color-secondary: #666666;
            --color-accent: #ff3c00;
            --color-background: #ffffff;
            --color-text: #1a1a1a;
            
            /* Typography */
            --font-primary: "SF Pro Display", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            --font-size-h1: clamp(2.5rem, 5vw, 4rem);
            --font-size-h2: clamp(1.5rem, 3vw, 2rem);
            --font-size-body: clamp(1rem, 1.2vw, 1.2rem);
            
            /* Spacing */
            --spacing-unit: clamp(1rem, 2vw, 2rem);
            --section-spacing: clamp(3rem, 8vw, 8rem);
            
            /* Transitions */
            --transition-speed: 0.3s;
            --transition-ease: cubic-bezier(0.4, 0, 0.2, 1);
            
            /* Layout */
            --container-width: min(90%, 1200px);
            --header-height: 80px;
        }

        /* Base Styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: var(--font-primary);
            color: var(--color-text);
            background: var(--color-background);
            line-height: 1.5;
            overflow-x: hidden;
        }

        /* Header & Navigation */
        .header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: var(--header-height);
            background: var(--color-background);
            z-index: 100;
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
        }

        .header__container {
            width: var(--container-width);
            height: 100%;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        /* Menu Toggle with Wix-style animations */
        .menu-toggle {
            width: 44px;
            height: 44px;
            background: transparent;
            border: none;
            padding: 0;
            cursor: pointer;
            display: none;
            align-items: center;
            justify-content: center;
            -webkit-tap-highlight-color: transparent;
            transition: transform var(--transition-speed) var(--transition-ease);
        }

        @media (max-width: 768px) {
            .menu-toggle {
                display: flex;
            }
        }

        .menu-toggle__container {
            width: 24px;
            height: 24px;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .menu-toggle__icon {
            width: 100%;
            height: 100%;
            position: relative;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 5px 0;
        }

        .menu-toggle__line {
            width: 100%;
            height: 2px;
            background-color: var(--color-text);
            border-radius: 1px;
            transition: transform var(--transition-speed) var(--transition-ease),
                        opacity var(--transition-speed) var(--transition-ease);
        }

        /* Navigation Menu */
        .navigation-menu {
            display: flex;
            gap: calc(var(--spacing-unit) * 2);
        }

        @media (max-width: 768px) {
            .navigation-menu {
                position: fixed;
                top: var(--header-height);
                left: 0;
                width: 100%;
                height: calc(100vh - var(--header-height));
                background: var(--color-background);
                flex-direction: column;
                align-items: center;
                justify-content: center;
                gap: var(--spacing-unit);
                transform: translateX(-100%);
                opacity: 0;
                transition: transform var(--transition-speed) var(--transition-ease),
                            opacity var(--transition-speed) var(--transition-ease);
            }

            .navigation-menu--visible {
                transform: translateX(0);
                opacity: 1;
            }

            .navigation-menu--hidden {
                transform: translateX(-100%);
                opacity: 0;
            }
        }

        .nav-item {
            color: var(--color-text);
            text-decoration: none;
            font-size: var(--font-size-body);
            transition: color var(--transition-speed) var(--transition-ease);
        }

        .nav-item:hover {
            color: var(--color-accent);
        }

        /* Main Content */
        .main {
            margin-top: var(--header-height);
            padding: var(--section-spacing) 0;
        }

        .container {
            width: var(--container-width);
            margin: 0 auto;
        }

        /* Hero Section */
        .hero {
            text-align: center;
            margin-bottom: var(--section-spacing);
        }

        .hero__title {
            font-size: var(--font-size-h1);
            margin-bottom: calc(var(--spacing-unit) * 2);
            line-height: 1.1;
        }

        .hero__subtitle {
            font-size: var(--font-size-h2);
            color: var(--color-secondary);
            max-width: 600px;
            margin: 0 auto;
        }

        /* Contact Grid */
        .contact-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: var(--spacing-unit);
            margin-bottom: var(--section-spacing);
        }

        .contact-card {
            padding: var(--spacing-unit);
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            transition: transform var(--transition-speed) var(--transition-ease);
        }

        .contact-card:hover {
            transform: translateY(-4px);
        }

        .contact-card__title {
            font-size: var(--font-size-h2);
            margin-bottom: var(--spacing-unit);
        }

        .contact-card__text {
            color: var(--color-secondary);
            margin-bottom: var(--spacing-unit);
        }

        .contact-card__link {
            color: var(--color-accent);
            text-decoration: none;
            font-weight: 500;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .contact-card__link:hover {
            text-decoration: underline;
        }

        /* Footer */
        .footer {
            background: var(--color-primary);
            color: var(--color-background);
            padding: var(--section-spacing) 0;
        }

        .footer__container {
            width: var(--container-width);
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: var(--spacing-unit);
        }

        .footer__title {
            font-size: var(--font-size-h2);
            margin-bottom: var(--spacing-unit);
        }

        .footer__text {
            opacity: 0.8;
            margin-bottom: var(--spacing-unit);
        }

        .footer__link {
            color: var(--color-background);
            text-decoration: none;
            opacity: 0.8;
            transition: opacity var(--transition-speed) var(--transition-ease);
        }

        .footer__link:hover {
            opacity: 1;
        }

        .social-links {
            display: flex;
            gap: var(--spacing-unit);
        }

        .social-link {
            color: var(--color-background);
            text-decoration: none;
            opacity: 0.8;
            transition: opacity var(--transition-speed) var(--transition-ease);
        }

        .social-link:hover {
            opacity: 1;
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="header__container">
            <a href="/" class="nav-item">Halo Lab</a>
            <button class="menu-toggle" role="button" aria-label="Toggle navigation menu" aria-expanded="false" tabindex="0">
                <div class="menu-toggle__container">
                    <div class="menu-toggle__icon">
                        <span class="menu-toggle__line"></span>
                        <span class="menu-toggle__line"></span>
                        <span class="menu-toggle__line"></span>
                    </div>
                </div>
            </button>
            <nav class="navigation-menu" role="navigation" aria-hidden="true">
                <a href="#about" class="nav-item">About</a>
                <a href="#services" class="nav-item">Services</a>
                <a href="#work" class="nav-item">Work</a>
                <a href="#contact" class="nav-item">Contact</a>
            </nav>
        </div>
    </header>

    <main class="main">
        <div class="container">
            <section class="hero">
                <h1 class="hero__title">Let's Talk</h1>
                <p class="hero__subtitle">We will respond to you within 24 hours and help bring your ideas to life.</p>
            </section>

            <section class="contact-grid">
                <div class="contact-card">
                    <h2 class="contact-card__title">Email Us</h2>
                    <p class="contact-card__text">For project inquiries and collaborations</p>
                    <a href="mailto:inquiry@example.com" class="contact-card__link">inquiry@example.com</a>
                </div>
                <div class="contact-card">
                    <h2 class="contact-card__title">Call Us</h2>
                    <p class="contact-card__text">Available during business hours</p>
                    <a href="tel:+12133378573" class="contact-card__link">+1 213 337 8573</a>
                </div>
                <div class="contact-card">
                    <h2 class="contact-card__title">Visit Us</h2>
                    <p class="contact-card__text">Our office locations worldwide</p>
                    <a href="#locations" class="contact-card__link">View Locations</a>
                </div>
            </section>
        </div>
    </main>

    <footer class="footer">
        <div class="footer__container">
            <div>
                <h2 class="footer__title">About Us</h2>
                <p class="footer__text">A short story about how a small agency turned into a global company with offices worldwide. To be closer to our clients.</p>
            </div>
            <div>
                <h2 class="footer__title">Connect</h2>
                <div class="social-links">
                    <a href="https://linkedin.com" class="social-link" target="_blank" rel="noopener">LinkedIn</a>
                    <a href="https://twitter.com" class="social-link" target="_blank" rel="noopener">Twitter</a>
                    <a href="https://instagram.com" class="social-link" target="_blank" rel="noopener">Instagram</a>
                </div>
            </div>
        </div>
    </footer>

    <script>
        // Pure function to initialize menu state
        const initializeMenuState = (menu, toggle) => {
            // Set initial state
            toggle.setAttribute('aria-expanded', 'false');
            menu.classList.remove('navigation-menu--visible');
            menu.setAttribute('aria-hidden', 'true');
        };

        // Pure function to toggle menu state
        const toggleMenuState = (menu, toggle, isVisible) => {
            toggle.setAttribute('aria-expanded', isVisible ? 'true' : 'false');
            menu.classList.toggle('navigation-menu--visible', isVisible);
            menu.setAttribute('aria-hidden', isVisible ? 'false' : 'true');
        };

        // Initialize menu functionality
        document.addEventListener('DOMContentLoaded', () => {
            const menu = document.querySelector('.navigation-menu');
            const toggle = document.querySelector('.menu-toggle');
            
            if (!menu || !toggle) return;

            // Set initial state
            initializeMenuState(menu, toggle);

            // Toggle menu on button click
            toggle.addEventListener('click', () => {
                const isCurrentlyVisible = toggle.getAttribute('aria-expanded') === 'true';
                toggleMenuState(menu, toggle, !isCurrentlyVisible);
            });

            // Close menu when clicking outside
            document.querySelector('.main').addEventListener('click', (event) => {
                const isVisible = toggle.getAttribute('aria-expanded') === 'true';
                if (isVisible && !menu.contains(event.target) && !toggle.contains(event.target)) {
                    toggleMenuState(menu, toggle, false);
                }
            });
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Render the index page."""
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(port=5000)
