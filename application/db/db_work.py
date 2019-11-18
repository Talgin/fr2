# Scipt to insert 
import psycopg2
from memsql.common import database
from numpy import linalg as LA
import numpy as np
import pandas as pd
from pandas import DataFrame
import struct


class databaseWorker:
    def __init__(self, connectionString, file_extension):
        self.connectionString = connectionString
        self.file_extension = file_extension

    def insertOriginal(self, title, i_date, i_time, img):
        """ insert original image as BLOB into tengrimage table """
        conn = None
        try:
            # connect to the PostgresQL database
            conn = psycopg2.connect(self.connectionString)
            # create a new cursor object
            cur = conn.cursor()
            # execute the INSERT statement
            cur.execute(
                "INSERT INTO public.tengrimage(title, i_date, i_time, img, i_extension) " + "VALUES(%s,%s,%s,%s,%s)",
                (title, i_date, i_time, psycopg2.Binary(img), self.file_extension))
            # commit the changes to the database
            conn.commit()
            # close the communication with the PostgresQL database
            cur.close()
            print('Successfully inserted ' + title)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: " + str(error))
        finally:
            if conn is not None:
                conn.close()

    def insertCrop(self, title, crop_date, crop_time, similarity, person_id, coord_x, coord_y, width_x, height_y):
        """ insert cropped and recognized image as BLOB into tengri_crops table """
        conn = None
        try:
            # connect to the PostgresQL database
            conn = psycopg2.connect(self.connectionString)
            # create a new cursor object
            cur = conn.cursor()
            # execute the INSERT statement
            cur.execute(
                "INSERT INTO public.tengri_crops(title, crop_date, crop_time, person_id, coord_x, coord_y, similarity, width_x, height_y) " +
                "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (title, crop_date, crop_time, person_id, coord_x, coord_y, similarity, width_x, height_y))
            # commit the changes to the database
            conn.commit()
            # close the communication with the PostgresQL database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print('Error: ' + str(error))
        finally:
            if conn is not None:
                conn.close()

    def getSimilarity(self, feature, host, port, user, pwd):
        conn = None
        res = None
        vectorStr = "".join([struct.pack('f', elem) for elem in feature])
        vectorStrEncoded = vectorStr.encode('hex')
        try:
            # connect to the MemSQL database
            conn = database.connect(host=host, port=port, user=user, password=pwd)
            # execute the INSERT statement
            # stre = "INSERT INTO FR.akkol_school(person_iin, feature_vector) VALUES ('"+ iin +"'"+", UNHEX('%s'))" % (vectorStrEncoded)
            res = conn.query(
                'SELECT red_id, fio, info, DOT_PRODUCT(feature_vector, UNHEX("%s")) as score from FR.red_test order by score '
                'desc limit 1;' % (vectorStrEncoded))
            # res = conn.query('SELECT person_iin, DOT_PRODUCT(UNHEX(feature_vector), UNHEX("%s")) as score from
            # FR.features_binary order by score desc limit 1;' % (vectorStrEncoded))
            conn.close()
        except:
            print('Select error')
        finally:
            if conn is not None:
                conn.close()
        return res

    def getSimilarity5(self, feature, host, port, user, pwd):
        conn = None
        res = None
        vectorStr = "".join([struct.pack('f', elem) for elem in feature])
        vectorStrEncoded = vectorStr.encode('hex')
        try:
            # connect to the MemSQL database
            conn = database.connect(host=host, port=port, user=user, password=pwd)
            # execute the INSERT statement
            # stre = "INSERT INTO FR.akkol_school(person_iin, feature_vector) VALUES ('"+ iin +"'"+", UNHEX('%s'))" % (vectorStrEncoded)
            res = conn.query(
                'SELECT udv_no, iin, fio, DOT_PRODUCT(feature_vector, UNHEX("%s")) as score from FR.tengri_test order by score '
                'desc limit 5;' % (vectorStrEncoded))
            # res = conn.query('SELECT person_iin, DOT_PRODUCT(UNHEX(feature_vector), UNHEX("%s")) as score from
            # FR.features_binary order by score desc limit 1;' % (vectorStrEncoded))
            conn.close()
        except:
            print('Select error')
        finally:
            if conn is not None:
                conn.close()
        return res

    def getSimilarityTest(self, feature, host, port, user, pwd):
        conn = None
        res = None
        vectorStr = "".join([struct.pack('f', elem) for elem in feature])
        vectorStrEncoded = vectorStr.encode('hex')
        try:
            # connect to the MemSQL database
            conn = database.connect(host=host, port=port, user=user, password=pwd)
            # execute the INSERT statement
            # stre = "INSERT INTO FR.akkol_school(person_iin, feature_vector) VALUES ('"+ iin +"'"+", UNHEX('%s'))" % (vectorStrEncoded)
            res = conn.query('SELECT red_id, fio, info, DOT_PRODUCT(feature_vector, UNHEX("%s")) as score from FR.red_test WHERE DOT_PRODUCT(feature_vector, UNHEX("%s")) >= 0.5;' % (vectorStrEncoded, vectorStrEncoded))
            # res = conn.query('SELECT person_iin, DOT_PRODUCT(UNHEX(feature_vector), UNHEX("%s")) as score from
            # FR.features_binary order by score desc limit 1;' % (vectorStrEncoded))
            conn.close()
        except:
            print('Select error')
        finally:
            if conn is not None:
                conn.close()
        return res

    def insertUsers(self, user_id, insert_date, insert_time, img, name, llist):
        """ insert cropped and recognized image as BLOB into tengri_crops table """
        conn = None
        try:
            # connect to the PostgresQL database
            conn = psycopg2.connect(self.connectionString)
            # create a new cursor object
            cur = conn.cursor()
            # execute the INSERT statement
            cur.execute(
                "INSERT INTO public.tengri_users(user_id, insert_date, insert_time, img, user_name, llist) " +
                "VALUES(%s,%s,%s,%s,%s,%s)",
                (user_id, insert_date, insert_time, psycopg2.Binary(img), name, llist))
            # commit the changes to the database
            conn.commit()
            # close the communication with the PostgresQL database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print('Error: ' + str(error))
        finally:
            if conn is not None:
                conn.close()
