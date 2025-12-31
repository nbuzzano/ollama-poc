# Búsqueda local de archivos

Se añadieron utilidades y ejemplos para permitir que el agente consulte archivos locales.

Qué se agregó

- `local_file_search` (en `agent/tools.py`): herramienta que busca en archivos `.txt` y `.csv` y devuelve rutas y fragmentos.
  - Por seguridad, la implementación está restringida al directorio configurado en `DATA_DIR`.

- `DATA_DIR` (en `config.py`): variable que apunta por defecto a `data/local_files` dentro del proyecto.

- Carpeta de ejemplo: `data/local_files/` con archivos dummy:
  - `notes.txt`
  - `logs.txt`
  - `dataset.csv`
  - `subdir/more_notes.txt`

- Scripts de prueba:
  - `scripts/test_local_search.py`: prueba la tool importando `agent.tools` y llamando a `local_file_search.run(...)` cuando aplica.
  - `scripts/test_local_search_standalone.py`: versión independiente que ejecuta la función sin dependencias externas.

Cómo probar

1. Activa el entorno virtual:

```bash
source venv/bin/activate
```

2. Ejecuta el script de prueba (asegurándote de que el paquete `agent` sea importable):

```bash
PYTHONPATH=. python3 scripts/test_local_search.py
```

Resultado esperado

- Se listarán las coincidencias encontradas dentro de `data/local_files`.
- Archivos fuera de `DATA_DIR` (por ejemplo `outside.txt` en la raíz) no aparecerán en los resultados.

Notas

- Si quieres permitir búsquedas en rutas arbitrarias, modifica `local_file_search` en `agent/tools.py`. Actualmente se fuerza el uso de `DATA_DIR`.
- Para integración directa en el agente, podríamos registrar `DATA_DIR` en el prompt o en `agent_builder.py` para que el agente invoque la tool automáticamente cuando detecte una pregunta que deba resolverse con datos locales.

Script de integración con el agente

Además de los scripts de prueba, existe `scripts/run_agent_query.py` que envía una pregunta directamente al agente (a través de `agent/agent_builder.py`) y muestra tanto la respuesta procesada como la salida cruda del LLM/chain. Úsalo para validar que, cuando el agente decide consultar archivos locales, las rutas y fragmentos provienen únicamente de `DATA_DIR`.

Ejemplo de uso:

```bash
source venv/bin/activate
PYTHONPATH=. python3 scripts/run_agent_query.py
```

El script imprime el prompt enviado, la salida del LLM (campo `LLM_RAW_OUTPUT`) y el resultado final del agente. Para comprobar aislamiento coloca un archivo que contenga la palabra clave fuera de `data/local_files/` (por ejemplo `outside.txt`) y verifica que no aparezca en la salida del agente.
