Parts Implemented by İbrahim Ethem TÜRKERİ
===========================================

Moby Coin Transaction
"""""""""""""""""""""

Created tables to see latest transactions


.. code-block:: python

	def create_cash_transactions(self):
	    with dbapi2.connect(self.connection_string) as connection:
	      cursor = connection.cursor()
	      sql_command="CREATE TABLE IF NOT EXISTS CASH_TRANSACTION (ID SERIAL PRIMARY KEY,SENDER_NAME VARCHAR(100), RECEIVER_NAME VARCHAR(100),CASH FLOAT,FOREIGN KEY (SENDER_NAME) REFERENCES USERS(USER_NAME),FOREIGN KEY (RECEIVER_NAME) REFERENCES USERS(USER_NAME))"
	      cursor.execute(sql_command)
	      connection.commit()
	      cursor.close()
	  def add_cash_transaction(self,cash_transaction):
	    with dbapi2.connect(self.connection_string) as connection:
	      cursor = connection.cursor()
	      sql_command="INSERT INTO CASH_TRANSACTION (SENDER_NAME,RECEIVER_NAME,CASH) VALUES ( %(sender_name)s, %(receiver_name)s, %(cash)s)"
	      cursor.execute(sql_command,{'sender_name':cash_transaction.sender_name,'receiver_name':cash_transaction.receiver_name,'cash':cash_transaction.cash})
	      connection.commit()
	      cursor.close()
	  def get_cash_transactions(self,user_name):
	    transaction_data = []
	    transactions = []
	    with dbapi2.connect(self.connection_string) as connection:
	      cursor = connection.cursor()
	      sql_command="SELECT * FROM CASH_TRANSACTION WHERE(SENDER_NAME = %(user_name)s OR RECEIVER_NAME = %(user_name)s)"
	      cursor.execute(sql_command,{'user_name':user_name})
	      transaction_data = cursor.fetchall()
	      connection.commit()
	      cursor.close()
	    for i in transaction_data:
	      transactions.append(Cash_Transactions(i[0],i[1],i[2],i[3]))
	    return transactions
	  def create_mobyCoin_transactions(self):
	    with dbapi2.connect(self.connection_string) as connection:
	      cursor = connection.cursor()
	      sql_command="""CREATE TABLE IF NOT EXISTS MOBYCOIN_TRANSACTION 
	      (ID SERIAL PRIMARY KEY,SENDER_NAME VARCHAR(100), RECEIVER_NAME VARCHAR(100),MOBYCOIN FLOAT,
	      FOREIGN KEY (SENDER_NAME) REFERENCES USERS(USER_NAME) ON DELETE CASCADE,FOREIGN KEY (RECEIVER_NAME) REFERENCES USERS(USER_NAME) ON DELETE CASCADE)"""
	      cursor.execute(sql_command)
	      connection.commit()
	      cursor.close()
	  def add_mobyCoin_transaction(self,mobycoin_transaction):
	    with dbapi2.connect(self.connection_string) as connection:
	      cursor = connection.cursor()
	      sql_command="INSERT INTO MOBYCOIN_TRANSACTION (SENDER_NAME,RECEIVER_NAME,MOBYCOIN) VALUES ( %(sender_name)s, %(receiver_name)s, %(mobycoin)s)"
	      cursor.execute(sql_command,{'sender_name':mobycoin_transaction.sender_name,'receiver_name':mobycoin_transaction.receiver_name,'mobycoin':mobycoin_transaction.mobyCoin})
	      connection.commit()
	      cursor.close()
	  def get_mobyCoin_transactions(self,user_name):
	    transaction_data = []
	    transactions = []
	    with dbapi2.connect(self.connection_string) as connection:
	      cursor = connection.cursor()
	      sql_command="SELECT * FROM MOBYCOIN_TRANSACTION WHERE(SENDER_NAME = %(user_name)s OR RECEIVER_NAME = %(user_name)s)"
	      cursor.execute(sql_command,{'user_name':user_name})
	      transaction_data = cursor.fetchall()
	      connection.commit()
	      cursor.close()
	    for i in transaction_data:
	      transactions.append(MobyCoin_Transactions(i[0],i[1],i[2],i[3]))
	    return transactionsd

Added buying cash
"""""""""""""""""

Users can exchange between currencies


Added Salary Payment
""""""""""""""""""""

.. code-block:: python

	def salary_payment_cash(self,balance_src,balance_dst,cash):
	    balance_src.cash -= cash
	    balance_dst.cash += cash
	    self.update_balance(balance_src)
	    self.update_balance(balance_dst)
	  def salary_payment_mobyCoin(self,balance_src,balance_dst,mobyCoin):
	    balance_src.mobyCoin -= mobyCoin
	    balance_dst.mobyCoin += mobyCoin
	    self.update_balance(balance_src)
	    self.update_balance(balance_dst)
	  def buy_mobycoin(self,balance,cash):
	    if(cash>balance.cash):
	      return False
	    added_coin = cash / 10
	    balance.mobyCoin += added_coin
	    balance.cash -= cash
	    self.update_balance(balance)
	    return True
	  def buy_cash(self,balance,cash_amount):
	    balance.cash += cash_amount
	    self.update_balance(balance)
	  def sell_mobycoin(self,balance,mobycoin):
	    if(mobycoin>balance.mobyCoin):
	      return False
	    added_cash = mobycoin*10
	    balance.mobyCoin -= mobycoin
	    balance.cash += added_cash
	    self.update_balance(balance)
	    return True


