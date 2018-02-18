from collections import namedtuple
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import pprint
import pickle

days = ['U', 'M', 'T', 'W', 'R', 'F', 'S']
subjs = ['AAEC', 'ACIS', 'AFST', 'AHRM', 'AINS', 'ALCE', 'ALS', 'AOE', 'APS', 'APSC', 'ARBC', 'ARCH', 'ART', 'AS', 'ASPT', 'AT', 'BC', 'BCHM', 'BIOL', 'BIT', 'BMES', 'BMSP', 'BMVS', 'BSE', 'BTDM', 'BUS', 'CEE', 'CEM', 'CHE', 'CHEM', 'CHN', 'CINE', 'CLA', 'CMDA', 'CNST', 'COMM', 'CONS', 'COS', 'CRIM', 'CS', 'CSES', 'DASC', 'ECE', 'ECON', 'EDCI', 'EDCO', 'EDCT', 'EDEL', 'EDEP', 'EDHE', 'EDIT', 'EDP', 'EDRE', 'EDTE', 'ENGE', 'ENGL', 'ENGR', 'ENSC', 'ENT', 'ESM', 'FA', 'FCS', 'FIN', 'FIW', 'FL', 'FMD', 'FR', 'FREC', 'FST', 'GBCB', 'GEOG', 'GEOS', 'GER', 'GIA', 'GR', 'GRAD', 'HD', 'HEB', 'HIST', 'HNFE', 'HORT', 'HTM', 'HUM', 'IDS', 'IS', 'ISC', 'ISE', 'ITAL', 'ITDS', 'JPN', 'JUD', 'LAHS', 'LAR', 'LAT', 'LDRS', 'MACR', 'MATH', 'ME', 'MGT', 'MINE', 'MKTG', 'MN', 'MS', 'MSE', 'MTRG', 'MUS', 'NANO', 'NEUR', 'NR', 'NSEG', 'PAPA', 'PHIL', 'PHS', 'PHYS', 'PM', 'PORT', 'PPWS', 'PSCI', 'PSVP', 'PSYC', 'REAL', 'RED', 'RLCL', 'RTM', 'RUS', 'SBIO', 'SOC', 'SPAN', 'SPIA', 'STAT', 'STL', 'STS', 'SYSB', 'TA', 'TBMH', 'UAP', 'UH', 'UNIV', 'VM', 'WGS']
bldngs = ['AA', 'ADRF', 'AGNEW', 'AIR', 'AIRCN', 'AIRPT', 'AIRSH', 'AJ E', 'AJ W', 'AJPAV', 'AQUAC', 'ARMRY', 'ART C', 'ASAB', 'B270C', 'B270D', 'B270E', 'B270F', 'BAR', 'BEEF', 'BFH', 'BFPC', 'BHAPT', 'BIOMP', 'BOOK', 'BRNCH', 'BRO', 'BROOK', 'BULL', 'BUR', 'BURCH', 'CAM E', 'CAM M', 'CAM', 'CAPRI', 'CARNA', 'CEC', 'CEN', 'CHAP', 'CHEDS', 'CHEMP', 'CHRNE', 'CIC', 'CMMID', 'CO', 'COLAV', 'COL', 'COLS2', 'COLSQ', 'COTA', 'CPAP', 'CRCIA', 'CSB', 'CSSER', 'DAIRY', 'DAV', 'DB', 'DBHCC', 'DEEMR', 'DER', 'DF', 'DOGK', 'DRAPA', 'DTNA', 'DTRIK', 'DURHM', 'EGG E', 'EGG M', 'EGG W', 'ELECS', 'EMPOR', 'ENGEL', 'ENGLF', 'FEM', 'FRALN', 'FSBRN', 'FST', 'GALRY', 'GBJ', 'GBLDG', 'GH A2', 'GH A3', 'GH A4', 'GH A5', 'GH A6', 'GH A7', 'GH F1', 'GH F2', 'GH F3', 'GH F4', 'GH F5', 'GH F6', 'GH F7', 'GH F8', 'GH F9', 'GH', 'GLCDB', 'GOODW', 'GRNDP', 'GROVE', 'GYM', 'HABB1', 'HAHN N', 'HAHN S', 'HAHN', 'HAN', 'HARP', 'HEND', 'HILL', 'HOLD', 'HOLTZ', 'HORSE', 'HOSP', 'HUTCH', 'ICTAS', 'ICTS2', 'ILOT', 'ILSB', 'INCIN', 'INS', 'ISCE', 'JCH', 'JOHN', 'KAMF', 'KENT', 'LANE', 'LARNA', 'LARTS', 'LATH', 'LEE', 'LFSCI', 'LIBR', 'LIBSF', 'LITRV', 'LOMAS', 'LYRIC', 'MAC', 'MAINT', 'MAJWM', 'MCB', 'MCCOM', 'MEDIA', 'MEQSD', 'MILES', 'MIL', 'MMLAB', 'MON', 'MPOOL', 'MRYMN', 'MSPRT', 'NCB', 'NCH', 'NEB', 'NEW', 'NHW', 'NOR', 'NOVAC', 'NRH E', 'NRH W', 'NVC', 'OBSRB', 'OSHA', 'OSP', 'OWENS', 'P HSE', 'PAB', 'PACKA', 'PACK', 'PAM', 'PAT', 'PAYNE', 'PH460', 'PHALL', 'PK', 'POWER', 'PRC', 'PRICE', 'PRINT', 'PRT E', 'PRT W', 'PRT', 'PSCA', 'PSC', 'PWCOM', 'PY', 'RAND', 'RASCH', 'RCTR1', 'RECRE', 'RFH', 'ROB', 'SANDY', 'SARDO', 'SAT', 'SAUND', 'SEB', 'SEC', 'SEITZ', 'SGCTR', 'SHANK', 'SHEEP', 'SHULT', 'SKEL', 'SL TW', 'SLUSH', 'SM CC', 'SMYTH', 'SOL', 'SPC A', 'SPC B', 'SPC C', 'SPC D', 'SPC E', 'SPC F', 'SPC G', 'SPC H', 'SPC I', 'SPC J', 'SPC K', 'SPC L', 'SPC M', 'SPC N', 'SPC O', 'SPC P', 'SPC Q', 'SPC R', 'SPCCS', 'SPCFH', 'SPCRM', 'SPEH', 'SQUIR', 'SSB', 'STAD', 'STCTR', 'STEG N', 'STEG S', 'SUBS2', 'SURGE', 'SWINE', 'SYSDEV', 'T101', 'TBA', 'TC', 'TESKE', 'THARV', 'THOM', 'TORG', 'UAIB', 'UCLUB', 'UPEST', 'VAW', 'VM 1', 'VM 2', 'VM 3', 'VM 4B', 'VM 4D', 'VM 4', 'VM4C1', 'VM4C2', 'VM4C3', 'VMED', 'VMIA', 'VTC', 'VTINN', 'VUAC', 'VVIEW', 'WAL', 'WHIT', 'WLH', 'WMS', 'WRGHT', 'WS A1']

Course = namedtuple('Course', ['crn', 'course', 'name', 'style', 'capacity', 'instructor', 'meetings'])
Meeting = namedtuple('Meeting', ['location', 'days', 'start', 'end'])

def get_courses(term, subj):
    headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
    data = {
        'BTN_PRESSED': '',
        'CAMPUS': '0',
        'CORE_CODE': 'AR%',
        'crn': '',
        'CRSE_NUMBER': '',
        'disp_comments_in': 'Y',
        'inst_name': '',
        'open_only': '',
        'SCHDTYPE': '%',
        'subj_code': subj,
        'TERMYEAR': term
        }

    res = requests.post('https://banweb.banner.vt.edu/ssb/prod/HZSKVTSC.P_ProcRequest',
                        headers=headers, data=data)

    # html.parser is not lenient enough to handle unterminated </tr>
    soup = BeautifulSoup(res.content, 'lxml')

    courses = []

    table = soup.find('table', class_='dataentrytable')
    if table is None:
        return courses

    rows = table.find_all('tr')
    if len(rows) < 1:
        raise Exception('No rows!')

    for row in rows[1:]:
        cells = [c.text.strip() for c in row.find_all('td')]
        # Course listing w/ room
        if len(cells) == 12:
            # Online or unscheduled course
            if cells[7] == '(ARR)' or cells[10] == 'TBA':
                continue
            
            courses.append(Course(
                crn=int(cells[0].replace('&nbsp', '')),
                course=cells[1],
                name=cells[2],
                style=cells[3],
                capacity=int(cells[5]),
                instructor=cells[6],
                meetings=[Meeting(
                    location=cells[10],
                    days=cells[7].split(' '),
                    start=cells[8],
                    end=cells[9]
                    )]
                ))
        # Course listing w/o room
        elif len(cells) == 11:
            pass
        # Additional times for previous course
        elif len(cells) == 10:
            # Online or unscheduled course
            if cells[8] == 'TBA':
                continue
            
            courses[-1].meetings.append(Meeting(
                location=cells[8],
                days=cells[5].split(' '),
                start=cells[6],
                end=cells[7]
                ))
        # Additional times for previous course w/o room
        elif len(cells) == 9:
            pass
        # Course listing w/o room
        # Rare, similar to (ARR) courses
        elif len(cells) == 7:
            pass
        # Comments for previous course
        elif len(cells) == 2:
            pass
        else:
            raise Exception('Unknown table row length ({})'.format(len(cells)), cells)
    
    return courses

def scrape_courses(term):
    courses = []
    for subj in subjs:
        subj_courses = get_courses(term, subj)
        print('{} courses in {}'.format(len(subj_courses), subj))
        courses += subj_courses

    with open('{}.dat'.format(term), 'wb') as f:
        pickle.dump(courses, f)

    print('Scraped {} courses for term {}'.format(len(courses), term))
    return courses

def load_courses(term):
    courses = []
    with open('{}.dat'.format(term), 'rb') as f:
        courses = pickle.load(f)
    return courses

#courses = scrape_courses('201801')
courses = load_courses('201801')

"""
occupancy = {}

for course in courses:
    for meeting in course.meetings:
        loc = meeting.location.split(' ')
        building = ' '.join(loc[:-1])
        room = loc[-1]

        if building not in bldngs:
            raise Exception('Invalid building {} for CRN {}'.format(course.crn, building))

        if building not in occupancy:
            occupancy[building] = {}

        if room not in occupancy[building]:
            occupancy[building][room] = {}

        for day in meeting.days:
            if day not in occupancy[building][room]:
                occupancy[building][room][day] = []

            start = datetime.strptime(meeting.start, '%I:%M%p')
            end = datetime.strptime(meeting.end, '%I:%M%p')

            occupancy[building][room][day].append([course.crn, start, end])
        """

rooms = {}

occupancy = {}

for course in courses:
    for meeting in course.meetings:
        loc = meeting.location.split(' ')
        building = ' '.join(loc[:-1])
        room = loc[-1]

        if building not in bldngs:
            raise Exception('Invalid building {} for CRN {}'.format(course.crn, building))

        if building not in rooms:
            rooms[building] = []

        if room not in rooms[building]:
            rooms[building].append(room)

        if building not in occupancy:
            occupancy[building] = {}

        start = datetime.strptime(meeting.start, '%I:%M%p')
        end = datetime.strptime(meeting.end, '%I:%M%p')
        time_block = (start, end)

        for day in meeting.days:
            if day not in occupancy[building]:
                occupancy[building][day] = {}

            if time_block not in occupancy[building][day]:
                occupancy[building][day][time_block] = []

            occupancy[building][day][time_block].append((course.crn, room))





day = 'W'
a = datetime(1900, 1, 1, 12, 5)
b = datetime(1900, 1, 1, 13, 5)
building = 'DER'

available = list(rooms[building])
unavailable = []
for (start, end), value in occupancy[building][day].items():
    # Our time is outside of this block
    if a >= end or b <= start:
        pass
    else:
        start_delta = (start - b).total_seconds() / 60.0
        end_delta = (end - a).total_seconds() / 60.0
        print(end, a, end_delta)
        
        for crn, room in value:
            if room in available:
                available.remove(room)
                unavailable.append((crn, room))

print('{} avail, {} unavail'.format(len(available), len(unavailable)))
