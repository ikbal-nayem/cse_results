import pymysql, json
from conf import db_info

class database:
	def __init__(self):
		self.mysql = pymysql.connect(host=db_info.HOST, db=db_info.DATABASE, user=db_info.USER, passwd=db_info.PASSWORD)
		self.c = self.mysql.cursor()
	
	def conn_close(self):
		self.mysql.commit()
		self.mysql.close()
	
	def add_email(self, reg_no, email):
		q1 = "select reg_no from student_info where email='{}'".format(email)
		self.c.execute(q1)
		if len(self.c.fetchall()) == 0:
			q2 = "update student_info set email='{}' where reg_no='{}'".format(email, reg_no)
			self.c.execute(q2)
			self.conn_close()
			return True
		else:
			self.conn_close()
			return False
	
	def find_email(self, semester, year):
		q = """select si.reg_no, email 
			from student_info as si, {}_semester as 3s 
			where si.reg_no=3s.reg_no and year='{}' 
			and email is not NULL""".format(semester, year)
		self.c.execute(q)
		address = [list(e) for e in self.c.fetchall()]
		self.conn_close()
		return address

	def find_name(self, batch):
		conn = self.mysql.cursor()
		q = "select name from student_info where batch='{}'".format(batch)
		conn.execute(q)
		names = [name[0] for name in conn.fetchall()]
		self.mysql.close()
		return names if len(names)!=0 else False

	def find_regi(self, batch, name=None):
		conn = self.mysql.cursor()
		if name:
			q = "select reg_no from student_info where batch={} and name='{}'".format(batch, name)
			conn.execute(q)
			reg = conn.fetchall()[0][0]
		else:
			q = "select reg_no from student_info where batch={}".format(int(batch))
			conn.execute(q)
			reg = [l[0] for l in conn.fetchall()]
		# self.mysql.close()
		return reg

	def show_info(self, reg_no, *argv):
		'''To select student information'''

		conn = self.mysql.cursor()
		if argv:
			q = "select "+','.join(argv)+" from student_info where reg_no='{}'".format(reg_no)
		else:
			q = "select * from student_info where reg_no='{}'".format(reg_no)
		conn.execute(q)
		try:
			return list(conn.fetchall()[0])
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
		try:
			code = self.show_courses(semester, session, 'code')
			codes = [ele[0] for ele in code]
			q = "select "+','.join(codes)+", year from {}_semester where reg_no='{}'".format(semester, reg_no)
			self.c.execute(q)
			res = self.c.fetchall()
			return res[0] if res else None
		except:
			self.conn_close()
			return False


	def insert_student(self, reg_no, name, batch, session):
		'''This function will add a new student information to student_info table if not exists'''

		conn = self.mysql.cursor()
		conn.execute("select reg_no from student_info where reg_no='{}'".format(str(reg_no)))
		if not conn.fetchall():
			q = "insert into student_info values('{}','{}',{},'{}')".format(str(reg_no), str(name), int(batch), str(session))
			conn.execute(q)
			self.mysql.commit()
			print(q)


	def insert_result(self, reg_no, semester, res_list, year, session):
		'''This will check each results if they are updated or not for each student if not it will update or insert into result table'''

		conn = self.mysql.cursor()
		if int(session[2:4]) >= 17:
			conn.execute("select code from course_new where semester='{}' order by code".format(str(semester)))
		else:
			conn.execute("select code from course where semester='{}' order by code".format(str(semester)))
		cList = [l[0] for l in conn.fetchall()]
		conn.execute("select year from {}_semester where reg_no='{}'".format(str(semester), str(reg_no)))
		check = conn.fetchall()
		if not check:
			print("New result found for -> {}".format(reg_no))
			q = "insert into {}_semester( reg_no, year, ".format(semester)+','.join(cList)+" ) values ( '{}', '{}', \'".format(reg_no, year)+"\', \'".join(res_list)+"\' )"
		elif int(check[0][0]) < int(year):
			print("An old result found -> {}".format(reg_no))
			conn.execute("delete from {}_semester where reg_no='{}'".format(semester, reg_no))
			q = "insert into {}_semester( reg_no, year, ".format(semester)+','.join(cList)+" ) values ( '{}', '{}', \'".format(reg_no, year)+"\', \'".join(res_list)+"\' )"
		else:
			print("Updated result already exiset -> {}".format(reg_no))
			return "exiset"
		conn.execute(q)
		self.mysql.commit()

###										grab results by scrapping

	def insertByScrapping(self, semester, reg, year, course_list, res_list):
		conn = self.mysql.cursor()
		conn.execute("select year from {}_semester where reg_no='{}'".format(semester, reg))
		previous_year = conn.fetchall()
		if not previous_year:
			print(f'New result for -> {reg}')
			conn.execute("insert into {}_semester(reg_no, year, {}) values('{}', '{}', '{}')".format(semester, ', '.join(course_list), reg, year, "\', \'".join(res_list)))
		elif int(previous_year[0][0]) < int(year):
			new = [f"{course}='{res_list[i]}'" for i, course in enumerate(course_list)]
			print(f'Updating result for -> {reg}')
			conn.execute("update {}_semester set {} where reg_no='{}'".format(semester, ', '.join(new), reg))
		self.mysql.commit()


class table(database):
	'''Creating all tables and upload all information into course table'''

	def create_tables(self, clist1, clist2):
		'''This method will take 2 course list ( old and new) and create all requres tables for the database'''

		try:
			course1 = 'create table course(code varchar(10) primary key, subjects varchar(50), credit float, semester varchar(4))'
			course2 = 'create table course_new(code varchar(10) primary key, subjects varchar(50), credit float, semester varchar(4))'
			student_info = 'create table student_info(reg_no varchar(12) primary key, name varchar(50), batch int(2), session varchar(10))'
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
			self.mysql.close()
			return dict(exception=True)
		except Exception:
			pass
			# return dict(exception=str(json.loads(e.args[0])))

	def create_semester_table(self):
		'''create all tables for 8 semesters'''

		semeList = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th']
		for seme in semeList:
			courseList = "(select code from course where semester='{}') union (select code from course_new where semester='{}')".format(seme,seme)
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

