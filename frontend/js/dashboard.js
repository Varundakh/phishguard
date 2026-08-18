// PhishGuard - Dashboard JavaScript
// Statistics and analytics page

const API_BASE = '/api';

// Initialize dashboard on page load
document.addEventListener('DOMContentLoaded', () => {
    loadStatistics();
    // Refresh statistics every 30 seconds
    setInterval(loadStatistics, 30000);
});

// Load and display statistics
async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE}/statistics`);
        
        if (!response.ok) {
            throw new Error('Failed to load statistics');
        }
        
        const stats = await response.json();
        displayStatistics(stats);
        
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Display statistics on the page
function displayStatistics(stats) {
    // Update stat cards
    document.getElementById('totalScans').textContent = stats.total_scans;
    document.getElementById('safeScans').textContent = stats.safe_scans;
    document.getElementById('moderateScans').textContent = stats.moderate_scans;
    document.getElementById('suspiciousScans').textContent = stats.suspicious_scans;
    document.getElementById('highRiskScans').textContent = stats.high_risk_scans;
    document.getElementById('avgScore').textContent = stats.average_risk_score.toFixed(1);
    
    // Update chart bars
    const total = stats.total_scans || 1; // Avoid division by zero
    
    const safePercent = (stats.safe_scans / total) * 100;
    const moderatePercent = (stats.moderate_scans / total) * 100;
    const suspiciousPercent = (stats.suspicious_scans / total) * 100;
    const highRiskPercent = (stats.high_risk_scans / total) * 100;
    
    document.getElementById('safeBar').style.width = `${safePercent}%`;
    document.getElementById('safeBar').textContent = safePercent > 10 ? `${safePercent.toFixed(0)}%` : '';
    
    document.getElementById('moderateBar').style.width = `${moderatePercent}%`;
    document.getElementById('moderateBar').textContent = moderatePercent > 10 ? `${moderatePercent.toFixed(0)}%` : '';
    
    document.getElementById('suspiciousBar').style.width = `${suspiciousPercent}%`;
    document.getElementById('suspiciousBar').textContent = suspiciousPercent > 10 ? `${suspiciousPercent.toFixed(0)}%` : '';
    
    document.getElementById('highRiskBar').style.width = `${highRiskPercent}%`;
    document.getElementById('highRiskBar').textContent = highRiskPercent > 10 ? `${highRiskPercent.toFixed(0)}%` : '';
}
