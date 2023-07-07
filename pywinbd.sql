-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: localhost
-- Время создания: Июл 07 2023 г., 22:01
-- Версия сервера: 10.4.28-MariaDB
-- Версия PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `pywinbd`
--

-- --------------------------------------------------------

--
-- Структура таблицы `levels`
--

CREATE TABLE `levels` (
  `id` int(11) NOT NULL,
  `name` tinytext NOT NULL,
  `desc` tinytext NOT NULL,
  `version` tinyint(4) NOT NULL,
  `authorID` int(11) NOT NULL,
  `gameVersion` tinyint(2) NOT NULL,
  `likes` int(11) NOT NULL,
  `downloads` int(11) NOT NULL,
  `audioTrack` tinyint(2) NOT NULL,
  `levelLength` tinyint(1) NOT NULL,
  `stars` tinyint(2) NOT NULL,
  `difficulty` tinyint(1) NOT NULL,
  `starAuto` tinyint(1) NOT NULL,
  `starDemon` tinyint(1) NOT NULL,
  `starDemonDiff` tinyint(1) NOT NULL,
  `rate` tinyint(1) NOT NULL,
  `starCoins` tinyint(1) NOT NULL,
  `coins` tinyint(1) NOT NULL,
  `original` int(11) NOT NULL,
  `twoPlayer` tinyint(1) NOT NULL,
  `songID` int(11) NOT NULL,
  `requestedStars` tinyint(2) NOT NULL,
  `isLDM` tinyint(1) NOT NULL,
  `objects` int(11) NOT NULL,
  `password` tinyint(4) NOT NULL DEFAULT 0,
  `uploadDate` int(11) NOT NULL DEFAULT 0,
  `updateDate` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `levels`
--

INSERT INTO `levels` (`id`, `name`, `desc`, `version`, `authorID`, `gameVersion`, `likes`, `downloads`, `audioTrack`, `levelLength`, `stars`, `difficulty`, `starAuto`, `starDemon`, `starDemonDiff`, `rate`, `starCoins`, `coins`, `original`, `twoPlayer`, `songID`, `requestedStars`, `isLDM`, `objects`, `password`, `uploadDate`, `updateDate`) VALUES
(1, 'test level 1', '', 1, 1, 21, 221, 323, 0, 1, 2, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0),
(2, 'test level 2', '', 1, 1, 21, 23, 37, 0, 0, 5, 4, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0),
(3, 'test level 3', '', 1, 1, 21, 623, 87, 0, 0, 3, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0),
(4, 'test level 4', '', 1, 1, 21, 45, 56, 0, 0, 7, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0),
(6, 'test level 6', '', 1, 1, 21, 46, 3558, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0),
(7, 'test level 7', '', 1, 1, 21, 46, 3558, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0),
(8, 'test level 8', '', 1, 1, 21, 465, 35583, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0),
(9, 'test level 9', '', 1, 1, 21, 29, 155, 0, 0, 9, 5, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0),
(10, 'test level 10', '', 1, 1, 21, 29, 155, 0, 0, 10, 5, 0, 1, 3, 1, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0),
(11, 'test level 11', '', 1, 1, 21, 29, 155, 0, 0, 10, 0, 0, 1, 4, 1, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0),
(12, 'test level 12', '', 1, 1, 21, 29, 155, 0, 0, 10, 0, 0, 1, 5, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0),
(128, 'test level 5', '', 1, 1, 21, 6787, 355, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 1, 0, 0);

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `userName` varchar(255) NOT NULL,
  `mail` varchar(255) NOT NULL,
  `role` int(11) NOT NULL,
  `passhash` varchar(255) NOT NULL,
  `verifed` int(11) NOT NULL,
  `stars` int(11) NOT NULL,
  `diamonds` int(11) NOT NULL,
  `coins` int(11) NOT NULL,
  `usr_coins` int(11) NOT NULL,
  `demons` int(11) NOT NULL,
  `cp` int(11) NOT NULL,
  `iconkit` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`iconkit`)),
  `networks` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`networks`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `userName`, `mail`, `role`, `passhash`, `verifed`, `stars`, `diamonds`, `coins`, `usr_coins`, `demons`, `cp`, `iconkit`, `networks`) VALUES
(24, 'WINnerGMD', 'sprot@gmail.com', 0, '$2b$12$VWAACqVFSNt8bIiWVXdsyOLtjPONoXKdJR5unq0jgOon9eL0vUe6W', 0, 900, 11894, 45, 78, 80, 0, '{\"color1\": 3, \"color2\": 5, \"accBall\": 1, \"accBird\": 1, \"accDart\": 1, \"accGlow\": 1, \"accIcon\": 131, \"accShip\": 1, \"accRobot\": 1, \"accSpider\": 1, \"accExplosion\": 1}', '{\"youtube\": \"hui\"}'),
(25, 'WINnerGDLol', 'enzor.pro777@gmail.hui', 0, '$2b$12$VWAACqVFSNt8bIiWVXdsyOLtjPONoXKdJR5unq0jgOon9eL0vUe6W', 0, 0, 0, 0, 0, 0, 0, '{\"color1\": 5, \"color2\": 2, \"accBall\": 1, \"accBird\": 1, \"accDart\": 1, \"accGlow\": 0, \"accIcon\": 127, \"accShip\": 1, \"accRobot\": 1, \"accSpider\": 1, \"accExplosion\": 1}', '{\"youtube\": \"hui\"}');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `levels`
--
ALTER TABLE `levels`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `levels`
--
ALTER TABLE `levels`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=130;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
