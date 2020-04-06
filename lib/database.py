###########
# Database handling for lioness
####
import MySQLdb


class DataBase():
        conn = ''
        dbname = ''
        username = ''
        mypass = ''

        def __init__(self, dbname, username, mypass):
                self.dbname = dbname
                self.username = username
                self.mypass = mypass
                self.connect()

        def show_tables(self):
                return self.query("""SHOW TABLES;""", ())
        def connect(self):                
                self.conn = MySQLdb.connect(user=self.username, passwd=self.mypass, db=self.dbname )

        def query(self, query, holders):
                #print("qing {}".format(query))
                r = ''
                c = ''
                try:
                    c = self.conn.cursor()
                except (AttributeError, MySQLdb.OperationalError):
                    self.connect()



                if (len(holders) == 0):
                            self.connect()
                            self.conn.query(query)
                            result = self.conn.use_result()
                            r = result.fetch_row(0)
                        #print(r)
                else:
                    try:
                            c = self.conn.cursor()
                            r = c.execute(query, holders)
                            r =  c.fetchall()
                            self.conn.commit()
                    except (AttributeError, MySQLdb.OperationalError):
                            r = "Attribute error"
                            
                return r

                
