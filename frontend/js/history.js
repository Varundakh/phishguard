// PhishGuard - History JavaScript
// Scan history and search functionality

const API_BASE = '/api';
const ITEMS_PER_PAGE = 10;

let currentPage = 1;
let allScans = [];
let filteredScans = [];

// DOM Elements
const searchInput = document.getElementById('searchInput');
const riskFilter = document.getElementById('riskFilter');
const clearHistoryBtn = document.getElementById('clearHistoryBtn');
const loadingState = document.getElementById('loadingState');
const emptyState = document.getElementById('emptyState');
const scansTableBody = document.getElementById('scansTableBody');
const paginationSection = document.getElementById('paginationSection');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const pageInfo = document.getElementById('pageInfo');

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadScans();
    
    // Event listeners
    searchInput.addEventListener('input', filterScans);
    riskFilter.addEventListener('change', filterScans);
    clearHistoryBtn.addEventListener('click', deleteAllScans);
    prevBtn.addEventListener('click', () => goToPage(currentPage - 1));
    nextBtn.addEventListener('click', () => goToPage(currentPage + 1));
});

// Load scans from API
async function loadScans() {
    try {
        showLoading();
        
        const response = await fetch(`${API_BASE}/scans?limit=1000`);
        
        if (!response.ok) {
            throw new Error('Failed to load scans');
        }
        
        const data = await response.json();
        allScans = data.scans || [];
        filteredScans = [...allScans];
        
        currentPage = 1;
        displayScans();
        
    } catch (error) {
        console.error('Error loading scans:', error);
        showEmptyState();
    }
}

// Filter scans based on search and risk level
function filterScans() {
    const searchTerm = searchInput.value.toLowerCase();
    const riskLevel = riskFilter.value;
    
    filteredScans = allScans.filter(scan => {
        const matchesSearch = scan.url.toLowerCase().includes(searchTerm);
        const matchesRisk = !riskLevel || scan.risk_level === riskLevel;
        return matchesSearch && matchesRisk;
    });
    
    currentPage = 1;
    displayScans();
}

// Display scans in table
function displayScans() {
    if (filteredScans.length === 0) {
        showEmptyState();
        return;
    }
    
    hideEmpty();
    hideLoading();
    
    // Calculate pagination
    const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
    const endIndex = startIndex + ITEMS_PER_PAGE;
    const paginatedScans = filteredScans.slice(startIndex, endIndex);
    const totalPages = Math.ceil(filteredScans.length / ITEMS_PER_PAGE);
    
    // Clear table
    scansTableBody.innerHTML = '';
    
    // Add rows
    paginatedScans.forEach(scan => {
        const row = document.createElement('tr');
        
        const date = new Date(scan.created_at).toLocaleString();
        const riskClass = scan.risk_level.toLowerCase();
        
        row.innerHTML = `
            <td>${escapeHtml(scan.url)}</td>
            <td><span class="risk-cell ${riskClass}">${scan.risk_level}</span></td>
            <td>${Math.round(scan.risk_score)}</td>
            <td>${date}</td>
            <td>
                <button class="btn btn-secondary" onclick="viewScan('${scan.scan_id}')">View</button>
                <button class="btn btn-danger" onclick="deleteScan('${scan.scan_id}')">Delete</button>
            </td>
        `;
        scansTableBody.appendChild(row);
    });
    
    // Update pagination
    updatePagination(totalPages);
}

// Update pagination controls
function updatePagination(totalPages) {
    if (totalPages <= 1) {
        paginationSection.style.display = 'none';
        return;
    }
    
    paginationSection.style.display = 'flex';
    pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;
    
    prevBtn.disabled = currentPage === 1;
    nextBtn.disabled = currentPage === totalPages;
}

// Navigate to page
function goToPage(page) {
    const totalPages = Math.ceil(filteredScans.length / ITEMS_PER_PAGE);
    if (page >= 1 && page <= totalPages) {
        currentPage = page;
        displayScans();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

// View scan details
async function viewScan(scanId) {
    try {
        const response = await fetch(`${API_BASE}/scans/${scanId}`);
        
        if (!response.ok) {
            alert('Failed to load scan details');
            return;
        }
        
        const scan = await response.json();
        
        // Display scan details (in a real app, you'd open a modal)
        alert(`URL: ${scan.url}\nRisk Level: ${scan.risk_level}\nScore: ${Math.round(scan.risk_score)}`);
        
    } catch (error) {
        console.error('Error viewing scan:', error);
        alert('Failed to view scan');
    }
}

// Delete individual scan
async function deleteScan(scanId) {
    if (!confirm('Are you sure you want to delete this scan?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/scans/${scanId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete scan');
        }
        
        loadScans();
        
    } catch (error) {
        console.error('Error deleting scan:', error);
        alert('Failed to delete scan');
    }
}

// Delete all scans
async function deleteAllScans() {
    if (!confirm('Are you sure? This will delete ALL scans permanently.')) {
        return;
    }
    
    try {
        showLoading();
        
        const response = await fetch(`${API_BASE}/scans`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete all scans');
        }
        
        loadScans();
        
    } catch (error) {
        console.error('Error deleting all scans:', error);
        alert('Failed to delete scans');
    }
}

// UI State functions
function showLoading() {
    loadingState.style.display = 'block';
    emptyState.style.display = 'none';
    scansTableBody.innerHTML = '';
}

function hideLoading() {
    loadingState.style.display = 'none';
}

function showEmptyState() {
    emptyState.style.display = 'block';
    loadingState.style.display = 'none';
    scansTableBody.innerHTML = '';
    paginationSection.style.display = 'none';
}

function hideEmpty() {
    emptyState.style.display = 'none';
}

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
