ALTER TABLE `webuser_decadesofvinyl.com-test`.`dov_woo_attribs` 
  DROP PRIMARY KEY, 
  DROP INDEX genre, 
  ADD PRIMARY KEY(`id`), 
  ADD UNIQUE INDEX name_term (attrib_name,attrib_term);
  
CREATE TABLE `dov_settings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `setting` varchar(20) NOT NULL,
  `value` varchar(200) NOT NULL,
  `insert_date` timestamp NULL DEFAULT '0000-00-00 00:00:00',
  `update_date` timestamp NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `dov_settings` ( `setting`, `value`, `insert_date`)
VALUES ('db_version', '1.1', now());
