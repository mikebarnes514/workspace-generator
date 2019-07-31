import synchsite
import sqldms
import subprocess
import shutil
from datetime import datetime
import logging
import os

currentTime = datetime.now().strftime('%Y-%m-%d-%H-%M')
logger = logging.getLogger(__name__)
    
def ArchiveLogs(is_personal):
    shutil.copy('files\\workspaces_{}.txt'.format('personal' if is_personal else 'public'), 'archive\\workspaces_{}-{}.txt'.format('personal' if is_personal else 'public', currentTime))
    shutil.copy('logs\\Debug.log', 'archive\\Debug-{}-{}.log'.format('personal' if is_personal else 'public', currentTime))
    shutil.copy('logs\\ErrorLog.log', 'archive\\ErrorLog-{}-{}.log'.format('personal' if is_personal else 'public', currentTime))
    shutil.copy('logs\\PagesFailed.log', 'archive\\PagesFailed-{}-{}.log'.format('personal' if is_personal else 'public', currentTime))
    shutil.copy('logs\\SuccessLog.log', 'archive\\SuccessLog-{}-{}.log'.format('personal' if is_personal else 'public', currentTime))
    shutil.copy('logs\\MaintenanceFailed.log', 'archive\\MaintenanceFailed-{}-{}.log'.format('personal' if is_personal else 'public', currentTime))
    shutil.copy('logs\\WSGResultLog.xml', 'archive\\WSGResultLog-{}-{}.xml'.format('personal' if is_personal else 'public', currentTime))

def SyncronizeCustomData():
    newCustom1 = synchsite.getCustom1ToAdd()
    updateCustom1 = synchsite.getCustom1ToUpdate()
    newCustom2 = synchsite.getCustom2ToAdd()
    updateCustom2 = synchsite.getCustom2ToUpdate()
    newCustom4 = synchsite.getCustom4ToAdd()
    newCustom5 = synchsite.getCustom5ToAdd()
    newCustom6 = synchsite.getCustom6ToAdd()
    
    logger.info('custom1 (new): {} | custom1 (update):{} | custom2 (new): {} | custom2 (update): {} | custom4: {} | custom5: {} | custom6: {}'.format(len(newCustom1), len(updateCustom1), len(newCustom2), len(updateCustom2), len(newCustom4), len(newCustom5), len(newCustom6)))
    if len(newCustom1) > 0:
        sqldms.insertCustom1(newCustom1)

    if len(updateCustom1) > 0:
        sqldms.updateCustom1(updateCustom1)

    if len(newCustom2) > 0:
        sqldms.insertCustom2(newCustom2)

    if len(updateCustom2) > 0:
        sqldms.updateCustom2(updateCustom2)

    if len(newCustom4) > 0:
        sqldms.insertCustom4(newCustom4)

    if len(newCustom5) > 0:
        sqldms.insertCustom5(newCustom5)

    if len(newCustom6) > 0:
        sqldms.insertCustom6(newCustom6)

    logger.info('custom data syncronized')

def AddWorkspaces():
    workspaces = synchsite.getWorkspacesToAdd()
    logger.info('public workspaces to add: {}'.format(len(workspaces)))
    if len(workspaces) > 0:
        with open('.\\files\\workspaces_public.txt', 'w') as f:
            for ws in workspaces:
                f.write('^'.join(ws))
                f.write('\n\r')

        subprocess.run('WorkspaceGeneratorCMD.exe -file ".\\files\\wsg_config_public.txt"')
        logger.info('workspacegeneratorcmd complete')
        ArchiveLogs(False)

def AddPersonalWorkspaces():
    workspaces = synchsite.getPersonalWorkspacesToAdd()
    logger.info('personal workspaces to add: {}'.format(len(workspaces)))
    if len(workspaces) > 0:
        with open('files\\workspaces_personal.txt', 'w') as f:
            for ws in workspaces:
                f.write('^'.join(ws))
                f.write('\n\r')

        subprocess.run('WorkspaceGeneratorCMD.exe -file ".\\files\\wsg_config_personal.txt"')
        logger.info('workspacegeneratorcmd complete')    
        ArchiveLogs(True)

def clearData():
    if os.path.exists('files\\workspaces_public.txt'): os.remove('files\\workspaces_public.txt')
    if os.path.exists('files\\workspaces_personal.txt'): os.remove('files\\workspaces_personal.txt')
    if os.path.exists('logs\\Debug.log'): os.remove('logs\\Debug.log')
    if os.path.exists('logs\\ErrorLog.log'): os.remove('logs\\ErrorLog.log')
    if os.path.exists('logs\\PagesFailed.log'): os.remove('logs\\PagesFailed.log')
    if os.path.exists('logs\\SuccessLog.log'): os.remove('logs\\SuccessLog.log')
    if os.path.exists('logs\\MaintenanceFailed.log'): os.remove('logs\\MaintenanceFailed.log')
    if os.path.exists('logs\\WSGResultLog.xml'): os.remove('logs\\WSGResultLog.xml')

def main():
    logger.info('-------------------- process starting --------------------')
    clearData()
    logger.info('syncronizing custom data')
    SyncronizeCustomData()
    logger.info('adding public workspaces')
    AddWorkspaces()
    logger.info('adding personal workspaces')
    AddPersonalWorkspaces()
    logger.info('-------------------- process complete --------------------')

if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler('wsg-log.txt')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    try:
        main()
    except Exception as err:
        logger.error(err)
