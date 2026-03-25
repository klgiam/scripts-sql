* help me generate insert sql for all the records in csv CRWD_DNSTY.DNSTY.DNSTY.sql
* Refer to the csv file referenced
* Refer to CRWD_DNSTY.DNSTY.DNSTY.sql for DDL of the table
* Column data the same except for:
- intervaltime -> use today's date for the date part but retain the time portion. E.g. 2026-03-24 23:55:00.000 -> 2026-03-25 23:55:00.000
- loadg_dtm -> use CURRENT_TIMESTAMP
- generate sql file INSERT_DNSTY_<timestamp>.sql

