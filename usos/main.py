import os
from dotenv import load_dotenv
from usos_mysql.usos_mysql_connector import USOSMySQLConnector
from usos_api_calls import *
from objects.user import User
from usos_mysql.update_tables import update_usos_courses, update_usos_programs

if __name__ == '__main__':
    load_dotenv()

    User.get_usos_api_key()
    usos_mysql_connector = USOSMySQLConnector()
    users = usos_mysql_connector.get_usos_users()

    test_user = User(os.getenv('TEST_USER_TOKEN'), os.getenv('TEST_USER_SECRET'), 'pl')

    courses = set()
    programs = set()
    for u in users:
        try:
            programs.update(get_user_programs(u))
            courses.update(get_user_courses(u))
        except Exception as err:
            print(err)

    print('User programs:')
    for i in sorted(programs, key=lambda x: x.program_name_pl):
        i: Program
        print(i.program_id, i.program_name_pl, sep=' - ')

    print('\nUser courses:')
    for i in sorted(courses, key=lambda x: x.course_name_pl):
        i: Course
        print(i.course_name_pl, i.class_type_pl, sep=' --- ')

    print('\nUpdating user_programs table...')
    update_usos_programs(programs, usos_mysql_connector)
    print('Done.')

    print('\nUpdating user_courses table...')
    update_usos_courses(courses, usos_mysql_connector)
    print('Done.')

    # print('\nUser points:')
    # user_points = get_user_points(test_user)
    # for course, points in user_points.items():
    #     print(course)
    #     for point in points:
    #         print('\t{} - Score: {} points [{}]'.format(point.name, point.points, point.comment))
    #
    # print('\nUser timetable for tomorrow:')
    # tt = get_timetable_for_tommorow(test_user)
    # print(tt)
