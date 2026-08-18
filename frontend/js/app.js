// PhishGuard - Main Application JavaScript
// Analyzer page functionality

const API_BASE = '/api';

// DOM Elements
const analyzerForm = document.getElementById('analyzerForm');
const urlInput = document.getElementById('urlInput');
const btnText = document.getElementById('btnText');
const btnSpinner = document.getElementById('btnSpinner');
const loadingState = document.getElementById('loadingState');
const errorState = document.getElementById('errorState');
const errorMessage = document.getElementById('errorMessage');
const resultsSection = document.getElementById('resultsSection');

// Form submission
analyzerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const url = urlInput.value.trim();
    
    if (!url) {
        showError('Please enter a URL');
        return;
    }
    
    await analyzeURL(url);
});

// Analyze URL function
async function analyzeURL(url) {
    try {
        // Show loading state
        showLoading();
        
        // Make API request
        const response = await fetch(`${API_BASE}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Analysis failed');
        }
        
        const result = await response.json();
        displayResults(result);
        
    } catch (error) {
        showError(error.message);
        console.error('Error:', error);
    }
}

// Display results
function displayResults(result) {
    // Hide loading state
    hideLoading();
    hideError();
    
    // Update risk score
    const riskScore = Math.round(result.risk_score);
    document.getElementById('riskScore').textContent = riskScore;
    document.getElementById('riskLevel').textContent = getRiskLevelLabel(result.risk_level);
    document.getElementById('riskCategory').textContent = `Risk Level: ${result.risk_level}`;
    
    // Update risk badge
    const riskBadge = document.getElementById('riskBadge');
    riskBadge.className = `risk-badge ${result.risk_level.toLowerCase()}`;
    riskBadge.textContent = result.risk_level;
    
    // Update gauge bar
    const gaugeBar = document.getElementById('gaugeBar');
    gaugeBar.style.width = `${riskScore}%`;
    
    // Update indicators
    const indicatorsList = document.getElementById('indicatorsList');
    indicatorsList.innerHTML = '';
    result.indicators.forEach(indicator => {
        const li = document.createElement('li');
        li.textContent = indicator;
        indicatorsList.appendChild(li);
    });
    
    // Update recommendations
    document.getElementById('recommendationText').textContent = result.recommendations;
    
    // Update technical details
    const technicalDetails = document.getElementById('technicalDetails');
    technicalDetails.innerHTML = '';
    Object.entries(result.technical_details || {}).forEach(([key, value]) => {
        const item = document.createElement('div');
        item.className = 'tech-item';
        item.innerHTML = `
            <div class="tech-label">${formatLabel(key)}</div>
            <div class="tech-value">${formatValue(value)}</div>
        `;
        technicalDetails.appendChild(item);
    });
    
    // Update scoring breakdown
    const breakdownDiv = document.getElementById('scoringBreakdown');
    breakdownDiv.innerHTML = '';
    (result.scoring_breakdown || []).forEach(item => {
        const div = document.createElement('div');
        div.className = 'breakdown-item';
        div.innerHTML = `
            <div>
                <div class="breakdown-feature">${item.feature}</div>
                <div class="breakdown-reason">${item.reason}</div>
            </div>
            <div class="breakdown-weight">+${item.weight}</div>
        `;
        breakdownDiv.appendChild(div);
    });
    
    // Show results section
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Helper functions
function getRiskLevelLabel(level) {
    const labels = {
        'LOW': '✅ Safe',
        'MODERATE': '⚠️ Moderate Risk',
        'SUSPICIOUS': '🚨 Suspicious',
        'HIGH': '🚨 High Risk'
    };
    return labels[level] || level;
}

function formatLabel(key) {
    return key
        .replace(/_/g, ' ')
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

function formatValue(value) {
    if (typeof value === 'boolean') {
        return value ? '✓ Yes' : '✗ No';
    }
    if (typeof value === 'string' && value.startsWith('http')) {
        return `<a href="${value}" target="_blank">${value}</a>`;
    }
    return value;
}

function showLoading() {
    analyzerForm.style.display = 'none';
    loadingState.style.display = 'block';
    errorState.style.display = 'none';
    resultsSection.style.display = 'none';
}

function hideLoading() {
    analyzerForm.style.display = 'flex';
    loadingState.style.display = 'none';
}

function showError(message) {
    analyzerForm.style.display = 'flex';
    loadingState.style.display = 'none';
    errorState.style.display = 'block';
    errorMessage.textContent = `⚠️ Error: ${message}`;
    resultsSection.style.display = 'none';
}

function hideError() {
    errorState.style.display = 'none';
}
