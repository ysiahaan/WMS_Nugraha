from flask import Flask
from flask import Response
from flask import send_file
from flask_cors import CORS
from flask import request
from flaskext.mysql import MySQL
from werkzeug.security import safe_str_cmp
from flask import jsonify
import random
import datetime
from shutil import copyfile
import os

#import flask.ext
import hashlib

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

semuaHuruf=["A","B","C","D","E","F","G","H","I",
                        "J","K","L","M","N","O","P","Q","R",
                        "S","T","U","V","W","X","Y","Z","All"]
    
semuaHurufAngka=["A","B","C","D","E","F","G","H","I",
            "J","K","L","M","N","O","P","Q","R",
            "S","T","U","V","W","X","Y","Z"
            ,"0","1","2","3","4","5","6","7","8","9"]

app = Flask(__name__)
#app.config['MYSQL_DATABASE_HOST'] = '202.157.184.178'
#app.config['MYSQL_DATABASE_HOST'] = 'toko4060.ath.cx'

if 1:
    #app.config['MYSQL_DATABASE_HOST'] = 'zeppy2.ath.cx'
    app.config['MYSQL_DATABASE_HOST'] = '192.168.51.87'
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
    #app.config['MYSQL_DATABASE_PORT'] = 5102
    app.config['MYSQL_DATABASE_PORT'] = 3306
    app.config['MYSQL_DATABASE_DB'] = 'nugraha_tb'

if 0:
    app.config['MYSQL_DATABASE_HOST'] = '192.168.10.88'
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
    app.config['MYSQL_DATABASE_PORT'] = 3306
    app.config['MYSQL_DATABASE_DB'] = 'nugraha_tb'

if 0:
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    app.config['MYSQL_DATABASE_USER'] = 'vbPro'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'vbPro'
    app.config['MYSQL_DATABASE_PORT'] = 3303
    app.config['MYSQL_DATABASE_DB'] = 'vb_ign'

#app.config['MYSQL_DATABASE_DB'] = 'vb_tp40'

folderAPI="/nug_api"
folderCRM="/nug_api"
folderEst="/est_api"
folderHRD="/hrd_api"
folderSales="/sales_api"
folderGdg="/gudang_api"

kunciHash="ign-secret"

app.config["JWT_SECRET_KEY"] = kunciHash  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(days=30)

jwt = JWTManager(app)
mysql = MySQL(app)
cors = CORS(app)

def autoAddTabel(col,dapat):
#    return

    namatabel=col
    query="describe %s"%namatabel
    conn=mysql.get_db()
    theCon=conn.cursor()
    
    dapatCol=[]
    theCon.execute(query)
    for single in ambilBanyakRowSQL(query):
        dapatCol.append(single[0].lower())
    
    try:
        for single in dapat:
            if single.lower() not in dapatCol:
                namaCol=single.lower()
                query="ALTER TABLE `%s` ADD COLUMN `%s` VARCHAR(50) DEFAULT '';"%(namatabel,namaCol)
                print query
                
                try:theCon.execute(query)
                except:1
    except:1
    
    conn.commit()
    theCon.close()
def ambilBanyakRowSQL(sqlStr,sqlUrut=""):
    conn2=mysql.get_db()
    curs=conn2.cursor()
    if sqlUrut=="":strUrut="order by id desc"
    else:strUrut=sqlUrut
        
    sqlStr1="%s %s"%(sqlStr,strUrut)
    try:curs.execute(sqlStr1)
    except:curs.execute(sqlStr)
    tobeRet = curs.fetchall()
    
    curs.close()
    return tobeRet
def ambilSatuRowSQL(sqlStr):
    conn2=mysql.get_db()
    curs=conn2.cursor()
    curs.execute(sqlStr)
    tobeRet = curs.fetchone()
    curs.close()
    return tobeRet
def bikinGetJSONExt(namatabel,strWhere):
    namaTabel=namatabel
    
    query="describe %s"%namatabel
    conn=mysql.get_db()
    theCon=conn.cursor()
    
    dapatCol=[]
    theCon.execute(query)
    for single in ambilBanyakRowSQL(query):
        dapatCol.append(single[0].lower())
    
    listSel=dapatCol
    
    autoAddTabel(namaTabel,listSel)
    
    strSelect=""
    for single in listSel:strSelect+="`%s`,"%single
    strSelect=strSelect[0:len(strSelect)-1]
                
    query="""select %s
        from %s %s """%(strSelect,namaTabel,strWhere)
    print query
    
    dic={}
    dic["error"]='false'
    dic["msg"]=""
    dic["data"]={}
    dic["data"]["rows"]=[]
    
    if 1:
    
        for single in ambilBanyakRowSQL(query):
            data1={}
            theCol=len(single)
            
            for single2 in range(theCol):
                strData1='%s'%single[single2]
                strData1=strData1.replace("\"","")
                strData1=strData1.replace("\'","")
                strData1=strData1.replace("\\","")
                strData1=strData1.replace("\\\\","")
                if '%s'%strData1=="None":data1[listSel[single2]]=""
                else:data1[listSel[single2]]=strData1
            
            dic["data"]["rows"].append(data1)
        dic["data"]["total"]=len(dic["data"]["rows"])
    
    strDic="%s"%dic
    #print strDic
    
#    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
#    print strDic
    return Response(strDic, mimetype='application/json')
def bikinGetJSONExtQueryMan(query,strWhere,dataCol):
    #namaTabel=namatabel
    
    listSel=dataCol
    
    strSelect=query
    
    query="""%s %s """%(strSelect,strWhere)
    print query
    
    dic={}
    dic["error"]='false'
    dic["msg"]=""
    dic["data"]={}
    dic["data"]["rows"]=[]
    
    if 1:
    
        for single in ambilBanyakRowSQL(query):
            data1={}
            theCol=len(single)
            
            for single2 in range(theCol):
                    if '%s'%single[single2]=="None":data1[listSel[single2]]=""
                    else:data1[listSel[single2]]=single[single2]
            
            dic["data"]["rows"].append(data1)
        dic["data"]["total"]=len(dic["data"]["rows"])
    
    strDic="%s"%dic
    #print strDic
    
#    strDic=strDic.replace("'",'"').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
#    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
#    print strDic
    return Response(strDic, mimetype='application/json')
def ubahJadiJSONfix(str):
#    return str.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('[u"','["').replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
    return str.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('[u"','["').replace('{u"','{"').replace("L,"," ,")

@app.route("%s/login"%folderAPI, methods=["POST"])
def login():
    username = request.json.get("nama", None)
    password = request.json.get("password", None)
#    role = request.json.get("password", None)
    
#    mtd=hashlib.sha1(kunciHash)
#    mtd.update(password)
    strPass=password#mtd.hexdigest()
            
    query="select kodesales,namasales from sales where namasales='%s' and kodesales='%s'"%(username,strPass)
    print query
    
    dapat=ambilSatuRowSQL(query)
    role1="Sales"
    level1="9"
    
    if username=="gudang" and password=="123456":
        role1="Gudang"
        
    else:
        try:
    #        role1=dapat[1]
            dapat=dapat[0]
        except:
            query="select idpeg,nama,level from pegawai where nama='%s' and idpeg='%s'"%(username,strPass)
            print query
            dapat=ambilSatuRowSQL(query)
            role1="Gudang"
            level1=dapat[2]
    
            try:
                dapat=dapat[0]
            except:
                return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token,role=role1,level=level1)

@app.route("%s/login2"%folderAPI, methods=["POST"])
def login2():

    username = request.args.get('nama')
    password = request.args.get('password')
#    role = request.json.get("password", None)
    
#    mtd=hashlib.sha1(kunciHash)
#    mtd.update(password)
    strPass=password#mtd.hexdigest()
            
    query="select kodesales,namasales from sales where namasales='%s' and kodesales='%s'"%(username,strPass)
    print query
    
    dapat=ambilSatuRowSQL(query)
    role1="Sales"
    level1="9"
    
    if username=="gudang" and password=="123456":
        role1="Gudang"
        
    else:
        try:
    #        role1=dapat[1]
            dapat=dapat[0]
        except:
            query="select idpeg,nama,level from pegawai where nama='%s' and idpeg='%s'"%(username,strPass)
            conn2=mysql.get_db()
            theCon2=conn2.cursor()
            theCon2.execute(query)
            if theCon2.rowcount==0:
                data1={}
                dic={}
                dic["error"]='true'
                dic["msg"]="Username/Password Salah"
                theCon2.close()
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                return Response(strDic, mimetype='application/json')
            print query
            dapat=ambilSatuRowSQL(query)
            role1="Gudang"
            level1=dapat[2]
    
            try:
                dapat=dapat[0]
            except:
                return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token,role=role1,level=level1,namaLogin=username)

@app.route("%s/gantiPass"%folderAPI, methods=["POST"])
def gantiPass():
    username = request.json.get("email", None)
    password = request.json.get("password", None)
#    role = request.json.get("password", None)
    
    mtd=hashlib.sha1(kunciHash)
    mtd.update(password)
    strPass=mtd.hexdigest()

    query="select * from relasi where nohp='%s'"%(username)
    dapat=ambilSatuRowSQL(query)
    ada=0
    try:
        len(dapat)
        ada=1
    except:1
            
    query="update relasi set alamatkirim='%s' where nohp='%s'"%(strPass,username)
    conn2=mysql.get_db()
    theCon=conn2.cursor()
    theCon.execute(query)
    dapat=theCon.rowcount
    conn2.commit()
    theCon.close()
    
    dapat=ambilSatuRowSQL(query)
    role1="Sales"
    if ada>0:return jsonify({"msg": "Berhasil Ganti Password"})
    else:return jsonify({"msg": "Bad username or password"}), 401

@app.route("/")
@app.route("%s/"%folderAPI, methods=["GET"])
def hello():
    ok2="""{"error":"false","msg":"Helow22"}"""
    return Response(ok2, mimetype='application/json')

    namatabel="company"
    query="describe %s"%namatabel
    conn=""
#    theCon=conn.cursor()
#    theCon.execute(query)
    
    str=""
    for single in ambilBanyakRowSQL(query):#theCon.fetchall():
        str+=single[0]
        
    ok2="""{"error":"false","msg":"%s"}"""%str
    
#            conn2=mysql.get_db()
#            theCon=conn2.cursor()
#            try:theCon.execute(query)
#            except:1
#            conn2.commit()
#            theCon.close()
            
    return Response(ok2, mimetype='application/json')
@app.route("%s/relasi"%folderAPI, methods=["GET"])
def hello2():
    namaTabel="relasi"
    strWhere="where 1"
    return bikinGetJSONExt(namaTabel,strWhere)
                
    ok2="""{"error":"false","msg":"Hello"}"""
    return Response(ok2, mimetype='application/json')
@app.route("%s/barang"%folderAPI, methods=["GET"])
#@jwt_required
def barang():
    #id1 = get_jwt_identity()
    #print id1
    
    theLimit= request.args.get('itemsPerPage')
    if '%s'%theLimit=="None":theLimit=100
    try:theLimit=int(theLimit)
    except:theLimit=100
    
    strLimit="limit %s"%theLimit
    
    numPage= request.args.get('numberPage')
    if '%s'%numPage=="None":numPage=1
    try:numPage=int(numPage)
    except:numPage=1
    numPage=numPage-1
    strPage="offset %s"%(numPage*theLimit)
    
    strCari= request.args.get('searchNama')
    if '%s'%strCari=="None":strCari="1"
    else:strCari="namabrg like '%s%s%s' order by namabrg"%('%',strCari,'%')
    
    namaTabel="barang"
    strWhere="where %s %s %s"%(strCari,strLimit,strPage)
    
    listSel=["kodebrg","namabrg","merk","stok","satuan","hbeli","hjual","hjual1","hjual2","hjual3","hjual4","hjual5","kodejen"]
    query="""select kodebrg,trim(namabrg) namabrg, trim(merk) merk ,sisa+tsisabeli-tsisajual stok, satuan,hbeli, hjual, hjual1,hjual2,hjual3,hjual4,hjual5,kodejen 
    from %s %s """%(namaTabel,strWhere)
    
    dic={}
    dic["error"]='false'
    dic["msg"]=""
    dic["data"]={}
    dic["data"]["rows"]=[]
    
    if 1:
        data1={}
        
        for single in ambilBanyakRowSQL(query):
            data1={}
            theCol=len(single)
            
            for single2 in range(theCol):
                strData1='%s'%single[single2]
                strData1=strData1.replace("\"","")
                strData1=strData1.replace("\'","")
                if '%s'%strData1=="None":data1[listSel[single2]]=""
                else:data1[listSel[single2]]=strData1
            
            dic["data"]["rows"].append(data1)
        dic["data"]["total"]=len(dic["data"]["rows"])
        
    
    strDic="%s"%dic
#    strDic=strDic.replace("'",'"').replace('": u','": ').replace(', u"',', "').replace(", u'",", '").replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
#    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

    return Response(strDic, mimetype='application/json')

@app.route('%s/getPODetAutoCom'%(folderAPI), methods=['GET', 'PUT'])
def getPODetAutoCom():
    if request.method == 'GET':
        id1= request.args.get('nopo')
        
        theLimit=100
        
        strLimit="limit %s"%theLimit
        
        strPage=""
        
        #strCari= request.args.get('query')
        #if '%s'%strCari=="None":strCari="1"
        #else:strCari="namabrg like '%s%s%s' order by namabrg"%('%',strCari,'%')
        
        #strCari= request.args.get('query')
        strCari="nomorpo='%s' "%id1
        strQ=request.args.get('query')
        strQ=strQ.replace(" ","%")
        strCari2="namabrg like '%s%s%s' "%('%',strQ,'%')
        
        namaTabel="notapodetail"
        strWhere="where %s %s %s"%(strCari,strLimit,strPage)
        
        listSel=["data","value","satuan"]
        query="""select * from (select kodeBarang,(select trim(namabrg) from barang where kodebrg=kodeBarang) namabrg,(select satuan from barang where kodebrg=kodeBarang) from %s %s) s where  %s"""%(namaTabel
        ,strWhere,strCari2)
        print query
        
        dic={}
        dic["error"]='false'
        dic["msg"]=""
        dic["suggestions"]=[]
    #    dic["data"]["rows"]=[]
        
        if 1:
            data1={}
            
            for single in ambilBanyakRowSQL(query):
                data1={}
                theCol=len(single)
                
                for single2 in range(theCol):
                    strData1='%s'%single[single2]
                    strData1=strData1.replace("\"","")
                    strData1=strData1.replace("\'","")
                    if '%s'%strData1=="None":data1[listSel[single2]]=""
                    else:data1[listSel[single2]]=strData1
                
                dic["suggestions"].append(data1)
    #        dic["data"]["total"]=len(dic["data"]["rows"])
            
        
        strDic="%s"%dic
    #    strDic=strDic.replace("'",'"').replace('": u','": ').replace(', u"',', "').replace(", u'",", '").replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
    #    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
        strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
        
    #    print strDic
        
        return Response(strDic, mimetype='application/json')
@app.route("%s/barangAutoComBySup"%folderAPI, methods=["GET"])
#@jwt_required
def barangAutoComBySup():
    #id1 = get_jwt_identity()
    #print id1
    id1= request.args.get('supp')
    
    theLimit=100
    
    strLimit="limit %s"%theLimit
    
    strPage=""
    
    strCari= request.args.get('query')
    if '%s'%strCari=="None":strCari="1"
    else:strCari="namabrg like '%s%s%s' and (koderel='%s' or koderel='') order by namabrg"%('%',strCari,'%',id1)
    
    namaTabel="barang"
    strWhere="where %s %s %s"%(strCari,strLimit,strPage)
    
    listSel=["data","value","harga","satuan","idbarang","jmlKarton","kodebrgkarton"]#,"merk","stok","satuan","hbeli","hjual","hjual1","hjual2","hjual3","hjual4","hjual5","kodejen"]
#    query="""select kodebrg,trim(namabrg) namabrg, trim(merk) merk ,sisa+tsisabeli-tsisajual stok, satuan,hbeli, hjual, hjual1,hjual2,hjual3,hjual4,hjual5,kodejen 
    query="""select kodebrg,trim(namabrg) namabrg,hjual,satuan,idbarang,(select jmlkarton from barangdet where barangdet.kodebrg=barang.kodebrg limit 1),(select kodebrgkarton from barangdet where barangdet.kodebrg=barang.kodebrg limit 1) from %s %s """%(namaTabel,strWhere)
    
    
#    strCari="koderel='%s' or koderel=''"%id1
#    strQ=request.args.get('query')
    #strQ=strQ.replace(" ","%")
#    strCari2="namabrg like '%s%s%s' order by namabrg"%('%',strQ,'%')    
    
#    namaTabel="barang"
#    strWhere="where %s %s %s"%(strCari,strLimit,strPage)
    
    
#    listSel=["data","value","harga","satuan","jmlKarton"]#,"merk","stok","satuan","hbeli","hjual","hjual1","hjual2","hjual3","hjual4","hjual5","kodejen"]
    #query="""select kodebrg,trim(namabrg) namabrg,hjual,satuan,(select jmlkarton from barangdet where barangdet.kodebrg=barang.kodebrg) from %s %s """%(namaTabel,strWhere)
#    query="""select * from (select kodebrg,trim(namabrg) namabrg,hjual,satuan,(select jmlkarton from barangdet where barangdet.kodebrg=barang.kodebrg)jmlkarton from %s %s) tab1 where %s"""%(namaTabel
#        ,strWhere,strCari2)

    
    dic={}
    dic["error"]='false'
    dic["msg"]=""
    dic["suggestions"]=[]
#    dic["data"]["rows"]=[]
    
    if 1:
        data1={}
        
        for single in ambilBanyakRowSQL(query):
            data1={}
            theCol=len(single)
            
            for single2 in range(theCol):
                strData1='%s'%single[single2]
                strData1=strData1.replace("\"","")
                strData1=strData1.replace("\'","")
                if '%s'%strData1=="None":data1[listSel[single2]]=""
                else:data1[listSel[single2]]=strData1
            
            dic["suggestions"].append(data1)
#        dic["data"]["total"]=len(dic["data"]["rows"])
        
    
    strDic="%s"%dic
#    strDic=strDic.replace("'",'"').replace('": u','": ').replace(', u"',', "').replace(", u'",", '").replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
#    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
    
#    print strDic
    
    return Response(strDic, mimetype='application/json')
@app.route("%s/barangAutoCom"%folderAPI, methods=["GET"])
#@jwt_required
def barangAutoCom():
    #id1 = get_jwt_identity()
    #print id1
    
    theLimit=100
    
    strLimit="limit %s"%theLimit
    
    strPage=""
    
    strCari= request.args.get('query')
    if '%s'%strCari=="None":strCari="1"
    else:strCari="namabrg like '%s%s%s' order by namabrg"%('%',strCari,'%')
    
    namaTabel="barang"
    strWhere="where %s %s %s"%(strCari,strLimit,strPage)
    
    listSel=["data","value","harga","satuan","jmlKarton"]#,"merk","stok","satuan","hbeli","hjual","hjual1","hjual2","hjual3","hjual4","hjual5","kodejen"]
#    query="""select kodebrg,trim(namabrg) namabrg, trim(merk) merk ,sisa+tsisabeli-tsisajual stok, satuan,hbeli, hjual, hjual1,hjual2,hjual3,hjual4,hjual5,kodejen 
    query="""select kodebrg,trim(namabrg) namabrg,hjual,satuan,(select jmlkarton from barangdet where barangdet.kodebrg=barang.kodebrg limit 1) from %s %s """%(namaTabel,strWhere)
    
    dic={}
    dic["error"]='false'
    dic["msg"]=""
    dic["suggestions"]=[]
#    dic["data"]["rows"]=[]
    
    if 1:
        data1={}
        
        for single in ambilBanyakRowSQL(query):
            data1={}
            theCol=len(single)
            
            for single2 in range(theCol):
                strData1='%s'%single[single2]
                strData1=strData1.replace("\"","")
                strData1=strData1.replace("\'","")
                if '%s'%strData1=="None":data1[listSel[single2]]=""
                else:data1[listSel[single2]]=strData1
            
            dic["suggestions"].append(data1)
#        dic["data"]["total"]=len(dic["data"]["rows"])
        
    
    strDic="%s"%dic
#    strDic=strDic.replace("'",'"').replace('": u','": ').replace(', u"',', "').replace(", u'",", '").replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
#    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
    
#    print strDic
    
    return Response(strDic, mimetype='application/json')

@app.route("%s/barangBaruAutoCom"%folderAPI, methods=["GET"])
#@jwt_required
def barangBaruAutoCom():
    #id1 = get_jwt_identity()
    #print id1
    
    theLimit=100
    
    strLimit="limit %s"%theLimit
    
    strPage=""
    
    strCari= request.args.get('query')
    if '%s'%strCari=="None":strCari="1"
    else:strCari="namabrg like '%s%s%s' order by namabrg"%('%',strCari,'%')
    
    namaTabel="barang"
    strWhere="where %s %s %s"%(strCari,strLimit,strPage)
    
    listSel=["data","value","satuan","barcode","kodebrgpack","kodebrgkarton","jumlahbrg","jmlpack","jmlkarton"]#,"merk","stok","satuan","hbeli","hjual","hjual1","hjual2","hjual3","hjual4","hjual5","kodejen"]
#    query="""select kodebrg,trim(namabrg) namabrg, trim(merk) merk ,sisa+tsisabeli-tsisajual stok, satuan,hbeli, hjual, hjual1,hjual2,hjual3,hjual4,hjual5,kodejen 
    query="""select trim(kodebrg),trim(namabrg) namabrg,satuan,trim(barcode),(select trim(kodebrgpack) from barangdet where barangdet.kodebrg=barang.kodebrg limit 1),
    (select trim(kodebrgkarton) from barangdet where barangdet.kodebrg=barang.kodebrg limit 1),(select jumlahbrg from barangdet where barangdet.kodebrg=barang.kodebrg limit 1),
    (select jmlpack from barangdet where barangdet.kodebrg=barang.kodebrg limit 1),(select jmlkarton from barangdet where barangdet.kodebrg=barang.kodebrg limit 1) from %s %s """%(namaTabel,strWhere)
    
    dic={}
    dic["error"]='false'
    dic["msg"]=""
    dic["suggestions"]=[]
#    dic["data"]["rows"]=[]
    
    if 1:
        data1={}
        
        for single in ambilBanyakRowSQL(query):
            data1={}
            theCol=len(single)
            
            for single2 in range(theCol):
                strData1='%s'%single[single2]
                strData1=strData1.replace("\"","")
                strData1=strData1.replace("\'","")
                if '%s'%strData1=="None":data1[listSel[single2]]=""
                else:data1[listSel[single2]]=strData1
            
            dic["suggestions"].append(data1)
#        dic["data"]["total"]=len(dic["data"]["rows"])
        
    
    strDic="%s"%dic
#    strDic=strDic.replace("'",'"').replace('": u','": ').replace(', u"',', "').replace(", u'",", '").replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
#    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
    
#    print strDic
    
    return Response(strDic, mimetype='application/json')


@app.route("%s/barangJWT"%folderAPI, methods=["GET"])
@jwt_required
def barangJWT():
    id1 = get_jwt_identity()
    print id1
    
    theLimit= request.args.get('itemsPerPage')
    if '%s'%theLimit=="None":theLimit=100
    try:theLimit=int(theLimit)
    except:theLimit=100
    
    strLimit="limit %s"%theLimit
    
    numPage= request.args.get('numberPage')
    if '%s'%numPage=="None":numPage=1
    try:numPage=int(numPage)
    except:numPage=1
    numPage=numPage-1
    strPage="offset %s"%(numPage*theLimit)
    
    strCari= request.args.get('searchNama')
    if '%s'%strCari=="None":strCari="1"
    else:strCari="namabrg like '%s%s%s' order by namabrg"%('%',strCari,'%')
    
    namaTabel="barang"
    strWhere="where %s %s %s"%(strCari,strLimit,strPage)
    
    listSel=["kodebrg","namabrg","merk","stok","satuan","hbeli","hjual","hjual1","hjual2","hjual3","hjual4","hjual5","kodejen"]
    query="""select kodebrg,trim(namabrg) namabrg, trim(merk) merk ,sisa+tsisabeli-tsisajual stok, satuan,hbeli, hjual, hjual1,hjual2,hjual3,hjual4,hjual5,kodejen 
    from %s %s """%(namaTabel,strWhere)
    
    dic={}
    dic["error"]='false'
    dic["msg"]=""
    dic["data"]={}
    dic["data"]["rows"]=[]
    
    if 1:
        data1={}
        
        for single in ambilBanyakRowSQL(query):
            data1={}
            theCol=len(single)
            
            for single2 in range(theCol):
                strData1='%s'%single[single2]
                strData1=strData1.replace("\"","")
                strData1=strData1.replace("\'","")
                if '%s'%strData1=="None":data1[listSel[single2]]=""
                else:data1[listSel[single2]]=strData1
            
            dic["data"]["rows"].append(data1)
        dic["data"]["total"]=len(dic["data"]["rows"])
        
    
    strDic="%s"%dic
    #strDic=strDic.replace("'",'"').replace('": u','": ').replace(', u"',', "').replace(", u'",", '").replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
#    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

    return Response(strDic, mimetype='application/json')
@app.route("%s/barangdet"%folderAPI, methods=["GET"])
#@jwt_required
def barangdet():
    #id1 = get_jwt_identity()
    #print id1
    
    theLimit= request.args.get('itemsPerPage')
    if '%s'%theLimit=="None":theLimit=100
    try:theLimit=int(theLimit)
    except:theLimit=100
    
    strLimit="limit %s"%theLimit
    
    numPage= request.args.get('numberPage')
    if '%s'%numPage=="None":numPage=1
    try:numPage=int(numPage)
    except:numPage=1
    numPage=numPage-1
    strPage="offset %s"%(numPage*theLimit)
    
    kodebrg= request.args.get('kodebrg')
    
    query="select kodebrg,jmlkarton,lokasikrtn from barangdet where kodebrgkarton='%s' limit 1"%(kodebrg)
    try:
        dapat=ambilSatuRowSQL(query)
        dapat[0]
    except:
        query="select kodebrg,jmlpack,lokasi from barangdet where kodebrgpack='%s'  limit 1"%(kodebrg)
        try:
            dapat=ambilSatuRowSQL(query)
            dapat[0]
    
        except:
            query="select kodebrg,jumlahbrg,lokasi from barangdet where kodebrg='%s' limit 1"%(kodebrg)
            try:
                dapat=ambilSatuRowSQL(query)
                dapat[0]
            except:
                query="select kodebrg,1,1 from barang where barcode='%s' or kodebrg='%s' limit 1"%(kodebrg,kodebrg)
                try:
                    dapat=ambilSatuRowSQL(query)
                    dapat[0]
                    
                    query="select kodebrg,jumlahbrg,lokasi from barangdet where kodebrg='%s' limit 1"%(dapat[0])
                    try:
                        dapat=ambilSatuRowSQL(query)
                        dapat[0]
#                    except:

                    except:
                        dic={}
                        dic["error"]='false'
                        dic["msg"]=""
                        dic["data"]={}
                        dic["data"]["rows"]=[]
                        strDic="%s"%dic
                        strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                        return Response(strDic, mimetype='application/json')
                except:
                        dic={}
                        dic["error"]='false'
                        dic["msg"]=""
                        dic["data"]={}
                        dic["data"]["rows"]=[]
                        strDic="%s"%dic
                        strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                        return Response(strDic, mimetype='application/json')
    queryBrg="select kodebrg,namabrg,barcode,'%s' jumlah, '%s' lokasi,(select jmlkarton from barangdet where barangdet.kodebrg=barang.kodebrg limit 1) jmlkarton,satuan from barang where kodebrg='%s'"%(dapat[1],dapat[2],dapat[0])
    print queryBrg
    
    infoSat=ambilSatuRowSQL(queryBrg)
    
    dic={}
    dic["error"]='false'
    dic["msg"]=""
    dic["data"]={}
    dic["data"]["rows"]=[]
    
    if 1:
        data1={}
        c=0
        for single2 in ["kodebrg","namabrg","barcode","jumlah","lokasi","jmlkarton","satuan"]:
            try:data1[single2]=infoSat[c]
            except:data1[single2]=""
            c+=1
                
        dic["data"]["rows"].append(data1)
        dic["data"]["total"]=len(dic["data"]["rows"])
        
    
    strDic="%s"%dic
    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

    return Response(strDic, mimetype='application/json')
@app.route("%s/customer"%folderAPI, methods=["GET"])
#@jwt_required
def customer():
    #id1 = get_jwt_identity()
    #print id1
    
    theLimit= request.args.get('itemsPerPage')
    if '%s'%theLimit=="None":theLimit=100
    try:theLimit=int(theLimit)
    except:theLimit=100
    
    strLimit="limit %s"%theLimit
    
    numPage= request.args.get('numberPage')
    if '%s'%numPage=="None":numPage=1
    try:numPage=int(numPage)
    except:numPage=1
    numPage=numPage-1
    strPage="offset %s"%(numPage*theLimit)
    
    strCari= request.args.get('searchNama')
    if '%s'%strCari=="None":strCari="1"
    else:strCari="namacus like '%s%s%s' order by namacus"%('%',strCari,'%')
    
    namaTabel="customer"
    strWhere="where %s %s %s"%(strCari,strLimit,strPage)
    
    listSel=['kodecus','kodekelcus','namacus','alamat','kelurahan','kecamatan','kota','propinsi','kodepos','telp','fax','plafon','pkp','npwp','nppkp','nsfpjk','tglpkp','tempo','jnstran','periode','kirim','namaorg','status','level','kodesales1','kodesales2','kodesales3','kodesales4']
    query="""select kodecus,kodekelcus,namacus,alamat,kelurahan,kecamatan,kota,propinsi,kodepos,telp,fax
        ,plafon,pkp,npwp,nppkp,nsfpjk,tglpkp,tempo,jnstran,periode,kirim,namaorg,status,level,kodesales1
        ,kodesales2,kodesales3,kodesales4
        from %s %s """%(namaTabel,strWhere)
    print query
    
    dic={}
    dic["error"]='false'
    dic["msg"]=""
    dic["data"]={}
    dic["data"]["rows"]=[]
    
    if 1:
        data1={}
        
        for single in ambilBanyakRowSQL(query):
            data1={}
            theCol=len(single)
            
            for single2 in range(theCol):
                strData1='%s'%single[single2]
                strData1=strData1.replace("\"","")
                strData1=strData1.replace("\'","")
                if '%s'%strData1=="None":data1[listSel[single2]]=""
                else:data1[listSel[single2]]=strData1
            
            dic["data"]["rows"].append(data1)
        dic["data"]["total"]=len(dic["data"]["rows"])
        
    
    strDic="%s"%dic
#    strDic=strDic.replace("'",'"').replace('": u','": ').replace(', u"',', "').replace(", u'",", '").replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
#    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

    return Response(strDic, mimetype='application/json')

@app.route("%s/customerAutoCom"%folderAPI, methods=["GET"])
#@jwt_required
def customerAutoCom():
    #id1 = get_jwt_identity()
    #print id1
    
    theLimit=100
    
    strLimit="limit %s"%theLimit
    
    strPage=""
    
    strCari= request.args.get('query')
    if '%s'%strCari=="None":strCari="1"
    else:strCari="namacus like '%s%s%s' order by namacus"%('%',strCari,'%')
    
    namaTabel="customer"
    strWhere="where %s %s %s"%(strCari,strLimit,strPage)
    
    listSel=['data','value']#,'alamat','kelurahan','kecamatan','kota','propinsi','kodepos','telp','fax','plafon','pkp','npwp','nppkp','nsfpjk','tglpkp','tempo','jnstran','periode','kirim','namaorg','status','level','kodesales1','kodesales2','kodesales3','kodesales4']
    query="""select kodecus,namacus from %s %s """%(namaTabel,strWhere)
    print query
    
    dic={}
    dic["error"]='false'
    dic["msg"]=""
    dic["suggestions"]=[]
    
    if 1:
        data1={}
        
        for single in ambilBanyakRowSQL(query):
            data1={}
            theCol=len(single)
            
            for single2 in range(theCol):
                strData1='%s'%single[single2]
                strData1=strData1.replace("\"","")
                strData1=strData1.replace("\'","")
                if '%s'%strData1=="None":data1[listSel[single2]]=""
                else:data1[listSel[single2]]=strData1
            
            dic["suggestions"].append(data1)
#        dic["data"]["total"]=len(dic["data"]["rows"])
        
    
    strDic="%s"%dic
#    strDic=strDic.replace("'",'"').replace('": u','": ').replace(', u"',', "').replace(", u'",", '").replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
#    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

    return Response(strDic, mimetype='application/json')
@app.route("%s/detCustomer"%folderAPI, methods=["GET"])
#@jwt_required
def detCustomer():
    #id1 = get_jwt_identity()
    #print id1
    
    strLimit=""
    strPage=""
    
    strCari= request.args.get('kodeCus')
    if '%s'%strCari=="None":strCari="0"
    else:strCari="kodeCus = '%s' "%(strCari)
    
    namaTabel="customer"
    strWhere="where %s %s %s"%(strCari,strLimit,strPage)
    
    listSel=['kodecus','kodekelcus','namacus','alamat','kelurahan','kecamatan','kota','propinsi','kodepos','telp','fax','plafon','pkp','npwp','nppkp','nsfpjk','tglpkp','tempo','jnstran','periode','kirim','namaorg','status','level','kodesales1','kodesales2','kodesales3','kodesales4']
    query="""select kodecus,kodekelcus,namacus,alamat,kelurahan,kecamatan,kota,propinsi,kodepos,telp,fax
        ,plafon,pkp,npwp,nppkp,nsfpjk,tglpkp,tempo,jnstran,periode,kirim,namaorg,status,level,kodesales1
        ,kodesales2,kodesales3,kodesales4
        from %s %s """%(namaTabel,strWhere)
    print query
    
    dic={}
    dic["error"]='false'
    dic["msg"]=""
    dic["data"]={}
    dic["data"]["rows"]=[]
    
    if 1:
        data1={}
        
        for single in ambilBanyakRowSQL(query):
            data1={}
            theCol=len(single)
            
            for single2 in range(theCol):
                strData1='%s'%single[single2]
                strData1=strData1.replace("\"","")
                strData1=strData1.replace("\'","")
                if '%s'%strData1=="None":data1[listSel[single2]]=""
                else:data1[listSel[single2]]=strData1
            
            dic["data"]["rows"].append(data1)
        dic["data"]["total"]=len(dic["data"]["rows"])
        
    
    strDic="%s"%dic
    #strDic=strDic.replace("'",'"').replace('": u','": ').replace(', u"',', "').replace(", u'",", '").replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
#    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

    return Response(strDic, mimetype='application/json')
@app.route("%s/sales"%folderAPI, methods=["GET"])
#@jwt_required
@app.route("%s/supplierAutoCom"%folderAPI, methods=["GET"])
#@jwt_required
def supplierAutoCom():
    #id1 = get_jwt_identity()
    #print id1
    
    theLimit=100
    
    strLimit="limit %s"%theLimit
    
    strPage=""
    
    strCari= request.args.get('query')
    if '%s'%strCari=="None":strCari="1"
    else:strCari="namarel like '%s%s%s' order by namarel"%('%',strCari,'%')
    
    namaTabel="relasi"
    strWhere="where %s %s %s"%(strCari,strLimit,strPage)
    
    listSel=['data','value']#,'alamat','propinsi','kota','kecamatan','kelurahan','kodepos','telp','fax','acbank','ket','akumulasi','hutang','hgiro','plafon','pkp','npwp','nppkp','nsfpjk','tglpkp','tempo','jnstran','namaorg','sebu1','kontak','sebut2','aktif','status']
    query="""select koderel,namarel from %s %s """%(namaTabel,strWhere)
    print query
    
    dic={}
    dic["error"]='false'
    dic["msg"]=""
    dic["suggestions"]=[]
    
    if 1:
        data1={}
        
        for single in ambilBanyakRowSQL(query):
            data1={}
            theCol=len(single)
            
            for single2 in range(theCol):
                strData1='%s'%single[single2]
                strData1=strData1.replace("\"","")
                strData1=strData1.replace("\'","")
                if '%s'%strData1=="None":data1[listSel[single2]]=""
                else:data1[listSel[single2]]=strData1
            
            dic["suggestions"].append(data1)
#        dic["data"]["total"]=len(dic["data"]["rows"])
        
    
    strDic="%s"%dic
#    strDic=strDic.replace("'",'"').replace('": u','": ').replace(', u"',', "').replace(", u'",", '").replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
#    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

    return Response(strDic, mimetype='application/json')
def sales():
    #id1 = get_jwt_identity()
    #print id1
    
    theLimit= request.args.get('itemsPerPage')
    if '%s'%theLimit=="None":theLimit=100
    try:theLimit=int(theLimit)
    except:theLimit=100
    
    strLimit="limit %s"%theLimit
    
    numPage= request.args.get('numberPage')
    if '%s'%numPage=="None":numPage=1
    try:numPage=int(numPage)
    except:numPage=1
    numPage=numPage-1
    strPage="offset %s"%(numPage*theLimit)
    
    strCari= request.args.get('searchNama')
    if '%s'%strCari=="None":strCari="1"
    else:strCari="namasales like '%s%s%s' order by namasales"%('%',strCari,'%')
    
    namaTabel="sales"
    strWhere="where %s %s %s"%(strCari,strLimit,strPage)
    
    return bikinGetJSONExt(namaTabel,strWhere)
@app.route("%s/pegawai"%folderAPI, methods=["GET"])
#@jwt_required
def pegawai():
    #id1 = get_jwt_identity()
    #print id1
    
    theLimit= request.args.get('itemsPerPage')
    if '%s'%theLimit=="None":theLimit=10
    try:theLimit=int(theLimit)
    except:theLimit=10
    
    strLimit="limit %s"%theLimit
    
    numPage= request.args.get('numberPage')
    if '%s'%numPage=="None":numPage=1
    try:numPage=int(numPage)
    except:numPage=1
    numPage=numPage-1
    strPage="offset %s"%(numPage*theLimit)
    
    strCari= request.args.get('searchNama')
    if '%s'%strCari=="None":strCari="1"
    else:strCari="nama like '%s%s%s' order by nama"%('%',strCari,'%')
    
    namaTabel="pegawai"
    strWhere="where %s %s %s"%(strCari,strLimit,strPage)
    
    return bikinGetJSONExt(namaTabel,strWhere)
@app.route("%s/inputBarangBaruAutoCom"%folderAPI, methods=["GET"])
#@jwt_required
def inputBarangBaruAutoCom():
    #id1 = get_jwt_identity()
    #print id1
    theLimit=10
    
    strLimit="limit %s"%theLimit
    
    strPage=""
    
    strCari= request.args.get('query')
    if '%s'%strCari=="None":strCari="1"
    else:strCari="namabrg like '%s%s%s' order by namabrg"%('%',strCari,'%')
    
    namaTabel="barang"
    strWhere="where %s %s %s"%(strCari,strLimit,strPage)
    
    listSel=["kodebrg","namabrg","barcode","kodebrgpack","kodebrgkarton"]#,"merk","stok","satuan","hbeli","hjual","hjual1","hjual2","hjual3","hjual4","hjual5","kodejen"]
    query="""select kodebrg,trim(namabrg) namabrg,barcode,(select kodebrgpack from barangdet where barangdet.kodebrg=barang.kodebrg limit 1),(select kodebrgkarton from barangdet where barangdet.kodebrg=barang.kodebrg limit 1) from barang %s """%(strWhere)
    print query
    
    dic={}
    dic["error"]='false'
    dic["msg"]=""
    dic["suggestions"]=[]
#    dic["data"]["rows"]=[]
    
    if 1:
        data1={}
        
        for single in ambilBanyakRowSQL(query):
            data1={}
            theCol=len(single)
            
            for single2 in range(theCol):
                strData1='%s'%single[single2]
                strData1=strData1.replace("\"","")
                strData1=strData1.replace("\'","")
                if '%s'%strData1=="None":data1[listSel[single2]]=""
                else:data1[listSel[single2]]=strData1
            
            dic["suggestions"].append(data1)
#        dic["data"]["total"]=len(dic["data"]["rows"])
        
    
    strDic="%s"%dic
#    strDic=strDic.replace("'",'"').replace('": u','": ').replace(', u"',', "').replace(", u'",", '").replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
#    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
    
#    print strDic
    
    return Response(strDic, mimetype='application/json')

       
if 1:# GET
        
      
    
        @app.route('%s/getCustomer'%(folderAPI), methods=['GET'])
        def getCustomer():
#            namaTabel="proyek"
            namaTabel="customer"
            
            if request.method == 'GET':
                
                id1= request.args.get('kodecus')
                
                strWhere="where kodecus='%s'"%id1
                return bikinGetJSONExt(namaTabel,strWhere)
            
        @app.route('%s/getPickingDet'%(folderAPI), methods=['GET', 'PUT'])
        def getPickingDet():
#            namaTabel="proyek"
            namaTabel="pickingdet"
            
            if request.method == 'GET':
                
                id1= request.args.get('noso')
          
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                query="select 'belum' from dsalesorder where noso='%s' and (stat1='' or stat1 is null) "%(id1)
                try:stat1=ambilSatuRowSQL(query)[0]
                except:stat1=""
                if stat1!="belum":
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="RESI Sudah Selesai"
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')   
                
                query="select noso,count(noso) from dsalesorder where noso='%s' and stat1='' group by noso "%id1
                print query
                try:jmlItem=int(ambilSatuRowSQL(query)[1])
                except:jmlItem=1
                jmlItem-=1;
                print "ini jmlItem ",jmlItem
                curs.execute(query)
                if curs.rowcount==0:
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Nota SO Tidak Ditemukan"
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')   
     
                query="""select id,CONVERT((jumlahbarang), SIGNED)jumlahbarang,CONVERT((SELECT jmlkarton FROM barangdet 
                    WHERE kodebrg=kodebarang LIMIT 1), SIGNED)jmlkarton from dsalesorder where noso='%s' and stat3='' having jumlahbarang>=jmlkarton 
                    order by jumlahbarang desc"""%id1
                curs.execute(query)
                if curs.rowcount>0:
                    dapat=ambilBanyakRowSQL(query)
                    for single in dapat:
                        query="update dsalesorder set stat3='karton' where id='%s'"%single[0]
                        curs.execute(query)
                        #print "masuk"
            
                              
                conn2.commit()
                curs.close()
                
                query="select count(*) from dsalesorder where noso='%s' and stat2!='' group by noso"%id1
                try:jumlahorder=int(ambilSatuRowSQL(query)[0])
                except:jumlahorder=0
                jumlahorder+=1
                
                strWhere="where noso='%s' limit 1"%id1   
                query="""select %s jmlitem,%s jumlahorder from dsalesorder"""%(jmlItem,jumlahorder)
                dataCol=["jmlitem","jumlahorder"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
                
        
        @app.route('%s/getSupplier'%(folderAPI), methods=['GET'])
        def getSupplier():
#            namaTabel="proyek"
            namaTabel="relasi"
            
            if request.method == 'GET':
                
                id1= request.args.get('kodesup')
                
                strWhere=""#"where koderel='%s'"%id1
                
                query="select namarel,koderel from relasi where koderel='%s' "%id1
                dataCol=["namarel","koderel"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
                #return bikinGetJSONExt(namaTabel,strWhere)
                
        @app.route('%s/getDstoklokasi'%(folderAPI), methods=['GET'])
        def getDstoklokasi():
#            namaTabel="proyek"
            namaTabel="dstoklokasi"
            
            if request.method == 'GET':
                
                id1= request.args.get('kodebarang')
                
                conn=mysql.get_db()
                theCon=conn.cursor()
                query="select kodebrg from barangdet where kodebrg='%s' or kodebrgpack='%s' or kodebrgkarton='%s'"%(id1,id1,id1)
                theCon.execute(query)
                if theCon.rowcount==0:
                    query="select kodebrg from barang where barcode='%s'"%id1
                    theCon.execute(query)
                    if theCon.rowcount==0:
                        query="select kodebarang from dstoklokasi where kodebarangkarton='%s'"%(id1)
                        theCon.execute(query)
                        if theCon.rowcount==0:
                            data1={}
                            dic={}
                            dic["error"]='true'
                            dic["msg"]="Kode Barang Tidak Ada"
                            theCon.close()
                            strDic="%s"%dic
                            strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                            return Response(strDic, mimetype='application/json')
                     
                dapat=ambilSatuRowSQL(query)[0]
                query="select trim(kodebarang) from dstoklokasi where jumlahbarang>0 and kodebarang='%s'"%(dapat)
                theCon.execute(query)
                if theCon.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Tidak Ada Stok Karton Dan Lepasan"
                    theCon.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')

   
                conn.commit()
                theCon.close()
                
                query="select convert(sum(jumlahbarang), CHAR)jmlpcs,lokasi from dstoklokasi where kodebarang='%s' and jumlahbarang>0 and satuan='' group by kodebarang"%dapat
                try:jmlPcs=ambilSatuRowSQL(query)[0]
                except:jmlPcs=0
                try:lokasilepasan=ambilSatuRowSQL(query)[1]
                except:lokasilepasan=""
                
                query="select convert(sum(jumlahbarang), CHAR)jmlkarton from dstoklokasi where kodebarang='%s' and jumlahbarang>0 and satuan='karton' group by kodebarang"%(dapat)
                try:jmlKarton=ambilSatuRowSQL(query)[0]
                except:jmlKarton=0
             
                if jmlKarton>0:
                    strWhere="where kodebarang='%s' and jumlahbarang>0 and satuan='karton'"%dapat
                    query="""select lokasi,kodebarang,kodebarangkarton,satuan,'%s' lokasilepasan,%s jmlPcs,%s jmlKarton, (select namabrg from barang where kodebrg=kodebarang limit 1),
                        (select satuan from barang where kodebrg=kodebarang limit 1),jumlahbarang from dstoklokasi"""%(lokasilepasan,jmlPcs,jmlKarton)
                else:
                    strWhere="where kodebarang='%s' and jumlahbarang>0 and satuan=''"%dapat
                    query="""select lokasi,kodebarang,kodebarangkarton,satuan,'%s' lokasilepasan,%s jmlPcs,%s jmlKarton, (select namabrg from barang where kodebrg=kodebarang limit 1),
                        (select satuan from barang where kodebrg=kodebarang limit 1),jumlahbarang from dstoklokasi"""%(lokasilepasan,jmlPcs,jmlKarton)
                
                dataCol=["lokasi","kodebarang","kodebarangkarton","satuankarton","lokasilepasan","jmlPcs","jmlKarton","namabarang","satuan","jumlahbarang"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
                #return bikinGetJSONExt(namaTabel,strWhere)
                
        @app.route('%s/getLokasiDstok'%(folderAPI), methods=['GET'])
        def getLokasiDstok():
#            namaTabel="proyek"
            namaTabel="dstoklokasi"
            
            if request.method == 'GET':
                
                id1= request.args.get('lokasi')
                
                strWhere="where lokasi='%s' and jumlahbarang>0 group by kodebarang"%(id1)
                query="select * from dstoklokasi %s"%strWhere
                print query
                
                conn=mysql.get_db()
                theCon=conn.cursor()
                theCon.execute(query)
                if theCon.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Lokasi Tidak Ditemukan Tidak Ada"
                    theCon.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
                
                query="""select lokasi,kodebarang,kodebarangkarton,satuan,CONVERT((sum(jumlahbarang)), SIGNED)jumlahbarang,
                    (select namabrg from barang where kodebrg=kodebarang limit 1),
                    (select satuan from barang where kodebrg=kodebarang limit 1),(select jmlkarton from barangdet where kodebrg=kodebarang limit 1) 
                    from dstoklokasi"""
                dataCol=["lokasi","kodebarang","kodebarangkarton","satuankarton","jumlahbarang","namabarang","satuan","jmlkarton"]
                print query
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
                #return bikinGetJSONExt(namaTabel,strWhere)
                 

if 1:# SALES ORDER
        @app.route('%s/getHSO'%(folderAPI), methods=['GET', 'POST'])
        def getHSO():
#            namaTabel="proyek"
            namaTabel="hsalesorder"
            
            if request.method == 'GET':
                
                
                if 1:#'%s'%id1!="None":
                    id1= request.args.get('noso')
                    
                    strWhere="where noso='%s'"%id1
                    
                    return bikinGetJSONExt(namaTabel,strWhere)
        @app.route('%s/getHSORange'%(folderAPI), methods=['GET', 'POST'])
        def getHSOTange():
#            namaTabel="proyek"
            namaTabel="hsalesorder"
            
            if request.method == 'GET':
                
                
                if 1:#'%s'%id1!="None":
                    tglA= request.args.get('tglA')
                    tglB= request.args.get('tglB')
                    id1= request.args.get('id1')
                    prioritas= request.args.get('prioritas')
                    
                    strPrio="1"
                    if prioritas=="1":strPrio="prioritas='true'"
                    if prioritas=="0":strPrio="prioritas='false'"
                    
                    theLimit= request.args.get('itemsPerPage')
                    if '%s'%theLimit=="None":theLimit=100
                    try:theLimit=int(theLimit)
                    except:theLimit=100
                    
                    strLimit="limit %s"%theLimit
                    
                    numPage= request.args.get('numberPage')
                    if '%s'%numPage=="None":numPage=1
                    try:numPage=int(numPage)
                    except:numPage=1
                    numPage=numPage-1
                    strPage="offset %s"%(numPage*theLimit)
                    
                    strWhere="where tanggal between '%s' and '%s' and %s and namacustomer like '%s%s%s' %s %s"%(tglA,tglB,strPrio,'%',id1,'%',strLimit,strPage)
                    return bikinGetJSONExt(namaTabel,strWhere)
                
        @app.route('%s/getDSO'%(folderAPI), methods=['GET', 'POST'])
        def getDSO():
#            namaTabel="proyek"
            namaTabel="dsalesorder"
            
            if request.method == 'GET':
                
                
                if 1:#'%s'%id1!="None":
                    id1= request.args.get('noso')
                    
                    strWhere="where noso='%s'"%id1
                    
                    return bikinGetJSONExt(namaTabel,strWhere)
        
        @app.route('%s/getDSOScan'%(folderAPI), methods=['GET', 'PUT'])
        def getDSOscan():
#            namaTabel="proyek"
            namaTabel="dsalesorder"
            
            if request.method == 'GET':
                
                id1= request.args.get('noso')
                ind1= request.args.get('index')
                
                dic={}
                dic["error"]='false'
                dic["msg"]=""
                dic["data"]={}
                dic["data"]["rows"]=[]
                
                #strKode="('-'"
                #for single in listKodeEval:strKode+=",'%s'"%single
                #strKode+=")"
                
                query="select count(*) from %s where noso='%s'"%(namaTabel,id1)
                try:dapatMax=int(ambilSatuRowSQL(query)[0])
                except:dapatMax=0
                
                query="select trim(kodebarang),id,jumlahbarang,(select jmlkarton from barangdet where kodebrg=kodebarang limit 1)jmlbrg,stat3 from %s where noso='%s'"%(namaTabel,id1)
                dapat=ambilBanyakRowSQL(query)
             
                strKBK=""
                strKB="('-'"
                for single in dapat:
                    int1 = int(single[2])
                    int2 = int(single[3])
                    try:int2=int(single[3])
                    except:int2=3000
                    #print int1,int2
                    if int1>=int2:
                        strKBK+=",'%s'"%single[1]
                    else:
                        strKB+=",'%s'"%single[0]
                strKB+=")"
          
                query="select kodebarang,(select id from dsalesorder where dsalesorder.kodebarang=dstoklokasi.kodebarang and stat3='' and noso='%s' limit 1),(select jmlkarton from barangdet where kodebrg=kodebarang limit 1) from dstoklokasi where kodebarang in %s and satuan='' group by kodebarang order by lokasi"%(id1,strKB)
                print query
                dapat=ambilBanyakRowSQL(query)
                strKB="order by field(id"
                for single in dapat:
                    strKB+=",'%s'"%single[1]
                strKB+=strKBK
                strKB+=")"
             
                query="""select (select trim(if(barcode='',idbarang,barcode))from barang where kodebrg= kodebarang limit 1)
                    ,namabarang,jumlahbarang,%s urutan, %s jmlItem,trim(kodebarang),(select satuan from barang where kodebrg= kodebarang limit 1)
                    from %s where noso ='%s' %s limit 1 offset %s
                    """%(ind1,dapatMax,namaTabel,id1,strKB,ind1)
                print query
                
                listSel=["kodebarang",'namabarang','jumlahbarang',"urutan",'jmlItem',"Kode","satuan"]
             
                for single in ambilBanyakRowSQL(query):
                    data1={}
                    theCol=len(single)
                    try:jb1=int(single[2])
                    except:jb1=0
                    
                    for single2 in range(theCol):
                        if '%s'%single[single2]=="None":data1[listSel[single2]]=""
                        else:data1[listSel[single2]]=single[single2]
                    
#                       print single[0]
                    
                    try:theLok=dataLokasi[single[5].lower()][0]
                    except:theLok=""
                    
                    data1['lokasi']=theLok#"lokasi"
                    queryBrg="select jumlahbrg,kodebrgpack,jmlpack,kodebrgkarton,jmlkarton,lokasikrtn from barangdet where kodebrg='%s'"%single[5]
                    
                    print queryBrg,jb1,
                    infoSat=[]
                    for single2 in ambilSatuRowSQL(queryBrg):infoSat.append(single2)
                    
                 
                    try:jmlKarton=int(infoSat[4])
                    except:jmlKarton=0
                    print jmlKarton
                    karton=0
                    if jb1>=jmlKarton:
                        query1="select lokasi from dstoklokasi where kodebarang='%s' and jumlahbarang>0 and satuan='karton'"%(single[5])
                        karton=1
                    else:
                        query1="select lokasi from dstoklokasi where kodebarang='%s' and jumlahbarang>0 and lokasi not like 'b%s' and satuan=''"%(single[5],"%")
                    print query1
                    
                    #LANGKAH INI UNTUK MENGURANGI STOK LEPASAN
                    conn2=mysql.get_db()
                    curs=conn2.cursor()
                    
                    curs.execute(query1)
                    if curs.rowcount>0:
                        lokasi=ambilSatuRowSQL(query1)[0]
                        #klo ketemu, lokasi di isi yang REAL dan MOTONG STOK
                        infoSat[5]=lokasi
                        data1['lokasi']=lokasi
                        
#                                query="update dstoklokasi set jumlahbarang=jumlahbarang-1 where kodebarang='%s' and lokasi='%s' and jumlahbarang>0"%(kodebrg,lokasi)
#                                print query
                        
                    curs.close()
                    
                    c=0
                    for single2 in ["jumlahbrg","kodebrgpack","jmlpack","kodebrgkarton","jmlkarton","lokasikrtn"]:
                        try:data1[single2]=infoSat[c]
                        except:data1[single2]=""
                        c+=1
                        
                    dic["data"]["rows"].append(data1)
                    
                dic["data"]["total"]=len(dic["data"]["rows"])
                
                strDic="%s"%dic
#                strDic=strDic.replace("'",'"').replace('": u','": ').replace(', u"',', "').replace(", u'",", '").replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
            #    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json')
            
            if request.method == 'PUT':
                
                dic={}
                dic["error"]='false'
                dic["msg"]=""
                dic["data"]={}
                dic["data"]["rows"]=[]
                
                id1= request.args.get('noso')
                ind1= request.args.get('index')
                jml= request.args.get('jumlahScan')
                picker= request.args.get('picker')
                id2 = request.args.get('jumlahorder')
                lokasi = request.args.get('lokasi')
                kodebarang = request.args.get('kodebar')
                jml2 = request.args.get('jmlScanKarton')
                if '%s'%jml2=="None":jml2="1"
                
                query="select trim(kodebarang),id,jumlahbarang,(select jmlkarton from barangdet where kodebrg=kodebarang limit 1)jmlbrg,stat3 from %s where noso='%s'"%(namaTabel,id1)
                dapat=ambilBanyakRowSQL(query)
             
                dataKB={}
                 
                strKBK=""
                strKB="('-'"
                for single in dapat:
                    int1 = int(single[2])
                    int2 = int(single[3])
                    try:int2=int(single[3])
                    except:int2=3000
                    #print int1,int2
                    if int1>=int2:
                        dataKB[single[0].lower()]=[single[3]]
                        strKBK+=",'%s'"%single[1]
                        dataKB[single[0].lower()]=[single[3]]
                    else:
                        dataKB[single[0].lower()]=[single[3]]
                        strKB+=",'%s'"%single[0]
                        dataKB[single[0].lower()]=[single[3]]
                
                strKB+=")"
                
                query="select kodebarang,(select id from dsalesorder where dsalesorder.kodebarang=dstoklokasi.kodebarang and stat3='' and noso='%s' limit 1),(select jmlkarton from barangdet where kodebrg=kodebarang limit 1) from dstoklokasi where kodebarang in %s and satuan='' group by kodebarang order by lokasi"%(id1,strKB)
                print query
                dapat=ambilBanyakRowSQL(query)
                strKB="order by field(id"
                for single in dapat:
                    strKB+=",'%s'"%single[1]
                strKB+=strKBK
                strKB+=")"
                 
                query="select id,trim(kodebarang),jumlahbarang from %s where noso ='%s' %s limit 1 offset %s "%(namaTabel,id1,strKB,ind1)
                dapatNSO=ambilSatuRowSQL(query)
                try:idSO=dapatNSO[0]
                except:idSO=""
                
                try:kodebrg=dapatNSO[1]
                except:kodebrg=""
                
                try:jb1=int(dapatNSO[2])
                except:jb1=""
                queryStok="select 1"
                
                try:jmlKarton=int(dataKB[kodebrg.lower()][0])
                except:jmlKarton=1
                try:jmlKarton2=int(jml)
                except:jmlKarton2=1
                karton=0
                if jmlKarton2>=jmlKarton:
                    query1="select lokasi from dstoklokasi where kodebarang='%s' and jumlahbarang>0 and satuan='karton'"%(kodebrg)
                    karton=1
                else:
                    query1="select lokasi from dstoklokasi where kodebarang='%s' and jumlahbarang>0 and satuan=''"%(kodebrg)
               
                #LANGKAH INI UNTUK MENGURANGI STOK LEPASAN
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                curs.execute(query1)
                if curs.rowcount>0:
                    lokasi=curs.fetchone()[0]
                    #klo ketemu, lokasi di isi yang REAL dan MOTONG STOK
#                            infoSat[5]=lokasi
                    
                    if karton:
                  
                        jmlTot=int(jml2)
    
                        query="select iddstoklokasi, jumlahbarang from dstoklokasi where kodebarang='%s' and lokasi='%s' and jumlahbarang>0 and satuan='karton' order by iddstoklokasi"%(kodebrg,lokasi)
                        dataBrgPO={}
                        for single in ambilBanyakRowSQL(query):
                            dataBrgPO[single[0]]=[single[1]]
            
                        
                        getId=0
                        
                        for single in dataBrgPO:
                            jmlRun=dataBrgPO[single][0]
                            idpodet=single
                            lagi=0
                            getId=0
                            if jmlRun>=jmlTot:  
                                query="update dstoklokasi set jumlahbarang=jumlahbarang-0 where iddstoklokasi='%s'"%(jmlTot,idpodet)
                                curs.execute(query)
                                lagi=1
                                getId=1
                            else:
                                query="update dstoklokasi set jumlahbarang=jumlahbarang-0 where iddstoklokasi='%s'"%(jmlRun,idpodet)
                                curs.execute(query)
                                jmlTot=jmlTot-jmlRun
                                lagi=0
                            
                            if lagi:break
                        
                    else:
                                         
                        jmlTot=int(jml)
                     
                        query="select iddstoklokasi, jumlahbarang from dstoklokasi where  kodebarang='%s' and lokasi='%s' and jumlahbarang>0 and satuan='' order by iddstoklokasi desc"%(kodebrg,lokasi)
                    
                    
                        cekSO=ambilSatuRowSQL(query)
                        dataBrgPO={}
                        for single in ambilBanyakRowSQL(query):
                            dataBrgPO[single[0]]=[single[1]]
                      
                        if 1:
                            for single in dataBrgPO:
                                jmlRun=dataBrgPO[single][0]
                                idpodet=single
                                lagi=0
                                getId=0
                                if jmlRun>=jmlTot:  
                                    query="update dstoklokasi set jumlahbarang=jumlahbarang-%s where iddstoklokasi='%s'"%(jmlTot,idpodet)
                                    curs.execute(query)
                                    lagi=1
                                    getId=1
                                else:
                                    query="update dstoklokasi set jumlahbarang=jumlahbarang-%s where iddstoklokasi='%s'"%(jmlRun,idpodet)
                                    curs.execute(query)
                                    jmlTot=jmlTot-jmlRun
                                    lagi=0
                                
                                if lagi:break
                        
                            
                    print query
        
                query="update %s set jml1='%s',stat1='picking',stat4=now(),stat2='%s' where id='%s'"%(namaTabel,jml,picker,idSO)
                print query
                
                conn2=mysql.get_db()
                theCon=conn2.cursor()
                theCon.execute(query)
                
                #query="insert into rekampicking (lokasi,noso,jumlahambil,kodebarang,tanggal,operator) values ('%s','%s','%s','%s',now(),'%s')"%(lokasi,id1,jml,kodebarang,picker)
                theCon.execute(query)
                conn2.commit()
                theCon.close()
                    
                
                strDic="%s"%dic
#                strDic=strDic.replace("'",'"').replace('": u','": ').replace(', u"',', "').replace(", u'",", '").replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
            #    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json')
            
        @app.route('%s/inputSO'%(folderAPI), methods=['GET', 'POST'])
        def inputSO():
#            namaTabel="proyek"
            namaTabel="hsalesorder"
            namaTabel2="dsalesorder"
            
            if request.method == 'GET':
                
                
                if 1:#'%s'%id1!="None":
                    id1= request.args.get('noso')
                    
                    strWhere="where noso='%s'"%id1
                    
                    return bikinGetJSONExt(namaTabel,strWhere)
            
            if request.method == 'POST':
                #print "post"
                dapat= request.get_json()
                dapat1= request.get_json()
                
                print dapat
                dapatHead=dapat['header']
                print dapatHead
                autoAddTabel(namaTabel,dapatHead)
                query="insert into %s ( "%namaTabel
                
                for single in dapatHead:query+="%s,"%single
                query=query[0:len(query)-1]
                query+=") values ( "
                
                for single in dapatHead:query+="'%s',"%dapatHead[single]
                query=query[0:len(query)-1]
                query+=")"
                
                print query
                
                conn2=mysql.get_db()
                theCon=conn2.cursor()
                theCon.execute(query)
                conn2.commit()
                theCon.close()
                    


                dapatDet=dapat['detail']
                
                for single in dapatDet:
                    autoAddTabel(namaTabel2,single)
                    dapat=single
                    query="insert into %s ( "%namaTabel2
                    
                    for single in dapat:query+="%s,"%single
                    query=query[0:len(query)-1]
                    query+=") values ( "
                    
                    for single in dapat:query+="'%s',"%dapat[single]
                    query=query[0:len(query)-1]
                    query+=")"
                    
                    print query
                
                    conn2=mysql.get_db()
                    theCon=conn2.cursor()
                    theCon.execute(query)
                    conn2.commit()
                    theCon.close()
                    
                ok2="""{"error":"false","msg":"Berhasil","data":%s}"""%"''"
                ok2=ubahJadiJSONfix(ok2)
                return Response(ok2, mimetype='application/json')
        @app.route('%s/inputSOIdx'%(folderAPI), methods=['GET', 'POST'])
        def inputSOIdx():
#            namaTabel="proyek"
            namaTabel="hsalesorder"
            namaTabel2="dsalesorder"
            
            
            if request.method == 'POST':
                #print "post"
                dapat= request.get_json()
                dapat1= request.get_json()
                
                print dapat
                dapatHead=eval(dapat[0])
                print dapatHead
                
#                return
                
                autoAddTabel(namaTabel,dapatHead)
                query="insert into %s ( "%namaTabel
                
                for single in dapatHead:query+="%s,"%single
                query=query[0:len(query)-1]
                query+=") values ( "
                
                for single in dapatHead:query+="'%s',"%dapatHead[single]
                query=query[0:len(query)-1]
                query+=")"
                
                print query
                
                conn2=mysql.get_db()
                theCon=conn2.cursor()
                theCon.execute(query)
                conn2.commit()
                theCon.close()
                    


                dapatDet=eval(dapat[1])
                
                for single in dapatDet:
                    autoAddTabel(namaTabel2,single)
                    dapat=single
                    query="insert into %s ( "%namaTabel2
                    
                    for single in dapat:query+="%s,"%single
                    query=query[0:len(query)-1]
                    query+=") values ( "
                    
                    for single in dapat:query+="'%s',"%dapat[single]
                    query=query[0:len(query)-1]
                    query+=")"
                    
                    print query
                
                    conn2=mysql.get_db()
                    theCon=conn2.cursor()
                    theCon.execute(query)
                    conn2.commit()
                    theCon.close()
                    
                ok2="""{"error":"false","msg":"Berhasil","data":%s}"""%"''"
                ok2=ubahJadiJSONfix(ok2)
                return Response(ok2, mimetype='application/json')
        @app.route('%s/inputSOIdxPotongStok'%(folderAPI), methods=['GET', 'POST'])
        def inputSOIdxPotongStok():
#            namaTabel="proyek"
            namaTabel="hsalesorder"
            namaTabel2="dsalesorder"
            
            
            if request.method == 'POST':
                #print "post"
                dapat= request.get_json()
                dapat1= request.get_json()
                
                print dapat
                dapatHead=eval(dapat[0])
                print dapatHead
                
#                return
                
                autoAddTabel(namaTabel,dapatHead)
                query="insert into %s ( "%namaTabel
                
                for single in dapatHead:query+="%s,"%single
                query=query[0:len(query)-1]
                query+=") values ( "
                
                for single in dapatHead:query+="'%s',"%dapatHead[single]
                query=query[0:len(query)-1]
                query+=")"
                
                print query
                
                conn2=mysql.get_db()
                theCon=conn2.cursor()
                theCon.execute(query)
                conn2.commit()
                theCon.close()
                    


                dapatDet=eval(dapat[1])
                
                for single in dapatDet:
                    autoAddTabel(namaTabel2,single)
                    dapat=single
                    query="insert into %s ( "%namaTabel2
                    
                    idx1=""
                    lokasi=""
                    jml1=0
                    c=0
                    for single in dapat:
                        if single.lower()=='lokasi':
                            idx1=c
                            lokasi=dapat[single]
                        elif single.lower()=='jml1':
                            jml1=dapat[single]
                            
                        else:query+="%s,"%single

                        c+=1
                    query=query[0:len(query)-1]
                    query+=") values ( "
                    c=0
                    for single in dapat:
                        if c==idx:1
                        else:query+="'%s',"%dapat[single]
                        c+=1
                    query=query[0:len(query)-1]
                    query+=")"
                    
                    print query
                
                    conn2=mysql.get_db()
                    theCon=conn2.cursor()
                    theCon.execute(query)
                    query="select iddstoklokasi, jumlahbarang from dstoklokasi where  kodebarang='%s' and lokasi='%s' and jumlahbarang>0 order by iddstoklokasi"%(kodebrg,lokasi)
                        #print query
                        
                    dataBrgPO={}
                    for single in ambilBanyakRowSQL(query):
                        dataBrgPO[single[0]]=[single[1]]
                    
                    try:jmlTot=int(jumlahbarang)
                    except:jmlTot=0
                    
                    jmlTot=jb1
                    
                    for single in dataBrgPO:
                        jmlRun=dataBrgPO[single][0]
                        lagi=0
                        if jmlRun>=jmlTot:
                            jmlRun=jmlTot
                            lagi=1
                        else:
                            jmlTot=jmlTot-jmlRun
                            
                        idpodet=single
                        query="update dstoklokasi set jumlahbarang=jumlahbarang-%s where iddstoklokasi='%s'"%(jmlRun,idpodet)
                        #print query
                        
                        curs.execute(query)
                        if lagi:break
                    theCon.execute(query)
                    
                    conn2.commit()
                    theCon.close()
                    
                ok2="""{"error":"false","msg":"Berhasil","data":%s}"""%"''"
                ok2=ubahJadiJSONfix(ok2)
                return Response(ok2, mimetype='application/json')

if 1:# PICKING
        @app.route('%s/pickingResi'%(folderAPI), methods=['GET', 'PUT'])
        def pickingResi():
#            namaTabel="proyek"
            namaTabel="dsalesorder"
            
            if request.method == 'GET':
                
                id1= request.args.get('noso')
                ind1= request.args.get('index')
                
                
                strWhere=""
                
                dic={}
                dic["error"]='false'
                dic["msg"]=""
                dic["data"]={}
                dic["data"]["rows"]=[]
                
                conn=mysql.get_db()
                theCon=conn.cursor()
             
                
                query="select trim(kodebarang),id,stat3 from %s where noso='%s' and stat1='' order by stat3"%(namaTabel,id1)
                theCon.execute(query)
                if theCon.rowcount>0:
                    dapat=ambilBanyakRowSQL(query)
                    print dapat
                    strKB="('-'"
                    strID="('-'"
                    for single in dapat:
                        if single[2]=="":
                            strKB+=",'%s'"%single[0]
                        strID+=",'%s'"%single[1]
                    strID+=")"
                    strKB+=")"
                 
                    query="select namabarang,jumlahbarang,trim(kodebarang),id,stat3 from %s where noso='%s' and stat1='' order by stat3 limit %s,1"%(namaTabel,id1,ind1)
                    print query
                    dataSO=ambilBanyakRowSQL(query)
                    for single in dataSO:
                        if single[4]: #KARTONAN
                            strNol = "'0.0%'"
                            strDel = "'8.%'"
                            query="""select iddstoklokasi,kodebarang,lokasi from dstoklokasi where kodebarang='%s' 
                                and satuan='karton' and jumlahbarang>0 and lokasi not like %s and lokasi not like %s order by tglmasuk desc limit 1"""%(single[2],strNol,strDel)
                            theCon.execute(query)
                            if theCon.rowcount==0:
                                query="""select iddstoklokasi,kodebarang,lokasi from dstoklokasi where kodebarang='%s' 
                                    and satuan='karton' and jumlahbarang>0 order by tglmasuk desc limit 1"""%(single[2])
                                theCon.execute(query)
                                if theCon.rowcount==0:
                                    query="""select iddstoklokasi,kodebarang,lokasi from dstoklokasi where kodebarang='%s' 
                                        and satuan='karton' and lokasi not like %s and lokasi not like %s order by tglMasuk desc limit 1"""%(single[2],strNol,strDel)
                                    theCon.execute(query)
                                    if theCon.rowcount==0:
                                        query="""select iddstoklokasi,kodebarang,lokasi from dstoklokasi where kodebarang='%s' 
                                            and satuan='karton' and lokasi not like %s order by tglMasuk desc limit 1"""%(single[2],strNol)
                                        theCon.execute(query)
                                        if theCon.rowcount==0:
                                            query="""select iddstoklokasi,kodebarang,lokasi from dstoklokasi where kodebarang='%s' 
                                                and satuan='karton' order by tglMasuk desc limit 1"""%(single[2])
                                            theCon.execute(query)
                                            if theCon.rowcount==0:
                                                conn.commit()
                                                theCon.close()
                                                query="select namabarang,jumlahbarang,id,trim(kodebarang),0 lokasi,0 stok,0 stokkarton from dsalesorder where id='%s' "%(single[3])
                                                dataCol=["namabarang","jumlahbarang","iddsalesorder","kodebarang","lokasi","stok","stokkarton"]
                                                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
                                            
                            dapat=ambilSatuRowSQL(query)
                            query="select CONVERT((sum(jumlahbarang)), SIGNED)jumlahbarang from dstoklokasi where kodebarang='%s' and satuan='' group by kodebarang"%(dapat[1])
                            try:stok=ambilSatuRowSQL(query)[0]
                            except:stok=0
                            
                            query="select CONVERT((sum(jumlahbarang)), SIGNED)jumlahbarang from dstoklokasi where kodebarang='%s' and lokasi='%s' and satuan='karton' group by lokasi"%(dapat[1],dapat[2])
                            try:stokkarton=ambilSatuRowSQL(query)[0]
                            except:stokkarton=0
                            
                            conn.commit()
                            theCon.close()
                            query="""select '%s' nama, %s jmlbrg,%s id,trim(kodebarang),lokasi,%s stok, %s stokkarton from dstoklokasi 
                                where iddstoklokasi='%s'"""%(single[0],single[1],single[3],stok,stokkarton,dapat[0])
                            dataCol=["namabarang","jumlahbarang","iddsalesorder","kodebarang","lokasi","stok","stokkarton"]
                            return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
                            
                        else: #LEPASAN
                            strB = "'B%'"
                            strL = "'0.0%'"
                            
                            #KALAU JUMLAH BARANG ADA YANG LEBIH DARI 0
                            query="""select trim(kodebarang),lokasi from dstoklokasi where kodebarang in %s and satuan=''
                                and lokasi not like %s and jumlahbarang>0 ORDER BY lokasi ASC, tglMasuk desc limit %s,1"""%(strKB,strB,ind1)
                            theCon.execute(query)
                            if theCon.rowcount==0:
                                #KALAU STOK 0 CARI LOKASI YANG BUKAN 0.00.00.0.0
                                query="""select trim(kodebarang),lokasi,0 stok from dstoklokasi where kodebarang in %s and satuan=''
                                    and lokasi not like %s and lokasi not like %s ORDER BY lokasi ASC, tglMasuk desc limit %s,1"""%(strKB,strB,strL,ind1)
                                theCon.execute(query)
                                if theCon.rowcount==0:
                                    #KALAU STOK HABIS, YANG PENTING ADA RIWAYAT LOKASI WALAUPUN 0.00.00.0.0
                                    query="""select trim(kodebarang),lokasi,0 stok from dstoklokasi where kodebarang in %s and satuan=''
                                        and lokasi not like %s ORDER BY lokasi ASC, tglMasuk desc limit %s,1"""%(strKB,strB,ind1)
                                    theCon.execute(query)
                                    if theCon.rowcount==0:
                                        #BELUM PERNAH ADA MASUK DSTOKLOKASI
                                        query="""select trim(kodebarang) from dsalesorder where kodebarang in %s and not exists 
                                            (select 1 from dstoklokasi where dsalesorder.kodebarang=dstoklokasi.kodebarang and satuan='' and lokasi not like %s)
                                            and noso='%s' and stat1='' order by stat3 limit 1"""%(strKB,strB,id1)
                                        dapat=ambilSatuRowSQL(query)
                                        query="""select namabarang,jumlahbarang,id,trim(kodebarang),'' lokasi,0 stok,0 stokkarton from dsalesorder where noso='%s' 
                                            and kodebarang=%s and stat3=''"""%(id1,dapat[0])
                                        dataCol=["namabarang","jumlahbarang","iddsalesorder","kodebarang","lokasi","stok","stokkarton"]
                                        conn.commit()
                                        theCon.close()
                                        return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
                            conn.commit()
                            theCon.close()
                            dapat=ambilSatuRowSQL(query)
                            query="select CONVERT((sum(jumlahbarang)), SIGNED)jumlahbarang from dstoklokasi where kodebarang='%s' and lokasi='%s' group by lokasi"%(dapat[0],dapat[1])
                            try:stok=ambilSatuRowSQL(query)[0]
                            except:stok=0
                            
                            query="select CONVERT((sum(jumlahbarang)), SIGNED)jumlahbarang from dstoklokasi where kodebarang='%s' and satuan='karton' group by kodebarang"%(dapat[0])
                            try:stokkarton=ambilSatuRowSQL(query)[0]
                            except:stokkarton=0

                            query="""select namabarang,jumlahbarang,id,trim(kodebarang),'%s' lokasi,%s stok,%s stokkarton from dsalesorder where noso='%s'
                                and kodebarang=%s and stat3=''"""%(dapat[1],stok,stokkarton,id1,dapat[0])
                            dataCol=["namabarang","jumlahbarang","iddsalesorder","kodebarang","lokasi","stok","stokkarton"]
                            return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
                else:
                    query="select trim(kodebarang),id,stat3 from %s where noso='%s' and stat1='skip' order by stat3"%(namaTabel,id1)
                    dapat=ambilBanyakRowSQL(query)
                    print dapat
                    strKB="('-'"
                    strID="('-'"
                    for single in dapat:
                        if single[2]=="":
                            strKB+=",'%s'"%single[0]
                        strID+=",'%s'"%single[1]
                    strID+=")"
                    strKB+=")"
                 
                    query="select namabarang,jumlahbarang,trim(kodebarang),id,stat3 from %s where noso='%s' and stat1='skip' order by stat3 limit %s,1"%(namaTabel,id1,ind1)
                    print query
                    dataSO=ambilBanyakRowSQL(query)
                    for single in dataSO:
                        if single[4]: #KARTONAN
                            strNol = "'0.0%'"
                            strDel = "'8.%'"
                            query="""select iddstoklokasi,kodebarang,lokasi from dstoklokasi where kodebarang='%s' 
                                and satuan='karton' and jumlahbarang>0 and lokasi not like %s and lokasi not like %s order by tglmasuk desc limit 1"""%(single[2],strNol,strDel)
                            theCon.execute(query)
                            if theCon.rowcount==0:
                                query="""select iddstoklokasi,kodebarang,lokasi from dstoklokasi where kodebarang='%s' 
                                    and satuan='karton' and jumlahbarang>0 order by tglmasuk desc limit 1"""%(single[2])
                                theCon.execute(query)
                                if theCon.rowcount==0:
                                    query="""select iddstoklokasi,kodebarang,lokasi from dstoklokasi where kodebarang='%s' 
                                        and satuan='karton' and lokasi not like %s and lokasi not like %s order by tglMasuk desc limit 1"""%(single[2],strNol,strDel)
                                    theCon.execute(query)
                                    if theCon.rowcount==0:
                                        query="""select iddstoklokasi,kodebarang,lokasi from dstoklokasi where kodebarang='%s' 
                                            and satuan='karton' and lokasi not like %s order by tglMasuk desc limit 1"""%(single[2],strNol)
                                        theCon.execute(query)
                                        if theCon.rowcount==0:
                                            query="""select iddstoklokasi,kodebarang,lokasi from dstoklokasi where kodebarang='%s' 
                                                and satuan='karton' order by tglMasuk desc limit 1"""%(single[2])
                                            theCon.execute(query)
                                            if theCon.rowcount==0:
                                                conn.commit()
                                                theCon.close()
                                                query="select namabarang,jumlahbarang,id,trim(kodebarang),0 lokasi,0 stok,0 stokkarton from dsalesorder where id='%s' "%(single[3])
                                                dataCol=["namabarang","jumlahbarang","iddsalesorder","kodebarang","lokasi","stok","stokkarton"]
                                                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
                                            
                            dapat=ambilSatuRowSQL(query)
                            query="select CONVERT((sum(jumlahbarang)), SIGNED)jumlahbarang from dstoklokasi where kodebarang='%s' and satuan='' group by kodebarang"%(dapat[1])
                            try:stok=ambilSatuRowSQL(query)[0]
                            except:stok=0
                            
                            query="select CONVERT((sum(jumlahbarang)), SIGNED)jumlahbarang from dstoklokasi where kodebarang='%s' and lokasi='%s' and satuan='karton' group by lokasi"%(dapat[1],dapat[2])
                            try:stokkarton=ambilSatuRowSQL(query)[0]
                            except:stokkarton=0
                            
                            conn.commit()
                            theCon.close()
                            query="""select '%s' nama, %s jmlbrg,%s id,trim(kodebarang),lokasi,%s stok, %s stokkarton from dstoklokasi 
                                where iddstoklokasi='%s'"""%(single[0],single[1],single[3],stok,stokkarton,dapat[0])
                            dataCol=["namabarang","jumlahbarang","iddsalesorder","kodebarang","lokasi","stok","stokkarton"]
                            return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
                            
                        else: #LEPASAN
                            strB = "'B%'"
                            strL = "'0.0%'"
                            
                            #KALAU JUMLAH BARANG ADA YANG LEBIH DARI 0
                            query="""select trim(kodebarang),lokasi from dstoklokasi where kodebarang in %s and satuan=''
                                and lokasi not like %s and jumlahbarang>0 ORDER BY lokasi ASC, tglMasuk desc limit %s,1"""%(strKB,strB,ind1)
                            theCon.execute(query)
                            if theCon.rowcount==0:
                                #KALAU STOK 0 CARI LOKASI YANG BUKAN 0.00.00.0.0
                                query="""select trim(kodebarang),lokasi,0 stok from dstoklokasi where kodebarang in %s and satuan=''
                                    and lokasi not like %s and lokasi not like %s ORDER BY lokasi ASC, tglMasuk desc limit %s,1"""%(strKB,strB,strL,ind1)
                                theCon.execute(query)
                                if theCon.rowcount==0:
                                    #KALAU STOK HABIS, YANG PENTING ADA RIWAYAT LOKASI WALAUPUN 0.00.00.0.0
                                    query="""select trim(kodebarang),lokasi,0 stok from dstoklokasi where kodebarang in %s and satuan=''
                                        and lokasi not like %s ORDER BY lokasi ASC, tglMasuk desc limit %s,1"""%(strKB,strB,ind1)
                                    theCon.execute(query)
                                    if theCon.rowcount==0:
                                        #BELUM PERNAH ADA MASUK DSTOKLOKASI
                                        query="""select trim(kodebarang) from dsalesorder where kodebarang in %s and not exists 
                                            (select 1 from dstoklokasi where dsalesorder.kodebarang=dstoklokasi.kodebarang and satuan='' and lokasi not like %s)
                                            and noso='%s' and stat1='' order by stat3 limit 1"""%(strKB,strB,id1)
                                        dapat=ambilSatuRowSQL(query)
                                        query="""select namabarang,jumlahbarang,id,trim(kodebarang),'' lokasi,0 stok,0 stokkarton from dsalesorder where noso='%s' 
                                            and kodebarang=%s and stat3=''"""%(id1,dapat[0])
                                        dataCol=["namabarang","jumlahbarang","iddsalesorder","kodebarang","lokasi","stok","stokkarton"]
                                        conn.commit()
                                        theCon.close()
                                        return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
                            conn.commit()
                            theCon.close()
                            dapat=ambilSatuRowSQL(query)
                            query="select CONVERT((sum(jumlahbarang)), SIGNED)jumlahbarang from dstoklokasi where kodebarang='%s' and lokasi='%s' group by lokasi"%(dapat[0],dapat[1])
                            try:stok=ambilSatuRowSQL(query)[0]
                            except:stok=0
                            
                            query="select CONVERT((sum(jumlahbarang)), SIGNED)jumlahbarang from dstoklokasi where kodebarang='%s' and satuan='karton' group by kodebarang"%(dapat[0])
                            try:stokkarton=ambilSatuRowSQL(query)[0]
                            except:stokkarton=0

                            query="""select namabarang,jumlahbarang,id,trim(kodebarang),'%s' lokasi,%s stok,%s stokkarton from dsalesorder where noso='%s'
                                and kodebarang=%s and stat3=''"""%(dapat[1],stok,stokkarton,id1,dapat[0])
                            dataCol=["namabarang","jumlahbarang","iddsalesorder","kodebarang","lokasi","stok","stokkarton"]
                            return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
                
            if request.method == 'PUT':
                
                dic={}
                dic["error"]='false'
                dic["msg"]=""
                dic["data"]={}
                dic["data"]["rows"]=[]
                
                noso= request.args.get('noso')
                idx= request.args.get('index')
                jml= request.args.get('jumlahScan')
                picker= request.args.get('picker')
                jml2 = request.args.get('jmlScanKarton')
                jmlItem = request.args.get('jmlItem')
                jmlOrder = request.args.get('jumlahorder')
                iddsales = request.args.get('iddsalesorder')
                lokasi = request.args.get('lokasi')
                kodebarang = request.args.get('kodebar')
                if '%s'%jml2=="None":jml2="1"
             
                query="select stat3 from dsalesorder where id='%s'"%(iddsales)
                stat3=ambilSatuRowSQL(query)
                try:karton=stat3[0]
                except:karton=""
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                print karton
                    
                if karton:
                    jmlTot=int(jml2)
                    query="select iddstoklokasi, jumlahbarang from dstoklokasi where kodebarang='%s' and lokasi='%s' and jumlahbarang>0 and satuan='karton' order by iddstoklokasi"%(kodebarang,lokasi)
                    dataBrgPO={}
                    for single in ambilBanyakRowSQL(query):
                        dataBrgPO[single[0]]=[single[1]]
                        
                    for single in dataBrgPO:
                        jmlRun=dataBrgPO[single][0]
                        idpodet=single
                        lagi=0
                        if jmlRun>=jmlTot:  
                            query="update dstoklokasi set jumlahbarang=jumlahbarang-%s where iddstoklokasi='%s'"%(jmlTot,idpodet)
                            curs.execute(query)
                            lagi=1
                        else:
                            query="update dstoklokasi set jumlahbarang=jumlahbarang-%s where iddstoklokasi='%s'"%(jmlRun,idpodet)
                            curs.execute(query)
                            jmlTot=jmlTot-jmlRun
                            lagi=0
                        
                        if lagi:break
                else:
                    jmlTot=int(jml)
                    query="select iddstoklokasi, jumlahbarang from dstoklokasi where  kodebarang='%s' and lokasi='%s' and jumlahbarang>0 and satuan='' order by iddstoklokasi desc"%(kodebarang,lokasi)
                    dataBrgPO={}
                    for single in ambilBanyakRowSQL(query):
                        dataBrgPO[single[0]]=[single[1]]
                  
                    if 1:
                        for single in dataBrgPO:
                            jmlRun=dataBrgPO[single][0]
                            idpodet=single
                            lagi=0
                            if jmlRun>=jmlTot:  
                                query="update dstoklokasi set jumlahbarang=jumlahbarang-%s where iddstoklokasi='%s'"%(jmlTot,idpodet)
                                curs.execute(query)
                                lagi=1
                            else:
                                query="update dstoklokasi set jumlahbarang=jumlahbarang-%s where iddstoklokasi='%s'"%(jmlRun,idpodet)
                                curs.execute(query)
                                jmlTot=jmlTot-jmlRun
                                lagi=0
                                
                            if lagi:break
             
                query="update %s set jml1='%s',stat1='picking',stat4=now(),stat2='%s' where id='%s'"%(namaTabel,jml,picker,iddsales)
                curs.execute(query)
                print query
                
                query="insert into rekampicking (lokasi,noso,jumlahambil,kodebarang,tanggal,operator) values ('%s','%s','%s','%s',now(),'%s')"%(lokasi,noso,jml,kodebarang,picker)
                curs.execute(query)
                      
                conn2.commit()
                curs.close()
             
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                
                return Response(strDic, mimetype='application/json')
            
        @app.route('%s/getBarangdet'%(folderAPI), methods=['GET'])
        def getBarangdet():
#            namaTabel="proyek"
            namaTabel="barangdet"
            
            if request.method == 'GET':
                
                id1= request.args.get('kodebarang')
                lokasi= request.args.get('lokasi')
                
                conn=mysql.get_db()
                theCon=conn.cursor()
                
                if lokasi=="":
                    query="""select idbarang from barang where kodebrg='%s'"""%(id1)
                    try:idbarang=ambilSatuRowSQL(query)[0]
                    except:idbarang=""
                    queryd="""insert into dstoklokasi(kodebarang,kodebarangkarton,tglmasuk,jumlahbarang,stokawal,sumber,satuan,lokasi)
                        values('%s','%sK',now(),0,0,'barangdet','','0.00.00.0.00'),
                        ('%s','%sK',now(),0,0,'barangdet','karton','0.00.00.0.00')"""%(id1,idbarang,id1,idbarang)
                    theCon.execute(queryd)
                    lokasi="0.00.00.0.00"
                
                strWhere="where kodebrg='%s'"%(id1)
                query="select jumlahbrg,jmlpack,kodebrgpack,kodebrgkarton,jmlkarton from barangdet %s"%strWhere
                theCon.execute(query)
                if theCon.rowcount==0:
                    query="""select idbarang from barang where kodebrg='%s'"""%(id1)
                    try:idbarang=ambilSatuRowSQL(query)[0]
                    except:idbarang=""
                    queryi="insert into barangdet (kodebrg,jumlahbrg,jmlpack,jmlkarton,kodebrgpack,kodebrgkarton) values('%s','1','12','3000','%sP','%sK')"%(id1,idbarang,idbarang)
                    theCon.execute(queryi)
                
                query="select CONVERT((sum(jumlahbarang)), SIGNED)jumlahbarang,satuan from dstoklokasi where kodebarang='%s' and lokasi='%s' group by lokasi"%(id1,lokasi)
                print query
                try:totpcs=ambilSatuRowSQL(query)
                except:totpcs=0
                print totpcs,lokasi
                if totpcs[1]=="karton":
                    query="select CONVERT((sum(jumlahbarang)), SIGNED)jumlahbarang from dstoklokasi where kodebarang='%s' and satuan='' group by kodebarang"%(id1)
                    try:totpcs=ambilSatuRowSQL(query)
                    except:totpcs=0

                query="""select jumlahbrg,jmlpack,kodebrgpack,kodebrgkarton,jmlkarton,
                    (select satuan from barang where kodebrg='%s' limit 1),
                    (select namabrg from barang where kodebrg='%s' limit 1),
                    (select trim(if(barcode='',idbarang,barcode))from barang where kodebrg='%s' limit 1),%s totpcs from barangdet"""%(id1,id1,id1,totpcs[0])
                
                conn.commit()
                theCon.close()
                dataCol=["jumlahbrg","jmlpack","kodebrgpack","kodebrgkarton","jmlkarton","satuan","namabarang","barcode","totalpcs"]
                print query
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
                #return bikinGetJSONExt(namaTabel,strWhere)
                
if 1:# CHECKING PACKING
        @app.route('%s/getNomerPacking'%(folderAPI), methods=['GET'])
        def getNomerPacking():
#            namaTabel="proyek"
            namaTabel="rdsalesorder"
            
            if request.method == 'GET':
                
                id1= request.args.get('noso')
          
                
                strWhere=""#"where koderel='%s'"%id1
                
                query="select MAX(CONVERT(stat1,UNSIGNED)) from rdsalesorder where noso='%s'"%id1
                dapat=ambilSatuRowSQL(query)[0]
                print dapat
                dataCol=["stat1"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
                 
        
        @app.route('%s/getDSOCheck'%(folderAPI), methods=['GET', 'PUT'])
        def getDSOcheck():
#            namaTabel="proyek"
            namaTabel="dsalesorder"
            namaTabel2="rdsalesorder"
            
            if request.method == 'GET':
                
                id1= request.args.get('noso')
                index1= request.args.get('index')
                kodebrg= request.args.get('kodebrg')
                
                if "%s"%index1!="None":
                    
                    query="select distinct(trim(kodebarang)) from %s where noso='%s'"%(namaTabel,id1)     
                    print query
                    strKB="('-'"
                    for single in ambilBanyakRowSQL(query):strKB+=",'%s'"%single[0]
                    strKB+=")"
                    
                    query="select trim(kodebrg),lokasi from barangdet where kodebrg in %s order by lokasi"%(strKB)
                    print query
                    
                    dapat=ambilBanyakRowSQL(query)
                    
                    strKB="order by field(kodebarang,''"
                    dataLokasi={}
                    for single in dapat:
                        strKB+=",'%s'"%single[0]
                        dataLokasi[single[0].lower()]=[single[1]]
                    strKB+=")"
                    
                    ind1=index1
                    
                    query="""select trim(kodebarang),namabarang,jumlahbarang,if(jml1 is null,0,jml1),if(stat1 is null,'belum',stat1) from %s 
                    where noso ='%s' %s limit 1 offset %s """%(namaTabel,id1,strKB,ind1)
                    print query
                    
                    listSel=["kodebarang",'namabarang','jumlahbarang',"jumlahscan","status"]
                    
                    dic={}
                    dic["error"]='false'
                    dic["msg"]=""
                    dic["data"]={}
                    dic["data"]["rows"]=[]

                    for single in ambilBanyakRowSQL(query):
                        data1={}
                        theCol=len(single)
                        
                        for single2 in range(theCol):
                            if '%s'%single[single2]=="None":data1[listSel[single2]]=""
                            else:data1[listSel[single2]]=single[single2]
                        
                        queryBrg="select jumlahbrg,kodebrgpack,jmlpack,kodebrgkarton,jmlkarton,lokasikrtn from barangdet where kodebrg='%s'"%single[0]
                        
                        print queryBrg
                        
                        infoSat=ambilSatuRowSQL(queryBrg)
                        c=0
                        
                        for single2 in ["jumlahbrg","kodebrgpack","jmlpack","kodebrgkarton","jmlkarton","lokasikrtn"]:
                            try:data1[single2]=infoSat[c]
                            except:data1[single2]=""
                            c+=1
                        
                        queryBrg="select barcode,satuan  from barang where kodebrg='%s'"%single[0]
                        infoSat=ambilSatuRowSQL(queryBrg)
                        c=0
                        for single2 in ["barcode","satuan"]:
                            try:data1[single2]=infoSat[c]
                            except:data1[single2]=""
                            c+=1
                            

                        dic["data"]["rows"].append(data1)
                        
                    dic["data"]["total"]=len(dic["data"]["rows"])
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                    return Response(strDic, mimetype='application/json')
                
                if "%s"%kodebrg!="None":
                    
                    query="""select trim(kodebarang),namabarang,jumlahbarang,if(jml1 is null,0,jml1),if(stat1 is null,'belum',stat1) from %s 
                    where noso ='%s' and trim(kodebarang)='%s' """%(namaTabel,id1,kodebrg)
                    print query
                    
                    listSel=["kodebarang",'namabarang','jumlahbarang',"jumlahscan","status"]
                    
                    dic={}
                    dic["error"]='false'
                    dic["msg"]=""
                    dic["data"]={}
                    dic["data"]["rows"]=[]

                    for single in ambilBanyakRowSQL(query):
                        data1={}
                        theCol=len(single)
                        jb1=0
                        kodebrg=single[0]
                        jb1=single[2]
                        for single2 in range(theCol):
                            if '%s'%single[single2]=="None":data1[listSel[single2]]=""
                            else:data1[listSel[single2]]=single[single2]
                            
                        
                        queryBrg="select jumlahbrg,kodebrgpack,jmlpack,kodebrgkarton,jmlkarton,lokasikrtn from barangdet where kodebrg='%s'"%single[0]
                        infoSat=ambilSatuRowSQL(queryBrg)
                        
                            

                        # ########################
                        c=0
                        for single2 in ["jumlahbrg","kodebrgpack","jmlpack","kodebrgkarton","jmlkarton","lokasikrtn"]:
                            
                            try:data1[single2]=infoSat[c]
                            except:data1[single2]=""
                            c+=1
                        
                        queryBrg="select barcode  from barang where kodebrg='%s'"%single[0]
                        infoSat=ambilSatuRowSQL(queryBrg)
                        c=0
                        for single2 in ["barcode"]:
                            try:data1[single2]=infoSat[c]
                            except:data1[single2]=""
                            c+=1
                            

                        dic["data"]["rows"].append(data1)
                        
                    dic["data"]["total"]=len(dic["data"]["rows"])
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                    return Response(strDic, mimetype='application/json')
                
                query="select 'belum' from %s where noso='%s' and (stat1='' or stat1 is null) "%(namaTabel,id1)
#                print query
                
                try:stat1=ambilSatuRowSQL(query)[0]
                except:stat1=""
                
                if stat1=="belum":
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Nota SO Belum Selesai Picking"
                    dic["data"]={}
                    dic["data"]["rows"]=[]
                    
                else:
                    
                    dic={}
                    dic["error"]='false'
                    dic["msg"]=""
                    dic["data"]={}
                    dic["data"]["rows"]=[]
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json')
            
            if request.method == 'PUT':
                
                dic={}
                dic["error"]='false'
                dic["msg"]=""
                dic["data"]={}
                dic["data"]["rows"]=[]
                
                id1= request.args.get('noso')
                barcode= request.args.get('barScan')
                index= request.args.get('index')
                jml1= request.args.get('jumlah')
                checker= '%s'%request.args.get('checker')
                
                query="select 'belum' from %s where noso='%s' and stat1='' "%(namaTabel,id1)
                print query
                
                try:stat1=ambilSatuRowSQL(query)[0]
                except:stat1=""
                
                if stat1=="belum":
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Nota SO Belum Selesai Picking"
                    dic["data"]={}
                    dic["data"]["rows"]=[]
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
                
                query="select kodebrg,satuan from barang where barcode=trim('%s')"%barcode
                dapat=ambilSatuRowSQL(query)
                try:barcode=dapat[0]
                except:
                    
                    query="select kodebrg,satuan from barang where idbarang= trim('%s')"%barcode
                    dapat=ambilSatuRowSQL(query)
                    try:barcode=dapat[0]
                    except:
                        dic={}
                        dic["error"]='true'
                        dic["msg"]="Barang Tidak Ada"
                        dic["data"]={}
                        dic["data"]["rows"]=[]
                        strDic="%s"%dic
                        strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                        return Response(strDic, mimetype='application/json')                        
                        return
                
                satuan=dapat[1]
                
                #ini
                query="select jml1,jml2,namabarang,id from %s where noso='%s' and kodebarang=trim('%s') and CONVERT(jml2, SIGNED) < CONVERT(jml1, SIGNED) order by stat3"%(namaTabel,id1,barcode)
                print query
                
                dapat=ambilSatuRowSQL(query)
                try:jmlPick=int(dapat[0])
                except:jmlPick=0
                
                try:jmlCheck=int(dapat[1])
                except:jmlCheck=0
                
                try:jmlBaru=int(jml1)
                except:jmlBaru=0
             
                try:
                    nama=dapat[2]
                    namabrg=dapat[2]
                except:
                    
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Barang Tidak Ketemu"
                    dic["data"]={}
                    dic["data"]["rows"]=[]
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')


                jmlSisa2=jmlPick-jmlCheck#-jmlBaru
                jmlSisa=jmlPick-jmlCheck-jmlBaru
                
                if jmlSisa>=0 and jmlPick>0:
                
#                    query="update %s set jml2=jml2+1 where noso='%s' and kodebarang='%s' "%(namaTabel,id1,barcode)
        #yg asli            #query="update %s set jml2=jml2+%s,stat5=now() where noso='%s' and kodebarang=trim('%s')  "%(namaTabel,jmlBaru,id1,barcode)
                    query="update %s set jml2=jml2+%s,stat5=now() where id='%s'"%(namaTabel,jmlBaru,dapat[3])
                    
                    print query
                    
                    conn2=mysql.get_db()
                    theCon=conn2.cursor()
                    theCon.execute(query)
                    conn2.commit()
#                    theCon.close()
                    #LANGKAH UNTUK MENGURANGI STOK LEPASAN
                    
                    query="select count(*) from %s where noso='%s' and kodebarang=trim('%s') and stat1='%s'"%(namaTabel2,id1,barcode,index)
                    
                    dapat=ambilSatuRowSQL(query)
                    
                    if dapat[0]==0:
                    
#                        query="insert into %s (kodebarang,namabarang,jumlahbarang,noso,stat1) values ('%s','%s',1,'%s','%s') "%(namaTabel2,barcode,nama,id1,index)
                        query="insert into %s (kodebarang,namabarang,jumlahbarang,noso,stat1,stat3) values ('%s','%s',%s,'%s','%s','%s') "%(namaTabel2,barcode,nama,jmlBaru,id1,index,checker)
                    
                    else:
#                        query="update %s set jumlahbarang=jumlahbarang+1 where kodebarang='%s' and noso='%s' and stat1='%s' "%(namaTabel2,barcode,id1,index)
                        query="""update %s set jumlahbarang=jumlahbarang+%s,stat3='%s' 
                        where kodebarang='%s' and noso='%s' and stat1='%s' """%(namaTabel2,jmlBaru,checker,barcode,id1,index)
                    
#                    conn2=mysql.get_db()
#                    theCon=conn2.cursor()
                    theCon.execute(query)
                    conn2.commit()
                    theCon.close()
                    
#                    try:jmlSisa=int(jmlSisa)-int(jml1)
#                    except:1
                    
                        
                        
                    dic["data"]["rows"]=[{"sisa":'%s'%jmlSisa,"total_brg":'%s'%jmlPick,"kode_barang":'%s'%barcode,"nama_barang":'%s'%namabrg
                    ,"noso":'%s'%id1,"noPack":'%s'%index,'satuan':'%s'%satuan}
                    ]
                    
                    queryBrg="select jumlahbrg,kodebrgpack,jmlpack,kodebrgkarton,jmlkarton,lokasikrtn from barangdet where kodebrg=trim('%s')"%barcode
                        
                    print queryBrg
                    
                    infoSat=ambilSatuRowSQL(queryBrg)
                    c=0
                    for single2 in ["jumlahbrg","kodebrgpack","jmlpack","kodebrgkarton","jmlkarton","lokasikrtn"]:
                        try:dic["data"]["rows"][0][single2]=infoSat[c]
                        except:dic["data"]["rows"][0][single2]=""
                        c+=1
                    
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                    return Response(strDic, mimetype='application/json')
                else:
                
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Barang Scan Berlebih"
                    dic["data"]={}
                    dic["data"]["rows"]=[]
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
        @app.route('%s/getDSOCheckFull'%(folderAPI), methods=['GET', 'PUT'])
        def getDSOcheckFull():
#            namaTabel="proyek"
            namaTabel="dsalesorder"
            namaTabel2="rdsalesorder"
            
            budget=5000000
            
            if request.method == 'GET':
                
                id1= request.args.get('noso')
                
                if "%s"%id1!="None":
                    
                    
                    query="select count(*) from %s where noso ='%s' and jml1!=jml2  and jml1!=''  "%(namaTabel,id1)
                    print query
                    
                    dapat=ambilBanyakRowSQL(query)
                    
                    listSel=["kodebarang",'namabarang','jumlahbarang',"jumlahscan","status"]
                
#                if 1:
                    if dapat==0:
                            
                        dic={}
                        dic["error"]='false'
                        dic["msg"]=""
                        dic["data"]={}
                        dic["data"]["rows"]=[]

                        for single in ambilBanyakRowSQL(query):
                            data1={}
                            theCol=len(single)
                            
                            for single2 in range(theCol):
                                if '%s'%single[single2]=="None":data1[listSel[single2]]=""
                                else:data1[listSel[single2]]=single[single2]
                            
                            dic["data"]["rows"].append(data1)
                            
                        dic["data"]["total"]=len(dic["data"]["rows"])
                        strDic="%s"%dic
                        strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                        return Response(strDic, mimetype='application/json')
                    else:
                        dic={}
                        dic["error"]='true'
                        dic["msg"]="Belum Selesai Checking"
                        dic["data"]={}
                
#                query="select 'belum' from %s where noso='%s' and jml2!=jumlahbarang "%(namaTabel,id1)
                query="select 'belum' from %s where noso='%s' and jml2+0!=jml1+0 "%(namaTabel,id1)
                print query
                
                try:stat1=ambilSatuRowSQL(query)[0]
                except:stat1=""
                
                if stat1=="belum":
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Nota SO Belum Selesai Packing"
                    dic["data"]={}
                    dic["data"]["rows"]=[]
                    
                else:
                    
                    dic={}
                    dic["error"]='false'
                    dic["msg"]="NOSO %s Cetak Packing"%id1
                    dic["data"]={}
                    dic["data"]["rows"]=[]
                    
                    
#                    print query
                    
                    conn2=mysql.get_db()
                    theCon=conn2.cursor()
                    query="update %s set stat4='cetakPacking',stat5='cetak_packing' where noso='%s' "%(namaTabel2,id1)
                    theCon.execute(query)
                    
                    query="select kodebarang, sum(jumlahbarang) from rdsalesorder where noso='%s' group by kodebarang "%(id1)
                    print query
                    strKB="('-'"
                    
                    for single in ambilBanyakRowSQL(query):
                        query1="""update djual set pcs ='%s'
#                        ,netto=round(pcs*(hjual*(1-(((disc1/100)+(disc2/100)+(disc3/100))))-disc1rp-disc2rp-disc3rp),0)
#                        ,netto=round(pcs*(hjual*((1-(disc1/100))-((1-(disc1/100))*disc2/100)-(((1-(disc1/100))*disc2/100)*disc3/100))-disc1rp-disc2rp-disc3rp),0)
                        ,netto=round(pcs*(hjual*((1-(disc1/100))-((1-(disc1/100))*disc2/100)-(((1-disc1/100)-(1-disc1/100)*disc2/100)*disc3/100)-disc1rp-disc2rp-disc3rp)),0)
#                        ,totdisc=round(pcs*(hjual*((((disc1/100)+(disc2/100)+(disc3/100))))-disc1rp-disc2rp-disc3rp),0)
#                        ,totdisc=round(pcs*(hjual*((((disc1/100)-((disc1/100)*disc2/100)-(((disc1/100)*disc2/100)*disc3/100))))-disc1rp-disc2rp-disc3rp),0)
                        ,totdisc=round(pcs*(hjual-(netto/pcs)),0)
                        where nojual='%s' and kodebrg='%s'"""%(int(single[1]),id1,single[0])
                        print query1
                        
                        theCon.execute(query1)
                        strKB+=",'%s'"%single[0]
                        
                    strKB+=")"
                    
                    query2="delete from djual where nojual='%s' and pcs=0"%(id1)
                    theCon.execute(query2)
                    
                    query2="delete from djual where nojual='%s' and kodebrg not in %s"%(id1,strKB)
                    theCon.execute(query2)
                    
                    query2="select sum(netto),sum(totdisc) from djual where nojual='%s' "%id1
                    dapat=ambilSatuRowSQL(query2)
                    
                    query3="update hjual  set totbrutto='%s',totdisc='%s',nilaifak='%s',piutang='%s' where nojual='%s'"%(dapat[0],dapat[1],dapat[0],dapat[0],id1)
                    print query3
                    theCon.execute(query3)
                    
                    totalbrutto = dapat[0]
                    #print totalbrutto
                    #print budget
                    if totalbrutto>budget:
                        query4="update hjual set diskonrp=-10000,nilaifak=nilaifak+10000,piutang=piutang+10000 where nojual='%s'"%id1
                        print query4
                        theCon.execute(query4)
                    conn2.commit()
                    theCon.close()
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json')
        @app.route('%s/getDSOPack'%(folderAPI), methods=['GET', 'PUT'])
        def getDSOPack():
#            namaTabel="proyek"
            namaTabel="rdsalesorder"
            
            if request.method == 'GET':
                
                id1= request.args.get('noso')
                nopack= request.args.get('nopack')
                
                if ('%s'%nopack)=="None":
                    strWhere="where noso='%s'"%id1
                    
                    return bikinGetJSONExt(namaTabel,strWhere)
                    
                else:
                    
                    strWhere="where noso='%s' and stat1='%s'"%(id1,nopack)
                    
                    return bikinGetJSONExt(namaTabel,strWhere)
            
            if request.method == 'PUT':
                
                id1= request.args.get('noso')
                nopack= request.args.get('nopack')
                stat= request.args.get('setStat')
                checker= '%s'%request.args.get('checker')
                
#                query="update %s set stat where noso='%s' and stat1='%s' "%(namaTabel,id1,nopack)
                    
                if ('%s'%nopack)!="None":
                    query="update %s set stat2='%s',stat3='%s' where noso='%s' and stat1='%s' "%(namaTabel,checker,stat,id1,nopack)
                                        
                    conn2=mysql.get_db()
                    theCon=conn2.cursor()
                    theCon.execute(query)
                    conn2.commit()
                    theCon.close()
                    
                    dic={}
                    dic["error"]='false'
                    dic["msg"]="SO %s No Pack %s Terupdate %s"%(id1,nopack,stat)
                    dic["data"]={}
                    
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
                    
                    
                else:
                    query="update %s set stat2='%s' where noso='%s'"%(namaTabel,stat,id1)
                    
                    conn2=mysql.get_db()
                    theCon=conn2.cursor()
                    theCon.execute(query)
                    conn2.commit()
                    theCon.close()
                    
                    dic={}
                    dic["error"]='false'
                    dic["msg"]="SO %s Terupdate %s"%(id1,stat)
                    dic["data"]={}
                    
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
            
        @app.route('%s/getDSODeliver'%(folderAPI), methods=['GET', 'PUT'])
        def getDSODeliver():
#            namaTabel="proyek"
            namaTabel="rdsalesorder"
            
            if request.method == 'GET':
                
                id1= request.args.get('noso')
                nopack= request.args.get('nopack')
                
                if ('%s'%nopack)=="None":
                    strWhere="where noso='%s'"%id1
                    
                    return bikinGetJSONExt(namaTabel,strWhere)
                    
                else:
                    
                    #strWhere="where noso='%s' and stat1='%s'"%(id1,nopack)
                    #return bikinGetJSONExt(namaTabel,strWhere)
                    strWhere="where noso='%s' and stat1='%s'"%(id1,nopack)
                                    
                    query="select * from %s %s"%(namaTabel,strWhere)
                    #print query
                    conn2=mysql.get_db()
                    theCon2=conn2.cursor()
                    try:theCon2.execute(query)
                    except:
                        data1={}
                        dic={}
                        dic["error"]='true'
                        dic["msg"]="Nomor Delivery Tidak ada "
                        theCon.close()
                        strDic="%s"%dic
                        strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                        return Response(strDic, mimetype='application/json')
                    
                    query="select namacustomer from hsalesorder where noso='%s'"%id1
                    print query
                    try:namacus=ambilSatuRowSQL(query)[0]
                    except:namacus=""
                    
                    theCon2.close()
                    
                    query="""select kodebarang,stat3,jumlahbarang,namabarang,(select satuan from barang where kodebrg=kodebarang limit 1),
                    (select namacus from customer where kodecus='%s') supplier from %s """%(namacus,namaTabel)
                    dataCol=["kodebarang","stat3","jumlahbarang","namabarang","satuan","namacus"]
                    return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
if 1:# REfilling

        @app.route('%s/inputNewLoc'%(folderAPI), methods=['GET'])
        def inputNewLoc():
            namaTabel="barangdet"
            namaTabel2="tempRefill"
            if request.method == 'GET':
                
                id1= '%s'%request.args.get('lokasi')
                namalogin= request.args.get('namalogin')
                barcode= request.args.get('barcode')
                
                conn2=mysql.get_db()
                theCon=conn2.cursor()
                query="select kodebrg from barang where kodebrg='%s'"%barcode
                theCon.execute(query)
                if theCon.rowcount==0:
                    query="select kodebrg from barangdet where kodebrgpack='%s' or kodebrgkarton='%s'"%(barcode,barcode)
                    theCon.execute(query)
                    if theCon.rowcount==0:
                        query="select kodebarang from dstoklokasi where kodebarang='%s'"%barcode
                        theCon.execute(query)
                        if theCon.rowcount==0:
                            data1={}
                            dic={}
                            dic["error"]='true'
                            dic["msg"]="Barcode Tidak Ditemukan"
                            theCon.close()
                            strDic="%s"%dic
                            strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                            return Response(strDic, mimetype='application/json')
                    
                kodebrg=ambilSatuRowSQL(query)[0]
                query="select namabrg,barcode=idbarang,barcode,0 stok from barang where kodebrg='%s'"%(kodebrg)
                namabrg=ambilSatuRowSQL(query)[0]
                query2="insert into temprefill (namaoperator,tglref,kodebrg,namabrg,lokasi,status) values('%s',now(),'%s','%s','%s','collect')"%(namalogin,kodebrg,namabrg,id1)
                theCon.execute(query2)
                conn2.commit()
                theCon.close()
                    
                strWhere=""
                dataCol=["namaBrg","perlucetakkarton","barcode","stok"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
        
        @app.route('%s/getBrgDariLokEcer'%(folderAPI), methods=['GET'])
        def getBrgDariLokEcer():
            namaTabel="barangdet"
            namaTabel2="tempRefill"
            if request.method == 'GET':
                
                id1= '%s'%request.args.get('lokasi')
                namalogin= request.args.get('namalogin')
                
                conn2=mysql.get_db()
                theCon=conn2.cursor()
                
                query="select kodebarang,kodebarangkarton from dstoklokasi where lokasi='%s' order by tglmasuk desc"%id1
                theCon.execute(query)
                if theCon.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Lokasi Kosong"
                    theCon.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
                
                dapat=ambilSatuRowSQL(query)
                query3="select * from temprefill where kodebrg='%s' and namaoperator='%s' and status='collect'"%(dapat[0],namalogin)
                theCon.execute(query3)
                if theCon.rowcount>0:
                    data1={}
                    dic={}
                    dic["error"]='truee'
                    dic["msg"]="Barang Masih Dalam Daftar Tugas"
                    theCon.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
                
                query="select namabrg,barcode=idbarang,barcode,(select CONVERT((sum(jumlahbarang)), SIGNED)jumlahbarang from dstoklokasi where kodebarang='%s' and lokasi='%s' and satuan='' group by kodebarang) from barang where kodebrg='%s'"%(dapat[0],id1,dapat[0])
                print query
                theCon.execute(query)
                if theCon.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Data Bermasalah"
                    theCon.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
                
                dapat2=ambilSatuRowSQL(query)
                query2="insert into temprefill (namaoperator,tglref,kodebrg,namabrg,lokasi,status) values('%s',now(),'%s','%s','%s','collect')"%(namalogin,dapat[0],dapat2[0],id1)
                theCon.execute(query2)
                conn2.commit()
                theCon.close()
                    
                strWhere=""
                dataCol=["namaBrg","perlucetakkarton","barcode","stok"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
            
               
        @app.route('%s/getLokasiDariKodeKarton'%(folderAPI), methods=['GET'])
        def getLokasiDariKodeKarton():
            namaTabel="dstoklokasi"
            if request.method == 'GET':
                
                id1= request.args.get('kodebrg')
                
                query="select CONVERT((sum(jumlahbarang)), SIGNED)jumlahbarang from %s where kodebarang=trim('%s') and satuan='karton' group by kodebarang"%(namaTabel,id1)
                conn=mysql.get_db()
                theCon=conn.cursor()
                theCon.execute(query)
                if theCon.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Kode Barang Tidak Ada di Stok Karton"
                    theCon.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
                    
                jml = ambilSatuRowSQL(query)[0]
                if jml==0:
                    theCon.close()
                    strWhere="where kodebarang=trim('%s') and satuan='karton' order by tglmasuk desc limit 1"%(id1)
                    query="""select kodebarang,%s stok,if(kodebarangkarton='','Tidak Ada Barcode',kodebarangkarton),lokasi,
                        (select namabrg from barang where trim(kodebrg)=trim(kodebarang) limit 1) namabrg,0 jumlahbarang
                        from %s """%(jml,namaTabel)
                    print query
                    dataCol=["kodebarang","stok","kodebarangkarton","lokasi","namabrg","jumlahbarang"]
                    return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
                theCon.close()
                strWhere="where kodebarang=trim('%s') and satuan='karton' and jumlahbarang>0 group by lokasi desc"%(id1)
                query="""select kodebarang,%s stok,if(kodebarangkarton='','Tidak Ada Barcode',kodebarangkarton),lokasi,
                    (select namabrg from barang where trim(kodebrg)=trim(kodebarang) limit 1) namabrg,CONVERT((sum(jumlahbarang)), SIGNED)jumlahbarang
                    from %s """%(jml,namaTabel)
                print query
                dataCol=["kodebarang","stok","kodebarangkarton","lokasi","namabrg","jumlahbarang"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
   
        @app.route('%s/getBrgDariLokKarton'%(folderAPI), methods=['GET', 'PUT', 'POST'])
        def getBrgDariLokKarton():
            namaTabel="barangdet"
            namaTabel2="tempRefill"
            if request.method == 'GET':
                
                namalogin= request.args.get('namalogin')
             
                query="""select kodebrg,namabrg,kodebrgkarton,idtemprefill,lokasi,
                    (select CONVERT((sum(jumlahbarang)), SIGNED)jumlahbarang from dstoklokasi where kodebarang=kodebrg and satuan='karton' group by kodebarang limit 1)
                    from temprefill where namaoperator='%s' and status='collect'"""%(namalogin)
                strWhere=""
                print query
                
                dataCol=["kodebrg","namabrg","kodebrgkarton","idtemprefill","lokasi","stok"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
            
            if request.method == 'PUT':                
                lokasi= request.args.get('lokasi')
                kodebrg= request.args.get('kodebrg')
                namalogin= request.args.get('namalogin')
                kodebrgkarton= request.args.get('kodebrgkarton')
                jml= request.args.get('jml')
                idrefill= request.args.get('idrefill')
                
                conn2=mysql.get_db()
                curs=conn2.cursor()
                query="select namabrg from temprefill where kodebrg='%s' and namaoperator='%s' and status='collect'"%(kodebrg,namalogin)
                curs.execute(query)
                if curs.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="kode barang tidak ada di data refill"
                    dic["data"]=data1
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                    return Response(strDic, mimetype='application/json') 
                namabrg=ambilSatuRowSQL(query)[0]
                query="select * from dstoklokasi where kodebarang='%s' and lokasi='%s' and satuan='karton'"%(kodebrg,lokasi)
                curs.execute(query)
                if curs.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Lokasi Tidak Sesuai"
                    dic["data"]=data1
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                    return Response(strDic, mimetype='application/json') 
                
                query="select * from dstoklokasi where kodebarang='%s' and lokasi='%s' and jumlahbarang>0 and satuan='karton'"%(kodebrg,lokasi)
                curs.execute(query)
                if curs.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="STOK KOSONG"
                    dic["data"]=data1
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                    return Response(strDic, mimetype='application/json') 
                
                query="select jmlkarton from barangdet where kodebrg='%s'"%kodebrg
                curs.execute(query)
                if curs.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="JML KARTON TIDAK TERSEDIA"
                    dic["data"]=data1
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                    return Response(strDic, mimetype='application/json') 
                
                jmlkarton=ambilSatuRowSQL(query)[0]
                query="select CONVERT((sum(jumlahbarang)), SIGNED) stok from dstoklokasi where kodebarang='%s' and lokasi='%s' and satuan='karton' group by lokasi having stok>=%s"%(kodebrg,lokasi,jml)
                curs.execute(query)
                if curs.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="STOK KARTONAN KURANG"
                    dic["data"]=data1
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                    return Response(strDic, mimetype='application/json') 
             
                #LANGKAH INI UNTUK MENGURANGI STOK KARTON
                jml2 = int(jml)*int(jmlkarton)
             
                query="update temprefill set status='pick_karton', jmlAmbil='%s',lokasikarton='%s',tglambil=now(),kodebrgkarton='%s' where idtemprefill='%s'"%(jml2,lokasi,kodebrgkarton,idrefill)
                curs.execute(query)
             
                #KURANGI STOK KARTON FLEKSIBEL
                jmlTot=int(jml)
                query="select iddstoklokasi, jumlahbarang from dstoklokasi where kodebarang='%s' and lokasi='%s' and jumlahbarang>0 and satuan='karton' order by iddstoklokasi"%(kodebrg,lokasi)
                dataBrgPO={}
                for single in ambilBanyakRowSQL(query):
                    dataBrgPO[single[0]]=[single[1]]
                    
                for single in dataBrgPO:
                    jmlRun=dataBrgPO[single][0]
                    idpodet=single
                    lagi=0
                    if jmlRun>=jmlTot:  
                        query="update dstoklokasi set jumlahbarang=jumlahbarang-%s where iddstoklokasi='%s'"%(jmlTot,idpodet)
                        curs.execute(query)
                        lagi=1
                    else:
                        query="update dstoklokasi set jumlahbarang=jumlahbarang-%s where iddstoklokasi='%s'"%(jmlRun,idpodet)
                        curs.execute(query)
                        jmlTot=jmlTot-jmlRun
                        lagi=0
                    
                    if lagi:break
            
                conn2.commit()
                curs.close()
                
                data1={}
                data1['lokasi']=lokasi
                data1['kodebrg']=kodebrg
                data1['namalogin']=namalogin
                
                dic={}
                dic["error"]='false'
                dic["msg"]="%s berkurang %s Q oleh operator %s "%(namabrg,jml,namalogin)
                dic["data"]=data1
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json')
                 
            
            if request.method == 'POST':      
                id1= request.args.get('lokasi')
                kodebrg= request.args.get('kodebrg')
                kodebrgkarton= request.args.get('kodebrgkarton')
                namalogin= request.args.get('namalogin')
                lokasi=id1
                
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                if kodebrgkarton.lower()!="%sk"%kodebrg:
                    
                    query="select * from barangdet where kodebrg='%s' and kodebrgkarton='%s'"%(kodebrg,kodebrgkarton)
                    curs.execute(query)
                    if curs.rowcount==0:
                        
                        data1={}
                        dic={}
                        dic["error"]='true'
                        dic["msg"]="kode barang karton tidak sama dengan kode barang pcs"
                        dic["data"]=data1
                        
                        strDic="%s"%dic
                        strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                        return Response(strDic, mimetype='application/json') 
                
                
                query="update temprefill set status='selesai_karton',lokasikarton='%s',kodebrgkarton='%s',tglambil=now() where kodebrg='%s' and namaoperator='%s' order by idtemprefill desc limit 1"%(lokasi,kodebrgkarton,kodebrg,namalogin)
#                print query
                curs.execute(query)
                
                
                
                conn2.commit()
                curs.close()
                
                data1={}
                data1['lokasi']=lokasi
                data1['kodebrg']=kodebrg
                data1['namalogin']=namalogin
                data1['status']="selesai_karton"
                
                dic={}
                dic["error"]='false'
                dic["msg"]="Karton %s terambil dari %s oleh %s !"%(kodebrg,lokasi,namalogin)
                dic["data"]=data1
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json')         
        @app.route('%s/getBrgKeLokEcer'%(folderAPI), methods=['GET'])
        def getBrgKeLokEcer():
            namaTabel="barangdet"
            namaTabel2="tempRefill"
            
            if request.method == 'GET':
                namalogin= request.args.get('namalogin')
                
                strWhere="where namaoperator='%s' and status='pick_karton'"%namalogin
                    
                return bikinGetJSONExt(namaTabel2,strWhere)   
            
        @app.route('%s/deleteTempRefill'%(folderAPI), methods=['DELETE'])
        def deleteTempRefill():
            namaTabel="tempRefill"
            
            if request.method == 'DELETE':                
                id1= request.args.get('id')
         
                conn2=mysql.get_db()
                curs=conn2.cursor()
                    
                query="delete from temprefill where idtemprefill='%s'"%id1
                curs.execute(query)
              
                conn2.commit()
                curs.close()
                
                dic={}
                dic["error"]='false'
                dic["msg"]="Temp Refill ID %s terhapus"%(id1)
                dic["data"]=id1
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json')     
        
        @app.route('%s/deleteTempRefillNew'%(folderAPI), methods=['DELETE'])
        def deleteTempRefillNew():
            namaTabel="tempRefill"
            
            if request.method == 'DELETE':                
                id1= request.args.get('id')
         
                conn2=mysql.get_db()
                curs=conn2.cursor()
             
            
                query="select kodebrg,jmlambil,lokasikarton from temprefill where idtemprefill='%s'"%id1
                print query
                dapat=ambilSatuRowSQL(query)
                if'%s'%dapat[1]=="None":
                    query="select lokasi from dstoklokasi where kodebarang='%s' and satuan='karton' order by tglmasuk limit 1"%dapat[0]
                    lokasi=ambilSatuRowSQL(query)[0]
                    query="delete from temprefill where idtemprefill='%s'"%id1
                    curs.execute(query)
                    conn2.commit()
                    curs.close()
                    
                    dic={}
                    dic["error"]='false'
                    dic["msg"]="BALIKAN BARANG KE LOKASI %s"%(lokasi)
                    dic["data"]=id1
                    
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                    return Response(strDic, mimetype='application/json') 
                
                query="select jmlkarton from barangdet where kodebrg='%s' limit 1"%dapat[0]
                jmlkarton=ambilSatuRowSQL(query)
             
                jml = int(dapat[1]) / int(jmlkarton[0])
                
                
         
                query="select iddstoklokasi from dstoklokasi where lokasi='%s' and kodebarang='%s' and jumlahbarang>0 limit 1"%(dapat[2],dapat[0])
                curs.execute(query)
                if curs.rowcount==0:
                    query="select iddstoklokasi from dstoklokasi where lokasi='%s' and kodebarang='%s' order by tglmasuk desc limit 1"%(dapat[2],dapat[0])
                    curs.execute(query)
                    if curs.rowcount==0:
                        data1={}
                        dic={}
                        dic["error"]='true'
                        dic["msg"]="Tidak Bisa Terhapus [!]"
                        theCon.close()
                        strDic="%s"%dic
                        strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                        return Response(strDic, mimetype='application/json')
                iddstok = ambilSatuRowSQL(query)
                print query
                print "ini id dstok:",iddstok
                query="delete from temprefill where idtemprefill='%s'"%id1
                curs.execute(query)
                 
                query="update dstoklokasi set jumlahbarang=jumlahbarang+%s where iddstoklokasi='%s'"%(jml,iddstok[0])
                curs.execute(query)
                print query
                
                conn2.commit()
                curs.close()
                
                dic={}
                dic["error"]='false'
                dic["msg"]="BALIKAN BARANG KE LOKASI %s"%(dapat[2])
                dic["data"]=id1
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json') 
            
        @app.route('%s/confirmStok'%(folderAPI), methods=['GET','POST','PUT'])
        def confirmStok():
            namaTabel="reffilertask"
            
            if request.method == 'GET':
                strWhere=""
                #query="select idreftask,lokasi,namabarang,count(*)tot,tanggal from reffilertask where userambil='' and status='refiller' group by kodebarang order by tanggal desc"
                conn=mysql.get_db()
                theCon=conn.cursor()
             
                query="select kodebarang from reffilertask where userambil='' and status='refiller' group by kodebarang"
                theCon.execute(query)
                if theCon.rowcount>0:
                    dapat=ambilBanyakRowSQL(query)
                    strKB="('-'"
                    for single in dapat:
                        strKB+=",'%s'"%single[0]
                    strKB+=")"
                query="select idreftask,lokasi,namabarang,tanggal from reffilertask where userambil='' and status='refiller' and kodebarang in %s order by tanggal desc"%strKB
                print query
                dataCol=["idreftask","lokasi","namabarang","total"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
            
            if request.method == 'PUT':         
                id1= request.args.get('idtask')  
                id2= request.args.get('user')
          
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                query="select kodebarang,lokasi,namabarang,userambil from reffilertask where idreftask='%s'"%id1
                userambil=ambilSatuRowSQL(query)[3]
                if userambil!="":
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Tugas Sudah Di Ambil Oleh %s"%userambil
                    curs.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
                dapat=ambilSatuRowSQL(query)
           
                query="insert into temprefill (namaoperator,tglref,kodebrg,namabrg,lokasi,status) values('%s',now(),'%s','%s','%s','collect')"%(id2,dapat[0],dapat[2],dapat[1])
                curs.execute(query)
        
                query="update reffilertask set userambil='%s' where idreftask='%s'"%(id2,id1)
                curs.execute(query)
                
                conn2.commit()
                curs.close()
                
                data1={}
                data1['user']=id2
                data1['status']="Task Diambil"
                
                dic={}
                dic["error"]='false'
                dic["msg"]="Task Diambil oleh %s"%id2
                dic["data"]=data1
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json')         
            
            if request.method == 'POST':      
                id1= request.args.get('lokasi')
                kodebrg= request.args.get('kodebarang')
                noso= request.args.get('noso')
                iddsales= request.args.get('iddsales')
                lokasi=id1
                
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                query="select namabrg from barang where kodebrg='%s' limit 1"%kodebrg
                namabrg=ambilSatuRowSQL(query)[0]
             
                if lokasi=="":
                    lokasi="Lokasi Tidak Ditemukan [!]"
                    
                print lokasi
                
             
                query="insert into %s (kodebarang,lokasi,namabarang,status,noso,tanggal) value ('%s','%s','%s','refiller','%s',now())"%(namaTabel,kodebrg,lokasi,namabrg,noso)
                curs.execute(query)
                
                query="update dsalesorder set stat1='skip' where id='%s'"%(iddsales)
                curs.execute(query)
             
                inserted_id = curs.lastrowid
                
                conn2.commit()
                curs.close()
                
                data1={}
                data1['id']=inserted_id
                data1['lokasi']=lokasi
                data1['kodebrg']=kodebrg
                data1['namabrg']=namabrg
                data1['status']="Task Baru"
                
                dic={}
                dic["error"]='false'
                dic["msg"]="Task Baru"
                dic["data"]=data1
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json')  
        @app.route('%s/getJmlReffiler'%(folderAPI), methods=['GET','PUT','POST'])
        def getJmlReffiler():
            

            namaTabel="barangdet"
            namaTabel2="tempRefill"
            if request.method == 'GET':
             
                kodebar = request.args.get('kodebar')
                idrefill = request.args.get('idrefill')
                
                query="select CONVERT((sum(jumlahbarang)), SIGNED)jumlahbarang from dstoklokasi where kodebarang='%s' and satuan='' group by kodebarang"%(kodebar)
                dapat=ambilSatuRowSQL(query)
                
                query="select '%s' stok,lokasi,namabrg,if(kodebrgkarton is null,'Tidak Ada Barcode',kodebrgkarton),jmlambil from temprefill where idtemprefill='%s'"%(dapat[0],idrefill)
                strWhere=""
                print query
                
                dataCol=["stok","lokasi","namabrg","kodebrgkarton","jmlambil"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
            
            if request.method == 'PUT':          
                dapat= request.get_json()
                kodebar= dapat['kodebarang']
                lokasi= dapat['lokasi']
                jml= dapat['jumlahbarang']
                user= dapat['operator']
                
                conn2=mysql.get_db()
                curs=conn2.cursor()
                query="select kodebarangkarton from dstoklokasi where kodebarang='%s' and lokasi='%s' and kodebarangkarton!='' order by tglmasuk desc"%(kodebar,lokasi)
                try:kodebarangkarton=ambilSatuRowSQL(query)[0]
                except:kodebarangkarton=""
             
                print kodebarangkarton
                #query="insert into dstoklokasi(kodebarang,kodebarangkarton,tglmasuk,lokasi,operator,tglmasuk,jumlahbarang,satuan,stokawal,sumber) values ('%s','%s','%s','%s',now(),'%s','%s','%s','opname')"%(kodebrgSat,kodebrgkarton,lokasi,namalogin,jumlahbarang,satuan,jumlahbarang)
                #curs.execute(query)
            
                query="""insert into dstoklokasi(kodebarang,kodebarangkarton,tglmasuk,lokasi,jumlahbarang,operator,stokawal,sumber)
                    values('%s','%s',now(),'%s','%s',trim('%s'),'%s','Refill')"""%(kodebar,kodebarangkarton,lokasi,jml,user,jml)
                curs.execute(query)
                print query
            
                conn2.commit()
                curs.close()
                
                data1={}
                dic={}
                dic["error"]='false'
                dic["msg"]="Barang Di Tambah"
                dic["data"]=""
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json')
            
            if request.method == 'POST': 
            
                dapat= request.get_json()
                idrefill= dapat['id']
                
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                query="update temprefill set status='selesai_refill',tgldrop=now() where idtemprefill='%s'"%(idrefill)
                curs.execute(query)
            
                conn2.commit()
                curs.close()
                
                data1={}
                dic={}
                dic["error"]='false'
                dic["msg"]="Refill Selesai"
                dic["data"]=""
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json')
            
        @app.route('%s/callCC'%(folderAPI), methods=['GET','POST','PUT'])
        def callCC():
            namaTabel="reffilertask"
            
            if request.method == 'GET':
                satuan= request.args.get('satuan')
                print satuan
                conn=mysql.get_db()
                theCon=conn.cursor()
                
                    
                if satuan=="0":
                    query="select idreftask from reffilertask where userambil='' and status='cc' and lokasi not like '9.%' group by kodebarang"
                    theCon.execute(query)
                    if theCon.rowcount>0:
                        dapat=ambilBanyakRowSQL(query)
                        strKB="('-'"
                        for single in dapat:
                            strKB+=",'%s'"%single[0]
                        strKB+=")"
                    strWhere=""
                    query="select idreftask,lokasi,namabarang,tanggal from reffilertask where userambil='' and status='cc' and idreftask in %s order by tanggal desc"%(strKB)
                    print query
                    dataCol=["idreftask","lokasi","namabarang","total"]
                    return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
                else:
                    strNot = "and lokasi not like '1.%' and lokasi not like '2.%' and lokasi not like '3.%'"
                    query="select idreftask from reffilertask where userambil='' and status='cc' %s group by kodebarang"%strNot
                    theCon.execute(query)
                    if theCon.rowcount>0:
                        dapat=ambilBanyakRowSQL(query)
                        strKB="('-'"
                        for single in dapat:
                            strKB+=",'%s'"%single[0]
                        strKB+=")"
                    strWhere=""
                    query="select idreftask,lokasi,namabarang,tanggal from reffilertask where userambil='' and status='cc' and idreftask in %s order by tanggal desc"%(strKB)
                    print query
                    dataCol=["idreftask","lokasi","namabarang","total"]
                    return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
            
            if request.method == 'PUT':         
                id1= request.args.get('idtask')  
                user= request.args.get('user')
          
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                #query="select kodebarang,lokasi,namabarang from reffilertask where idreftask='%s'"%id1
                #dapat=ambilSatuRowSQL(query)
           
                #query="insert into temprefill (namaoperator,tglref,kodebrg,namabrg,lokasi,status) values('%s',now(),'%s','%s','%s','collect')"%(user,dapat[0],dapat[2],lokasi)
                #curs.execute(query)
                
                query="select kodebarang,lokasi from reffilertask where idreftask='%s'"%(id1)
                try:dapat=ambilSatuRowSQL(query)
                except:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Tidak Bisa Mengambil Tugas"
                    theCon.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
        
                query="update reffilertask set userambil='%s' where kodebarang='%s' and lokasi='%s'"%(user,dapat[0],dapat[1])
                curs.execute(query)
                
                conn2.commit()
                curs.close()
                
                data1={}
                data1['kodebarang']=dapat[0]
                data1['user']=user
                data1['status']="Task Diambil"
                
                dic={}
                dic["error"]='false'
                dic["msg"]="Stok Diperbarui Oleh %s"%user
                dic["data"]=data1
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json')         
            
            if request.method == 'POST':      
                id1= request.args.get('lokasi')
                kodebrg= request.args.get('kodebarang')
                noso= request.args.get('noso')
                lokasi=id1
                
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
             
                if lokasi=="":
                    lokasi="Lokasi Tidak Ditemukan [!]"
                    
                print lokasi
                
                query="select namabrg from barang where kodebrg='%s'"%kodebrg
                namabrg=ambilSatuRowSQL(query)[0]
                
             
                query="insert into %s (kodebarang,lokasi,namabarang,status,noso,tanggal) value ('%s','%s','%s','cc','%s',now())"%(namaTabel,kodebrg,lokasi,namabrg,noso)
                curs.execute(query)
             
                inserted_id = curs.lastrowid
                
                conn2.commit()
                curs.close()
                
                data1={}
                data1['id']=inserted_id
                data1['lokasi']=lokasi
                data1['kodebrg']=kodebrg
                data1['namabrg']=namabrg
                data1['status']="Task Baru"
                
                dic={}
                dic["error"]='false'
                dic["msg"]="Task Baru"
                dic["data"]=data1
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json')
if 1:# Stok Opname
    
        @app.route('%s/getStokLocation'%(folderAPI), methods=['GET', 'PUT'])
        def getLocationInfo():
            namaTabel="dstoklokasi"
            if request.method == 'GET':
                
                id1= request.args.get('lokasi')
                id2= request.args.get('barcode')
                print id2
                if '%s'%id2=="":
                    strWhere=""
                    query="select trim(kodebarang),iddstoklokasi,trim(kodebarangkarton) from %s where lokasi='%s' order by tglmasuk desc limit 1"%(namaTabel,id1)
                    conn=mysql.get_db()
                    theCon=conn.cursor()
                    theCon.execute(query)
                    if theCon.rowcount==0:
                        data1={}
                        dic={}
                        dic["error"]='true'
                        dic["msg"]="Lokasi Tidak Ada"
                        theCon.close()
                        strDic="%s"%dic
                        strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                        return Response(strDic, mimetype='application/json')
                    dapat=ambilSatuRowSQL(query)
                    query="select trim(barcode) from barang where kodebrg='%s' limit 1"%dapat[0]
                    try:barcode=ambilSatuRowSQL(query)[0]
                    except:
                        query="select trim(kodebrgpack) from barangdet where kodebrg='%s' limit 1"%dapat[0]
                        try:barcode=ambilSatuRowSQL(query)[0]
                        except:
                            query="select trim(kodebrgkarton) from barangdet where kodebrg='%s' limit 1"%dapat[0]
                            try:barcode=ambilSatuRowSQL(query)[0]
                            except:
                                barcode=dapat[2]
                    query="""select trim(kodebarang),'%s' kodebarangkarton,CONVERT((sum(jumlahbarang)), SIGNED)jumlahbarang,satuan
                        ,(select namabrg from barang where trim(kodebrg)=trim(kodebarang) limit 1) namabrg,%s iddstoklokasi
                        from %s where lokasi='%s' and kodebarang='%s' group by kodebarang order by tglmasuk desc limit 1"""%(barcode,dapat[1],namaTabel,id1,dapat[0])
                   
                    theCon.close()
                    dataCol=["kodebarang","kodebarangkarton","jumlahbarang","satuan","namabrg","iddstoklokasi"]
                    return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
                else:
                    strWhere=""
                    conn=mysql.get_db()
                    theCon=conn.cursor()
                    query="select trim(kodebrg) from barang where barcode='%s' limit 1"%id2
                    try:kodebarang=ambilSatuRowSQL(query)[0]
                    except:
                        query="select trim(kodebrg) from barangdet where kodebrgpack='%s' or kodebrgkarton='%s' limit 1"%(id2,id2)
                        try:kodebarang=ambilSatuRowSQL(query)[0]
                        except:
                            query="select trim(kodebarang) from dstoklokasi where kodebarangkarton='%s' limit 1"%id2
                            try:kodebarang=ambilSatuRowSQL(query)[0]
                            except:
                                data1={}
                                dic={}
                                dic["error"]='true'
                                dic["msg"]="Kode Barang Tidak Ditemukan"
                                theCon.close()
                                strDic="%s"%dic
                                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                                return Response(strDic, mimetype='application/json')
                    
                    query="select kodebarang from dstoklokasi where lokasi='%s' and kodebarang='%s' and satuan='' order by tglmasuk desc"%(id1,kodebarang)
                    print query
                    theCon.execute(query)
                    if theCon.rowcount==0:
                        data1={}
                        dic={}
                        data1['kodebrg']=kodebarang
                        dic["data"]=data1
                        dic["error"]='true'
                        dic["msg"]="Barang Tidak Ada Riwayat Di Bin Ini"
                        theCon.close()
                        strDic="%s"%dic
                        strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                        return Response(strDic, mimetype='application/json')
                    kodebarang=ambilSatuRowSQL(query)[0]
                    query="""select trim(kodebarang),kodebarangkarton,CONVERT((sum(jumlahbarang)), SIGNED)jumlahbarang,satuan
                        ,(select namabrg from barang where trim(kodebrg)=trim(kodebarang) limit 1) namabrg,iddstoklokasi
                        from dstoklokasi where lokasi='%s' and kodebarang='%s'  group by kodebarang order by tglmasuk desc limit 1 """%(id1,kodebarang)
                    
                    theCon.close()
                    dataCol=["kodebarang","kodebarangkarton","jumlahbarang","satuan","namabrg","iddstoklokasi"]
                    return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
        
        @app.route('%s/getStokLocationLepasan'%(folderAPI), methods=['GET', 'PUT'])
        def getStokLocationLepasan():
            namaTabel="dstoklokasi"
            if request.method == 'GET':
                
                id1= request.args.get('lokasi')
                id2= request.args.get('kodebarang')
                strWhere=""
                query="""select trim(kodebarang),kodebarangkarton,CONVERT((sum(jumlahbarang)), SIGNED)jumlahbarang,satuan
                    ,(select namabrg from barang where trim(kodebrg)=trim(kodebarang) limit 1) namabrg,iddstoklokasi
                    from dstoklokasi where lokasi='%s' and kodebarang='%s' and satuan='' group by kodebarang order by tglmasuk desc limit 1"""%(id1,id2)

                dataCol=["kodebarang","kodebarangkarton","jumlahbarang","satuan","namabrg","iddstoklokasi"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
               
        @app.route('%s/getStokLocationKarton'%(folderAPI), methods=['GET', 'PUT'])
        def getStokLocationKarton():
            namaTabel="dstoklokasi"
            if request.method == 'GET':
                
                id1= request.args.get('kodebarang')
                id2= request.args.get('lokasi')
                
                strWhere=""
                query="""select trim(kodebarang),kodebarangkarton,CONVERT((sum(jumlahbarang)), SIGNED)jumlahbarang,satuan
                ,(select namabrg from barang where trim(kodebrg)=trim(kodebarang) limit 1) namabrg,iddstoklokasi
                from %s where lokasi='%s' and kodebarang='%s' and satuan='karton' group by kodebarang limit 1"""%(namaTabel,id2,id1)
                print query
                
                dataCol=["kodebarang","kodebarangkarton","jumlahbarang","satuan","namabrg","iddstoklokasi"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
            
             
        @app.route('%s/getDataLocationKarton'%(folderAPI), methods=['GET', 'PUT'])
        def getDataLocationKarton():
            namaTabel="dstoklokasi"
            if request.method == 'GET':
                
                id1= request.args.get('lokasi')
                barcode= request.args.get('barcode')
                
                strWhere=""
                if '%s'%barcode=="":
                    query="""select trim(kodebarang),trim(kodebarangkarton),CONVERT((sum(jumlahbarang)), SIGNED)jumlahbarang,
                        (select namabrg from barang where trim(kodebrg)=trim(kodebarang) limit 1) namabrg,iddstoklokasi 
                        from %s where lokasi='%s' and satuan='karton' and jumlahbarang>0 group by kodebarang"""%(namaTabel,id1)
                else:
                    query="""select trim(kodebarang),trim(kodebarangkarton),CONVERT((sum(jumlahbarang)), SIGNED)jumlahbarang,
                        (select namabrg from barang where trim(kodebrg)=trim(kodebarang) limit 1) namabrg,iddstoklokasi 
                        from %s where lokasi='%s' and kodebarangkarton='%s' and satuan='karton' group by kodebarang"""%(namaTabel,id1,barcode)
                print barcode
                
                conn=mysql.get_db()
                theCon=conn.cursor()
                theCon.execute(query)
                if theCon.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Lokasi Tidak Ada Riwayat Barang"
                    dic["data"]=data1
                    theCon.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json') 
              
                theCon.close()
                dataCol=["kodebarang","kodebarangkarton","jumlahbarang","namabrg","iddstoklokasi"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
            
       
        @app.route('%s/getDataLocationInbound'%(folderAPI), methods=['GET', 'PUT'])
        def getDataLocationInbound():
            namaTabel="dstoklokasi"
            if request.method == 'GET':
                
                id1= request.args.get('lokasi')
                barcode= request.args.get('barcode')
                
                strWhere=""
                if '%s'%barcode=="":
                    query="""select trim(kodebarang),trim(kodebarangkarton),CONVERT((sum(jumlahbarang)), SIGNED)jumlahbarang,
                        (select namabrg from barang where trim(kodebrg)=trim(kodebarang) limit 1) namabrg,iddstoklokasi,satuan 
                        from %s where lokasi='%s' and jumlahbarang>0 group by kodebarang"""%(namaTabel,id1)
                else:
                    query="""select trim(kodebarang),trim(kodebarangkarton),CONVERT((sum(jumlahbarang)), SIGNED)jumlahbarang,
                        (select namabrg from barang where trim(kodebrg)=trim(kodebarang) limit 1) namabrg,iddstoklokasi,satuan 
                        from %s where lokasi='%s' and kodebarangkarton='%s' group by kodebarang"""%(namaTabel,id1,barcode)
                print barcode
                
                conn=mysql.get_db()
                theCon=conn.cursor()
                theCon.execute(query)
                if theCon.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Lokasi Tidak Ada Riwayat Barang"
                    dic["data"]=data1
                    theCon.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json') 
              
                theCon.close()
                dataCol=["kodebarang","kodebarangkarton","jumlahbarang","namabrg","iddstoklokasi","satuan"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
             
        @app.route('%s/getStokKodeBarang'%(folderAPI), methods=['GET', 'PUT', ])
        def getStokKodeBrang():
            namaTabel="dstoklokasi"
            if request.method == 'GET':
                
                id1= request.args.get('kodebarang')
                satuan= request.args.get('satuan')
                
#                strWhere="where kodebarang='%s' and jumlahbarang>0"%id1
                strWhere="where (kodebarangkarton='%s' or kodebarang='%s') and jumlahbarang>0 and satuan='%s'"%(id1,id1,satuan)
                
                namatabel=namaTabel    
                query="describe %s"%namatabel
                conn=mysql.get_db()
                theCon=conn.cursor()
                
                dapatCol=[]
                theCon.execute(query)
                for single in ambilBanyakRowSQL(query):
                    dapatCol.append(single[0].lower())
                
                
                listSel=dapatCol
                
                autoAddTabel(namaTabel,listSel)
                
#                listSel.append("jmlkarton")
                
                strSelect=""
                for single in listSel:strSelect+="`%s`,"%single
                strSelect=strSelect[0:len(strSelect)-1]
                
                listSel.append("jmlkarton")
                
                query="""select %s,(select jmlkarton from barangdet where kodebrg=kodebarang order by idbarangdet desc limit 1) jmlkarton from %s %s """%(strSelect,namaTabel,strWhere)
                print query
                
                dic={}
                dic["error"]='false'
                dic["msg"]=""
                dic["data"]={}
                dic["data"]["rows"]=[]
                
                if 1:
                
                    for single in ambilBanyakRowSQL(query):
                        data1={}
                        theCol=len(single)
                        
                        for single2 in range(theCol):
                            strData1='%s'%single[single2]
                            strData1=strData1.replace("\"","")
                            strData1=strData1.replace("\'","")
                            if '%s'%strData1=="None":data1[listSel[single2]]=""
                            else:data1[listSel[single2]]=strData1
                        
                        dic["data"]["rows"].append(data1)
                    dic["data"]["total"]=len(dic["data"]["rows"])
                
                strDic="%s"%dic
                #print strDic
                
            #    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
            #    print strDic
                return Response(strDic, mimetype='application/json')
        @app.route('%s/isiStokLokasi'%(folderAPI), methods=['GET', 'PUT', 'POST'])
        def isiStokLokasi():
            namaTabel="dstoklokasi"
            if request.method == 'PUT':                
                id1= request.args.get('lokasi')
                jumlahbrg= request.args.get('jumlahbrg')
                kodebrg= request.args.get('kodebrg')
                kodebrgkarton= request.args.get('kodebrgkarton')
                namalogin= request.args.get('namalogin')
                satuan= '%s'%request.args.get('satuan')
                if satuan=='None':satuan="karton"
                
                lokasi=id1
                
                if lokasi=="None" or kodebrgkarton=="None" or namalogin=='None':
                
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Parameter tidak komplit"
                    dic["data"]=data1
                    
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                    return Response(strDic, mimetype='application/json') 
                
                conn2=mysql.get_db()
                curs=conn2.cursor()
                query="select kodebarang from dstoklokasi where (kodebarang='%s' or kodebarangkarton='%s') and lokasi='%s' and jumlahbarang>0 "%(kodebrg,kodebrgkarton,lokasi)
                curs.execute(query)
                if curs.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Kode barang tidak ada di data lokasi / sudah habis"
                    dic["data"]=data1
                    
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                    return Response(strDic, mimetype='application/json') 
                
                try:kodebrg=ambilSatuRowSQL(query)[0]
                except:kodebrg=""
                
                query="select sum(jumlahbarang) from dstoklokasi where kodebarang='%s' and lokasi='%s'"%(kodebrg,lokasi)
                try:jmlLama=ambilSatuRowSQL(query)[0]
                except:jmlLama=0
                query="insert into dstokopn (kodebarang,jmlin,jmlout,tgl,lokasi,operator,satuan) values ('%s','%s','%s',now(),'%s','%s','%s')"%(kodebrg,jumlahbrg,jmlLama,lokasi,namalogin,satuan)
                curs.execute(query)
                
                query="update dstoklokasi set jumlahbarang='0' where kodebarang = '%s' and lokasi='%s' and jumlahbarang>0 "%(kodebrg,lokasi)
                curs.execute(query)
                query="update dstoklokasi set jumlahbarang='%s',tglpindah=now(),operator='%s' where kodebarang = '%s' and lokasi='%s' order by iddstoklokasi desc limit 1"%(jumlahbrg,namalogin,kodebrg,lokasi)
                curs.execute(query)

                ket="SO Barang : %s Oleh : %s Lokasi : %s Jumlah : %s"%(kodebrg,namalogin,lokasi,jumlahbrg)
                query="insert into rekamjejak (tanggal,kegiatan,operator,keterangan) values (now(),'SO Ganti','%s','%s')"%(namalogin,ket)
                curs.execute(query)

                conn2.commit()
                curs.close()
                
                data1={}
                data1['lokasi']=lokasi
                data1['kodebrg']=kodebrg
                data1['namalogin']=namalogin
                
                dic={}
                dic["error"]='false'
                dic["msg"]="lokasi %s stok %s terisi oleh %s !"%(lokasi,kodebrg,namalogin)
                dic["data"]=data1
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json')                
            
            if request.method == 'POST':      
                
                id1= request.args.get('lokasi')
                kodebrg= request.args.get('kodebrg')
                kodebrgkarton= request.args.get('kodebrg')
                namalogin= request.args.get('namalogin')
                jumlahbarang= request.args.get('jumlahbarang')
                satuan= '%s'%request.args.get('satuan')
                if satuan=='None':satuan="karton"
                
                lokasi=id1
                query="select kodebrg from barangdet where (kodebrgkarton='%s' or kodebrgpack='%s' or kodebrg='%s' or kodebrgkarton='%s' or kodebrgpack='%s' or kodebrg='%s')"%(kodebrg,kodebrg,kodebrg,kodebrgkarton,kodebrgkarton,kodebrgkarton)
                try:kodebrgSat=ambilSatuRowSQL(query)[0]
                except:
                    query="select kodebrg from barang where (trim(barcode)=trim('%s') or trim(barcode)=trim('%s'))"%(kodebrg,kodebrgkarton)
                    try:kodebrgSat=ambilSatuRowSQL(query)[0]
                    except:kodebrgSat=kodebrg
                
                #print query
                
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                query="select * from dstoklokasi where (kodebarangkarton='%s' or kodebarang='%s' or kodebarangkarton='%s' or kodebarang='%s') and jumlahbarang>0 and lokasi='%s'"%(kodebrgSat,kodebrgSat,kodebrg,kodebrg,lokasi)
                print query
                
                curs.execute(query)
                if curs.rowcount>0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Kode Barang di lokasi termasuk masih ada!"
                    dic["data"]=data1
                    
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                    return Response(strDic, mimetype='application/json') 
                    
                query="insert into dstoklokasi(kodebarang,kodebarangkarton,lokasi,operator,tglmasuk,jumlahbarang,satuan,stokawal,sumber) values ('%s','%s','%s','%s',now(),'%s','%s','%s','opname')"%(kodebrgSat,kodebrgkarton,lokasi,namalogin,jumlahbarang,satuan,jumlahbarang)
                curs.execute(query)
                
                ket="SO Barang : %s Oleh : %s Lokasi : %s Jumlah : %s"%(kodebrg,namalogin,lokasi,jumlahbarang)
                query="insert into rekamjejak (tanggal,kegiatan,operator,keterangan) values (now(),'SO Tambah','%s','%s')"%(namalogin,ket)
                curs.execute(query)
                
#                query="update temprefill set status='selesai_refill' where kodebrg='%s' and namaoperator='%s' and status='selesai_karton'"%(kodebrg,namalogin)
#                print query
                
#                curs.execute(query)
                conn2.commit()
                curs.close()
                
                data1={}
                data1['lokasi']=lokasi
                data1['kodebrg']=kodebrg
                data1['namalogin']=namalogin
                data1['status']="ISI Stok Lokasi"
                
                dic={}
                dic["error"]='false'
                dic["msg"]="%s %s terisi ke %s oleh %s !"%(satuan,kodebrg,lokasi,namalogin)
                dic["data"]=data1
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json')         
            
        @app.route('%s/ccStok'%(folderAPI), methods=['PUT','POST'])
        def ccStok():
            namaTabel="dstoklokasi"
            if request.method == 'PUT':                
                id1= request.args.get('lokasi')
                jml= request.args.get('jumlahbarang')
                barcode= request.args.get('barcode')
                user= request.args.get('namalogin')
                kodebarang= request.args.get('kodebarang')
                iddstok=request.args.get('iddstok')
                lokasi=id1
      
                conn2=mysql.get_db()
                curs=conn2.cursor()
                query="select trim(kodebrg) from barang where barcode='%s' limit 1"%barcode
                curs.execute(query)
                if curs.rowcount==0:
                    query="select trim(kodebrg) from barangdet where kodebrgpack='%s' or kodebrgkarton='%s' limit 1"%(barcode,barcode)
                    curs.execute(query)
                    if curs.rowcount==0:
                        query="select trim(kodebarang) from dstoklokasi where kodebarangkarton='%s' and satuan='' order by tglmasuk desc limit 1"%(barcode)
                        curs.execute(query)
                        if curs.rowcount==0:
                            data1={}
                            dic={}
                            dic["error"]='true'
                            dic["msg"]="Barcode Tidak Sesuai"
                            dic["data"]=data1
                            curs.close()
                            strDic="%s"%dic
                            strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                            return Response(strDic, mimetype='application/json') 
                print query
                kodebrg=ambilSatuRowSQL(query)[0]
                print kodebrg,kodebarang
                if kodebrg!=kodebarang:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Barcode Tidak Sama"
                    dic["data"]=data1
                    curs.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                    return Response(strDic, mimetype='application/json') 
                
                query="select CONVERT((sum(jumlahbarang)), SIGNED)jumlahbarang from dstoklokasi where kodebarang='%s' and lokasi='%s' group by lokasi"%(kodebrg,lokasi)
                try:jmlLama=ambilSatuRowSQL(query)[0]
                except:jmlLama=0
                query="insert into dstokopn (kodebarang,jmlin,jmlout,tgl,lokasi,operator,satuan) values ('%s','%s','%s',now(),'%s','%s','')"%(kodebrg,jml,jmlLama,lokasi,user)
                curs.execute(query)
                
                #hapus Stok Sesuai Kodarang dan Lokasi
                query="update dstoklokasi set jumlahbarang='0' where kodebarang='%s' and lokasi='%s' and jumlahbarang>0 "%(kodebrg,lokasi)
                curs.execute(query)
                
                #update Stok Sesuai Iddstok yang di ambil dari halaman page 
                query="update dstoklokasi set jumlahbarang='%s',tglpindah=now(),operator='%s',tglmasuk=now() where iddstoklokasi='%s' limit 1"%(jml,user,iddstok)
                curs.execute(query)

                ket="SO Barang : %s Oleh : %s Lokasi : %s Jumlah : %s"%(kodebrg,user,lokasi,jml)
                query="insert into rekamjejak (tanggal,kegiatan,operator,keterangan) values (now(),'SO Ganti','%s','%s')"%(user,ket)
                curs.execute(query)

                conn2.commit()
                curs.close()
                
                data1={}
                data1['lokasi']=lokasi
                data1['kodebrg']=kodebrg
                data1['namalogin']=user
                
                dic={}
                dic["error"]='false'
                dic["msg"]="lokasi %s stok %s diubah oleh %s !"%(lokasi,kodebrg,user)
                dic["data"]=data1
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json') 
            
            if request.method == 'POST':                
                lokasi= request.args.get('lokasi')
                jumlahbarang= request.args.get('jumlahbarang')
                kodebarangkarton= request.args.get('kodebarangkarton')
                namauser= request.args.get('namauser')
                kodebarang= request.args.get('kodebarang')
                satuan= '%s'%request.args.get('satuan')
                if satuan=='None':satuan="karton"
                
                conn2=mysql.get_db()
                curs=conn2.cursor()
                query="select kodebarang from dstoklokasi where kodebarangkarton='%s' order by tglmasuk desc limit 1"%(kodebarangkarton)
                curs.execute(query)
                if curs.rowcount==0:
                    query="select kodebrg from barang where barcode='%s'"%(kodebarangkarton)
                    curs.execute(query)
                    if curs.rowcount==0:
                        query="select kodebrg from barangdet where kodebrgpack='%s' or kodebrgkarton='%s' limit 1"%(kodebarangkarton,kodebarangkarton)
                        curs.execute(query)
                        if curs.rowcount==0:
                            data1={}
                            dic={}
                            dic["error"]='true'
                            dic["msg"]="Barcode Tidak Ditemukan"
                            dic["data"]=data1
                            curs.close()
                            strDic="%s"%dic
                            strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                            return Response(strDic, mimetype='application/json') 
                kodebarang=ambilSatuRowSQL(query)[0] 
                
                query="select kodebarang from dstoklokasi where lokasi='%s' and jumlahbarang>0 limit 1"%(lokasi)
                curs.execute(query)
                if curs.rowcount==0:
                    #tambah barang di bin
                    query="insert into dstoklokasi(kodebarang,kodebarangkarton,lokasi,operator,tglmasuk,jumlahbarang,satuan,stokawal,sumber) values ('%s','%s','%s','%s',now(),'%s','%s','%s','opname')"%(kodebarang,kodebarangkarton,lokasi,namauser,jumlahbarang,satuan,jumlahbarang)
                    curs.execute(query)
                    conn2.commit()
                    curs.close()
                    
                    data1={}
                    data1['lokasi']=lokasi
                    data1['kodebrg']=kodebarang
                    data1['namalogin']=namauser
                    
                    dic={}
                    dic["error"]='false'
                    dic["msg"]="lokasi %s stok %s diubah oleh %s !"%(lokasi,kodebarang,namauser)
                    dic["data"]=data1
                    
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                    return Response(strDic, mimetype='application/json')  

                kodebaranglama=ambilSatuRowSQL(query)[0]
                #hapus Stok Di Bin Lama
                query="update dstoklokasi set jumlahbarang='0' where kodebarang='%s' and lokasi='%s' and jumlahbarang>0"%(kodebaranglama,lokasi)
                curs.execute(query)
                
                #tambah barang di bin
                query="insert into dstoklokasi(kodebarang,kodebarangkarton,lokasi,operator,tglmasuk,jumlahbarang,satuan,stokawal,sumber) values ('%s','%s','%s','%s',now(),'%s','%s','%s','opname')"%(kodebarang,kodebarangkarton,lokasi,namauser,jumlahbarang,satuan,jumlahbarang)
                curs.execute(query)

                ket="SO Barang : %s Oleh : %s Lokasi : %s Jumlah : %s"%(kodebarang,namauser,lokasi,jumlahbarang)
                query="insert into rekamjejak (tanggal,kegiatan,operator,keterangan) values (now(),'SO Ganti','%s','%s')"%(namauser,ket)
                curs.execute(query)

                conn2.commit()
                curs.close()
                
                data1={}
                data1['lokasi']=lokasi
                data1['kodebrg']=kodebarang
                data1['namalogin']=namauser
                
                dic={}
                dic["error"]='false'
                dic["msg"]="lokasi %s stok %s diubah oleh %s !"%(lokasi,kodebarang,namauser)
                dic["data"]=data1
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json')  
            
        @app.route('%s/ccStokKarton'%(folderAPI), methods=['PUT'])
        def ccStokKarton():
            namaTabel="dstoklokasi"
            if request.method == 'PUT':                
                id1= request.args.get('lokasi')
                jml= request.args.get('jumlahbarang')
                barcode= request.args.get('barcode')
                user= request.args.get('namalogin')
                kodebarang= request.args.get('kodebarang')
                iddstok=request.args.get('iddstok')
                lokasi=id1
      
                conn2=mysql.get_db()
                curs=conn2.cursor()
                query="select trim(kodebrg) from barang where barcode='%s' and kodebrg='%s' limit 1"%(barcode,kodebarang)
                curs.execute(query)
                if curs.rowcount==0:
                    query="select trim(kodebrg) from barangdet where kodebrgpack='%s' or kodebrgkarton='%s' and kodebrg='%s' limit 1"%(barcode,barcode,kodebarang)
                    curs.execute(query)
                    if curs.rowcount==0:
                        query="select trim(kodebarang) from dstoklokasi where kodebarangkarton='%s' and satuan='karton' and kodebarang='%s' order by tglmasuk desc limit 1"%(barcode,kodebarang)
                        curs.execute(query)
                        if curs.rowcount==0:
                            data1={}
                            dic={}
                            dic["error"]='true'
                            dic["msg"]="Barcode Tidak Sesuai"
                            dic["data"]=data1
                            curs.close()
                            strDic="%s"%dic
                            strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                            return Response(strDic, mimetype='application/json') 
 
                
                query="select CONVERT((sum(jumlahbarang)), SIGNED)jumlahbarang from dstoklokasi where kodebarang='%s' and lokasi='%s' and satuan='karton' group by lokasi"%(kodebarang,lokasi)
                try:jmlLama=ambilSatuRowSQL(query)[0]
                except:jmlLama=0
                query="insert into dstokopn (kodebarang,jmlin,jmlout,tgl,lokasi,operator,satuan) values ('%s','%s','%s',now(),'%s','%s','karton')"%(kodebarang,jml,jmlLama,lokasi,user)
                curs.execute(query)
                
                #hapus Stok Sesuai Kodarang dan Lokasi
                query="update dstoklokasi set jumlahbarang='0' where kodebarang='%s' and lokasi='%s' and satuan='karton' and jumlahbarang>0 "%(kodebarang,lokasi)
                curs.execute(query)
                
                #update Stok Sesuai Iddstok yang di ambil dari halaman page 
                query="update dstoklokasi set jumlahbarang='%s',tglpindah=now(),operator='%s',tglmasuk=now() where iddstoklokasi='%s' limit 1"%(jml,user,iddstok)
                curs.execute(query)

                ket="SO Barang : %s Oleh : %s Lokasi : %s Jumlah : %s"%(kodebarang,user,lokasi,jml)
                query="insert into rekamjejak (tanggal,kegiatan,operator,keterangan) values (now(),'SO Ganti','%s','%s')"%(user,ket)
                curs.execute(query)

                conn2.commit()
                curs.close()
                
                data1={}
                data1['lokasi']=lokasi
                data1['kodebrg']=kodebarang
                data1['namalogin']=user
                
                dic={}
                dic["error"]='false'
                dic["msg"]="lokasi %s stok %s terisi oleh %s !"%(lokasi,kodebarang,user)
                dic["data"]=data1
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json')              
         
        @app.route('%s/deleteStokLokasi'%(folderAPI), methods=['DELETE'])
        def deleteStokLokasi():
            namaTabel="dstoklokasi"
            
            if request.method == 'DELETE': 
            
                lokasi= request.args.get('lokasi')
                kodebarang= request.args.get('kodebrg')
                operator= request.args.get('namalogin')
                
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                query="delete from dstoklokasi where (kodebarang='%s' or kodebarangkarton='%s') and lokasi='%s' and jumlahbarang>0"%(kodebarang,kodebarang,lokasi)
                curs.execute(query)
                ket="Hapus Barang : %s Oleh : %s Lokasi : %s"%(kodebarang,operator,lokasi)
                query="insert into rekamjejak (tanggal,kegiatan,operator,keterangan) values (now(),'Hapus','%s','%s')"%(operator,ket)
                curs.execute(query)
                conn2.commit()
                curs.close()
                
                dic={}
                dic["error"]='false'
                dic["msg"]="Stok %s lokasi %s terhapus"%(kodebarang,lokasi)
                dic["data"]=ket
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json')                
        @app.route('%s/pindahStokLokasi'%(folderAPI), methods=['PUT'])
        def pindahStokLokasi():
            namaTabel="dstoklokasi"
            
            
            if request.method == 'PUT':                
                id1= request.args.get('lokasi')
                lokasiBaru= request.args.get('lokasiBaru')
                namalogin= request.args.get('namalogin')
                operator= namalogin
                lokasi=id1
                
                if lokasi=="None" or lokasiBaru=="None" or namalogin=='None':
                
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Parameter tidak komplit"
                    dic["data"]=data1
                    
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                    return Response(strDic, mimetype='application/json') 
                
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                query="select kodebarang from dstoklokasi where lokasi='%s' and jumlahbarang>0 "%(lokasi)
                curs.execute(query)
                if curs.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Barang tidak ada di data lokasi / sudah habis"
                    dic["data"]=data1
                    
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                    return Response(strDic, mimetype='application/json') 
                
                try:kodebrg=ambilSatuRowSQL(query)[0]
                except:kodebrg=""
                
                query="update dstoklokasi set lokasi='%s',tglpindah=now(),operator='%s' where lokasi='%s' and jumlahbarang>0"%(lokasiBaru,namalogin,lokasi)
                print query
                
                curs.execute(query)
                
                ket="Pindah Barang : %s Oleh : %s Lokasi : %s Ke Lokasi %s"%(kodebrg,operator,lokasi,lokasiBaru)
                query="insert into rekamjejak (tanggal,kegiatan,operator,keterangan) values (now(),'Pindah','%s','%s')"%(operator,ket)
                curs.execute(query)
                
                conn2.commit()
                curs.close()
                
                data1={}
                data1['lokasi']=lokasi
                data1['lokasiBaru']=lokasiBaru
                data1['kodebrg']=kodebrg
                data1['namalogin']=namalogin
                
                dic={}
                dic["error"]='false'
                dic["msg"]="lokasi %s di pindah ke %s terisi oleh %s !"%(lokasi,lokasiBaru,namalogin)
                dic["data"]=data1
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json')                
        @app.route('%s/pindahStokLokasiPerKode'%(folderAPI), methods=['PUT'])
        def pindahStokLokasiPerKode():
            namaTabel="dstoklokasi"
            
            
            if request.method == 'PUT':                
                id1= request.args.get('lokasi')
                lokasiBaru= request.args.get('lokasiBaru')
                kodebrg= request.args.get('kodebrg')
                namalogin= request.args.get('namalogin')
                operator= namalogin
                lokasi=id1
                
                if lokasi=="None" or lokasiBaru=="None" or namalogin=='None':
                
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Parameter tidak komplit"
                    dic["data"]=data1
                    
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                    return Response(strDic, mimetype='application/json') 
                
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                query="select kodebrg from barangdet where kodebrgpack='%s' or kodebrgkarton='%s'"%(kodebrg,kodebrg)
                curs.execute(query)
                if curs.rowcount==0:
                    query="select kodebrg from barang where barcode='%s'"%kodebrg
                    curs.execute(query)
                    if curs.rowcount==0:
                        query="select kodebarang from dstoklokasi where kodebarangkarton='%s'"%kodebrg
                        curs.execute(query)
                        data1={}
                        dic={}
                        if curs.rowcount==0:
                            curs.execute(query)
                            dic["error"]='true'
                            dic["msg"]="Barang tidak ada di data lokasi / sudah habis"
                            dic["data"]=data1
                        
                        strDic="%s"%dic
                        strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                        return Response(strDic, mimetype='application/json') 
                    
                try:kodebrg=ambilSatuRowSQL(query)[0]
                except:kodebrg=""
                
                query="select kodebarang from dstoklokasi where lokasi='%s' and (kodebarang ='%s' or kodebarangkarton='%s') and jumlahbarang>0 "%(lokasi,kodebrg,kodebrg)
                curs.execute(query)
                if curs.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Barang tidak ada di data lokasi / sudah habis"
                    dic["data"]=data1
                    
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                    return Response(strDic, mimetype='application/json') 
                
               
                
                query="update dstoklokasi set lokasi='%s',tglpindah=now(),operator='%s' where lokasi='%s' and (kodebarang ='%s' or kodebarangkarton='%s') and jumlahbarang>0"%(lokasiBaru,namalogin,lokasi,kodebrg,kodebrg)
                print query
                
                curs.execute(query)
                
                ket="Pindah Barang : %s Oleh : %s Lokasi : %s Ke Lokasi %s"%(kodebrg,operator,lokasi,lokasiBaru)
                query="insert into rekamjejak (tanggal,kegiatan,operator,keterangan) values (now(),'Pindah','%s','%s')"%(operator,ket)
                curs.execute(query)
                
                conn2.commit()
                curs.close()
                
                data1={}
                data1['lokasi']=lokasi
                data1['lokasiBaru']=lokasiBaru
                data1['kodebrg']=kodebrg
                data1['namalogin']=namalogin
                
                dic={}
                dic["error"]='false'
                dic["msg"]="lokasi %s di pindah ke %s terisi oleh %s !"%(lokasi,lokasiBaru,namalogin)
                dic["data"]=data1
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json') 
        @app.route('%s/pindahLokasiPerJumlah'%(folderAPI), methods=['PUT'])
        def pindahLokasiPerJumlah():
            namaTabel="dstoklokasi"
            
            
            if request.method == 'PUT':                
                id1= request.args.get('lokasi')
                lokasibaru= request.args.get('lokasiBaru')
                kodebrg= request.args.get('kodebrg')
                kodebarangkarton= request.args.get('kodebarangkarton')
                namalogin= request.args.get('namalogin')
                jumlah= request.args.get('jml')
                iddstok = request.args.get('iddstok')
                operator= namalogin
                lokasi=id1
                jml=jumlah

                
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                if 0:
                    query="select kodebrg from barangdet where kodebrgpack='%s' or kodebrgkarton='%s'"%(kodebrg,kodebrg)
                    curs.execute(query)
                    if curs.rowcount==0:
                        query="select kodebrg from barang where barcode='%s'"%kodebrg
                        if curs.rowcount==0:
                            data1={}
                            dic={}
                            dic["error"]='true'
                            dic["msg"]="Barang tidak ada di data lokasi / sudah habis"
                            dic["data"]=data1
                            
                            strDic="%s"%dic
                            strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                            return Response(strDic, mimetype='application/json') 
                        
                    try:kodebrg=ambilSatuRowSQL(query)[0]
                    except:kodebrg=""
                
                #update
                query="update dstoklokasi set jumlahbarang=jumlahbarang-%s where lokasi='%s' and (kodebarang ='%s' or kodebarangkarton='%s') and jumlahbarang>0"%(jml,lokasi,kodebrg,kodebrg)
                curs.execute(query)
                
                #insert
                query="insert into dstoklokasi(kodebarang,kodebarangkarton,lokasi,operator,tglmasuk,jumlahbarang,satuan,stokawal,sumber,referensi) values ('%s','%s','%s','%s',now(),'%s','karton','%s','Pecahan Pindah Lokasi','%s')"%(kodebrg,kodebarangkarton,lokasibaru,namalogin,jumlah,jumlah,iddstok)
                curs.execute(query)
                
                ket="Pindah Barang : %s Oleh : %s Lokasi : %s Ke Lokasi %s"%(kodebrg,operator,lokasi,lokasibaru)
                query="insert into rekamjejak (tanggal,kegiatan,operator,keterangan) values (now(),'Pecah Barang','%s','%s')"%(operator,ket)
                curs.execute(query)
                
                conn2.commit()
                curs.close()
                
                data1={}
                data1['lokasi']=lokasi
                data1['lokasiBaru']=lokasibaru
                data1['kodebrg']=kodebrg
                data1['namalogin']=namalogin
                
                dic={}
                dic["error"]='false'
                dic["msg"]="lokasi %s di Pecah ke %s terisi oleh %s !"%(lokasi,lokasibaru,namalogin)
                dic["data"]=data1
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json') 
        @app.route('%s/getDataBarangDstoklokasi'%(folderAPI), methods=['GET', 'POST', 'PUT', 'DELETE'])
        def getDataBarangDstoklokasi():
           
            if request.method == 'GET':
                namaTabel="dstoklokasi"
                
                id1= request.args.get('lokasi')
                id2= request.args.get('barcode')
                
                strWhere="where lokasi='%s' and kodebarangkarton='%s' and jumlahbarang>0"%(id1,id2)                    
                query="select * from %s %s limit 1"%(namaTabel,strWhere)
                
                conn2=mysql.get_db()    
                theCon2=conn2.cursor()
                theCon2.execute(query)
                if theCon2.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Barang Tidak Ditemukan"
                    theCon2.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
                    
                theCon2.close()
                query="""select iddstoklokasi,kodebarang,kodebarangkarton,lokasi,jumlahbarang,(select namabrg from barang where kodebrg=kodebarang)namabrg from %s"""%(namaTabel)
                dataCol=["iddstoklokasi","kodebarang","kodebarangkarton","lokasi","jumlahbarang","namabrg"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
if 1:# TOPED
        @app.route('%s/tokpedGetList'%(folderAPI), methods=['GET', 'POST', 'PUT', 'DELETE'])
        def tokpedGetList():
           
            if request.method == 'GET':
                namaTabel="dsalesorder"
                
                noso= request.args.get('noso')
                
                strWhere="where noso='%s' "%noso                    
                query="select * from %s %s"%(namaTabel,strWhere)
                
                conn2=mysql.get_db()    
                theCon2=conn2.cursor()
                theCon2.execute(query)
                if theCon2.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Nomor PO  Tidak ada "
                    theCon.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
                    
                theCon2.close()
                
                return bikinGetJSONExt(namaTabel,strWhere)
              
        @app.route('%s/tokpedInputData'%(folderAPI), methods=['GET', 'POST', 'PUT', 'DELETE'])
        def tokpedInputData():
           
            if request.method == 'GET':
                namaTabel="dstoklokasi"
                
                lokasi= request.args.get('lokasi')
                barcode= request.args.get('barcode')
                
#               strWhere="where kodebarang='%s' and jumlahbarang>0"%id1
                query="select kodebrg from barang where barcode='%s'"%(barcode)
                try:strKB=ambilSatuRowSQL(query)[0]
                except:
                    query="select kodebrg from barangdet where kodebrgpack='%s' or kodebrgkarton='%s'"%(barcode,barcode)
                    try:strKB=ambilSatuRowSQL(query)[0]
                    except:strKB=""
                strQueryKB=""
                if strKB!="":strQueryKB="or kodebarang ='%s'"%strKB
                
                strWhere="where (kodebarangkarton='%s' or kodebarang='%s' %s) and jumlahbarang>0 and lokasi='%s' limit 1"%(barcode,barcode,strQueryKB,lokasi)
                #strWhere="where (kodebarangkarton='%s' or kodebarang='%s') and jumlahbarang>0 and satuan='' and lokasi='%s' limit 1"%(barcode,barcode,lokasi)
                
                namatabel=namaTabel    
                query="describe %s"%namatabel
                conn=mysql.get_db()
                theCon=conn.cursor()
                
                dapatCol=[]
                theCon.execute(query)
                for single in ambilBanyakRowSQL(query):
                    dapatCol.append(single[0].lower())
                
                
                listSel=dapatCol
                
                autoAddTabel(namaTabel,listSel)
                
#                listSel.append("jmlkarton")
                
                strSelect=""
                for single in listSel:strSelect+="`%s`,"%single
                strSelect=strSelect[0:len(strSelect)-1]
                
                listSel.append("namabrg")
                listSel.append("hjual")
                listSel.append("jmlkarton")
                
                query="""select %s,(select trim(namabrg) from barang where kodebrg=kodebarang order by idbarang desc limit 1),
                    (select hjual from barang where kodebrg=kodebarang order by idbarang desc limit 1) barang,
                    (select jmlkarton from barangdet where kodebrg=kodebarang limit 1) jmlkarton from %s %s """%(strSelect,namaTabel,strWhere)
                print query
                
                dic={}
                dic["error"]='false'
                dic["msg"]=""
                dic["data"]={}
                dic["data"]["rows"]=[]
                
                if 1:
                
                    for single in ambilBanyakRowSQL(query):
                        data1={}
                        theCol=len(single)
                        
                        for single2 in range(theCol):
                            strData1='%s'%single[single2]
                            strData1=strData1.replace("\"","")
                            strData1=strData1.replace("\'","")
                            if '%s'%strData1=="None":data1[listSel[single2]]=""
                            else:data1[listSel[single2]]=strData1
                        
                        dic["data"]["rows"].append(data1)
                    dic["data"]["total"]=len(dic["data"]["rows"])
                
                strDic="%s"%dic
                #print strDic
                
            #    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
            #    print strDic
                return Response(strDic, mimetype='application/json')
            
            if request.method == 'POST':
                namaTabel="hsalesorder"
          
                noso= request.args.get('noso')
                namacustomer= request.args.get('namacustomer')
                
                #
            
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                query="select stat5 from rdsalesorder where noso='%s'"%noso
                try:stat5=ambilSatuRowSQL(query)[0]
                except:stat5=""
                if stat5=="cetak_packing":
                    data1={}
                    dic={}
                    dic["error"]='packing'
                    dic["msg"]="SO Sudah Selesai Packing"
                    dic["data"]=data1
                    
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                    return Response(strDic, mimetype='application/json')
          
                query="select noso from hsalesorder where noso='%s' and kode='%s'"%(noso,namacustomer)
                curs.execute(query)
                if curs.rowcount!=0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="SO Sudah Ada, Silahkan Edit"
                    dic["data"]=data1
                    
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                    return Response(strDic, mimetype='application/json')
                
                #
          
                query="insert into hsalesorder (kode,tanggal,noso,namacustomer) values ('%s',now(),'%s','%s')"%(namacustomer,noso,namacustomer)
                curs.execute(query)

                conn2.commit()
                curs.close()
                    
                data1={}
                data1['noso']=noso
                data1['namacustomer']=namacustomer
                
                dic={}
                dic["error"]='false'
                dic["msg"]="Data Terisi"
                dic["data"]=data1
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                
                return Response(strDic, mimetype='application/json')
            
            if request.method == 'PUT':
                namaTabel="hsalesorder"
                
                noso= request.args.get('noso')
                kode= request.args.get('kode')
                total = request.args.get('total')
                
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                query="update hsalesorder set totalso='%s' where kode='%s' and noso='%s'"%(total,kode,noso)
                curs.execute(query)

                conn2.commit()
                curs.close()
                    
                data1={}
                
                dic={}
                dic["error"]='false'
                dic["msg"]="Data Terinput Type Customer %s SO %s Dengan Total %s"%(kode,noso,total)
                dic["data"]=data1
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                
                return Response(strDic, mimetype='application/json')
        @app.route('%s/editToped'%(folderAPI), methods=['GET','POST','PUT', 'DELETE'])
        def editToped():
            if request.method == 'DELETE': 
      
                iddstoklokasi= request.args.get('iddstoklokasi')
                jml=request.args.get('jumlahbarang')
                
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                jmlTot=int(jml)
             
                query="update dstoklokasi set jumlahbarang=jumlahbarang+%s where iddstoklokasi='%s'"%(jmlTot,iddstoklokasi)
                print query
                curs.execute(query)
                ket=""#%(id1,noso)
                
                conn2.commit()
                curs.close()
                
                dic={}
                dic["error"]='false'
                dic["msg"]="Stok %s Ditambah Jumlah %s"%(iddstoklokasi,jmlTot)
                dic["data"]=ket
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json') 
        @app.route('%s/getIdDtoklokasi'%(folderAPI), methods=['GET','POST','PUT', 'DELETE'])
        def getIdDtoklokasi():
            
            if request.method == 'GET':
                namaTabel="dsalesorder"
                
                kodebarang= request.args.get('kodebarang')
                namabarang= request.args.get('namabarang')
                hargabarang= request.args.get('hargabarang')
                jumlahbarang= request.args.get('jumlahbarang')
                noso= request.args.get('noso')
                lokasi= request.args.get('lokasi')
                user= request.args.get('namalogin')
                iddstoklokasi= request.args.get('iddstoklokasi')
                
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                #query="insert into dsalesorder (kodebarang,namabarang,hargabarang,jumlahbarang,noso) values ('%s','%s','%s','%s','%s')"%(kodebarang,namabarang,hargabarang,jumlahbarang,noso)
                #curs.execute(query)
                
                #query=" select * from dsalesorder where noso='%s' "%(noso)
                #print query
                
                #query="insert into dsalesorder (kodebarang,namabarang,hargabarang,jumlahbarang,noso,stat1,jml1,stat2,stat4,stat3) values ('%s','%s','%s','%s','%s','picking','%s','%s',now(),'%s')"%(kodebarang,namabarang,hargabarang,jumlahbarang,noso,jumlahbarang,user,iddstoklokasi)
                #curs.execute(query)
                jmlTot=int(jumlahbarang)
                
                query="select iddstoklokasi, jumlahbarang from dstoklokasi where  kodebarang='%s' and lokasi='%s' and jumlahbarang>0 order by iddstoklokasi"%(kodebarang,lokasi)
                #print query                    
                dataBrgPO={}
                for single in ambilBanyakRowSQL(query):
                    dataBrgPO[single[0]]=[single[1]]
       
                
                
                for single in dataBrgPO:
                    jmlRun=dataBrgPO[single][0]
                    idpodet=single
                    lagi=0
                    #print dataBrgPO
                    #print jmlRun
                    #print jmlTot
                    #print idpodet
                    if jmlRun>=jmlTot:lagi=1
                    else:lagi=0
                    
                    if lagi:break
             
                #jmlTot=jumlahbarang-jmlRun
                #query="update dstoklokasi set jumlahbarang=jumlahbarang-%s where iddstoklokasi='%s'"%(jmlTot,iddstoklokasi)
                #print query
                #curs.execute(query)
               
                query="select iddstoklokasi from dstoklokasi where iddstoklokasi=%s"%(idpodet)
                #print query
                listSel=["iddstoklokasi"]
                
                conn2.commit()
                curs.close()
                
                dic={}
                dic["error"]='false'
                dic["msg"]=""
                dic["data"]={}
                dic["data"]["rows"]=[]
                
                if 1:
                
                    for single in ambilBanyakRowSQL(query):
                        data1={}
                        theCol=len(single)
                        
                        for single2 in range(theCol):
                            strData1='%s'%single[single2]
                            strData1=strData1.replace("\"","")
                            strData1=strData1.replace("\'","")
                            if '%s'%strData1=="None":data1[listSel[single2]]=""
                            else:data1[listSel[single2]]=strData1
                        
                        dic["data"]["rows"].append(data1)
                    dic["data"]["total"]=len(dic["data"]["rows"])
                
                strDic="%s"%dic
                #print strDic
                
            #    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
            #    print strDic
                return Response(strDic, mimetype='application/json')
        @app.route('%s/inDariTopedToDSO'%(folderAPI), methods=['GET','POST','PUT', 'DELETE'])
        def inDariTopedToDSO():
            
            if request.method == 'POST':
                namaTabel="dsalesorder"
                
                kodebarang= request.args.get('kodebarang')
                namabarang= request.args.get('namabarang')
                hargabarang= request.args.get('hargabarang')
                jumlahbarang= request.args.get('jumlahbarang')
                noso= request.args.get('noso')
                lokasi= request.args.get('lokasi')
                user= request.args.get('namalogin')
                iddstoklokasi= request.args.get('iddstoklokasi')
                karton= request.args.get('karton')
                
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                #query="insert into dsalesorder (kodebarang,namabarang,hargabarang,jumlahbarang,noso) values ('%s','%s','%s','%s','%s')"%(kodebarang,namabarang,hargabarang,jumlahbarang,noso)
                #curs.execute(query)
                
                #query=" select * from dsalesorder where noso='%s' "%(noso)
                #print query
                
                query="insert into rekampicking (lokasi,noso,jumlahambil,kodebarang,tanggal,operator) values ('%s','%s','%s','%s',now(),'%s')"%(lokasi,noso,jumlahbarang,kodebarang,user)
                curs.execute(query)
                
                query="insert into dsalesorder (kodebarang,namabarang,hargabarang,jumlahbarang,noso,stat1,jml1,stat2,stat4,stat3) values ('%s','%s','%s','%s','%s','picking','%s','%s',now(),'%s')"%(kodebarang,namabarang,hargabarang,jumlahbarang,noso,jumlahbarang,user,iddstoklokasi)
                curs.execute(query)
                jmlTot=int(jumlahbarang)
                
                if 0:
                    query="select iddstoklokasi, jumlahbarang from dstoklokasi where  kodebarang='%s' and lokasi='%s' and jumlahbarang>0 order by iddstoklokasi"%(kodebarang,lokasi)
                    #print query                    
                    dataBrgPO={}
                    for single in ambilBanyakRowSQL(query):
                        dataBrgPO[single[0]]=[single[1]]
           
                    
                    
                    for single in dataBrgPO:
                        jmlRun=dataBrgPO[single][0]
                        idpodet=single
                        lagi=0
                        #print dataBrgPO
                        #print jmlRun
                        #print jmlTot
                        #print idpodet
                        if jmlRun>=jmlTot:lagi=1
                        else:lagi=0
                        
                        if lagi:break
                 
                    #jmlTot=jumlahbarang-jmlRun
                
                if karton==1:
                    query="select jmlkarton from barangdet where kodebrg='%s'"%kodebarang
                    jumlahkarton=int(ambilSatuRowSQL(query)[0])
                    jmlTot=jmlTot/jumlahkarton
                    query="update dstoklokasi set jumlahbarang=jumlahbarang-%s where iddstoklokasi='%s'"%(jmlTot,iddstoklokasi)
                    curs.execute(query) 
                else:
                    query="update dstoklokasi set jumlahbarang=jumlahbarang-%s where iddstoklokasi='%s'"%(jmlTot,iddstoklokasi)
                    curs.execute(query)
               
                query="select kodebarang,namabarang,hargabarang,jumlahbarang,noso,(select iddstoklokasi from dstoklokasi where iddstoklokasi='%s') from dsalesorder where noso='%s' "%(iddstoklokasi,noso)
                #print query
                listSel=["kodebarang","namabarang","hargabarang","jumlahbarang","noso","iddstoklokasi"]
                
                conn2.commit()
                curs.close()
                
                dic={}
                dic["error"]='false'
                dic["msg"]=""
                dic["data"]={}
                dic["data"]["rows"]=[]
                
                if 1:
                
                    for single in ambilBanyakRowSQL(query):
                        data1={}
                        theCol=len(single)
                        
                        for single2 in range(theCol):
                            strData1='%s'%single[single2]
                            strData1=strData1.replace("\"","")
                            strData1=strData1.replace("\'","")
                            if '%s'%strData1=="None":data1[listSel[single2]]=""
                            else:data1[listSel[single2]]=strData1
                        
                        dic["data"]["rows"].append(data1)
                    dic["data"]["total"]=len(dic["data"]["rows"])
                
                strDic="%s"%dic
                #print strDic
                
            #    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace('"false"',"false").replace("'false'","false").replace("L,"," ,")
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
            #    print strDic
                return Response(strDic, mimetype='application/json')
            if request.method == 'PUT':
            
                namaTabel="dsalesorder"
                
                noso= request.args.get('noso')
                id1= request.args.get('jumlahbarang')
                iddstoklokasi= request.args.get('iddstoklokasi')
                id2= request.args.get('kodebarang')
                
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                jmlTot=int(id1)
                
                query="update dstoklokasi set jumlahbarang=jumlahbarang-%s where iddstoklokasi='%s'"%(jmlTot,iddstoklokasi)
                #print query
                curs.execute(query)
                
                query="update dsalesorder set jumlahbarang='%s',stat4=now(),jml1='%s' where noso='%s' and kodebarang='%s'"%(id1,id1,noso,id2)
                curs.execute(query)

                conn2.commit()
                curs.close()
                    
                data1={}
                
                dic={}
                dic["error"]='false'
                dic["msg"]="Data Terupdate Nomor So %s Kode Barang %s Dengan Jumlah Barang %s"%(noso,id2,id1)
                dic["data"]=data1
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                
                return Response(strDic, mimetype='application/json')
            if request.method == 'DELETE': 
            
                noso= request.args.get('noso')
                id1= request.args.get('kodebarang')
                iddstoklokasi= request.args.get('iddstoklokasi')
                jml= request.args.get('jumlahbarang')
                karton= request.args.get('karton')
                
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                jmlTot=int(jml)
                
                print jmlTot
                print iddstoklokasi
                
                if karton==1:
                    query="select jmlkarton from barangdet where kodebrg='%s'"%kodebarang
                    jumlahkarton=int(ambilSatuRowSQL(query)[0])
                    jmlTot=jmlTot/jumlahkarton
                    query="update dstoklokasi set jumlahbarang=jumlahbarang+%s where iddstoklokasi='%s'"%(jmlTot,iddstoklokasi)
                    curs.execute(query) 
                else:
                    query="update dstoklokasi set jumlahbarang=jumlahbarang+%s where iddstoklokasi='%s'"%(jmlTot,iddstoklokasi)
                    curs.execute(query)
                
                #query="update dstoklokasi set jumlahbarang=jumlahbarang+%s where iddstoklokasi='%s'"%(jmlTot,iddstoklokasi)
                #print query
                #curs.execute(query)
                
                query="delete from dsalesorder where noso='%s' and kodebarang='%s'"%(noso,id1)
                curs.execute(query)
                ket="Barang : %s Nomor So : %s Telah Di Hapus"%(id1,noso)
                #query="insert into rekamjejak (tanggal,kegiatan,operator,keterangan) values (now(),'Hapus','%s','%s')"%(operator,ket)
                #curs.execute(query)
                conn2.commit()
                curs.close()
                
                dic={}
                dic["error"]='false'
                dic["msg"]="Barang %s Nomor So %s terhapus"%(id1,noso)
                dic["data"]=ket
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json') 
if 1:# INBOUND
        @app.route("%s/getSupplierAutoComFromNota"%folderAPI, methods=["GET"])
        #@jwt_required
        def getSupplierAutoComFromNota():
            
            if 1:
                #id1 = get_jwt_identity()
                #print id1
                
                theLimit= request.args.get('itemsPerPage')
                if '%s'%theLimit=="None":theLimit=100
                try:theLimit=int(theLimit)
                except:theLimit=100
                
                strLimit="limit %s"%theLimit
                
                numPage= request.args.get('numberPage')
                if '%s'%numPage=="None":numPage=1
                try:numPage=int(numPage)
                except:numPage=1
                numPage=numPage-1
                strPage="offset %s"%(numPage*theLimit)
                
                kodebrg= request.args.get('kodebrg')
                
                query="select kodebrg,jmlkarton,lokasikrtn,(select ket1 from notapodetailreceive where kodebarang=kodebrg limit 1) from barangdet where kodebrgkarton='%s' limit 1"%(kodebrg)
                try:
                    dapat=ambilSatuRowSQL(query)
                    dapat[0]
                    #dapat[3]
                except:
                    query="select kodebrg,jmlpack,lokasi from barangdet where kodebrgpack='%s'  limit 1"%(kodebrg)
                    try:
                        dapat=ambilSatuRowSQL(query)
                        dapat[0]
                        #dapat[3]
                    except:
                        query="select kodebrg,jumlahbrg,lokasi from barangdet where kodebrg='%s' limit 1"%(kodebrg)
                        try:
                            dapat=ambilSatuRowSQL(query)
                            dapat[0]
                            #dapat[3]
                        except:
                            query="select kodebrg from barang where barcode='%s' or kodebrg='%s' limit 1"%(kodebrg,kodebrg)
                            try:
                                dapat=ambilSatuRowSQL(query)
                                dapat[0]
                                #dapat[3]
                                query="select kodebarang,idpodet,namalengkap,ket1,(jumlahbarang-ket2)sisa from notapodetailreceive where kodebarang='%s' and ket2<jumlahbarang limit 1"%(dapat[0])
                                #print query
                                try:
                                    dapat=ambilSatuRowSQL(query)
                                    dapat[0]
                                    #dapat[3]
            #                    except:

                                except:
                                    dic={}
                                    dic["error"]='true'
                                    dic["msg"]="Kode Barang Tidak Ada"
                                    dic["data"]={}
                                    dic["data"]["rows"]=[]
                                    strDic="%s"%dic
                                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                                    return Response(strDic, mimetype='application/json')
                            except:
                                print query
                                dic={}
                                dic["error"]='true'
                                dic["msg"]="Kode Barang Tidak Ada"
                                dic["data"]={}
                                dic["data"]["rows"]=[]
                                strDic="%s"%dic
                                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                                return Response(strDic, mimetype='application/json')
                
                queryBrg="select kodebarang,namalengkap,idpodet,ket1,(jumlahbarang-ket2)sisa,(select jmlkarton from barangdet where kodebrg=kodebarang limit 1),supplier from notapodetailreceive where kodebarang='%s' and ket2<jumlahbarang"%(dapat[0])
                #queryBrg="select sum(jumlahbarang) from notapodetailreceive where ket1='%s' and kodebarang='%s' and ket2<jumlahbarang group by kodebarang"%(dapat[3],dapat[0])
                print queryBrg
                
                infoSat=ambilSatuRowSQL(queryBrg)
                
                dic={}
                dic["error"]='false'
                dic["msg"]=""
                dic["data"]={}
                dic["data"]["rows"]=[]
                
                if 1:
                    data1={}
                    c=0
                    for single2 in ["kodebarang","namalengkap","idpodet","ket1","sisa","jmlkarton","supplier"]:
                        try:data1[single2]=infoSat[c]
                        except:data1[single2]=""
                        c+=1
                            
                    dic["data"]["rows"].append(data1)
                    dic["data"]["total"]=len(dic["data"]["rows"])
                    
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json')
        @app.route('%s/getListDstoklokasi'%(folderAPI), methods=['GET', 'PUT'])
        def getListDstoklokasi():
            namaTabel="dstoklokasi"
            if request.method == 'GET':
                
                id1= request.args.get('kodebarang')
                
                strWhere="where kodebarang='%s' and jumlahbarang>0 "%id1
                
                query="select * from %s %s"%(namaTabel,strWhere)
                
                conn2=mysql.get_db()
                theCon2=conn2.cursor()
                theCon2.execute(query)
                if theCon2.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Barang Terdaftar Di Dstoklokasi"
                    theCon2.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
                    
                theCon2.close()
                query="""select kodebarang,kodebarangkarton,lokasi,jumlahbarang from %s"""%(namaTabel)
                dataCol=["kodebarang","kodebarangkarton","lokasi","jumlahbarang"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
        @app.route('%s/getDataBarangDatang'%(folderAPI), methods=['GET', 'POST', 'PUT','DELETE'])
        def getDataBarangDatang():
            namaTabel="notapodetailreceive"
            namaTebel2="dstoklokasi"
            if request.method == 'GET':
                
                id1= request.args.get('idpodet')
                
             
                strWhere="where idpodet='%s'"%id1
                
                query="select * from %s %s"%(namaTabel,strWhere)
                
                conn2=mysql.get_db()
                theCon2=conn2.cursor()
                theCon2.execute(query)
                if theCon2.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Tidak Ada Barang Datang"
                    theCon2.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
                    
                theCon2.close()
                query="""select namalengkap,jumlahbarang,ket1,supplier,ket2,kodebarang,satuan,(select jmlkarton from barangdet where kodebrg=kodebarang)jmlkarton,(jumlahbarang-ket2) from %s"""%(namaTabel)
                dataCol=["namalengkap","jumlahbarang","ket1","supplier","ket2","kodebarang","satuan","jmlkarton","sisa"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
                #return bikinGetJSONExt(namaTabel,strWhere)
                
            if request.method == 'POST':     
                
                lok= request.args.get('nopalet')
                
              
                 
                strWhere=""
                                    
                conn=mysql.get_db()
                theCon=conn.cursor()
                
             
                dapat= request.get_json()
                print dapat
                isiSO=eval('%s'%dapat)
                
                for single in isiSO:
                    kb=single['kb']
                    kbr=single['kbr']
                    us=single['us']
                    jml=single['jml']
                    jmlkarton=single['jmlkarton']
                    st=single['st']
                    id=single['id']
                    sj=single['sj']
                    supplier=single['supplier']
                    #query="update %s set nom1=nom1+%s where kodebarang='%s' and nomorpo='%s'"%(namaTabel,jb,kb,id1)
                    #print query
                    #theCon.execute(query)
                    print jmlkarton
                    
                    query="insert into dstoklokasi(kodebarang,kodebarangkarton,lokasi,operator,tglmasuk,jumlahbarang,satuan,stokawal,sumber,referensi,suratJalan,kodesup) values ('%s','%s','%s','%s',now(),'%s','%s','%s','Inbound Surat Jalan','%s','%s','%s')"%(
                        kb,kbr,lok,us,jml,st,jml,id,sj,supplier)
                    theCon.execute(query)
                    print query
                   
                
                conn.commit()
                theCon.close()
                
                return bikinGetJSONExt(namaTebel2,strWhere)
            
            if request.method == 'PUT':
                jumlahbarang= request.args.get('jmltotal')
                idpodet= request.args.get('idpodet')
             
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                query="update notapodetailreceive set ket2=ket2+'%s' where idpodet='%s'"%(jumlahbarang,idpodet)
                curs.execute(query)
                
                conn2.commit()
                curs.close()
                
                data1={}
                dic={}
                dic["error"]='false'
                dic["msg"]="SJ Update"
                dic["data"]=data1
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json')    
            if request.method == 'DELETE':
                idpodet= request.args.get('idpodet')
                jumlahbarang= request.args.get('jmltotal')
             
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                query="update notapodetailreceive set ket2=ket2-'%s' where idpodet='%s'"%(jumlahbarang,idpodet)
                curs.execute(query)
                
                conn2.commit()
                curs.close()
                
                data1={}
                dic={}
                dic["error"]='false'
                dic["msg"]="ket2 Nota PO Delete"
                dic["data"]=data1
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json') 
        @app.route('%s/listSuratJalan'%(folderAPI), methods=['GET','DELETE'])
        def listSuratJalan():
            namaTabel="notapodetailreceive"
            if request.method == 'GET':
                
                id1= request.args.get('supp')
                
                
                print id1
                if '%s'%id1=="":strWhere="where ket2<jumlahbarang group by ket1"
                else:strWhere="where ket2<jumlahbarang and ket1='%s'"%id1
             
                print strWhere
            
                #strWhere="where ket1='%s' "%id1
                #strWhere="where ket2<jumlahbarang"
                #strWhere=""
                
                query="select * from %s %s"%(namaTabel,strWhere)
                
                conn2=mysql.get_db()
                theCon2=conn2.cursor()
                theCon2.execute(query)
                if theCon2.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Tidak Ada Barang Datang"
                    theCon2.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
                    
                theCon2.close()
                query="""select idpodet,(select namarel from relasi where koderel=supplier limit 1) namarel,ket1,namalengkap,jumlahbarang,ket1,supplier,ket2
                ,kodebarang,satuan,(select jmlkarton from barangdet where kodebrg=kodebarang limit 1)jmlkarton,(jumlahbarang-ket2) from %s"""%(namaTabel)
                dataCol=["idpodet","namasupp","srtjalan","namalengkap","jumlahbarang","ket1","supplier","ket2","kodebarang","satuan","jmlkarton","sisa"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
            
            if request.method == 'DELETE':
                
                sj= request.args.get('sj')
                supp= request.args.get('supp')
                
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                query="delete from notapodetailreceive where ket1='%s' and supplier='%s'"%(sj,supp)
                curs.execute(query)
                ket="Surat Jalan Terhapus"
                conn2.commit()
                curs.close()
                
                dic={}
                dic["error"]='false'
                dic["msg"]="Surat Jalan Terhapus"
                dic["data"]=ket
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json') 
        @app.route('%s/listAllSuratJalan'%(folderAPI), methods=['GET'])
        def listAllSuratJalan():
            namaTabel="notapodetailreceive"
            if request.method == 'GET':
                
                id1= request.args.get('ket1')
                
             
                strWhere="where ket1='%s'"%(id1)
             
                print strWhere
            
                #strWhere="where ket1='%s' "%id1
                #strWhere="where ket2<jumlahbarang"
                #strWhere=""
                
                query="select * from %s %s"%(namaTabel,strWhere)
                
                conn2=mysql.get_db()
                theCon2=conn2.cursor()
                theCon2.execute(query)
                if theCon2.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Tidak Ada Barang Datang"
                    theCon2.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
                    
                theCon2.close()
                query="""select idpodet,(select namarel from relasi where koderel=supplier limit 1),ket1,namalengkap,jumlahbarang,ket1,supplier,ket2,kodebarang,satuan,(select jmlkarton from barangdet where kodebrg=kodebarang limit 1)jmlkarton,(jumlahbarang-ket2) from %s"""%(namaTabel)
                dataCol=["idpodet","namasupp","srtjalan","namalengkap","jumlahbarang","ket1","supplier","ket2","kodebarang","satuan","jmlkarton","sisa"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
            
        @app.route('%s/listSuratJalanByDate'%(folderAPI), methods=['GET', 'PUT'])
        def listSuratJalanByDate():
            namaTabel="notapodetailreceive"
            if request.method == 'GET':
                
                id1= request.args.get('tgl1')
                id2= request.args.get('tgl2')
                
                strWhere="where tglbeli between '%s' and '%s' group by ket1"%(id1,id2)
             
                #print strWhere
            
                #strWhere="where ket1='%s' "%id1
                #strWhere="where ket2<jumlahbarang"
                #strWhere=""
                
                query="select * from %s %s"%(namaTabel,strWhere)
                
                print query
                
                conn2=mysql.get_db()
                theCon2=conn2.cursor()
                theCon2.execute(query)
                if theCon2.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Tidak Ada Barang Datang"
                    theCon2.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
                    
                theCon2.close()
                query="""select supplier,(select trim(namarel) from relasi where koderel=supplier),ket1,(ket2<jumlahbarang),sum(jumlahbarang),sum(ket2),if(sum(ket2)<>sum(jumlahbarang),1,0) from %s"""%(namaTabel)
                dataCol=["supplier","namasupp","srtjalan","full","t1","t2","cekfull"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
        
        @app.route('%s/getFull'%(folderAPI), methods=['GET'])
        def getFull():
            namaTabel="notapodetailreceive"
            if request.method == 'GET':
                
                id1= request.args.get('tgl1')
                id2= request.args.get('tgl2')
                
                strWhere="where tglbeli between '%s' and '%s' order by ket1"%(id1,id2)
                
                query="select * from %s %s"%(namaTabel,strWhere)
                
                print query
                
                conn2=mysql.get_db()
                theCon2=conn2.cursor()
                theCon2.execute(query)
                if theCon2.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Tidak Ada Barang Datang"
                    theCon2.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
                    
                theCon2.close()
                query="""select supplier,(select namarel from relasi where koderel=supplier),ket1,(ket2<jumlahbarang) from %s"""%(namaTabel)
                dataCol=["supplier","namasupp","srtjalan","full"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
     
        @app.route('%s/getPOrange'%(folderAPI), methods=['GET'])
        def getPOrange():
            namaTabel="notapo"
            if request.method == 'GET':
                
                id1= request.args.get('tglStart')
                id2= request.args.get('tglStop')
                id3= request.args.get('supplier')
                
                strWhere="where tglbeli between '%s' and '%s 23:59' and supplier like '%s%s%s' "%(id1,id2,"%",id3,"%")
                                    
                query="select * from %s %s"%(namaTabel,strWhere)
                print query
                conn2=mysql.get_db()
                theCon2=conn2.cursor()
                try:theCon2.execute(query)
                except:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Nomor PO Tidak ada "
                    theCon.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
                    
                if theCon2.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Nomor PO Tidak ada "
                    theCon.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
                
                
                theCon2.close()
                
                query="""select nomorpo,(select namarel from relasi where supplier=koderel limit 1),
                (select count(kodebarang) from notapodetail where notapodetail.nomorpo=notapo.nomorpo),
                (select count(distinct(kodebarang)) from notapodetailreceive where notapodetailreceive.nomorpo=notapo.nomorpo) supplier from %s """%(namaTabel)
                dataCol=["nomorpo","supplier","jmldatang","jmlorder"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
            
        @app.route('%s/getPO'%(folderAPI), methods=['GET'])
        def getPO():
            namaTabel="notapo"
            if request.method == 'GET':
                
                id1= request.args.get('nopo')
                
                strWhere="where nomorpo='%s' "%id1
                                    
                query="select * from %s %s"%(namaTabel,strWhere)
                
                conn2=mysql.get_db()
                theCon2=conn2.cursor()
                theCon2.execute(query)
                if theCon2.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Nomor PO  Tidak ada "
                    theCon.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
                    
                theCon2.close()
                
                return bikinGetJSONExt(namaTabel,strWhere)
        @app.route('%s/getPODet'%(folderAPI), methods=['GET'])
        def getPODet():
            namaTabel="notapodetail"
            if request.method == 'GET':
                
                id1= request.args.get('nopo')
                id2= request.args.get('kodebrg')
                
                #strWhere="where nomorpo='%s' "%id1
                strWhere="where nomorpo='%s' and kodebarang='%s'"%(id1,id2)
                                    
                query="select * from %s %s"%(namaTabel,strWhere)
                conn2=mysql.get_db()
                theCon2=conn2.cursor()
                theCon2.execute(query)
                if theCon2.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Nomor PO  Tidak ada "
                    theCon.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
                    
                theCon2.close()
                
                return bikinGetJSONExt(namaTabel,strWhere)
        @app.route('%s/getCountPoDet'%(folderAPI), methods=['GET'])
        def getCountPoDet():
            namaTabel="notapodetail"
            if request.method == 'GET':
                
                id1= request.args.get('nopo')
                
                #strWhere="where nomorpo='%s' "%id1
                strWhere="where nomorpo='%s'"%id1
                                    
                query="select * from %s %s"%(namaTabel,strWhere)
                conn2=mysql.get_db()
                theCon2=conn2.cursor()
                theCon2.execute(query)
                if theCon2.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Nomor PO  Tidak ada "
                    theCon.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
                    
                theCon2.close()
                
                query="select count(kodebarang),(select count(distinct(kodebarang)) from notapodetailreceive %s) from %s "%(strWhere,namaTabel)
                dataCol=["jmlorder","jmldatang"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
        @app.route('%s/receivePODet'%(folderAPI), methods=['GET','POST','PUT','DELETE']) # UPDATE YOEL
        def receivePODet():
            namaTabel="notapodetail"
            namaTabel2="notapodetailreceive"
            
            if request.method == 'GET':
                id1= request.args.get('nopo')
                id2= request.args.get('kodebrg')
                strWhere="where nomorpo='%s' and kodebarang='%s' group by kodebarang"%(id1,id2)
                query="select kodebarang,sum(jumlahbarang) jumlahbarang from %s "%(namaTabel2)
                
                #strWhere="where nomorpo='%s' group by kodebarang"%id1
                #query="select kodebarang,sum(jumlahbarang) from %s "%(namaTabel2)
                dataCol=["kodebarang","jumlahbarang"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
                
            if request.method == 'POST':
                
                
                if 0:
                    #id1= request.args.get('nopo')
                    nosj= request.args.get('nosj')
                    nom1= request.args.get('nom1')
    #                kb= request.args.get('kodebarang')
    #                jb= request.args.get('jumlahbarang')
                    
                    strWhere="where ket1='%s' "%nosj
                                        
                    query="select * from %s %s"%(namaTabel,strWhere)
                    
                    conn2=mysql.get_db()
                    theCon=conn2.cursor()
                    theCon.execute(query)
                    if theCon.rowcount==0:
                        data1={}
                        dic={}
                        dic["error"]='true'
                        dic["msg"]="Nomor PO  Tidak ada "
                        theCon.close()
                        strDic="%s"%dic
                        strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                        return Response(strDic, mimetype='application/json')
                    
                    dapat= request.get_json()
                    print dapat
                    isiSO=eval('%s'%dapat)
                    
                    for single in isiSO:
                        kb=single['kb']
                        jb=single['jb']
                        hb=single['hb']
                        sup=single['sup']
                        #query="update %s set nom1=nom1+%s where kodebarang='%s' and nomorpo='%s'"%(namaTabel,jb,kb,id1)
                        #print query
                        #theCon.execute(query)
                        
                        #query="insert into %s (jumlahbarang,kodebarang,nomorpo,tglbeli,hargabeli,supplier,ket1) values ('%s','%s','%s',now(),'%s','%s','%s')"%(
                        #    namaTabel2,jb,kb,id1,hb,sup,nosj)
                        #print query
                        #theCon.execute(query)
                        query="insert into %s (jumlahbarang,kodebarang,tglbeli,hargabeli,supplier,ket1,nom1) values ('%s','%s',now(),'%s','%s','%s','%s')"%(
                        namaTabel2,jb,kb,hb,sup,nosj,nom1)
                        #print query
                        theCon.execute(query)
                    
                    conn2.commit()
                    
                    theCon.close()
                    
                    return bikinGetJSONExt(namaTabel,strWhere)
                
                #id1= request.args.get('nopo')
                nosj= request.args.get('nosj')
#                kb= request.args.get('kodebarang')
#                jb= request.args.get('jumlahbarang')
                
                strWhere="where ket1='%s' "%nosj
                                    
                query="select * from %s %s"%(namaTabel,strWhere)
                
                conn2=mysql.get_db()
                theCon=conn2.cursor()
                theCon.execute(query)
                if theCon.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='false'
                    dic["msg"]="Surat Jalan Baru "
                    #theCon.close()
                    #strDic="%s"%dic
                    #strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    #return Response(strDic, mimetype='application/json')
                
                if theCon.rowcount!=0:
                    data1={}
                    dic={}
                    dic["error"]='false'
                    dic["msg"]="Surat Jalan Lama "
                    #theCon.close()
                    #strDic="%s"%dic
                    #strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    #return Response(strDic, mimetype='application/json')
                    
                dapat= request.get_json()
                print dapat
                isiSO=eval('%s'%dapat)
                
                for single in isiSO:
                    kb=single['kb']
                    jb=single['jb']
                    hb=single['hb']
                    sup=single['sup']
                    nb=single['nb']
                    st=single['st']
                    #query="update %s set nom1=nom1+%s where kodebarang='%s' and nomorpo='%s'"%(namaTabel,jb,kb,id1)
                    #print query
                    #theCon.execute(query)
                    
                    query="insert into %s (jumlahbarang,kodebarang,tglbeli,hargabeli,supplier,ket1,satuan,namalengkap,ket2) values ('%s','%s',now(),'%s','%s','%s','%s','%s',0)"%(
                        namaTabel2,jb,kb,hb,sup,nosj,st,nb)
                    #print query
                    theCon.execute(query)
                
                conn2.commit()
                
                theCon.close()
                
                return bikinGetJSONExt(namaTabel,strWhere)
            
            if request.method == 'PUT':
                namaTabel="notapodetailreceive"
                
                id1= request.args.get('idpodet')
                total= request.args.get('total')
                nama= request.args.get('nama')
                kode= request.args.get('kode')
                satuan= request.args.get('satuan')
   
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                query="update notapodetailreceive set tglbeli=now(),jumlahbarang='%s',satuan='%s',kodebarang='%s',namalengkap='%s' where idpodet='%s'"%(total,satuan,kode,nama,id1)
                curs.execute(query)
                
                conn2.commit()
                curs.close()
                    
                data1={}
                
                dic={}
                dic["error"]='false'
                dic["msg"]="Data Barang Terupdate Di DB Notapodetailreceive"
                dic["data"]=data1
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                
                return Response(strDic, mimetype='application/json')
            
            if request.method == 'DELETE':
                
                id1= request.args.get('idpodet')
                
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                query="delete from notapodetailreceive where idpodet='%s'"%(id1)
                curs.execute(query)
                ket="Item Barang Terhapus"
                conn2.commit()
                curs.close()
                
                dic={}
                dic["error"]='false'
                dic["msg"]="Item Barang Terhapus"
                dic["data"]=ket
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json') 
            
        @app.route('%s/receiveGetList'%(folderAPI), methods=['GET','PUT']) # UPDATE YOEL
        def receiveGetList():
            namaTabel="notapodetailreceive"
            
            if request.method == 'GET':
                id1= request.args.get('nosj')
                id2= request.args.get('supp')
                strWhere="where ket1='%s' and supplier='%s' order by namalengkap"%(id1,id2)
                query="select * from %s"%(namaTabel)
                
                #strWhere="where nomorpo='%s' group by kodebarang"%id1
                #query="select kodebarang,sum(jumlahbarang) from %s "%(namaTabel2)
                #dataCol=["kodebarang","jumlahbarang"]
                return bikinGetJSONExt(namaTabel,strWhere)
            
            if request.method == 'PUT':
                namaTabel="barangdet"
                
                id1= request.args.get('kodebar')
                jumlahkarton= request.args.get('jumlahkarton')
   
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                jmlTot=int(jumlahkarton)
                
                query="update barangdet set jmlkarton=%s where kodebrg='%s'"%(jmlTot,id1)
                curs.execute(query)
                
                conn2.commit()
                curs.close()
                    
                data1={}
                
                dic={}
                dic["error"]='false'
                dic["msg"]="Data Jumlah Karton Terupdate"
                dic["data"]=data1
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                
                return Response(strDic, mimetype='application/json')
                
        @app.route('%s/listReceivePODet'%(folderAPI), methods=['GET','PUT'])
        def listReceivePODet():
            namaTabel="notapodetail"
            namaTabel2="notapodetailreceive"
            
            if request.method == 'GET':
                
                id1= request.args.get('nopo')
                
                #strWhere="where nomorpo='%s' "%id1
                strWhere=""#where nomorpo='%s'"%id1
                                    
                query="select * from %s %s"%(namaTabel2,strWhere)
                conn2=mysql.get_db()
                theCon2=conn2.cursor()
                theCon2.execute(query)
                if theCon2.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Nomor PO  Tidak ada "
                    theCon.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
                    
                theCon2.close()
                
                query="select jumlahbarang,kodebarang,(select jumlahbarang from notapodetail where nomorpo='%s' and notapodetail.kodebarang=notapodetailreceive.kodebarang limit 1),(select namabrg from barang where notapodetailreceive.kodebarang=barang.kodebrg) from notapodetailreceive  where nomorpo='%s'"%(id1,id1)
                
                dataCol=["jmldatang","kodebarang","jmlorder","namabrg"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
            
            if request.method == 'PUT':
                
                id1= request.args.get('kodebar')
                idbarang= request.args.get('idbarang')
   
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                query="update barangdet set kodebrgkarton='%s' where kodebrg='%s'"%(idbarang,id1)
                curs.execute(query)
                
                conn2.commit()
                curs.close()
                    
                data1={}
                
                dic={}
                dic["error"]='false'
                dic["msg"]="Data Kode Barang Karton Terupdate"
                dic["data"]=data1
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                
                return Response(strDic, mimetype='application/json')
                
        @app.route('%s/isiStokPalet'%(folderAPI), methods=['GET', 'PUT', 'POST'])
        def isiStokPalet():
            namaTabel="dstoklokasi"
            
            if request.method == 'POST':      
                
                id1= request.args.get('lokasi')
                kodebrg= request.args.get('kodebrg')
                kodebrgkarton= request.args.get('kodebrg')
                namalogin= request.args.get('namalogin')
                jumlahbarang= request.args.get('jumlahbarang')
                jumlahkarton= request.args.get('jumlahkarton')
                idpodet= ""#request.args.get('idpodet')
                
                satuan= '%s'%request.args.get('satuan')
                if satuan=='None':satuan="karton"
                
                lokasi=id1
                query="select kodebrg from barangdet where (kodebrgkarton='%s' or kodebrgpack='%s' or kodebrg='%s' or kodebrgkarton='%s' or kodebrgpack='%s' or kodebrg='%s')"%(kodebrg,kodebrg,kodebrg,kodebrgkarton,kodebrgkarton,kodebrgkarton)
                try:kodebrgSat=ambilSatuRowSQL(query)[0]
                except:
                    query="select kodebrg from barang where (trim(barcode)=trim('%s') or trim(barcode)=trim('%s'))"%(kodebrg,kodebrgkarton)
                    try:kodebrgSat=ambilSatuRowSQL(query)[0]
                    except:kodebrgSat=kodebrg
                
                print query
                
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                query="select * from dstoklokasi where (kodebarangkarton='%s' or kodebarang='%s') and jumlahbarang>0 and lokasi='%s'"%(kodebrg,kodebrg,lokasi)
                curs.execute(query)
                if curs.rowcount>0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Kode Barang di lokasi termasuk masih ada!"
                    dic["data"]=data1
                    
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                    return Response(strDic, mimetype='application/json') 
                    
                query="insert into dstoklokasi(kodebarang,kodebarangkarton,lokasi,operator,tglmasuk,jumlahbarang,satuan,stokawal,sumber,referensi) values ('%s','%s','%s','%s',now(),'%s','%s','%s','Check In PO','%s')"%(kodebrgSat,kodebrgkarton,lokasi,namalogin,jumlahkarton,satuan,jumlahkarton,idpodet)
                curs.execute(query)
                
                query="select idpodet, (jumlahbarang-if(nom1 is null,0,nom1)) from notapodetailreceive where  kodebarang='%s' and jumlahbarang>0 order by idpodet"%kodebrgSat
                #print query
                
                dataBrgPO={}
                for single in ambilBanyakRowSQL(query):
                    dataBrgPO[single[0]]=[single[1]]
                
                try:jmlTot=int(jumlahbarang)
                except:jmlTot=0
                
                for single in dataBrgPO:
                    jmlRun=dataBrgPO[single][0]
                    lagi=0
                    if jmlRun>=jmlTot:
                        jmlRun=jmlTot
                        lagi=1
                    else:
                        jmlTot=jmlTot-jmlRun
                        
                    idpodet=single
                    query="update notapodetailreceive set nom1=if(nom1 is null,0,nom1)+%s where idpodet='%s'"%(jmlRun,idpodet)
                    print query
                    
                    curs.execute(query)
                    if lagi:break
                
                ket="Check In PO : %s Oleh : %s Lokasi : %s Jumlah : %s"%(kodebrg,namalogin,lokasi,jumlahbarang)
                query="insert into rekamjejak (tanggal,kegiatan,operator,keterangan) values (now(),'Check In PO','%s','%s')"%(namalogin,ket)
                curs.execute(query)
                
#                query="update temprefill set status='selesai_refill' where kodebrg='%s' and namaoperator='%s' and status='selesai_karton'"%(kodebrg,namalogin)
#                print query
                
#                curs.execute(query)
                conn2.commit()
                curs.close()
                
                data1={}
                data1['lokasi']=lokasi
                data1['kodebrg']=kodebrg
                data1['namalogin']=namalogin
                data1['status']="ISI Stok Lokasi"
                
                dic={}
                dic["error"]='false'
                dic["msg"]="%s %s terisi ke %s oleh %s !"%(satuan,kodebrg,lokasi,namalogin)
                dic["data"]=data1
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json')         
        @app.route('%s/deleteStokPalet'%(folderAPI), methods=['DELETE'])
        def deleteStokPalet():
            namaTabel="dstoklokasi"
            
            if request.method == 'DELETE': 
            
                lokasi= request.args.get('lokasi')
                kodebarang= request.args.get('kodebrg')
                operator= request.args.get('namalogin')
                
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                query="delete from dstoklokasi where (kodebarang='%s' or kodebarangkarton='%s') and lokasi='%s' and jumlahbarang>0"%(kodebarang,kodebarang,lokasi)
                curs.execute(query)
                ket="Hapus Barang : %s Oleh : %s Lokasi : %s"%(kodebarang,operator,lokasi)
                query="insert into rekamjejak (tanggal,kegiatan,operator,keterangan) values (now(),'Hapus','%s','%s')"%(operator,ket)
                curs.execute(query)
                conn2.commit()
                curs.close()
                
                dic={}
                dic["error"]='false'
                dic["msg"]="Stok %s lokasi %s terhapus"%(kodebarang,lokasi)
                dic["data"]=ket
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json') 
            
if 1:# DELIVERY
        @app.route('%s/getNoDelivery'%(folderAPI), methods=['GET' , 'PUT'])
        def getNoDelivery():
            namaTabel2="hdel"
            
            if request.method == 'GET':
          
        
                date1= request.args.get('date1')
                date2= request.args.get('date2')
                if date1=='None':date1=""
                if date2=='None':date2=""
                
                strWhere="where stat1=''"#where nomorpo='%s'"%id1
                if(date1!="" and date2!=""): 
                    strWhere="where stat1='' and tanggalterbit between '%s 00:00:00' and '%s 23:59:59'"%(date1,date2)
                                    
                query="select * from %s %s"%(namaTabel2,strWhere)
                conn2=mysql.get_db()
                theCon2=conn2.cursor()
                theCon2.execute(query)
                if theCon2.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Nomor Delivery Tidak Ada "
                    theCon2.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
                    
                theCon2.close()
                
                query="select idhdel,nodelivery, jmlCus, jmlKoli, jmlInv from hdel"
                
                dataCol=["idhdel","nodeliv","jmlcus","jmlkoli","jmlinv"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
            
            if request.method == 'PUT':
             
                id1 = request.args.get('nodel')
                kodtruk= request.args.get('kodtruk')
                driver= request.args.get('driver')
                asisten= request.args.get('asisten')
                area= request.args.get('area')
                operator= request.args.get('operator')
                
                #strWhere="where nomorpo='%s' "%id1
                strWhere="where noDelivery='%s'"%(id1)
                
                                      
                query="update hdel set sopir='%s',operator='%s',stat2='%s',stat3='%s',stat4='%s' where nodelivery='%s'"%(driver,operator,asisten,area,kodtruk,id1)
                conn2=mysql.get_db()
                theCon2=conn2.cursor()  
                theCon2.execute(query)
                
                conn2.commit()
                theCon2.close()
                
                data1={}
                
                dic={}
                dic["error"]='false'
                dic["msg"]="Data Pengiriman Update"
                dic["data"]=data1
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                
                return Response(strDic, mimetype='application/json')
        @app.route('%s/getNosoDeliv'%(folderAPI), methods=['GET' ,'PUT'])
        def getNosoDeliv():
            namaTabel2="ddel"
            
            if request.method == 'GET':
             
                id1= request.args.get('nodel')
                #strWhere="where nomorpo='%s' "%id1
                strWhere="where noDelivery='%s'"%id1
                                    
                query="select * from %s %s"%(namaTabel2,strWhere)
                conn2=mysql.get_db()
                theCon2=conn2.cursor()
                theCon2.execute(query)
                if theCon2.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Nomor Delivery Tidak Ada "
                    theCon2.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
                    
                theCon2.close()
                
                query="select idddel,nodelivery,noso, namacus, jmlKoli, area, sales, stat2 from %s"%(namaTabel2)
                
                dataCol=["idddel","nodelivery","noso","namacus","jmlKoli","area","sales","kolimasuk"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
            
            if request.method == 'PUT':
             
                nodel= request.args.get('nodel')
                noso= request.args.get('noso')
                kol= request.args.get('kol')
                #strWhere="where nomorpo='%s' "%id1
                strWhere="where noDelivery='%s' and noso='%s'"%(nodel,noso)
                                    
                query="select * from %s %s"%(namaTabel2,strWhere)
                conn2=mysql.get_db()
                theCon2=conn2.cursor()
                theCon2.execute(query)
                if theCon2.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Nomor SO Tidak Ada Dalam Daftar Delivery"
                    theCon2.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json') 
                
                query="select * from rdsalesorder where noso='%s' and stat1='%s'"%(noso,kol)
                theCon2.execute(query)
                if theCon2.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="KOLI Tidak Ada"
                    theCon2.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')   
                    
                query="select deliv from rdsalesorder where noso='%s' and deliv='%s'"%(noso,kol)
                theCon2.execute(query)
                if theCon2.rowcount>0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="KOLI Sudah Terscan"
                    theCon2.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')    
                
                query="select * from rdsalesorder where noso='%s' and stat1='%s' and deliv!=1"%(noso,kol)
                theCon2.execute(query)
                if theCon2.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Nomor SO Sudah Terscan"
                    theCon2.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')   
                
                
                query="update ddel set stat2=stat2+1 where nodelivery='%s' and noso='%s'"%(nodel,noso)
                theCon2.execute(query)
                
                query="update rdsalesorder set deliv='%s' where noso='%s' and stat1='%s'"%(kol,noso,kol)
                theCon2.execute(query)
                
                conn2.commit()
                theCon2.close()
                
                data1={}
                
                dic={}
                dic["error"]='false'
                dic["msg"]="Data Delivery Terupdate"
                dic["data"]=data1
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                
                return Response(strDic, mimetype='application/json')
              
        @app.route('%s/getSelesaiScanDelivery'%(folderAPI), methods=['GET'])
        def getSelesaiScanDelivery():
            namaTabel2="ddel"
            
            if request.method == 'GET':
             
                id1= request.args.get('nodel')
                #strWhere="where nomorpo='%s' "%id1
                strWhere="where noDelivery='%s' order by namacus"%id1
                                    
                query="select * from %s %s"%(namaTabel2,strWhere)
                conn2=mysql.get_db()
                theCon2=conn2.cursor()
                theCon2.execute(query)
                if theCon2.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Belum Ada SO Di Cek"
                    theCon2.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
                    
                theCon2.close()
                
                query="select idddel,nodelivery,noso, namacus, jmlKoli, area, sales, stat2 from %s"%(namaTabel2)
                
                dataCol=["idddel","nodelivery","noso","namacus","jmlKoli","area","sales","kolimasuk"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
        
        @app.route('%s/getFullItemDelivery'%(folderAPI), methods=['PUT'])
        def getFullItemDelivery():
            namaTabel2="ddel"
            
            if request.method == 'PUT':
             
                id1= request.args.get('nodel')
                #strWhere="where nomorpo='%s' "%id1
                strWhere="where noDelivery='%s' and stat2<>jmlkoli"%id1
                                    
                query="select * from %s %s"%(namaTabel2,strWhere)
                conn2=mysql.get_db()
                theCon2=conn2.cursor()
                theCon2.execute(query)
                if theCon2.rowcount!=0:
                    
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Masih Ada KOLI Belum Di Scan"
                    theCon2.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
                   
                query="update hdel set stat1=1 where nodelivery='%s'"%(id1)
                theCon2.execute(query)
                
                conn2.commit()
                    
                theCon2.close()
                    
                data1={}
                
                dic={}
                dic["error"]='false'
                dic["msg"]="Delivery Selesai"
                dic["data"]=data1
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                
                return Response(strDic, mimetype='application/json')
            
        @app.route('%s/getRdSalesKoliList'%(folderAPI), methods=['GET'])
        def getRdSalesKoliList():
            namaTabel2="rdsalesorder"
            
            if request.method == 'GET':
             
                id1= request.args.get('noso')
                #strWhere="where nomorpo='%s' "%id1
                strWhere="where noso='%s' and stat1<>deliv group by stat1"%id1
                                    
                query="select * from %s %s"%(namaTabel2,strWhere)
                print query
                conn2=mysql.get_db()
                theCon2=conn2.cursor()
                theCon2.execute(query)
                if theCon2.rowcount==0:
                    
                    theCon2.close()
                
                    strWhere="where noso='%s' group by stat1 order by stat1 asc"%id1
                    
                    query="select stat1,deliv from %s"%(namaTabel2)
                    
                    print query
                    
                    dataCol=["stat1","deliv"]
                    return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
                   
                theCon2.close()
                
                strWhere="where noso='%s' group by stat1 order by deliv desc"%id1
                
                query="select stat1,deliv from %s"%(namaTabel2)
                
                print query
                
                dataCol=["stat1","deliv"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
            
        @app.route('%s/pindahDeliv'%(folderAPI), methods=['PUT'])
        def pindahDeliv():
            namaTabel2="ddel"
         
            if request.method == 'PUT':
                
                dapat= request.get_json()
                nodel=dapat['nodel']
                noso=dapat['noso']
                
                #strWhere="where nomorpo='%s' "%id1
                strWhere="where noso='%s'"%(noso)
             
                query="select idddel,nodelivery,noso,namacus,jmlkoli,area,sales,stat1 from %s %s"%(namaTabel2,strWhere)
                dapat=ambilSatuRowSQL(query)
                conn2=mysql.get_db()
                theCon2=conn2.cursor()
                theCon2.execute(query)
                if theCon2.rowcount==0:
                    query="select noso from dsalesorder %s"%(strWhere)
                    theCon2.execute(query)
                    if theCon2.rowcount==0:
                        data1={}
                        dic={}
                        dic["error"]='true'
                        dic["msg"]="Nomor SO Tidak Ditemukan"
                        theCon2.close()
                        strDic="%s"%dic
                        strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                        return Response(strDic, mimetype='application/json') 
                    
                    strWhere="where nojual='%s'"%(noso)
                    query="select kodecus,kodesales,totbrutto,(select namacus from customer where customer.kodecus=hjual.kodecus limit 1),(select namasales from sales where sales.kodesales=hjual.kodesales limit 1),(select kota from customer where customer.kodecus=hjual.kodecus limit 1),(select MAX(CONVERT(rdsalesorder.stat1,UNSIGNED)) from rdsalesorder where rdsalesorder.noso='%s' limit 1) from hjual %s"%(noso,strWhere)
                    dapat=ambilSatuRowSQL(query)
                    print dapat[2] #stat1
                    print dapat[3] #namacus
                    print dapat[4] #namasales
                    print dapat[5] #area
                    print dapat[6] #jml koli
                                
                 
                    #insert ke ddel baru
                    query="insert into ddel (nodelivery,noso,namacus,jmlkoli,area,sales,tgldelivery,stat1) values ('%s','%s','%s','%s','%s','%s',now(),'%s')"%(nodel,noso,dapat[3],dapat[6],dapat[5],dapat[4],dapat[2])
                    theCon2.execute(query)
                    
                    #update hdel baru
                    query="update hdel set jmlkoli=jmlkoli+'%s',jmlinv=jmlinv+1,totnominal=totnominal+'%s',jmlCus=jmlCus+1 where nodelivery='%s'"%(dapat[6],dapat[2],nodel)
                    theCon2.execute(query)
                    
                    conn2.commit()
                    theCon2.close()
                    
                    data1={}
                    
                    dic={}
                    dic["error"]='false'
                    dic["msg"]="Data Delivery Ditambahkan"
                    dic["data"]=data1
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    
                    return Response(strDic, mimetype='application/json')
                    
                query="select idddel,nodelivery,noso,namacus,jmlkoli,area,sales,stat1 from %s where noso='%s' and stat2>0"%(namaTabel2,noso)
                theCon2.execute(query)
                if theCon2.rowcount!=0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Nomor SO Masuk Daftar Pengiriman"
                    theCon2.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json') 
          
                
                print dapat[0]
                print dapat[1]
                print dapat[2]
                print dapat[3]
                print dapat[4]
                print dapat[5]
                print dapat[6]
                print dapat[7]
                                
                #delete ddel lama
                query="delete from ddel where idddel='%s'"%(dapat[0])
                theCon2.execute(query)
                
                #update hdel lama
                query="update hdel set jmlkoli=jmlkoli-'%s',jmlinv=jmlinv-1,totnominal=totnominal-'%s' where nodelivery='%s'"%(dapat[4],dapat[7],dapat[1])
                theCon2.execute(query)
                
                #insert ke ddel baru
                query="insert into ddel (nodelivery,noso,namacus,jmlkoli,area,sales,tgldelivery,stat1) values ('%s','%s','%s','%s','%s','%s',now(),'%s')"%(nodel,noso,dapat[3],dapat[4],dapat[5],dapat[6],dapat[7])
                theCon2.execute(query)
                
                #update hdel baru
                query="update hdel set jmlkoli=jmlkoli+'%s',jmlinv=jmlinv+1,totnominal=totnominal+'%s' where nodelivery='%s'"%(dapat[4],dapat[7],nodel)
                theCon2.execute(query)
                
                conn2.commit()
                theCon2.close()
                
                data1={}
                
                dic={}
                dic["error"]='false'
                dic["msg"]="Data Delivery Terupdate"
                dic["data"]=data1
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                
                return Response(strDic, mimetype='application/json')
                    
                
if 1:# ADMIN
        @app.route('%s/getLvlOpe'%(folderAPI), methods=['GET' , 'PUT', 'DELETE'])
        def getLvlOpe():
            namaTabel2="dashboardmenu"
            
            if request.method == 'GET':
          
                id1= request.args.get('level')
                #strWhere="where nomorpo='%s' "%id1
                strWhere=""
                
                query="select count(kodebarang) from reffilertask where userambil='' and status='refiller'"
                taskrefill=int(ambilSatuRowSQL(query)[0])
                print taskrefill
                query="""select lvloperator,reffiler,inbound,editso,stoklokasi,penerimaan,
                    purchasing,delivery,admin,packing,namamenu,stok,iddashboard,pindahlok,picking,onlineshop,%s taskrefill
                    from dashboardmenu where lvloperator='%s' order by lvloperator"""%(taskrefill,id1)
            
                print query
                dataCol=["lvloperator","reffiler","inbound","editso","stoklokasi","penerimaan","purchasing","delivery","admin","packing","namamenu","stok","iddashboard","pindahlok","picking","onlineshop","taskrefill"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
            
            if request.method == 'PUT':
                
                lvl= request.args.get('lvl')
                tbl = request.args.get('tbl')
             
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                query="update dashboardmenu set %s=1 where lvloperator='%s'"%(tbl,lvl)
                print query
                curs.execute(query)
                
                conn2.commit()
                curs.close()
                
                data1={}
                dic={}
                dic["error"]='false'
                dic["msg"]="Menu Update"
                dic["data"]=data1
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json')    
            if request.method == 'DELETE':
                lvl= request.args.get('lvl')
                tbl = request.args.get('tbl')
             
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                query="update dashboardmenu set %s=0 where lvloperator='%s'"%(tbl,lvl)
                print query
                curs.execute(query)
                
                conn2.commit()
                curs.close()
                
                data1={}
                dic={}
                dic["error"]='false'
                dic["msg"]="Menu Update"
                dic["data"]=data1
                
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                return Response(strDic, mimetype='application/json') 
        @app.route('%s/getMenu'%(folderAPI), methods=['GET' , 'PUT'])
        def getMenu():
            namaTabel2="menudet"
            
            if request.method == 'GET':
       
                #strWhere="where nomorpo='%s' "%id1
                strWhere=""#where nomorpo='%s'"%id1
             
                return bikinGetJSONExt(namaTabel2,strWhere)
            
        @app.route('%s/getAdmin'%(folderAPI), methods=['GET'])
        def getAdmin():
            namaTabel2="pegawai"
            
            if request.method == 'GET':
          
                #strWhere="where nomorpo='%s' "%id1
                strWhere="where level!='' and catatan!='FAKTURIS' AND catatan!='HRO' AND catatan!='' group by level order by level "#where nomorpo='%s'"%id1
             
                query="select level,catatan from pegawai"
                
                dataCol=["level","devisi"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
            
        @app.route('%s/editSo'%(folderAPI), methods=['GET', 'PUT'])
        def editSo():
            namaTabel2="dsalesorder"
            
            if request.method == 'GET':
          
                id1 = request.args.get('noso')
       
                strWhere="where noso='%s' order by stat2 desc"%id1
                query="select * from %s %s"%(namaTabel2,strWhere)
                #print query
                
                conn2=mysql.get_db()
                theCon2=conn2.cursor()
                theCon2.execute(query)
                if theCon2.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Tidak Ada Data"
                    theCon2.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
             
                return bikinGetJSONExt(namaTabel2,strWhere)
            
            if request.method == 'PUT':
          
                dapat= request.get_json()
                
                id1=dapat['id1']
                jml1=dapat['jml1'] #jumlah inputan terbaru
                jml2=dapat['jml2']
                _jml1=dapat['_jml1'] #jumlah sebelum
                kodebrg = dapat['kodebrg']
                user = dapat['user']
          
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
                query="select jmlkarton from barangdet where kodebrg='%s'"%kodebrg
                single=ambilSatuRowSQL(query)
                try:karton=single[0]
                except:karton=0
                
                jmlkarton = int(karton)
                jml = int(jml1)
                _jml = int(_jml1)
             
                diff=0
                if 1:
                    if jml>_jml:# tambah stok / kurang stok
                        diff = jml-_jml #cek selisih
                        if diff>=jmlkarton: #kartonan atau lepasan
                            diff = diff/jmlkarton
                            query="update dstoklokasi set jumlahbarang=jumlahbarang-'%s', where kodebarang='%s' and satuan='karton' and jumlahbarang>0 limit 1"%(diff,kodebrg)
                            #print query
                            curs.execute(query)
                          
                        else:
                            query="update dstoklokasi set jumlahbarang=jumlahbarang-'%s' where kodebarang='%s' and satuan='' and jumlahbarang>0 limit 1"%(diff,kodebrg)
                            #print query
                            curs.execute(query)
                            
                    else: #kurang stok
                        if jml==0:
                            query="update dstoklokasi set jumlahbarang=jumlahbarang+'%s' where kodebarang='%s' and satuan='karton' and jumlahbarang>0 limit 1"%(_jml,kodebrg)
                            curs.execute(query)
                        else:
                            diff = _jml-jml #cek selisih
                            if diff>=jmlkarton: #kartonan atau lepasan
                                diff = diff/jmlkarton
                                query="update dstoklokasi set jumlahbarang=jumlahbarang+'%s' where kodebarang='%s' and satuan='karton' and jumlahbarang>0 limit 1"%(diff,kodebrg)
                                #print query
                                curs.execute(query)
                              
                            else:
                                query="update dstoklokasi set jumlahbarang=jumlahbarang+'%s' where kodebarang='%s' and satuan='' and jumlahbarang>0 limit 1"%(diff,kodebrg)
                                #print query
                                curs.execute(query)
                    
                
                query="update dsalesorder set jml1='%s',stat1='picking',jml2='%s',stsEdit='edit',stat4=now(),stat2='%s' where id='%s'"%(jml1,jml2,user,id1)
                #print query
                curs.execute(query)

                conn2.commit()
                curs.close()
                
                dic={}
                dic["error"]='false'
                dic["msg"]="SO Terupdate"
                dic["data"]=""
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                
                return Response(strDic, mimetype='application/json')
            
if 1: #New Reffiller
        @app.route('%s/newReffil'%(folderAPI), methods=['GET','POST'])
        def newReffil():
            namaTabel2="dstoklokasi"
            
            if request.method == 'GET':
       
                id1= request.args.get('lokasi')
                conn2=mysql.get_db()
                theCon2=conn2.cursor()
                query="select kodebarang from dstoklokasi where lokasi='%s' and jumlahbarang>0 group by kodebarang"%id1
                theCon2.execute(query)
                if theCon2.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Tidak Ada Barang Di Lokasi"
                    theCon2.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
             
                strWhere=""
                theCon2.close()
                query="""select iddstoklokasi,kodebarang,CONVERT((sum(jumlahbarang)), SIGNED)jumlahbarang,kodebarangkarton,
                    (select namabrg from barang where kodebrg=kodebarang limit 1) from %s 
                    where lokasi='%s' and jumlahbarang>0 group by kodebarang"""%(namaTabel2,id1)
                dataCol=["iddstok","kodebarang","stok","kodebarangkarton","namabarang"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
            
            if request.method == 'POST':
                namaTabel="temprefill"
                
                dapat= request.get_json()
                iddstok=dapat['iddstok']
                nama=dapat['namaoperator']
                kodebrg=dapat['kodebrg']
                namabrg=dapat['namabrg']
                lokasi=dapat['lokasi']
                jmlambil=dapat['jmlkarton']
                kodebrgkarton=dapat['kodebrgkarton']
                
                conn2=mysql.get_db()
                curs=conn2.cursor()
                query="select * from %s where namaoperator='%s' and kodebrg='%s' and status='collect'"%(namaTabel,nama,kodebrg)
                curs.execute(query)
                if curs.rowcount!=0:
                    data1={}
                    dic={}
                    dic["error"]='true'
                    dic["msg"]="Sudah Masuk Daftar Tugas Reffill"
                    dic["data"]=data1
                    conn2.commit()
                    curs.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")

                    return Response(strDic, mimetype='application/json')
             
                if kodebrgkarton=="":
                    query="select kodebarangkarton from dstoklokasi where kodebarang='%s' and satuan='karton' and kodebarangkarton!='' order by tglmasuk desc limit 1"%kodebrg
                    print query
                    try:kodebrgkarton=ambilSatuRowSQL(query)[0]
                    except:kodebrgkarton=""
                    
                
                query="select jmlkarton from barangdet where kodebrg='%s'"%kodebrg
                try:jmlkarton=ambilSatuRowSQL(query)[0]
                except:jmlkarton=1
                
                jumlahpcs = int(jmlkarton)*int(jmlambil)
            
                query="""insert into temprefill (namaOperator,tglRef,kodebrg,namabrg,jmlAmbil,tglambil,status,kodebrgkarton,lokasiKarton) 
                    values ('%s',now(),'%s','%s','%s',now(),'collect','%s','%s')"""%(nama,kodebrg,namabrg,jumlahpcs,kodebrgkarton,lokasi)
                #print query
                curs.execute(query)
             
                #KURANGI STOK KARTON FLEKSIBEL
                jmlTot=int(jmlambil)
                query="select iddstoklokasi, jumlahbarang from dstoklokasi where kodebarang='%s' and lokasi='%s' and jumlahbarang>0 and satuan='karton' order by iddstoklokasi"%(kodebrg,lokasi)
                dataBrgPO={}
                for single in ambilBanyakRowSQL(query):
                    dataBrgPO[single[0]]=[single[1]]
                    
                for single in dataBrgPO:
                    jmlRun=dataBrgPO[single][0]
                    idpodet=single
                    lagi=0
                    if jmlRun>=jmlTot:  
                        query="update dstoklokasi set jumlahbarang=jumlahbarang-%s where iddstoklokasi='%s'"%(jmlTot,idpodet)
                        curs.execute(query)
                        lagi=1
                    else:
                        query="update dstoklokasi set jumlahbarang=jumlahbarang-%s where iddstoklokasi='%s'"%(jmlRun,idpodet)
                        curs.execute(query)
                        jmlTot=jmlTot-jmlRun
                        lagi=0
                    
                    if lagi:break
                #query="update dstoklokasi set jumlahbarang=jumlahbarang-%s where iddstoklokasi='%s'"%(jml,iddstok)
                #print query
                #curs.execute(query)
                conn2.commit()
                curs.close()
                
                dic={}
                dic["error"]='false'
                dic["msg"]="Tugas Terisi"
                dic["data"]=""
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                
                return Response(strDic, mimetype='application/json')
            
        @app.route('%s/newReffilGet'%(folderAPI), methods=['GET', 'POST'])
        def newReffilGet():
            namaTabel2="temprefill"
            
            if request.method == 'GET':
       
                id1= request.args.get('user')
                strWhere="where namaoperator='%s' and status='collect'"%id1
             
                query="select * from %s %s"%(namaTabel2,strWhere)
                print query
                
                conn2=mysql.get_db()
                theCon2=conn2.cursor()
                theCon2.execute(query)
                if theCon2.rowcount==0:
                    data1={}
                    dic={}
                    dic["error"]='false'
                    dic["msg"]="Belum Ada Tugas"
                    theCon2.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
                
                theCon2.close()
                query="select idtempRefill,trim(kodebrg),namabrg,(select lokasi from dstoklokasi where kodebarang=kodebrg and satuan='' order by tglmasuk desc limit 1),jmlambil from %s"%namaTabel2
                dataCol=["idtemp","kodebrg","namabrg","lokasi","jmlambil"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
            if request.method == 'POST':
                namaTabel="dstoklokasi"
                
                dapat= request.get_json()
                kodebrg=dapat['kodebarang']
                kodebrgkarton=dapat['kodebarangkarton']
                lokasi=dapat['lokasi']
                namalogin=dapat['operator']
                jumlahbrg=dapat['jumlahbarang']
                idtemp=dapat['idtemp']
             
                conn2=mysql.get_db()
                curs=conn2.cursor()
                
          
                query="insert into dstoklokasi(kodebarang,kodebarangkarton,lokasi,operator,tglmasuk,jumlahbarang,sumber,stokawal) values ('%s','%s','%s','%s',now(),'%s','refill_new','%s')"%(kodebrg,kodebrgkarton,lokasi,namalogin,jumlahbrg,jumlahbrg)
                #print query
                curs.execute(query)
                
                query="update temprefill set lokasi='%s', tgldrop=now(), status='selesai_refill' where idtemprefill='%s'"%(lokasi,idtemp)
                #print query
                curs.execute(query)

                conn2.commit()
                curs.close()
                
                dic={}
                dic["error"]='false'
                dic["msg"]="Stok Ditambah"
                dic["data"]=""
                strDic="%s"%dic
                strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                
                return Response(strDic, mimetype='application/json')
        @app.route('%s/newReffilJml'%(folderAPI), methods=['GET','PUT'])
        def newReffilJml():
            namaTabel2="dstoklokasi"
            
            if request.method == 'GET':
       
                id1= request.args.get('kodebrg')
                user= request.args.get('user')
                strWhere="where kodebarang='%s' and satuan='' group by lokasi"%id1
             
                query="select * from %s %s"%(namaTabel2,strWhere)
                print query
                
                conn2=mysql.get_db()
                theCon2=conn2.cursor()
                theCon2.execute(query)
                if theCon2.rowcount==0:
                    theCon2.close()
                    strWhere="where kodebrg='%s'"%id1
                    query="select trim(kodebrg),'Tidak Ditemukan Lokasi',0 stok,namabrg,(select kodebrgkarton from barangdet where barangdet.kodebrg=barang.kodebrg limit 1) from barang"
                    print query
                    dataCol=["kodebrg","lokasi","stok","namabrg","kodebarangkarton"]
                    return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
                 

                theCon2.close()
                query="select trim(kodebarang),lokasi,CONVERT(sum(jumlahbarang), CHAR),(select namabrg from barang where kodebrg=kodebarang limit 1),kodebarangkarton from %s"%(namaTabel2)
                print query
                dataCol=["kodebrg","lokasi","stok","namabrg","kodebarangkarton"]
                return bikinGetJSONExtQueryMan(query,strWhere,dataCol)
            
        @app.route('%s/inputDataBaru'%(folderAPI), methods=['PUT'])
        def inputDataBaru():
            namaTabel2="dstoklokasi"
            
            if request.method == 'PUT':
       
                dapat= request.get_json()
                id1= dapat['kodebarang']
                barcode= dapat['barcode']
                jml= dapat['jml']
                pack= dapat['kodebrgpack']
                jmlpack= dapat['jmlpack']
                karton= dapat['kodebrgkarton']
                jmlkarton= dapat['jmlkarton']
                lokasi= dapat['lokasi']
                satuan= dapat['satuan']
                userlogin= dapat['user']
                
                
                conn2=mysql.get_db()
                theCon2=conn2.cursor()
                print satuan
                
                #LEPASAN
                if '%s'%satuan=="":
                    if '%s'%lokasi!="":
                        query="select * from dstoklokasi where kodebarang='%s' and satuan=''"%(id1)
                        print query
                        theCon2.execute(query)
                        if theCon2.rowcount>0:
                            data1={}
                            dic={}
                            dic["error"]='true'
                            dic["msg"]="Barang Sudah Punya Riwayat Di Lepasan"
                            theCon2.close()
                            strDic="%s"%dic
                            strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                            return Response(strDic, mimetype='application/json')
                        query="""insert into dstoklokasi (kodebarang,kodebarangkarton,tglmasuk,lokasi,jumlahbarang,operator,satuan,stokawal,sumber) 
                            values('%s','%s',now(),'%s',0,'%s','%s',0,'Input New')"""%(id1,karton,lokasi,userlogin,satuan)
                        theCon2.execute(query)
                        print query
                    if '%s'%barcode!="":
                        query="""update barang set barcode='%s' where kodebrg='%s'"""%(barcode,id1)
                        theCon2.execute(query)
                        query="""update barangdet set jumlahbrg='%s' where kodebrg='%s'"""%(jml,id1)
                        theCon2.execute(query)
                    if '%s'%pack!="":
                        query="""update barangdet set kodebrgpack='%s',jmlpack='%s' where kodebrg='%s'"""%(pack,jmlpack,id1)
                        theCon2.execute(query)
                    if '%s'%karton!="":
                        query="""update barangdet set kodebrgkarton='%s',jmlkarton='%s' where kodebrg='%s'"""%(karton,jmlkarton,id1)
                        theCon2.execute(query)
                    print lokasi,barcode,pack,karton
                    
                    conn2.commit()
                    theCon2.close()
                    
                    data1={}
                    dic={}
                    dic["error"]='false'
                    dic["msg"]="Input Lepasan Berhasil"
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
                        
                #KARTONAN
                if '%s'%satuan!="":
                    if '%s'%lokasi!="":
                        query="select * from dstoklokasi where kodebarang='%s' and lokasi='%s' and satuan='karton'"%(id1,lokasi)
                        theCon2.execute(query)
                        if theCon2.rowcount!=0:
                            data1={}
                            dic={}
                            dic["error"]='false'
                            dic["msg"]="Barang Sudah Punya Riwayat Di Kartonan"
                            theCon2.close()
                            strDic="%s"%dic
                            strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                            return Response(strDic, mimetype='application/json')
                        query="""insert into dstoklokasi (kodebarang,kodebarangkarton,tglmasuk,lokasi,jumlahbarang,operator,satuan,stokawal,sumber) 
                            values('%s','%s',now(),'%s',0,'%s','%s',0,'Input New')"""%(id1,karton,lokasi,userlogin,satuan)
                        theCon2.execute(query)
                    if '%s'%barcode!="":
                        query="""update barang set barcode='%s' where kodebrg='%s'"""%(barcode,id1)
                        theCon2.execute(query)
                        query="""update barangdet set jumlahbrg='%s' where kodebrg='%s'"""%(jml,id1)
                        theCon2.execute(query)
                    if '%s'%pack!="":
                        query="""update barangdet set kodebrgpack='%s',jmlpack='%s' where kodebrg='%s'"""%(pack,jmlpack,id1)
                        theCon2.execute(query)
                    if '%s'%karton!="":
                        query="""update barangdet set kodebrgkarton='%s',jmlkarton='%s' where kodebrg='%s'"""%(karton,jmlkarton,id1)
                        theCon2.execute(query)
                        
                        
                    conn2.commit()
                    theCon2.close()
                    
                        
                    data1={}
                    dic={}
                    dic["error"]='false'
                    dic["msg"]="Input Kartonan Berhasil"
                    theCon2.close()
                    strDic="%s"%dic
                    strDic=strDic.replace("'",'"').replace('L,',',').replace('": u','": ').replace(', u"',', "').replace('{u"','{"').replace("L,"," ,")
                    return Response(strDic, mimetype='application/json')
                    

if __name__ == "__main__":

#3305 mulai
#3301 mulai2
    app.run(host="0.0.0.0", port=3301, debug=True)
#    app.run(host="0.0.0.0", port=5000, debug=True)
#    cors.run()
#    cors