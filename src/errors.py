class TableDoesNotExist(Exception):
    pass

class ColumnDoesNotExist(Exception):

    def __init__(self, tableName, column):
        super().__init__(f'ERROR! Colum "{column}" does not exist in Table "{tableName}"')