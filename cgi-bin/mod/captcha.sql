-- phpMyAdmin SQL Dump
-- version 2.11.2.2
-- http://www.phpmyadmin.net
--
-- Хост: localhost
-- Время создания: Май 23 2008 г., 12:20
-- Версия сервера: 5.0.45
-- Версия PHP: 5.2.5

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

--
-- База данных: `bazan_bazan`
--

-- --------------------------------------------------------

--
-- Структура таблицы `captcha_img`
--

CREATE TABLE `captcha_img` (
  `id` bigint(20) NOT NULL auto_increment,
  `file_name` char(32) collate cp1251_bin NOT NULL,
  `kod` char(4) collate cp1251_bin NOT NULL,
  `ip` char(15) collate cp1251_bin NOT NULL,
  `time_reg` bigint(20) NOT NULL default '0',
  PRIMARY KEY  (`id`),
  KEY `file_name_to_ip` (`file_name`,`ip`)
) ENGINE=MyISAM  DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin COMMENT='для картинок captcha';
