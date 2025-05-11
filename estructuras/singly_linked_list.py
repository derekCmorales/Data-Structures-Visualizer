import json


class NodoLista:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

    def to_dict(self):
        return {
            'valor': self.valor,
            'tipo_valor': self._obtener_tipo_valor(),
            'direccion': id(self),
            'siguiente': id(self.siguiente) if self.siguiente else None
        }

    def _obtener_tipo_valor(self):
        tipos = {
            int: 'int',
            float: 'float',
            bool: 'bool',
            str: 'str'
        }
        return tipos.get(type(self.valor), str(type(self.valor)))


class ListaSimple:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.tamaño = 0
        self.tipo_dato = None

    def esta_vacia(self):
        return self.cabeza is None

    def insertar_inicio(self, valor):
        if self.tipo_dato is None:
            self.tipo_dato = type(valor)
        elif not isinstance(valor, self.tipo_dato):
            raise TypeError(f"Tipo incorrecto. Se esperaba {self.tipo_dato.__name__}")

        nuevo = NodoLista(valor)
        if self.esta_vacia():
            self.cola = nuevo
        else:
            nuevo.siguiente = self.cabeza
        self.cabeza = nuevo
        self.tamaño += 1

    def insertar_final(self, valor):
        if self.tipo_dato is None:
            self.tipo_dato = type(valor)
        elif not isinstance(valor, self.tipo_dato):
            raise TypeError(f"Tipo incorrecto. Se esperaba {self.tipo_dato.__name__}")

        nuevo = NodoLista(valor)
        if self.esta_vacia():
            self.cabeza = nuevo
        else:
            self.cola.siguiente = nuevo
        self.cola = nuevo
        self.tamaño += 1

    def eliminar_inicio(self):
        if self.esta_vacia():
            raise IndexError("La lista está vacía")

        valor = self.cabeza.valor
        self.cabeza = self.cabeza.siguiente
        if self.cabeza is None:
            self.cola = None
        self.tamaño -= 1
        return valor

    def eliminar_final(self):
        if self.esta_vacia():
            raise IndexError("La lista está vacía")

        if self.cabeza == self.cola:
            valor = self.cabeza.valor
            self.cabeza = self.cola = None
        else:
            actual = self.cabeza
            while actual.siguiente != self.cola:
                actual = actual.siguiente
            valor = self.cola.valor
            actual.siguiente = None
            self.cola = actual
        self.tamaño -= 1
        return valor

    def buscar(self, valor):
        actual = self.cabeza
        index = 0
        while actual:
            if actual.valor == valor:
                return index
            actual = actual.siguiente
            index += 1
        return -1

    def obtener_elementos(self):
        elementos = []
        actual = self.cabeza
        while actual:
            elementos.append(actual.to_dict())
            actual = actual.siguiente
        return elementos

    def guardar_a_archivo(self, filename):
        datos = {
            'tipo_estructura': 'lista_simple',
            'tamaño': self.tamaño,
            'tipo_dato': self._nombre_tipo(),
            'elementos': self.obtener_elementos()
        }
        with open(filename, 'w') as f:
            json.dump(datos, f, indent=4)

    @classmethod
    def cargar_desde_archivo(cls, filename):
        with open(filename, 'r') as f:
            datos = json.load(f)

        if datos['tipo_estructura'] != 'lista_simple':
            raise ValueError("Archivo no corresponde a lista simple")

        lista = cls()
        nodos = {}

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

        # Reconstruir enlaces
        actual = lista.cabeza
        for elemento in datos['elementos']:
            if elemento['siguiente']:
                actual.siguiente = nodos.get(elemento['siguiente'])
            actual = actual.siguiente

        return lista

    def _nombre_tipo(self):
        tipos = {
            int: 'int',
            float: 'float',
            bool: 'bool',
            str: 'str'
        }
        return tipos.get(self.tipo_dato, str(self.tipo_dato))

    def reiniciar(self):
        self.cabeza = self.cola = None
        self.tamaño = 0
        self.tipo_dato = None