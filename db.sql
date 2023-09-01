-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Хост: localhost:3306
-- Время создания: Сен 01 2023 г., 05:20
-- Версия сервера: 8.0.34-0ubuntu0.20.04.1
-- Версия PHP: 7.4.3-4ubuntu2.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `mysqladmin1`
--

-- --------------------------------------------------------

--
-- Структура таблицы `comments`
--

CREATE TABLE `comments` (
  `id` int NOT NULL,
  `authorId` int DEFAULT NULL,
  `authorName` varchar(255) DEFAULT NULL,
  `levelID` int NOT NULL,
  `content` text,
  `timestamp` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '',
  `likes` int DEFAULT NULL,
  `progress` int DEFAULT NULL,
  `is_spam` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `gauntlets`
--

CREATE TABLE `gauntlets` (
  `id` int NOT NULL,
  `indexpack` int NOT NULL,
  `levels` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `levels`
--

CREATE TABLE `levels` (
  `id` int NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `desc` text,
  `version` int DEFAULT NULL,
  `authorID` int DEFAULT NULL,
  `authorName` varchar(255) DEFAULT NULL,
  `gameVersion` int DEFAULT NULL,
  `likes` int DEFAULT NULL,
  `downloads` int DEFAULT NULL,
  `AudioTrack` int DEFAULT NULL,
  `lenght` int DEFAULT NULL,
  `stars` int DEFAULT NULL,
  `difficulty` int DEFAULT NULL,
  `coins` int DEFAULT NULL,
  `user_coins` int DEFAULT NULL,
  `rate` int DEFAULT NULL,
  `original` int DEFAULT NULL,
  `two_players` int DEFAULT NULL,
  `song_id` int DEFAULT NULL,
  `is_ldm` int DEFAULT NULL,
  `objects` int DEFAULT NULL,
  `password` int DEFAULT NULL,
  `upload_date` varchar(255) DEFAULT NULL,
  `update_date` int DEFAULT NULL,
  `LevelString` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `posts`
--

CREATE TABLE `posts` (
  `id` int NOT NULL,
  `accountID` int DEFAULT NULL,
  `content` text,
  `likes` int NOT NULL DEFAULT '0',
  `timestamp` varchar(255) NOT NULL DEFAULT '0-0-0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `roles`
--

CREATE TABLE `roles` (
  `id` int NOT NULL,
  `color` varchar(255) DEFAULT NULL,
  `BadgeID` int DEFAULT NULL,
  `typeMod` int DEFAULT NULL,
  `rateLevels` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `roles`
--

INSERT INTO `roles` (`id`, `color`, `BadgeID`, `typeMod`, `rateLevels`) VALUES
(1, '121', 0, 0, 0);

-- --------------------------------------------------------

--
-- Структура таблицы `songs`
--

CREATE TABLE `songs` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `author` varchar(255) NOT NULL,
  `link` text NOT NULL,
  `size` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `userName` varchar(255) DEFAULT NULL,
  `mail` varchar(255) DEFAULT NULL,
  `role` int DEFAULT NULL,
  `passhash` varchar(255) DEFAULT NULL,
  `verified` tinyint(1) DEFAULT NULL,
  `stars` int DEFAULT NULL,
  `diamonds` int DEFAULT NULL,
  `coins` int DEFAULT NULL,
  `usr_coins` int DEFAULT NULL,
  `demons` int DEFAULT NULL,
  `cp` int DEFAULT NULL,
  `iconkits` json DEFAULT NULL,
  `networks` json DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `gauntlets`
--
ALTER TABLE `gauntlets`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `levels`
--
ALTER TABLE `levels`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `songs`
--
ALTER TABLE `songs`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `userName` (`userName`),
  ADD UNIQUE KEY `mail` (`mail`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `comments`
--
ALTER TABLE `comments`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;

--
-- AUTO_INCREMENT для таблицы `gauntlets`
--
ALTER TABLE `gauntlets`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;

--
-- AUTO_INCREMENT для таблицы `levels`
--
ALTER TABLE `levels`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;

--
-- AUTO_INCREMENT для таблицы `posts`
--
ALTER TABLE `posts`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;

--
-- AUTO_INCREMENT для таблицы `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;

--
-- AUTO_INCREMENT для таблицы `songs`
--
ALTER TABLE `songs`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
