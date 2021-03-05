-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Nov 09, 2020 at 07:26 PM
-- Server version: 5.7.31
-- PHP Version: 7.3.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ws`
--

-- --------------------------------------------------------

--
-- Table structure for table `chambre`
--

DROP TABLE IF EXISTS `chambre`;
CREATE TABLE IF NOT EXISTS `chambre` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hotel_id` int(11) NOT NULL,
  `number_of_nights` int(11) NOT NULL,
  `departure_date` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Hotel_ID` (`hotel_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `chambre`
--

INSERT INTO `chambre` (`id`, `hotel_id`, `number_of_nights`, `departure_date`) VALUES
(1, 1, 5, '2020-11-08'),
(2, 2, 6, '2020-11-08'),
(3, 1, 15, '2020-11-09'),
(4, 1, 3, '2020-11-08');

-- --------------------------------------------------------

--
-- Table structure for table `client`
--

DROP TABLE IF EXISTS `client`;
CREATE TABLE IF NOT EXISTS `client` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` text NOT NULL,
  `password` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `client`
--

INSERT INTO `client` (`id`, `username`, `password`) VALUES
(1, 'samir', 'akarioh');

-- --------------------------------------------------------

--
-- Table structure for table `hotel`
--

DROP TABLE IF EXISTS `hotel`;
CREATE TABLE IF NOT EXISTS `hotel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text NOT NULL,
  `adress` text NOT NULL,
  `stars` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `hotel`
--

INSERT INTO `hotel` (`id`, `name`, `adress`, `stars`) VALUES
(1, 'Samir', 'azidjjizadj', 3),
(2, 'Malek', 'azidjjizadj', 5);

-- --------------------------------------------------------

--
-- Table structure for table `reservation`
--

DROP TABLE IF EXISTS `reservation`;
CREATE TABLE IF NOT EXISTS `reservation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hotel_id` int(11) NOT NULL,
  `chambre_id` int(11) NOT NULL,
  `departure_date` date NOT NULL,
  `arrival_date` date NOT NULL,
  `client_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Hotel_ID2` (`hotel_id`),
  KEY `Chambre_ID` (`chambre_id`),
  KEY `Client_ID` (`client_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `chambre`
--
ALTER TABLE `chambre`
  ADD CONSTRAINT `Hotel_ID` FOREIGN KEY (`hotel_id`) REFERENCES `hotel` (`id`);

--
-- Constraints for table `reservation`
--
ALTER TABLE `reservation`
  ADD CONSTRAINT `Chambre_ID` FOREIGN KEY (`chambre_id`) REFERENCES `chambre` (`id`),
  ADD CONSTRAINT `Client_ID` FOREIGN KEY (`client_id`) REFERENCES `client` (`id`),
  ADD CONSTRAINT `Hotel_ID2` FOREIGN KEY (`hotel_id`) REFERENCES `hotel` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
