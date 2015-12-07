# encoding:utf-8
import MySQLdb

class Mysqlexec(object):
    def __init__(self, host, user, pasd, db,isdict=False) :
        self.conn = MySQLdb.connect(host=host, user=user, passwd=pasd, port=3306, db=db, charset="utf8")
        if isdict == True:
            self.cur = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        else:
            self.cur = self.conn.cursor()
        
    def __enter__(self):
        return self
        
    def __exit__(self, exception_type, exception_value, exception_traceback):
        if exception_type is None:   
            self.conn.commit()
            self.cur.close()
            self.conn.close()
        else:  
            slef.cursor.rollback()  
        return False

    def sql(self, sql):
        self.cur.execute(sql)
        return self.cur
 
