import re
import results
import sys

def get_result(post_USN):
    vtuStudent = results.student() #make object of class Student
    usn = post_USN
    data = vtuStudent.connectToVtu(usn) #call the function with USN!! returns SOUP Object ***IMPORTANT PART***
    if data == None:
		return "Results not announced/USN does'nt exsist"
    else:
        marks,nameofusn = vtuStudent.extractResults(data) #call function with SOUP Object
        # subjects_vtu = []
        # marks_ext = []
        # marks_int = []
        # for i in range(0,len(marks)):
        #     #print "Subject \n"
        #     subjects_vtu.append(marks[i][0])
        #     #print "Marks \n"
        #     marks_ext.append(marks[i][1])
        #     marks_int.append(marks[i][2])
        return (marks,nameofusn)


def get_total(sem):
    if sem == 8:
        return 750
    elif sem == 1 or 2:
        return 775
    else:
        return 900
# main()
