import os
import pandas as pd
from datetime import datetime

EXPORT_FOLDER = "reports"

def export_notas_to_csv(notas_list, report_type):
    os.makedirs(EXPORT_FOLDER, exist_ok=True)
    filename = f"{report_type}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = os.path.join(EXPORT_FOLDER, filename)

    df = pd.DataFrame({'notas': notas_list})
    df.to_csv(filepath, index=False)
    return filepath

def export_alumno_notas_to_csv(notas_list, report_type):
    os.makedirs(EXPORT_FOLDER, exist_ok=True)
    filename = f"{report_type}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = os.path.join(EXPORT_FOLDER, filename)

    df = pd.DataFrame(notas_list, columns=['codigo', 'nombre_seccion', 'nota', 'fecha', 'semestre'])
    df.to_csv(filepath, index=False)
    return filepath