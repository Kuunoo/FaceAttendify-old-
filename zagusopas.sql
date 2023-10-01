-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 09, 2023 at 03:10 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `zagusopas`
--

-- --------------------------------------------------------

--
-- Table structure for table `accs_hist`
--

CREATE TABLE `accs_hist` (
  `accs_id` int(11) NOT NULL,
  `accs_date` date NOT NULL,
  `accs_prsn` varchar(3) NOT NULL,
  `accs_added` datetime NOT NULL DEFAULT current_timestamp(),
  `group_id` int(11) NOT NULL,
  `random_attendance_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `attendance`
--

CREATE TABLE `attendance` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `random_attendance_id` int(11) NOT NULL,
  `present_or_absent` int(11) NOT NULL,
  `mode` varchar(50) NOT NULL,
  `created` timestamp NOT NULL DEFAULT current_timestamp(),
  `modified` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `groups`
--

CREATE TABLE `groups` (
  `id` int(11) NOT NULL,
  `group_name` varchar(50) NOT NULL,
  `creater_id` int(11) NOT NULL,
  `created` timestamp NOT NULL DEFAULT current_timestamp(),
  `modified` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `groups`
--

INSERT INTO `groups` (`id`, `group_name`, `creater_id`, `created`, `modified`) VALUES
(16, 'Test2', 14, '2023-09-08 17:06:37', '2023-09-08 17:06:37'),
(17, 'Test 3', 14, '2023-09-09 12:39:57', '2023-09-09 12:39:57'),
(18, 'Test 4', 14, '2023-09-09 12:54:03', '2023-09-09 12:54:03');

-- --------------------------------------------------------

--
-- Table structure for table `img_dataset`
--

CREATE TABLE `img_dataset` (
  `img_id` int(11) NOT NULL,
  `img_person` varchar(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `img_dataset`
--

INSERT INTO `img_dataset` (`img_id`, `img_person`) VALUES
(1, '16'),
(2, '16'),
(3, '16'),
(4, '16'),
(5, '16'),
(6, '16'),
(7, '16'),
(8, '16'),
(9, '16'),
(10, '16'),
(11, '16'),
(12, '16'),
(13, '16'),
(14, '16'),
(15, '16'),
(16, '16'),
(17, '16'),
(18, '16'),
(19, '16'),
(20, '16'),
(21, '16'),
(22, '16'),
(23, '16'),
(24, '16'),
(25, '16'),
(26, '16'),
(27, '16'),
(28, '16'),
(29, '16'),
(30, '16'),
(31, '16'),
(32, '16'),
(33, '16'),
(34, '16'),
(35, '16'),
(36, '16'),
(37, '16'),
(38, '16'),
(39, '16'),
(40, '16'),
(41, '16'),
(42, '16'),
(43, '16'),
(44, '16'),
(45, '16'),
(46, '16'),
(47, '16'),
(48, '16'),
(49, '16'),
(50, '16'),
(51, '16'),
(52, '16'),
(53, '16'),
(54, '16'),
(55, '16'),
(56, '16'),
(57, '16'),
(58, '16'),
(59, '16'),
(60, '16'),
(61, '16'),
(62, '16'),
(63, '16'),
(64, '16'),
(65, '16'),
(66, '16'),
(67, '16'),
(68, '16'),
(69, '16'),
(70, '16'),
(71, '16'),
(72, '16'),
(73, '16'),
(74, '16'),
(75, '16'),
(76, '16'),
(77, '16'),
(78, '16'),
(79, '16'),
(80, '16'),
(81, '16'),
(82, '16'),
(83, '16'),
(84, '16'),
(85, '16'),
(86, '16'),
(87, '16'),
(88, '16'),
(89, '16'),
(90, '16'),
(91, '16'),
(92, '16'),
(93, '16'),
(94, '16'),
(95, '16'),
(96, '16'),
(97, '16'),
(98, '16'),
(99, '16'),
(100, '16'),
(101, '22'),
(102, '22'),
(103, '22'),
(104, '22'),
(105, '22'),
(106, '22'),
(107, '22'),
(108, '22'),
(109, '22'),
(110, '22'),
(111, '22'),
(112, '22'),
(113, '22'),
(114, '22'),
(115, '22'),
(116, '22'),
(117, '22'),
(118, '22'),
(119, '22'),
(120, '22'),
(121, '22'),
(122, '22'),
(123, '22'),
(124, '22'),
(125, '22'),
(126, '22'),
(127, '22'),
(128, '22'),
(129, '22'),
(130, '22'),
(131, '22'),
(132, '22'),
(133, '22'),
(134, '22'),
(135, '22'),
(136, '22'),
(137, '22'),
(138, '22'),
(139, '22'),
(140, '22'),
(141, '22'),
(142, '22'),
(143, '22'),
(144, '22'),
(145, '22'),
(146, '22'),
(147, '22'),
(148, '22'),
(149, '22'),
(150, '22'),
(151, '22'),
(152, '22'),
(153, '22'),
(154, '22'),
(155, '22'),
(156, '22'),
(157, '22'),
(158, '22'),
(159, '22'),
(160, '22'),
(161, '22'),
(162, '22'),
(163, '22'),
(164, '22'),
(165, '22'),
(166, '22'),
(167, '22'),
(168, '22'),
(169, '22'),
(170, '22'),
(171, '22'),
(172, '22'),
(173, '22'),
(174, '22'),
(175, '22'),
(176, '22'),
(177, '22'),
(178, '22'),
(179, '22'),
(180, '22'),
(181, '22'),
(182, '22'),
(183, '22'),
(184, '22'),
(185, '22'),
(186, '22'),
(187, '22'),
(188, '22'),
(189, '22'),
(190, '22'),
(191, '22'),
(192, '22'),
(193, '22'),
(194, '22'),
(195, '22'),
(196, '22'),
(197, '22'),
(198, '22'),
(199, '22'),
(200, '22'),
(201, '23'),
(202, '23'),
(203, '23'),
(204, '23'),
(205, '23'),
(206, '23'),
(207, '23'),
(208, '23'),
(209, '23'),
(210, '23'),
(211, '23'),
(212, '23'),
(213, '23'),
(214, '23'),
(215, '23'),
(216, '23'),
(217, '23'),
(218, '23'),
(219, '23'),
(220, '23'),
(221, '23'),
(222, '23'),
(223, '23'),
(224, '23'),
(225, '23'),
(226, '23'),
(227, '23'),
(228, '23'),
(229, '23'),
(230, '23'),
(231, '23'),
(232, '23'),
(233, '23'),
(234, '23'),
(235, '23'),
(236, '23'),
(237, '23'),
(238, '23'),
(239, '23'),
(240, '23'),
(241, '23'),
(242, '23'),
(243, '23'),
(244, '23'),
(245, '23'),
(246, '23'),
(247, '23'),
(248, '23'),
(249, '23'),
(250, '23'),
(251, '23'),
(252, '23'),
(253, '23'),
(254, '23'),
(255, '23'),
(256, '23'),
(257, '23'),
(258, '23'),
(259, '23'),
(260, '23'),
(261, '23'),
(262, '23'),
(263, '23'),
(264, '23'),
(265, '23'),
(266, '23'),
(267, '23'),
(268, '23'),
(269, '23'),
(270, '23'),
(271, '23'),
(272, '23'),
(273, '23'),
(274, '23'),
(275, '23'),
(276, '23'),
(277, '23'),
(278, '23'),
(279, '23'),
(280, '23'),
(281, '23'),
(282, '23'),
(283, '23'),
(284, '23'),
(285, '23'),
(286, '23'),
(287, '23'),
(288, '23'),
(289, '23'),
(290, '23'),
(291, '23'),
(292, '23'),
(293, '23'),
(294, '23'),
(295, '23'),
(296, '23'),
(297, '23'),
(298, '23'),
(299, '23'),
(300, '23');

-- --------------------------------------------------------

--
-- Table structure for table `join_groups`
--

CREATE TABLE `join_groups` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `user_approved` int(11) NOT NULL,
  `created` timestamp NOT NULL DEFAULT current_timestamp(),
  `modified` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `join_groups`
--

INSERT INTO `join_groups` (`id`, `group_id`, `user_id`, `user_approved`, `created`, `modified`) VALUES
(41, 16, 16, 0, '2023-09-08 17:06:45', '2023-09-08 17:06:45'),
(42, 17, 22, 0, '2023-09-09 12:40:18', '2023-09-09 12:40:18'),
(43, 18, 23, 0, '2023-09-09 12:54:27', '2023-09-09 12:54:27'),
(44, 18, 24, 0, '2023-09-09 12:54:27', '2023-09-09 12:54:27'),
(45, 18, 25, 0, '2023-09-09 12:54:27', '2023-09-09 12:54:27');

-- --------------------------------------------------------

--
-- Table structure for table `prs_mstr`
--

CREATE TABLE `prs_mstr` (
  `prs_nbr` varchar(3) NOT NULL,
  `prs_name` varchar(50) NOT NULL,
  `prs_skill` varchar(30) NOT NULL,
  `prs_active` varchar(1) NOT NULL DEFAULT 'Y',
  `prs_added` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `prs_mstr`
--

INSERT INTO `prs_mstr` (`prs_nbr`, `prs_name`, `prs_skill`, `prs_active`, `prs_added`) VALUES
('101', 'raja dash', 'SOFTWARE', 'Y', '2023-05-02 21:05:29'),
('102', 'raja dash1', 'HARDWARE', 'Y', '2023-05-02 21:16:55'),
('103', 'fgfgf', 'ELECTRICAL', 'Y', '2023-05-02 21:39:50'),
('104', 'fgfgf', 'ELECTRICAL', 'Y', '2023-05-05 08:35:16'),
('105', 'dds', 'SOFTWARE', 'Y', '2023-05-07 13:45:45'),
('106', 'Zagusopas', 'SOFTWARE', 'Y', '2023-09-08 22:46:58'),
('107', 'Zagusopass', 'SOFTWARE', 'Y', '2023-09-08 22:47:30');

-- --------------------------------------------------------

--
-- Table structure for table `random_attendance`
--

CREATE TABLE `random_attendance` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `random_time` time NOT NULL,
  `duration` int(11) NOT NULL,
  `status` varchar(50) NOT NULL,
  `setdate` date NOT NULL,
  `created` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `random_attendance`
--

INSERT INTO `random_attendance` (`id`, `user_id`, `group_id`, `random_time`, `duration`, `status`, `setdate`, `created`) VALUES
(158, 14, 15, '01:04:00', 2, 'active', '0000-00-00', '2023-09-08 17:03:18'),
(159, 14, 15, '01:06:00', 2, 'active', '0000-00-00', '2023-09-08 17:03:18'),
(160, 14, 15, '01:09:00', 2, 'active', '0000-00-00', '2023-09-08 17:03:18'),
(161, 14, 15, '01:12:00', 2, 'active', '0000-00-00', '2023-09-08 17:03:18'),
(162, 14, 15, '01:14:00', 2, 'active', '0000-00-00', '2023-09-08 17:03:18'),
(163, 14, 16, '01:14:00', 2, 'active', '0000-00-00', '2023-09-08 17:13:34'),
(164, 14, 16, '01:18:00', 2, 'active', '0000-00-00', '2023-09-08 17:13:34'),
(165, 14, 16, '01:23:00', 2, 'active', '0000-00-00', '2023-09-08 17:13:34'),
(166, 14, 16, '01:25:00', 2, 'active', '0000-00-00', '2023-09-08 17:13:35'),
(167, 14, 16, '01:28:00', 2, 'active', '0000-00-00', '2023-09-08 17:28:21'),
(168, 14, 16, '01:29:00', 2, 'active', '0000-00-00', '2023-09-08 17:28:21'),
(169, 14, 16, '01:31:00', 2, 'active', '0000-00-00', '2023-09-08 17:28:21'),
(170, 14, 16, '01:33:00', 2, 'active', '0000-00-00', '2023-09-08 17:28:21'),
(171, 14, 16, '01:35:00', 2, 'active', '0000-00-00', '2023-09-08 17:28:21'),
(172, 14, 16, '01:38:00', 2, 'active', '0000-00-00', '2023-09-08 17:28:21'),
(173, 14, 17, '20:46:00', 2, 'active', '0000-00-00', '2023-09-09 12:43:45'),
(174, 14, 17, '20:49:00', 2, 'active', '0000-00-00', '2023-09-09 12:43:45'),
(175, 14, 17, '20:51:00', 2, 'active', '0000-00-00', '2023-09-09 12:43:45'),
(176, 14, 17, '20:52:00', 2, 'active', '0000-00-00', '2023-09-09 12:43:45'),
(177, 14, 17, '20:57:00', 2, 'active', '0000-00-00', '2023-09-09 12:43:45'),
(178, 14, 17, '20:58:00', 2, 'active', '0000-00-00', '2023-09-09 12:43:45'),
(179, 14, 17, '20:59:00', 2, 'active', '0000-00-00', '2023-09-09 12:43:45'),
(180, 14, 18, '20:56:00', 1, 'active', '0000-00-00', '2023-09-09 12:55:48'),
(181, 14, 18, '20:59:00', 1, 'active', '0000-00-00', '2023-09-09 12:55:48'),
(182, 14, 18, '21:01:00', 1, 'active', '0000-00-00', '2023-09-09 12:55:48'),
(183, 14, 18, '21:03:00', 1, 'active', '0000-00-00', '2023-09-09 12:55:48'),
(184, 14, 18, '21:08:00', 1, 'active', '0000-00-00', '2023-09-09 12:55:48');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(100) NOT NULL,
  `address_line1` varchar(100) NOT NULL,
  `address_line2` varchar(100) NOT NULL,
  `user_role` varchar(50) NOT NULL,
  `user_name` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `created_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `modified_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `dob` date NOT NULL,
  `photo` varchar(100) NOT NULL,
  `approved` int(11) NOT NULL,
  `i_d` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `first_name`, `last_name`, `email`, `phone`, `address_line1`, `address_line2`, `user_role`, `user_name`, `password`, `created_date`, `modified_date`, `dob`, `photo`, `approved`, `i_d`) VALUES
(14, 'JD', 'Manalili', 'jd@gmail.com', '09708187465', '', '', 'admin', '', '1234', '2023-09-08 15:52:50', '2023-09-08 16:25:05', '2001-06-14', 'JD-jd.jpg', 0, ''),
(15, 'Jopay', 'Aguilar', 'jopay@gmail.com', '', '', '', 'admin', '', '1234', '2023-09-08 16:27:22', '2023-09-08 16:27:58', '0000-00-00', 'Jopay-jopay.jpg', 0, ''),
(20, 'Paolo', 'Parazo', 'pao@gmail.com', '', '', '', 'admin', '', '1234', '2023-09-09 12:27:44', '2023-09-09 12:27:44', '0000-00-00', '', 0, ''),
(21, 'Jonel', 'Samson', 'jonel@gmail.com', '', '', '', 'admin', '', '1234', '2023-09-09 12:28:05', '2023-09-09 12:28:05', '0000-00-00', '', 0, ''),
(23, 'One', 'Sample', 'one@gmail.com', '', '', '', '', '', '1234', '2023-09-09 12:52:58', '2023-09-09 12:52:58', '0000-00-00', 'One-jonel.jpg', 0, ''),
(24, 'Two', 'Sample', 'two@gmail.com', '', '', '', '', '', '1234', '2023-09-09 12:53:21', '2023-09-09 12:53:21', '0000-00-00', '', 0, ''),
(25, 'Three', 'Sample', 'three@gmail.com', '', '', '', '', '', '1234', '2023-09-09 12:53:35', '2023-09-09 12:53:35', '0000-00-00', '', 0, '');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accs_hist`
--
ALTER TABLE `accs_hist`
  ADD PRIMARY KEY (`accs_id`),
  ADD KEY `accs_date` (`accs_date`);

--
-- Indexes for table `attendance`
--
ALTER TABLE `attendance`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `groups`
--
ALTER TABLE `groups`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `img_dataset`
--
ALTER TABLE `img_dataset`
  ADD PRIMARY KEY (`img_id`);

--
-- Indexes for table `join_groups`
--
ALTER TABLE `join_groups`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `prs_mstr`
--
ALTER TABLE `prs_mstr`
  ADD PRIMARY KEY (`prs_nbr`);

--
-- Indexes for table `random_attendance`
--
ALTER TABLE `random_attendance`
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
-- AUTO_INCREMENT for table `accs_hist`
--
ALTER TABLE `accs_hist`
  MODIFY `accs_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=108;

--
-- AUTO_INCREMENT for table `attendance`
--
ALTER TABLE `attendance`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `groups`
--
ALTER TABLE `groups`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `join_groups`
--
ALTER TABLE `join_groups`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT for table `random_attendance`
--
ALTER TABLE `random_attendance`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=185;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
