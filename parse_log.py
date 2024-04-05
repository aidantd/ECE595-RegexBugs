"""
parse_log.py - Parse change log files to CSV
---------------------------------------------
To run, call from command line. 

parse_log will read the input files and create new CSV files, or
overwrite existing files, that contain columns for the version 
number, revision date, and revision description.

Change Logs currently supported:
- PCRE
- PCRE2
"""

"""
Created 03/14/2024
Michael Heinz
ECE59500 - Advanced Software Engineering, Purdue Univ.
Regex Bugs group project
"""

from enum import Enum
class LogType(Enum):
    PCRE = 1
    PCRE2 = 2

def decode_and_parse_pcre(data):
    """
    Parse PCRE Changelog text bytes and return a list with one row per
    revision, and the following columns: version number, date, description
    """
    
    # Decode bytes into text
    #   Note: ChangeLog_pcre.txt was downloaded from web and is encoded in 
    #         iso-8859-1. Using utf-8 will result in an error
    t = data.decode('iso-8859-1')
    
    # Find all line separators
    import re
    revisions = []
    for m in re.finditer(r'\n([^\n]+)\n(---+)\n', t):
        # print('%d: %02d-%02d: %s' % (i, m.start(), m.end(), m.group(2)))
        # i += 1
        revisions.append([m.start(), m.end(), m.group(1)])
       
    # Go back through and capture all description text between
    # revision subtitles. Also, parse revision subtitle into
    # number and date.
    for i in range(len(revisions)):
        rev = revisions[i]

        # Determine indices for revision description text
        start = rev[1]+1
        if i<len(revisions)-1:
            stop = revisions[i+1][0]
        else:
            stop = len(t)

        # Parse revision description text blocks into separate rows
        desc = t[start:stop].split('\n\n')
        
        # Parse version number and date from subtitle string
        ver = rev[2].split()
        ver_number = ver[1]
        if len(ver)>3:
            ver = [ver[0], ver[1], '-'.join(ver[2:])]
        ver_date = ver[2]

        # Reconstruct revision element and update array
        revisions[i] = [ver_number, ver_date, desc]
    
    # Flatten description lists
    flat_result = []
    for rev in revisions:
        for d in rev[2]:
            # Clean up line for easier importing/reading later
            d = d.replace('\n',' ') # remove line breaks within text block
            d = d.replace('  ',' ') # remove two-space indents
            d = d.replace('    ',' ') # remove four-space indents
            d = d.strip() # remove leading and/or trailing whitespace
            if len(d)<1:
                # skip empty lines
                continue
            # Avoid #NAME? error in Excel for leading '-' character, use '*' instead
            if d[0] == '-':
                d = '*' + d[1:]

            flat_result.append([rev[0], rev[1], d])

    return flat_result

def read_file_as_bytes(input_file):
    """
    Read changelog file as bytes instead of string to avoid decoding issues
    """
    
    # Read input_file
    print(f'Attempting to read from: {input_file}')
    with open(input_file, 'rb') as f:
        data = f.read()
        f.close()
    print(f'Read {len(data)} bytes from {input_file}')
    return data

def write_revisions_to_file_as_csv(revisions, output_file):
    """
    Write revisions data structure to a comma-separated values (CSV) file
    """
    import csv
    with open(output_file,'w',newline='') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='excel')
        csvwriter.writerow(['Version','Date','Description'])
        csvwriter.writerows(revisions)
    print(f'Wrote {len(revisions)} rows to {output_file}\n')


def parse_log(input_file, output_file, log_type = LogType.PCRE):
    
    data = read_file_as_bytes(input_file)

    if log_type is LogType.PCRE or LogType.PCRE2:
        revisions = decode_and_parse_pcre(data)
    else:
        raise Exception(f'Unrecognized input log_type: {log_type}')

    write_revisions_to_file_as_csv(revisions, output_file)
    

if __name__ == "__main__":
    parse_log('ChangeLog_pcre.txt', 'ChangeLog_pcre.csv', LogType.PCRE)
    parse_log('ChangeLog_pcre2.txt', 'ChangeLog_pcre2.csv', LogType.PCRE2)
