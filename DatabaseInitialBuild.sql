/* Initial creation of Weather Manager database */
/* Creates the database and table structure */
/* Requires root access to the database */

/* WARNING!! IF YOU ALREADY HAVE A DATABASE IN PLACE THIS WILL */
/* COMPLETELY DELETE IT - Backup your data first */

/* Create the database */
DROP DATABASE IF EXISTS weathermanager;
CREATE DATABASE weathermanager;

USE weathermanager;

/* Add tables */
CREATE TABLE Observations(
	ObservationId INT AUTO_INCREMENT PRIMARY KEY,
	ObservationTime DATETIME NOT NULL,
	SolarRadiationHigh DECIMAL(5,1) UNSIGNED NOT NULL,
	UvHigh DECIMAL(4,1) UNSIGNED NOT NULL,
	WindDirectionMean DECIMAL(3) UNSIGNED NOT NULL,
	HumidityHigh TINYINT UNSIGNED NOT NULL,
	HumidityLow TINYINT UNSIGNED NOT NULL,
	HumidityMean DECIMAL(4,1) UNSIGNED NOT NULL,
	TemperatureHigh DECIMAL(3,1) NOT NULL,
	TemperatureLow DECIMAL(3,1) NOT NULL,
	TemperatureMean DECIMAL(3,1) NOT NULL,
	WindSpeedHigh DECIMAL(4,1) NOT NULL,
	WindSpeedLow DECIMAL(4,1) NOT NULL,
	WindSpeedMean DECIMAL(4,1) NOT NULL,
	WindGustHigh DECIMAL(4,1) NOT NULL,
	WindGustLow DECIMAL(4,1) NOT NULL,
	WindGustMean DECIMAL(4,1) NOT NULL,
	DewPointHigh DECIMAL(3,1) NOT NULL,
	DewPointLow DECIMAL(3,1) NOT NULL,
	DewPointMean DECIMAL(3,1) NOT NULL,
	WindChillHigh DECIMAL(3,1) NOT NULL,
	WindChillLow DECIMAL(3,1) NOT NULL,
	WindChillMean DECIMAL(3,1) NOT NULL,
	HeatIndexHigh DECIMAL(3,1) UNSIGNED NOT NULL,
	HeatIndexLow DECIMAL(3,1) UNSIGNED NOT NULL,
	HeatIndexMean DECIMAL(3,1) UNSIGNED NOT NULL,
	PressureHigh DECIMAL(6,2) UNSIGNED NOT NULL,
	PressureLow DECIMAL(6,2) UNSIGNED NOT NULL,
	PressureTrend DECIMAL(4,2) NOT NULL,observations
	PrecipitationRate DECIMAL(5,2) UNSIGNED NOT NULL,
	PrecipitationTotal DECIMAL(5,2) UNSIGNED NOT NULL
)

CREATE TABLE `extremes` (
	`extremeId` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	`Name` VARCHAR(50) NOT NULL COMMENT 'Description of extreme',
	`Date` DATETIME NOT NULL COMMENT 'Date on which the extreme occured',
	`Rank` TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '1 = 1st etc',
	`HighInt` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'Highest integer of the extreme',
	`LowInt` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'Lowest integer of the extreme',
	`HighFloat` FLOAT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'Highest float of the extreme',
	`LowFloat` FLOAT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'Lowest float of the extreme',
	PRIMARY KEY (`extremeId`) USING BTREE,
	UNIQUE INDEX `Name` (`Name`)
)