CREATE TABLE workers(
    id_workers integer NOT NULL,
    fio VARCHAR(50),
	login VARCHAR(50),
	password VARCHAR(50),
	PRIMARY KEY("id_workers"));



CREATE TABLE schedule (
 id_schedule integer NOT NULL,
 id_workers integer NOT NULL,
 events VARCHAR(120),
 date_event date,
 time_event time, 
 place_event VARCHAR(40),
 PRIMARY KEY(id_schedule),
 FOREIGN KEY(id_workers) REFERENCES workers);


