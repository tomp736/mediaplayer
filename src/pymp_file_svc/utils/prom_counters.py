from prometheus_client import Counter

fileaccess_validate_filename_total = Counter(f"fileaccess_validate_filename_total", "fileaccess_validate_filename_total")
fileaccess_validate_filename_error_empty_total = Counter(f"fileaccess_validate_filename_error_empty_total", "fileaccess_validate_filename_error_empty_total")
fileaccess_validate_filename_error_length_total = Counter(f"fileaccess_validate_filename_error_length_total", "fileaccess_validate_filename_error_length_total")
fileaccess_validate_filename_error_regex_total = Counter(f"fileaccess_validate_filename_error_regex_total", "fileaccess_validate_filename_error_regex_total")

fileaccess_write_file_total = Counter(f"fileaccess_write_file_total", "fileaccess_write_file_total")

def inc_fileaccess_validate_filename_total():
    fileaccess_validate_filename_total.inc()
    
def inc_fileaccess_validate_filename_error_empty_total():
    fileaccess_validate_filename_error_empty_total.inc()
    
def inc_fileaccess_validate_filename_error_length_total():
    fileaccess_validate_filename_error_length_total.inc()
    
def inc_fileaccess_validate_filename_error_regex_total():
    fileaccess_validate_filename_error_regex_total.inc()
    
def inc_fileaccess_write_file_total():
    fileaccess_write_file_total.inc()