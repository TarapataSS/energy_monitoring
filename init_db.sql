
CREATE TABLE event (
    data_time timestamp,
    id_worker INT,
    action INT,
    machine varchar(255));


CREATE TABLE workers (
id_worker INT,
full_name varchar(255)
);