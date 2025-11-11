<script setup>
import AdminNavbar from '@/components/AdminNavbar.vue'
import AdminFooter from '@/components/AdminFooter.vue'
import AdminSearch from '@/components/AdminSearch.vue';
</script>

<template>
  <div class="dashboard-page">
    <AdminNavbar />

    <main class="content-wrapper">
      <div class="admin-container">
        <div class="admin-card">
          <div class="card-header">
            <h2 class="card-title">Welcome to the Dashboard 👋</h2>
            <p class="card-subtitle">Manage parking lots, spots, and users easily.</p>
          </div>
          
          <div class="search-section">
            <AdminSearch />
          </div>

          <!-- <div class="dashboard-summary">
            <p class="summary-text">Dashboard features coming soon: Quick Statistics & Recent Activity.</p>
          </div> -->
        </div>
      </div>
    </main>
    
    <AdminFooter />
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

/* Apply the Poppins font globally within this component */
.dashboard-page {
  font-family: 'Poppins', sans-serif;
  min-height: 100vh;
  background-color: #f8fafc; /* Lighter background for a cleaner dashboard feel */
}

.content-wrapper {
  padding: 2rem;
  /* Adjust min-height to push footer down */
  min-height: calc(100vh - var(--navbar-height, 60px) - var(--footer-height, 80px)); 
  padding-bottom: 3rem; /* Extra space above the footer */
}

.admin-container {
  width: 100%;
  max-width: 1200px; /* Wider max-width for a dashboard layout */
  margin: 0 auto; /* Center the content */
}

/* --- Card Styling (Matching Registration Card) --- */
.admin-card {
  background: white; /* Simpler white background, but keeping the clean aesthetic */
  border-radius: 1rem;
  padding: 2.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05); /* Lighter shadow for dashboard */
  border: 1px solid #e2e8f0; /* Subtle border */
}

.card-header {
  text-align: left;
  margin-bottom: 2rem;
  border-bottom: 1px solid #f1f5f9; /* Separator for header */
  padding-bottom: 1.5rem;
}

.card-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.card-subtitle {
  font-size: 1rem;
  color: #64748b;
  margin: 0.5rem 0 0 0;
}

.search-section {
    margin-bottom: 2rem;
}

.dashboard-summary {
    padding-top: 1rem;
    text-align: center;
    color: #94a3b8;
    font-size: 0.9rem;
}

.summary-text {
    border: 1px dashed #cbd5e1;
    padding: 1.5rem;
    border-radius: 0.5rem;
}

/* Responsive */
@media (max-width: 768px) {
  .content-wrapper {
    padding: 1.5rem;
  }
  
  .admin-card {
    padding: 1.5rem;
  }

  .card-title {
    font-size: 1.5rem;
  }

  .card-subtitle {
    font-size: 0.9rem;
  }
}
</style>