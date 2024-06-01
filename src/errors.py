# errors.py
# Copyright (C) 2024 the PostPie developers
# (See DEVELOPERS FILE)

class TableDoesNotExist(Exception):
    pass

class ColumnDoesNotExist(Exception):

    def __init__(self, tableName, column):
        super().__init__(f'ERROR! Colum "{column}" does not exist in Table "{tableName}"')