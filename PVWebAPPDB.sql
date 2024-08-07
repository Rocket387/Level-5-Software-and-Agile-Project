CREATE TABLE Users (
    User_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(150) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Roles_ID INT NOT NULL,
    FOREIGN KEY (Roles_ID) REFERENCES Roles(Roles_ID)
);

CREATE TABLE Notes (
    Notes_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    note_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    User_ID INTEGER NOT NULL,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID)
);

CREATE TABLE UserNotes (
    User_ID INTEGER NOT NULL,
    Notes_ID INTEGER NOT NULL,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Notes_ID) REFERENCES Notes(Notes_ID),
    PRIMARY KEY (User_ID, Notes_ID)
);


CREATE TABLE Roles (
     Roles_ID INTEGER PRIMARY KEY AUTOINCREMENT,
     role_name VARCHAR(100) UNIQUE NOT NULL
);


INSERT INTO Roles (role_name) VALUES ('Admin');
INSERT INTO Roles (role_name) VALUES ('User');

INSERT INTO Users (username, email, password, Roles_ID)
VALUES('roccharl', 'roccharl@amazon.co.uk', 'password', 1);

SELECT * FROM Users

SELECT * FROM Roles

DROP TABLE Roles
DROP TABLE Notes
DROP TABLE UserNotes
DROP TABLE Users
