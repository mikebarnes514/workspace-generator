import pyodbc
import logging

try:
    #conn = pyodbc.connect('DRIVER={SQL Server Native Client 10.0};SERVER=GR-SQLDMS-01;DATABASE=MJ_DMS;Trusted_Connection=yes;')
    conn = pyodbc.connect('DSN=SQLDMS')
    cursor = conn.cursor()
except Exception as err:
    logging.warn('failed to connect to MJ_DMS on GR-SQLDMS-01: {}'.format(err.message))
    quit()

def insertCustom1(records):
    for alias,desc in records:
        try:
            cursor.execute("insert into MHGROUP.CUSTOM1 (CUSTOM_ALIAS, C_DESCRIPT, ENABLED, IS_HIPAA) VALUES ('{}', '{}', 'Y', 'N')".format(alias, desc.replace("'", "''")))
            cursor.commit()
        except Exception as err:
            logging.warn('could not insert ("{}", "{}") into CUSTOM1: {}'.format(alias, desc, str(err)))

def updateCustom1(records):
    for alias,desc in records:
        try:
            cursor.execute("update MHGROUP.CUSTOM1 set C_DESCRIPT = '{}' where CUSTOM_ALIAS = '{}'".format(desc.replace("'", "''"), alias))
            cursor.commit()
        except Exception as err:
            logging.warn('could not update C_DESCRIPT to "{}" for "{}" in CUSTOM1: {}'.format(desc,alias, str(err)))

def insertCustom2(records):
    for  palias,pdesc,alias,desc in records:
        try:
            cursor.execute("insert into MHGROUP.CUSTOM2 (CPARENT_ALIAS, CUSTOM_ALIAS, C_DESCRIPT, ENABLED, IS_HIPAA) VALUES('{}', '{}', '{}', 'Y', 'N')".format(palias, alias, desc.replace("'", "''")))
            cursor.commit()
        except Exception as err:
            logging.warn('could not insert ("{}", "{}") into CUSTOM2: {}'.format(alias, desc, str(err)))

def updateCustom2(records):
    for  palias,pdesc,alias,desc in records:
        try:
            cursor.execute("update MHGROUP.CUSTOM2 SET C_DESCRIPT = '{}' WHERE CPARENT_ALIAS = '{}' AND CUSTOM_ALIAS = '{}'".format(desc.replace("'", "''"), palias, alias))
            cursor.commit()
        except Exception as err:
            logging.warn('could not update C_DESCRIPT to "{}" for "{}-{}" in CUSTOM2: {}'.format(desc,palias,alias, str(err)))

def insertCustom4(records):
    for alias,desc in records:
        try:
            cursor.execute("insert into MHGROUP.CUSTOM4 (CUSTOM_ALIAS, C_DESCRIPT, ENABLED, IS_HIPAA) VALUES('{}', '{}', 'Y', 'N')".format(alias, desc.replace("'", "''")))
            cursor.commit()
        except Exception as err:
            logging.warn('could not insert ("{}", "{}") into CUSTOM4: {}'.format(alias, desc, str(err)))

def insertCustom5(records):
    for alias,desc in records:
        try:
            cursor.execute("insert into MHGROUP.CUSTOM5 (CUSTOM_ALIAS, C_DESCRIPT, ENABLED, IS_HIPAA) VALUES('{}', '{}', 'Y', 'N')".format(alias, desc.replace("'", "''")))
            cursor.commit()
        except Exception as err:
            logging.warn('could not insert ("{}", "{}") into CUSTOM5: {}'.format(alias, desc, str(err)))

def insertCustom6(records):
    for alias,desc in records:
        try:
            cursor.execute("insert into MHGROUP.CUSTOM6 (CUSTOM_ALIAS, C_DESCRIPT, ENABLED, IS_HIPAA) VALUES('{}', '{}', 'Y', 'N')".format(alias, desc.replace("'", "''")))
            cursor.commit()
        except Exception as err:
            logging.warn('could not insert ("{}", "{}") into CUSTOM6: {}'.format(alias, desc, str(err)))
    

        
