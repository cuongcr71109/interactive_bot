-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 03, 2021 at 07:49 AM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `interact_tool`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `user_id` int(10) DEFAULT NULL,
  `content` varchar(255) DEFAULT NULL,
  `group_id` varchar(255) DEFAULT NULL,
  `delay` int(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `user_id`, `content`, `group_id`, `delay`) VALUES
(1, 1, 'Hello.', '-1001274866902', 1),
(2, 3, 'Nice to see you', '-1001274866902', 1),
(3, 2, 'Hi. How are you?', '-1001274866902', 1),
(4, 1, 'I\'m fine. Thanks. And you?', '-1001274866902', 1),
(5, 2, 'I\'m fine. Thanks', '-1001274866902', 1),
(6, 3, 'Hello.', '-563690107', 2),
(7, 2, 'Nice to see you', '-563690107', 2),
(8, 1, 'Hi. How are you?', '-563690107', 2),
(9, 3, 'I\'m fine. Thanks. And you?', '-563690107', 2),
(10, 2, 'I\'m fine. Thanks', '-563690107', 2);

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `id` int(10) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `fname` varchar(255) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `isAdmin` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`id`, `username`, `password`, `fname`, `phone`, `isAdmin`) VALUES
(1, 'admin', '21232f297a57a5a743894a0e4a801fc3', 'admin', '+84123456789', 1),
(2, 'quannm', 'e10adc3949ba59abbe56e057f20f883e', 'NMQ', '+84123456789', 0),
(3, 'nmq', 'e10adc3949ba59abbe56e057f20f883e', 'NMQ', '+84123456789', 0);

-- --------------------------------------------------------

--
-- Table structure for table `groups`
--

CREATE TABLE `groups` (
  `id` int(10) NOT NULL,
  `customer_username` varchar(255) NOT NULL,
  `group_id` varchar(255) NOT NULL,
  `group_title` varchar(255) NOT NULL,
  `group_type` varchar(15) NOT NULL,
  `group_link` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `groups`
--

INSERT INTO `groups` (`id`, `customer_username`, `group_id`, `group_title`, `group_type`, `group_link`) VALUES
(13, 'quannm', '-1001158850531', 'Test BOT', 'private', 'https://t.me/joinchat/HZesgX2L5zcpKvq0'),
(14, 'quannm', '-1001429987581', 'test', 'private', 'https://t.me/joinchat/VTvg_eT6s7Rz-AIj'),
(15, 'quannm', '-1001170310837', 'TestKDbot', 'private', 'https://t.me/joinchat/RcGGtdG60NynCrJK'),
(16, 'quannm', '-1001159430667', 'Test Tool', 'public', 'https://t.me/testInteractTool'),
(35, 'admin', '-1001158850531', 'Test BOT', 'private', 'https://t.me/joinchat/HZesgX2L5zcpKvq0'),
(36, 'admin', '-1001429987581', 'test', 'private', 'https://t.me/joinchat/VTvg_eT6s7Rz-AIj'),
(37, 'admin', '-1001170310837', 'TestKDbot', 'private', 'https://t.me/joinchat/RcGGtdG60NynCrJK'),
(38, 'admin', '-1001159430667', 'Test Tool', 'public', 'https://t.me/testInteractTool'),
(39, 'admin', '-1001274866902', 'Test Interact', 'private', 'https://t.me/joinchat/H9rYoLjUYKtakiYt'),
(40, 'admin', '-563690107', '+1 Group Test', 'private', 'https://t.me/joinchat/IZk6e7P52S4M0CA6');

-- --------------------------------------------------------

--
-- Table structure for table `nmq`
--

CREATE TABLE `nmq` (
  `id` int(11) NOT NULL,
  `user_id` int(10) DEFAULT NULL,
  `content` varchar(255) DEFAULT NULL,
  `group_id` varchar(255) DEFAULT NULL,
  `delay` int(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `quannm`
--

CREATE TABLE `quannm` (
  `id` int(11) NOT NULL,
  `user_id` int(10) DEFAULT NULL,
  `content` varchar(255) DEFAULT NULL,
  `group_id` varchar(255) DEFAULT NULL,
  `delay` int(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `quannm`
--

INSERT INTO `quannm` (`id`, `user_id`, `content`, `group_id`, `delay`) VALUES
(1, 1, 'Hello.', '-1001158850531', 1),
(2, 3, 'Nice to see you', '-1001158850531', 1),
(3, 2, 'Hi. How are you?', '-1001158850531', 1),
(4, 1, 'I\'m fine. Thanks. And you?', '-1001158850531', 1),
(5, 2, 'I\'m fine. Thanks', '-1001158850531', 1);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(10) NOT NULL,
  `user_id` int(10) NOT NULL,
  `api_id` int(10) NOT NULL,
  `api_hash` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `phone` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `user_id`, `api_id`, `api_hash`, `username`, `phone`) VALUES
(1, 784093829, 2484767, 'df8557fedd7d125f1128eec0fb021f27', 'quannmUET', '84856852624'),
(2, 1442776649, 2358245, '4dc2303f73b28a1c0c8ecc7a25ab8d65', 'quannmMQM', '84394880604'),
(3, 1396995011, 2258165, '82199b4a98663ac87b1299a8587ad50a', 'cuongtv18', '84376091463');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `groups`
--
ALTER TABLE `groups`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `nmq`
--
ALTER TABLE `nmq`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `quannm`
--
ALTER TABLE `quannm`
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
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `groups`
--
ALTER TABLE `groups`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `nmq`
--
ALTER TABLE `nmq`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `quannm`
--
ALTER TABLE `quannm`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
