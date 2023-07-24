import sys, getopt
import os
import logging

from .lfs_blob_client import LFSBlobClient

def main():
    fileToRemove = None
    blobToRemove = None
    argv = sys.argv[1:]
    try:
        options, args = getopt.getopt(argv, "p:n:", ["path", "name"])
    except:
        print("Error Message ")

    for name, value in options:
        if name in ['-p', '--path']:
            fileToRemove = value
        elif name in ['-n', '--name']:
            blobToRemove = value

    # fileToRemove = argv[-1]
    logger = logging.getLogger()

    if fileToRemove is not None:
        if os.path.isdir(fileToRemove):
            logger.error('HSM operates on files, not on folders. The input path refers to a folder.')
        elif os.path.exists(fileToRemove):
            LFSBlobClient().lfs_hsm_remove(filePath=fileToRemove)
        else:
            logger.error('The file provided does not exist on the system')
    elif blobToRemove is not None:
        LFSBlobClient().lfs_hsm_remove(blobName=blobToRemove)
