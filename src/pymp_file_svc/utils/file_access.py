import uuid
import os
import fcntl
import logging
from .prom_counters import *
        
folder = os.environ.get('UPLOAD_FOLDER', '/files')

def validate_filename(filename):
    inc_fileaccess_validate_filename_total();
    if filename == '':
        inc_fileaccess_validate_filename_error_empty_total();
        logging.info(f"{filename} empty.")
        return False
    if len(filename) > 255:
        inc_fileaccess_validate_filename_error_length_total();
        logging.info(f"{filename} must be less than 255 chars.")
        return False
    if any(c in '<>: "\\/|?*' for c in filename):
        inc_fileaccess_validate_filename_error_regex_total();
        logging.info(f"{filename} failed regex check.")
        return False
    return True
        
def get_folder(filename):
    hash_value = hash(filename)
    hash_hex = hex(hash_value)
    filefolder = hash_hex[2:26]
    return filefolder

def write_file(filename, file):
    inc_fileaccess_write_file_total()
    filefolder = get_folder(filename)
    fileuuid = str(uuid.uuid4())
    fullpath = os.path.join(folder, filefolder, fileuuid)
    fullslpath = os.path.join(folder, file.filename)
    
    # Create folder if not exists.
    fullfilefolder = os.path.join(folder, filefolder)
    if not os.path.exists(fullfilefolder):
        os.makedirs(fullfilefolder)

    # Open the file for writing using a filestream
    with open(fullpath, 'wb') as f:
        # Acquire an exclusive lock on the file
        fcntl.flock(f, fcntl.LOCK_EX)
        # Write to the file
        f.write(file.read())
        # Release the lock
        fcntl.flock(f, fcntl.LOCK_UN)

    os.symlink(f"./{filefolder}/{fileuuid}", f"{fullslpath}.tmp")
    os.rename(f"{fullslpath}.tmp", fullslpath)

    return fileuuid