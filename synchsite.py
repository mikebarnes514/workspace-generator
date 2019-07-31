import pyodbc
import logging
import struct
from datetime import datetime, timedelta

def datetime_as_string(raw_bytes):
    tup = struct.unpack('<2l', raw_bytes)
    days = tup[0]
    partial_day = round(tup[1] / 300.0, 3)
    date_time = datetime(1900, 1, 1) + timedelta(days=days) + timedelta(seconds=partial_day)
    return date_time.strftime('%m/%d/%Y')[:23]

try:
    #conn = pyodbc.connect('DRIVER={SQL Server Native Client 10.0};SERVER=GR-SQL-04;DATABASE=SynchSite;Trusted_Connection=yes;')
    conn = pyodbc.connect('DSN=SYNCHSITE')
    conn.add_output_converter(pyodbc.SQL_TYPE_TIMESTAMP, datetime_as_string)
    cursor = conn.cursor()
except Exception as err:
    logging.warn('failed to connect to SynchSite on GR-SQL-04: {}'.format(str(err)))
    quit()

def getCustom1ToAdd():
    return cursor.execute("select CUSTOM_ALIAS, C_DESCRIPT from dbo.vwCustom1_Add").fetchall()

def getCustom1ToUpdate():
    return cursor.execute("select CUSTOM_ALIAS, C_DESCRIPT from vwCustom1_UPDATE").fetchall()

def getCustom2ToAdd():
    return cursor.execute("select CPARENT_ALIAS, CPARENT_NAME, CUSTOM_ALIAS, C_DESCRIPT from vwCustom2_Add").fetchall()

def getCustom2ToUpdate():
    return cursor.execute("select CPARENT_ALIAS, CPARENT_NAME, CUSTOM_ALIAS, C_DESCRIPT from vwCustom2_UPDATE").fetchall()

def getCustom4ToAdd():
    return cursor.execute("select CUSTOM_ALIAS, C_DESCRIPT from vwCustom4_Add").fetchall()

def getCustom5ToAdd():
    return cursor.execute("select CUSTOM_ALIAS, C_DESCRIPT from vwCustom5_Add").fetchall()

def getCustom6ToAdd():
    return cursor.execute("select CUSTOM_ALIAS, C_DESCRIPT from vwCustom6_Add").fetchall()

def getWorkspacesToAdd():
    return cursor.execute("select distinct sLibrary, sOwner, sName, sDescription, sTemplate, sCategory, C1ALIAS, C2ALIAS, C3ALIAS, C4ALIAS, C5ALIAS, C6ALIAS, C7ALIAS, C8ALIAS, C9ALIAS, C10ALIAS, C11ALIAS, C12ALIAS, C13ALIAS, C14ALIAS, C15ALIAS, C16ALIAS, C29ALIAS, C30ALIAS, C31ALIAS, CDBL1, CDBL2, CDBL3, CDBL4, CBOOL1, CBOOL2, CBOOL3, CBOOL4, CDATE1, CDATE2, CDATE3, CDATE4, sEmail from vw_WorkspaceCandidateAdd").fetchall()

def getPersonalWorkspacesToAdd():
    return cursor.execute("select distinct sLibrary, sOwner, sName, sDescription, sTemplate, sCategory, C1ALIAS, C2ALIAS, C3ALIAS, C4ALIAS, C5ALIAS, C6ALIAS, C7ALIAS, C8ALIAS, C9ALIAS, C10ALIAS, C11ALIAS, C12ALIAS, C13ALIAS, C14ALIAS, C15ALIAS, C16ALIAS, C29ALIAS, C30ALIAS, C31ALIAS, CDBL1, CDBL2, CDBL3, CDBL4, CBOOL1, CBOOL2, CBOOL3, CBOOL4, CDATE1, CDATE2, CDATE3, CDATE4, sEmail from vw_WorkspacePERSONALCandidateAdd").fetchall()

def getTemplateMappings():
    return cursor.execute("select CATEGORY, sWorkspaceID from vwWorkspace_ID where WorkspaceType = 'template'").fetchall()

