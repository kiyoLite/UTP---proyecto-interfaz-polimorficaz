import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

# Permitir ejecución directa del archivo
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from controller.hospital_controller import HospitalController


class HospitalView:
    """
    Vista de Gestión de Centros Hospitalarios diseñada para personal médico y administrativo.
    """

    def __init__(self, master=None, on_open_doctor_view=None):
        if master is None:
            self.root = tk.Tk()
            self._is_standalone = True
        else:
            self.root = master
            self._is_standalone = False

        self.on_open_doctor_view = on_open_doctor_view
        self.controller = HospitalController()

        if self._is_standalone:
            self.root.title("Portal Médico - Directorio de Hospitales")
            self.root.geometry("820x680")
            self.root.minsize(700, 540)

        self._build_ui()
        self._listar_hospitales()

    def _build_ui(self):
        # Encabezado clínico
        header_frame = ttk.Frame(self.root, padding=(15, 12))
        header_frame.pack(fill=tk.X)

        title_box = ttk.Frame(header_frame)
        title_box.pack(side=tk.LEFT)

        ttk.Label(
            title_box,
            text="Directorio y Sedes Hospitalarias",
            font=("Segoe UI", 15, "bold"),
        ).pack(anchor=tk.W)

        ttk.Label(
            title_box,
            text="Administración de instituciones médicas y consulta de su equipo de especialistas",
            font=("Segoe UI", 9),
            foreground="#555555",
        ).pack(anchor=tk.W)

        if self.on_open_doctor_view:
            ttk.Button(
                header_frame,
                text="Ver Directorio Médico ➔",
                command=self.on_open_doctor_view,
            ).pack(side=tk.RIGHT, pady=5)

        ttk.Separator(self.root, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=15, pady=(0, 5))

        # Contenedor principal
        main_frame = ttk.Frame(self.root, padding=12)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Barra superior: Registro y Búsqueda en dos paneles organizados
        top_panels = ttk.Frame(main_frame)
        top_panels.pack(fill=tk.X, pady=(0, 8))

        # Panel 1: Registrar nuevo centro
        new_frame = ttk.LabelFrame(top_panels, text=" Registrar Nueva Sede Hospitalaria ", padding=10)
        new_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))

        ttk.Label(new_frame, text="Nombre de la Institución:").grid(row=0, column=0, sticky=tk.W, pady=4)
        self.entry_nombre = ttk.Entry(new_frame, width=32)
        self.entry_nombre.grid(row=0, column=1, sticky=tk.EW, padx=6, pady=4)

        btn_guardar = ttk.Button(new_frame, text="Registrar Hospital", command=self._agregar_hospital)
        btn_guardar.grid(row=0, column=2, padx=4, pady=4)

        # Panel 2: Búsqueda rápida
        search_frame = ttk.LabelFrame(top_panels, text=" Búsqueda de Institución ", padding=10)
        search_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(6, 0))

        ttk.Label(search_frame, text="Nombre o Código:").grid(row=0, column=0, sticky=tk.W, pady=4)
        self.entry_buscar = ttk.Entry(search_frame, width=22)
        self.entry_buscar.grid(row=0, column=1, sticky=tk.EW, padx=6, pady=4)

        btn_buscar = ttk.Button(search_frame, text="Consultar", command=self._buscar_hospital)
        btn_buscar.grid(row=0, column=2, padx=4, pady=4)

        # Directorio de Hospitales
        list_frame = ttk.LabelFrame(main_frame, text=" Red de Hospitales Disponibles ", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

        cols = ("id", "nombre", "doctores")
        self.tree_hospitales = ttk.Treeview(list_frame, columns=cols, show="headings", height=5)
        self.tree_hospitales.heading("id", text="Código")
        self.tree_hospitales.heading("nombre", text="Institución Hospitalaria")
        self.tree_hospitales.heading("doctores", text="Especialistas Asignados")

        self.tree_hospitales.column("id", width=70, anchor=tk.CENTER)
        self.tree_hospitales.column("nombre", width=450, anchor=tk.W)
        self.tree_hospitales.column("doctores", width=160, anchor=tk.CENTER)

        scroll_h = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree_hospitales.yview)
        self.tree_hospitales.configure(yscroll=scroll_h.set)

        self.tree_hospitales.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_h.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree_hospitales.bind("<<TreeviewSelect>>", self._on_hospital_select)

        # Barra de acción de la tabla
        table_bar = ttk.Frame(main_frame)
        table_bar.pack(fill=tk.X, pady=(0, 6))

        ttk.Button(table_bar, text="🔄 Actualizar Directorio", command=self._listar_hospitales).pack(side=tk.LEFT)
        self.lbl_info_seleccion = ttk.Label(
            table_bar,
            text="Haga clic en una sede para ver su personal médico en el panel inferior.",
            foreground="#666666",
            font=("Segoe UI", 9, "italic"),
        )
        self.lbl_info_seleccion.pack(side=tk.RIGHT, padx=5)

        # Panel Detalle: Personal Médico Asignado a la Sede
        self.detail_frame = ttk.LabelFrame(
            main_frame,
            text=" Personal Médico Asignado al Centro Seleccionado ",
            padding=10,
        )
        self.detail_frame.pack(fill=tk.BOTH, expand=True)

        doc_cols = ("nombre", "especialidad")
        self.tree_doctores = ttk.Treeview(self.detail_frame, columns=doc_cols, show="headings", height=4)
        self.tree_doctores.heading("nombre", text="Profesional Médico")
        self.tree_doctores.heading("especialidad", text="Especialidad Clínica")
        self.tree_doctores.column("nombre", width=360, anchor=tk.W)
        self.tree_doctores.column("especialidad", width=360, anchor=tk.W)

        scroll_d = ttk.Scrollbar(self.detail_frame, orient=tk.VERTICAL, command=self.tree_doctores.yview)
        self.tree_doctores.configure(yscroll=scroll_d.set)

        self.tree_doctores.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_d.pack(side=tk.RIGHT, fill=tk.Y)

    def _agregar_hospital(self):
        nombre = self.entry_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Campo Requerido", "Por favor ingrese el nombre del centro hospitalario.")
            return

        try:
            nuevo_id = self.controller.agregar(nombre)
            messagebox.showinfo(
                "Centro Registrado",
                f"El centro hospitalario '{nombre}' ha sido registrado exitosamente con el código #{nuevo_id}.",
            )
            self.entry_nombre.delete(0, tk.END)
            self._listar_hospitales()
        except Exception as e:
            messagebox.showerror("Error de Registro", f"No fue posible guardar el hospital:\n{e}")

    def _buscar_hospital(self):
        criterio = self.entry_buscar.get().strip()
        if not criterio:
            messagebox.showwarning("Búsqueda", "Ingrese el nombre o código del centro que desea consultar.")
            return

        try:
            hospital = self.controller.obtener_por_id(criterio)
            if hospital:
                self._mostrar_doctores_en_detalle(hospital.hospital_name, hospital.doctors)
                # Seleccionar visualmente en la tabla si existe
                for item in self.tree_hospitales.get_children():
                    if str(self.tree_hospitales.item(item)["values"][0]) == str(hospital.hospital_id):
                        self.tree_hospitales.selection_set(item)
                        self.tree_hospitales.see(item)
                        break
                messagebox.showinfo(
                    "Centro Hospitalario Encontrado",
                    f"Institución: {hospital.hospital_name}\n"
                    f"Código de registro: #{hospital.hospital_id}\n"
                    f"Especialistas en sede: {len(hospital.doctors)}",
                )
            else:
                messagebox.showinfo(
                    "Sin Resultados",
                    f"No se encontró ninguna institución médica registrada con '{criterio}'.",
                )
        except Exception as e:
            messagebox.showerror("Error en Consulta", f"Ocurrió un error al realizar la búsqueda:\n{e}")

    def _listar_hospitales(self):
        for item in self.tree_hospitales.get_children():
            self.tree_hospitales.delete(item)
        try:
            hospitales = self.controller.listar_todos()
            for h in hospitales:
                self.tree_hospitales.insert(
                    "",
                    tk.END,
                    values=(h.hospital_id, h.hospital_name, f"{len(h.doctors)} profesional(es)"),
                )
            self.lbl_info_seleccion.config(
                text=f"Total de centros activos: {len(hospitales)} | Haga clic en una sede para ver sus especialistas."
            )
        except Exception as e:
            messagebox.showerror("Error de Conexión", f"No se pudo cargar la red de hospitales:\n{e}")

    def _on_hospital_select(self, event):
        seleccion = self.tree_hospitales.selection()
        if not seleccion:
            return
        item = self.tree_hospitales.item(seleccion[0])
        h_id = item["values"][0]
        h_nombre = item["values"][1]
        hospital = self.controller.obtener_por_id(h_id)
        if hospital:
            self._mostrar_doctores_en_detalle(h_nombre, hospital.doctors)

    def _mostrar_doctores_en_detalle(self, nombre_hospital, doctores):
        self.detail_frame.config(text=f" Especialistas asignados a: {nombre_hospital} ({len(doctores)} médicos) ")
        for row in self.tree_doctores.get_children():
            self.tree_doctores.delete(row)

        if not doctores:
            self.tree_doctores.insert("", tk.END, values=("(Sin médicos asignados actualmente)", "-"))
            return

        for doc in doctores:
            self.tree_doctores.insert("", tk.END, values=(doc.doctor_name, doc.speciality))

    def run(self):
        if self._is_standalone:
            self.root.mainloop()


if __name__ == "__main__":
    app = HospitalView()
    app.run()
