# from flask_mysqldb import MySQL
import pymysql

class database:
	def __init__(self):
		# self.mysql = pymysql.connect(host='sql12.freesqldatabase.com', db='sql12284684', user='sql12284684', passwd='g4smdBelKh')
		self.mysql = pymysql.connect(host='localhost', db='test', user='iku', passwd='welcome')
		self.c = self.mysql.cursor()
	

	def admin(self, email):
		self.c.execute("select password from admin where email='{}'".format(email))
		passwd = self.c.fetchall()
		return passwd[0][0] if passwd else False
	

	def show_info(self, reg_no, *argv):
		'''To select student information'''

		if argv:
			q = "select "+','.join(argv)+" from student_info where reg_no='{}'".format(reg_no)
		else:
			q = "select * from student_info where reg_no='{}'".format(reg_no)
		self.c.execute(q)
		try:
			return list(self.c.fetchall()[0])
		except:
			return None


	def show_courses(self, semester, session, *argv):
		''' To select courses list for a session '''

		if int(session[2:4]) >= 17:
			course = 'course_new'
		else:
			course = 'course'
		if argv:
			q = "select "+','.join(argv)+" from {} where semester='{}' order by code".format(course, semester)
		else:
			q = "select code, subjects, credit from {} where semester='{}' order by code".format(course, semester)
		self.c.execute(q)
		return self.c.fetchall()

	def show_result(self, reg_no, semester, session):
		code = self.show_courses(semester, session, 'code')
		codes = [ele[0] for ele in code]
		q = "select "+','.join(codes)+", year from {}_semester where reg_no='{}'".format(semester, reg_no)
		self.c.execute(q)
		res = self.c.fetchall()
		if res:
			return self.c.fetchall()[0]
		return None


	def insert_student(self, reg_no, name, batch, session):
		'''This function will add a new student information to student_info table if not exists'''

		self.c.execute('select reg_no from student_info where reg_no="{}"'.format(str(reg_no)))
		if not self.c.fetchall():
			q = "insert into student_info values('{}','{}',{},'{}')".format(str(reg_no), str(name), int(batch), str(session))
			self.c.execute(q)
			self.mysql.commit()
			print(q)


	def insert_result(self, reg_no, semester, res_list, year, session):
		'''This will check each results if they are updated or not for each student if not it will update or insert into result table'''

		if int(session[2:4]) >= 17:
			self.c.execute("select code from course_new where semester='{}' order by code".format(str(semester)))
		else:
			self.c.execute("select code from course where semester='{}' order by code".format(str(semester)))
		cList = [l[0] for l in self.c.fetchall()]
		self.c.execute("select year from {}_semester where reg_no='{}'".format(str(semester), str(reg_no)))
		check = self.c.fetchall()
		if not check:
			print("New result found -> {}".format(reg_no))
			q = "insert into {}_semester( reg_no, year, ".format(semester)+','.join(cList)+" ) values ( '{}', '{}', \'".format(reg_no, year)+"\', \'".join(res_list)+"\' )"
		elif int(check[0][0]) < int(year):
			print("An old result found -> {}".format(reg_no))
			self.c.execute("delete from {}_semester where reg_no='{}'".format(semester, reg_no))
			q = "insert into {}_semester( reg_no, year, ".format(semester)+','.join(cList)+" ) values ( '{}', '{}', \'".format(reg_no, year)+"\', \'".join(res_list)+"\' )"
		else:
			print("Updated result already exiset -> {}".format(reg_no))
			return "exiset"
		self.c.execute(q)
		self.mysql.commit()

	

class table:
	'''Creating all tables and upload all information into course table'''

	def __init__(self):
		self.mysql = pymysql.connect(host='localhost', db='test', user='iku', passwd='welcome')
		self.c = self.mysql.cursor()

	def create_tables(self, clist1, clist2):
		'''This method will take 2 course list ( old and new) and create all requres tables for the database'''

		course1 = 'create table course(code varchar(10) primary key, subjects varchar(50), credit float, semester varchar(4))'
		course2 = 'create table course_new(code varchar(10) primary key, subjects varchar(50), credit float, semester varchar(4))'
		student_info = 'create table student_info(reg_no varchar(12) primary key, name varchar(40), batch int(2), session varchar(7))'
		self.c.execute(course1)
		self.c.execute(course2)
		print('course table ready..')
		print('uploading into course table...', end=' ')
		self.insert_course(clist1, clist2)
		print("done")
		print("creating student_info..")
		self.c.execute(student_info)
		self.mysql.commit()
		print('creating semester tables...')
		self.create_semester_table()
		print('done')
		self.mysql.commit()

	def create_semester_table(self):
		'''create all tables for 8 semesters'''

		semeList = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th']
		for seme in semeList:
			courseList = '(select code from course where semester="{}") union (select code from course_new where semester="{}")'.format(seme,seme)
			self.c.execute(courseList)
			courseList = [l[0] for l in self.c.fetchall()]
			q = "create table {}_semester(reg_no varchar(12) primary key, ".format(seme)+' varchar(2), '.join(courseList)+" varchar(2), year varchar(4))"
			self.c.execute(q)
			print('created {} semester.'.format(seme))
		self.mysql.commit()

	def insert_course(self, clist1, clist2):
		'''insert valuse into course tables'''

		for li in clist1:
			q = "insert into course values('{}', '{}', {}, '{}')".format(li[0], li[1], float(li[2]), li[3])
			self.c.execute(q)
		for li in clist2:
			q = "insert into course_new values('{}', '{}', {}, '{}')".format(li[0], li[1], float(li[2]), li[3])
			self.c.execute(q)
		self.mysql.commit()



# database().show_result('16502000664', '4th', '2016-17')
# s = database().show_courses('3rd')
# i = database().show_info('16502000667')
# database().insert_student('16502000663', 'iku', 8, 'zzf')
# database().insert_result('1st', '2017-18')
# print(s)
# print(g)
# print(i)