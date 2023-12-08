import mysql.connector

class Database:
    def __init__(self):
        self.my_db = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='',
            database='recipe'
        )
        self.my_cursor = self.my_db.cursor()

    def close_connection(self):
        self.my_cursor.close()
        self.my_db.close()

class DatabaseAccess:
    def __init__(self):
        self.database = Database()

    def read_id(self, table_name, mode='ASC'):
        '''Read recipe ids from database'''
        try:
            sql = 'SELECT recipe_id FROM {} ORDER BY recipe_id {}'.format(table_name, mode)
            self.database.my_cursor.execute(sql)
            result = self.database.my_cursor.fetchall()
            return result
        except mysql.connector.Error as e:
            return str(e)
        
    def check_not_exist_id(self, first_table, second_table):
        '''Check recipe ids that not exist in second table'''
        try:
            sql = 'SELECT a.recipe_id FROM {} a WHERE a.recipe_id NOT IN (SELECT DISTINCT p.recipe_id FROM {} p) ORDER BY recipe_id'.format(first_table, second_table)
            self.database.my_cursor.execute(sql)
            result = self.database.my_cursor.fetchall()
            return result
        except mysql.connector.Error as e:
            return str(e)

    def read_ingredients(self, table_name, mode='ASC'):
        '''Read ingredients from database'''
        try:
            sql = 'SELECT ingredient FROM {} ORDER BY recipe_id {}'.format(table_name, mode)
            self.database.my_cursor.execute(sql)
            result = self.database.my_cursor.fetchall()
            return result
        except mysql.connector.Error as e:
            return str(e)
        
    def read_ingredients_by_ids(self, table_name, recipe_ids):
        '''Read ingredients from database by recipe ids'''
    
        try:
            sql = 'SELECT ingredient FROM {} WHERE recipe_id IN ({})'.format(table_name, recipe_ids)
            self.database.my_cursor.execute(sql)
            result = self.database.my_cursor.fetchall()
            return result
        except mysql.connector.Error as e:
            return str(e)
        
    def insert_many_ingredients(self, list_data, table_name='recipe_details'):
        '''Insert multiple ingredients to database'''
        try:
            sql = 'INSERT INTO {} (recipe_id, ingredient) VALUES (%s, %s)'.format(table_name)
            self.database.my_cursor.executemany(sql, list_data)
            self.database.my_db.commit()
            return self.database.my_cursor.rowcount
        except mysql.connector.Error as e:
            return str(e)

    def close_connection(self):
        self.database.close_connection()