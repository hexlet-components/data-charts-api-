import os
from dotenv import load_dotenv
from datetime import datetime
from data_generator.prepare_data import (
    duplicate_visit,
    make_ad_campaign,
    make_regs,
    make_user_reg,
    make_user_visit,
    make_visits,
    modify_visits_and_regs,
    SOURCES
)
from data_generator.utils import gen_week_periods, get_path
import csv
import json

load_dotenv()

BEGIN_DATE = datetime.fromisoformat('2023-03-01')
END_DATE = datetime.fromisoformat('2023-09-01')
DATABASE_URL = os.getenv('DATABASE_URL')


def generate_data():
    visits = make_visits(BEGIN_DATE, END_DATE)
    regs = make_regs(visits)
    ad_weeks = gen_week_periods(BEGIN_DATE, END_DATE, 2, 6)
    m_visits, m_regs = modify_visits_and_regs(visits, regs, ad_weeks)

    with open(get_path('data') / 'visits.json', 'w') as v, open(get_path('data') / 'regs.json', 'w') as r:
        n_visits = {','.join(str(_) for _ in k):v for k, v in visits.items()}
        v.write(json.dumps(n_visits))
        n_regs = {','.join(str(_) for _ in k):v for k, v in regs.items()}
        r.write(json.dumps(n_regs))

    with open(get_path('data') / 'mod_visits.json', 'w') as v:
        with open(get_path('data') / 'mod_regs.json', 'w') as r:
            v.write(json.dumps({','.join(str(_) for _ in k):v for k, v in m_visits.items()}))
            r.write(json.dumps({','.join(str(_) for _ in k):v for k, v in m_regs.items()}))

    with open(get_path('data') / 'ad_campaigns.json', 'w') as a:
        campaigns = []
        for begin, end in ad_weeks:
            c = make_ad_campaign(begin, end)
            campaigns.extend(c)
        a.write(json.dumps(campaigns))

    with open(get_path('data') / 'visits.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for date, v_per_day in m_visits.items():
            for _ in range(v_per_day[SOURCES.WEB]):
                visit = make_user_visit(date, SOURCES.WEB)
                duplicates = list(duplicate_visit(visit, (0, 3), begin=BEGIN_DATE, end=END_DATE))
                writer.writerow(visit)
                writer.writerows(duplicates)
            for _ in range(v_per_day[SOURCES.ANDROID]):
                visit = make_user_visit(date, SOURCES.ANDROID)
                writer.writerow(visit)
            for _ in range(v_per_day[SOURCES.IOS]):
                visit = make_user_visit(date, SOURCES.IOS)
                writer.writerow(visit)
            for _ in range(v_per_day[SOURCES.BOT]):
                visit = make_user_visit(date, SOURCES.BOT)
                writer.writerow(visit)

    with open(get_path('data') / 'regs.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for date, r_per_day in m_regs.items():
            for _ in range(r_per_day[SOURCES.WEB]):
                reg = make_user_reg(date, SOURCES.WEB)
                writer.writerow(reg)
            for _ in range(r_per_day[SOURCES.ANDROID]):
                reg = make_user_reg(date, SOURCES.ANDROID)
                writer.writerow(reg)
            for _ in range(r_per_day[SOURCES.IOS]):
                reg = make_user_reg(date, SOURCES.IOS)
                writer.writerow(reg)

    with open(get_path('data') / 'ads.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(c.values() for c in campaigns)


if __name__ == '__main__':
    generate_data()
