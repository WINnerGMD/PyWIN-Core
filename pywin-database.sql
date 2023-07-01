-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: localhost
-- Время создания: Июл 01 2023 г., 16:11
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
-- База данных: `pywin-database`
--

-- --------------------------------------------------------

--
-- Структура таблицы `levels`
--

CREATE TABLE `levels` (
  `levelID` int(11) NOT NULL,
  `levelName` tinytext NOT NULL,
  `levelDesc` tinytext NOT NULL,
  `levelVersion` tinyint(4) NOT NULL,
  `userID` int(11) NOT NULL,
  `accountID` int(11) NOT NULL,
  `gameVersion` tinyint(2) NOT NULL,
  `likes` int(11) NOT NULL,
  `downloads` int(11) NOT NULL,
  `audioTrack` tinyint(2) NOT NULL,
  `levelLength` tinyint(1) NOT NULL,
  `starStars` tinyint(2) NOT NULL,
  `starDifficulty` tinyint(1) NOT NULL,
  `starAuto` tinyint(1) NOT NULL,
  `starDemon` tinyint(1) NOT NULL,
  `starDemonDiff` tinyint(1) NOT NULL,
  `starFeatured` tinyint(1) NOT NULL,
  `starEpic` tinyint(1) NOT NULL,
  `starCoins` tinyint(1) NOT NULL,
  `coins` tinyint(1) NOT NULL,
  `original` int(11) NOT NULL,
  `twoPlayer` tinyint(1) NOT NULL,
  `songID` int(11) NOT NULL,
  `requestedStars` tinyint(2) NOT NULL,
  `isLDM` tinyint(1) NOT NULL,
  `objects` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `levels`
--

INSERT INTO `levels` (`levelID`, `levelName`, `levelDesc`, `levelVersion`, `userID`, `accountID`, `gameVersion`, `likes`, `downloads`, `audioTrack`, `levelLength`, `starStars`, `starDifficulty`, `starAuto`, `starDemon`, `starDemonDiff`, `starFeatured`, `starEpic`, `starCoins`, `coins`, `original`, `twoPlayer`, `songID`, `requestedStars`, `isLDM`, `objects`) VALUES
(1, 'test level 1', '', 1, 1, 1, 21, 221, 323, 0, 0, 2, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 1),
(2, 'test level 2', '', 1, 1, 1, 21, 23, 37, 0, 0, 5, 4, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 1),
(3, 'test level 3', '', 1, 1, 1, 21, 623, 87, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1),
(4, 'test level 4', '', 1, 1, 1, 21, 45, 56, 0, 0, 7, 5, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 1),
(5, 'test level 5', '', 1, 1, 1, 21, 6787, 355, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1),
(6, 'test level 6', '', 1, 1, 1, 21, 46, 3558, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1),
(7, 'test level 7', '', 1, 1, 1, 21, 46, 3558, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1),
(8, 'test level 8', '', 1, 1, 1, 21, 465, 35583, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 1),
(9, 'test level 9', '', 1, 1, 1, 21, 29, 155, 0, 0, 9, 5, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 1),
(10, 'test level 10', '', 1, 1, 1, 21, 29, 155, 0, 0, 10, 5, 0, 1, 3, 1, 0, 0, 0, 0, 0, 0, 2, 0, 1),
(11, 'test level 11', '', 1, 1, 1, 21, 29, 155, 0, 0, 10, 0, 0, 1, 4, 1, 0, 0, 0, 0, 0, 0, 2, 0, 1),
(12, 'test level 12', '', 1, 1, 1, 21, 29, 155, 0, 0, 10, 0, 0, 1, 5, 1, 0, 0, 0, 0, 0, 0, 2, 0, 1);

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `userName` varchar(255) NOT NULL,
  `mail` varchar(255) NOT NULL,
  `passhash` varchar(255) NOT NULL,
  `verifed` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `userName`, `mail`, `passhash`, `verifed`) VALUES
(24, 'WINnerGMD', 'sprot@gmail.com', '$2b$12$VWAACqVFSNt8bIiWVXdsyOLtjPONoXKdJR5unq0jgOon9eL0vUe6W', 0),
(25, 'WINnerGDLol', 'enzor.pro777@gmail.hui', '$2b$12$VWAACqVFSNt8bIiWVXdsyOLtjPONoXKdJR5unq0jgOon9eL0vUe6W', 0);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `levels`
--
ALTER TABLE `levels`
  ADD PRIMARY KEY (`levelID`);

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
  MODIFY `levelID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
