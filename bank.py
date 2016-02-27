__author__ = 'jeremyt'
import pymysql


class Account:
    def __init__(self):
        self.name = ''
        self.number = ''
        self.balance = 0
        self.db_init()

    def deposit(self, number, amount):
        if amount <= 0:
            raise ValueError('amount must be positive')

        self.cur.execute("select balance from account where account_id=" + number)

        for row in self.cur.fetchall():
            self.balance = row["balance"]

        self.balance += amount
        self.cur.execute("update account set balance=" + str(self.balance))
        self.conn.commit()

        sql = "insert into log (account_id,amount) values('" + number + "'," + str(amount) + ")"
        # print sql
        self.cur.execute(sql)
        self.conn.commit()

    def withdraw(self, number, amount):

        if amount > self.balance:
            raise ValueError('balance not enough')

        self.cur.execute("select balance from account where account_id=" + number)

        for row in self.cur.fetchall():
            self.balance = row["balance"]

        self.balance -= amount
        self.cur.execute("update account set balance=" + str(self.balance))
        self.conn.commit()

        sql = "insert into log (account_id,amount) values('" + number + "'," + str(amount * -1) + ")"
        # print sql
        self.cur.execute(sql)
        self.conn.commit()

    def show(self, number):

        self.cur.execute("select * from account where account_id=" + number)

        for row in self.cur.fetchall():
            self.name = row["name"]
            self.balance = row["balance"]

        print 'Account({0}, {1}, {2})'.format(self.name, number, self.balance)

    def __str__(self):
        return 'Account({0}, {1}, {2})'.format(
            self.name, self.number, self.balance)

    def db_init(self):

        try:
            self.conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='12345678', db='bank')
            self.cur = self.conn.cursor(pymysql.cursors.DictCursor)

        except  Exception:
            print("db conn error")
