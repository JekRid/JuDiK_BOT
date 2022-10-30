
CREATE TABLE worker(
    id_worker integer NOT NULL,
	id_tg VARCHAR(50),
    fam_worker VARCHAR(50),
	name_worker VARCHAR(50),
	otch_worker VARCHAR(50),
	login VARCHAR(50),
	password VARCHAR(50),
	PRIMARY KEY("id_worker"));
	

CREATE TABLE event (
 id_event integer NOT NULL,
 event_name VARCHAR(120),
 date_event date,
 time_event time,  
 duration_event integer NOT NULL,
 place_event VARCHAR(40),
 PRIMARY KEY("id_event")); 


create table schedule (
id_event integer NOT NULL,
id_worker integer NOT NULL,
FOREIGN KEY("id_event") REFERENCES event("id_event"),
FOREIGN KEY("id_worker") REFERENCES worker("id_worker"));


