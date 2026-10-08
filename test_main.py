"""
Pruebas automatizadas del Sistema Club Salud.
Ejecutar con: pytest -v test_main.py
"""

import sys
import types


# ---------------------------------------------------------------------
# Doble de prueba para Tkinter.
# Permite importar main.py sin abrir la ventana gráfica durante pytest.
# ---------------------------------------------------------------------
class DummyWidget:
    def __init__(self, *args, **kwargs):
        self.value = ""

    def pack(self, *args, **kwargs):
        pass

    def grid(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        self.value = ""

    def insert(self, *args, **kwargs):
        pass

    def get(self):
        return self.value

    def curselection(self):
        return ()

    def destroy(self):
        pass

    def title(self, *args, **kwargs):
        pass

    def geometry(self, *args, **kwargs):
        pass


class DummyTk(DummyWidget):
    def mainloop(self):
        # Evita bloquear pytest.
        pass


fake_tk = types.ModuleType("tkinter")
fake_tk.Tk = DummyTk
fake_tk.Toplevel = DummyWidget
fake_tk.Label = DummyWidget
fake_tk.LabelFrame = DummyWidget
fake_tk.Frame = DummyWidget
fake_tk.Entry = DummyWidget
fake_tk.Button = DummyWidget
fake_tk.Listbox = DummyWidget
fake_tk.END = "end"

fake_messagebox = types.SimpleNamespace(
    showwarning=lambda *args, **kwargs: None,
    showerror=lambda *args, **kwargs: None,
    showinfo=lambda *args, **kwargs: None,
)

fake_simpledialog = types.SimpleNamespace(
    askstring=lambda *args, **kwargs: None,
)

fake_tk.messagebox = fake_messagebox
fake_tk.simpledialog = fake_simpledialog

sys.modules["tkinter"] = fake_tk


import SistemaFinal as main

# ---------------------------------------------------------------------
# Validaciones de datos
# ---------------------------------------------------------------------

def test_validar_dni_correcto():
    assert main.validar_dni("12345678") is True


def test_validar_dni_incorrecto():
    assert main.validar_dni("1234567") is False
    assert main.validar_dni("123456789") is False
    assert main.validar_dni("1234ABCD") is False


def test_validar_telefono_correcto():
    assert main.validar_telefono("987654321") is True


def test_validar_telefono_incorrecto():
    assert main.validar_telefono("98765432") is False
    assert main.validar_telefono("9876543210") is False
    assert main.validar_telefono("98765ABCD") is False


def test_validar_fecha():
    assert main.validar_fecha("25/09/2026") is True
    assert main.validar_fecha("31/02/2026") is False
    assert main.validar_fecha("2026-09-25") is False


def test_validar_hora():
    assert main.validar_hora("09:30") is True
    assert main.validar_hora("25:00") is False
    assert main.validar_hora("9:30") is False


def test_validar_campos_obligatorios():
    assert main.validar_campos_obligatorios(
        ["Camila", "12345678", "987654321"]
    ) is True

    assert main.validar_campos_obligatorios(
        ["Camila", "", "987654321"]
    ) is False


# ---------------------------------------------------------------------
# Protección básica de datos
# ---------------------------------------------------------------------

def test_ocultar_dni():
    assert main.ocultar_dni("12345678") == "****5678"


def test_ocultar_telefono():
    assert main.ocultar_telefono("987654321") == "******321"


# ---------------------------------------------------------------------
# Clases, encapsulamiento y relaciones
# ---------------------------------------------------------------------

def crear_paciente(codigo="P001", dni="12345678", nombre="Ana Torres"):
    return main.Paciente(
        codigo,
        nombre,
        dni,
        "Dirección ficticia",
        "987654321",
        25,
        "F",
        "10/05/2001",
        "Cajamarca",
        "Universitario",
        "Soltera",
        "Estudiante",
        "María Torres",
        "Madre",
        "999888777",
    )


def test_paciente_getters():
    paciente = crear_paciente()

    assert paciente.get_codigo() == "P001"
    assert paciente.get_nombre() == "Ana Torres"
    assert paciente.get_dni() == "12345678"
    assert paciente.get_edad() == 25


def test_medico_getters():
    medico = main.Medico("M999", "Dr. Prueba", "Medicina General")

    assert medico.get_codigo() == "M999"
    assert medico.get_nombre() == "Dr. Prueba"
    assert medico.get_especialidad() == "Medicina General"


def test_cita_y_estado():
    paciente = crear_paciente()
    medico = main.Medico("M999", "Dr. Prueba", "Medicina General")
    cita = main.Cita(
        "C001",
        paciente,
        medico,
        "25/09/2026",
        "09:00",
    )

    assert cita.get_codigo() == "C001"
    assert cita.get_paciente() is paciente
    assert cita.get_medico() is medico
    assert cita.get_estado() == "Programada"

    cita.cambiar_estado("Cancelada")
    assert cita.get_estado() == "Cancelada"


# ---------------------------------------------------------------------
# Programación funcional: filter, map y reduce
# ---------------------------------------------------------------------

def test_busqueda_paciente_por_dni():
    paciente = crear_paciente(
        codigo="TEST-DNI",
        dni="87654321",
        nombre="Paciente Prueba",
    )

    original = list(main.pacientes)
    try:
        main.pacientes.append(paciente)

        encontrado = main.buscar_paciente_por_dni("87654321")
        no_encontrado = main.buscar_paciente_por_dni("00000000")

        assert encontrado is paciente
        assert no_encontrado is None
    finally:
        main.pacientes[:] = original


def test_busqueda_paciente_por_nombre():
    paciente = crear_paciente(
        codigo="TEST-NOMBRE",
        dni="11223344",
        nombre="Luciana Morales",
    )

    original = list(main.pacientes)
    try:
        main.pacientes.append(paciente)

        resultados = main.buscar_paciente_por_nombre("luciana")

        assert paciente in resultados
    finally:
        main.pacientes[:] = original


def test_map_nombres_pacientes():
    original = list(main.pacientes)
    try:
        main.pacientes[:] = [
            crear_paciente("P101", "11111111", "Ana"),
            crear_paciente("P102", "22222222", "Luis"),
        ]

        assert main.obtener_nombres_pacientes() == ["Ana", "Luis"]
    finally:
        main.pacientes[:] = original


def test_reduce_contar_atenciones():
    original = list(main.atenciones)
    try:
        main.atenciones.clear()

        paciente = crear_paciente()
        medico = main.Medico("M900", "Dr. Test", "Medicina General")

        main.atenciones.extend([
            main.AtencionMedica(
                "A001", paciente, medico, "25/09/2026",
                "Control", "Diagnóstico 1", "Tratamiento 1"
            ),
            main.AtencionMedica(
                "A002", paciente, medico, "26/09/2026",
                "Control", "Diagnóstico 2", "Tratamiento 2"
            ),
        ])

        assert main.contar_atenciones() == 2
    finally:
        main.atenciones[:] = original


# ---------------------------------------------------------------------
# Disponibilidad de citas: componente técnico crítico
# ---------------------------------------------------------------------

def test_verificar_disponibilidad_horario_libre():
    original = list(main.citas)
    try:
        main.citas.clear()

        medico = main.Medico("M800", "Dr. Disponible", "Medicina General")

        assert main.verificar_disponibilidad(
            medico,
            "25/09/2026",
            "09:00",
        ) is True
    finally:
        main.citas[:] = original


def test_verificar_disponibilidad_horario_ocupado():
    original = list(main.citas)
    try:
        main.citas.clear()

        paciente = crear_paciente()
        medico = main.Medico("M801", "Dr. Ocupado", "Medicina General")

        main.citas.append(
            main.Cita(
                "C900",
                paciente,
                medico,
                "25/09/2026",
                "09:00",
            )
        )

        assert main.verificar_disponibilidad(
            medico,
            "25/09/2026",
            "09:00",
        ) is False
    finally:
        main.citas[:] = original


def test_verificar_disponibilidad_otro_horario():
    original = list(main.citas)
    try:
        main.citas.clear()

        paciente = crear_paciente()
        medico = main.Medico("M802", "Dr. Horario", "Medicina General")

        main.citas.append(
            main.Cita(
                "C901",
                paciente,
                medico,
                "25/09/2026",
                "09:00",
            )
        )

        assert main.verificar_disponibilidad(
            medico,
            "25/09/2026",
            "10:00",
        ) is True
    finally:
        main.citas[:] = original


# ---------------------------------------------------------------------
# Singleton
# ---------------------------------------------------------------------

def test_gestor_clinica_singleton():
    gestor_1 = main.GestorClinica()
    gestor_2 = main.GestorClinica()

    assert gestor_1 is gestor_2


# ---------------------------------------------------------------------
# Generación de códigos
# ---------------------------------------------------------------------

def test_generar_codigo_paciente():
    original = list(main.pacientes)
    try:
        main.pacientes.clear()
        assert main.generar_codigo_paciente() == "P001"

        main.pacientes.append(crear_paciente())
        assert main.generar_codigo_paciente() == "P002"
    finally:
        main.pacientes[:] = original
