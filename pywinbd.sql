-- phpMyAdmin SQL Dump
-- version 5.1.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jul 07, 2023 at 11:36 AM
-- Server version: 5.7.24
-- PHP Version: 8.0.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pywinbd`
--

-- --------------------------------------------------------

--
-- Table structure for table `levels`
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
  `password` tinyint(4) NOT NULL DEFAULT '0',
  `uploadDate` int(11) NOT NULL DEFAULT '0',
  `updateDate` int(11) NOT NULL DEFAULT '0',
  `string` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `levels`
--

INSERT INTO `levels` (`id`, `name`, `desc`, `version`, `authorID`, `gameVersion`, `likes`, `downloads`, `audioTrack`, `levelLength`, `stars`, `difficulty`, `starAuto`, `starDemon`, `starDemonDiff`, `rate`, `starCoins`, `coins`, `original`, `twoPlayer`, `songID`, `requestedStars`, `isLDM`, `objects`, `password`, `uploadDate`, `updateDate`, `string`) VALUES
(1, 'test level 1', '', 1, 1, 21, 221, 323, 0, 1, 2, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, ''),
(2, 'test level 2', '', 1, 1, 21, 23, 37, 0, 0, 5, 4, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, ''),
(3, 'test level 3', '', 1, 1, 21, 623, 87, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, ''),
(4, 'test level 4', '', 1, 1, 21, 46, 56, 0, 0, 7, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, ''),
(6, 'test level 6', '', 1, 1, 21, 45, 3558, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, ''),
(7, 'test level 7', '', 1, 1, 21, 46, 3558, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, ''),
(8, 'test level 8', '', 1, 1, 21, 465, 35583, 0, 0, 9, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, ''),
(9, 'test level 9', '', 1, 1, 21, 29, 155, 0, 0, 7, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, ''),
(10, 'test level 10', '', 1, 1, 21, 29, 155, 0, 0, 10, 5, 0, 1, 3, 1, 1, 1, 0, 0, 0, 2, 0, 1, 0, 0, 0, ''),
(11, 'test level 11', '', 1, 1, 21, 30, 155, 0, 0, 1, 0, 1, 1, 4, 1, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, ''),
(12, 'test level 12', '', 1, 1, 21, 29, 155, 0, 0, 3, 2, 0, 1, 5, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, ''),
(128, 'test level 5', '', 1, 1, 21, 6787, 355, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 1, 0, 0, ''),
(129, 'test level 8', '', 1, 1, 21, 465, 35583, 0, 0, 7, 4, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, '');

-- --------------------------------------------------------

--
-- Table structure for table `users`
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
  `iconkit` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `networks` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `userName`, `mail`, `role`, `passhash`, `verifed`, `stars`, `diamonds`, `coins`, `usr_coins`, `demons`, `cp`, `iconkit`, `networks`) VALUES
(24, 'WINnerGMD', 'sprot@gmail.com', 2, '$2b$12$VWAACqVFSNt8bIiWVXdsyOLtjPONoXKdJR5unq0jgOon9eL0vUe6W', 0, 0, 0, 0, 0, 0, 0, '{\"color1\": 0, \"color2\": 3, \"accBall\": 1, \"accBird\": 1, \"accDart\": 1, \"accGlow\": 0, \"accIcon\": 1, \"accShip\": 1, \"accRobot\": 1, \"accSpider\": 1, \"accExplosion\": 1}', '{\"youtube\": \"hui\"}'),
(25, 'WINnerGDLol', 'enzor.pro777@gmail.hui', 1, '$2b$12$VWAACqVFSNt8bIiWVXdsyOLtjPONoXKdJR5unq0jgOon9eL0vUe6W', 0, 37, 0, 4, 0, 0, 0, '{\"color1\": 3, \"color2\": 0, \"accBall\": 1, \"accBird\": 1, \"accDart\": 1, \"accGlow\": 0, \"accIcon\": 3, \"accShip\": 1, \"accRobot\": 1, \"accSpider\": 1, \"accExplosion\": 1}', '{\"youtube\": \"hui\"}');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `levels`
--
ALTER TABLE `levels`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `levels`
--
ALTER TABLE `levels`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=130;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
