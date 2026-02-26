let network = null;
let nodesDataSet = null;
let reportData = null;
let allNodes = [];
let allEdges = [];
let filteredNodes = [];
let filteredEdges = [];
let cycles = [];
let deadModules = [];
let graphData = {};
let selectedNodeId = null;

const splash = document.getElementById('splash');
const splashCard = document.getElementById('splashCard');
const progressFill = document.getElementById('progressFill');
const cardsContainer = document.getElementById('cards');
const mainApp = document.getElementById('mainApp');
const cards = document.querySelectorAll('.card');
const networkContainer = document.getElementById('network');
const sidebar = document.getElementById('sidebar');
const fileInput = document.getElementById('fileInput');
const searchInput = document.getElementById('search');
const detailPanel = document.getElementById('detailPanel');
const closePanel = document.getElementById('closePanel');

const cycleColors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6'];

console.log("TEST:", [
    !!document.getElementById('splash'),
    !!document.getElementById('splashCard'),
    !!document.getElementById('progressFill'),
    document.querySelectorAll('.card').length
]);

function waitForFonts() {
    return new Promise((resolve) => {
        if (document.fonts && document.fonts.ready) {
            document.fonts.ready.then(() => {
                resolve();
            });
        } else {
            setTimeout(resolve, 100);
        }
    });
}

function animateProgressFill(duration = 3500) {
    return new Promise((resolve) => {
        if (!progressFill) {
            resolve();
            return;
        }
        
        progressFill.style.width = '0%';
        progressFill.style.transition = `width ${duration}ms ease-in-out`;
        
        setTimeout(() => {
            progressFill.style.width = '100%';
        }, 50);
        
        setTimeout(() => {
            resolve();
        }, duration);
    });
}

function showCard(card, index) {
    return new Promise((resolve) => {
        setTimeout(() => {
            card.classList.remove('hide');
            card.classList.add('show');
            setTimeout(resolve, 600);
        }, index * 300);
    });
}

function hideCard(card) {
    return new Promise((resolve) => {
        card.classList.remove('show');
        card.classList.add('hide');
        setTimeout(resolve, 300);
    });
}

async function runSplashSequence() {
    console.log("Splash running", {splash, splashCard, progressFill, cards});
    
    if (!splash || !splashCard || !progressFill) {
        console.error('Splash elements missing');
        showMainApp();
        return;
    }
    
    try {
        await waitForFonts();
        
        await animateProgressFill(3500);
        
        if (cardsContainer && cards.length > 0) {
            cardsContainer.classList.remove('hidden');
            
            for (let i = 0; i < cards.length; i++) {
                await showCard(cards[i], i);
            }
            
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            for (let i = 0; i < cards.length; i++) {
                await hideCard(cards[i]);
            }
            
            await new Promise(resolve => setTimeout(resolve, 300));
            cardsContainer.classList.add('hidden');
        }
        
        if (splash) {
            splash.style.opacity = '0';
            splash.style.transition = 'opacity 0.5s ease-out';
            await new Promise(resolve => setTimeout(resolve, 500));
            splash.remove();
        }
        
        showMainApp();
        await loadReportData();
        
    } catch (error) {
        console.error('Splash sequence error:', error);
        showMainApp();
    }
}

function showMainApp() {
    if (mainApp) {
        mainApp.classList.remove('hidden');
    }
}

function checkFileExists(url) {
    return fetch(url, { method: 'HEAD' })
        .then(response => response.ok)
        .catch(() => false);
}

async function loadReportData() {
    const reportPath = 'sample_reports/sample_report.json';
    
    try {
        const exists = await checkFileExists(reportPath);
        if (!exists) {
            console.log('Sample report file does not exist, skipping load');
            return;
        }
        
        const response = await fetch(reportPath);
        if (!response.ok) {
            console.log('Failed to load report data');
            return;
        }
        
        reportData = await response.json();
        console.log('Report data loaded:', reportData);
        
        if (reportData) {
            processReportData(reportData);
            updateSummary();
            updateCyclesList();
            updateDeadList();
            renderNetwork();
        }
    } catch (error) {
        console.error('Error loading report data:', error);
    }
}

function processReportData(data) {
    if (!data || typeof data !== 'object') {
        return;
    }
    
    allNodes = [];
    allEdges = [];
    cycles = [];
    deadModules = [];
    graphData = {};
    
    if (data.graph && typeof data.graph === 'object') {
        graphData = data.graph;
        
        Object.keys(graphData).forEach((moduleName, index) => {
            const nodeId = moduleName;
            const dependencies = graphData[moduleName] || [];
            
            allNodes.push({
                id: nodeId,
                label: moduleName,
                title: moduleName,
                color: '#3498db'
            });
            
            dependencies.forEach(dep => {
                allEdges.push({
                    id: `edge_${nodeId}_${dep}`,
                    from: nodeId,
                    to: dep,
                    arrows: 'to'
                });
            });
        });
    }
    
    if (data.cycles && Array.isArray(data.cycles)) {
        cycles = data.cycles;
    }
    
    if (data.dead_modules && Array.isArray(data.dead_modules)) {
        deadModules = data.dead_modules;
        
        deadModules.forEach(moduleName => {
            const node = allNodes.find(n => n.id === moduleName);
            if (node) {
                node.color = '#e74c3c';
            }
        });
    }
    
    highlightCycles();
    
    filteredNodes = [...allNodes];
    filteredEdges = [...allEdges];
}

function highlightCycles() {
    cycles.forEach((cycle, cycleIndex) => {
        if (Array.isArray(cycle) && cycle.length > 0) {
            const color = cycleColors[cycleIndex % cycleColors.length];
            cycle.forEach(moduleName => {
                const node = allNodes.find(n => n.id === moduleName);
                if (node && !deadModules.includes(moduleName)) {
                    node.color = color;
                }
            });
        }
    });
    
    if (nodesDataSet) {
        cycles.forEach((cycle, cycleIndex) => {
            if (Array.isArray(cycle) && cycle.length > 0) {
                const color = cycleColors[cycleIndex % cycleColors.length];
                cycle.forEach(moduleName => {
                    if (!deadModules.includes(moduleName)) {
                        nodesDataSet.update({
                            id: moduleName,
                            color: {
                                background: color,
                                border: '#ffffff',
                                highlight: {
                                    background: '#4f46e5',
                                    border: '#ffffff'
                                },
                                hover: {
                                    background: '#6366f1',
                                    border: '#ffffff'
                                }
                            }
                        });
                    }
                });
            }
        });
        
        deadModules.forEach(moduleName => {
            nodesDataSet.update({
                id: moduleName,
                color: {
                    background: '#e74c3c',
                    border: '#ffffff',
                    highlight: {
                        background: '#4f46e5',
                        border: '#ffffff'
                    },
                    hover: {
                        background: '#6366f1',
                        border: '#ffffff'
                    }
                }
            });
        });
    }
}

function updateSummary() {
    const statModules = document.getElementById('statModules');
    const statEdges = document.getElementById('statEdges');
    const statCycles = document.getElementById('statCycles');
    const statDead = document.getElementById('statDead');
    
    if (statModules) statModules.textContent = allNodes.length;
    if (statEdges) statEdges.textContent = allEdges.length;
    if (statCycles) statCycles.textContent = cycles.length;
    if (statDead) statDead.textContent = deadModules.length;
}

function updateCyclesList() {
    const cyclesList = document.getElementById('cyclesList');
    if (!cyclesList) return;
    
    cyclesList.innerHTML = '';
    
    if (cycles.length === 0) {
        cyclesList.innerHTML = '<p style="color: rgba(255,255,255,0.5); font-size: 12px;">No cycles found</p>';
        return;
    }
    
    cycles.forEach((cycle, index) => {
        if (Array.isArray(cycle) && cycle.length > 0) {
            const cycleDiv = document.createElement('div');
            cycleDiv.className = 'cycle-item';
            cycleDiv.style.borderLeftColor = cycleColors[index % cycleColors.length];
            cycleDiv.style.borderLeftWidth = '3px';
            cycleDiv.textContent = cycle.join(' → ');
            cycleDiv.onclick = () => highlightCycle(cycle);
            cyclesList.appendChild(cycleDiv);
        }
    });
}

function updateDeadList() {
    const deadList = document.getElementById('deadList');
    if (!deadList) return;
    
    deadList.innerHTML = '';
    
    if (deadModules.length === 0) {
        deadList.innerHTML = '<p style="color: rgba(255,255,255,0.5); font-size: 12px;">No dead modules</p>';
        return;
    }
    
    deadModules.forEach(moduleName => {
        const deadDiv = document.createElement('div');
        deadDiv.className = 'dead-item';
        deadDiv.textContent = moduleName;
        deadDiv.onclick = () => highlightNode(moduleName);
        deadList.appendChild(deadDiv);
    });
}

function highlightCycle(cycle) {
    if (!network || !Array.isArray(cycle)) return;
    
    const cycleNodeIds = cycle.filter(id => allNodes.some(n => n.id === id));
    network.selectNodes(cycleNodeIds);
    network.focus(cycleNodeIds[0], {
        scale: 1.5,
        animation: true
    });
}

function highlightNode(nodeId) {
    if (!network) return;
    
    network.selectNodes([nodeId]);
    network.focus(nodeId, {
        scale: 1.5,
        animation: true
    });
}

function convertNodeColors(nodes) {
    return nodes.map(node => {
        if (typeof node.color === 'string') {
            return {
                ...node,
                color: {
                    background: node.color,
                    border: '#ffffff',
                    highlight: {
                        background: '#4f46e5',
                        border: '#ffffff'
                    },
                    hover: {
                        background: '#6366f1',
                        border: '#ffffff'
                    }
                }
            };
        }
        return node;
    });
}

function renderNetwork() {
    if (!networkContainer) {
        console.error('Network container not found');
        return;
    }
    
    if (typeof vis === 'undefined') {
        console.error('vis-network library not loaded');
        return;
    }
    
    if (filteredNodes.length === 0) {
        filteredNodes = [
            { id: '1', label: 'No data', color: { background: '#95a5a6', border: '#ffffff' } }
        ];
    }
    
    const processedNodes = convertNodeColors(filteredNodes);
    
    nodesDataSet = new vis.DataSet(processedNodes);
    const edges = new vis.DataSet(filteredEdges);
    
    const data = { nodes: nodesDataSet, edges };
    
    const options = {
        nodes: {
            shape: 'dot',
            size: 8,
            borderWidth: 1,
            color: {
                background: '#111827',
                border: '#ffffff',
                highlight: {
                    background: '#4f46e5',
                    border: '#ffffff'
                },
                hover: {
                    background: '#6366f1',
                    border: '#ffffff'
                }
            },
            font: {
                color: '#fff',
                size: 12
            }
        },
        edges: {
            arrows: 'to',
            color: {
                color: '#94a3b8',
                highlight: '#f43f5e',
                hover: '#f43f5e'
            },
            width: 1,
            smooth: {
                type: 'dynamic'
            }
        },
        physics: {
            enabled: true,
            stabilization: {
                iterations: 200
            },
            barnesHut: {
                gravitationalConstant: -2000,
                centralGravity: 0.1,
                springLength: 150,
                springConstant: 0.04,
                damping: 0.09
            }
        },
        interaction: {
            hover: true,
            tooltipDelay: 100,
            zoomView: true,
            dragView: true
        }
    };
    
    network = new vis.Network(networkContainer, data, options);
    
    network.on('click', (params) => {
        if (params.nodes.length > 0) {
            const nodeId = params.nodes[0];
            showDetailPanel(nodeId);
        } else {
            hideDetailPanel();
        }
    });
    
    network.on('hoverNode', (params) => {
        networkContainer.style.cursor = 'pointer';
    });
    
    network.on('blurNode', () => {
        networkContainer.style.cursor = 'default';
    });
    
    highlightCycles();
}

function showDetailPanel(nodeId) {
    if (!detailPanel || !graphData) return;
    
    selectedNodeId = nodeId;
    const imports = graphData[nodeId] || [];
    
    const importedBy = Object.keys(graphData).filter(module => {
        const deps = graphData[module] || [];
        return deps.includes(nodeId);
    });
    
    const detailTitle = document.getElementById('detailTitle');
    const detailImports = document.getElementById('detailImports');
    const detailImportedBy = document.getElementById('detailImportedBy');
    
    if (detailTitle) detailTitle.textContent = nodeId;
    
    if (detailImports) {
        detailImports.innerHTML = '';
        if (imports.length === 0) {
            detailImports.innerHTML = '<li style="color: rgba(255,255,255,0.5);">None</li>';
        } else {
            imports.forEach(imp => {
                const li = document.createElement('li');
                li.textContent = imp;
                li.onclick = () => highlightNode(imp);
                li.style.cursor = 'pointer';
                detailImports.appendChild(li);
            });
        }
    }
    
    if (detailImportedBy) {
        detailImportedBy.innerHTML = '';
        if (importedBy.length === 0) {
            detailImportedBy.innerHTML = '<li style="color: rgba(255,255,255,0.5);">None</li>';
        } else {
            importedBy.forEach(imp => {
                const li = document.createElement('li');
                li.textContent = imp;
                li.onclick = () => highlightNode(imp);
                li.style.cursor = 'pointer';
                detailImportedBy.appendChild(li);
            });
        }
    }
    
    detailPanel.classList.remove('hidden');
}

function hideDetailPanel() {
    if (detailPanel) {
        detailPanel.classList.add('hidden');
        selectedNodeId = null;
    }
}

function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = (e) => {
        try {
            const data = JSON.parse(e.target.result);
            reportData = data;
            processReportData(data);
            updateSummary();
            updateCyclesList();
            updateDeadList();
            renderNetwork();
        } catch (error) {
            console.error('Error parsing JSON:', error);
            alert('Invalid JSON file');
        }
    };
    reader.readAsText(file);
}

function handleSearch() {
    const query = searchInput.value.toLowerCase().trim();
    
    if (!query) {
        filteredNodes = [...allNodes];
        filteredEdges = [...allEdges];
    } else {
        filteredNodes = allNodes.filter(node => 
            node.label.toLowerCase().includes(query)
        );
        
        const filteredNodeIds = new Set(filteredNodes.map(n => n.id));
        filteredEdges = allEdges.filter(edge => 
            filteredNodeIds.has(edge.from) && filteredNodeIds.has(edge.to)
        );
    }
    
    if (network) {
        const processedNodes = convertNodeColors(filteredNodes);
        const nodes = new vis.DataSet(processedNodes);
        const edges = new vis.DataSet(filteredEdges);
        network.setData({ nodes, edges });
        nodesDataSet = nodes;
        highlightCycles();
    }
    
    if (query && filteredNodes.length > 0) {
        highlightNode(filteredNodes[0].id);
    }
}

if (fileInput) {
    fileInput.addEventListener('change', handleFileUpload);
}

if (searchInput) {
    searchInput.addEventListener('input', handleSearch);
}

if (closePanel) {
    closePanel.addEventListener('click', hideDetailPanel);
}

document.addEventListener('DOMContentLoaded', () => {
    const hasSeenSplash = sessionStorage.getItem('dpv_splash_seen');
    
    if (hasSeenSplash) {
        showMainApp();
        loadReportData();
    } else {
        runSplashSequence();
        sessionStorage.setItem('dpv_splash_seen', 'true');
    }
});
