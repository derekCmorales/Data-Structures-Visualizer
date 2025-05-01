class NodoCola:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

class Cola:
    def __init__(self):
        self.frente = None
        self.final = None
        self.tamaño = 0
        self.tipo_dato = None

    def esta_vacia(self):
        return self.frente is None

    def insertar(self, valor):
        if self.tipo_dato is None:
            self.tipo_dato = type(valor)
        elif not isinstance(valor, self.tipo_dato):
            raise TypeError(f"La cola solo acepta {self.tipo_dato.__name__}. Se ingresó: {type(valor).__name__}")

        nuevo = NodoCola(valor)
        if self.esta_vacia():
            self.frente = self.final = nuevo
        else:
            self.final.siguiente = nuevo
            self.final = nuevo
        self.tamaño += 1

    def eliminar(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        valor = self.frente.valor
        self.frente = self.frente.siguiente
        if self.frente is None:
            self.final = None
        self.tamaño -= 1
        return valor

    def buscar(self, valor):
        actual = self.frente
        pos = 0
        while actual:
            if actual.valor == valor:
                return pos
            actual = actual.siguiente
            pos += 1
        return -1

    def obtener_todos(self):
        elementos = []
        actual = self.frente
        while actual:
            elementos.append(actual.valor)
            actual = actual.siguiente
        return elementos

    def reiniciar(self):
        self.frente = None
        self.final = None
        self.tamaño = 0
        self.tipo_dato = None