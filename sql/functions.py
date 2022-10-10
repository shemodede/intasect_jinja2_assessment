import sqlite3
from sqlite3 import Error
from .statements import *


def create_db(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def create_table(db_file, create_statement):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute(create_statement)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def create_tables(db_file):
    create_table(db_file, create_user_table)
    create_table(db_file, create_chassis_types_table)
    create_table(db_file, create_vehicles_table)
    create_table(db_file, create_tyrelocation_table)
    create_table(db_file, create_tyres_table)

def insert_user_data(db_file, name, email, loginid, password, usertype):
    conn = sqlite3.connect(db_file)
    conn.execute(insert_user_data_statement, (name, email, loginid, password, usertype))
    conn.commit()
    conn.close()

def insert_chassis_type_data(db_file, name):
    conn = sqlite3.connect(db_file)
    conn.execute(insert_chassis_type_statement, [name])
    conn.commit()
    conn.close()

def select_chassis_type_data(db_file):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute(select_chassis_type_statement)
    rows = cur.fetchall()
    return rows

def insert_vehicle_data(db_file, fleet_code, regnumber, chassisid):
    conn = sqlite3.connect(db_file)
    conn.execute(insert_vehicle_data_statement, (fleet_code, regnumber, chassisid))
    conn.commit()
    conn.close()

def select_vehicle_data(db_file):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute(select_vehicle_data_statement)
    rows = cur.fetchall()
    return rows

def insert_tyre_data(db_file, name, serialnum):
    conn = sqlite3.connect(db_file)
    conn.execute(insert_tyre_data_statement, (name, serialnum))
    conn.commit()
    conn.close()

def select_tyre_data(db_file):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute(select_tyre_data_statement)
    rows = cur.fetchall()
    return rows

def insert_tyre_location_data(db_file, tyreid, dateticks, direction, vehicleid):
    conn = sqlite3.connect(db_file)
    conn.execute(insert_tyre_location_data_statement, (tyreid, dateticks, direction, vehicleid))
    conn.commit()
    conn.close()

def select_tyre_location_data(db_file):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute(select_tyre_location_data_statement)
    rows = cur.fetchall()
    return rows

def update_user_profile(db_file, name, email, password, loginid, userid):
    conn = sqlite3.connect(db_file)
    conn.execute(update_user_profile_statement, (name, email, password, loginid, userid))
    conn.commit()
    conn.close()

def get_tyre_journey_data(db_file):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute(select_tyre_journey_data_statement)
    rows = cur.fetchall()
    return rows

def get_user_object(db_file, loginid, password):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute(select_user_object_statement, (loginid, password))
    row = cur.fetchone()
    return row

def get_user_object_with_id(db_file, user_id):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute(select_user_object_by_id_statement, [user_id])
    row = cur.fetchone()
    return row

