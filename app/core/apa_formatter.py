from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
import os

class APAFormatter:
    def __init__(self, file_path, version, paragraphs_data, style_map_inverse):
        self.file_path = file_path
        self.version = version
        self.paragraphs_data = paragraphs_data
        self.style_map_inverse = style_map_inverse
        self.doc = Document(file_path)

    def aplicar_reglas_globales(self):
        # Margenes estandar APA (1 pulgada / 2.54 cm)
        for section in self.doc.sections:
            section.top_margin = Cm(2.54)
            section.bottom_margin = Cm(2.54)
            section.left_margin = Cm(2.54)
            section.right_margin = Cm(2.54)

        # Configuracion del estilo base
        style = self.doc.styles['Normal']
        font = style.font
        font.name = 'Times New Roman'
        font.size = Pt(12)
        
        pf = style.paragraph_format
        pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT

    def formatear_bloque(self, paragraph, estilo_espanol):
        # Reset de formato de parrafo
        pf = paragraph.paragraph_format
        pf.first_line_indent = 0
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
        
        # Acceder al run para formato de fuente (negritas/cursivas)
        if not paragraph.runs:
            paragraph.add_run(paragraph.text)
        
        for run in paragraph.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12)
            run.bold = False
            run.italic = False

            if estilo_espanol == "Párrafo Normal":
                pf.first_line_indent = Cm(1.27)
            
            elif estilo_espanol in ["Título Principal", "Título 1"]:
                pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run.bold = True
            
            elif estilo_espanol == "Título 2":
                run.bold = True
            
            elif estilo_espanol == "Título 3":
                if "7a" in self.version:
                    run.bold = True
                    run.italic = True
                else: # APA 6
                    pf.first_line_indent = Cm(1.27)
                    run.bold = True

    def procesar(self, solo_indices=None):
        self.aplicar_reglas_globales()
        
        for p_data in self.paragraphs_data:
            idx = p_data["id"]
            
            # Si solo se formatea una seleccion, saltamos los demas
            if solo_indices is not None and idx not in solo_indices:
                continue
                
            real_paragraph = self.doc.paragraphs[idx]
            self.formatear_bloque(real_paragraph, p_data["current_style"])

        nombre_base, ext = os.path.splitext(self.file_path)
        ruta_salida = f"{nombre_base}_APA_PROCESADO{ext}"
        self.doc.save(ruta_salida)
        return ruta_salida