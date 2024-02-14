-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 14, 2024 at 09:02 AM
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
-- Database: `16data`
--

-- --------------------------------------------------------

--
-- Table structure for table `booking`
--

CREATE TABLE `booking` (
  `Booking_ID` varchar(10) NOT NULL,
  `No_of_Tickets` int(11) NOT NULL,
  `Total_Cost` int(11) NOT NULL,
  `Card_Number` varchar(19) DEFAULT NULL,
  `Name_on_card` varchar(21) DEFAULT NULL,
  `User_ID` varchar(5) DEFAULT NULL,
  `Show_ID` varchar(10) DEFAULT NULL,
  `Email_ID` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `booking`
--

INSERT INTO `booking` (`Booking_ID`, `No_of_Tickets`, `Total_Cost`, `Card_Number`, `Name_on_card`, `User_ID`, `Show_ID`, `Email_ID`) VALUES
('B001', 2, 20, '1234567890123456789', 'John Doe', 'U001', 'SH001', 'john@example.com'),
('B002', 3, 30, '9876543210987654321', 'Alice Smith', 'U002', 'SH002', 'alice@example.com'),
('B003', 1, 15, NULL, NULL, 'U003', 'SH003', 'bob@example.com');

-- --------------------------------------------------------

--
-- Table structure for table `movie`
--

CREATE TABLE `movie` (
  `Movie_ID` varchar(5) NOT NULL,
  `Name` varchar(30) NOT NULL,
  `Language` varchar(10) DEFAULT NULL,
  `Genre` varchar(20) DEFAULT NULL,
  `Category` varchar(5) DEFAULT NULL,
  `Duration` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `movie`
--

INSERT INTO `movie` (`Movie_ID`, `Name`, `Language`, `Genre`, `Category`, `Duration`) VALUES
('001', 'Pacific Rim Uprising', 'English', 'Fantasy/SciFi', 'U/A', '1.33'),
('002', 'Strangers : Prey at night', 'English', 'Horror', 'U/A', '2.20'),
('003', 'Tomb Raider', 'English', 'Fantasy/Action', 'A', '5.5'),
('004', 'Midnight Sun', 'English', 'Romance', 'R', '1.3'),
('005', 'Peter Rabbit', 'English', 'Fantasy/Adventure', 'U/A', '2'),
('006', 'Black Panther', 'English', 'Fantasy/SciFi', 'U/A', '2'),
('007', 'Maze Runner: The Death Cure', 'English', 'Fantasy/SciFi', 'U/A', '2'),
('008', 'Insidious: The Last Key', 'English', 'Horror', 'U/A', '2'),
('M001', 'Pacific Rim Uprising', 'English', 'Fantasy/SciFi', 'U/A', '2h 11m'),
('M002', 'Strangers : Prey at night', 'English', 'Horror', 'U/A', '1h 25m'),
('M003', 'Tomb Raider', 'English', 'Fantasy/Action', 'A', '2h 3m');

-- --------------------------------------------------------

--
-- Table structure for table `screen`
--

CREATE TABLE `screen` (
  `Screen_ID` varchar(5) NOT NULL,
  `No_of_Seats` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `screen`
--

INSERT INTO `screen` (`Screen_ID`, `No_of_Seats`) VALUES
('S001', 100),
('S002', 120),
('S003', 80);

-- --------------------------------------------------------

--
-- Table structure for table `show`
--

CREATE TABLE `show` (
  `Show_ID` varchar(10) NOT NULL,
  `Show_Time` time NOT NULL,
  `Show_Date` date NOT NULL,
  `Seats_Remaining` int(11) NOT NULL CHECK (`Seats_Remaining` >= 0),
  `Screen_ID` varchar(5) NOT NULL,
  `Movie_ID` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `show`
--

INSERT INTO `show` (`Show_ID`, `Show_Time`, `Show_Date`, `Seats_Remaining`, `Screen_ID`, `Movie_ID`) VALUES
('SH001', '15:00:00', '2024-02-10', 100, 'S001', 'M001'),
('SH002', '18:30:00', '2024-02-10', 120, 'S002', 'M002'),
('SH003', '21:00:00', '2024-02-10', 80, 'S003', 'M003');

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

CREATE TABLE `ticket` (
  `Ticket_ID` varchar(20) NOT NULL,
  `Booking_ID` varchar(10) DEFAULT NULL,
  `Screen_ID` varchar(5) NOT NULL,
  `Price` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`Ticket_ID`, `Booking_ID`, `Screen_ID`, `Price`) VALUES
('T001', 'B001', 'S001', 10),
('T002', 'B001', 'S001', 10),
('T003', 'B002', 'S002', 10),
('T004', 'B002', 'S002', 10),
('T005', 'B002', 'S002', 10),
('T006', 'B003', 'S003', 15);

-- --------------------------------------------------------

--
-- Table structure for table `ticket_type`
--

CREATE TABLE `ticket_type` (
  `Type` varchar(5) NOT NULL,
  `Cost` decimal(5,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ticket_type`
--

INSERT INTO `ticket_type` (`Type`, `Cost`) VALUES
('Premi', 30),
('Regul', 10),
('VIP', 20);

-- --------------------------------------------------------

--
-- Table structure for table `web_user`
--

CREATE TABLE `web_user` (
  `Web_User_ID` varchar(5) NOT NULL,
  `First_Name` varchar(15) DEFAULT NULL,
  `Last_Name` varchar(20) DEFAULT NULL,
  `Email_ID` varchar(30) DEFAULT NULL,
  `Age` int(11) DEFAULT NULL,
  `Phone_Number` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `web_user`
--

INSERT INTO `web_user` (`Web_User_ID`, `First_Name`, `Last_Name`, `Email_ID`, `Age`, `Phone_Number`) VALUES
('U001', 'John', 'Doe', 'john@example.com', 30, '1234567890'),
('U002', 'Alice', 'Smith', 'alice@example.com', 25, '9876543210'),
('U003', 'Bob', 'Johnson', 'bob@example.com', 35, '4567890123');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `booking`
--
ALTER TABLE `booking`
  ADD PRIMARY KEY (`Booking_ID`),
  ADD KEY `User_ID` (`User_ID`),
  ADD KEY `Show_ID` (`Show_ID`);

--
-- Indexes for table `movie`
--
ALTER TABLE `movie`
  ADD PRIMARY KEY (`Movie_ID`);

--
-- Indexes for table `screen`
--
ALTER TABLE `screen`
  ADD PRIMARY KEY (`Screen_ID`);

--
-- Indexes for table `show`
--
ALTER TABLE `show`
  ADD PRIMARY KEY (`Show_ID`),
  ADD KEY `Screen_ID` (`Screen_ID`),
  ADD KEY `Movie_ID` (`Movie_ID`);

--
-- Indexes for table `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`Ticket_ID`),
  ADD KEY `Booking_ID` (`Booking_ID`);

--
-- Indexes for table `ticket_type`
--
ALTER TABLE `ticket_type`
  ADD PRIMARY KEY (`Type`);

--
-- Indexes for table `web_user`
--
ALTER TABLE `web_user`
  ADD PRIMARY KEY (`Web_User_ID`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `booking`
--
ALTER TABLE `booking`
  ADD CONSTRAINT `booking_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `web_user` (`Web_User_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `booking_ibfk_2` FOREIGN KEY (`Show_ID`) REFERENCES `show` (`Show_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `show`
--
ALTER TABLE `show`
  ADD CONSTRAINT `show_ibfk_1` FOREIGN KEY (`Screen_ID`) REFERENCES `screen` (`Screen_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `show_ibfk_2` FOREIGN KEY (`Movie_ID`) REFERENCES `movie` (`Movie_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `ticket`
--
ALTER TABLE `ticket`
  ADD CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`Booking_ID`) REFERENCES `booking` (`Booking_ID`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
