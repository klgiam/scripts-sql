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

### School Holidays
For dates within the range below, they are non term time days, so TERM_F = N
Vacation: 12 weeks  Sun, 10 May 2026 ~ Sun, 2 Aug 2026 
Vacation: 5 weeks  Sun, 7 Dec 2025 ~ Sun, 11 Jan 2026 