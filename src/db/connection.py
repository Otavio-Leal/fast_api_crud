from loguru import logger
import psycopg2

logger.add("src/logs/db_connection.log", rotation="500 MB")
    
class PostgreSQLConnection:
    
    def __init__(self, dbname, user, password, host, port='5432'):
        self.dbname = dbname
        self.user = user
        self.password =  password
        self.host = host
        self.port = port
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host, port=self.port)
            logger.info("Database connection sucessfull")
        except psycopg2.Error as e:
            logger.error(f"Database connection error:{e}")

    def select_user(self, query):
        if not self.conn:
            logger.info("You are not connected")
            return None
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            return rows
        except psycopg2.Error as e:
            logger.error(f"Erro executing select: {e}")
            return None

    def insert_user(self, id, name, area, job_description, role, salary, is_active, last_evaluation):
        if not self.conn:
            logger.info("You are not connected")
            return None
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO users (id, name, area, job_description, role, salary, is_active, last_evaluation) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (id, name, area, job_description, role, salary, is_active, last_evaluation)
            )
            self.conn.commit()
            cursor.close()
            logger.info("Registered user")
        except psycopg2.Error as e:
            logger.error(f"Erro executing insert: {e}")    
                 

    def update_user(self, id, name=None, area=None, job_description=None, role=None, salary=None, is_active=None, last_evaluation=None):
        if not self.conn:
            logger.info("You are not connected")
            return None
        
        try:
            cursor = self.conn.cursor()    
            update_query = "UPDATE users SET"
            update_values = []
            
            if name is not None:
                update_query += " name = %s,"
                update_values.append(name)
                
            if area is not None:
                update_query += " area = %s,"
                update_values.append(area)
            
            if job_description is not None:
                update_query += " job_description = %s,"
                update_values.append(job_description)
                
            if role is not None:
                update_query += " role = %s,"
                update_values.append(role)
                
            if salary is not None:
                update_query += " salary = %s,"
                update_values.append(salary)
                
            if is_active is not None:
                update_query += " is_active = %s,"
                update_values.append(is_active)
                
            if last_evaluation is not None:
                update_query += " last_evaluation = %s,"
                update_values.append(last_evaluation)
                
            update_query = update_query.rstrip(',') + " WHERE id = %s"
            update_values.append(id)
            
            cursor.execute(update_query, tuple(update_values))
            self.conn.commit()
            cursor.close()
            logger.info("Updated user") 
        except psycopg2.Error as e:
            logger.error(f"Erro executing update: {e}")
            return None

    def delete_user(self, query):
        if not self.conn:
            logger.info("You are not connected")
            return None
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            cursor.close()
            return None
        except psycopg2.Error as e:
            logger.error(f"Erro executing delete: {e}")
            return None

    def close(self):
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
            


        