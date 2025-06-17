document.addEventListener("DOMContentLoaded", () => {
    const alumnoSelect = document.getElementById("alumno_id");
    const seccionSelect = document.getElementById("seccion_id");
    const evaluacionSelect = document.getElementById("evaluacion_id");

    if (!alumnoSelect || !seccionSelect || !evaluacionSelect) return;

    alumnoSelect.addEventListener("change", () => {
        const alumnoId = alumnoSelect.value;
        seccionSelect.innerHTML = '<option value="">Seleccione un alumno</option>';
        evaluacionSelect.innerHTML = '<option value="">Seleccione una seccion</option>';

        if (alumnoId) {
            fetch(`/api/secciones_por_alumno/${alumnoId}`)
                .then(res => res.json())
                .then(secciones => {
                    seccionSelect.innerHTML = '<option value="">Seleccione una sección</option>';
                    secciones.forEach(s => {
                        const opt = document.createElement("option");
                        opt.value = s.id;
                        opt.textContent = s.nombre;
                        seccionSelect.appendChild(opt);
                    });
                })
                .catch(() => {
                    seccionSelect.innerHTML = '<option value="">Error al cargar secciones</option>';
                });
        }
    });

    seccionSelect.addEventListener("change", () => {
        const seccionId = seccionSelect.value;
        evaluacionSelect.innerHTML = '<option value="">Cargando evaluaciones...</option>';

        if (seccionId) {
            fetch(`/api/evaluaciones_por_seccion/${seccionId}`)
                .then(res => res.json())
                .then(evaluaciones => {
                    evaluacionSelect.innerHTML = '<option value="">Seleccione una evaluación</option>';
                    evaluaciones.forEach(e => {
                        const opt = document.createElement("option");
                        opt.value = e.id;
                        opt.textContent = `${e.nombre} (${e.tipo_categoria})`;
                        evaluacionSelect.appendChild(opt);
                    });
                })
                .catch(() => {
                    evaluacionSelect.innerHTML = '<option value="">Error al cargar evaluaciones</option>';
                });
        }
    });
});
