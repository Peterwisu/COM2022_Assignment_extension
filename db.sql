CREATE DATABASE udp;

use udp;
CREATE TABLE users(
    id int NOT NULL AUTO_INCREMENT,
    username varchar(255) NOT NULL,
    pass_word varchar(255) NOT NULL,
    PRIMARY KEY (id)
);

INSERT INTO users(username,pass_word) 
VALUES ("peter","1234"),("wish","1234"),("mouaz","1234"),("fay","1234");
