from geopandas.geoseries import GeoSeries
from shapely import geometry
from shapely.geometry import Point, LineString, Polygon
import geopandas as gpd
import pandas as pd
import database_connect as dc
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import math
import datetime
pd.options.display.max_rows = 1000
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
cities = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))
italy = world.query("name=='Italy'")
nfp = "C:/Users/Olevam/Documents/GPandaDoc/Data/Limiti01012021_g/Reg01012021_g/Reg01012021_g_WGS84.shp"
data = gpd.read_file(nfp)
data = data.to_crs(world.crs)
def allpoints ():
    dc.cur.execute(''' SELECT ST_AsText(geocoordinates::geometry), locations FROM coordinates''')
    df = pd.DataFrame(dc.cur.fetchall())
    df.columns = ['geometry','locations']
    gs = gpd.GeoSeries.from_wkt(df ['geometry'])
    gdf = gpd.GeoDataFrame(df, geometry=gs)
    gdf.crs = 'EPSG:3395'
    withdist = pd.DataFrame(gdf.distance(gdf.loc[5, 'geometry']))
    withdist.columns = ['distance']
    gdfwithdist = gpd.GeoDataFrame(pd.concat([gdf, withdist], axis=1))
    gdffpl = gdfwithdist.loc[gdfwithdist['distance']<= 8.721407]

    fig, ax = plt.subplots(figsize=(15,15))
    ax.set_aspect('equal')
    italy.plot(ax=ax, color='white', edgecolor='black')
    gdffpl.plot(ax=ax, marker='.',color ='red',markersize=100)
    for x,y, label in zip (gdffpl.geometry.x,gdffpl.geometry.y, gdffpl.locations):
       ax.annotate(label, xy=(x, y), xytext=(3,3), textcoords='offset points')
    plt.show

def loc_mon (monastery):
    dc.cur.execute('''SELECT coordinates.locations, ST_AsText(geocoordinates::geometry), count(*) FROM alldocuments
    JOIN land_loc ON land_loc.docid = alldocuments.docid
    JOIN coordinates ON coordinates.coordid = land_loc.coordid
    WHERE alldocuments.docid IN (
    SELECT DISTINCT alldocuments.docid FROM alldocuments
    JOIN actor ON actor.docid = alldocuments.docid 
    WHERE monastery = %s 
    )
    GROUP BY coordinates.locations, ST_AsText(geocoordinates::geometry)
    ORDER BY count desc''', [monastery])
    fig, ax = plt.subplots()
    df = pd.DataFrame(dc.cur.fetchall(), columns=['locations', 'geometry', 'number'])
    gs = gpd.GeoSeries.from_wkt(df ['geometry'])
    gdf = gpd.GeoDataFrame(df, geometry=gs, crs='EPSG:3395')
    italy.plot(ax=ax)
    gdf.plot(ax=ax, column='number')
    
def loc_leader_time (monastery, origin):
    leaderlisttime = []
    leaderlist = []
    lead_loc = []
    l_yearb = []
    l_yeare = []
    coordlist = []

    doSomething(origin, leaderlisttime)

    for leader_list_item in leaderlisttime[0]:
        if leader_list_item[0] not in leaderlist:
            leaderlist.append (leader_list_item[0])
        else:
            continue
    lead_loc = []
    for leader in leaderlist:
        doSomething1(monastery, origin, lead_loc, leader)
        doSomething2(origin, l_yearb, leader)
        doSomething3(origin, l_yeare, leader)
   
    for a in range(len(lead_loc)):
        for x in lead_loc[a]:
            coordlist.append(x[1])  
    df= pd.DataFrame(coordlist, columns=['geometry'])
    gs = gpd.GeoSeries.from_wkt(df ['geometry'])
    gdf = gpd.GeoDataFrame(df, geometry=gs, crs='EPSG:3395')
    a = gdf.geometry.x
    b = gdf.geometry.y
   
    x= math.trunc(len(leaderlist)/2)
    fig, axs = plt.subplots(x,2,figsize=(15,15))
    plt.subplots_adjust(left=0.1,
                   bottom=0.1, 
                   right=0.6, 
                   top=0.9, 
                   wspace=1, 
                   hspace=1)
    for i in range (len(leaderlist)): 
       df= pd.DataFrame(lead_loc[i], columns=['locations', 'geometry', 'number'])
       gs = gpd.GeoSeries.from_wkt(df ['geometry'])
       gdf = gpd.GeoDataFrame(df, geometry=gs, crs='EPSG:3395')
       if i <=x-1:
           axs[i,0].set(xlim=(a.min()+ 0.1,a.max()+ 0.1), ylim=(b.min()+ 0.1,b.max()+ 0.1))
           axs[i,0].set_title(leaderlist[i] + " " + str(l_yearb[i][0][0].year) + " - " + str(l_yeare[i][0][0].year), loc='right')
           data.plot(ax=axs[i,0],color = 'none', edgecolor ='black')
           gdf.plot (ax=axs[i,0], column = 'number')
           axs[i,0].annotate('Milan', xy=(9.19, 45.4642), xytext=(3,3), textcoords='offset points', fontsize=7)
       elif i > x-1:
           axs[i-x, 1].set(xlim=(a.min()+0.1,a.max()+ 0.1)  , ylim=(b.min()+ 0.1,b.max()+ 0.1)) 
           axs[i-x,1].set_title(leaderlist[i] + " "+ str(l_yearb[i][0][0].year) + " - " + str(l_yeare[i][0][0].year), loc='left')
           data.plot(ax=axs[i-x,1], color = 'none', edgecolor ='black')
           gdf.plot (ax=axs[i-x,1], column = 'number')
           axs[i-x, 1].annotate('Milan', xy=(9.19, 45.4642), xytext=(3,3), textcoords='offset points', fontsize=7)
           
    plt.show()

def doSomething(origin, leaderlisttime):
    dc.cur.execute('''
    SELECT DISTINCT leader.firstname, year FROM alldocuments
    JOIN leader ON alldocuments.docid = leader.docid 
    WHERE origin = %s AND leader.firstname <> 'None'
    ORDER BY year
        ''', [origin])
    leaderlisttime.append(dc.cur.fetchall())

def doSomething3(origin, l_yeare, leader):
    dc.cur.execute('''
            SELECT year FROM alldocuments 
            JOIN leader ON alldocuments.docid = leader.docid
            WHERE origin = %s AND leader.firstname = %s
            ORDER BY year desc
            LIMIT 1
            ''',[origin, leader])
    l_yeare.append(dc.cur.fetchall())

def doSomething2(origin, l_yearb, leader):
    query1 = '''
            SELECT year FROM alldocuments 
            JOIN leader ON alldocuments.docid = leader.docid
            WHERE origin = %s AND leader.firstname = %s
            ORDER BY year asc
            LIMIT 1
            '''
    dc.cur.execute(query1, [origin, leader])
    l_yearb.append(dc.cur.fetchall())

def doSomething1(monastery, origin, lead_loc, leader):
    query = '''
        SELECT coordinates.locations, ST_AsText(geocoordinates::geometry), count(*) FROM alldocuments 
        JOIN land_loc ON land_loc.docid = alldocuments.docid
        JOIN coordinates ON coordinates.coordid = land_loc.coordid
        WHERE alldocuments.docid IN (SELECT DISTINCT alldocuments.docid FROM alldocuments
        JOIN actor ON actor.docid = alldocuments.docid 
        WHERE monastery = %s) 
         AND alldocuments.year BETWEEN (
            SELECT year FROM alldocuments 
            JOIN leader ON alldocuments.docid = leader.docid
            WHERE origin = %s AND leader.firstname = %s
            ORDER BY year asc
            LIMIT 1) 
        AND (SELECT year FROM alldocuments 
            JOIN leader ON alldocuments.docid = leader.docid
            WHERE origin = %s AND leader.firstname = %s
            ORDER BY year desc
            LIMIT 1)
        GROUP BY coordinates.locations, ST_AsText(geocoordinates::geometry)
        ORDER BY count desc
        '''
    dc.cur.execute(query, [monastery, origin, leader, origin, leader])
    lead_loc.append(dc.cur.fetchall())
loc_leader_time(2, 'Margherita')

      