/* Add user permissions to the Weather Manager database. */
/* Run the DatabaseInitialBuild script first. */

/* YOU NEED TO AMEND THIS SCRIPT TO ADD YOUR OWN USER NAME AND HOST NAME */

GRANT SELECT, INSERT, UPDATE, DELETE ON weathermanager.* TO 'yourname'@'localhost';