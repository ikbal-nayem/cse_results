from db_operation import database, table
from flask import jsonify
from adminPanel import admin
from multiprocessing import Process
import calculator
import os

class backend:
    def __init__(self):
        self.db = database()
        self.table = table()
   

    def txt2list(self, file):
        '''This function read .txt file of result sheet and return a list of each lines information'''

        with open(file, 'r') as f:
	        li = f.readlines()
        info = []
        for i, l in enumerate(li):
            if l[0] == '|':
                l = l.strip().split('|')
                l.pop(0)
                l.pop(-1)
                for i in range(int(len(l))):
                    l[i] = l[i].strip()
                if l[0] != 'ROLL NO':
                    info.append(l)
        return info


    def create_tables_in_database(self):
        '''This mathod will pass 2 lists to database operetion class to create all tables into the database'''

        file1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/course_files/courselist1.txt')          #put the .txt files location of course
        file2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/course_files/courselist2.txt')          #put the .txt files location of course
        courseList1 = []
        courseList2 = []
        with open(file1, 'r') as f1:
            courses1 = f1.readlines()
        with open(file2, 'r') as f2:
            courses2 = f2.readlines()
        for course in courses1:
            co = course.split('|')
            for i, c in enumerate(co):
                co[i] = c.strip()
            if len(co)>1:
                courseList1.append(co)
        for course in courses2:
            co = course.split('|')
            for i, c in enumerate(co):
                co[i] = c.strip()
            if len(co)>1:
                courseList2.append(co)
        return self.table.create_tables(courseList1, courseList2)
    

    def upload_results(self, filename, semester, year, user):
        '''This will take result (.txt) file and pass to the student_info and result table'''

        file = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'upload'), filename)
        li = self.txt2list(file)
        for l in li:
            reg_no, _, session, name, res = l[1], l[0], l[2], l[3], l[4:]
            batch = int(session[2:4])-8
            self.db.insert_student(reg_no, name, batch, session)
            self.db.insert_result(reg_no, semester, res, year, session)
        try:
            os.remove(file)
            admin().post_log({'admin': user, 'session': session, 'semester': semester, 'year': year})
            self.send_mail(semester, year)
        except Exception:
            pass
    
    def send_mail(self, semester, year):
        from service import mail
        email = mail()
        process = Process(target=email.send, args=(semester, year))
        process.start()

    def generate_API(self, reg_no, semester):
        '''This function will generate a json API for template and requested clients'''
        
        info = self.db.show_info(reg_no)
        if info == None:
            return {'exception': 'student_not_found', 'registration': reg_no, 'name': '', 'batch': '', 'session': '', 'semester': '','result': '','cgpa': '',}
        courses = list([list(course) for course in self.db.show_courses(semester, info[3])])
        credit = [cr[2] for cr in courses]
        res = self.db.show_result(reg_no, semester, info[3])
        if res:
            list(res)
            exception = "result_found"
        else:
            exception = "result_not_published_yet"
            return {'exception': exception,'registration': info[0],'name': info[1],'batch': info[2],'session': info[3],'semester': semester,'courses': courses,'grades': None,'result': None,'cgpa': None,'exam year': None,}
        grades = {}
        cgpa = calculator.cgpa(res[:-1], credit)
        if cgpa=='Fail':
            result = 'Failed'.upper()
            cgpa = 0
        else:
            result='Passed'.upper()
        for i, v in enumerate([code[0] for code in courses]):
            grades[v]=res[i]
        json = {
            'exception': exception,
            'registration': info[0],
            'name': info[1],
            'batch': info[2],
            'session': info[3],
            'semester': semester,
            'courses': courses,
            'grades': grades,
            'result': result,
            'cgpa': cgpa,
            'exam year': res[-1],
        }
        self.db.conn_close()
        return json

