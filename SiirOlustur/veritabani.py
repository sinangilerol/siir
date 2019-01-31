import sqlite3 as sql
import os

# ileride performansı artırmak icin listeler tuple'a donusturulemeli !!!

#------------------------------------------------------------------------------
def vtAc():  # eger farklı bir klasor yolu kullanılırsa burası degistirilmeli   
    return sql.connect(os.path.join(os.path.abspath(os.path.join(os.getcwd(),os.pardir) ) ,"SiirV2.db") )
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def tumsairlerigetir():
    db=vtAc()
    cs=db.cursor()
    datas=cs.execute("select sair_id,sair_ad from Sair ")
    sairs=[]
    for i in datas:
        sairs.append(i)
    db.close()
    return sairs

def sairinsiirlerinigetir(sair_id):
    db=vtAc()
    cs=db.cursor()
    datas=cs.execute("select siir_id,siir_adi from Siirler where sair_id = {} ".format(sair_id))
    siirs=[]
    for i in datas:
        siirs.append(i)
    db.close()
    return siirs
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def convert_sairsids_as_str(sairs): # where xxx in () --> in icine yazılabillecek formata donusturur.
    return ",".join(map(str,sairs))
def convert_siirsids_as_str(siirs):
    return ",".join(map(str,siirs))
#------------------------------------------------------------------------------


#------------------------------------------------------------------------
def idToStr(_id):
    db=vtAc()
    cs=db.cursor()
    datas=cs.execute("select kelime from Kelimeler where kelime_id = {} ".format(_id))
    return datas.fetchone()[0]
#------------------------------------------------------------------------

#------------------------------------------------------------------------
def tekkelimecumle(uyak,sairs,siirs):
    satir=[ ]
    if sairs or siirs: #boş değilse
        satir = tekkelimecumle_ozel(uyak,sairs,siirs)
    else: # boş yani herkesden çekecek
        satir = tekkelimecumle_genel(uyak)
    return satir
def tekkelimecumle_ozel(uyak,sairs,siirs):
    
    db=vtAc()
    cs=db.cursor()
    
    datas=cs.execute("""select TKC.tek_kelime_id  from
                     Tek_Kelime_Cumle TKC inner join Tek_Kelime_Cumle_Siir_Graf TKCSG on
                     TKC.tek_kelime_id=TKCSG.tek_kelime_id inner join Siirler ON TKCSG.siir_id=Siirler.siir_id
                     inner join Sair ON Sair.sair_id=Siirler.sair_id inner join Kelimeler ON Kelimeler.kelime_id=TKC.tek_kelime_id
                     where (Sair.sair_id in ({sair}) or Siirler.siir_id in ({siir})) and Kelimeler.kelime like '%{uyak}' order by random() limit 1""".format
                     (sair = convert_sairsids_as_str(sairs) , siir = convert_siirsids_as_str(siirs) , uyak = uyak ) )

    
    
    _ =[ ]
    for i in datas:
        _.append(i[0])

    return _
                     
    
def tekkelimecumle_genel(uyak):
    
    db=vtAc()
    cs=db.cursor()
    datas=cs.execute("""select TKC.tek_kelime_id 
                    from Tek_Kelime_Cumle TKC inner join Tek_Kelime_Cumle_Siir_Graf TKCSG on
                     TKC.tek_kelime_id=TKCSG.tek_kelime_id inner join Siirler ON TKCSG.siir_id=Siirler.siir_id
                     inner join Sair ON Sair.sair_id=Siirler.sair_id inner join Kelimeler ON Kelimeler.kelime_id=TKC.tek_kelime_id
                     where Kelimeler.kelime like '%{uyak}'  order by random() limit 1 """.format( uyak = uyak ) )
    
    
    _ =[ ]
    for i in datas:
        _.append(i[0])

    return _
#--------------------------------------------------------------------------


#-------------------------------------------------------------------
def ikikelimecumle(uyak,sairs,siirs):
    satir = []
    if sairs or siirs: #boş değilse
        satir = ikikelimecumle_ozel(uyak,sairs,siirs)
    else: # boş yani herkesden çekecek
        satir = ikikelimecumle_genel(uyak)
    return satir
def ikikelimecumle_ozel(uyak,sairs,siirs):

    
    db=vtAc()
    cs=db.cursor()
    datas=cs.execute("""select IKC.ilk_kelime_id , IKC.son_kelime_id  from
                     Iki_Kelime_Cumle IKC inner join Iki_Kelime_Cumle_Siir_Graf IKCSG on
                     IKC.iki_kelime_cumle_id = IKCSG.iki_kelime_cumle_id inner join Siirler on IKCSG.siir_id=Siirler.siir_id
                     inner join Sair ON Sair.sair_id=Siirler.sair_id inner join Kelimeler ON Kelimeler.kelime_id=IKC.son_kelime_id
                     where (Sair.sair_id in ({sair}) or Siirler.siir_id in ({siir})) and Kelimeler.kelime like '%{uyak}'  order by random() limit 1 """.format
                     (sair = convert_sairsids_as_str(sairs) , siir = convert_siirsids_as_str(siirs) , uyak = uyak ) )

    
    
    _ =[ ]
    for i in datas:
        
        _.append(i[0])
        _.append(i[1])

    return _
    

    
def ikikelimecumle_genel(uyak):
    
    db=vtAc()
    cs=db.cursor()
    datas=cs.execute("""select IKC.ilk_kelime_id , IKC.son_kelime_id  from
                     Iki_Kelime_Cumle IKC inner join Iki_Kelime_Cumle_Siir_Graf IKCSG on
                     IKC.iki_kelime_cumle_id = IKCSG.iki_kelime_cumle_id inner join Siirler on IKCSG.siir_id=Siirler.siir_id
                     inner join Sair ON Sair.sair_id=Siirler.sair_id inner join Kelimeler ON Kelimeler.kelime_id=IKC.son_kelime_id
                     where Kelimeler.kelime like '%{uyak}' order by random() limit 1""".format( uyak = uyak ) )

    
    
    _ =[ ]
    for i in datas:
        _.append(i[0])
        _.append(i[1])

    return _
#-------------------------------------------------------------------

#-------------------------------------------------------------------
#+++++++++++++++++++++++++++++++
def cokkelimecumle_baslat(sairs,siirs):
    graf = [ 0 , 0 ]
    if sairs or siirs: #boş değilse
        graf = cokkelimecumle_baslat_ozel(sairs,siirs)
    else: # boş yani herkesden çekecek
        graf = cokkelimecumle_baslat_genel()
    return graf    
def cokkelimecumle_baslat_ozel(sairs,siirs):

    
    db=vtAc()
    cs=db.cursor()
    datas=cs.execute("""select BC.baslatici_kelime_id , BC.devam_kelime_id from
                     Baslat_Cumle BC inner join Baslat_Cumle_Siir_Graf BCSG on
                     BCSG.baslat_cumle_id = BC.baslat_cumle_id inner join Siirler on BCSG.siir_id=Siirler.siir_id
                     inner join Sair ON Sair.sair_id=Siirler.sair_id 
                     where (Sair.sair_id in ({sair}) or Siirler.siir_id in ({siir}))  order by random() limit 1 """.format
                     (sair = convert_sairsids_as_str(sairs) , siir = convert_siirsids_as_str(siirs) ) )

    
    
    _ = [ 0 , 0 ]
    for i in datas:
        _ = i[0],i[1]
    
    return _

def cokkelimecumle_baslat_genel():
    
    
    db=vtAc()
    cs=db.cursor()
    datas=cs.execute("""select BC.baslatici_kelime_id, BC.devam_kelime_id from
                     Baslat_Cumle BC 
                      order by random() limit 1 """  )

    
    
    _ = [ 0 , 0 ]
    for i in datas:
        _ = i[0],i[1]
    
    return _
#+++++++++++++++++++++++++++++++


def cokkelimecumle_devam(sairs,siirs,devam_kelime_id):
    graf = 0
    if sairs or siirs: #boş değilse
        graf = cokkelimecumle_devam_ozel(sairs,siirs,devam_kelime_id)
    else: # boş yani herkesden çekecek
        graf = cokkelimecumle_devam_genel(devam_kelime_id)
    return graf    
def cokkelimecumle_devam_ozel(sairs,siirs,devam_kelime_id):
    
    db=vtAc()
    cs=db.cursor()
    datas=cs.execute("""select DC.devam_son_id from
                     Devam_Cumle DC inner join Devam_Cumle_Siir_Graf DCSG on
                     DCSG.devam_cumle_id = DC.devam_cumle_id inner join Siirler on DCSG.siir_id=Siirler.siir_id
                     inner join Sair ON Sair.sair_id=Siirler.sair_id 
                     where (DC.devam_ilk_id={_id}) and (Sair.sair_id in ({sair}) or Siirler.siir_id in ({siir}))
                     order by random() limit 1 """.format
                     (_id = devam_kelime_id , sair = convert_sairsids_as_str(sairs) ,
                      siir = convert_siirsids_as_str(siirs) ) )

    
    
    _ = 0
    for i in datas:
        _ = i[0]
    
    return _

def cokkelimecumle_devam_genel(devam_kelime_id):
    
    
    db=vtAc()
    cs=db.cursor()
    datas=cs.execute("""select DC.devam_son_id  from
                     Devam_Cumle DC where (DC.devam_ilk_id = {_id}) 
                      order by random() limit 1 """.format (_id = devam_kelime_id)  )

    
    _ = 0
    for i in datas:
        _ = i[0]
    
    return _

def cokkelimecumle_bitir(uyak,sairs,siirs,bitir_kelime_id):
    graf = 0
    if sairs or siirs: #boş değilse
        graf = cokkelimecumle_bitir_ozel(uyak,sairs,siirs,bitir_kelime_id)
    else: # boş yani herkesden çekecek
        graf = cokkelimecumle_bitir_genel(uyak,bitir_kelime_id)
    return graf    
def cokkelimecumle_bitir_ozel(uyak,sairs,siirs,bitir_kelime_id):
    
    db=vtAc()
    cs=db.cursor()
    datas=cs.execute("""select BC.bitirici_kelime_id 
                    from Bitir_Cumle BC  
                    inner join Bitir_Cumle_Siir_Graf BCSG on 
                    BCSG.bitir_cumle_id = BC.bitir_cumle_id
                    inner join Siirler on BCSG.siir_id = Siirler.siir_id
                    inner join Sair on Sair.sair_id = Siirler.sair_id
                    inner join Kelimeler on Kelimeler.kelime_id=BC.bitirici_kelime_id
                     where (BC.son_devam_kelime_id= {_id}) and (Sair.sair_id in ({sair}) or
                     Siirler.siir_id in ({siir}) ) and Kelimeler.kelime like '%{uyak}'
                    order by random() limit 1 """.format
                     (_id = bitir_kelime_id , sair = convert_sairsids_as_str(sairs) ,
                      siir = convert_siirsids_as_str(siirs) , uyak = uyak ) )

    
    _ = 0
    for i in datas:
        _ = i[0]
    
    return _
def cokkelimecumle_bitir_genel(uyak,bitir_kelime_id):
    
    db=vtAc()
    cs=db.cursor()
    datas=cs.execute("""select BC.bitirici_kelime_id 
                    from Bitir_Cumle BC  
                    inner join Bitir_Cumle_Siir_Graf BCSG on 
                    BCSG.bitir_cumle_id = BC.bitir_cumle_id
                    inner join Siirler on BCSG.siir_id = Siirler.siir_id
                    inner join Sair on Sair.sair_id = Siirler.sair_id
                    inner join Kelimeler on Kelimeler.kelime_id=BC.bitirici_kelime_id
                     where (BC.son_devam_kelime_id= {_id}) and Kelimeler.kelime like '%{uyak}'
                    order by random() limit 1 """.format
                     (_id = bitir_kelime_id , uyak = uyak ) )

    _ = 0
    for i in datas:
        _ = i[0]
    
    return _

#-------------------------------------------------------------------

        
if __name__ == "__main__":
    pass
