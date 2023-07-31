import sys, getopt
import os
import logging

from .lfs_blob_client import LFSBlobClient

def main():
    argv = sys.argv[1:]
    try:
        options, args = getopt.getopt(argv, "c:", ["cleanup"])
    except:
        print("Error Message ")

    logger = logging.getLogger()
    fileToRemove = argv[-1]
    isLocal = True
    for name, value in options:
        if name in ['-c', '--cleanup']:
            isLocal = False

    if os.path.isdir(fileToRemove):
        logger.error('HSM operates on files, not on folders. The input path refers to a folder.')
    elif os.path.exists(fileToRemove) == isLocal:
        LFSBlobClient().lfs_hsm_remove(fileToRemove, isLocal)
    elif not os.path.exists(fileToRemove) and isLocal:
        logger.error('The file provided does not exist on the system')
    elif os.path.exists(fileToRemove) and not isLocal:
        logger.error('Cannot cleanup remote file, the file still exists on the lustre filesystem')

# TODO: cleanup cl arg options, add getting blob from url (azure blob does not use FID), add checks (blob.exists() before/after del..)
# TODO: custom rbh commands (store blob url = container url + relative path as lhsm.uuid in rbh DB to delete lost files? get path from DB as SELECT `one_path`('fid'))
