import pyexcel_ods3 as ods3

def ods_to_dict(speadsheet):
    data = ods3.get_data(speadsheet)

    result_dict = {}
    for sheet_name, sheet_data in data.items():
        header = sheet_data[0]
        sheet_dict = {}
        for row in sheet_data[1:]:
            try:
                row_dict = {}
                for i, value in enumerate(row):
                    row_dict[header[i]] = value
                sheet_dict[row[0]] = row_dict
            except IndexError:
                pass
        result_dict[sheet_name] = sheet_dict
    
    return result_dict
