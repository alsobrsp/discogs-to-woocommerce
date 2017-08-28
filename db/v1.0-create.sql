-- phpMyAdmin SQL Dump
-- version 4.2.12deb2+deb8u1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Aug 28, 2017 at 03:31 PM
-- Server version: 5.6.30-1
-- PHP Version: 5.6.20-0+deb8u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `webuser_decadesofvinyl.com-dev`
--

-- --------------------------------------------------------

--
-- Table structure for table `dov_discogs_fields`
--

CREATE TABLE IF NOT EXISTS `dov_discogs_fields` (
`id` int(11) NOT NULL,
  `field_id` int(11) NOT NULL,
  `field_name` varchar(45) COLLATE utf8mb4_unicode_520_ci NOT NULL,
  `insert_date` timestamp NULL DEFAULT NULL,
  `update_date` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;

-- --------------------------------------------------------

--
-- Table structure for table `dov_discogs_instances`
--

CREATE TABLE IF NOT EXISTS `dov_discogs_instances` (
`import_id` int(11) NOT NULL,
  `instance_id` int(11) NOT NULL,
  `woo_id` int(11) DEFAULT NULL,
  `rating` int(11) DEFAULT NULL,
  `title` varchar(45) CHARACTER SET utf8 COLLATE utf8_unicode_520_ci NOT NULL,
  `folder_id` int(11) NOT NULL,
  `discogs_date_added` datetime NOT NULL COMMENT 'The imported instance information',
  `notes` longtext CHARACTER SET utf8 COLLATE utf8_unicode_520_ci,
  `notes_chksum` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_520_ci DEFAULT NULL,
  `release_id` int(11) NOT NULL,
  `insert_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `update_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;

-- --------------------------------------------------------

--
-- Table structure for table `dov_discogs_releases`
--

CREATE TABLE IF NOT EXISTS `dov_discogs_releases` (
`id` int(11) NOT NULL,
  `release_id` int(11) NOT NULL,
  `woo_attrib_id` int(11) DEFAULT NULL,
  `title` varchar(255) CHARACTER SET latin1 DEFAULT NULL,
  `artists` varchar(4096) CHARACTER SET latin1 DEFAULT NULL,
  `labels` varchar(4096) CHARACTER SET latin1 DEFAULT NULL,
  `styles` varchar(512) CHARACTER SET latin1 DEFAULT NULL,
  `genres` varchar(512) CHARACTER SET latin1 DEFAULT NULL,
  `url` varchar(512) CHARACTER SET latin1 DEFAULT NULL,
  `discogs_date_added` timestamp NULL DEFAULT NULL,
  `discogs_date_changed` timestamp NULL DEFAULT NULL,
  `insert_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `update_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;

-- --------------------------------------------------------

--
-- Table structure for table `dov_run_log`
--

CREATE TABLE IF NOT EXISTS `dov_run_log` (
`id` int(11) NOT NULL,
  `process` varchar(30) NOT NULL,
  `run_id` char(36) NOT NULL,
  `start_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `finish_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `complete` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `dov_sales_channels`
--

CREATE TABLE IF NOT EXISTS `dov_sales_channels` (
`id` int(11) NOT NULL,
  `instance_id` int(11) NOT NULL,
  `sales_channels` varchar(256) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `sold` tinyint(1) DEFAULT NULL,
  `insert_date` timestamp NULL DEFAULT NULL,
  `update_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;

-- --------------------------------------------------------

--
-- Table structure for table `dov_woo_attribs`
--

CREATE TABLE IF NOT EXISTS `dov_woo_attribs` (
`id` int(11) NOT NULL,
  `attrib_name` varchar(25) NOT NULL,
  `attrib_term` varchar(50) NOT NULL,
  `woo_attrib_id` int(11) DEFAULT NULL,
  `insert_date` timestamp NULL DEFAULT NULL,
  `update_date` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `dov_woo_attribs_tmp`
--

CREATE TABLE IF NOT EXISTS `dov_woo_attribs_tmp` (
`id` int(11) NOT NULL,
  `attrib_name` varchar(25) NOT NULL,
  `attrib_term` varchar(50) NOT NULL,
  `woo_attrib_id` int(11) DEFAULT NULL,
  `insert_date` timestamp NULL DEFAULT NULL,
  `update_date` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `dov_woo_instances`
--

CREATE TABLE IF NOT EXISTS `dov_woo_instances` (
`import_id` int(11) NOT NULL,
  `instance_id` int(11) NOT NULL,
  `woo_id` int(11) DEFAULT NULL,
  `insert_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `update_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `dov_discogs_fields`
--
ALTER TABLE `dov_discogs_fields`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `dov_discogs_instances`
--
ALTER TABLE `dov_discogs_instances`
 ADD PRIMARY KEY (`import_id`,`instance_id`,`release_id`), ADD UNIQUE KEY `instance_id_UNIQUE` (`instance_id`);

--
-- Indexes for table `dov_discogs_releases`
--
ALTER TABLE `dov_discogs_releases`
 ADD PRIMARY KEY (`id`,`release_id`), ADD UNIQUE KEY `release_id` (`release_id`);

--
-- Indexes for table `dov_run_log`
--
ALTER TABLE `dov_run_log`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `dov_sales_channels`
--
ALTER TABLE `dov_sales_channels`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `instance_id` (`instance_id`);

--
-- Indexes for table `dov_woo_attribs`
--
ALTER TABLE `dov_woo_attribs`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `name_term` (`attrib_name`,`attrib_term`);

--
-- Indexes for table `dov_woo_attribs_tmp`
--
ALTER TABLE `dov_woo_attribs_tmp`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `genre` (`attrib_term`);

--
-- Indexes for table `dov_woo_instances`
--
ALTER TABLE `dov_woo_instances`
 ADD PRIMARY KEY (`import_id`,`instance_id`), ADD UNIQUE KEY `instance_id_UNIQUE` (`instance_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `dov_discogs_fields`
--
ALTER TABLE `dov_discogs_fields`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `dov_discogs_instances`
--
ALTER TABLE `dov_discogs_instances`
MODIFY `import_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `dov_discogs_releases`
--
ALTER TABLE `dov_discogs_releases`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `dov_run_log`
--
ALTER TABLE `dov_run_log`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `dov_sales_channels`
--
ALTER TABLE `dov_sales_channels`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `dov_woo_attribs`
--
ALTER TABLE `dov_woo_attribs`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `dov_woo_attribs_tmp`
--
ALTER TABLE `dov_woo_attribs_tmp`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `dov_woo_instances`
--
ALTER TABLE `dov_woo_instances`
MODIFY `import_id` int(11) NOT NULL AUTO_INCREMENT;
