export async function handleSuccessfulUpload(response, dropdown) {
    const result = await response.json();
    alert(result.message);
    dropdown.toggleDropdown(); 
    window.location.reload();
}

export async function handleServerError(response) {
    const error = await response.json();
    return new Error(error.message || 'Error al subir el archivo');
}

export function handleUploadError(error) {
    alert('Error: ' + error.message);
    console.error('Error:', error);
}

