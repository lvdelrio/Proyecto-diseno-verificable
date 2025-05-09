document.addEventListener('DOMContentLoaded', function() {
    initSlidePanels();
});

function initSlidePanels() {
    setupPanelTriggers();
    setupOverlayClickHandler();
}

function setupPanelTriggers() {
    const panelTriggers = document.querySelectorAll('[data-panel-target]');
    
    panelTriggers.forEach(trigger => {
        setupSinglePanelTrigger(trigger);
    });
}

function setupSinglePanelTrigger(trigger) {
    const panelElements = getPanelElements(trigger);
    
    if (arePanelElementsVisible(panelElements)) {
        attachPanelEventListeners(panelElements);
    }
}

function getPanelElements(trigger) {
    const panelId = trigger.dataset.panelTarget;
    const panel = document.getElementById(panelId);
    const overlay = document.getElementById('overlay');
    const closeBtn = panel ? panel.querySelector('[data-action="close-panel"]') : null;
    
    return { trigger, panel, overlay, closeBtn, panelId };
}

function arePanelElementsVisible({ panel, overlay }) {
    return panel && overlay;
}

function attachPanelEventListeners({ trigger, panel, overlay, closeBtn }) {
    trigger.addEventListener('click', () => togglePanel(panel, overlay));

    if (closeBtn) {
        closeBtn.addEventListener('click', () => togglePanel(panel, overlay));
    }
}

function setupOverlayClickHandler() {
    const overlay = document.getElementById('overlay');
    
    if (overlay) {
        overlay.addEventListener('click', () => closeAllActivePanels(overlay));
    }
}

function closeAllActivePanels(overlay) {
    const activePanels = document.querySelectorAll('.slide-panel.active');
    
    activePanels.forEach(panel => {
        togglePanel(panel, overlay);
    });
}

function togglePanel(panel, overlay) {
    toggleElementClass(panel, 'active');
    toggleElementClass(overlay, 'hidden');
    toggleElementClass(document.body, 'overflow-hidden');
}

function toggleElementClass(element, className) {
    element.classList.toggle(className);
}

window.togglePanelById = function(panelId) {
    const panelElements = {
        panel: document.getElementById(panelId),
        overlay: document.getElementById('overlay')
    };
    
    if (arePanelElementsValid(panelElements)) {
        togglePanel(panelElements.panel, panelElements.overlay);
    }
};