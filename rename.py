import os
import datetime

os.chdir('dataset')

count = 0
for f in os.listdir():
    # Split by name and ext
    file_name, file_ext = os.path.splitext(f)
    # File name by _
    company, date, name = file_name.split('_')
    # Get month and date
    month = date[:3]
    year = date[3:]
    # Get number of mon abbreviation
    datetime_object = datetime.datetime.strptime(month, "%b")
    month_num = datetime_object.month
    # Rename
    new_name = f'{year}{month_num:02d}-{month}{file_ext}'
    os.rename(f, new_name)

    count+=1
print(f'Successfully renamed {count} files.')