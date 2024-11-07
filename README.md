# Proyecto de Gestión de Estudiantes

Este proyecto es una aplicación para gestionar estudiantes usando una base de datos PostgreSQL. A continuación, se explican los pasos para configurar el entorno de desarrollo utilizando Docker, junto con los contenedores necesarios para PostgreSQL y pgAdmin.

## Requisitos Previos

- **Docker** instalado en tu sistema. Si aún no lo tienes, puedes obtenerlo desde [aquí](https://docs.docker.com/get-docker/).

## Configuración del Entorno

### 1. Instalar Docker

Asegúrate de tener Docker correctamente instalado y en funcionamiento en tu sistema. Sigue las instrucciones de instalación en la [documentación oficial de Docker](https://docs.docker.com/get-docker/).

### 2. Crear Contenedores para PostgreSQL y pgAdmin

- **Contenedor de PostgreSQL**: Ejecuta el siguiente comando para crear el contenedor de PostgreSQL.

  ```bash
  docker run --name postgres-container -e POSTGRES_USER=usuario -e POSTGRES_PASSWORD=contraseña -e POSTGRES_DB=nombre_db -p 5432:5432 -d postgres

- Reemplaza usuario, contraseña y nombre_db con los valores deseados para tu base de datos.

- **Contenedor de pgAdmin**: Ejecuta el siguiente comando para crear el contenedor de pgAdmin, que te permitirá gestionar la base de datos desde una interfaz web.
  ```bash
    docker run --name pgadmin-container -e PGADMIN_DEFAULT_EMAIL=correo@ejemplo.com -e PGADMIN_DEFAULT_PASSWORD=contraseña -p 80:80 -d dpage/pgadmin4

- Reemplaza correo@ejemplo.com y contraseña con los datos que utilizarás para iniciar sesión en pgAdmin.
### 3. Configuración de la Base de Datos en pgAdmin

- Accede a pgAdmin desde tu navegador ingresando http://localhost y usa las credenciales configuradas (correo y contraseña).

- En pgAdmin, añade una nueva conexión al servidor de PostgreSQL:

- Haz clic en Add New Server.
- En la pestaña General, asigna un nombre a tu servidor.
- En la pestaña Connection, usa estos valores:
Host: postgres-container (o localhost si prefieres conectar localmente).
Port: 5432.
Username y Password: las mismas configuradas en el contenedor de PostgreSQL.
- Haz clic en Save para conectar.

### 4. Crear la Base de Datos y las Tablas

- **Crear la base de datos**:  Utiliza el siguiente comando en pgAdmin o en la línea de comandos de PostgreSQL:

  ```bash
  CREATE DATABASE nombre_db;

- Reemplaza nombre_db con el nombre de la base de datos que configuraste en el contenedor de PostgreSQL.
- **Crear las tablas**: Ver el código sql en **tablas_muestra.sql**

### 5. Conectar la Aplicación

Ahora que PostgreSQL está configurado y conectado, puedes ejecutar la aplicación y empezar a gestionar las notas de los estudiantes. Asegúrate de que el archivo de configuración de la aplicación tenga los mismos datos de acceso configurados en PostgreSQL.