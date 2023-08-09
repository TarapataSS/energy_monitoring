
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

CREATE TABLE public.sensor_data (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE),
	reading_time timestamptz NULL,
	voltage_a numeric(7, 3) NULL,
	current_a numeric(7, 3) NULL,
	active_power_a numeric(8, 4) NULL,
	reactive_power_a numeric(8, 4) NULL,
	full_power_a numeric(8, 4) NULL,
	power_factor_a numeric(4, 3) NULL,
	voltage_b numeric(7, 3) NULL,
	current_b numeric(7, 3) NULL,
	active_power_b numeric(8, 4) NULL,
	reactive_power_b numeric(8, 4) NULL,
	full_power_b numeric(8, 4) NULL,
	power_factor_b numeric(4, 3) NULL,
	voltage_c numeric(7, 3) NULL,
	current_c numeric(7, 3) NULL,
	active_power_c numeric(8, 4) NULL,
	reactive_power_c numeric(8, 4) NULL,
	full_power_c numeric(8, 4) NULL,
	power_factor_c numeric(4, 3) NULL,
	interfacial_angle_a_b numeric(6, 3) NULL,
	interfacial_angle_b_c numeric(6, 3) NULL,
	interfacial_angle_c_a numeric(6, 3) NULL,
	interfacial_voltage_a_b numeric(6, 3) NULL,
	interfacial_voltage_b_c numeric(6, 3) NULL,
	interfacial_voltage_c_a numeric(6, 3) NULL,
	CONSTRAINT sensor_data_pkey PRIMARY KEY (id)
);