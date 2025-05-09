import { setupFormSubmission } from './send_json.js';

document.addEventListener('DOMContentLoaded', function() {
    const jsonUploadComponents = document.querySelectorAll('.json-upload-component');
    
    jsonUploadComponents.forEach(component => {
        initJsonUploadComponent(component);
    });
});

function initJsonUploadComponent(component) {
    const componentId = component.dataset.componentId;
    const uploadUrl = component.dataset.uploadUrl;
    
    const elements = getComponentElements(component, componentId);
    setupToggleDropdown(elements.uploadBtn, elements.cancelBtn, elements.dropdown);
    setupClickOutsideHandler(elements.dropdown, elements.uploadBtn);
    setupFormSubmission(component, componentId, uploadUrl, elements.form, elements.dropdown);
}

function getComponentElements(component, componentId) {
    return {
        uploadBtn: component.querySelector(`#jsonUploadBtn_${componentId}`),
        dropdown: component.querySelector(`#jsonUploadDropdown_${componentId}`),
        cancelBtn: component.querySelector(`#cancelBtn_${componentId}`),
        form: component.querySelector(`#bulkUploadForm_${componentId}`)
    };
}

function setupToggleDropdown(uploadBtn, cancelBtn, dropdown) {
    const toggleDropdown = () => dropdown.classList.toggle('hidden');
    
    uploadBtn.addEventListener('click', toggleDropdown);
    cancelBtn.addEventListener('click', toggleDropdown);
    dropdown.toggleDropdown = toggleDropdown;
}

function setupClickOutsideHandler(dropdown, uploadBtn) {
    document.addEventListener('click', function(event) {
        if (!dropdown.contains(event.target) 
            && event.target !== uploadBtn 
            && !uploadBtn.contains(event.target)) {
            dropdown.classList.add('hidden');
        }
    });
}