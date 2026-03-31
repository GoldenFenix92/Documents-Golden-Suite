import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from core.document_parser import DocumentParser

# Configuracion global del tema inicial
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class DocumentsGoldenSuite(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Variables de estado para la paginacion
        self.datos_documento = []
        self.parrafos_por_pagina = 15  # Cantidad de parrafos a mostrar por "hoja"

        # Configuracion de la ventana principal
        self.title("Documents Golden Suite - Formateador APA")
        self.geometry("750x550")
        self.minsize(600, 450)

        # GRID LAYOUT PRINCIPAL
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1) # El frame del visor es ahora la fila 3

        # 1. Cabecera (Frame superior)
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="ew")
        self.top_frame.grid_columnconfigure(0, weight=1)

        self.lbl_titulo = ctk.CTkLabel(self.top_frame, text="Formateador APA Auto", font=ctk.CTkFont(size=24, weight="bold"))
        self.lbl_titulo.grid(row=0, column=0, sticky="w")

        self.theme_menu = ctk.CTkOptionMenu(self.top_frame, values=["System", "Dark", "Light"], command=self.cambiar_tema, width=100)
        self.theme_menu.grid(row=0, column=1, sticky="e")

        self.lbl_subtitulo = ctk.CTkLabel(self, text="Selecciona un documento .docx para analizar y aplicar formato", text_color="gray")
        self.lbl_subtitulo.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")

        # 2. Barra de Paginacion (NUEVO)
        self.paginacion_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.paginacion_frame.grid(row=2, column=0, padx=20, pady=(0, 5), sticky="ew")
        
        self.lbl_pagina_actual = ctk.CTkLabel(self.paginacion_frame, text="Hoja / Bloque:", font=ctk.CTkFont(weight="bold"))
        self.lbl_pagina_actual.pack(side="left", padx=(0, 10))

        self.combo_paginas = ctk.CTkOptionMenu(self.paginacion_frame, values=["-"], state="disabled", command=self.cambiar_pagina)
        self.combo_paginas.pack(side="left")

        # 3. Visor Logico (Scrollable Frame)
        self.visor_frame = ctk.CTkScrollableFrame(self, label_text="Visor de Estilos Detectados")
        self.visor_frame.grid(row=3, column=0, padx=20, pady=5, sticky="nsew")

        self.lbl_placeholder = ctk.CTkLabel(self.visor_frame, text="Carga un documento para ver los estilos aqui.")
        self.lbl_placeholder.pack(pady=50)

        # 4. Panel Inferior (Controles)
        self.panel_inferior = ctk.CTkFrame(self, fg_color="transparent")
        self.panel_inferior.grid(row=4, column=0, padx=20, pady=20, sticky="ew")
        self.panel_inferior.grid_columnconfigure(0, weight=1)
        self.panel_inferior.grid_columnconfigure(1, weight=1)

        self.combo_version = ctk.CTkComboBox(self.panel_inferior, values=["APA 7a Edicion", "APA 6a Edicion"])
        self.combo_version.grid(row=0, column=0, padx=(0, 10), sticky="w")

        self.btn_cargar = ctk.CTkButton(self.panel_inferior, text="Explorar y Cargar .docx", command=self.cargar_archivo)
        self.btn_cargar.grid(row=0, column=1, padx=10, sticky="e")

        self.btn_procesar = ctk.CTkButton(self.panel_inferior, text="Aplicar Formato", state="disabled", fg_color="green", hover_color="darkgreen")
        self.btn_procesar.grid(row=0, column=2, padx=(10, 0), sticky="e")

    def cambiar_tema(self, nuevo_modo: str):
        ctk.set_appearance_mode(nuevo_modo)

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
                    ctk.CTkLabel(self.visor_frame, text="El documento esta vacio.").pack(pady=20)
                    return

                # Calcular total de paginas/bloques
                import math
                total_paginas = math.ceil(len(self.datos_documento) / self.parrafos_por_pagina)
                opciones_paginas = [f"Página {i+1} de {total_paginas}" for i in range(total_paginas)]
                
                # Configurar el menu desplegable de paginas
                self.combo_paginas.configure(values=opciones_paginas, state="normal")
                self.combo_paginas.set(opciones_paginas[0])
                
                # Renderizar la primera pagina
                self.btn_procesar.configure(state="normal")
                self.cambiar_pagina(opciones_paginas[0])
                
            except Exception as e:
                import tkinter.messagebox as messagebox
                messagebox.showerror("Error de Lectura", str(e))

    def limpiar_visor(self):
        for widget in self.visor_frame.winfo_children():
            widget.destroy()

    def cambiar_pagina(self, seleccion: str):
        # Extraer el numero de pagina seleccionado (Ej: de "Página 2 de 5" extrae el int 2)
        numero_pagina = int(seleccion.split(" ")[1])
        
        # Calcular los indices de inicio y fin para hacer un slice de la lista
        indice_inicio = (numero_pagina - 1) * self.parrafos_por_pagina
        indice_fin = indice_inicio + self.parrafos_por_pagina
        
        datos_pagina_actual = self.datos_documento[indice_inicio:indice_fin]
        
        self.limpiar_visor()
        
        estilos_permitidos = ["Normal", "Heading 1", "Heading 2", "Heading 3", "Title", "Subtitle"]

        # Renderizar solo los parrafos correspondientes a este bloque
        for item in datos_pagina_actual:
            fila_frame = ctk.CTkFrame(self.visor_frame, fg_color="transparent")
            fila_frame.pack(fill="x", pady=2, padx=5)
            fila_frame.grid_columnconfigure(0, weight=1)
            
            lbl_texto = ctk.CTkLabel(fila_frame, text=item["preview_text"], anchor="w", justify="left")
            lbl_texto.grid(row=0, column=0, sticky="ew", padx=(0, 10))
            
            estilo_actual = item["current_style"]
            if estilo_actual not in estilos_permitidos:
                estilos_permitidos.append(estilo_actual)
                
            combo_estilo = ctk.CTkComboBox(fila_frame, values=estilos_permitidos, width=150)
            combo_estilo.set(estilo_actual)
            combo_estilo.grid(row=0, column=1, sticky="e")

if __name__ == "__main__":
    app = DocumentsGoldenSuite()
    app.mainloop()