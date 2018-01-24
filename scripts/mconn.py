from time import sleep
import mysql.connector
import os

class Mconn:
	'This class defines connectivity with the database to operate on the demands'

	def __init__(self, ip):
		self.ip = ip
		#s = self.login()
		self.cnx =""
		self.login(self.ip)


	def login(self, ip):
		while 1==1:
			login = ""
			passw = ""
			print "login processing.."

			#check whether file exists
			if os.path.isfile('snortdbcred'):
				file = open("snortdbcred", "r")
				login = file.readline()
				login = login.strip()

				passw = file.readline()
				passw = passw.strip()

				dbname = file.readline()
				dbname = dbname.strip()


				#print passw+"."+login
			else:
				print "You can create the file \"snortdbcred\" in the upper folder and put the login and password seperated by new line character"
				login = raw_input("Enter login:\n")
				passw = raw_input("Enter password:\n")

			#connection:
			try:
				self.cnx = mysql.connector.connect(user=login, password=passw,
                              host=ip,
                              database=dbname)
				if self.cnx:
					print "connected"
				#self.cnx.close()

				return True
			except mysql.connector.Error as err:
			  	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			  		print "Something is wrong with your user name or password"
			  	elif err.errno == errorcode.ER_BAD_DB_ERROR:
			  		print "Database does not exist"
			  	else:
			  		print(err)

					return False
			
	def shAggressor(self):
		self.login(self.ip)

		#uzywamy kursora do pobierania danych bazy
		cursor = self.cnx.cursor()
		query = ("select inet_ntoa(ip_src) as \"SRC\",count(*) as \"count\"from iphdr group by ip_src limit 5;")
		cursor.execute(query)

		#przygotuje zmienne aggrIp oraz aggrcount odpowiadajace odpowiednio za adres IP aresora oraz liczbe pakietow,
		# nastepnie listy te bede przypisywal jako wartosci do konkretnych atrybutow slownika dictMan

		aggrIp = []
		aggrCount = []
		dictMan = {
			"aggressorIP":aggrIp,
			"aggrCount":aggrCount,
			}
		for (SRC, COUNT) in cursor:
			#print SRC," wywalil juz ",COUNT," alarmow."
			dictMan['aggressorIP'].append(SRC)
			dictMan['aggrCount'].append(COUNT)

		#print dictMan
		self.closecnx()

		return dictMan

	def closecnx(self):
		#print "INFO:Connection closed"
		cursor = self.cnx.cursor()
