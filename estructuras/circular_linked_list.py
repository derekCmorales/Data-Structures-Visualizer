# circular_linked_list.py
import json
from estructuras.singly_linked_list import NodoLista, ListaSimple

class ListaCircular(ListaSimple):
    def __init__(self):
        super().__init__()

    def insertar_inicio(self, valor):
        if self.tipo_dato is None:
            self.tipo_dato = type(valor)
        elif not isinstance(valor, self.tipo_dato):
            raise TypeError(f"Tipo incorrecto. Se esperaba {self.tipo_dato.__name__}")

        nuevo = NodoLista(valor)
        if self.esta_vacia():
            self.cabeza = self.cola = nuevo
            nuevo.siguiente = self.cabeza
        else:
            nuevo.siguiente = self.cabeza
            self.cabeza = nuevo
            self.cola.siguiente = self.cabeza  # Mantener circularidad
        self.tamaño += 1

    def insertar_final(self, valor):
        if self.tipo_dato is None:
            self.tipo_dato = type(valor)
        elif not isinstance(valor, self.tipo_dato):
            raise TypeError(f"Tipo incorrecto. Se esperaba {self.tipo_dato.__name__}")

        nuevo = NodoLista(valor)
        if self.esta_vacia():
            self.cabeza = self.cola = nuevo
            nuevo.siguiente = self.cabeza
        else:
            self.cola.siguiente = nuevo
            self.cola = nuevo
            nuevo.siguiente = self.cabeza  # Enlace circular
        self.tamaño += 1

    def eliminar_inicio(self):
        if self.esta_vacia():
            raise IndexError("La lista está vacía")

        valor = self.cabeza.valor
        if self.tamaño == 1:
            self.cabeza = self.cola = None
        else:
            self.cabeza = self.cabeza.siguiente
            self.cola.siguiente = self.cabeza  # Actualizar enlace circular
        self.tamaño -= 1
        return valor

    def eliminar_final(self):
        if self.esta_vacia():
            raise IndexError("La lista está vacía")

        valor = self.cola.valor
        if self.tamaño == 1:
            self.cabeza = self.cola = None
        else:
            actual = self.cabeza
            while actual.siguiente != self.cola:
                actual = actual.siguiente
            actual.siguiente = self.cabeza  # Nuevo último nodo apunta a cabeza
            self.cola = actual
        self.tamaño -= 1
        return valor

class ListaCircular(ListaSimple):

    def rotar_izquierda(self):
        if self.tamaño > 1:
            old_head = self.cabeza
            self.cabeza = self.cabeza.siguiente
            self.cola.siguiente = old_head  # Mantener circularidad
            self.cola = old_head

    def rotar_derecha(self):
        if self.tamaño > 1:
            actual = self.cabeza
            while actual.siguiente != self.cola:
                actual = actual.siguiente
            new_head = self.cola
            new_head.siguiente = self.cabeza
            self.cola = actual
            self.cola.siguiente = new_head
            self.cabeza = new_head

    def buscar(self, valor):
        if self.esta_vacia():
            return -1

        index = 0
        actual = self.cabeza
        for _ in range(self.tamaño):
            if actual.valor == valor:
                return index
            actual = actual.siguiente
            index += 1
        return -1

    @classmethod
    def cargar_desde_archivo(cls, filename):
        with open(filename, 'r') as f:
            datos = json.load(f)

        if datos['tipo_estructura'] != 'lista_simple':
            raise ValueError("Archivo no corresponde a lista simple")

        lista = cls()
        nodos = {}

        # Primera pasada: crear nodos
        for elemento in datos['elementos']:
            valor = elemento['valor']
            tipo = elemento['tipo_valor']

            if tipo == 'int':
                valor = int(valor)
            elif tipo == 'float':
                valor = float(valor)
            elif tipo == 'bool':
                valor = bool(valor)

            lista.insertar_final(valor)
            nodos[elemento['direccion']] = lista.cola

        # Segunda pasada: establecer circularidad
        if lista.tamaño > 0:
            lista.cola.siguiente = lista.cabeza

        return lista

    def guardar_a_archivo(self, filename):
        datos = {
            'tipo_estructura': 'lista_circular',  # Identificador único
            'tamaño': self.tamaño,
            'tipo_dato': self._nombre_tipo(),
            'elementos': self.obtener_elementos()
        }
        with open(filename, 'w') as f:
            json.dump(datos, f, indent=4)