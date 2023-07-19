
CREATE TABLE event (
    data_time timestamp,
    id_worker INT,
    action INT,
    machine varchar(255));


CREATE TABLE workers (
id_worker INT,
full_name varchar(255)
);


CREATE TABLE public.regs (
	id int4 NOT NULL,
	reg_ip varchar(20) NULL,
	reg_info int4 NULL,
	CONSTRAINT regs_pkey PRIMARY KEY (id)
);