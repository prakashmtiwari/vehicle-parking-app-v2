<script setup>
import AdminNavbar from '@/components/AdminNavbar.vue'
import AdminFooter from '@/components/AdminFooter.vue'
import AdminCharts from '@/components/AdminCharts.vue';
import AdminParkingHistory from '@/components/adminParkingHistory.vue';
</script>

<template>
  <div class="dashboard-page">
    <AdminNavbar />

    <main class="content-wrapper">
      <div class="dashboard-container">
        <!-- Page Header -->
        <div class="page-header">
          <div class="header-content">
            <h1 class="page-title">Summary Dashboard</h1>
            <p class="page-subtitle">Monitor parking history and revenue analytics in real-time</p>
          </div>
        </div>

        <!-- Analytics Section -->
        <div class="dashboard-section">
          <!-- <div class="section-header">
            <h2 class="section-title">Revenue Analytics</h2>
            <p class="section-description">Visual insights into collected revenue and trends</p>
          </div> -->
          <div class="section-content">
            <AdminCharts />
          </div>
        </div>

        <!-- Parking History Section -->
        <div class="dashboard-section">
          <div class="section-header">
            <h2 class="section-title">Parking History</h2>
            <p class="section-description">Complete record of all parking reservations and transactions</p>
          </div>
          <div class="section-content">
            <AdminParkingHistory />
          </div>
        </div>

      </div>
    </main>

    <AdminFooter />
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

/* Global Styles */
.dashboard-page {
  padding-top: 100px;
  font-family: 'Poppins', sans-serif;
  min-height: 100vh;
  background-color: #f8fafc;
}

.content-wrapper {
  padding: 2rem;
  min-height: calc(100vh - var(--navbar-height, 60px) - var(--footer-height, 80px));
  padding-bottom: 3rem;
}

.dashboard-container {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
}

/* Page Header */
.page-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 1rem;
  padding: 2.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.header-content {
  text-align: left;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: white;
  margin: 0 0 0.5rem 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.page-subtitle {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  font-weight: 400;
}

/* Dashboard Sections */
.dashboard-section {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.dashboard-section:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
}

.dashboard-section:last-child {
  margin-bottom: 0;
}

/* Section Header */
.section-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f1f5f9;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.section-title::before {
  content: '';
  width: 4px;
  height: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 2px;
}

.section-description {
  font-size: 0.9rem;
  color: #64748b;
  margin: 0;
  padding-left: 1rem;
}

/* Section Content */
.section-content {
  position: relative;
}

/* Responsive Design */
@media (max-width: 768px) {
  .content-wrapper {
    padding: 1rem;
  }

  .page-header {
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .page-subtitle {
    font-size: 0.9rem;
  }

  .dashboard-section {
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }

  .section-title {
    font-size: 1.25rem;
  }

  .section-description {
    font-size: 0.85rem;
  }
}

/* Ensure components inside sections have proper spacing */
.section-content :deep(.admin-card),
.section-content :deep(.chart-container),
.section-content :deep(.history-table) {
  box-shadow: none;
  border: none;
}
</style>