# Calendar CSV Instructions

## PH_F — Public Holiday Flag

`PH_F` indicates whether a date is a Singapore public holiday.

| Value | Meaning |
|---|---|
| `Y` | Public holiday |
| `N` | Not a public holiday |

### How to get Singapore public holidays

1. Check the official source: **Ministry of Manpower (MOM)**
   - URL: https://www.mom.gov.sg/employment-practices/public-holidays
   - Lists all gazetted public holidays for the current and upcoming year.

2. Alternatively, use the **data.gov.sg** open dataset:
   - URL: https://data.gov.sg/datasets/d_3751791452397f748de72aa5a3a2cb7/view
   - Provides a downloadable CSV of public holidays by year.

### How to update PH_F in the CSV

For any date that falls on a public holiday, change `PH_F` from `N` to `Y`.

**Example** — Good Friday (3 Apr 2026):
```
Before: 2026-04-03,Weekday,N,Y
After:  2026-04-03,Weekday,Y,Y
```

> **Note:** Public holidays that fall on a Sunday are typically substituted with the following Monday (in lieu day) — remember to also mark the in-lieu date as `PH_F = Y`.

### Known Singapore public holidays — Mar & Apr 2026

| Date | Holiday |
|---|---|
| 2026-03-20 | Hari Raya Puasa (Eid al-Fitr) |
| 2026-04-03 | Good Friday |
