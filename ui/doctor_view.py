import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

# Permitir ejecución directa del archivo
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from controller.doctor_controller import DoctorController
from controller.hospital_controller import HospitalController


class DoctorView:
    """
    Vista de Gestión del Personal Médico diseñada para profesionales de la salud.
    """

    def __init__(self, master=None, on_open_hospital_view=None):
        if master is None:
            self.root = tk.Tk()
            self._is_standalone = True
        else:
            self.root = master
            self._is_standalone = False

        self.on_open_hospital_view = on_open_hospital_view
        self.controller = DoctorController()
        self.hospital_controller = HospitalController()
        self.hospitales_map = {}
        self.hospitales_nombre_por_id = {}

        if self._is_standalone:
            self.root.title("Portal Médico - Directorio de Especialistas")
            self.root.geometry("820x680")
            self.root.minsize(700, 540)

        self._build_ui()
        self.cargar_hospitales_combo()
        self._listar_doctores()

    def _build_ui(self):
        # Encabezado clínico
        header_frame = ttk.Frame(self.root, padding=(15, 12))
        header_frame.pack(fill=tk.X)

        title_box = ttk.Frame(header_frame)
        title_box.pack(side=tk.LEFT)

        ttk.Label(
            title_box,
            text="Directorio y Personal Médico",
            font=("Segoe UI", 15, "bold"),
        ).pack(anchor=tk.W)

        ttk.Label(
            title_box,
            text="Registro de especialistas clínicos y asignación a sus centros de atención médica",
            font=("Segoe UI", 9),
            foreground="#555555",
        ).pack(anchor=tk.W)

        if self.on_open_hospital_view:
            ttk.Button(
                header_frame,
                text="Ver Sedes Hospitalarias ➔",
                command=self.on_open_hospital_view,
            ).pack(side=tk.RIGHT, pady=5)

        ttk.Separator(self.root, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=15, pady=(0, 5))

        # Contenedor principal
        main_frame = ttk.Frame(self.root, padding=12)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. Formulario para registrar nuevo especialista
        form_frame = ttk.LabelFrame(main_frame, text=" Registrar Nuevo Especialista ", padding=10)
        form_frame.pack(fill=tk.X, pady=(0, 8))

        # Fila 1: Nombre y Especialidad
        ttk.Label(form_frame, text="Nombre del Médico:").grid(row=0, column=0, sticky=tk.W, padx=4, pady=4)
        self.entry_nombre = ttk.Entry(form_frame, width=28)
        self.entry_nombre.grid(row=0, column=1, sticky=tk.W, padx=6, pady=4)

        ttk.Label(form_frame, text="Especialidad Clínica:").grid(row=0, column=2, sticky=tk.W, padx=4, pady=4)
        self.entry_especialidad = ttk.Entry(form_frame, width=24)
        self.entry_especialidad.grid(row=0, column=3, sticky=tk.W, padx=6, pady=4)

        # Fila 2: Hospital Asignado y Botón Guardar
        ttk.Label(form_frame, text="Centro de Asignación:").grid(row=1, column=0, sticky=tk.W, padx=4, pady=4)
        self.combo_hospital = ttk.Combobox(form_frame, width=26, state="readonly")
        self.combo_hospital.grid(row=1, column=1, sticky=tk.W, padx=6, pady=4)

        btn_guardar = ttk.Button(form_frame, text="Registrar Especialista", command=self._agregar_doctor)
        btn_guardar.grid(row=1, column=3, sticky=tk.E, padx=6, pady=4)

        # 2. Búsqueda de médicos
        search_frame = ttk.LabelFrame(main_frame, text=" Consulta de Especialista ", padding=10)
        search_frame.pack(fill=tk.X, pady=(0, 8))

        ttk.Label(search_frame, text="Código del Médico:").grid(row=0, column=0, sticky=tk.W, padx=4, pady=4)
        self.entry_buscar_id = ttk.Entry(search_frame, width=20)
        self.entry_buscar_id.grid(row=0, column=1, sticky=tk.W, padx=6, pady=4)

        btn_buscar = ttk.Button(search_frame, text="Consultar Ficha", command=self._buscar_doctor)
        btn_buscar.grid(row=0, column=2, padx=6, pady=4)

        # 3. Directorio General de Médicos
        list_frame = ttk.LabelFrame(main_frame, text=" Plantilla Médica Activa ", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 6))

        cols = ("id", "nombre", "especialidad", "hospital")
        self.tree_doctores = ttk.Treeview(list_frame, columns=cols, show="headings", height=10)
        self.tree_doctores.heading("id", text="Código")
        self.tree_doctores.heading("nombre", text="Profesional Médico")
        self.tree_doctores.heading("especialidad", text="Especialidad")
        self.tree_doctores.heading("hospital", text="Centro Hospitalario Asignado")

        self.tree_doctores.column("id", width=70, anchor=tk.CENTER)
        self.tree_doctores.column("nombre", width=260, anchor=tk.W)
        self.tree_doctores.column("especialidad", width=200, anchor=tk.W)
        self.tree_doctores.column("hospital", width=230, anchor=tk.W)

        scroll_d = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree_doctores.yview)
        self.tree_doctores.configure(yscroll=scroll_d.set)

        self.tree_doctores.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_d.pack(side=tk.RIGHT, fill=tk.Y)

        # Barra inferior de control
        bottom_bar = ttk.Frame(main_frame)
        bottom_bar.pack(fill=tk.X, pady=4)

        ttk.Button(bottom_bar, text="🔄 Actualizar Directorio de Médicos", command=self._listar_doctores).pack(side=tk.LEFT)
        self.lbl_status = ttk.Label(bottom_bar, text="", foreground="#666666", font=("Segoe UI", 9, "italic"))
        self.lbl_status.pack(side=tk.RIGHT, padx=5)

    def cargar_hospitales_combo(self):
        try:
            self.hospitales_map.clear()
            self.hospitales_nombre_por_id.clear()
            hospitales = self.hospital_controller.listar_todos()
            opciones = []
            for h in hospitales:
                label = f"{h.hospital_name} (#{h.hospital_id})"
                self.hospitales_map[label] = h.hospital_id
                self.hospitales_nombre_por_id[h.hospital_id] = h.hospital_name
                opciones.append(label)

            self.combo_hospital["values"] = opciones
            if opciones:
                self.combo_hospital.current(0)
        except Exception as e:
            print(f"Error cargando lista de centros hospitalarios: {e}")

    def _agregar_doctor(self):
        nombre = self.entry_nombre.get().strip()
        especialidad = self.entry_especialidad.get().strip()
        hosp_label = self.combo_hospital.get()

        if not nombre:
            messagebox.showwarning("Campo Requerido", "Ingrese el nombre del médico o especialista.")
            return

        if not especialidad:
            messagebox.showwarning("Campo Requerido", "Ingrese la especialidad clínica del profesional.")
            return

        if not hosp_label or hosp_label not in self.hospitales_map:
            messagebox.showwarning("Centro Hospitalario", "Seleccione una institución hospitalaria de la lista.")
            return

        hospital_id = self.hospitales_map[hosp_label]
        hospital_nombre = self.hospitales_nombre_por_id.get(hospital_id, f"Hospital #{hospital_id}")

        try:
            nuevo_id = self.controller.agregar(nombre, especialidad, hospital_id)
            messagebox.showinfo(
                "Especialista Registrado",
                f"El profesional '{nombre}' ({especialidad}) ha sido asignado a '{hospital_nombre}' exitosamente.\n"
                f"Código de registro: #{nuevo_id}",
            )
            self.entry_nombre.delete(0, tk.END)
            self.entry_especialidad.delete(0, tk.END)
            self._listar_doctores()
        except Exception as e:
            messagebox.showerror("Error al Guardar", f"No fue posible registrar al médico:\n{e}")

    def _buscar_doctor(self):
        id_str = self.entry_buscar_id.get().strip()
        if not id_str:
            messagebox.showwarning("Búsqueda", "Ingrese el código numérico del médico a consultar.")
            return

        try:
            doctor = self.controller.obtener_por_id(id_str)
            if doctor:
                h_nombre = self.hospitales_nombre_por_id.get(doctor.hospital_id, f"Hospital #{doctor.hospital_id}")
                # Resaltar en la lista
                for item in self.tree_doctores.get_children():
                    if str(self.tree_doctores.item(item)["values"][0]) == str(doctor.doctor_id):
                        self.tree_doctores.selection_set(item)
                        self.tree_doctores.see(item)
                        break

                messagebox.showinfo(
                    "Ficha del Profesional Médico",
                    f"Código: #{doctor.doctor_id}\n"
                    f"Profesional: {doctor.doctor_name}\n"
                    f"Especialidad: {doctor.speciality}\n"
                    f"Centro Asignado: {h_nombre}",
                )
            else:
                messagebox.showinfo(
                    "Sin Resultados",
                    f"No se encontró ningún médico registrado con el código #{id_str}.",
                )
        except Exception as e:
            messagebox.showerror("Error en Consulta", f"Ocurrió un error al buscar el médico:\n{e}")

    def _listar_doctores(self):
        for item in self.tree_doctores.get_children():
            self.tree_doctores.delete(item)
        try:
            self.cargar_hospitales_combo()
            doctores = self.controller.listar_todos()
            for d in doctores:
                h_nombre = self.hospitales_nombre_por_id.get(d.hospital_id, f"Sede #{d.hospital_id}")
                self.tree_doctores.insert(
                    "",
                    tk.END,
                    values=(d.doctor_id, d.doctor_name, d.speciality, h_nombre),
                )
            self.lbl_status.config(text=f"Total de especialistas registrados: {len(doctores)}")
        except Exception as e:
            messagebox.showerror("Error de Conexión", f"No se pudo cargar el directorio de médicos:\n{e}")

    def run(self):
        if self._is_standalone:
            self.root.mainloop()


if __name__ == "__main__":
    app = DoctorView()
    app.run()
