CREATE DATABASE `ensemble`;

DROP TABLE IF EXISTS `patient_details`;

CREATE TABLE `patient_details` (
`id` int NOT NULL AUTO_INCREMENT, 
`user_name` text NOT NULL,
`user_mail` text,
`user_phone` text NOT NULL,
`symptoms` text NOT NULL,
`prognosis` text,
`created_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
`updated_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = latin1;


DROP TABLE IF EXISTS `pneumonia_action`;

CREATE TABLE `pneumonia_action` (
`id` int NOT NULL AUTO_INCREMENT, 
`user_id` int NOT NULL,
`pneumonia_action` text  NOT NULL,
`result` text  NOT NULL,
`created_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
`updated_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (`id`),
FOREIGN KEY (user_id) REFERENCES patient_details(id)
) ENGINE = InnoDB DEFAULT CHARSET = latin1;