import urllib.request as req
from bs4 import BeautifulSoup as soup
import math, datetime, time, logging
import easy_sqlite as lite

class_blocks = [
    "02-block-e",
    "01-block-d"
    ]

def mean(array):
    avg = sum(array) / len(array)
    return avg
def median(array):
    o = list(reversed(sorted(array)))
    mod = len(o) % 2
    #print(mod)
    if mod:
        return o[math.floor(len(o) / 2) + 1]
    else:
        return (o[math.floor(len(o) / 2) - 1] + o[(math.floor(len(o) / 2))]) / 2

def get_student_marks(block):
    res = req.urlopen("http://mrjtaylor.weebly.com/mpm-1dw---%s.html" % block)
    res = res.read()
    tree = soup(res,"html.parser")
    g1 = []
    for i in tree.findAll("tr"):
        g = i.find("td")
        if g != None:
            g1.append(g)
    # refin for names
    g2 = []
    for i in g1:
        g = i.find("font")
        if g != None:
            g2.append(g)
    names = []
    begin = False
    for name in g2:
        t = name.text
        if t == "EntryNumber":
            begin = False
        if begin:
            names.append(t)
        if t == "Code Name":
            begin = True
    # refine for marks
    m1 = []
    for i in tree.findAll("tr"):
        g = i.find("b")
        if g != None:
            m1.append(g)
    marks = []
    cont = False
    for mark in m1:
        t = mark.text
        if t == "EntryNumber":
            cont = False
        if cont:
            marks.append(int(t))
        if t == "Code Name":
            cont = True
    
    re = {}
    for name in names:
        #we're hoping there are no identical names...
        re[name] = marks[names.index(name)]
    ##print(re)
    return re
#now database stuff
def enter_marks(dbname,markz,block):
    # we're assuming the <markz> variable will be in the format given by the get_student_marks function.
    db = lite.database(dbname)
    start_time = time.time()
    if db.get_tables().__contains__("marks_" + str(datetime.datetime.now().year) + "_block_" + block):
        table = db.__getattribute__("marks_" + str(datetime.datetime.now().year) + "_block_" + block)
        for i in markz:
            table.entry([start_time,i,markz[i]])
    else:
        raise Exception("Database is missing the correct tables! Try our calibrate_database function")
def calibrate_database(dbname,block):
    db = lite.database(dbname)
    ##print("calibrating : [%s]..." % ("marks_" + str(datetime.datetime.now().year) + "_block_" + block))
    db.create_table("marks_" + str(datetime.datetime.now().year) + "_block_" + block,[["Timestamp",123.12315],["Name","aiyshgdiauhsd"],["Mark",74.342]])
def update_data(block):
    # block e is my class
    markzz = get_student_marks(block)
    enter_marks("marks.db",markzz,block[-1])
def serve():
    global class_blocks
    logging.basicConfig(filename="math_grade_server_logs.log",level="DEBUG")
    # 1 = seconds, 60 = minute, 60 = hour, 24 = day, 7 = week
    wait = 1 * 60 * 60 * 24
    serving = True
    for block in class_blocks:
        calibrate_database("marks.db",block[-1])
    while serving:
        logging.log(logging.INFO,"-------------------------------------------------------")
        logging.log(logging.INFO,"        SERVER HAS BEGUN UPDATING DATABASE")
        logging.log(logging.INFO,"Time: " + str(time.time()))
        for block in class_blocks:
            logging.log(logging.INFO,"Updating block: %s...." % block)
            ##try:
            if 1:
                update_data(block)
            ##except:
            ##    logging.log(logging.CRITICAL,"***HIT ERROR WHILE UPDATING***")
        logging.log(logging.INFO,"      SERVER HAS FINISHED UDPATING ITS DATABASE")
        logging.log(logging.INFO,"Beginning to sleep for %s days (seconds: %s)" % ((wait/24/60/60),wait))
        time.sleep(wait)
if __name__ == '__main__':
    serve()
