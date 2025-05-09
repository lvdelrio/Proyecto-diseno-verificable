import { handleSuccessfulUpload, handleServerError, handleUploadError } from './handle_json_upload.js';

export function setupFormSubmission(component, componentId, uploadUrl, form, dropdown) {
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const fileInput = component.querySelector(`#jsonFile_${componentId}`);
        const file = fileInput.files[0];
        
        if (!validateFile(file)) return;
        
        try {
            await processFileUpload(file, uploadUrl, dropdown);
        } catch (error) {
            handleUploadError(error);
        }
    });
}

function validateFile(file) {
    if (!file) {
        alert('Por favor seleccione un archivo JSON');
        return false;
    }
    return true;
}

async function processFileUpload(file, uploadUrl, dropdown) {
    const fileContent = await readFileAsJson(file);
    const response = await sendJsonToServer(fileContent, uploadUrl);
    
    if (response.ok) {
        await handleSuccessfulUpload(response, dropdown);
    } else {
        throw await handleServerError(response);
    }
}

function readFileAsJson(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        
        reader.onload = event => {
            try {
                const jsonData = JSON.parse(event.target.result);
                resolve(jsonData);
            } catch (e) {
                console.error('Error parseo de JSON:', e.message);
                reject(new Error('El archivo no es un JSON válido'));
            }
        };
        
        reader.onerror = () => {
            reject(new Error('Error al leer el archivo'));
        };
        
        reader.readAsText(file);
    });
}

function sendJsonToServer(jsonData, uploadUrl) {
    return fetch(uploadUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(jsonData)
    });
}