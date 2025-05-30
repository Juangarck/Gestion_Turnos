-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación primer version: 22-04-2020 a las 08:23:55
-- Versión del servidor: 10.4.10-MariaDB
-- Versión de PHP: 7.1.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `turnero`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `atencion`
--

CREATE TABLE `atencion` (
  `id` int(11) NOT NULL,
  `turno` varchar(5) COLLATE utf8_spanish2_ci NOT NULL,
  `idCaja` int(11) NOT NULL,
  `idUsuario` int(11) NOT NULL,
  `atendido` int(11) NOT NULL,
  `fechaAtencion` datetime NOT NULL,
  `idTurno` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cajas`
--

CREATE TABLE `cajas` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) COLLATE utf8_spanish2_ci NOT NULL,
  `idUsuario` int(11) NOT NULL,
  `fecha_de_registro` datetime NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

--
-- Volcado de datos para la tabla `cajas`
--

INSERT INTO `cajas` (`id`, `nombre`, `idUsuario`, `fecha_de_registro`) VALUES
(1, 'Ventanilla 1', 8, '0000-00-00 00:00:00'),
(2, 'Ventanilla 2', 9, '0000-00-00 00:00:00'),
(3, 'Ventanilla 3', 10, '0000-00-00 00:00:00'),
(4, 'Ventanilla 4', 11, '0000-00-00 00:00:00'),
(5, 'Ventanilla 5', 12, '2020-02-14 17:27:38');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `info_empresa`
--

CREATE TABLE `info_empresa` (
  `id` int(11) NOT NULL,
  `logo` varchar(100) COLLATE utf8_spanish2_ci NOT NULL,
  `nombre` varchar(100) COLLATE utf8_spanish2_ci NOT NULL,
  `direccion` varchar(100) COLLATE utf8_spanish2_ci NOT NULL,
  `telefono` varchar(100) COLLATE utf8_spanish2_ci NOT NULL,
  `correo` varchar(100) COLLATE utf8_spanish2_ci NOT NULL,
  `fecha_actualizacion` datetime NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

--
-- Volcado de datos para la tabla `info_empresa`
--

INSERT INTO `info_empresa` (`id`, `logo`, `nombre`, `direccion`, `telefono`, `correo`, `fecha_actualizacion`) VALUES
(1, 'img/49550310_598832710562102_5995102219237874750_n.jpg', 'Agencia Catastral de Cundinamarca', 'Calle 24 # 43a-42 Bogotá, Colombia', '3225089900', 'atencionalciudadano@acc.gov.co', '2024-05-08 16:26:11');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `noticias`
--

CREATE TABLE `noticias` (
  `id` int(11) NOT NULL,
  `noticia` varchar(255) COLLATE utf8_spanish2_ci NOT NULL,
  `fecha` datetime NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

-- --------------------------------------------------------
-- 
-- Estructura de tabla para los clientes o interesados
-- 
CREATE TABLE `clientes` (
    `id` int(11) NOT NULL,
    `nombre` VARCHAR(100) NOT NULL,
    `cedula` VARCHAR(20) UNIQUE NOT NULL,
    `telefono` VARCHAR(20),
    `email` VARCHAR(100),
    `municipio` VARCHAR(100),
    `direccion` TEXT,
    `fechaRegistro` DATETIME NOT NULL,
    `autorizacion` BOOLEAN NOT NULL DEFAULT TRUE
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

--
-- Estructura de tabla para la tabla `turnos`
--

CREATE TABLE `turnos` (
  `id` int(11) NOT NULL,
  `turno` varchar(5) COLLATE utf8_spanish2_ci NOT NULL,
  `atendido` int(11) NOT NULL,
  `idCliente` int(11) NOT NULL,
  `tramite` VARCHAR(1),
  `fechaRegistro` datetime NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `usuario` varchar(100) COLLATE utf8_spanish2_ci NOT NULL,
  `password` varchar(100) COLLATE utf8_spanish2_ci NOT NULL,
  `idCaja` int(11) NOT NULL,
  `fecha_alta` datetime NOT NULL,
  `fecha_actualizacion` datetime NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `usuario`, `password`, `idCaja`, `fecha_alta`, `fecha_actualizacion`) VALUES
(9, 'laura', '680e89809965ec41e64dc7e447f175ab', 2, '2018-01-11 03:04:27', '0000-00-00 00:00:00'),
(8, 'oscar', 'f156e7995d521f30e6c59a3d6c75e1e5', 1, '2018-01-11 03:04:16', '0000-00-00 00:00:00'),
(10, 'rocio', '325daa03a34823cef2fc367c779561ba', 3, '2018-01-11 03:04:58', '0000-00-00 00:00:00'),
(11, 'patricio', '295299b687749528c9a9e551d11e17ea', 4, '2018-01-11 03:05:07', '0000-00-00 00:00:00'),
(12, 'Alberto', '177dacb14b34103960ec27ba29bd686b', 5, '2020-02-14 17:27:56', '0000-00-00 00:00:00');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `atencion`
--
ALTER TABLE `atencion`
  ADD PRIMARY KEY (`id`),
  ADD CONSTRAINT fk_funcionario FOREIGN KEY (idUsuario) REFERENCES usuarios(id),
  ADD CONSTRAINT fk_turno FOREIGN KEY (idTurno) REFERENCES turnos(id),
  ADD CONSTRAINT fk_ventanilla FOREIGN KEY (idCaja) REFERENCES cajas(id);


--
-- Indices de la tabla `cajas`
--
ALTER TABLE `cajas`
  ADD PRIMARY KEY (`id`),
  ADD CONSTRAINT fk_usuario
  FOREIGN KEY (idUsuario) REFERENCES usuarios(id);

--
-- Indices de la tabla `info_empresa`
--
ALTER TABLE `info_empresa`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `noticias`
--
ALTER TABLE `noticias`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `turnos`
--
ALTER TABLE `turnos`
  ADD PRIMARY KEY (`id`),
  ADD CONSTRAINT fk_cliente
  FOREIGN KEY (idCliente) REFERENCES clientes(id);
--
-- Indices de la tabla `usuarios` SE OMITE AGREGAR LA FK DE CAJA, PORQUE YA ESTA REFERENCIADA EN CAJA Y SE DEBE MODIFCAR EL ESQUEMA DE LA DB
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`);
--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `atencion`
--
ALTER TABLE `atencion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cajas`
--
ALTER TABLE `cajas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `info_empresa`
--
ALTER TABLE `info_empresa`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `noticias`
--
ALTER TABLE `noticias`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `turnos`
--
ALTER TABLE `turnos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
