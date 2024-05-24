def test(**kwargs):
    columnNames = " ".join(kwargs.keys())
    columnValues = ' '.join([f" {values}" for values in kwargs.values()])

    columnNames = columnNames.split()
    columnValues = columnValues.split()

    print(columnNames)

    sqlComand = ''

    for i in range(len(columnNames)):
        sqlComand += columnNames[i] + " " + columnValues[i] + ' , '

    sqlComand = sqlComand.split()
    sqlComand[-1] = ''
    sqlComand = ' '.join(sqlComand)

    print(sqlComand)
    
test(name='VARCHAR(255)', age='INT')
