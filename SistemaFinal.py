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

