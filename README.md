```
pip install --upgrade openai
pip install tqdm
pip install PyPDF2
```

Cambia las siguientes variables

Linea 66-96
```
    directorio_entrada (str): Ruta al directorio con los archivos PDF originales.
    directorio_salida (str): Ruta al directorio donde se guardarán las traducciones.
    idioma_destino (str): Idioma al que se traducirán los textos.
```

```
python3 papertraduser.py
```

Agregar multihilo es fácil pero dispararia los costes expnencialmente en un corto plazo de tiempo
