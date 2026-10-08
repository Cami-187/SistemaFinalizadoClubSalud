# PRIVACIDAD: las búsquedas públicas muestran el DNI parcialmente oculto.
# PROTOTIPO ACADÉMICO: los datos se conservan en memoria durante la ejecución.
# Para uso real con datos clínicos se requieren autenticación, autorización,
# cifrado de almacenamiento, control de accesos y medidas legales adicionales.

import tkinter as tk
from tkinter import messagebox, simpledialog
from functools import reduce
from datetime import datetime
import re
import logging
import os
import hmac


# SISTEMA CLUB SALUD
# Sistema de gestión de pacientes, citas y atenciones médicas
#
# PARADIGMAS UTILIZADOS:
# 1. Programación Orientada a Objetos (POO)
# 2. Programación Funcional
# 3. Programación Estructurada


# Validaciones independientes de la interfaz (SRP y pruebas unitarias).
# VALIDACIONES Y PROTECCION BASICA DE DATOS
def validar_dni(dni):
    return bool(re.fullmatch(r"[0-9]{8}", dni))


def validar_telefono(telefono):
    return bool(re.fullmatch(r"[0-9]{9}", telefono))


def validar_fecha(fecha):
    try:
        datetime.strptime(fecha, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def validar_hora(hora):
    try:
        datetime.strptime(hora, "%H:%M")
        return bool(re.fullmatch(r"[0-9]{2}:[0-9]{2}", hora))
    except ValueError:
        return False


def ocultar_dni(dni):
    return "****" + dni[-4:]


# Clave de acceso definida fuera del codigo (variable de entorno).
# No se guarda la contrasena en el programa ni se muestra al escribirla.
def autorizar_acceso_clinico():
    clave_configurada = os.environ.get("CLUB_SALUD_CLAVE_MEDICA", "")
    if not clave_configurada:
        messagebox.showwarning(
            "Acceso no configurado",
            "Configure CLUB_SALUD_CLAVE_MEDICA antes de consultar datos clinicos."
        )
        return False
    clave_ingresada = simpledialog.askstring(
        "Acceso restringido", "Ingrese la clave del personal autorizado:", show="*"
    )
    if clave_ingresada is None:
        return False
    if not hmac.compare_digest(clave_ingresada, clave_configurada):
        messagebox.showerror("Acceso denegado", "Clave incorrecta.")
        return False
    return True


def ocultar_telefono(numero):
    return "*" * max(0, len(numero) - 3) + numero[-3:]


logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")


# CLASE PACIENTE
# RF01: Registrar pacientes
# RF04: Consultar información clínica autorizada

# HERENCIA: Paciente y Medico comparten los datos basicos de Persona.
# 1. MODELOS Y CLASES
class Persona:
    def __init__(self, nombre):
        self._nombre = nombre

    def get_nombre(self):
        return self._nombre


class Paciente(Persona):

    def __init__(
        self,
        codigo,
        nombre,
        dni,
        direccion,
        telefono,
        edad,
        sexo,
        fecha_nacimiento,
        procedencia,
        grado_instruccion,
        estado_civil,
        ocupacion,
        acompanante,
        parentesco,
        telefono_acompanante
    ):

        super().__init__(nombre)
        self.__codigo = codigo
        self.__nombre = nombre
        self.__dni = dni
        self.__direccion = direccion
        self.__telefono = telefono
        self.__edad = edad
        self.__sexo = sexo
        self.__fecha_nacimiento = fecha_nacimiento
        self.__procedencia = procedencia
        self.__grado_instruccion = grado_instruccion
        self.__estado_civil = estado_civil
        self.__ocupacion = ocupacion
        self.__acompanante = acompanante
        self.__parentesco = parentesco
        self.__telefono_acompanante = telefono_acompanante

    # --------------------------------------------------------
    # GETTERS
    # --------------------------------------------------------

    def get_codigo(self):
        return self.__codigo

    def get_nombre(self):
        return self.__nombre

    def get_dni(self):
        return self.__dni

    def get_direccion(self):
        return self.__direccion

    def get_telefono(self):
        return self.__telefono

    def get_edad(self):
        return self.__edad

    def get_sexo(self):
        return self.__sexo

    def get_fecha_nacimiento(self):
        return self.__fecha_nacimiento

    def get_procedencia(self):
        return self.__procedencia

    def get_grado_instruccion(self):
        return self.__grado_instruccion

    def get_estado_civil(self):
        return self.__estado_civil

    def get_ocupacion(self):
        return self.__ocupacion

    def get_acompanante(self):
        return self.__acompanante

    def get_parentesco(self):
        return self.__parentesco

    def get_telefono_acompanante(self):
        return self.__telefono_acompanante

    # --------------------------------------------------------
    # MÉTODO DE PRESENTACIÓN
    # --------------------------------------------------------

    def mostrar_datos(self):

        return (
            "Código: " + self.__codigo
            + "\nNombre: " + self.__nombre
            + "\nDNI: " + ocultar_dni(self.__dni)
            + "\nDirección: [dato reservado]"
            + "\nTeléfono: " + ocultar_telefono(self.__telefono)
            + "\nEdad: " + str(self.__edad)
            + "\nSexo: " + self.__sexo
            + "\nFecha de nacimiento: "
            + self.__fecha_nacimiento
            + "\nProcedencia: " + self.__procedencia
            + "\nGrado de instrucción: "
            + self.__grado_instruccion
            + "\nEstado civil: "
            + self.__estado_civil
            + "\nOcupación: " + self.__ocupacion
            + "\nAcompañante: " + self.__acompanante
            + "\nParentesco: " + self.__parentesco
            + "\nTeléfono acompañante: "
            + ocultar_telefono(self.__telefono_acompanante)
        )

# CLASE MÉDICO

class Medico(Persona):

    def __init__(self, codigo, nombre, especialidad):

        super().__init__(nombre)
        self.__codigo = codigo
        self.__nombre = nombre
        self.__especialidad = especialidad

    def get_codigo(self):
        return self.__codigo

    def get_nombre(self):
        return self.__nombre

    def get_especialidad(self):
        return self.__especialidad

    def mostrar_datos(self):

        return (
            self.__codigo
            + " | "
            + self.__nombre
            + " | "
            + self.__especialidad
        )


# CLASE CITA
# RF02: Gestionar y agendar citas

# COMPOSICION: el detalle de horario pertenece a una cita concreta.
class DetalleHorario:
    def __init__(self, fecha, hora):
        self.fecha = fecha
        self.hora = hora


class Cita:

    def __init__(
        self,
        codigo,
        paciente,
        medico,
        fecha,
        hora
    ):

        self.__codigo = codigo
        self.__paciente = paciente
        self.__medico = medico
        self.__horario = DetalleHorario(fecha, hora)
        self.__fecha = fecha
        self.__hora = hora
        self.__estado = "Programada"

    def get_codigo(self):
        return self.__codigo

    def get_paciente(self):
        return self.__paciente

    def get_medico(self):
        return self.__medico

    def get_fecha(self):
        return self.__fecha

    def get_hora(self):
        return self.__hora

    def get_estado(self):
        return self.__estado

    def cambiar_estado(self, nuevo_estado):

        self.__estado = nuevo_estado

    def mostrar_cita(self):

        return (
            self.__codigo
            + " | Paciente: "
            + self.__paciente.get_nombre()
            + " | Médico: "
            + self.__medico.get_nombre()
            + " | Especialidad: "
            + self.__medico.get_especialidad()
            + " | Fecha: "
            + self.__fecha
            + " | Hora: "
            + self.__hora
            + " | Estado: "
            + self.__estado
        )


# CLASE ATENCIÓN MÉDICA
# RF03: Registrar atenciones médicas
# RF04: Consultar antecedentes y diagnósticos

class AtencionMedica:

    def __init__(
        self,
        codigo,
        paciente,
        medico,
        fecha,
        motivo,
        diagnostico,
        tratamiento
    ):

        self.__codigo = codigo
        self.__paciente = paciente
        self.__medico = medico
        self.__fecha = fecha
        self.__motivo = motivo
        self.__diagnostico = diagnostico
        self.__tratamiento = tratamiento

    def get_codigo(self):
        return self.__codigo

    def get_paciente(self):
        return self.__paciente

    def get_medico(self):
        return self.__medico

    def get_fecha(self):
        return self.__fecha

    def get_motivo(self):
        return self.__motivo

    def get_diagnostico(self):
        return self.__diagnostico

    def get_tratamiento(self):
        return self.__tratamiento

    def mostrar_atencion(self):

        return (
            self.__codigo
            + " | Paciente: "
            + self.__paciente.get_nombre()
            + " | Médico: "
            + self.__medico.get_nombre()
            + " | Fecha: "
            + self.__fecha
            + " | Diagnóstico: "
            + self.__diagnostico
        )


# COLECCIONES PRINCIPALES

# SINGLETON: una sola gestion de las colecciones de la clinica.
# AGREGACION: los pacientes existen como objetos independientes del gestor.
# 2. GESTION CENTRALIZADA (SINGLETON)
class GestorClinica:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.pacientes = []
            cls._instancia.medicos = []
            cls._instancia.citas = []
            cls._instancia.atenciones = []
        return cls._instancia

    def registrar_paciente(self, paciente):
        self.pacientes.append(paciente)

    def registrar_cita(self, cita):
        self.citas.append(cita)

    def registrar_atencion(self, atencion):
        self.atenciones.append(atencion)


gestor = GestorClinica()
pacientes = gestor.pacientes
medicos = gestor.medicos
citas = gestor.citas
atenciones = gestor.atenciones


# DATOS INICIALES DE MÉDICOS

medicos.append(
    Medico(
        "M001",
        "Dr. Carlos Perez",
        "Medicina General"
    )
)

medicos.append(
    Medico(
        "M002",
        "Dra. Maria Lopez",
        "Pediatria"
    )
)

medicos.append(
    Medico(
        "M003",
        "Dr. Juan Torres",
        "Medicina Interna"
    )
)

# FUNCIONES DE BÚSQUEDA
# PROGRAMACIÓN FUNCIONAL: FILTER

# 3. BUSQUEDAS Y PROCESAMIENTO DE DATOS
def buscar_paciente_por_dni(dni):

    resultado = list(
        filter(
            lambda paciente:
            paciente.get_dni() == dni,
            pacientes
        )
    )

    if len(resultado) > 0:
        return resultado[0]

    return None


def buscar_paciente_por_nombre(nombre):

    resultado = list(
        filter(
            lambda paciente:
            nombre.lower()
            in paciente.get_nombre().lower(),
            pacientes
        )
    )

    return resultado


def buscar_medico_por_nombre(nombre):

    resultado = list(
        filter(
            lambda medico:
            medico.get_nombre().lower()
            == nombre.lower(),
            medicos
        )
    )

    if len(resultado) > 0:
        return resultado[0]

    return None


# BÚSQUEDA DE ATENCIONES DE UN PACIENTE
# PROGRAMACIÓN FUNCIONAL: FILTER

def obtener_atenciones_paciente(paciente):

    return list(
        filter(
            lambda atencion:
            atencion.get_paciente().get_codigo()
            == paciente.get_codigo(),
            atenciones
        )
    )

# OBTENER NOMBRES
# PROGRAMACIÓN FUNCIONAL: MAP

def obtener_nombres_pacientes():

    return list(
        map(
            lambda paciente:
            paciente.get_nombre(),
            pacientes
        )
    )


# OBTENER DIAGNÓSTICOS
# PROGRAMACIÓN FUNCIONAL: MAP

def obtener_diagnosticos():

    return list(
        map(
            lambda atencion:
            atencion.get_diagnostico(),
            atenciones
        )
    )


# ESTADÍSTICA
# PROGRAMACIÓN FUNCIONAL: REDUCE

def contar_atenciones():

    total = reduce(
        lambda acumulado, atencion:
        acumulado + 1,
        atenciones,
        0
    )

    return total


# CONTAR ATENCIONES POR ESPECIALIDAD

def contar_por_especialidad(especialidad):

    resultado = list(
        filter(
            lambda atencion:
            atencion.get_medico().get_especialidad()
            == especialidad,
            atenciones
        )
    )

    return len(resultado)


# VERIFICAR DISPONIBILIDAD
# RF02

def verificar_disponibilidad(
    medico,
    fecha,
    hora
):

    resultado = list(
        filter(
            lambda cita:
            cita.get_medico().get_codigo()
            == medico.get_codigo()
            and cita.get_fecha() == fecha
            and cita.get_hora() == hora
            and cita.get_estado() == "Programada",
            citas
        )
    )

    return len(resultado) == 0


# GENERAR CÓDIGOS

def generar_codigo_paciente():

    numero = len(pacientes) + 1

    return "P" + str(numero).zfill(3)


def generar_codigo_cita():

    numero = len(citas) + 1

    return "C" + str(numero).zfill(3)


def generar_codigo_atencion():

    numero = len(atenciones) + 1

    return "A" + str(numero).zfill(3)


# VALIDAR CAMPOS
# PROGRAMACIÓN ESTRUCTURADA

def validar_campos_obligatorios(campos):

    for campo in campos:

        if campo.strip() == "":
            return False

    return True


# 4. FORMULARIOS Y OPERACIONES
def limpiar_formulario():

    entradas = [
        entrada_nombre,
        entrada_dni,
        entrada_direccion,
        entrada_telefono,
        entrada_edad,
        entrada_sexo,
        entrada_fecha_nacimiento,
        entrada_procedencia,
        entrada_grado,
        entrada_estado_civil,
        entrada_ocupacion,
        entrada_acompanante,
        entrada_parentesco,
        entrada_telefono_acompanante,
        entrada_fecha_cita,
        entrada_hora_cita,
        entrada_medico
    ]

    for entrada in entradas:
        entrada.delete(0, tk.END)


# AGENDAR CITA
# RF01 + RF02

def agendar_cita():

    try:

        nombre = entrada_nombre.get().strip()
        dni = entrada_dni.get().strip()
        direccion = entrada_direccion.get().strip()
        telefono = entrada_telefono.get().strip()
        edad = entrada_edad.get().strip()
        sexo = entrada_sexo.get().strip()
        fecha_nacimiento = entrada_fecha_nacimiento.get().strip()
        procedencia = entrada_procedencia.get().strip()
        grado = entrada_grado.get().strip()
        estado_civil = entrada_estado_civil.get().strip()
        ocupacion = entrada_ocupacion.get().strip()
        acompanante = entrada_acompanante.get().strip()
        parentesco = entrada_parentesco.get().strip()
        telefono_acompanante = (
            entrada_telefono_acompanante.get().strip()
        )

        fecha_cita = entrada_fecha_cita.get().strip()
        hora_cita = entrada_hora_cita.get().strip()
        nombre_medico = entrada_medico.get().strip()

        # ----------------------------------------------------
        # VALIDACIÓN
        # ----------------------------------------------------

        campos_obligatorios = [
            nombre,
            dni,
            telefono,
            edad,
            sexo,
            fecha_cita,
            hora_cita,
            nombre_medico
        ]

        if not validar_campos_obligatorios(
            campos_obligatorios
        ):

            messagebox.showwarning(
                "Datos incompletos",
                "Complete todos los campos obligatorios."
            )

            return

        if not validar_dni(dni):
            messagebox.showwarning("DNI incorrecto", "El DNI debe tener 8 dígitos.")
            return
        if not validar_telefono(telefono):
            messagebox.showwarning("Teléfono incorrecto", "El teléfono debe tener 9 dígitos.")
            return
        if not validar_fecha(fecha_cita) or not validar_hora(hora_cita):
            messagebox.showwarning("Fecha u hora incorrecta", "Use DD/MM/AAAA y HH:MM (24 horas).")
            return

        # ----------------------------------------------------
        # VALIDAR EDAD
        # ----------------------------------------------------

        try:

            edad_numero = int(edad)

            if edad_numero < 0 or edad_numero > 120:

                messagebox.showwarning(
                    "Edad incorrecta",
                    "Ingrese una edad válida entre 0 y 120."
                )

                return

        except ValueError:

            messagebox.showwarning(
                "Edad incorrecta",
                "La edad debe ser un número entero."
            )

            return

        # ----------------------------------------------------
        # BUSCAR PACIENTE
        # ----------------------------------------------------

        paciente = buscar_paciente_por_dni(dni)

        if paciente is None:

            codigo_paciente = generar_codigo_paciente()

            paciente = Paciente(
                codigo_paciente,
                nombre,
                dni,
                direccion,
                telefono,
                edad_numero,
                sexo,
                fecha_nacimiento,
                procedencia,
                grado,
                estado_civil,
                ocupacion,
                acompanante,
                parentesco,
                telefono_acompanante
            )

            mensaje_paciente = (
                "Paciente registrado correctamente."
            )

        else:

            mensaje_paciente = (
                "Paciente existente encontrado."
            )

        # ----------------------------------------------------
        # BUSCAR MÉDICO
        # ----------------------------------------------------

        medico = buscar_medico_por_nombre(
            nombre_medico
        )

        if medico is None:

            messagebox.showerror(
                "Médico no encontrado",
                "El médico ingresado no existe.\n\n"
                "Médicos disponibles:\n"
                "Dr. Carlos Perez\n"
                "Dra. Maria Lopez\n"
                "Dr. Juan Torres"
            )

            return

        # ----------------------------------------------------
        # VERIFICAR DISPONIBILIDAD
        # ----------------------------------------------------

        if not verificar_disponibilidad(
            medico,
            fecha_cita,
            hora_cita
        ):

            messagebox.showerror(
                "Horario ocupado",
                "El médico ya tiene una cita "
                "programada en esa fecha y hora."
            )

            return

        # ----------------------------------------------------
        # CREAR CITA
        # ----------------------------------------------------

        codigo_cita = generar_codigo_cita()

        nueva_cita = Cita(
            codigo_cita,
            paciente,
            medico,
            fecha_cita,
            hora_cita
        )

        if buscar_paciente_por_dni(dni) is None:
            gestor.registrar_paciente(paciente)
        gestor.registrar_cita(nueva_cita)

        lista_citas.insert(
            tk.END,
            nueva_cita.mostrar_cita()
        )

        messagebox.showinfo(
            "Cita registrada",
            mensaje_paciente
            + "\n\n"
            + "Cita registrada correctamente."
            + "\nCódigo de cita: "
            + codigo_cita
        )

        limpiar_formulario()

    except Exception:
        logging.warning("No se pudo registrar una cita")
        messagebox.showerror(
            "Error",
            "Ocurrió un problema durante "
            "el registro.\n\n"
            + "Revise los datos o contacte al administrador."
        )

# REGISTRAR ATENCIÓN MÉDICA
# RF03

def registrar_atencion():
    if not autorizar_acceso_clinico():
        return

    ventana_atencion = tk.Toplevel(ventana)

    ventana_atencion.title(
        "Registrar atención médica"
    )

    ventana_atencion.geometry(
        "550x500"
    )

    # --------------------------------------------------------
    # PACIENTE
    # --------------------------------------------------------

    tk.Label(
        ventana_atencion,
        text="DNI del paciente:"
    ).pack(pady=5)

    entrada_dni_atencion = tk.Entry(
        ventana_atencion,
        width=40
    )

    entrada_dni_atencion.pack()

    # --------------------------------------------------------
    # MÉDICO
    # --------------------------------------------------------

    tk.Label(
        ventana_atencion,
        text="Médico:"
    ).pack(pady=5)

    entrada_medico_atencion = tk.Entry(
        ventana_atencion,
        width=40
    )

    entrada_medico_atencion.pack()

    # --------------------------------------------------------
    # FECHA
    # --------------------------------------------------------

    tk.Label(
        ventana_atencion,
        text="Fecha:"
    ).pack(pady=5)

    entrada_fecha_atencion = tk.Entry(
        ventana_atencion,
        width=40
    )

    entrada_fecha_atencion.pack()

    # --------------------------------------------------------
    # MOTIVO
    # --------------------------------------------------------

    tk.Label(
        ventana_atencion,
        text="Motivo de consulta:"
    ).pack(pady=5)

    entrada_motivo = tk.Entry(
        ventana_atencion,
        width=40
    )

    entrada_motivo.pack()

    # --------------------------------------------------------
    # DIAGNÓSTICO
    # --------------------------------------------------------

    tk.Label(
        ventana_atencion,
        text="Diagnóstico:"
    ).pack(pady=5)

    entrada_diagnostico = tk.Entry(
        ventana_atencion,
        width=40
    )

    entrada_diagnostico.pack()

    # --------------------------------------------------------
    # TRATAMIENTO
    # --------------------------------------------------------

    tk.Label(
        ventana_atencion,
        text="Tratamiento:"
    ).pack(pady=5)

    entrada_tratamiento = tk.Entry(
        ventana_atencion,
        width=40
    )

    entrada_tratamiento.pack()

    # --------------------------------------------------------
    # GUARDAR
    # --------------------------------------------------------

    def guardar_atencion():

        dni = entrada_dni_atencion.get().strip()
        nombre_medico = (
            entrada_medico_atencion.get().strip()
        )
        fecha = entrada_fecha_atencion.get().strip()
        motivo = entrada_motivo.get().strip()
        diagnostico = entrada_diagnostico.get().strip()
        tratamiento = entrada_tratamiento.get().strip()

        if not validar_campos_obligatorios(
            [
                dni,
                nombre_medico,
                fecha,
                motivo,
                diagnostico,
                tratamiento
            ]
        ):

            messagebox.showwarning(
                "Datos incompletos",
                "Complete todos los campos."
            )

            return

        if not validar_dni(dni) or not validar_fecha(fecha):
            messagebox.showwarning("Datos incorrectos", "Ingrese DNI de 8 dígitos y fecha DD/MM/AAAA.")
            return

        paciente = buscar_paciente_por_dni(dni)

        if paciente is None:

            messagebox.showerror(
                "Paciente no encontrado",
                "No existe un paciente registrado "
                "con ese DNI."
            )

            return

        medico = buscar_medico_por_nombre(
            nombre_medico
        )

        if medico is None:

            messagebox.showerror(
                "Médico no encontrado",
                "El médico ingresado no existe."
            )

            return

        codigo = generar_codigo_atencion()

        nueva_atencion = AtencionMedica(
            codigo,
            paciente,
            medico,
            fecha,
            motivo,
            diagnostico,
            tratamiento
        )

        atenciones.append(
            nueva_atencion
        )

        lista_atenciones.insert(
            tk.END,
            nueva_atencion.mostrar_atencion()
        )

        messagebox.showinfo(
            "Atención registrada",
            "La atención médica fue registrada "
            "correctamente.\n\n"
            "Código: " + codigo
        )

        ventana_atencion.destroy()

    tk.Button(
        ventana_atencion,
        text="REGISTRAR ATENCIÓN",
        command=guardar_atencion,
        width=25
    ).pack(pady=20)


# CONSULTAR HISTORIA CLÍNICA
# RF04

def consultar_historia():
    if not autorizar_acceso_clinico():
        return

    dni = entrada_busqueda_dni.get().strip()

    if dni == "":

        messagebox.showwarning(
            "Dato requerido",
            "Ingrese el DNI del paciente."
        )

        return

    paciente = buscar_paciente_por_dni(dni)

    if paciente is None:

        messagebox.showerror(
            "Paciente no encontrado",
            "No existe un paciente con ese DNI."
        )

        return

    atenciones_paciente = obtener_atenciones_paciente(
        paciente
    )

    texto = (
        "HISTORIA CLÍNICA AUTORIZADA\n"
        "\n"
        + paciente.mostrar_datos()
        + "\n\n"
        + "ATENCIONES MÉDICAS\n"
        + "--------------------------------\n"
    )

    if len(atenciones_paciente) == 0:

        texto += "No existen atenciones registradas."

    else:

        for atencion in atenciones_paciente:

            texto += (
                "\nCódigo: "
                + atencion.get_codigo()
                + "\nFecha: "
                + atencion.get_fecha()
                + "\nMédico: "
                + atencion.get_medico().get_nombre()
                + "\nMotivo: "
                + atencion.get_motivo()
                + "\nDiagnóstico: "
                + atencion.get_diagnostico()
                + "\nTratamiento: "
                + atencion.get_tratamiento()
                + "\n--------------------------------\n"
            )

    messagebox.showinfo(
        "Historia clínica",
        texto
    )

# MOSTRAR PACIENTES
# RF06

def mostrar_pacientes():

    if len(pacientes) == 0:

        messagebox.showinfo(
            "Pacientes",
            "No hay pacientes registrados."
        )

        return

    nombres = obtener_nombres_pacientes()

    texto = "PACIENTES REGISTRADOS\n\n"

    for nombre in nombres:

        texto += "- " + nombre + "\n"

    messagebox.showinfo(
        "Pacientes",
        texto
    )


# BUSCAR PACIENTE POR NOMBRE
# RF06
# PROGRAMACIÓN FUNCIONAL

def buscar_paciente():

    nombre = entrada_busqueda_nombre.get().strip()

    if nombre == "":

        messagebox.showwarning(
            "Dato requerido",
            "Ingrese un nombre para buscar."
        )

        return

    resultados = buscar_paciente_por_nombre(
        nombre
    )

    if len(resultados) == 0:

        messagebox.showinfo(
            "Resultado",
            "No se encontraron pacientes."
        )

        return

    texto = "RESULTADOS DE BÚSQUEDA\n\n"

    for paciente in resultados:

        texto += (
            paciente.get_codigo()
            + " | "
            + paciente.get_nombre()
            + " | DNI: "
            + ocultar_dni(paciente.get_dni())
            + "\n"
        )

    messagebox.showinfo(
        "Pacientes encontrados",
        texto
    )


# MOSTRAR ESTADÍSTICAS
# RF05
# MAP + FILTER + REDUCE

def mostrar_estadisticas(diagnosticos=None):

    total_pacientes = len(pacientes)
    total_citas = len(citas)
    total_atenciones = contar_atenciones()


    texto = (
        "ESTADÍSTICAS DEL SISTEMA\n\n"
        "Total de pacientes: "
        + str(total_pacientes)
        + "\n"
        "Total de citas: "
        + str(total_citas)
        + "\n"
        "Total de atenciones: "
        + str(total_atenciones)
        + "\n\n"
        "ATENCIONES POR ESPECIALIDAD\n"
        "--------------------------------\n"
    )

    for medico in medicos:

        especialidad = medico.get_especialidad()

        cantidad = contar_por_especialidad(
            especialidad
        )

        texto += (
            especialidad
            + ": "
            + str(cantidad)
            + "\n"
        )

    texto += (
        "\nDIAGNÓSTICOS REGISTRADOS\n"
        "--------------------------------\n"
    )

    if len(diagnosticos) == 0:

        texto += "No existen diagnósticos registrados."

    else:

        for diagnostico in diagnosticos:

            texto += "- " + diagnostico + "\n"

    messagebox.showinfo(
        "Estadísticas",
        texto
    )


# CANCELAR CITA
# PROGRAMACIÓN ESTRUCTURADA

def cancelar_cita():

    seleccion = lista_citas.curselection()

    if len(seleccion) == 0:

        messagebox.showwarning(
            "Seleccionar cita",
            "Seleccione una cita de la lista."
        )

        return

    indice = seleccion[0]

    cita = citas[indice]

    if cita.get_estado() == "Cancelada":

        messagebox.showinfo(
            "Cita",
            "La cita ya se encuentra cancelada."
        )

        return

    cita.cambiar_estado("Cancelada")

    lista_citas.delete(indice)

    lista_citas.insert(
        indice,
        cita.mostrar_cita()
    )

    messagebox.showinfo(
        "Cita cancelada",
        "La cita fue cancelada correctamente."
    )

# INTERFAZ GRÁFICA PRINCIPAL

# MVC: el controlador recibe eventos de la vista Tkinter.
# El modelo son las clases y el gestor definidos arriba.
# 5. CONTROLADOR DE EVENTOS (MVC)
class ControladorClinica:
    def agendar(self):
        agendar_cita()

    def atender(self):
        registrar_atencion()

    def ver_pacientes(self):
        mostrar_pacientes()

    def cancelar(self):
        cancelar_cita()

    def estadisticas(self):
        mostrar_estadisticas()

    def limpiar(self):
        limpiar_formulario()

    def buscar(self):
        buscar_paciente()

    def historia(self):
        consultar_historia()


controlador = ControladorClinica()

# 6. INTERFAZ GRAFICA ORIGINAL
ventana = tk.Tk()

ventana.title(
    "Club Salud - Sistema de Gestión"
)

ventana.geometry(
    "1150x900"
)


# TÍTULO

titulo = tk.Label(
    ventana,
    text="CLUB SALUD",
    font=("Arial", 22, "bold")
)

titulo.pack(pady=10)


subtitulo = tk.Label(
    ventana,
    text=(
        "Sistema de gestión de pacientes, "
        "citas y atenciones médicas"
    ),
    font=("Arial", 11)
)

subtitulo.pack()


# FRAME PACIENTE

frame_paciente = tk.LabelFrame(
    ventana,
    text="Datos generales del paciente",
    padx=10,
    pady=10
)

frame_paciente.pack(
    padx=15,
    pady=10,
    fill="x"
)


# FILA 1

tk.Label(
    frame_paciente,
    text="Nombre:"
).grid(row=0, column=0, padx=5, pady=5)

entrada_nombre = tk.Entry(
    frame_paciente,
    width=25
)

entrada_nombre.grid(
    row=0,
    column=1,
    padx=5
)


tk.Label(
    frame_paciente,
    text="DNI:"
).grid(row=0, column=2, padx=5)

entrada_dni = tk.Entry(
    frame_paciente,
    width=20
)

entrada_dni.grid(
    row=0,
    column=3,
    padx=5
)


# FILA 2

tk.Label(
    frame_paciente,
    text="Dirección:"
).grid(row=1, column=0, padx=5, pady=5)

entrada_direccion = tk.Entry(
    frame_paciente,
    width=25
)

entrada_direccion.grid(
    row=1,
    column=1,
    padx=5
)


tk.Label(
    frame_paciente,
    text="Teléfono:"
).grid(row=1, column=2, padx=5)

entrada_telefono = tk.Entry(
    frame_paciente,
    width=20
)

entrada_telefono.grid(
    row=1,
    column=3,
    padx=5
)


# FILA 3

tk.Label(
    frame_paciente,
    text="Edad:"
).grid(row=2, column=0, padx=5, pady=5)

entrada_edad = tk.Entry(
    frame_paciente,
    width=25
)

entrada_edad.grid(
    row=2,
    column=1,
    padx=5
)


tk.Label(
    frame_paciente,
    text="Sexo:"
).grid(row=2, column=2, padx=5)

entrada_sexo = tk.Entry(
    frame_paciente,
    width=20
)

entrada_sexo.grid(
    row=2,
    column=3,
    padx=5
)


# FILA 4

tk.Label(
    frame_paciente,
    text="F. nacimiento:"
).grid(row=3, column=0, padx=5, pady=5)

entrada_fecha_nacimiento = tk.Entry(
    frame_paciente,
    width=25
)

entrada_fecha_nacimiento.grid(
    row=3,
    column=1,
    padx=5
)


tk.Label(
    frame_paciente,
    text="Procedencia:"
).grid(row=3, column=2, padx=5)

entrada_procedencia = tk.Entry(
    frame_paciente,
    width=20
)

entrada_procedencia.grid(
    row=3,
    column=3,
    padx=5
)


# FILA 5

tk.Label(
    frame_paciente,
    text="Grado instrucción:"
).grid(row=4, column=0, padx=5, pady=5)

entrada_grado = tk.Entry(
    frame_paciente,
    width=25
)

entrada_grado.grid(
    row=4,
    column=1,
    padx=5
)


tk.Label(
    frame_paciente,
    text="Estado civil:"
).grid(row=4, column=2, padx=5)

entrada_estado_civil = tk.Entry(
    frame_paciente,
    width=20
)

entrada_estado_civil.grid(
    row=4,
    column=3,
    padx=5
)


# FILA 6

tk.Label(
    frame_paciente,
    text="Ocupación:"
).grid(row=5, column=0, padx=5, pady=5)

entrada_ocupacion = tk.Entry(
    frame_paciente,
    width=25
)

entrada_ocupacion.grid(
    row=5,
    column=1,
    padx=5
)


tk.Label(
    frame_paciente,
    text="Acompañante:"
).grid(row=5, column=2, padx=5)

entrada_acompanante = tk.Entry(
    frame_paciente,
    width=20
)

entrada_acompanante.grid(
    row=5,
    column=3,
    padx=5
)


# FILA 7

tk.Label(
    frame_paciente,
    text="Parentesco:"
).grid(row=6, column=0, padx=5, pady=5)

entrada_parentesco = tk.Entry(
    frame_paciente,
    width=25
)

entrada_parentesco.grid(
    row=6,
    column=1,
    padx=5
)


tk.Label(
    frame_paciente,
    text="Tel. acompañante:"
).grid(row=6, column=2, padx=5)

entrada_telefono_acompanante = tk.Entry(
    frame_paciente,
    width=20
)

entrada_telefono_acompanante.grid(
    row=6,
    column=3,
    padx=5
)


# FRAME CITA

frame_cita = tk.LabelFrame(
    ventana,
    text="Datos de la cita",
    padx=10,
    pady=10
)

frame_cita.pack(
    padx=15,
    pady=5,
    fill="x"
)


tk.Label(
    frame_cita,
    text="Médico:"
).grid(row=0, column=0, padx=5, pady=5)

entrada_medico = tk.Entry(
    frame_cita,
    width=25
)

entrada_medico.grid(
    row=0,
    column=1,
    padx=5
)


tk.Label(
    frame_cita,
    text="Ej.: Dr. Carlos Perez"
).grid(
    row=0,
    column=2,
    padx=5
)


tk.Label(
    frame_cita,
    text="Fecha:"
).grid(row=1, column=0, padx=5, pady=5)

entrada_fecha_cita = tk.Entry(
    frame_cita,
    width=25
)

entrada_fecha_cita.grid(
    row=1,
    column=1,
    padx=5
)


tk.Label(
    frame_cita,
    text="Ej.: 25/09/2026"
).grid(
    row=1,
    column=2,
    padx=5
)


tk.Label(
    frame_cita,
    text="Hora:"
).grid(row=2, column=0, padx=5, pady=5)

entrada_hora_cita = tk.Entry(
    frame_cita,
    width=25
)

entrada_hora_cita.grid(
    row=2,
    column=1,
    padx=5
)


tk.Label(
    frame_cita,
    text="Ej.: 09:00"
).grid(
    row=2,
    column=2,
    padx=5
)


# BOTONES PRINCIPALES

frame_botones = tk.Frame(ventana)

frame_botones.pack(pady=10)


tk.Button(
    frame_botones,
    text="AGENDAR CITA",
    command=controlador.agendar,
    width=20
).grid(row=0, column=0, padx=5)


tk.Button(
    frame_botones,
    text="REGISTRAR ATENCIÓN",
    command=controlador.atender,
    width=20
).grid(row=0, column=1, padx=5)


tk.Button(
    frame_botones,
    text="VER PACIENTES",
    command=controlador.ver_pacientes,
    width=20
).grid(row=0, column=2, padx=5)


tk.Button(
    frame_botones,
    text="CANCELAR CITA",
    command=controlador.cancelar,
    width=20
).grid(row=0, column=3, padx=5)


tk.Button(
    frame_botones,
    text="ESTADÍSTICAS",
    command=controlador.estadisticas,
    width=20
).grid(row=1, column=0, padx=5, pady=5)


tk.Button(
    frame_botones,
    text="LIMPIAR",
    command=controlador.limpiar,
    width=20
).grid(row=1, column=1, padx=5, pady=5)


# BÚSQUEDA Y CONSULTA
# RF04 + RF06

frame_busqueda = tk.LabelFrame(
    ventana,
    text="Búsqueda y consulta",
    padx=10,
    pady=10
)

frame_busqueda.pack(
    padx=15,
    pady=5,
    fill="x"
)


tk.Label(
    frame_busqueda,
    text="Nombre:"
).grid(
    row=0,
    column=0,
    padx=5
)


entrada_busqueda_nombre = tk.Entry(
    frame_busqueda,
    width=25
)

entrada_busqueda_nombre.grid(
    row=0,
    column=1,
    padx=5
)


tk.Button(
    frame_busqueda,
    text="BUSCAR PACIENTE",
    command=controlador.buscar
).grid(
    row=0,
    column=2,
    padx=10
)


tk.Label(
    frame_busqueda,
    text="DNI:"
).grid(
    row=1,
    column=0,
    padx=5,
    pady=5
)


entrada_busqueda_dni = tk.Entry(
    frame_busqueda,
    width=25
)

entrada_busqueda_dni.grid(
    row=1,
    column=1,
    padx=5
)


tk.Button(
    frame_busqueda,
    text="CONSULTAR HISTORIA",
    command=controlador.historia
).grid(
    row=1,
    column=2,
    padx=10
)


# LISTA DE CITAS

tk.Label(
    ventana,
    text="CITAS AGENDADAS",
    font=("Arial", 12, "bold")
).pack(pady=5)


lista_citas = tk.Listbox(
    ventana,
    width=135,
    height=7
)

lista_citas.pack(
    padx=15,
    pady=5
)


# LISTA DE ATENCIONES

tk.Label(
    ventana,
    text="ATENCIONES MÉDICAS REGISTRADAS",
    font=("Arial", 12, "bold")
).pack(pady=5)


lista_atenciones = tk.Listbox(
    ventana,
    width=135,
    height=6
)

lista_atenciones.pack(
    padx=15,
    pady=5
)


# PIE DE SISTEMA

tk.Label(
    ventana,
    text=(
        "Prototipo de viabilidad - Clínica Club Salud | "
        "POO + Programación Funcional + Estructurada"
    ),
    font=("Arial", 9)
).pack(pady=8)


# INICIAR SISTEMA

ventana.mainloop()


