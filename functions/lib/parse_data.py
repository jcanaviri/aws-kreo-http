def parse_data(raw_data):
    """Returns data and files send from form-data"""
    chunks = raw_data.split('\r\n')
    data = {}
    filename_file = {}
    files = {}

    for i in range(len(chunks)):
        if not chunks[i] or \
            '------WebkitFormBoundary' in chunks[i] or \
            '----------------------------' in chunks[i]:
            continue
        else:
            if 'Content-Disposition' in chunks[i]:
                split_by_part = chunks[i].split(';')
                if len(split_by_part) == 3:
                    keynameJunk = split_by_part[1].translate({ord('\"'): None})
                    keynameJunk = keynameJunk.strip()
                    key = keynameJunk[5:]

                    filenameJunk = split_by_part[2].translate({ord('\"'): None})
                    filenameJunk = filenameJunk.strip()
                    filename = filenameJunk[9:]
                    i += 3

                    filename_file['filename'] = filename
                    filename_file['file'] = chunks[i]
                    files[key] = filename_file
                else:
                    keyContent = split_by_part[1].translate({ord('\"'): None})
                    keyContent = keyContent.strip()
                    keyContentFilter = keyContent[5:]
                    i += 2
                    data[keyContentFilter] = chunks[i]
    
    filteredData = {}
    filteredData['data'] = data
    filteredData['files'] = files

    return filteredData
