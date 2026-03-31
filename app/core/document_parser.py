from docx import Document

class DocumentParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.document = None
        self.paragraphs_data = []

    def parse_document(self) -> list:
        """
        Abre el documento .docx, extrae el texto y el estilo de cada parrafo.
        Retorna una lista de diccionarios con la informacion estructurada.
        """
        try:
            self.document = Document(self.file_path)
            self.paragraphs_data = []
            
            for index, paragraph in enumerate(self.document.paragraphs):
                text = paragraph.text.strip()
                
                # Omitir parrafos completamente vacios para no saturar la interfaz
                if not text:
                    continue
                    
                style_name = paragraph.style.name
                
                # Truncar el texto para la previsualizacion en la UI (maximo 80 caracteres)
                preview_text = text if len(text) <= 80 else text[:77] + "..."
                
                self.paragraphs_data.append({
                    "id": index,
                    "preview_text": preview_text,
                    "original_text": text,
                    "current_style": style_name
                })
                
            return self.paragraphs_data
            
        except Exception as e:
            raise Exception(f"Error critico al leer el archivo Word: {str(e)}")