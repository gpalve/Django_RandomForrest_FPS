
import re
from django.shortcuts import render
from joblib import load 
import pandas as pd
import pymysql as pm
from sqlalchemy import create_engine
from django.templatetags.static import static
import pickle



model = load('model/fm.pkl')


# Create your views here.
def index(request):
    context = {'result':''}
    data = {'name':[],'email':[],'age':[],'season':[],'childish_disease':[],'acc_trauma':[],'surgical':[],'surgical':[],'fever_lastyr':[],'alcohol':[],'smoking':[],'sitting':[]}
    df = pd.DataFrame(data)
    conn = create_engine("mysql+pymysql://root:@localhost/fps")
   
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        age = str(request.POST.get('age'))
        season = str(request.POST.get('season'))
        childish_disease = str(request.POST.get('childish_disease'))
        acc_trauma = str(request.POST.get('acc_trauma'))
        surgical = str(request.POST.get('surgical'))
        fever_lastyr = str(request.POST.get('fever_lastyr'))
        alcohol = str(request.POST.get('alcohol'))
        smoking = str(request.POST.get('smoking'))
        sitting = str(request.POST.get('sitting'))

        result =model.predict([[float(season),float(age),float(childish_disease),float(acc_trauma),float(surgical),float(fever_lastyr),float(alcohol),float(smoking),float(sitting)]])

        df['name'] = [name]
        df['email'] = [email]
        df['age'] = [age]
        df['season'] = [season]
        df['childish_disease'] = [childish_disease]
        df['acc_trauma'] = [acc_trauma]
        df['surgical'] = [surgical]
        df['fever_lastyr'] = [fever_lastyr]
        df['alcohol'] = [alcohol]
        df['smoking'] = [smoking]
        df['sitting'] = [sitting]
        df['result'] = ['Normal' if result[0] == 1 else 'Abnormal']
        df.to_sql(name='fps_customer',con=conn,if_exists='append',index=False)

        context = {
            'result':result[0],
            'name': name ,
            'email' : email
        }
        return render(request,'index.html',context)
    return render(request,'index.html',{})

    
