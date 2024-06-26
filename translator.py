import os
import PyPDF2
from openai import OpenAI
from tqdm import tqdm


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def extraer_texto_pdf(ruta_pdf):
    """
    Extrae el texto de un archivo PDF.
    
    Args:
        ruta_pdf (str): Ruta al archivo PDF.
    
    Returns:
        str: Texto extraído del PDF.
    """
    with open(ruta_pdf, 'rb') as archivo:
        lector = PyPDF2.PdfReader(archivo)
        texto = "".join(pagina.extract_text() for pagina in lector.pages)
    return texto

def traducir_texto(texto, idioma_destino, stream=False):
    """
    Traduce el texto dado al idioma especificado utilizando la API de OpenAI.
    
    Args:
        texto (str): Texto a traducir.
        idioma_destino (str): Idioma al que se traducirá el texto.
        stream (bool): Si se debe mostrar la traducción en tiempo real.
    
    Returns:
        str: Texto traducido.
    """
    chunks = [texto[i:i+4000] for i in range(0, len(texto), 4000)]
    traduccion_completa = ""
    
    for i, chunk in enumerate(tqdm(chunks, desc="Traduciendo chunks", unit="chunk"), 1):
        contexto = f"Traducción del chunk {i} de {len(chunks)}. "
        try:
            respuesta = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"Eres un traductor de papers experto. Traduce el siguiente texto al {idioma_destino} manteniendo el contexto y la coherencia. Debes de hablar con un estilo claro profesional y tecnico, tienes la opción de añadir explicaciones y texto extra si se requiere, este texto ira entre parentesis y con dos saltos de líneas y pondra GPT, todo lo que no sea traducción"},
                    {"role": "user", "content": contexto + chunk}
                ],
                stream=True
            )
            
            chunk_traduccion = ""
            for evento in respuesta:
                if evento.choices[0].delta.content:
                    chunk_traduccion += evento.choices[0].delta.content
                    if stream:
                        print(evento.choices[0].delta.content, end='', flush=True)
            
            traduccion_completa += chunk_traduccion.strip()
            if stream:
                print("\n--- Fin del chunk ---\n")
        
        except Exception as e:
            print(f"\nError al procesar el chunk {i}: {str(e)}")
    
    return traduccion_completa

def procesar_lote_pdfs(directorio_entrada, directorio_salida, idioma_destino, mostrar_en_directo=False):
    """
    Procesa un lote de archivos PDF, extrayendo su texto y traduciéndolo.
    
    Args:
        directorio_entrada (str): Ruta al directorio con los archivos PDF originales.
        directorio_salida (str): Ruta al directorio donde se guardarán las traducciones.
        idioma_destino (str): Idioma al que se traducirán los textos.
        mostrar_en_directo (bool): Si se debe mostrar la traducción en tiempo real.
    """
    os.makedirs(directorio_salida, exist_ok=True)
    
    archivos_pdf = [archivo for archivo in os.listdir(directorio_entrada) if archivo.endswith('.pdf')]
    
    for archivo in tqdm(archivos_pdf, desc="Procesando PDFs", unit="archivo"):
        ruta_entrada = os.path.join(directorio_entrada, archivo)
        ruta_salida = os.path.join(directorio_salida, f"traducido_{archivo}.txt")
        
        texto_original = extraer_texto_pdf(ruta_entrada)
        texto_traducido = traducir_texto(texto_original, idioma_destino, mostrar_en_directo)
        
        with open(ruta_salida, 'w', encoding='utf-8') as archivo_salida:
            archivo_salida.write(texto_traducido)

def main():
    directorio_entrada = r'Ruta/De/Los/Pdfs'
    directorio_salida = r'Ruta/en/la/que/se/guardan/los/pdfs'
    idioma_destino = 'español'
    stream = False  
    
    procesar_lote_pdfs(directorio_entrada, directorio_salida, idioma_destino, stream)

if __name__ == "__main__":
    main()
