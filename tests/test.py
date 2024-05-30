# test.py
# Copyright (C) 2024 the PostPie developers
# (See DEVELOPERS FILE)

def test(**kwargs):

    columns = " ".join(kwargs.keys())
    values = ' '.join([f" '{values}'" for values in kwargs.values()])

    columns = columns.split()
    values = values.split()

    sqlCommand = ""

    for i in range(len(columns)):
        sqlCommand += columns[i] + " = " + values[i] + " , "

    sqlCommand = sqlCommand.split()
    sqlCommand[-1] = ''
    sqlCommand = ' '.join(sqlCommand)

    print(sqlCommand)
    
test(name="Brandon", age=12) 
