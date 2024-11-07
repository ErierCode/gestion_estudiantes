CREATE TABLE carreras (
    codigo SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE cursos (
    codigo VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100)
);

CREATE TABLE carreras_cursos (
    codigo_carrera INT,
    codigo_curso VARCHAR(20),
    PRIMARY KEY (codigo_carrera, codigo_curso),
    FOREIGN KEY (codigo_carrera) REFERENCES carreras(codigo),
    FOREIGN KEY (codigo_curso) REFERENCES cursos(codigo)
);

CREATE TABLE estudiantes (
    carnet VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100),
    codigo_carrera INT, 
    FOREIGN KEY (codigo_carrera) REFERENCES carreras(codigo)
);

CREATE TABLE estudiantes_cursos (
    carnet VARCHAR(20),
    codigo_curso VARCHAR(20),
    PRIMARY KEY (carnet, codigo_curso),
    FOREIGN KEY (carnet) REFERENCES estudiantes(carnet),
    FOREIGN KEY (codigo_curso) REFERENCES cursos(codigo)
);

CREATE TABLE notas (
    carnet VARCHAR(20),
    codigo_curso VARCHAR(20),
    zona DECIMAL(5,2),
    primer_parcial DECIMAL(5,2),
    segundo_parcial DECIMAL(5,2),
    examen_final DECIMAL(5,2),
    PRIMARY KEY (carnet, codigo_curso),
    FOREIGN KEY (carnet) REFERENCES estudiantes(carnet),
    FOREIGN KEY (codigo_curso) REFERENCES cursos(codigo)
);
