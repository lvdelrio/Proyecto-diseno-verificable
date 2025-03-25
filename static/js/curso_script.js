
function deleteCurso(id) {
    fetch(`/borrar_curso/${id}`, { method: 'POST' })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
