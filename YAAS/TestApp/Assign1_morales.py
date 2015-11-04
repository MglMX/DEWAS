__author__ = 'Miguel Morales'
import re
from datetime import datetime, timedelta

class AverageCalc:
    def __init__(self, list):
        self.list=list
        self.answers = {'a': 'Low average','b' : 'Medium average','c':'High average'}

    @classmethod
    def initWithString(cls,string):
        list=re.findall("\d+",string)
        return cls(list)

    def average(self):
        total=0
        for n in self.list:
            total += int(n)
        average = total/len(self.list)

        if(average<6):
            print self.answers['a']
        elif(average<12):
            print self.answers['b']
        else:
            print self.answers['c']

calc = AverageCalc([33,4,0,1,3])
calc2 = AverageCalc([1,2,3,4,5])
calc.average()
calc2.average()

calc3 = AverageCalc.initWithString("l33t h4x0r 1s pwn3d")
calc4 = AverageCalc.initWithString("H3ll0 3v3ry 0n3 11!!")
calc3.average()
calc4.average()


#############################

def articlePrinter(folder):
    result = re.search("\w+/(?P<date>\d+/\d+/\d+)/(?P<name>.+)",folder)
    name = str(result.group("name"))
    sDate = str(result.group("date"))
    date = datetime.strptime(sDate,"%Y/%m/%d")
    days = str((datetime.now()-date).days)
    print "('"+name + "','" + sDate + "'," + days + ")"


def check(date):
    date= datetime.strptime(date,"%d.%m.%Y_%H:%M")
    print str((date-datetime.now()).seconds)
    if (date-datetime.now()).days > 3:
        print "More than 3 days woohoo: "

    print "days: "+str((date-datetime.now()).days)


articlePrinter("articles/2010/10/21/my_summer")
articlePrinter("articles/2015/09/12/winter_photos")

check("07.11.2015_18:33")






