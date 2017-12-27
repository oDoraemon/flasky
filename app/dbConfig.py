import MySQLdb

class dbTest:
    DB_HOST = '192.168.15.30'
    DB_PORT = 3306
    DB_USER = 'srp_admin'
    DB_PASS = 'houyang@wws'
    DB_NAME = 'test'

    def get_db(self, config):
            conn = MySQLdb.connect(host=self.DB_HOST, port=self.DB_PORT, user=self.DB_USER, passwd=self.DB_PASS, db=self.DB_NAME, )
        except MySQLdb.Error,e:

