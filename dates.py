import datetime as yr
import pandas as pd 
import database_connect as dc
yearlist = range(1100, 1301, 10)
yearset = []
declist = []
yeardate = []
decade = []
for decades in yearlist:
    yearset.append([decades, 1, 1])
for x in range(len(yearset)):
    yeardate.append(yr.date(yearset[x][0], yearset [x][1], yearset [x][2]))
for y in range(len(yeardate)):
    decade.append(yeardate[y].strftime("%Y"))

#yearframe = pd.DataFrame(declist)
#yearframe.columns = ["decades"]


    #must remeber to put the print into the loop funciton
#using pandas worked, but calling each aspect of the list separetly also worked
#for le in range(len(yearset)): 
#    print(yearset[le])
#yearframe = pd.DataFrame (yearset)
#yearframe.columns = ["year", "month", "day"]
#for x in yearframe.index:
#   decadelist = yr.date(yearframe.year[x], yearframe.month[x], yearframe.day[x])
#  print (decadelist)

#or I could use this...

#yearframe = pd.DataFrame (pd.period_range('1100-01-01', '1300-01-01', freq='10Y'))
#yearframe.columns = ['decade'] 
##pd.DataFrame (pd.)
##span.columns = ["years"]
##span['year'] = pd.DatetimeIndex(span['years']).year
#yearframe.decade.strftime("%Y")

#yearframe = pd.period_range('1100-01-01', '1300-01-01', freq='10Y')
#decades = pd.DataFrame(yearframe.strftime ("%Y"))
#decades.columns = ["decade"]
#decades.decade

def origin_doctype(origin, monastery): #this query gets the actual data and puts it in a dataframe
    dc.cur.execute(''' SELECT DISTINCT COUNT (alldocuments.doctype), alldocuments.doctype, alldocuments.year FROM alldocuments
    JOIN actor ON alldocuments.docid = actor.docid
    WHERE origin = %s AND monastery = %s
    GROUP BY alldocuments.doctype, alldocuments.year
    ORDER BY alldocuments.year;
''', [origin, monastery])