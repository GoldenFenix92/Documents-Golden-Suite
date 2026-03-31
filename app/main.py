import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as messagebox
import math

from core.document_parser import DocumentParser
from core.apa_formatter import APAFormatter
from ui.apa_guide import APAGuideWindow

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Se agregaron los nuevos formatos estructurales
TRADUCCION_ESTILOS = {
    "Normal": "Párrafo Normal",
    "Heading 1": "Título 1",
    "Heading 2": "Título 2",
    "Heading 3": "Título 3",
    "Title": "Título Principal",
    "Subtitle": "Subtítulo",
    "Reference": "Referencia",
    "Block Quote": "Cita en Bloque"
}
ESTILOS_INVERSOS = {v: k for k, v in TRADUCCION_ESTILOS.items()}
OPCIONES_ESTILOS_ESPANOL = list(TRADUCCION_ESTILOS.values())

class DocumentsGoldenSuite(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.datos_documento = []
        self.parrafos_por_pagina = 10
        self.ventana_guia = None

        self.title("Documents Golden Suite - Formateador APA")
        self.geometry("950x650")
        self.minsize(850, 500)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # 1. Cabecera
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="ew")
        self.top_frame.grid_columnconfigure(0, weight=1)

        self.lbl_titulo = ctk.CTkLabel(self.top_frame, text="Formateador APA Auto", font=ctk.CTkFont(size=24, weight="bold"))
        self.lbl_titulo.grid(row=0, column=0, sticky="w")

        self.top_controls = ctk.CTkFrame(self.top_frame, fg_color="transparent")
        self.top_controls.grid(row=0, column=1, sticky="e")
        
        self.btn_guia = ctk.CTkButton(self.top_controls, text="Ver Guía APA", command=self.abrir_guia_apa, fg_color="transparent", border_width=1, text_color=("black", "white"))
        self.btn_guia.pack(side="left", padx=10)

        self.theme_menu = ctk.CTkOptionMenu(self.top_controls, values=["Sistema", "Oscuro", "Claro"], command=self.cambiar_tema, width=120)
        self.theme_menu.pack(side="left")
        self.theme_menu.set("Sistema")

        self.lbl_subtitulo = ctk.CTkLabel(self, text="Selecciona un documento .docx para analizar y aplicar formato", text_color="gray")
        self.lbl_subtitulo.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")

        # 2. Barra de Paginacion
        self.paginacion_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.paginacion_frame.grid(row=2, column=0, padx=20, pady=(0, 5), sticky="ew")
        self.paginacion_frame.grid_columnconfigure(4, weight=1) 
        
        self.lbl_pagina_actual = ctk.CTkLabel(self.paginacion_frame, text="Hoja:", font=ctk.CTkFont(weight="bold"))
        self.lbl_pagina_actual.grid(row=0, column=0, padx=(0, 10))

        self.btn_prev = ctk.CTkButton(self.paginacion_frame, text="<", width=30, command=self.pagina_anterior, state="disabled")
        self.btn_prev.grid(row=0, column=1, padx=5)

        self.combo_paginas = ctk.CTkOptionMenu(self.paginacion_frame, values=["-"], state="disabled", command=self.cambiar_pagina)
        self.combo_paginas.grid(row=0, column=2, padx=5)

        self.btn_next = ctk.CTkButton(self.paginacion_frame, text=">", width=30, command=self.pagina_siguiente, state="disabled")
        self.btn_next.grid(row=0, column=3, padx=5)

        self.btn_restaurar = ctk.CTkButton(self.paginacion_frame, text="Restaurar Página", command=self.restaurar_pagina, fg_color="transparent", border_width=1, text_color=("black", "white"), state="disabled")
        self.btn_restaurar.grid(row=0, column=5, sticky="e")

        # 3. Visor Logico
        self.visor_frame = ctk.CTkScrollableFrame(self, label_text="Visor de Estructura del Documento")
        self.visor_frame.grid(row=3, column=0, padx=20, pady=5, sticky="nsew")

        self.lbl_placeholder = ctk.CTkLabel(self.visor_frame, text="Carga un documento para visualizar la estructura aquí.")
        self.lbl_placeholder.pack(pady=50)

        # 4. Panel Inferior Mejorado (Seleccion de Version y Fuente)
        self.panel_inferior = ctk.CTkFrame(self, fg_color="transparent")
        self.panel_inferior.grid(row=4, column=0, padx=20, pady=20, sticky="ew")
        self.panel_inferior.grid_columnconfigure(2, weight=1)

        self.combo_version = ctk.CTkComboBox(self.panel_inferior, values=["APA 7a Edición", "APA 6a Edición"], command=self.evaluar_version_apa)
        self.combo_version.grid(row=0, column=0, padx=(0, 10), sticky="w")
        
        # Opciones de fuente permitidas en APA 7
        fuentes_apa7 = ["Times New Roman 12", "Arial 11", "Calibri 11", "Georgia 11"]
        self.combo_fuente = ctk.CTkComboBox(self.panel_inferior, values=fuentes_apa7, width=170)
        self.combo_fuente.grid(row=0, column=1, padx=(0, 10), sticky="w")
        self.combo_fuente.set("Times New Roman 12") # Valor por defecto

        self.btn_cargar = ctk.CTkButton(self.panel_inferior, text="Explorar y Cargar .docx", command=self.cargar_archivo)
        self.btn_cargar.grid(row=0, column=3, padx=10, sticky="e")

        self.btn_procesar = ctk.CTkButton(self.panel_inferior, text="Aplicar Formato", state="disabled", fg_color="green", hover_color="darkgreen", command=self.ejecutar_formateo)
        self.btn_procesar.grid(row=0, column=4, padx=(10, 0), sticky="e")

    def evaluar_version_apa(self, seleccion):
        # Si se selecciona APA 6, se bloquea la fuente a Times New Roman 12 obligatoriamente
        if "6a" in seleccion:
            self.combo_fuente.set("Times New Roman 12")
            self.combo_fuente.configure(state="disabled")
        else:
            self.combo_fuente.configure(state="normal")

    def cambiar_tema(self, nuevo_modo: str):
        mapa_temas = {"Sistema": "System", "Oscuro": "Dark", "Claro": "Light"}
        ctk.set_appearance_mode(mapa_temas[nuevo_modo])

    def abrir_guia_apa(self):
        if self.ventana_guia is None or not self.ventana_guia.winfo_exists():
            self.ventana_guia = APAGuideWindow(self)
        else:
            self.ventana_guia.focus()

    def cargar_archivo(self):
        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar documento de Word",
            filetypes=[("Documentos de Word", "*.docx")]
        )
        
        if ruta_archivo:
            self.lbl_subtitulo.configure(text=f"Archivo activo: {ruta_archivo}")
            try:
                parser = DocumentParser(ruta_archivo)
                self.datos_documento = parser.parse_document()
                
                if not self.datos_documento:
                    self.limpiar_visor()
                    ctk.CTkLabel(self.visor_frame, text="El documento está vacío o no contiene texto procesable.").pack(pady=20)
                    return

                total_paginas = math.ceil(len(self.datos_documento) / self.parrafos_por_pagina)
                self.opciones_paginas = [f"Página {i+1} de {total_paginas}" for i in range(total_paginas)]
                
                self.combo_paginas.configure(values=self.opciones_paginas, state="normal")
                self.combo_paginas.set(self.opciones_paginas[0])
                
                self.btn_procesar.configure(state="normal")
                self.btn_restaurar.configure(state="normal")
                
                self.cambiar_pagina(self.opciones_paginas[0])
                
            except Exception as e:
                messagebox.showerror("Error de Lectura", str(e))

    def actualizar_botones_paginacion(self, indice_actual):
        self.btn_prev.configure(state="normal" if indice_actual > 0 else "disabled")
        self.btn_next.configure(state="normal" if indice_actual < len(self.opciones_paginas) - 1 else "disabled")

    def pagina_anterior(self):
        indice_actual = self.opciones_paginas.index(self.combo_paginas.get())
        if indice_actual > 0:
            nueva_pagina = self.opciones_paginas[indice_actual - 1]
            self.combo_paginas.set(nueva_pagina)
            self.cambiar_pagina(nueva_pagina)

    def pagina_siguiente(self):
        indice_actual = self.opciones_paginas.index(self.combo_paginas.get())
        if indice_actual < len(self.opciones_paginas) - 1:
            nueva_pagina = self.opciones_paginas[indice_actual + 1]
            self.combo_paginas.set(nueva_pagina)
            self.cambiar_pagina(nueva_pagina)

    def restaurar_pagina(self):
        self.cambiar_pagina(self.combo_paginas.get())

    def limpiar_visor(self):
        for widget in self.visor_frame.winfo_children():
            widget.destroy()

    def traducir_estilo(self, estilo_ingles):
        return TRADUCCION_ESTILOS.get(estilo_ingles, estilo_ingles)

    def guardar_cambio_estilo(self, nuevo_estilo, item_data):
        item_data["current_style"] = nuevo_estilo

    def cambiar_pagina(self, seleccion: str):
        numero_pagina = int(seleccion.split(" ")[1])
        indice_actual = numero_pagina - 1
        
        self.actualizar_botones_paginacion(indice_actual)

        indice_inicio = indice_actual * self.parrafos_por_pagina
        indice_fin = indice_inicio + self.parrafos_por_pagina
        datos_pagina_actual = self.datos_documento[indice_inicio:indice_fin]
        
        self.limpiar_visor()

        for item in datos_pagina_actual:
            fila_frame = ctk.CTkFrame(self.visor_frame, fg_color=("gray85", "gray20"), corner_radius=8)
            fila_frame.pack(fill="x", pady=6, padx=10)
            
            fila_frame.grid_columnconfigure(0, weight=0)
            fila_frame.grid_columnconfigure(1, weight=1)
            
            estilo_traducido = self.traducir_estilo(item["current_style"])
            lista_opciones = OPCIONES_ESTILOS_ESPANOL.copy()
            
            if estilo_traducido not in lista_opciones:
                lista_opciones.append(estilo_traducido)
                
            combo_estilo = ctk.CTkComboBox(fila_frame, values=lista_opciones, width=160, 
                                           command=lambda v, i=item: self.guardar_cambio_estilo(v, i))
            combo_estilo.set(estilo_traducido)
            combo_estilo.grid(row=0, column=0, sticky="nw", padx=(15, 15), pady=15)
            
            lbl_texto = ctk.CTkLabel(fila_frame, text=item["preview_text"], anchor="nw", justify="left", wraplength=500)
            lbl_texto.grid(row=0, column=1, sticky="nsew", padx=(0, 15), pady=15)

    def ejecutar_formateo(self):
        version = self.combo_version.get()
        fuente = self.combo_fuente.get()
        
        pregunta = messagebox.askyesnocancel(
            "Alcance del Formato",
            "¿Desea aplicar el formato a TODO el documento?\n\n"
            "SÍ: Todo el documento (Recomendado).\n"
            "NO: Solo los párrafos visibles en esta página.\n"
            "CANCELAR: Abortar proceso."
        )

        if pregunta is None: return 

        indices_a_procesar = None
        if pregunta is False: 
            num_pag = int(self.combo_paginas.get().split(" ")[1])
            inicio = (num_pag - 1) * self.parrafos_por_pagina
            fin = inicio + self.parrafos_por_pagina
            indices_a_procesar = [p["id"] for p in self.datos_documento[inicio:fin]]
        else:
            messagebox.showwarning(
                "Aviso de Automatización",
                "Se aplicará el formato global. Tenga en cuenta que la detección automática "
                "de títulos se basa en los estilos actuales de Word; si un título no fue "
                "etiquetado correctamente en el visor, el resultado podría no ser exacto."
            )

        try:
            ruta_activa = self.lbl_subtitulo.cget("text").replace("Archivo activo: ", "")
            # Se añade la fuente al inicializador del Formatter
            formatter = APAFormatter(ruta_activa, version, fuente, self.datos_documento, ESTILOS_INVERSOS)
            resultado = formatter.procesar(solo_indices=indices_a_procesar)
            
            messagebox.showinfo("Éxito", f"Documento generado exitosamente en:\n{resultado}")
        except Exception as e:
            messagebox.showerror("Error de Formateo", f"No se pudo procesar el archivo: {str(e)}")

if __name__ == "__main__":
    app = DocumentsGoldenSuite()
    app.mainloop()