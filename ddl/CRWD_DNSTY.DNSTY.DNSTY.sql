CREATE TABLE CRWD_DNSTY.DNSTY.DNSTY (
	intervaltime datetime NULL,
	intervaltime_epoch numeric(18,0) NULL,
	building_code varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	building_type varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	floor varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	total_users numeric(18,0) NULL,
	density numeric(18,0) NULL,
	loadg_dtm smalldatetime NULL
);