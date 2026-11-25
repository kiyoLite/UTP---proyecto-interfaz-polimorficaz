import tkinter as tk
from tkinter import ttk
from ui.hospital_view import HospitalView
from ui.doctor_view import DoctorView


class MainWindow:
    """
    Componente Principal del Sistema de Información Hospitalaria.
    Proporciona un entorno unificado con navegación por pestañas para el personal médico.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión Hospitalaria (SGH) - Portal Médico")
        self.root.geometry("860x700")
        self.root.minsize(740, 580)

        self._configure_theme()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        frame_hospital = ttk.Frame(self.notebook)
        frame_doctor = ttk.Frame(self.notebook)

        self.notebook.add(frame_hospital, text=" 🏥 Centros Hospitalarios ")
        self.notebook.add(frame_doctor, text=" 🩺 Directorio de Especialistas ")

        # Instanciar vistas modulares pasando callbacks de navegación fluida
        self.hospital_view = HospitalView(
            master=frame_hospital,
            on_open_doctor_view=lambda: self.notebook.select(1),
        )
        self.doctor_view = DoctorView(
            master=frame_doctor,
            on_open_hospital_view=lambda: self.notebook.select(0),
        )

    def _configure_theme(self):
        style = ttk.Style()
        # Usar un tema nativo limpio
        disponibles = style.theme_names()
        if "vista" in disponibles:
            style.theme_use("vista")
        elif "clam" in disponibles:
            style.theme_use("clam")

        # Configuración estética global
        style.configure("TLabel", font=("Segoe UI", 9))
        style.configure("TButton", font=("Segoe UI", 9), padding=5)
        style.configure("TLabelframe.Label", font=("Segoe UI", 9, "bold"))
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=24)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
