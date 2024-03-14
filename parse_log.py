"""
parse_log.py - Parse change log files to CSV
---------------------------------------------
To run, call from command line. 

parse_log will read the input files and create new CSV files, or
overwrite an existing files, that contain columns for the version 
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

def parse_log(input_file, output_file):
    # Read input_file
    print(f'Attempting to read from: {input_file}')
    with open(input_file, 'rb') as f:
        data = f.read()
        f.close()
    print(f'Read {len(data)} bytes from {input_file}')

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
    for i in range(len(revisions)):
        rev = revisions[i]
        start = rev[1]+1
        if i<len(revisions)-1:
            stop = revisions[i+1][0]
        else:
            stop = len(t)

        ver = rev[2].split()
        if len(ver)>3:
            ver = [ver[0], ver[1], '-'.join(ver[2:])]

        ver_number = ver[1]
        ver_date = ver[2]
        desc = t[start:stop].strip()
        desc = desc.replace('\n', ' ')
        desc = desc.replace('"', "'") # make sure all quotes are single-quotes

        revisions[i] = [ver_number, ver_date, desc]
    
    # print(revisions[-1])

    # Prepare output text
    t_out = ''
    for rev in revisions:
        t_out += f'"{rev[0]}", "{rev[1]}", "{rev[2]}"\n'

    # Output to file
    with open(output_file,'w') as f:
        f.write(t_out)
        f.close()

    print(f'Wrote {len(revisions)} lines to {output_file}')

if __name__ == "__main__":
    parse_log('ChangeLog_pcre.txt', 'ChangeLog_pcre.csv')
    parse_log('ChangeLog_pcre2.txt', 'ChangeLog_pcre2.csv')
