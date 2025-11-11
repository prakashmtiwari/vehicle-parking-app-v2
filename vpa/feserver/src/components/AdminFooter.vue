<template>
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-content">
        <div class="footer-brand">
          <svg class="footer-logo" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17a2 2 0 01-2 2H5a2 2 0 01-2-2v-4a2 2 0 012-2h2a2 2 0 012 2v4zm10 0a2 2 0 01-2 2h-2a2 2 0 01-2-2v-4a2 2 0 012-2h2a2 2 0 012 2v4zM3 9h18v2H3V9zm4-4h10v2H7V5z"/>
          </svg>
          <span class="brand-text">ParkApp</span>
        </div>
        
        <div class="footer-divider"></div>
        
        <p class="footer-text">
          © {{ new Date().getFullYear() }} Vehicle Parking App. All rights reserved.
        </p>
        
        <div class="footer-links">
          <a href="#" class="footer-link">Dashboard</a>
          <span class="separator">•</span>
          <a href="#" class="footer-link">Settings</a>
          <span class="separator">•</span>
          <a href="#" class="footer-link">Support</a>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap');

.footer {
  background: rgba(102, 126, 234, 0.95);
  backdrop-filter: blur(20px);
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.15);
  position: relative;
  width: 100%;
  margin-top: auto;
  font-family: 'Poppins', sans-serif;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem 2rem 0.75rem;
}

.footer-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  margin-bottom: 0;
}

.footer-logo {
  width: 1.5rem;
  height: 1.5rem;
  color: white;
}

.brand-text {
  color: white;
  font-size: 1rem;
  font-weight: 600;
  letter-spacing: -0.5px;
}

.footer-divider {
  width: 60px;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.5), transparent);
  margin: 0;
}

.footer-text {
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.825rem;
  font-weight: 400;
  margin: 0;
  text-align: center;
}

.footer-links {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  flex-wrap: wrap;
  justify-content: center;
}

.footer-link {
  color: rgba(255, 255, 255, 0.85);
  text-decoration: none;
  font-size: 0.8rem;
  font-weight: 500;
  transition: all 0.3s ease;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
}

.footer-link:hover {
  color: white;
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-1px);
}

.separator {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.8rem;
}

/* Responsive */
@media (max-width: 768px) {
  .footer-container {
    padding: 0.875rem 1rem 0.625rem;
  }

  .footer-brand {
    margin-bottom: 0;
  }

  .brand-text {
    font-size: 0.9rem;
  }

  .footer-text {
    font-size: 0.775rem;
  }

  .footer-links {
    gap: 0.5rem;
    font-size: 0.75rem;
  }

  .footer-link {
    font-size: 0.75rem;
  }
}

@media (max-width: 480px) {
  .footer-links {
    flex-direction: column;
    gap: 0.4rem;
  }

  .separator {
    display: none;
  }
}
</style>