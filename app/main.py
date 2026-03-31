import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog

# Configuracion global del tema inicial
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class DocumentsGoldenSuite(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuracion de la ventana principal
        self.title("Documents Golden Suite - Formateador APA")
        self.geometry("700x500")
        self.minsize(600, 400)

        # GRID LAYOUT PRINCIPAL
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # 1. Cabecera (Frame superior para titulo y switch de tema)
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="ew")
        self.top_frame.grid_columnconfigure(0, weight=1)

        self.lbl_titulo = ctk.CTkLabel(self.top_frame, text="Formateador APA Auto", font=ctk.CTkFont(size=24, weight="bold"))
        self.lbl_titulo.grid(row=0, column=0, sticky="w")

        # Menu desplegable para el cambio de tema manual
        self.theme_menu = ctk.CTkOptionMenu(self.top_frame, values=["System", "Dark", "Light"],
                                            command=self.cambiar_tema, width=100)
        self.theme_menu.grid(row=0, column=1, sticky="e")

        self.lbl_subtitulo = ctk.CTkLabel(self, text="Selecciona un documento .docx para analizar y aplicar formato", text_color="gray")
        self.lbl_subtitulo.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")

        # 2. Visor Logico (Scrollable Frame donde iran los parrafos detectados)
        self.visor_frame = ctk.CTkScrollableFrame(self, label_text="Visor de Estilos Detectados")
        self.visor_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        # Mensaje temporal dentro del visor
        self.lbl_placeholder = ctk.CTkLabel(self.visor_frame, text="Carga un documento para ver los estilos aqui.")
        self.lbl_placeholder.pack(pady=50)

        # 3. Panel Inferior (Controles)
        self.panel_inferior = ctk.CTkFrame(self, fg_color="transparent")
        self.panel_inferior.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
        self.panel_inferior.grid_columnconfigure(0, weight=1)
        self.panel_inferior.grid_columnconfigure(1, weight=1)

        # Selector de Version APA
        self.combo_version = ctk.CTkComboBox(self.panel_inferior, values=["APA 7a Edicion", "APA 6a Edicion"])
        self.combo_version.grid(row=0, column=0, padx=(0, 10), sticky="w")

        # Boton para cargar archivo
        self.btn_cargar = ctk.CTkButton(self.panel_inferior, text="Explorar y Cargar .docx", command=self.cargar_archivo)
        self.btn_cargar.grid(row=0, column=1, padx=10, sticky="e")

        # Boton para aplicar formato (Deshabilitado por defecto)
        self.btn_procesar = ctk.CTkButton(self.panel_inferior, text="Aplicar Formato", state="disabled", fg_color="green", hover_color="darkgreen")
        self.btn_procesar.grid(row=0, column=2, padx=(10, 0), sticky="e")

    def cambiar_tema(self, nuevo_modo: str):
        # Funcion que aplica el cambio de tema visual
        ctk.set_appearance_mode(nuevo_modo)

    def cargar_archivo(self):
        # Abre el explorador de archivos nativo
        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar documento de Word",
            filetypes=[("Documentos de Word", "*.docx")]
        )
        
        if ruta_archivo:
            print(f"Archivo seleccionado: {ruta_archivo}")
            self.lbl_placeholder.configure(text=f"Archivo cargado:\n{ruta_archivo}\n\n(Pronto: Analisis de estilos en esta area)")
            self.btn_procesar.configure(state="normal")

if __name__ == "__main__":
    app = DocumentsGoldenSuite()
    app.mainloop()