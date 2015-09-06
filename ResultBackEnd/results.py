import re
import mechanize
from BeautifulSoup import BeautifulSoup

class student:

	def __init__(self) :
		self.HTMLtoPrint=""
		self.stuName=""
		self.stuSem=""
		self.stuMarks=[]

	def get_name(self):
	    return self.stuName

	def remove_html_tags(self,data):
	    p = re.compile(r'<.*?>')
	    return p.sub('', data)

	#Connect to the server
	def connectToVtu(self,usn):
		br = mechanize.Browser()
		print "Connecting...\n"
		while True:
			try:
				br.open("http://results.vtu.ac.in")
				br.select_form(name="new")
				br["rid"]=usn
				response =br.submit()

				print "Waiting for response...\n"
				data=response.get_data()
				break
			except:
				print "Timed out. Retrying\n"

		if not re.search("Results are not yet available for this university seat",data) == None:
			return None
		#print data #website data with HTML tags
		return BeautifulSoup( data ) #back to crawler.py with Soup object!

	def extractResults(self, soup): #takes Soup object and ...
		print "Generating Output...\n"

		table = soup.findAll('table', width="515") # BS method returns all table data

		tableText = table[0].prettify() #prettify?
		self.HTMLtoPrint = tableText
		tableSoup = BeautifulSoup( tableText )

		bRows=tableSoup.findAll('b')

		#Remove last two (as they are not nessesary)
		bRows.pop()
		bRows.pop()

		self.stuName=self.remove_html_tags(bRows[0].text)
		print self.stuName + "\n"

		self.stuSem=self.remove_html_tags(bRows[2].text)

		stuSubjects=tableSoup.findAll('i')

		marksTemp=tableSoup.findAll('td', width='60')

		#remove the extra (the table headings)

		for i in range(4):
		  marksTemp.pop(0)


		#Get the subjects
		for i in range(len(stuSubjects)-1):
		  stuSubjects[i]=self.remove_html_tags(stuSubjects[i].text)


		#self.stuMarks is a list of lists with all the details[[sub,ext,int,tot,res],....]
		self.stuMarks=[]

		for i in range(len(stuSubjects)):
		   subSet=[]
		   subSet.append(stuSubjects[i])
		#    i=i*3
		   for j in range(4):
		      subSet.append(self.remove_html_tags(marksTemp.pop(0).text))
		    #   i=i+1
		   #! This part is funky :\
		   subSet[0]=self.remove_html_tags(str(subSet[0]))
		   p = re.compile(r'\n*       *')
		   subSet[0]=p.sub('',subSet[0])
		   #! End of funkyness
		   self.stuMarks.append(subSet)
		   # print stuMarks
		   #print subSet #final data that is written!

		#    subjects_vtu = []
		#    marks_ext = []
		#    marks_int = []
		#
		#    for i in range(0,len(self.stuMarks)):
		# 	  #print "Subject \n"
		# 	  subjects_vtu.append(self.stuMarks[i][0])
		# 	  #print "Marks \n"
		# 	  marks_ext.append(self.stuMarks[i][1])
		# 	  marks_int.append(self.stuMarks[i][2])
		#
		# print "Subjects \n"
		# print '[%s]' % ', '.join(map(str, subjects_vtu))
		# print "\n"
		#
		# print "External Marks"
		# print '[%s]' % ', '.join(map(str, marks_ext))
		# print "\n"
		#
		# print "Internal Marks"
		# print '[%s]' % ', '.join(map(str, marks_int))
		# print "\n"
		return (self.stuMarks,self.stuName)
