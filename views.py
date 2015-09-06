from ResultBackEnd import resultlogic, USNValidate
from flask import Flask, request, flash, url_for, redirect, render_template, abort
import json

app=Flask(__name__)
app.config.from_pyfile('AppConfig.cfg')
app.config['PROPAGATE_EXCEPTIONS'] = True

@app.route('/result',methods=['GET', 'POST'])
def result():
    return render_template('result.html')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        U = request.form['USN']
        u1 = USNValidate.USN(U)
        if u1.isValidUSN() == False:
            error = u1.getErrors()
            flash (error)
        else:
            marks,usn_name = resultlogic.get_result(U)
            sub=marks[0]
            subjects_vtu = []
            marks_ext = []
            marks_int = []
            total_sub = []
            for i in range(0,len(marks)):
                #print "Subject \n"
                subjects_vtu.append(marks[i][0])
                #print "Marks \n"
                marks_ext.append(int(marks[i][1]))
                marks_int.append(int(marks[i][2]))
                total_sub.append(marks_int[i]+marks_ext[i])
            int_sum_per = (sum(x for x in marks_int))
            ext_sum_per = (sum(x for x in marks_ext))
            # usn_name= "namehere"
            usn_college=u1.college
            usn_reg= u1.region
            usn_branch=u1.stream
            return render_template('result.html',name=usn_name,college=usn_college,region=usn_reg,branch=usn_branch,n=range(len(marks)), sub=subjects_vtu,extr=marks_ext,intr=marks_int,extpr=ext_sum_per,intpr=int_sum_per,tot=total_sub)
    return render_template('main.html', error=error)

if __name__ == "__main__":
    app.run()
