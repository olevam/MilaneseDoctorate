import pandas as pd 
import matplotlib
from matplotlib import pyplot as plt
import database_connect as dc
origin = input("Enter monastery code: ")
dc.cur.execute(''' SELECT COUNT (alldocuments.doctype), alldocuments.doctype, alldocuments.year FROM alldocuments
    WHERE origin = %s
    GROUP BY alldocuments.doctype, alldocuments.year
    ORDER BY alldocuments.year;
''', [origin])
adocyear= pd.DataFrame(dc.cur.fetchall())
adocyear.columns = ['doc_count', 'type', 'year']
dc.cur.execute ('''SELECT doctype.translation, alldocuments.doctype FROM alldocuments 
JOIN doctype ON alldocuments.doctype = doctype.id
WHERE origin = %s
GROUP BY doctype.translation, alldocuments.doctype 
ORDER BY alldocuments.doctype
''', [origin])
docgroup = pd.DataFrame(dc.cur.fetchall())
docgroup.columns = ['doctype', "dt_num"]
docnumber_list = docgroup.dt_num.tolist()
for m_query in docnumber_list:
        name_doc = docgroup.doctype[docnumber_list.index(m_query)]
        plt.scatter(adocyear.query('type == @m_query').year, adocyear.query('type ==  @m_query').doc_count, label = name_doc,)
        plt.legend()
        plt.savefig (f"TestGraphs/{name_doc}.png", dpi =400)
    