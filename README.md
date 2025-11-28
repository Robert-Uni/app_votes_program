#Proyecto de Votacion
#Resumen
Este proyecto implementa un sistema básico de votaciones con API REST usando Flask y MySQL.
Permite registrar votos, consultar estadísticas y visualizar gráficos de resultados.

#Requisitos

Asegúrate de tener instalado:

Python 3.10+

MySQL Server

pip (gestor de paquetes)

#instalacion

git clone https://github.com/Robert-Uni/app_votes_program/tree/main#readme

Base de Datos

CREATE DATABASE votaciones;
USE votaciones;

CREATE TABLE voter (
    id_voter INT PRIMARY KEY AUTO_INCREMENT UNIQUE,
    Name_voter VARCHAR(100),
    email VARCHAR(100),
    has_voted TINYINT DEFAULT 0
);

CREATE TABLE candidate (
    id_candidate INT PRIMARY KEY AUTO_INCREMENT,
    name_candidate VARCHAR(100),
    party VARCHAR(100),
    votes INT
);

CREATE TABLE vote (
    id_vote INT PRIMARY KEY AUTO_INCREMENT,
    id_voter INT UNIQUE NOT NULL,
    id_candidate INT NOT NULL,
    FOREIGN KEY(id_candidate) REFERENCES candidate(id_candidate),
    FOREIGN KEY(id_voter) REFERENCES voter(id_voter)
);

#EJEMPLO DE USO DE LA API (POSTMAN)
<img width="1907" height="1014" alt="image" src="https://github.com/user-attachments/assets/966173ae-bc6c-4a45-bdb1-51453c2144be" />
<img width="1919" height="1017" alt="image" src="https://github.com/user-attachments/assets/5be7f49b-7332-4031-b9a0-13c503984cce" />


Grafica

<img width="1919" height="1009" alt="image" src="https://github.com/user-attachments/assets/76488d8a-57f3-4592-bd3a-661c7b1b2841" />

