import database_connect as dc
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.axis as axis
import matplotlib.dates as mdates
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
def origin_doctype(origin): #this query gets the actual data and puts it in a dataframe
    for og in origin:
        if og == 'BSA':
            monastery = '38'
        elif og == 'Lorenzo':
            monastery = '21'
        dc.cur.execute(''' SELECT DISTINCT alldocuments.docid , alldocuments.doctype, alldocuments.year FROM alldocuments
        JOIN actor ON alldocuments.docid = actor.docid
        WHERE origin = %s AND monastery = %s
        GROUP BY alldocuments.docid, alldocuments.doctype, alldocuments.year 
        ORDER BY alldocuments.year;
        ''', [og, monastery])
        adocyear= pd.DataFrame(dc.cur.fetchall())
        adocyear.columns = ['docid', 'type', 'year']
        docyeargroup = adocyear.groupby([adocyear.type, adocyear.year]).size().reset_index(name='counts')
        dc.cur.execute ('''SELECT doctype.translation, alldocuments.doctype FROM alldocuments 
        JOIN doctype ON alldocuments.doctype = doctype.id
        WHERE origin = %s
        GROUP BY doctype.translation, alldocuments.doctype 
        ORDER BY alldocuments.doctype
        ''', [og]) #this query allows me to loop through the right number of doctypes per instiution without using if statements. I create a list of all the doctypes and put them into a query 
        docgroup = pd.DataFrame(dc.cur.fetchall())
        docgroup.columns = ['doctype', "dt_num"]
        docnumber_list = docgroup.dt_num.tolist()
        for m_query in docnumber_list:
            name_doc = docgroup.doctype[docnumber_list.index(m_query)]
            venfig = plt.figure(figsize = (10,10)) #create a figure
            ev_decade = mdates.YearLocator(10) #this is for the ticks - it shows every 10 years
            axes_1 = venfig.add_axes([0,0,1,1]) #this adds the axes, and gives their position (left,bottom,width, height)
            axes_1.set_title (name_doc)
            axes_1.scatter (docyeargroup.query('type == @m_query').year, docyeargroup.query('type ==  @m_query').counts, label = name_doc,)
            axes_1.xaxis.set_major_locator(ev_decade) #if you have not created the axes this won't work!
            axes_1.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
            axes_1.yaxis.set_major_locator(MultipleLocator(1)) #you need to import the ticker for this as above
            axes_1.legend ()
            venfig.savefig(f"TestGraphs/{name_doc}{og}.jpg", bbox_inches='tight', dpi = 400 )
origin_doctype (['BSA','Lorenzo'])
