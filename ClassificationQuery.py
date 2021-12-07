import database_connect as dc
import pandas as pd
monastery = []
abbey = []
canonry = []
dtype = []
dc.cur.execute('''
SELECT doctype.id FROM doctype
''')
for record in dc.cur:
    dtype.append (record[0])
dc.cur.execute('''
SELECT monastery.monasteryid FROM monastery 
JOIN actor on monastery.monasteryid = actor.monastery
WHERE classification = '5'
GROUP BY monasteryid
''')
for record in dc.cur:
    monastery.append (record[0])

dc.cur.execute('''
SELECT monastery.monasteryid FROM monastery 
JOIN actor on monastery.monasteryid = actor.monastery
WHERE classification IN ('59')
GROUP BY monasteryid
''')
for record in dc.cur:
    abbey.append (record[0])
dc.cur.execute('''
SELECT monastery.monasteryid FROM monastery 
JOIN actor on monastery.monasteryid = actor.monastery
WHERE classification IN ('60')
GROUP BY monasteryid
''')
for record in dc.cur:
    canonry.append (record[0])
def mon_classificaiton (monastery, doctype, classificaiton):
    if doctype is None:
        doctype = tuple(dtype)
    query = []
    OName= []           
    for og in monastery:
        if og in abbey and classificaiton == 5: 
            classid = '59'
        elif og in monastery and classificaiton == 5:
            classid = '5'
        elif og in canonry and classificaiton == 5:
            classid = '60'
        else: 
            classid = classificaiton
        dc.cur.execute('''
         SELECT Count (DISTINCT alldocuments.docid) FROM alldocuments 
        JOIN actor ON actor.docid = alldocuments.docid 
        WHERE monastery = %s AND doctype IN %s
        ; 
        ''', [og, doctype])
        for record in dc.cur:
            query.append(record[0])
        OName.append (str(og) + ' all')
        if classid != 5:
            dc.cur. execute('''
            SELECT COUNT (DISTINCT alldocuments.docid) FROM alldocuments
            JOIN actor ON alldocuments.docid = actor.docid
            WHERE alldocuments.docid IN (
            SELECT DISTINCT alldocuments.docid FROM alldocuments
            JOIN actor ON actor.docid = alldocuments.docid 
            WHERE monastery = %s 
            )
            AND doctype IN %s AND classification = %s
            ''', [og, doctype, classid])
            for record in dc.cur:
                query.append(record[0])
        else:
            dc.cur.execute('''
         SELECT Count (DISTINCT alldocuments.docid) FROM alldocuments 
        JOIN actor ON actor.docid = alldocuments.docid 
        WHERE monastery = %s AND doctype IN %s AND classification = %s
        ; 
        ''', [og, doctype, classid])
        for record in dc.cur:
                query.append(record[0])
        OName.append (str(og) + ' class')
    result = pd.DataFrame({'Monastery': OName, 'Count': query})
    print (result)
#mon_classificaiton([38], (6,), 3)
