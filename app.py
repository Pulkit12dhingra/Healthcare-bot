from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
from collections import Counter
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def space_seperated(s1,s2):
    c=0
    if (len(s2)<len(s1)):
        for i in s2:
            for j in s1:            
                if i==j:
                    c+=1
        if c==len(s2):
            return 1
        else:
            return 0
    else:
        for i in s1:
            for j in s2:            
                if i==j:
                    c+=1
        if c==len(s1):
            return 1
        else:
            return 0

def Most_Common(lst):
    data = Counter(lst)
    return data.most_common(1)[0][0]


@app.route('/predict',methods=['POST'])
def predict():

	int_features = [str(x) for x in request.form.values()]
	test_string=int_features[0]
	#print(test_string)
	if test_string==" ":
		return render_template('index.html', prediction_text="Please fill in some symptoms")
	else:
		s1=test_string.split(",")
		train=pd.read_csv("Training.csv")
		x=train.drop(["prognosis"],axis=1)	
		list2=list(x.columns)
		s2=[]
		features=[]
		for i in list2:
		    s2.append(i.replace("_"," "))
		for i in s1:
		    for j in s2:
		        #print(i,j)
		        in1=i.split()
		        in2=j.split()
		        r=space_seperated(in1,in2)
		        if r==1:
		            
		            features.append(j.replace(" ","_"))

		default_data=dict.fromkeys(list(x.columns),0)
		for i in features:
		    if i in default_data:
		        default_data[i]=1

		t=np.array(list(default_data.values())).reshape(1,-1)
		algo_GB = pickle.load(open('GaussianNB.sav', 'rb'))
		a1=list(algo_GB.predict(t))
		algo_SVC = pickle.load(open('SVC.sav', 'rb'))
		a2=list(algo_SVC.predict(t))
		algo_log = pickle.load(open('Logistic.sav', 'rb'))
		a3=list(algo_log.predict(t))
		l=[]
		l.append(*train["prognosis"].unique()[a1])
		l.append(*train["prognosis"].unique()[a2])
		l.append(*train["prognosis"].unique()[a3])
		op="You are likely to have "+Most_Common(l)


		return render_template('index.html', prediction_text=op)
	    	   



if __name__ == "__main__":
    app.run(debug=True)