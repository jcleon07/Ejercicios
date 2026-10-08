"""
Actores: Estudiante, Profesor y Funcionario.

Clases:
- Persona: clase padre con id y nombre.
- Estudiante y Profesor: piden libros prestados, cada uno con su límite.
- Funcionario: es el que presta y recibe los libros.
- Libro: tiene nombre y si está prestado o no.

Relaciones:
- Estudiante, Profesor y Funcionario heredan de Persona.
- Estudiante y Profesor tienen una lista de libros.
- Funcionario usa a la persona y al libro para hacer el préstamo.
"""


class Persona:
    def __init__(self, id, nombre):
        self.__id = id
        self.__nombre = nombre

    def get_nombre(self):
        return self.__nombre

    def descripcion(self):
        return f"Persona {self.__nombre}"


class Estudiante(Persona):
    def __init__(self, id, nombre):
        super().__init__(id, nombre)
        self.__libros = []

    def limite_libros(self):
        return 3

    def puede_prestar(self):
        return len(self.__libros) < self.limite_libros()

    def agregar_libro(self, libro):
        self.__libros.append(libro)

    def quitar_libro(self, libro):
        self.__libros.remove(libro)

    def get_libros(self):
        return [libro.get_nombre() for libro in self.__libros]

    def descripcion(self):
        return f"Estudiante {self.get_nombre()}"


class Profesor(Estudiante):
    # Hereda la lógica pero puede llevar más libros
    def limite_libros(self):
        return 5

    def descripcion(self):
        return f"Profesor {self.get_nombre()}"


class Funcionario(Persona):
    def prestar(self, persona, libro):
        if libro.esta_prestado():
            print(f"'{libro.get_nombre()}' ya está prestado")
        elif not persona.puede_prestar():
            print(f"{persona.descripcion()} ya tiene el máximo de libros")
        else:
            libro.prestar()
            persona.agregar_libro(libro)
            print(f"{self.get_nombre()} le prestó '{libro.get_nombre()}' a {persona.descripcion()}")

    def recibir(self, persona, libro):
        libro.devolver()
        persona.quitar_libro(libro)
        print(f"{persona.descripcion()} devolvió '{libro.get_nombre()}'")

    def descripcion(self):
        return f"Funcionario {self.get_nombre()}"


class Libro:
    def __init__(self, nombre):
        self.__nombre = nombre
        self.__prestado = False

    def get_nombre(self):
        return self.__nombre

    def esta_prestado(self):
        return self.__prestado

    def prestar(self):
        self.__prestado = True

    def devolver(self):
        self.__prestado = False



ana = Estudiante(1, "Ana")
luis = Profesor(2, "Luis")
marta = Funcionario(3, "Marta")

libros = [Libro("Clean Code"), Libro("Refactoring"),
            Libro("Design Patterns"), Libro("Cálculo")]

# Polimorfismo: misma llamada, resultado distinto
for persona in [ana, luis, marta]:
    print(persona.descripcion())

for libro in libros:
    marta.prestar(ana, libro)

marta.prestar(luis, libros[0])
marta.recibir(ana, libros[0])
marta.prestar(luis, libros[0])

print("Libros de Ana:", ana.get_libros())
print("Libros de Luis:", luis.get_libros())
