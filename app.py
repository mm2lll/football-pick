from flask import Flask, jsonify, render_template, request
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB = Path(__file__).with_name('football.db')
MATCHES = [
 {'id':1,'home':'레알 마드리드','away':'맨체스터 시티','homeCode':'RMA','awayCode':'MCI','date':'시연 경기 · 일정 미정','stage':'UCL · DEMO','homeForm':'WWWDL','awayForm':'WWLWW','odds':[1.92,3.65,3.90]},
 {'id':2,'home':'바이에른 뮌헨','away':'아스널','homeCode':'FCB','awayCode':'ARS','date':'시연 경기 · 일정 미정','stage':'UCL · DEMO','homeForm':'WWLWW','awayForm':'DWWLD','odds':[1.78,3.80,4.20]},
 {'id':3,'home':'파리 생제르맹','away':'FC 바르셀로나','homeCode':'PSG','awayCode':'BAR','date':'시연 경기 · 일정 미정','stage':'UCL · DEMO','homeForm':'WDWWL','awayForm':'WLWWD','odds':[2.20,3.45,3.10]}
]

def connect():
    db=sqlite3.connect(DB,timeout=10)
    db.row_factory=sqlite3.Row
    return db

def init_db():
    with connect() as db:
        db.execute('CREATE TABLE IF NOT EXISTS predictions (id INTEGER PRIMARY KEY AUTOINCREMENT, match_id INTEGER NOT NULL, choice INTEGER NOT NULL)')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/matches')
def matches():
    return jsonify(MATCHES)

@app.route('/api/predict',methods=['POST'])
def predict():
    data=request.get_json(silent=True)
    if not isinstance(data,dict):
        return jsonify(error='JSON 형식이 올바르지 않습니다.'),400
    mid,choice=data.get('match_id'),data.get('choice')
    if type(mid) is not int or not any(m['id']==mid for m in MATCHES):
        return jsonify(error='존재하지 않는 경기입니다.'),400
    if type(choice) is not int or choice not in (0,1,2):
        return jsonify(error='예측 선택이 올바르지 않습니다.'),400
    with connect() as db:
        db.execute('INSERT INTO predictions (match_id,choice) VALUES (?,?)',(mid,choice))
    return jsonify(message='예측이 저장되었습니다.'),201

@app.route('/api/results/<int:mid>')
def results(mid):
    if not any(m['id']==mid for m in MATCHES):
        return jsonify(error='존재하지 않는 경기입니다.'),404
    with connect() as db:
        rows=db.execute('SELECT choice, COUNT(*) AS n FROM predictions WHERE match_id=? GROUP BY choice',(mid,)).fetchall()
    counts=[0,0,0]
    for r in rows: counts[r['choice']]=r['n']
    total=sum(counts)
    return jsonify(total=total,counts=counts,percentages=[round(n*100/total,1) if total else 0 for n in counts])

init_db()
if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
