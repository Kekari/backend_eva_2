-- Antes de ejecutar el script, cambia CAMBIAR_ESTA_CLAVE por la clave que quieras usar.
-- Pon esa misma clave en PASSWORD en el archivo .env de Django.

CREATE DATABASE IF NOT EXISTS `tflow`
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'admin'@'%'
    IDENTIFIED BY 'CAMBIAR_ESTA_CLAVE';

GRANT ALL PRIVILEGES ON `tflow`.* TO 'admin'@'%';
FLUSH PRIVILEGES;
