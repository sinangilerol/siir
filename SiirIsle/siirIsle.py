import os
import re
import sqlite3 as sql
from veritabaniislemleri import * 

dir_name=os.path.join(os.getcwd(),"Siirler")#siirlerin olduğu klasöre geçtik
db=sql.connect(os.path.join(os.path.abspath(os.path.join(os.getcwd(),os.pardir) ) ,"SiirV2.db") )
cs=db.cursor()

#------------------------------------------
def sairGetir(baslangic,bitis):
    sairs=os.listdir(dir_name)
    sairSayisi=len(sairs)
    if bitis < baslangic or bitis > sairSayisi or baslangic > sairSayisi :
        print("HATA!")
        if bitis < baslangic:
            print("Parametreleri kontrol edin")
        if bitis > sairSayisi:
            print("max sair sayisini gectin.Max sair sayisi: ",sairSayisi)
        return []
    else:
        sair_list=[]
        for i in range(baslangic,bitis):
            sair_list.append(sairs[i])
        return sair_list
#------------------------------------------------
def siirGetir(sair):
    siirs=os.listdir(os.path.join(dir_name,sair))
    return siirs
#----------------------------------------------
def duzelt(string):
    string=string.replace("?"," ? ").replace("!"," ! ")
    new_l=[]
    spaciel=["ı","ö","ü","ş","ğ","ç"," ","?","!"]
    for i in string:
        if not i.isalpha():
            if i in spaciel:
                new_l.append(i)
            else:
                new_l.append(" ")
        else:
            new_l.append(i)
    return "".join(new_l)
    
def satirKontrol(satir):
    if satir.strip():
        return True
    return False
#---------------------------------------------
def cumleParcala(cumle):
    cumle=cumle.lower()
    kelimelist=[]
    for i in cumle.split():
        if i.strip():
            kelimelist.append(i)
    return kelimelist
#---------------------------------------------
def siirOku(sair,siir):
    f=open(os.path.join(os.path.join(dir_name,sair),siir),encoding="utf-8")

    #print(f.read().replace("\n","")) 
    satir= [] 
    for x in f:
        x=duzelt(x)
        if satirKontrol(x):
            satir.append(x)
    f.close()
    return satir
#--------------------String islemleri-----------------------------------

def tekkelimeislemleri(kelimeler_id,siir_id):
    kelimelerekle_GRAF(kelimeler_id,siir_id)
    tekkelimecumleekle_GRAF(tekkelimecumleekle(kelimeler_id[0]),siir_id)
    
def ikikelimeislemleri(kelimeler_id,siir_id):
    kelimelerekle_GRAF(kelimeler_id,siir_id)
    ikikelimecumleekle_GRAF(ikikelimecumleekle(kelimeler_id[0],kelimeler_id[1]),siir_id)

def cokkelimeislemleri(kelimeler_id,siir_id):
    kelimelerekle_GRAF(kelimeler_id,siir_id)
    for i in range(0,len(kelimeler_id)-1):
        if i== 0:
            baslatcumleekle_GRAF(baslatcumleekle(kelimeler_id[0],kelimeler_id[1]),siir_id)
        elif i== len(kelimeler_id)-2:
            bitircumleekle_GRAF(bitircumleekle(kelimeler_id[i],kelimeler_id[i+1]),siir_id)
        else:
            devamcumleekle_GRAF(devamcumleekle(kelimeler_id[i],kelimeler_id[i+1]),siir_id)

            
def satirekle(kelimeler,siir_id):
    if len(kelimeler) == 1:
        tekkelimeislemleri(kelimeler,siir_id)
    elif len(kelimeler) == 2:
        ikikelimeislemleri(kelimeler,siir_id)
    else:
        cokkelimeislemleri(kelimeler,siir_id)

def ozelkarakterkaldir(siir_isim):
    return siir_isim.replace(".txt","").replace("'","").replace(",","").replace("-","").replace('"',"").replace("_","").replace(";","").replace("!","").replace("?","").replace(".","").replace("/","")
    


def  main():
    sairs=sairGetir(744,745) # tum sairleri aynı anda islemek zor oldugundan parca parca okundu.
    if sairs: #boş değilse
        for i in sairs:
            print(i," ekleniyor....")
            siirs=siirGetir(i)
            sair_id=sairekle(i,len(siirs))
            for j in siirs:
                print("     ----",j," ekleniyor...")
                siir_id=siirekle(ozelkarakterkaldir(j),sair_id) 
                satirs=siirOku(i,j)
                for k in satirs:
                    kelimeler=cumleParcala(k)
                    satirekle(kelimelerekle(kelimeler),siir_id)
                    
if __name__ == "__main__":
    main()








    
