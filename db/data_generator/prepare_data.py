import json
from faker import Faker
from random import randint, choice, gauss, uniform
from collections import namedtuple
from datetime import datetime
from dateutil.relativedelta import relativedelta
from types import SimpleNamespace
from copy import deepcopy

from data_generator.utils import get_month_day, random_week_in_month, get_path

fake = Faker()
Faker.seed(1234)

# VISITS
# web: 800-2000 per day
# mobile: 100-400 per day
# bots: 30% of total visits (once week per month)

V_WEB = (270, 700)
V_MOBILE = (33, 130)
V_BOTS = (90, 240)

APPLE_SHARE = (20, 40)
ANDROID_SHARE = (100 - APPLE_SHARE[1], 100 - APPLE_SHARE[0])

SOURCES = SimpleNamespace(WEB='web', IOS='ios', ANDROID='android', BOT='bot')


def generate_daily_visit_counts(platform):
    if platform == SOURCES.WEB:
        return randint(*V_WEB)
    # 70% android market share
    if platform == SOURCES.ANDROID:
        return int(randint(*V_MOBILE) * uniform(*ANDROID_SHARE)/100)
    # 30% apple market share
    if platform == SOURCES.IOS:
        return int(randint(*V_MOBILE) * uniform(*APPLE_SHARE)/100)
    if platform == SOURCES.BOT:
        return randint(*V_BOTS)


# generates dict with daily visits count for each platform
def make_visits(begin_date, end_date):
    visits = {}
    bot_days = [
        get_month_day(w_st, w_end)
        for w_st, w_end
        in random_week_in_month(begin_date, end_date)
    ]

    for date in get_month_day(begin_date, end_date):
        bot_visits = generate_daily_visit_counts(platform=SOURCES.BOT) if date in bot_days else 0
        visits[date] = {
            SOURCES.WEB: generate_daily_visit_counts(platform=SOURCES.WEB),
            SOURCES.ANDROID: generate_daily_visit_counts(platform=SOURCES.ANDROID),
            SOURCES.IOS: generate_daily_visit_counts(platform=SOURCES.IOS),
            SOURCES.BOT: bot_visits
        }
    return visits

# REGS
# web: 3-10% of VISITS
# mobile: 80-90% of VISITS

R_WEB = (3, 10)
R_MOBILE = (80, 90)
R_TOTAL = (4, 8)
AGENTS = json.loads(open(get_path('fixtures') / 'agents.json').read())


def get_source(platform):
    return SOURCES.__getattribute__(platform.upper())


def get_agents(platform):
    plat = AGENTS.get(platform, (p for tp in AGENTS.values() for p in tp))
    agents = [a for a in plat]
    return agents


def get_type(platform):
    if platform == SOURCES.WEB:
        return choice(['email', 'google', 'apple', 'yandex'])
    if platform == 'android':
        return choice(['email', 'google'])
    if platform == SOURCES.IOS:
        return choice(['email', 'apple'])


# generates dict with daily registrations count for each platform
def make_regs(visits):
    registrations = {}
    for date, v_per_day in visits.items():
        con_web = uniform(*R_WEB)
        con_android = uniform(*R_MOBILE)
        con_ios = uniform(*R_MOBILE)
        registrations[date] = {
            SOURCES.WEB: int(v_per_day[SOURCES.WEB] * con_web / 100),
            SOURCES.ANDROID: int(v_per_day[SOURCES.ANDROID] * con_android / 100),
            SOURCES.IOS: int(v_per_day[SOURCES.IOS] * con_ios / 100)
        }
    return registrations


def make_user_visit(date, platform):
    Row = namedtuple('Row', 'visit_id, source, user_agent, date')
    agents = get_agents(platform)
    hour = randint(0, 23)
    minute = randint(0, 59)
    second = randint(0, 59)
    month, day = date
    user_agent = choice(agents)
    source = get_source(platform)
    return Row(
        fake.uuid4(),
        source,
        user_agent,
        datetime(2023, month, day, hour, minute, second).isoformat()
    )


def make_user_reg(date, platform):
    Row = namedtuple('Row', 'registration, user_id, email, source, registration_type')
    hour = randint(0, 23)
    minute = randint(0, 59)
    second = randint(0, 59)
    month, day = date
    source = get_source(platform)
    registration_type = get_type(platform)
    return Row(
        datetime(2023, month, day, hour, minute, second).isoformat(),
        fake.iana_id(),
        fake.email(),
        source,
        registration_type
    )


def duplicate_visit(visit, count, begin, end):
    a, b = count
    mean = (a + b) / 2
    sigma = (b - a) / 6
    # assume that duplicates distributes by normal distribution
    duples = [visit] * int(gauss(mean, sigma))
    for d in duples:
        visit_id, source, user_agent, date = d
        days = randint(-4, 4)
        hour = randint(0, 23)
        minute = randint(0, 59)
        second = randint(0, 59)
        new_date = datetime.fromisoformat(date) + relativedelta(days=days, hours=hour, minutes=minute, seconds=second)
        if new_date < begin:
            new_date += relativedelta(days=+5)
        if new_date > end:
            new_date += relativedelta(days=-5)
        Row = namedtuple('Row', 'visit_id, source, user_agent, date')
        yield Row(visit_id, source, user_agent, new_date.isoformat())


AD_MOD = (1, 3)

# change visits and registrations for each day in ad days
def modify_visits_and_regs(visits, regs, periods):
    cp_visits = deepcopy(visits)
    cp_regs = deepcopy(regs)
    for begin, end in periods:
        # time lag in visits and regs changes
        new_begin = begin + relativedelta(days=randint(0, 3))
        for ad_day in get_month_day(new_begin, end):
            # if day exists in visits, so day exists in regs too
            if cp_visits.get(ad_day):
                # multiply visit by ad modificator for each day
                vis_mod = uniform(*AD_MOD)
                # multiply regs by number less or equal than visits
                reg_mod = uniform(1, vis_mod)
                for platform in cp_visits[ad_day]:
                    # change visits for all platforms except bots
                    if platform != 'bot':
                        new_visits = int(cp_visits[ad_day][platform] * vis_mod)
                        cp_visits[ad_day][platform] = new_visits
                for platform in cp_regs[ad_day]:
                    new_regs = int(cp_regs[ad_day][platform] * reg_mod)
                    cp_regs[ad_day][platform] = new_regs

    return cp_visits, cp_regs


UTM_SOURCES = ['yandex', 'vk', 'google', 'youtube', 'tg']
UTM_CAMPAIGNS = json.loads(open(get_path('fixtures') / 'utm_campaigns.json').read())
AD_COST = [100, 300]


def get_medium(source):
    if source in ('tg', 'vk'):
        return 'social'
    if source in ('youtube', 'yandex', 'google'):
        return 'cpc'


def make_ad_campaign(start_date, end_date):
    utm_campaign = choice(UTM_CAMPAIGNS)
    utm_source = choice(UTM_SOURCES)
    result = []
    for date in get_month_day(start_date, end_date):
        hour = randint(0, 23)
        minute = randint(0, 59)
        second = randint(0, 59)
        month, day = date
        utm_medium = get_medium(utm_source)
        cost = randint(*AD_COST)

        result.append({
            'date': datetime(2023, month, day, hour, minute, second).isoformat(),
            'utm_source': utm_source,
            'utm_medium': utm_medium,
            'utm_campaign': utm_campaign,
            'cost': cost
        })
    return result
