import re
from flask import Request

def get_request_range(request:Request):
    range_header = request.headers.get('Range', None)
    sByte, eByte = 0, None
    if range_header:
        match = re.search(r'(\d+)-(\d*)', range_header)
        if match is not None:
            groups = match.groups()
            if groups[0]:
                sByte = int(groups[0])
            if groups[1]:
                eByte = int(groups[1])

    return sByte, eByte