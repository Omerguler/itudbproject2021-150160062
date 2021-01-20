Parts Implemented by Eray FELEK
================================

Balance Table
"""""""""""""

Every user require a balance table to keep track of their current cash and coin balance.

Balance CRUD
"""""""""""""

Implementation of balance CRUD operations

.. code-block:: python

      class Balance:
         def __init__(self, Id,User_name, Cash=0, MobyCoin=0):
	  	self.id = Id
	    	self.user_name = User_name
	    	self.cash = Cash
	    	self.mobyCoin = MobyCoin

	def create_balance(self):
	    with dbapi2.connect(self.connection_string) as connection:
	      cursor = connection.cursor()
	      sql_command="CREATE TABLE IF NOT EXISTS BALANCE (ID SERIAL PRIMARY KEY, USER_NAME VARCHAR(100) REFERENCES USERS(USER_NAME),CASH FLOAT, MOBYCOIN FLOAT)"
	      cursor.execute(sql_command)
	      connection.commit()
	      cursor.close()
	  def get_balance(self,user_name):
	    balance_data = []
	    with dbapi2.connect(self.connection_string) as connection:
	      cursor = connection.cursor()
	      sql_command="SELECT * FROM BALANCE WHERE(USER_NAME = %(user_name)s)"
	      cursor.execute(sql_command,{'user_name':user_name})
	      balance_data = cursor.fetchone()
	      connection.commit()
	      cursor.close()
	    return Balance(balance_data[0],balance_data[1],balance_data[2],balance_data[3])
	  def add_balance(self,balance):
	    with dbapi2.connect(self.connection_string) as connection:
	      cursor = connection.cursor()
	      sql_command="INSERT INTO BALANCE (USER_NAME,CASH,MOBYCOIN) VALUES ( %(user_name)s, %(cash)s, %(mobycoin)s)"
	      cursor.execute(sql_command,{'user_name':balance.user_name,'cash':balance.cash,'mobycoin':balance.mobyCoin})
	      connection.commit()
	      cursor.close()
	  def delete_balance(self,balance_id):
	    with dbapi2.connect(self.connection_string) as connection:
	      cursor = connection.cursor()
	      sql_command="DELETE FROM BALANCE WHERE (ID = %(id)s)"
	      cursor.execute(sql_command,{'id':balance_id})
	      connection.commit()
	      cursor.close()
	  def update_balance(self,balance):
	    with dbapi2.connect(self.connection_string) as connection:
	      cursor = connection.cursor()
	      sql_command="UPDATE BALANCE SET CASH = %(cash)s,MOBYCOIN = %(mobycoin)s WHERE (ID = %(id)s)"
	      cursor.execute(sql_command,{'cash':balance.cash,'mobycoin':balance.mobyCoin,'id':balance.id})
	      connection.commit()
	      cursor.close()

Cash and MobyCoin Transfer
""""""""""""""""""""""""""
Users can transfer their cash or MobyCoin to other users

.. code-block:: python

  def transfer_between_users_cash(self,balance_src,balance_dst,cash):
    if(cash>balance_src.cash):
      return False
    balance_src.cash -= cash
    balance_dst.cash += cash
    self.update_balance(balance_src)
    self.update_balance(balance_dst)
    return True
  def transfer_between_users_mobycoin(self,balance_src,balance_dst,mobycoin):
    if(mobycoin>balance_src.mobyCoin):
      return False
    balance_src.mobyCoin -= mobycoin
    balance_dst.mobyCoin += mobycoin
    self.update_balance(balance_src)
    self.update_balance(balance_dst)
    return True



Seperated files
""""""""""""""""""""""""""

Constructed views.py



