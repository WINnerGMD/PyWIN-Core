-- phpMyAdmin SQL Dump
-- version 5.1.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jul 10, 2023 at 04:20 PM
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
  `desc` tinytext,
  `version` tinyint(4) NOT NULL,
  `authorID` int(11) NOT NULL,
  `gameVersion` tinyint(2) NOT NULL,
  `likes` int(11) DEFAULT '0',
  `downloads` int(11) DEFAULT '0',
  `audioTrack` tinyint(2) NOT NULL DEFAULT '0',
  `levelLength` tinyint(1) NOT NULL,
  `stars` tinyint(2) DEFAULT '0',
  `difficulty` tinyint(1) DEFAULT '0',
  `starAuto` tinyint(1) DEFAULT '0',
  `starDemon` tinyint(1) DEFAULT '0',
  `starDemonDiff` tinyint(1) DEFAULT '0',
  `rate` tinyint(1) DEFAULT '0',
  `starCoins` tinyint(1) DEFAULT '0',
  `coins` tinyint(1) DEFAULT '0',
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

-- --------------------------------------------------------

--
-- Table structure for table `songs`
--

CREATE TABLE `songs` (
  `id` int(11) NOT NULL,
  `songid` int(11) NOT NULL,
  `link` text NOT NULL,
  `name` varchar(255) NOT NULL,
  `author` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `songs`
--

INSERT INTO `songs` (`id`, `songid`, `link`, `name`, `author`) VALUES
(2, 2232, 'https://audio.ngfiles.com/2000/2232_newgrounds_guitar.mp3?f1121439350', 'NICE GUITAR PIECE', 'beatspitta');

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
-- Indexes for dumped tables
--

--
-- Indexes for table `levels`
--
ALTER TABLE `levels`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `songs`
--
ALTER TABLE `songs`
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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=141;

--
-- AUTO_INCREMENT for table `songs`
--
ALTER TABLE `songs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
