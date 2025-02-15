import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    def __init__(self, name, breed, id=None):
        self.name = name
        self.breed = breed
        self.id = id
    
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs
                (id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    def save(self):
        if self.id:
            self.update()
        else:
            sql = """
                INSERT INTO dogs (name, breed)
                VALUES (?, ?)
            """
            CURSOR.execute(sql, (self.name, self.breed))
            CONN.commit()
            self.id = CURSOR.lastrowid
    
    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog
    
    @classmethod
    def new_from_db(cls, row):
        id, name, breed = row
        return cls(name, breed, id)
    
    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM dogs
        """
        results = CURSOR.execute(sql).fetchall()
        return [cls.new_from_db(row) for row in results]
    
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM dogs
            WHERE name = ?
            LIMIT 1
        """
        result = CURSOR.execute(sql, (name,)).fetchone()
        if result:
            return cls.new_from_db(result)
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM dogs
            WHERE id = ?
            LIMIT 1
        """
        result = CURSOR.execute(sql, (id,)).fetchone()
        if result:
            return cls.new_from_db(result)
    
    @classmethod
    def find_or_create_by(cls, name, breed):
        dog = cls.find_by_name(name)
        if not dog:
            dog = cls.create(name, breed)
        return dog
    
    def update(self):
        sql = """
            UPDATE dogs SET name = ?, breed = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()
#GDC#8