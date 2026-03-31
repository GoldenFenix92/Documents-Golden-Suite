import customtkinter as ctk

class APAGuideWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("Guía de Formatos APA (7a Edición)")
        self.geometry("600x450")
        self.minsize(500, 400)
        
        # Evitar que el usuario abra multiples ventanas de ayuda
        self.grab_set() 
        
        # Contenedor principal
        main_frame = ctk.CTkScrollableFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(main_frame, text="Manual Rápido: Niveles de Título APA", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(10, 20), anchor="w")
        
        # Diccionario con las reglas para iterar y crear la interfaz dinamicamente
        reglas_apa = [
            ("Título Principal", "Se usa exclusivante para el título general del documento (Portada o inicio del texto). Va centrado, en negrita y cada palabra principal inicia en mayúscula."),
            ("Título 1", "Encabezados principales (Ej. Metodología, Resultados, Discusión). Va centrado, en negrita. El texto inicia en un nuevo párrafo."),
            ("Título 2", "Subsecciones del Título 1 (Ej. Participantes, Instrumentos). Va alineado a la izquierda, en negrita. El texto inicia en un nuevo párrafo."),
            ("Título 3", "Subsecciones del Título 2. Va alineado a la izquierda, en negrita y cursiva. El texto inicia en un nuevo párrafo."),
            ("Párrafo Normal", "Texto base del documento. Lleva interlineado doble, alineación a la izquierda (sin justificar) y sangría de 1.27 cm (media pulgada) en la primera línea de cada párrafo.")
        ]
        
        for titulo, descripcion in reglas_apa:
            card = ctk.CTkFrame(main_frame, fg_color=("gray85", "gray20"), corner_radius=8)
            card.pack(fill="x", pady=8)
            
            ctk.CTkLabel(card, text=titulo, font=ctk.CTkFont(weight="bold", size=14)).pack(anchor="w", padx=15, pady=(15, 5))
            ctk.CTkLabel(card, text=descripcion, justify="left", wraplength=500).pack(anchor="w", padx=15, pady=(0, 15))
            
        btn_cerrar = ctk.CTkButton(self, text="Entendido", command=self.destroy)
        btn_cerrar.pack(pady=10)