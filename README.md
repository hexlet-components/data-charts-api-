# API for charts-project

## Commands

```bash
# build project
make build

# run project
make compose
```

## API

```bash
# return all visits from begin to end dates
/visits?begin=BEGIN_DATE&end=END_DATE

# return all registrations from begin to end dates
/registrations?begin=BEGIN_DATE&end=END_DATE
```


## DB

### Credentials

```text
db: chartsdb
user: student
password: student
```

---

### Schema

Postgres DB with tables:

```sql
visits
    visit_id VARCHAR(255),
    source VARCHAR(255),
    user_agent VARCHAR(255),
    datetime TIMESTAMP

registrations
    datetime TIMESTAMP,
    user_id VARCHAR(255),
    email VARCHAR(255),
    source VARCHAR(255),
    registration_type VARCHAR(255)

ads
    datetime TIMESTAMP,
    utm_source VARCHAR(255),
    utm_campaign VARCHAR(255),
    utm_medium VARCHAR(255),
    cost NUMERIC
```

## Data

To generate new data run script from directory */db*

```bash
make generate
```

It will generate a set of the following data:

- *visits.json* - daily visits per platform
- *regs.json* - daily registrations for each platform
- *ad_campaings.json* - advertising campaigns
- *mod_visits.json* - visits **after** ad campaigns have been applied
- *mod_regs.json* - registrations **after** ad campaigns have been applied
- *visits.csv* - total collected visits
- *regs.csv* - total registrations
- *ads.csv* - final advertising campaigns
