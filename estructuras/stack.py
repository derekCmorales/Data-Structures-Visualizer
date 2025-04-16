# estructuras/stack.py

class NodoPila:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

class Pila:
    def __init__(self):
        self.cima = None
        self.tamaño = 0

    def esta_vacia(self):
        return self.cima is None

    def insertar(self, valor):
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
        """Retorna una lista de los valores en la pila, desde la cima hasta el fondo."""
        elementos = []
        actual = self.cima
        while actual:
            elementos.append(actual.valor)
            actual = actual.siguiente
        return elementos
