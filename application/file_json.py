import os
import json
import psycopg2

try:
    conn = psycopg2.connect("dbname='face_reco' user='face_reco_admin' host='localhost' password='qwerty123'")
except:
    print ("I am unable to connect to the database")


def count_files(pk):
    path_detected = os.getcwd() + '/media/folders/final/detected'
    path_unknown = os.getcwd() + '/media/folders/final/unknown'
    # two folders files
    all_detected = os.listdir(path_detected)
    all_unknown = os.listdir(path_unknown)

    # get all result in one list
    all_res = all_detected + all_unknown
    all_res.sort(reverse=True)

    step = 20

    if not pk == 0:
        all_res = all_res[pk * step - step:pk * step]

    # count all number of list
    all_number = len(all_res)

    # json result
    total_res = dict()

    total_res["total"] = all_number
    total_res["totalNotFiltered"] = all_number
    rows = list()

    for res in all_res:
        mid_dict = dict()
        if res in all_detected:
            t = res.split('-')
            html = '<img src="/static/folders/final/detected/' + res + '" alt="crop_camera" class = "image_res" id="' \
                   + res + '">'
            mid_dict['detected'] = html
            html = '<img src="/static/folders/db/' + t[1] + '.jpg" alt="original_db"  class="image_res">'
            mid_dict['matched'] = html
            mid_dict['name'] = t[1]
            mid_dict['confidence'] = t[2]
            date = t[0][:-6].split('_')
            date = date[0] + '/' + date[1] + '/' + date[2] + ' ' + date[3] + ':' + date[4] + ':' + date[5]
            mid_dict['date'] = date
        else:
            html = '<img src="/static/folders/final/unknown/' + res + '" alt="crop_camera" class = "image_res" id="' \
                   + res + '">'
            mid_dict['detected'] = html
            mid_dict['matched'] = 'Unknown'
            mid_dict['name'] = 'Unknown'
            mid_dict['confidence'] = '0'
            date = res[:-6].split('_')
            date = date[0] + '/' + date[1] + '/' + date[2] + ' ' + date[3] + ':' + date[4] + ':' + date[5]
            mid_dict['date'] = date

        rows.append(mid_dict)

    total_res["rows"] = rows

    return total_res


def count_users(pk):
    cur = conn.cursor()
    step = 20
    sql_string = 'SELECT * FROM (SELECT * FROM public.tengri_crops ORDER BY id DESC LIMIT ' + str(step) \
                 + ') as foo ORDER BY id desc'
    cur.execute(sql_string)
    res_sql = cur.fetchall()
    print(res_sql)

    total_res = dict()

    total_res["total"] = 20
    total_res["totalNotFiltered"] = 20
    rows = list()
    for res in res_sql:
        mid_dict = dict()
        if res[4] != '0':
            html = '<img src="/static/folders/final/detected/' + res[1] + '" alt="crop_camera" class = "image_res" id="' \
                   + res[1] + '">'
            mid_dict['detected'] = html
            html = '<img src="/static/folders/db/' + res[4] + '.jpg" alt="original_db"  class="image_res">'
            mid_dict['matched'] = html
            mid_dict['confidence'] = str(res[7])
            mid_dict['date'] = str(res[2]) + ' ' + str(res[3])

        else:
            html = '<img src="/static/folders/final/unknown/' + res[1] + '" alt="crop_camera" class = "image_res" id="' \
                   + res[1] + '">'
            mid_dict['detected'] = html
            mid_dict['matched'] = 'Unknown'
            mid_dict['confidence'] = '0'
            mid_dict['date'] = str(res[2]) + ' ' + str(res[3])
        rows.append(mid_dict)

    total_res["rows"] = rows
    print(total_res)
    return total_res


def telegram():
    path_detected = os.getcwd() + '/application/static/folders/final/detected'
    path_unknown = os.getcwd() + '/application/static/folders/final/unknown'
    # two folders files
    all_detected = os.listdir(path_detected)

    all_detected.sort(reverse=True)

    total_res = dict()

    total_res['rows'] = all_detected

    return total_res
