CREATE DATABESE IF NOT EXISTS curzo_web;

USE curzo_web;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    edad INT NOT NULL,
);

ININSERT INTO usuarios (nombre, edad) VALUES ('Ana', 20);
INSERT INTO usuarios (nombre, edad) VALUES ('Luis', 25);
INSERT INTO usuarios (nombre, edad) VALUES ('Camila', 22);