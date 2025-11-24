// FRED Portfolio Advisor - Frontend Application
const API_BASE_URL = 'http://localhost:5001/api';

let ratesChart = null;
let dashboardData = null;

// Initialize the dashboard when page loads
document.addEventListener('DOMContentLoaded', () => {
    loadDashboardData();
});

// Load all dashboard data
async function loadDashboardData() {
    try {
        showLoading(true);
        const response = await fetch(`${API_BASE_URL}/dashboard`);
        const data = await response.json();

        if (data.success) {
            dashboardData = data;
            renderDashboard(data);
            showLoading(false);
        } else {
            showError('Failed to load data: ' + data.error);
        }
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showError('Unable to connect to API server. Make sure the backend is running on http://localhost:5001');
    }
}

// Render the complete dashboard
function renderDashboard(data) {
    // Update last update time
    document.getElementById('lastUpdate').textContent = `Last updated: ${data.last_update}`;

    // Render hero section
    renderHeroSection(data);

    // Render indicators
    renderIndicators(data.indicators);

    // Render charts
    renderCharts(data.historical_data);

    // Render yield curve info
    renderYieldCurveInfo(data.yield_curve, data.inflation_pressure);

    // Render portfolio recommendation
    renderPortfolioRecommendation(data.recommendation, data.asset_class_outlook);

    // Render scenarios
    renderScenarios(data.alternative_scenarios);
}

// Render hero section with policy stance
function renderHeroSection(data) {
    const stance = data.policy_stance.stance;
    const heroCard = document.getElementById('heroCard');

    // Set color theme based on stance
    heroCard.className = 'rounded-2xl shadow-xl p-8 text-center ';
    if (stance === 'Hawkish') {
        heroCard.classList.add('stance-hawkish');
        document.getElementById('stanceEmoji').textContent = '🔴';
    } else if (stance === 'Dovish') {
        heroCard.classList.add('stance-dovish');
        document.getElementById('stanceEmoji').textContent = '🟢';
    } else {
        heroCard.classList.add('stance-neutral');
        document.getElementById('stanceEmoji').textContent = '🟡';
    }

    document.getElementById('stanceTitle').textContent = stance;
    document.getElementById('stanceDescription').textContent = data.policy_stance.description;
    document.getElementById('executiveSummary').textContent = data.executive_summary;
    document.getElementById('fedFundsRate').textContent = data.indicators.fed_funds_rate.toFixed(2) + '%';
    document.getElementById('inflationRate').textContent = data.indicators.inflation_rate.toFixed(2) + '%';
}

// Render economic indicators
function renderIndicators(indicators) {
    const grid = document.getElementById('indicatorsGrid');
    grid.innerHTML = '';

    const indicatorCards = [
        {
            label: '10-Year Treasury',
            value: indicators.treasury_10y,
            unit: '%',
            icon: '📈'
        },
        {
            label: '2-Year Treasury',
            value: indicators.treasury_2y,
            unit: '%',
            icon: '📊'
        },
        {
            label: 'Yield Curve Spread',
            value: indicators.yield_curve,
            unit: '',
            icon: '📉'
        },
        {
            label: 'Unemployment Rate',
            value: indicators.unemployment,
            unit: '%',
            icon: '👥'
        }
    ];

    indicatorCards.forEach(card => {
        const cardEl = document.createElement('div');
        cardEl.className = 'bg-white rounded-xl shadow-lg p-6 card-hover';
        cardEl.innerHTML = `
            <div class="flex items-start justify-between">
                <div>
                    <p class="text-sm text-gray-600 font-medium">${card.label}</p>
                    <p class="text-3xl font-bold text-gray-900 mt-2">${card.value !== null ? card.value.toFixed(2) + card.unit : 'N/A'}</p>
                </div>
                <div class="text-4xl">${card.icon}</div>
            </div>
        `;
        grid.appendChild(cardEl);
    });
}

// Render historical charts
function renderCharts(historicalData) {
    const ctx = document.getElementById('ratesChart').getContext('2d');

    // Destroy existing chart if it exists
    if (ratesChart) {
        ratesChart.destroy();
    }

    const fedFundsData = historicalData.fed_funds_rate;
    const treasury10yData = historicalData.treasury_10y;
    const treasury2yData = historicalData.treasury_2y;

    ratesChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: fedFundsData.dates,
            datasets: [
                {
                    label: 'Fed Funds Rate',
                    data: fedFundsData.values,
                    borderColor: 'rgb(59, 130, 246)',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: '10-Year Treasury',
                    data: treasury10yData.values,
                    borderColor: 'rgb(16, 185, 129)',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    tension: 0.4,
                    fill: false
                },
                {
                    label: '2-Year Treasury',
                    data: treasury2yData.values,
                    borderColor: 'rgb(249, 115, 22)',
                    backgroundColor: 'rgba(249, 115, 22, 0.1)',
                    tension: 0.4,
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            }
        }
    });
}

// Render yield curve info
function renderYieldCurveInfo(yieldCurve, inflationPressure) {
    const container = document.getElementById('yieldCurveInfo');

    const riskColors = {
        'Low': 'bg-green-100 text-green-800',
        'Moderate': 'bg-yellow-100 text-yellow-800',
        'High': 'bg-red-100 text-red-800'
    };

    container.innerHTML = `
        <div class="border-l-4 border-blue-500 pl-4">
            <h5 class="font-semibold text-gray-900 mb-2">Yield Curve Status</h5>
            <p class="text-2xl font-bold text-gray-800">${yieldCurve.status}</p>
            <p class="text-sm text-gray-600 mt-1">${yieldCurve.description}</p>
        </div>

        <div class="border-l-4 border-orange-500 pl-4">
            <h5 class="font-semibold text-gray-900 mb-2">Spread</h5>
            <p class="text-2xl font-bold text-gray-800">${yieldCurve.spread !== undefined ? yieldCurve.spread.toFixed(2) : 'N/A'}</p>
            <p class="text-sm text-gray-600 mt-1">10Y - 2Y Treasury</p>
        </div>

        <div class="border-l-4 border-red-500 pl-4">
            <h5 class="font-semibold text-gray-900 mb-2">Recession Risk</h5>
            <p class="text-lg font-semibold">
                <span class="px-3 py-1 rounded-full ${riskColors[yieldCurve.recession_risk] || 'bg-gray-100 text-gray-800'}">
                    ${yieldCurve.recession_risk}
                </span>
            </p>
        </div>

        <div class="border-l-4 border-purple-500 pl-4">
            <h5 class="font-semibold text-gray-900 mb-2">Inflation Pressure</h5>
            <p class="text-lg font-semibold">
                <span class="px-3 py-1 rounded-full" style="background-color: ${inflationPressure.color === 'orange' ? '#fed7aa' : '#d1fae5'}; color: ${inflationPressure.color === 'orange' ? '#9a3412' : '#065f46'}">
                    ${inflationPressure.status}
                </span>
            </p>
            <p class="text-sm text-gray-600 mt-1">${inflationPressure.description}</p>
        </div>
    `;
}

// Render portfolio recommendation
function renderPortfolioRecommendation(recommendation, assetOutlook) {
    document.getElementById('strategyName').textContent = recommendation.strategy_name;
    document.getElementById('riskLevel').textContent = 'Risk: ' + recommendation.risk_level;
    document.getElementById('timeframe').textContent = recommendation.timeframe;
    document.getElementById('strategyRationale').textContent = recommendation.rationale;

    // Key actions
    const actionsContainer = document.getElementById('keyActions');
    actionsContainer.innerHTML = '';
    recommendation.key_actions.forEach((action, index) => {
        const li = document.createElement('li');
        li.className = 'flex items-start gap-3';
        li.innerHTML = `
            <span class="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold">${index + 1}</span>
            <span class="text-gray-700 pt-0.5">${action}</span>
        `;
        actionsContainer.appendChild(li);
    });

    // Allocation bars
    const allocationContainer = document.getElementById('allocationBars');
    allocationContainer.innerHTML = '';
    Object.entries(recommendation.allocation).forEach(([asset, percentage]) => {
        const bar = document.createElement('div');
        bar.innerHTML = `
            <div class="flex justify-between text-sm mb-1">
                <span class="font-medium text-gray-700">${asset}</span>
                <span class="font-bold text-gray-900">${percentage}%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-3">
                <div class="bg-gradient-to-r from-blue-500 to-blue-600 h-3 rounded-full transition-all duration-500" style="width: ${percentage}%"></div>
            </div>
        `;
        allocationContainer.appendChild(bar);
    });

    // Asset outlook
    const outlookContainer = document.getElementById('assetOutlook');
    outlookContainer.innerHTML = '';
    Object.entries(assetOutlook).forEach(([asset, details]) => {
        const outlookCard = document.createElement('div');
        outlookCard.className = 'border-l-4 border-blue-500 pl-3';
        outlookCard.innerHTML = `
            <h5 class="font-semibold text-gray-900">${asset}</h5>
            <div class="flex items-center gap-2 mt-1">
                <span class="text-sm font-medium text-gray-700">${details.outlook}</span>
                <span class="text-xs px-2 py-0.5 bg-gray-100 rounded-full">${details.score}/10</span>
            </div>
            <p class="text-xs text-gray-600 mt-1">${details.comment}</p>
        `;
        outlookContainer.appendChild(outlookCard);
    });
}

// Render alternative scenarios
function renderScenarios(scenarios) {
    const grid = document.getElementById('scenariosGrid');
    grid.innerHTML = '';

    scenarios.forEach(scenario => {
        const card = document.createElement('div');
        card.className = 'bg-white rounded-xl shadow-lg p-6 card-hover';
        card.innerHTML = `
            <h4 class="text-lg font-bold text-gray-900 mb-2">${scenario.scenario}</h4>
            <p class="text-sm text-gray-600 mb-3">
                <span class="font-medium">Probability:</span> ${scenario.probability}
            </p>
            <p class="text-sm text-gray-700 mb-4">
                <span class="font-semibold">Trigger:</span> ${scenario.trigger}
            </p>
            <div class="border-t pt-4">
                <p class="text-sm font-semibold text-gray-900 mb-2">${scenario.adjustment.action}</p>
                <ul class="space-y-1">
                    ${scenario.adjustment.changes.map(change => `
                        <li class="text-xs text-gray-600 flex items-start gap-2">
                            <span class="text-blue-500 mt-0.5">▸</span>
                            <span>${change}</span>
                        </li>
                    `).join('')}
                </ul>
            </div>
        `;
        grid.appendChild(card);
    });
}

// Refresh data
async function refreshData() {
    await loadDashboardData();
}

// Export report
async function exportReport() {
    try {
        const response = await fetch(`${API_BASE_URL}/export/report`);
        const data = await response.json();

        if (data.success) {
            // Create a formatted text report
            let reportText = `FEDERAL RESERVE POLICY ANALYSIS & PORTFOLIO STRATEGY REPORT\n`;
            reportText += `Generated: ${data.report.report_date}\n`;
            reportText += `${'='.repeat(80)}\n\n`;

            reportText += `EXECUTIVE SUMMARY\n`;
            reportText += `${'-'.repeat(80)}\n`;
            reportText += `${data.report.summary}\n\n`;

            reportText += `POLICY STANCE: ${data.report.policy_stance}\n`;
            reportText += `RECOMMENDED STRATEGY: ${data.report.recommendation}\n\n`;

            reportText += `KEY ACTIONS:\n`;
            data.report.key_actions.forEach((action, i) => {
                reportText += `${i + 1}. ${action}\n`;
            });
            reportText += `\n`;

            reportText += `ASSET ALLOCATION:\n`;
            reportText += `${'-'.repeat(80)}\n`;
            Object.entries(data.report.allocation).forEach(([asset, pct]) => {
                reportText += `${asset.padEnd(35)} ${pct}%\n`;
            });
            reportText += `\n`;

            reportText += `CURRENT INDICATORS:\n`;
            reportText += `${'-'.repeat(80)}\n`;
            Object.entries(data.report.indicators).forEach(([key, value]) => {
                if (value !== null) {
                    reportText += `${key.replace(/_/g, ' ').toUpperCase().padEnd(25)} ${typeof value === 'number' ? value.toFixed(2) : value}\n`;
                }
            });

            // Download as text file
            const blob = new Blob([reportText], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `Fed_Policy_Report_${new Date().toISOString().split('T')[0]}.txt`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);

            alert('✓ Report exported successfully!');
        } else {
            alert('Failed to export report: ' + data.error);
        }
    } catch (error) {
        console.error('Export error:', error);
        alert('Failed to export report. Please try again.');
    }
}

// Show/hide loading state
function showLoading(show) {
    document.getElementById('loadingState').classList.toggle('hidden', !show);
    document.getElementById('dashboard').classList.toggle('hidden', show);
}

// Show error message
function showError(message) {
    document.getElementById('loadingState').innerHTML = `
        <div class="text-center py-20">
            <div class="text-6xl mb-4">⚠️</div>
            <p class="text-xl text-gray-800 font-semibold mb-2">Error Loading Data</p>
            <p class="text-gray-600 max-w-md mx-auto">${message}</p>
            <button onclick="loadDashboardData()" class="mt-6 bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition">
                Try Again
            </button>
        </div>
    `;
}
