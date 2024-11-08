import psycopg2
import sys
import random
import datetime

HOSTNAME = 'localhost'
DATABASE = 'gestion_estudiantes'
USERNAME = 'postgres'
PASSWORD = 'pass123'
PORT = '5432'

def conectar_db():
    return psycopg2.connect(
        host=HOSTNAME, 
        user=USERNAME,
        password=PASSWORD,
        database=DATABASE,
        port=PORT 
    )
    
class Estudiante:

    def __init__(self, carnet, nombre, carrera ) -> None:
        self.carnet = carnet
        self.carrera = carrera
        self.nombre = nombre

    @staticmethod
    def crear_estudiante(carnet, nombre, codigo_carrera):
        conexion = conectar_db()
        cursor = conexion.cursor()

        cursor.execute(
            "INSERT INTO estudiantes (carnet, nombre, codigo_carrera) VALUES (%s, %s, %s)", 
            (carnet, nombre, codigo_carrera)
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    @staticmethod
    def obtener_nombre(carnet, adition = ""):
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT nombre FROM estudiantes WHERE carnet = %s", (carnet,))
        nombre = cursor.fetchone()
        print(f'    carnet: {carnet}, nombre: {nombre[0]} {adition}')        
    
    @staticmethod
    def obtener_estudiante(carnet):
        conexion = conectar_db()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM estudiantes WHERE carnet = %s", (carnet,))
        estudiante = cursor.fetchone()

        if estudiante:
            Estudiante(estudiante[0], estudiante[1], estudiante[2]).mostrar_informacion()
            
            cursor.execute("SELECT codigo_curso FROM estudiantes_cursos WHERE carnet = %s", (carnet,))
            codigos_cursos = cursor.fetchall()
            if codigos_cursos:
                print("Cursos asignados:")
                for codigo_curso in codigos_cursos:
                    cursor.execute("SELECT * FROM cursos WHERE codigo = %s", (codigo_curso,))
                    curso = cursor.fetchone()
                    Curso(curso[0], curso[1]).mostrar_informacion()
            else:
                print("El estudiante no tiene cursos asignados")
                
            cursor.close()
            conexion.close()
            return Estudiante(estudiante[0], estudiante[1], estudiante[2])
        else:
            cursor.close()
            conexion.close()
            print("Estudiante no encontrado")
            return None

    @staticmethod
    def eliminar_estudiante(carnet):
        conexion = conectar_db()
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM estudiantes WHERE carnet = %s", (carnet,))
        conexion.commit()
        cursor.close()
        conexion.close()
        
    @staticmethod
    def editar_estudiante(sql, params):
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        try:
            cursor.execute(sql, params)
            conexion.commit()
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
        finally:
            cursor.close()
            conexion.close()


    def mostrar_informacion(self):
        carrera = Carrera.obtener_carrera(self.carrera)
        print(f'Carnet: {self.carnet}, Nombre: {self.nombre}, Carrera: {carrera.nombre}')
    
    def obtener_estuadiantes():
        conexion = conectar_db()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM estudiantes ORDER BY carnet")
        estudiantes = cursor.fetchall()
        cursor.close()
        conexion.close()
        
        for estudiante in estudiantes:
            estudiante = Estudiante(estudiante[0], estudiante[1], estudiante[2])
            estudiante.mostrar_informacion()

        return estudiantes

class Carrera:

    def __init__(self, codigo, nombre) -> None:
        self.codigo = codigo
        self.nombre = nombre

    @staticmethod
    def crear_carrera(codigo, nombre):
        conexion = conectar_db()
        cursor = conexion.cursor()

        try:
            cursor.execute(
                "INSERT INTO carreras (codigo, nombre) VALUES (%s, %s)", 
                (codigo, nombre)
            )
            conexion.commit()
            print(f"Carrera {nombre} registrada exitosamente.")
        except Exception as e:
            print(f"Error al crear la carrera: {e}")
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def obtener_carrera(codigo):
        conexion = conectar_db()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM carreras WHERE codigo = %s", (codigo,))
        carrera = cursor.fetchone()
        cursor.close()
        conexion.close()

        if carrera:
            return Carrera(carrera[0], carrera[1])
        else:
            return None
    
    def obtener_carreras():
        conexion = conectar_db()
        cursor = conexion.cursor()

        cursor.execute("SELECT codigo, nombre FROM carreras")
        carreras = cursor.fetchall()
        cursor.close()
        conexion.close()

        return carreras

    @staticmethod
    def eliminar_carrera(codigo):
        conexion = conectar_db()
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM carrera WHERE codigo = %s", (codigo,))
        conexion.commit()
        cursor.close()
        conexion.close()

    def mostrar_informacion(self):
        print(f'Código: {self.codigo}, Nombre: {self.nombre}')
        cursos = obtener_cursos_disponibles_por_carrera(self.codigo)
        estudiantes = obtener_estudiantes_por_carrera(self.codigo)
        print("Cursos disponibles:")
        for curso in cursos:
            print(f'- codigo: {curso[0]}, nombre: {curso[1]}')
        print("")
        print("Estudiantes asignados a la carrera:")
        for estudiante in estudiantes:
            print(f'- carnet: {estudiante[0]}, nombre: {estudiante[1]}')
            
    def agregar_curso(codigo_carrera, codigo_curso):
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        try:
            cursor.execute("INSERT INTO carreras_cursos (codigo_carrera, codigo_curso) VALUES (%s, %s)", 
                (codigo_carrera, codigo_curso)
            )
            conexion.commit()
            print(f"Curso registrado exitosamente.")
        except Exception as e:
            print(f"Error al crear el curso: {e}")
        finally:
            cursor.close()
            conexion.close()

class Curso:

    def __init__(self, codigo, nombre) -> None:
        self.codigo = codigo
        self.nombre = nombre

    @staticmethod
    def crear_curso(codigo, nombre):
        conexion = conectar_db()
        cursor = conexion.cursor()

        cursor.execute(
            "INSERT INTO cursos (codigo, nombre) VALUES (%s, %s)", 
            (codigo, nombre)
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    @staticmethod
    def obtener_curso(codigo):
        conexion = conectar_db()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM cursos WHERE codigo = %s", (codigo,))
        curso = cursor.fetchone()               
        cursor.close()
        conexion.close()

        if curso:
            return Curso(curso[0], curso[1])
        else:
            return None
        
    def curso_estudiantes(codigo):
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT * FROM estudiantes_cursos WHERE codigo_curso = %s", (codigo,))
        estudiantes = cursor.fetchall()
        
        print("Estudiantes del curso:")
        for estudiante in estudiantes:
            Estudiante.obtener_nombre(estudiante[0])
    
    def obtener_cursos():
        conexion = conectar_db()
        cursor = conexion.cursor()

        cursor.execute("SELECT codigo, nombre FROM cursos")
        cursos = cursor.fetchall()
        cursor.close()
        conexion.close()

        return cursos

    @staticmethod
    def eliminar_curso(codigo):
        conexion = conectar_db()
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM carreras_cursos WHERE codigo_curso = %s", (codigo,))
        cursor.execute("DELETE FROM estudiantes_cursos WHERE codigo_curso = %s", (codigo,))
        cursor.execute("DELETE FROM cursos WHERE codigo = %s", (codigo,))
        conexion.commit()
        cursor.close()
        conexion.close()
        
        print(f"Curso con código {codigo} eliminado.")
    
    def mostrar_informacion(self):
        print(f'Código: {self.codigo}, Nombre: {self.nombre}')


   
def registrar_notas(carnet, codigo_curso, zona, primer_parcial, segundo_parcial, examen_final):
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO notas (carnet, codigo_curso, zona, primer_parcial, segundo_parcial, examen_final)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (carnet, codigo_curso) DO UPDATE
            SET zona = EXCLUDED.zona,
                primer_parcial = EXCLUDED.primer_parcial,
                segundo_parcial = EXCLUDED.segundo_parcial,
                examen_final = EXCLUDED.examen_final;
            """, 
            (carnet, codigo_curso, zona, primer_parcial, segundo_parcial, examen_final)
        )
        conexion.commit()
        print("Notas registradas en la base de datos.")

    except Exception as e:
        print(f"Error al registrar las notas: {e}")
    finally:
        cursor.close()
        conexion.close()

def obtener_notas(carnet, codigo_curso):
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT primer_parcial, segundo_parcial, examen_final FROM notas WHERE carnet = %s AND codigo_curso = %s", 
        (carnet, codigo_curso)
    )
    notas = cursor.fetchone()
    cursor.close()
    conexion.close()

    if notas:
        print(f'Notas: 1er parcial: {notas[0]}, 2do parcial: {notas[1]}, Examen final: {notas[2]}')
    else:
        print('No se encontraron notas para este estudiante en este curso.')


def reporte_mejores_peores_estudiantes(codigo_curso):
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT carnet, 
               (zona + primer_parcial + segundo_parcial + examen_final) AS suma
        FROM notas
        WHERE codigo_curso = %s
        ORDER BY suma DESC
        LIMIT 5;
        """,
        (codigo_curso,)
    )
    mejores = cursor.fetchall()

    cursor.execute(
        """
        SELECT carnet, 
               (zona + primer_parcial + segundo_parcial + examen_final) AS suma
        FROM notas
        WHERE codigo_curso = %s
        ORDER BY suma ASC
        LIMIT 5;
        """,
        (codigo_curso,)
    )
    peores = cursor.fetchall()

    cursor.close()
    conexion.close()

    print("Mejores estudiantes:")
    for estudiante in mejores:
        Estudiante.obtener_nombre(estudiante[0], f', nota: {estudiante[1]}')

    print("\nPeores estudiantes:")
    for estudiante in peores:
        Estudiante.obtener_nombre(estudiante[0], f', nota: {estudiante[1]}')

def promedio_curso(codigo_curso):
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT  
            SUM(zona + primer_parcial + segundo_parcial + examen_final) AS total_suma
        FROM notas
        WHERE codigo_curso = %s
        """,
        (codigo_curso,)
    )
    total_suma = cursor.fetchone()[0] 
    
    cursor.execute(
        """
        SELECT 
            COUNT(*) 
        FROM notas
        WHERE codigo_curso = %s
        """,
        (codigo_curso,)
    )
    cantidad_estudiantes = cursor.fetchone()[0]  

    cursor.close()
    conexion.close()
    
    if cantidad_estudiantes > 0:
        promedio = total_suma / cantidad_estudiantes
        print(f"El promedio del curso {codigo_curso} es: {promedio:.2f}")
    else:
        print(f"No hay estudiantes con notas en el curso {codigo_curso}.")

def promedio_estudiante(carnet):
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Obtener la suma total de notas del estudiante
    cursor.execute(
        """
        SELECT  
            SUM(zona + primer_parcial + segundo_parcial + examen_final) AS total_suma
        FROM notas
        WHERE carnet = %s
        """,
        (carnet,)
    )
    total_suma = cursor.fetchone()[0]  # La suma de las notas de todos los cursos del estudiante
    
    # Obtener la cantidad de cursos en los que el estudiante tiene notas
    cursor.execute(
        """
        SELECT 
            COUNT(*) 
        FROM notas
        WHERE carnet = %s
        """,
        (carnet,)
    )
    cantidad_cursos = cursor.fetchone()[0]  # La cantidad de cursos

    cursor.close()
    conexion.close()
    
    print("")
    if cantidad_cursos > 0:
        promedio = total_suma / cantidad_cursos
        print(f"El promedio del estudiante {carnet} es: {promedio:.2f}")
    else:
        print(f"No hay registros de notas para el estudiante con carnet {carnet}.")

def reporte_notas_faltantes(codigo_curso):
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT estudiantes.carnet, estudiantes.nombre
        FROM estudiantes
        JOIN estudiantes_cursos ON estudiantes.carnet = estudiantes_cursos.carnet
        LEFT JOIN notas ON estudiantes_cursos.carnet = notas.carnet AND estudiantes_cursos.codigo_curso = notas.codigo_curso
        WHERE estudiantes_cursos.codigo_curso = %s
        AND notas.carnet IS NULL
        """,
        (codigo_curso,)
    )
    
    estudiantes_faltantes = cursor.fetchall()

    cursor.close()
    conexion.close()

    # Mostrar reporte de estudiantes faltantes
    if estudiantes_faltantes:
        print(f"Estudiantes sin notas en el curso {codigo_curso}:")
        for carnet, nombre in estudiantes_faltantes:
            print(f"- Carnet: {carnet}, Nombre: {nombre}")
    else:
        print(f"Todos los estudiantes en el curso {codigo_curso} tienen sus notas registradas.")
    

def registrar_estudiante():
    nombre = input("Ingrese el nombre del estudiante: ")
    
    carrera = seleccionar_carrera()
    carnet = generar_carnet(carrera.codigo)
    Estudiante.crear_estudiante(carnet, nombre, carrera.codigo )
    print("")
    print(f"Estudiante {nombre} registrado/a exitosamente con el carnet {carnet} y la carrera {carrera.nombre}.")
        
def editar_estudiante():
    carnet = input("Ingrese el carnet del estudiante a editar: ")
    estudiante = Estudiante.obtener_estudiante(carnet)
    
    if estudiante:
        repetir = True
        while repetir:
            
            print("""
            Seleccione lo que desea editar:
            1. Nombre del estudiante
            2. Carrera
            3. Cursos
            0. Salir
            """)
            opcion = input("Ingrese su opción: ")
            
            if opcion == "1":
                nuevo_nombre = input("Ingrese el nuevo nombre del estudiante: ")
                estudiante.nombre = nuevo_nombre
                sql = "UPDATE estudiantes SET nombre = %s WHERE carnet = %s"
                Estudiante.editar_estudiante(sql, (nuevo_nombre, estudiante.carnet))
                print(f"Nombre actualizado a: {estudiante.nombre}")
            
            elif opcion == "2":
                carrera = seleccionar_carrera()
                nuevo_carnet = generar_carnet(carrera.codigo)
                sql = "UPDATE estudiantes SET carnet = %s, codigo_carrera = %s WHERE carnet = %s"
                Estudiante.editar_estudiante(sql, (nuevo_carnet, carrera.codigo, estudiante.carnet))
                print(f"Carrera actualizada a: {Carrera.obtener_carrera(carrera.codigo).nombre}")
                print(f"Nuevo carnet para {estudiante.nombre}: {nuevo_carnet}")
                repetir = False
        
            elif opcion == "3":
                cursos_disponibles = obtener_cursos_disponibles_por_carrera(estudiante.carrera)

                print("Cursos disponibles para esta carrera:")
                for curso in cursos_disponibles:
                    print(f"Código: {curso[0]}, Nombre: {curso[1]}")

                print("")
                codigo_curso = input("Ingrese el código del curso a asignar: ")

                if codigo_curso in [curso[0] for curso in cursos_disponibles]:
                    asignar_curso_a_estudiante(estudiante.carnet, codigo_curso)
                    print("Curso asignado correctamente.")
                else:
                    print("El curso seleccionado no es válido.")
            elif opcion == "0":
                print("Saliendo del menú de edición.")
                repetir = False
            
            else:
                print("Opción no válida, por favor intente de nuevo.")

def eliminar_estudiante():
    carnet = input("Ingrese el carnet del estudiante a eliminar: ")
    estudiante = Estudiante.obtener_estudiante(carnet)
    if estudiante:
        Estudiante.eliminar_estudiante(carnet)
        print(f"Estudiante con carnet {carnet} eliminado.")

def buscar_estudiante():
    carnet = input("Ingrese el carnet del estudiante: ")
    Estudiante.obtener_estudiante(carnet)
    

def registrar_carrera():
    codigo = input("Ingrese el código de la carrera: ")
    nombre = input("Ingrese el nombre de la carrera: ")
    Carrera.crear_carrera(codigo, nombre)
    
def eliminar_carrera():
    codigo = input("Ingrese el código de la carrera a eliminar: ")
    carrera = Carrera.obtener_carrera(codigo)
    if carrera:
        Carrera.eliminar_carrera(codigo)
        print(f"Carrera con código {codigo} eliminada.")
    else:
        print("Carrera no encontrada.")

def buscar_carrera():
    codigo = input("Ingrese el código de la carrera: ")
    carrera = Carrera.obtener_carrera(codigo)
    if carrera:
        carrera.mostrar_informacion()
    else:
        print("Carrera no encontrad.")
        
def mostrar_carreras():
    carreras = Carrera.obtener_carreras()
    for carrera in carreras:
        print(f"Codigo: {carrera[0]}, Nombre: {carrera[1]}")
        
def registrar_curso():
    codigo_curso = input("Ingrese el código del curso: ")
    nombre = input("Ingrese el nombre del curso: ")
    carrera = seleccionar_carrera()
    Curso.crear_curso(codigo_curso, nombre)
    Carrera.agregar_curso(carrera.codigo, codigo_curso)
    print(f"Curso {nombre} registrado exitosamente.")

def eliminar_curso():
    codigo = input("Ingrese el código del curso a eliminar: ")
    curso = Curso.obtener_curso(codigo)
    if curso:
        Curso.eliminar_curso(codigo)
    else:
        print("Curso no encontrado.")

def buscar_curso():
    codigo = input("Ingrese el código del curso: ")
    curso = Curso.obtener_curso(codigo)
    if curso:
        curso.mostrar_informacion()
        Curso.curso_estudiantes(codigo)
    else:
        print("Curso no encontrado.")

def registrar_notas_menu():
    carnet = input("Ingrese el carnet del estudiante: ")
    estudiante = Estudiante.obtener_estudiante(carnet)
    if estudiante:
        curso = seleccionar_curso()  
        
        codigo_curso = curso.codigo     
        try:
            zona = float(input("Ingrese la zona del curso (0-35): "))
            primer_parcial = float(input("Ingrese la nota del primer parcial (0-15): "))
            segundo_parcial = float(input("Ingrese la nota del segundo parcial (0-15): "))
            examen_final = float(input("Ingrese la nota del examen final (0-35): "))

            if (zona > 35 or primer_parcial > 15 or segundo_parcial > 15 or examen_final > 35):
                print("Error: Las notas deben estar en el rango establecido.")
                return
            
            if zona + primer_parcial + segundo_parcial + examen_final > 100:
                print("Error: La suma de las notas de la zona no puede ser mayor a 100.")
                return

            registrar_notas(carnet, codigo_curso, zona, primer_parcial, segundo_parcial, examen_final)

        except ValueError:
            print("Error: Asegúrese de ingresar un número válido para las notas.")

def buscar_estudiantes():
    criterio = input("Ingrese el criterio de búsqueda (nombre o carnet): ")
    print(f"Buscando estudiantes por {criterio}...")

def ver_alumnos_en_curso():
    codigo_curso = input("Ingrese el código del curso: ")
    print(f"Viendo alumnos inscritos en el curso {codigo_curso}...")

def reporte_mejores_peores_estudiantes_menu():
    cursos = Curso.obtener_cursos()
    for curso in cursos:
        Curso(curso[0], curso[1]).mostrar_informacion()
        
    curso = seleccionar_curso()
    reporte_mejores_peores_estudiantes(curso.codigo)

def reporte_promedios_menu():
    print("""
        Seleccione lo que desea ver:
        1. Promedio de un curso
        2. Promedio de un estudiante
        0. Salir
        """)
    opcion = input("Ingrese su opción: ")
    if opcion == "1":
        cursos = Curso.obtener_cursos()
        for curso in cursos:
            Curso(curso[0], curso[1]).mostrar_informacion()
        curso = seleccionar_curso()
        promedio_curso(curso.codigo)
    elif opcion == "2":
        carnet = input("Ingrese el carnet del estudiante: ")
        estudiante = Estudiante.obtener_estudiante(carnet)
        if estudiante:
            promedio_estudiante(carnet)
    elif opcion == "0":
        print("Saliendo del menú.")
    else:
        print("Opción no válida, por favor intente de nuevo.")


def reporte_notas_faltantes_menu():
    cursos = Curso.obtener_cursos()
    for curso in cursos:
        Curso(curso[0], curso[1]).mostrar_informacion()
    curso = seleccionar_curso()
    reporte_notas_faltantes(curso.codigo)
    
def generar_carnet(codigo_carrera):
    año_actual = datetime.datetime.now().year
    ultimos_dos_digitos_año = str(año_actual)[-2:]
    digitos_random = str(random.randint(1000, 9999))
    carnet = f"{codigo_carrera}-{ultimos_dos_digitos_año}-{digitos_random}"
    return carnet

def seleccionar_carrera():
    print("    Carreras disponibles:")
    carreras = Carrera.obtener_carreras()
    
    for carrera in carreras:
        print(f"    Código: {carrera[0]}, Nombre: {carrera[1]}")
    
    codigo_carrera = input("Ingrese el código de la carrera: ")
    carrera = None
    if codigo_carrera:
        carrera = Carrera.obtener_carrera(codigo_carrera)
    
    if carrera:
        return carrera
    else:
        print("Seleccione una carrera valida.")
        return seleccionar_carrera()
    
def seleccionar_curso():
    print("")
    codigo_curso = input("Ingrese el código del curso: ")
    curso = None
    if codigo_curso:
        curso = Curso.obtener_curso(codigo_curso)

    if curso:
        return curso
    else:
        print("Seleccione un curso valido.")
        return seleccionar_curso()
    
def obtener_cursos_disponibles_por_carrera(codigo_carrera):
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT c.codigo, c.nombre
        FROM cursos c
        INNER JOIN carreras_cursos cc ON c.codigo = cc.codigo_curso
        WHERE cc.codigo_carrera = %s
    """, (codigo_carrera,))

    cursos = cursor.fetchall()
    cursor.close()
    conexion.close()

    return cursos

def obtener_estudiantes_por_carrera(codigo_carrera):
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT carnet, nombre
        FROM estudiantes 
        WHERE codigo_carrera = %s
        ORDER BY carnet ASC
    """, (codigo_carrera,))

    estudiantes = cursor.fetchall()
    cursor.close()
    conexion.close()

    return estudiantes

def asignar_curso_a_estudiante(carnet, codigo_curso):
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO estudiantes_cursos (carnet, codigo_curso)
        VALUES (%s, %s)
        ON CONFLICT (carnet, codigo_curso) DO NOTHING;
    """, (carnet, codigo_curso))

    conexion.commit()
    cursor.close()
    conexion.close()


def salir():
    print("Saliendo del programa...")
    sys.exit()
    
def mostrar_menu():
    print("""
        0. Salir
        
    Gestión de Estudiantes
        1. Registrar Estudiante
        2. Editar Estudiante
        3. Eliminar Estudiante
        4. Buscar Estudiante
        5. Mostrar Estudiantes
    
    Gestión de Cursos
        6. Registrar Curso
        7. Eliminar Curso
        8. Buscar Curso y sus alumnos
        
    Gestión de Carreras
        9. Registrar Carrera
        10. Eliminar Carrera
        11. Buscar Carrera
        12. Mostrar Carreras
        

    Gestión de Notas y Reportes
        13. Registrar Notas
        14. Estudiantes con Mejores y Peores Calificaciones
        15. Promedios por Curso y Estudiante
        16. Alumnos con Notas Faltantes
    """)

if __name__ == "__main__":
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            registrar_estudiante()
        elif opcion == "2":
            editar_estudiante()
        elif opcion == "3":
            eliminar_estudiante()
        elif opcion == "4":
            buscar_estudiante()
        elif opcion == "5":
            Estudiante.obtener_estuadiantes()
        elif opcion == "6":
            registrar_curso()
        elif opcion == "7":
            eliminar_curso()
        elif opcion == "8":
            buscar_curso()
        elif opcion == "9":
            registrar_carrera()
        elif opcion == "10":
            eliminar_carrera()
        elif opcion == "11":
            buscar_carrera()
        elif opcion == "12":
            mostrar_carreras()
        elif opcion == "13":
            registrar_notas_menu()
        elif opcion == "14":
            reporte_mejores_peores_estudiantes_menu()
        elif opcion == "15":
            reporte_promedios_menu()
        elif opcion == "16":
            reporte_notas_faltantes_menu()
        elif opcion == "0":
            salir()
        else:
            print("Opción no válida, intente de nuevo.")
