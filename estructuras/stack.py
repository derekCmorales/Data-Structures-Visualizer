import json


class NodoPila:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

    def to_dict(self):
        return {
            'valor': self.valor,
            'tipo_valor': self._obtener_tipo_valor(self.valor)
        }

    def _obtener_tipo_valor(self, valor):
        """Obtiene el nombre del tipo de forma segura"""
        tipo = type(valor)
        if tipo == int:
            return 'int'
        elif tipo == float:
            return 'float'
        elif tipo == bool:
            return 'bool'
        elif tipo == str:
            return 'str'
        else:
            return str(tipo)


class Pila:
    def __init__(self):
        self.cima = None
        self.tamaño = 0
        self.tipo_dato = None

    def esta_vacia(self):
        return self.cima is None

    def insertar(self, valor):
        if self.tipo_dato is None:
            self.tipo_dato = type(valor)
        elif not isinstance(valor, self.tipo_dato):
            raise TypeError(f"La pila solo acepta {self.tipo_dato.__name__}")

        nuevo = NodoPila(valor)
        nuevo.siguiente = self.cima
        self.cima = nuevo
        self.tamaño += 1

    def eliminar(self):
        if self.esta_vacia():
            raise IndexError("La pila está vacía")
        valor = self.cima.valor
        self.cima = self.cima.siguiente
        self.tamaño -= 1
        return valor

    def buscar(self, valor):
        actual = self.cima
        pos = 0
        while actual:
            if actual.valor == valor:
                return pos
            actual = actual.siguiente
            pos += 1
        return -1

    def obtener_todos(self):
        """Retorna una lista de los valores en la pila, desde la cima hasta el fondo"""
        elementos = []
        actual = self.cima
        while actual:
            elementos.append(actual.valor)
            actual = actual.siguiente
        return elementos

    def _obtener_elementos(self):
        """Recorre la pila y devuelve una lista de elementos en formato de diccionario"""
        elementos = []
        actual = self.cima
        while actual is not None:
            elementos.append(actual.to_dict())
            actual = actual.siguiente
        return elementos

    def _obtener_nombre_tipo(self, tipo):
        """Obtiene el nombre del tipo de forma segura"""
        if tipo is None:
            return None
        if tipo == int:
            return 'int'
        elif tipo == float:
            return 'float'
        elif tipo == bool:
            return 'bool'
        elif tipo == str:
            return 'str'
        else:
            return str(tipo)

    def guardar_a_archivo(self, filename):
        datos = {
            'tipo_estructura': 'pila',
            'tamaño': self.tamaño,
            'tipo_dato': self._obtener_nombre_tipo(self.tipo_dato),
            'elementos': self._obtener_elementos()
        }
        with open(filename, 'w') as f:
            json.dump(datos, f, indent=4)

    @classmethod
    def cargar_desde_archivo(cls, filename):
        with open(filename, 'r') as f:
            datos = json.load(f)

        if datos['tipo_estructura'] != 'pila':
            raise ValueError("El archivo no contiene una pila")

        pila = cls()
        for elemento in reversed(datos['elementos']):
            valor = elemento['valor']
            tipo_valor = elemento['tipo_valor']

            # Convertir al tipo original
            if tipo_valor == 'int':
                valor = int(valor)
            elif tipo_valor == 'float':
                valor = float(valor)
            elif tipo_valor == 'bool':
                valor = bool(valor) if isinstance(valor, bool) else valor.lower() == 'true'
            elif tipo_valor == 'str':
                valor = str(valor)

            pila.insertar(valor)
        return pila

    def reiniciar(self):
        """Vacía la pila y reinicia su tipo"""
        self.cima = None
        self.tamaño = 0
        self.tipo_dato = None