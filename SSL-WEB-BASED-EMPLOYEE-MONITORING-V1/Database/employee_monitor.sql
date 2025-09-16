-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 16, 2025 at 12:50 PM
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
-- Database: `employee_monitor`
--

-- --------------------------------------------------------

--
-- Table structure for table `screenshots`
--

CREATE TABLE `screenshots` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `file_path` varchar(255) NOT NULL,
  `filename` varchar(200) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `screenshots`
--

INSERT INTO `screenshots` (`id`, `user_id`, `file_path`, `filename`, `created_at`) VALUES
(1, 1, 'uploads/user_1/screenshot_1758007788_09e274c4.png', 'screenshot_1758007788_09e274c4.png', '2025-09-16 07:29:48'),
(2, 1, 'uploads/user_1/screenshot_1758008089_3faf08b8.png', 'screenshot_1758008089_3faf08b8.png', '2025-09-16 07:34:49'),
(3, 1, 'uploads/user_1/screenshot_1758011397_c08cbc9a.png', 'screenshot_1758011397_c08cbc9a.png', '2025-09-16 08:29:57'),
(4, 1, 'uploads/user_1/screenshot_1758011962_f02026cd.png', 'screenshot_1758011962_f02026cd.png', '2025-09-16 08:39:22'),
(5, 1, 'uploads/user_1/screenshot_1758011991_448e4e61.png', 'screenshot_1758011991_448e4e61.png', '2025-09-16 08:39:51'),
(6, 1, 'uploads/user_1/screenshot_1758012292_0ac12814.png', 'screenshot_1758012292_0ac12814.png', '2025-09-16 08:44:52'),
(7, 1, 'uploads/user_1/screenshot_1758012592_f31cc1f5.png', 'screenshot_1758012592_f31cc1f5.png', '2025-09-16 08:49:52'),
(8, 1, 'uploads/user_1/screenshot_1758012892_af0a8f3d.png', 'screenshot_1758012892_af0a8f3d.png', '2025-09-16 08:54:52'),
(9, 1, 'uploads/user_1/screenshot_1758013192_c7c41bbe.png', 'screenshot_1758013192_c7c41bbe.png', '2025-09-16 08:59:52'),
(10, 1, 'uploads/user_1/screenshot_1758015930_38f9d808.png', 'screenshot_1758015930_38f9d808.png', '2025-09-16 09:45:30'),
(11, 1, 'uploads/user_1/screenshot_1758016226_6d47bc63.png', 'screenshot_1758016226_6d47bc63.png', '2025-09-16 09:50:26'),
(12, 1, 'uploads/user_1/screenshot_1758016526_2b46ed47.png', 'screenshot_1758016526_2b46ed47.png', '2025-09-16 09:55:26'),
(13, 1, 'uploads/user_1/screenshot_1758016827_b67daed9.png', 'screenshot_1758016827_b67daed9.png', '2025-09-16 10:00:27'),
(14, 1, 'uploads/user_1/screenshot_1758017127_09da737d.png', 'screenshot_1758017127_09da737d.png', '2025-09-16 10:05:27'),
(15, 1, 'uploads/user_1/screenshot_1758017427_20315afe.png', 'screenshot_1758017427_20315afe.png', '2025-09-16 10:10:27'),
(16, 1, 'uploads/user_1/screenshot_1758017727_b8f19e2a.png', 'screenshot_1758017727_b8f19e2a.png', '2025-09-16 10:15:27'),
(17, 1, 'uploads/user_1/screenshot_1758018027_c4fb8565.png', 'screenshot_1758018027_c4fb8565.png', '2025-09-16 10:20:27'),
(18, 1, 'uploads/user_1/screenshot_1758018726_f910de66.png', 'screenshot_1758018726_f910de66.png', '2025-09-16 10:32:06'),
(19, 1, 'uploads/user_1/screenshot_1758019027_aa9f3e3d.png', 'screenshot_1758019027_aa9f3e3d.png', '2025-09-16 10:37:07'),
(20, 1, 'uploads/user_1/screenshot_1758019467_f87d3f7d.png', 'screenshot_1758019467_f87d3f7d.png', '2025-09-16 10:44:27');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `screenshots`
--
ALTER TABLE `screenshots`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `screenshots`
--
ALTER TABLE `screenshots`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
