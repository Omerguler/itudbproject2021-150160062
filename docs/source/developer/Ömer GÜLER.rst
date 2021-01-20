Parts Implemented by Ömer GÜLER
================================

Added styling
"""""""""""""

Used bootsrap to make our application UI better.


Designed and implemented Request CRUD
"""""""""""""""""""""""""""""""""""""

.. code-block:: python

	def create_cash_requests(self):
	    with dbapi2.connect(self.connection_string) as connection:
	      cursor = connection.cursor()
	      sql_command="CREATE TABLE IF NOT EXISTS CASH_REQUESTS (ID SERIAL PRIMARY KEY,SENDER_NAME VARCHAR(100), RECEIVER_NAME VARCHAR(100),CASH FLOAT,DESCRIPTION VARCHAR(100),FOREIGN KEY (SENDER_NAME) REFERENCES USERS(USER_NAME),FOREIGN KEY (RECEIVER_NAME) REFERENCES USERS(USER_NAME))"
	      cursor.execute(sql_command)
	      connection.commit()
	      cursor.close()
	  def add_cash_request(self,cash_request):
	    with dbapi2.connect(self.connection_string) as connection:
	      cursor = connection.cursor()
	      sql_command="INSERT INTO CASH_REQUESTS (SENDER_NAME,RECEIVER_NAME,CASH,DESCRIPTION) VALUES ( %(sender_name)s, %(receiver_name)s, %(cash)s,%(description)s)"
	      cursor.execute(sql_command,{'sender_name':cash_request.sender_name,'receiver_name':cash_request.receiver_name,'cash':cash_request.cash,'description':cash_request.description})
	      connection.commit()
	      cursor.close()
	  def delete_cash_request(self,cash_request_id):
	    with dbapi2.connect(self.connection_string) as connection:
	      cursor = connection.cursor()
	      sql_command="DELETE FROM CASH_REQUESTS WHERE (ID = %(id)s)"
	      cursor.execute(sql_command,{'id':cash_request_id})
	      connection.commit()
	      cursor.close()
	  def get_cash_requests(self,user_name):
	    request_data = []
	    requests = []
	    with dbapi2.connect(self.connection_string) as connection:
	      cursor = connection.cursor()
	      sql_command="SELECT * FROM CASH_REQUESTS WHERE(SENDER_NAME = %(user_name)s )"
	      cursor.execute(sql_command,{'user_name':user_name})
	      request_data = cursor.fetchall()
	      connection.commit()
	      cursor.close()
	    for i in request_data:
	      requests.append(Cash_Requests(i[0],i[1],i[2],i[3],i[4]))
	    return requests
	  def get_cash_request(self,request_id):
	    request_data = []
	    with dbapi2.connect(self.connection_string) as connection:
	      cursor = connection.cursor()
	      sql_command="SELECT * FROM CASH_REQUESTS WHERE(ID = %(request_id)s )"
	      cursor.execute(sql_command,{'request_id':request_id})
	      request_data = cursor.fetchone()
	      connection.commit()
	      cursor.close()
	    return Cash_Requests(request_data[0],request_data[1],request_data[2],request_data[3],request_data[4])
	  def create_mobyCoin_requests(self):
	    with dbapi2.connect(self.connection_string) as connection:
	      cursor = connection.cursor()
	      sql_command="""CREATE TABLE IF NOT EXISTS MOBYCOIN_REQUESTS 
	      (ID SERIAL PRIMARY KEY,SENDER_NAME VARCHAR(100), RECEIVER_NAME VARCHAR(100),MOBYCOIN FLOAT,DESCRIPTION VARCHAR(100),
	      FOREIGN KEY (SENDER_NAME) REFERENCES USERS(USER_NAME) ON DELETE CASCADE,FOREIGN KEY (RECEIVER_NAME) REFERENCES USERS(USER_NAME) ON DELETE CASCADE)"""
	      cursor.execute(sql_command)
	      connection.commit()
	      cursor.close()
	  def add_mobyCoin_request(self,mobycoin_request):
	    with dbapi2.connect(self.connection_string) as connection:
	      cursor = connection.cursor()
	      sql_command="INSERT INTO MOBYCOIN_REQUESTS (SENDER_NAME,RECEIVER_NAME,MOBYCOIN,DESCRIPTION) VALUES ( %(sender_name)s, %(receiver_name)s, %(mobycoin)s,%(description)s)"
	      cursor.execute(sql_command,{'sender_name':mobycoin_request.sender_name,'receiver_name':mobycoin_request.receiver_name,'mobycoin':mobycoin_request.mobyCoin,'description':mobycoin_request.description})
	      connection.commit()
	      cursor.close()
	  def get_mobyCoin_requests(self,user_name):
	    request_data = []
	    requests = []
	    with dbapi2.connect(self.connection_string) as connection:
	      cursor = connection.cursor()
	      sql_command="SELECT * FROM MOBYCOIN_REQUESTS WHERE(SENDER_NAME = %(user_name)s)"
	      cursor.execute(sql_command,{'user_name':user_name})
	      request_data = cursor.fetchall()
	      connection.commit()
	      cursor.close()
	    for i in request_data:
	      requests.append(MobyCoin_Requests(i[0],i[1],i[2],i[3],i[4]))
	    return requests
	  def get_mobyCoin_request(self,request_id):
	    request_data = []
	    with dbapi2.connect(self.connection_string) as connection:
	      cursor = connection.cursor()
	      sql_command="SELECT * FROM MOBYCOIN_REQUESTS WHERE(ID = %(request_id)s)"
	      cursor.execute(sql_command,{'request_id':request_id})
	      request_data = cursor.fetchone()
	      connection.commit()
	      cursor.close()
	    return MobyCoin_Requests(request_data[0],request_data[1],request_data[2],request_data[3],request_data[4])
	  def delete_mobyCoin_request(self,request_id):
	    with dbapi2.connect(self.connection_string) as connection:
	      cursor = connection.cursor()
	      sql_command="DELETE FROM MOBYCOIN_REQUESTS WHERE (ID = %(id)s)"
	      cursor.execute(sql_command,{'id':request_id})
	      connection.commit()
	      cursor.close()

Sign-up, sign-in, sign-out 
""""""""""""""""""""""""""

Designed and implemented Sign-up, sign-in, sign-out operations

.. code-block:: python

   def create_user(self):
    with dbapi2.connect(self.connection_string) as connection:
      cursor = connection.cursor()
      sql_command="CREATE TABLE IF NOT EXISTS USERS (USER_NAME VARCHAR(100) PRIMARY KEY, PASSWORD VARCHAR(100))"
      cursor.execute(sql_command)
      connection.commit()
      cursor.close()
  def add_user(self,user):
    user.password = hasher.hash(user.password)
    with dbapi2.connect(self.connection_string) as connection:
      cursor = connection.cursor()
      sql_command="INSERT INTO USERS (USER_NAME,PASSWORD) VALUES (%(user_name)s, %(password)s)"
      cursor.execute(sql_command,{'user_name':user.user_name,'password':user.password})
      connection.commit()
      cursor.close()
  def get_hashed_password(self,name):
    with dbapi2.connect(self.connection_string) as connection:
      cursor = connection.cursor()
      sql_command="SELECT PASSWORD FROM USERS WHERE(USER_NAME = %(user_name)s)"
      cursor.execute(sql_command,{'user_name':name})
      hashed_password = cursor.fetchone()
      connection.commit()
      cursor.close()
    return hashed_password
  def verify_user(self,password,hashed_password):
    return(hasher.verify(password,hashed_password))



