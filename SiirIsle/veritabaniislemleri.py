import sqlite3 as sql
import os
#------------------------------------------------------------------------------
def vtAc():    
    return sql.connect(os.path.join(os.path.abspath(os.path.join(os.getcwd(),os.pardir) ) ,"SiirV2.db") )
#------------------------------------------------------------------------------

def sairekle(sair,siirsayisi):#tamam
    db=vtAc()
    cs=db.cursor()
    datas=cs.execute("select * from Sair where sair_ad='{name}' ".format(name=sair))
    d=datas.fetchone()
    if not d == None: # eğer sair varsa
        sair_id,sair_ad,s_sayisi=d
        yenisiirsayisi=s_sayisi+siirsayisi
        cs.execute("update Sair set siir_sayisi = {ss} where sair_id={id_}".format(ss=yenisiirsayisi,id_=sair_id))
        db.commit()
        db.close()
        return sair_id
    else:
        cs.execute("insert into Sair (sair_ad,siir_sayisi) values ('{ad}',{ss}) ".format(ad=sair,ss=siirsayisi))
        db.commit()
        datas=cs.execute("select * from Sair where sair_ad='{name}' ".format(name=sair))
        d=datas.fetchone()
        sair_id,sair_ad,s_sayisi=d
        db.close()
        return sair_id
    
def siirekle(siirad,sair_id):
    db=vtAc()
    cs=db.cursor()
    cs.execute("insert into Siirler (sair_id,siir_adi) values ({id_},'{ad}') ".format(id_=sair_id,ad=siirad))
    db.commit()
    datas=cs.execute("select * from Siirler where siir_adi='{name}' and sair_id={id_} ".format(name=siirad,id_=sair_id))
    d=datas.fetchone()
    siir_id,sair_id,siir_adi=d
    db.close()
    return siir_id
#------------------------------------------------------------------------------
def kelimeekle(kelime): #kelime varsa adedini artirip idsini gonderir,yoksa adedini 1 yapar ekler idsini gonderir  
    db=vtAc()
    cs=db.cursor()
    datas=cs.execute("select * from Kelimeler where kelime='{klm}' ".format(klm=kelime))
    d=datas.fetchone()
    if not d == None: # eğer kelime onceden varsa
        kelime_id,kelime,adet=d
        adet=adet+1
        cs.execute("update Kelimeler set adet = {ss} where kelime_id={id_}".format(ss=adet,id_=kelime_id))
        db.commit()
        db.close()
        return kelime_id
    else:
        cs.execute("insert into Kelimeler (kelime,adet) values ('{klm}',{ss}) ".format(klm=kelime,ss=1))
        db.commit()
        datas=cs.execute("select * from Kelimeler where kelime='{i}' ".format(i=kelime))
        d=datas.fetchone()
        kelime_id,kelime,adet=d
        db.close()
        return kelime_id

def kelimelerekle(cumle):# geriye listedeki  kelimeleri ekleyerek idlerini gonderir
    kelimeids=[]
    for i in cumle:
        kelimeids.append(kelimeekle(i))
    return kelimeids
#------------------------------------------------------------------------------
def kelimeekle_GRAF(kelimeid,siirid): #
    db=vtAc()
    cs=db.cursor()
    datas=cs.execute("select * from Kelimeler_Siir_Graf where kelime_id={kid} and siir_id={sid} ".format(kid=kelimeid,sid=siirid))
    d=datas.fetchone()
    if not d == None: # eğer kelime grafi onceden varsa
        id_,kelime_id,siir_id,adet=d
        adet=adet+1
        cs.execute("update Kelimeler_Siir_Graf set adet = {ss} where id={id_}".format(ss=adet,id_=id_))
        db.commit()
        db.close()
      
    else:
        cs.execute("insert into Kelimeler_Siir_Graf (kelime_id,siir_id,adet) values ({kid},{sid},{a}) ".format(kid=kelimeid,sid=siirid,a=1))
        db.commit()
        db.close()
    
def kelimelerekle_GRAF(kelimeidlist,siirid): 
    for i in kelimeidlist:
        kelimeekle_GRAF(i,siirid)
#-------------------------------------------------------------
def tekkelimecumleekle(kelimeid):
    db=vtAc()
    cs=db.cursor()
    datas=cs.execute("select * from Tek_Kelime_Cumle where tek_kelime_id={i} ".format(i=kelimeid))
    d=datas.fetchone()
    if not d == None: # eğer kelime onceden varsa
        tek_kelime_id,yalniz_kelime_id,adet=d
        adet=adet+1
        cs.execute("update Tek_Kelime_Cumle set adet = {ss} where tek_kelime_id={id_}".format(ss=adet,id_=kelimeid))
        db.commit()
        db.close()
        return tek_kelime_id
    else:
        cs.execute("insert into Tek_Kelime_Cumle (yalniz_kelime_id,adet) values ({klm},{ss}) ".format(klm=kelimeid,ss=1))
        db.commit()
        datas=cs.execute("select * from Tek_Kelime_Cumle where yalniz_kelime_id={i} ".format(i=kelimeid))
        d=datas.fetchone()
        tek_kelime_id,yalniz_kelime_id,adet=d
        db.close()
        return tek_kelime_id
def tekkelimecumleekle_GRAF(tekkelimeid,siirid):
    db=vtAc()
    cs=db.cursor()
    datas=cs.execute("select * from Tek_Kelime_Cumle_Siir_Graf where tek_kelime_id={i} and siir_id={s} ".format(i=tekkelimeid,s=siirid))
    d=datas.fetchone()
    if not d == None: # eğer kelime onceden varsa
        id_,tek_kelime_id,siir_id,adet=d
        adet=adet+1
        cs.execute("update Tek_Kelime_Cumle_Siir_Graf set adet = {ss} where id={id_}".format(ss=adet,id_=id_))
        db.commit()
        db.close()
        
    else:
        cs.execute("insert into Tek_Kelime_Cumle_Siir_Graf (tek_kelime_id,siir_id,adet) values ({klm},{ss},{a}) ".format(klm=tekkelimeid,ss=siirid,a=1))
        db.commit()
        db.close()
#-------------------------------------------------------------
def baslatcumleekle(baslatid,devamid):
    db=vtAc()
    cs=db.cursor()
    datas=cs.execute("select * from Baslat_Cumle where baslatici_kelime_id={bki} and devam_kelime_id ={dki}".format(bki=baslatid,dki=devamid))
    d=datas.fetchone()
    if not d == None: # eğer kelime onceden varsa
        baslat_cumle_id,baslatici_kelime_id,devam_kelime_id,adet=d
        adet=adet+1
        cs.execute("update Baslat_Cumle set adet = {ss} where baslat_cumle_id={id_}".format(ss=adet,id_=baslat_cumle_id))
        db.commit()
        db.close()
        return baslat_cumle_id
    else:
        cs.execute("insert into Baslat_Cumle (baslatici_kelime_id,devam_kelime_id,adet) values ({bki},{dki},{a}) ".format(bki=baslatid,dki=devamid,a=1))
        db.commit()
        datas=cs.execute("select * from Baslat_Cumle where baslatici_kelime_id={bki} and devam_kelime_id ={dki}".format(bki=baslatid,dki=devamid))
        d=datas.fetchone()
        baslat_cumle_id,baslatici_kelime_id,devam_kelime_id,adet=d
        db.close()
        return baslat_cumle_id
def baslatcumleekle_GRAF(baslatcumleid,siirid):
    db=vtAc()
    cs=db.cursor()
    datas=cs.execute("select * from Baslat_Cumle_Siir_Graf where baslat_cumle_id={i} and siir_id={s} ".format(i=baslatcumleid,s=siirid))
    d=datas.fetchone()
    if not d == None: # eğer kelime onceden varsa
        id_,baslat_cumle_id,siir_id,adet=d
        adet=adet+1
        cs.execute("update Baslat_Cumle_Siir_Graf set adet = {ss} where id={id_}".format(ss=adet,id_=id_))
        db.commit()
        db.close()
        
    else:
        cs.execute("insert into Baslat_Cumle_Siir_Graf (baslat_cumle_id,siir_id,adet) values ({klm},{ss},{a}) ".format(klm=baslatcumleid,ss=siirid,a=1))
        db.commit()
        db.close()
#------------------------------------------------------------------------------
def bitircumleekle(sondevamid,bitirid):
    db=vtAc()
    cs=db.cursor()
    datas=cs.execute("select * from Bitir_Cumle where son_devam_kelime_id={sdk} and bitirici_kelime_id ={bki}".format(sdk=sondevamid,bki=bitirid))
    d=datas.fetchone()
    if not d == None: # eğer kelime onceden varsa
        bitir_cumle_id,son_devam_kelime_id,bitirici_kelime_id,adet=d
        adet=adet+1
        cs.execute("update Bitir_Cumle set adet = {ss} where bitir_cumle_id={id_}".format(ss=adet,id_=bitir_cumle_id))
        db.commit()
        db.close()
        return bitir_cumle_id
    else:
        cs.execute("insert into Bitir_Cumle (son_devam_kelime_id,bitirici_kelime_id,adet) values ({sdki},{bki},{a}) ".format(sdki=sondevamid,bki=bitirid,a=1))
        db.commit()
        datas=cs.execute("select * from Bitir_Cumle where son_devam_kelime_id={sdk} and bitirici_kelime_id ={bki}".format(sdk=sondevamid,bki=bitirid))
        d=datas.fetchone()
        bitir_cumle_id,son_devam_kelime_id,bitirici_kelime_id,adet=d
        db.close()
        return bitir_cumle_id
def bitircumleekle_GRAF(bitircumleid,siirid):
    db=vtAc()
    cs=db.cursor()
    datas=cs.execute("select * from Bitir_Cumle_Siir_Graf where bitir_cumle_id={i} and siir_id={s} ".format(i=bitircumleid,s=siirid))
    d=datas.fetchone()
    if not d == None: # eğer kelime onceden varsa
        id_,bitir_cumle_id,siir_id,adet=d
        adet=adet+1
        cs.execute("update Bitir_Cumle_Siir_Graf set adet = {ss} where id={id_}".format(ss=adet,id_=id_))
        db.commit()
        db.close()
        
    else:
        cs.execute("insert into Bitir_Cumle_Siir_Graf (bitir_cumle_id,siir_id,adet) values ({klm},{ss},{a}) ".format(klm=bitircumleid,ss=siirid,a=1))
        db.commit()
        db.close()
#--------------------------------------------------------------------------
def devamcumleekle(devamilk,devamson):
    db=vtAc()
    cs=db.cursor()
    datas=cs.execute("select * from Devam_Cumle where devam_ilk_id={di} and devam_son_id ={ds}".format(di=devamilk,ds=devamson))
    d=datas.fetchone()
    if not d == None: # eğer kelime onceden varsa
        devam_cumle_id,devam_ilk_id,devam_son_id,adet=d
        adet=adet+1
        cs.execute("update Devam_Cumle set adet = {ss} where devam_cumle_id={id_}".format(ss=adet,id_=devam_cumle_id))
        db.commit()
        db.close()
        return devam_cumle_id
    else:
        cs.execute("insert into Devam_Cumle (devam_ilk_id,devam_son_id,adet) values ({di},{ds},{a}) ".format(di=devamilk,ds=devamson,a=1))
        db.commit()
        datas=cs.execute("select * from Devam_Cumle where devam_ilk_id={di} and devam_son_id ={ds}".format(di=devamilk,ds=devamson))
        d=datas.fetchone()
        devam_cumle_id,devam_ilk_id,devam_son_id,adet=d
        db.close()
        return devam_cumle_id


def devamcumleekle_GRAF(devamcumleid,siirid):
    db=vtAc()
    cs=db.cursor()
    datas=cs.execute("select * from Devam_Cumle_Siir_Graf where devam_cumle_id={i} and siir_id={s} ".format(i=devamcumleid,s=siirid))
    d=datas.fetchone()
    if not d == None: # eğer kelime onceden varsa
        id_,devam_cumle_id,siir_id,adet=d
        adet=adet+1
        cs.execute("update Devam_Cumle_Siir_Graf set adet = {ss} where id={id_}".format(ss=adet,id_=id_))
        db.commit()
        db.close()
        
    else:
        cs.execute("insert into Devam_Cumle_Siir_Graf (devam_cumle_id,siir_id,adet) values ({klm},{ss},{a}) ".format(klm=devamcumleid,ss=siirid,a=1))
        db.commit()
        db.close()
#---------------------------------------------------------------------------------
def ikikelimecumleekle(ilkkelime,sonkelime):
    db=vtAc()
    cs=db.cursor()
    datas=cs.execute("select * from Iki_Kelime_Cumle where ilk_kelime_id={i} and son_kelime_id ={s}".format(i=ilkkelime,s=sonkelime))
    d=datas.fetchone()
    if not d == None: # eğer kelime onceden varsa
        iki_kelime_cumle_id,ilk_kelime_id,son_kelime_id,adet=d
        adet=adet+1
        cs.execute("update Iki_Kelime_Cumle set adet = {ss} where iki_kelime_cumle_id={id_}".format(ss=adet,id_=iki_kelime_cumle_id))
        db.commit()
        db.close()
        return iki_kelime_cumle_id
    else:
        cs.execute("insert into Iki_Kelime_Cumle (ilk_kelime_id,son_kelime_id,adet) values ({i},{s},{a}) ".format(i=ilkkelime,s=sonkelime,a=1))
        db.commit()
        datas=cs.execute("select * from Iki_Kelime_Cumle where ilk_kelime_id={i} and son_kelime_id ={s}".format(i=ilkkelime,s=sonkelime))
        d=datas.fetchone()
        iki_kelime_cumle_id,ilk_kelime_id,son_kelime_id,adet=d
        db.close()
        return iki_kelime_cumle_id
def ikikelimecumleekle_GRAF(ikikelimecumleid,siirid):
    db=vtAc()
    cs=db.cursor()
    datas=cs.execute("select * from Iki_Kelime_Cumle_Siir_Graf where iki_kelime_cumle_id={i} and siir_id={s} ".format(i=ikikelimecumleid,s=siirid))
    d=datas.fetchone()
    if not d == None: # eğer kelime onceden varsa
        id_,iki_kelime_cumle_id,siir_id,adet=d
        adet=adet+1
        cs.execute("update Iki_Kelime_Cumle_Siir_Graf set adet = {ss} where id={id_}".format(ss=adet,id_=id_))
        db.commit()
        db.close()
        
    else:
        cs.execute("insert into Iki_Kelime_Cumle_Siir_Graf (iki_kelime_cumle_id,siir_id,adet) values ({klm},{ss},{a}) ".format(klm=ikikelimecumleid,ss=siirid,a=1))
        db.commit()
        db.close()
#--------------------------------------------------------------------------------------------
 
def main():
    pass

if __name__ == "__main__":
    main()

