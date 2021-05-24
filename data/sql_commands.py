SELECT_TABLE_NAMES = """
SELECT name FROM sqlite_master WHERE type='table';
"""

CREATE_USER_TABLE = """
CREATE TABLE users (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name            VARCHAR(100) NOT NULL,
        birth_date      DATE NOT NULL,
        cpf             VARCHAR(11) NOT NULL UNIQUE,
        cep             VARCHAR(8) NOT NULL,
        type_location   VARCHAR(100) NOT NULL,
        street_location VARCHAR(100) NOT NULL,
        number          VARCHAR(10) NOT NULL,
        complement      VARCHAR(100),
        district        VARCHAR(100) NOT NULL,
        city            VARCHAR(100) NOT NULL,
        state VARCHAR(2) NOT NULL,
        email           VARCHAR(100) NOT NULL UNIQUE
        );
"""

INSERT_USER = """
INSERT 
    INTO users 
        (name, birth_date, cpf, cep, type_location, 
        street_location, number, complement, district, 
        city, state, email)
    VALUES
        ('%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'); 
"""