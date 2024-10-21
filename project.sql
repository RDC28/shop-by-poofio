-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 21, 2024 at 08:11 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `project`
--

-- --------------------------------------------------------

--
-- Table structure for table `contacts`
--

CREATE TABLE `contacts` (
  `sno` int(11) NOT NULL,
  `name` text NOT NULL,
  `email` text NOT NULL,
  `phone_no` int(11) NOT NULL,
  `message` text NOT NULL,
  `date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contacts`
--

INSERT INTO `contacts` (`sno`, `name`, `email`, `phone_no`, `message`, `date`) VALUES
(0, 'baba', 'rohitrdccoc@gmail.com', 2147483647, 'test', '2024-10-19 18:54:42');

-- --------------------------------------------------------

--
-- Table structure for table `shop_items`
--

CREATE TABLE `shop_items` (
  `sno` int(11) NOT NULL,
  `slug` text NOT NULL,
  `name` text NOT NULL,
  `price` double NOT NULL,
  `saleprice` double NOT NULL,
  `info` text NOT NULL,
  `manufacturer` text NOT NULL,
  `date` datetime NOT NULL,
  `imgfile` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `shop_items`
--

INSERT INTO `shop_items` (`sno`, `slug`, `name`, `price`, `saleprice`, `info`, `manufacturer`, `date`, `imgfile`) VALUES
(3, 'tuna', 'tuna', 9.99, 6.99, 'tuna tuna', 'tuna', '2024-10-19 19:18:28', 'tuna.gif'),
(4, 'mei', 'mei', 7.99, 4.99, 'mei', 'mei', '2024-10-19 19:28:57', 'mei.gif'),
(5, 'cirno', 'cirno', 99999.99, 9.99, 'cirno', 'cirno', '2024-10-19 19:29:28', 'cirno-fumo.gif'),
(6, 'seele', 'seele', 88.88, 8.88, 'seele', 'seele', '2024-10-19 19:29:57', 'seele.jpeg');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `contacts`
--
ALTER TABLE `contacts`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `shop_items`
--
ALTER TABLE `shop_items`
  ADD PRIMARY KEY (`sno`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `shop_items`
--
ALTER TABLE `shop_items`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
