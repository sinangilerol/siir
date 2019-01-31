import sys
import random
import veritabani as vt
feature_list=[]

#----------------------------------
MAX_SATIR_SAYISI=15
MIN_SATIR_SAYISI=1

MAX_KITA_SAYISI=10
MIN_KITA_SAYISI=1

MAX_KELIME_SAYISI=10
MIN_KELIME_SAYISI=1

RECURSIVE_COUNTER = 0
MAX_RECURSİVE_COUNTER = 5
#----------------------------------

class SatirUretici:
    def __init__( self , uyak , sairs , siirs  ):
        self.uyak = uyak 
        self.sairs = sairs
        self.siirs = siirs
        #----------------------------------
        self.COK_KELİME_REC_COUNTER = 0
        self.COK_KELİME_REC_COUNTER_MAX = 50
        self.COK_KELIME_REC_BASLANGIC_COUNTER = 0
        self.COK_KELIME_REC_BASLANGIC_MAX = 3
        self.COK_KELIME_REC_DEVAM_COUNTER = 0
        self.COK_KELIME_REC_DEVAM_MAX = 2
        #----------------------------------
    def uret(self,kelime_sayisi):
        satir_ids = [ ]
        if kelime_sayisi == 0:
            kelime_sayisi = self.kelime_sayisi_uret()
        
        if kelime_sayisi == 1:
            satir_ids= self.tekkelimeislemleri()
        elif kelime_sayisi == 2:
            satir_ids=self.ikikelimeislemleri()
        else :
            satir_list = [ ]
            satir_ids=self.cokkelimeislemleri(kelime_sayisi , self.uyak , self.sairs , self.siirs,satir_list , 0)
        
        kelimeler=self.idToStr(satir_ids)
        satir =self.kelimelerToSatir(kelimeler)
        return satir
        
    
    def tekkelimeislemleri(self):
        result=vt.tekkelimecumle(self.uyak,self.sairs,self.siirs)

        if not result: #yani boşsa
            result=vt.tekkelimecumle(self.uyak, [ ] , [ ] )
            if not result : #yine bossa
                result =vt.tekkelimecumle( "" , [ ] , [ ] )

        return result
        
        
    def ikikelimeislemleri(self):
        result = vt.ikikelimecumle(self.uyak , self.sairs,self.siirs)

        if not result: #yani boşsa
            result=vt.ikikelimecumle(self.uyak, [ ] , [ ] )
            if not result : #yine bossa
                result =vt.ikikelimecumle( "" , [ ] , [ ] )
        return result
        
    def cokkelimeislemleri(self,kelime_sayisi,uyak,sairs,siirs,satir_list ,cikis_olmayan_graf_id):
        self.COK_KELİME_REC_COUNTER = self.COK_KELİME_REC_COUNTER +1
        if self.COK_KELİME_REC_COUNTER  == self.COK_KELİME_REC_COUNTER_MAX :
            self.COK_KELİME_REC_COUNTER = 0
            print ("RECURSIVE SINIRI ASILDI....")
            return self.cokkelimeislemleri(kelime_sayisi,"",[ ],[ ],[ ] ,0)

        print (kelime_sayisi,uyak,sairs,siirs,satir_list ,cikis_olmayan_graf_id,sep= "  <--->  ")

#-----------------------------------------------------------------------------------------     
        if len ( satir_list ) == 0: #baslangic islemleri
            baslangic_id,baslangic_devam_id = vt.cokkelimecumle_baslat(sairs,siirs)

            if baslangic_id == 0 : # sonuc yoksa
            # bu koşul neredeyse imkansız ... ama genede yazdım
                return self.cokkelimeislemleri(kelime_sayisi,uyak,  [ ] , [ ] , satir_list , 0)
            
                    

            elif baslangic_id == cikis_olmayan_graf_id: #...
                self.COK_KELIME_REC_BASLANGIC_COUNTER = self.COK_KELIME_REC_BASLANGIC_COUNTER + 1

                if self.COK_KELIME_REC_BASLANGIC_COUNTER == self.COK_KELIME_REC_BASLANGIC_MAX : #  parametreleri genellestir
                    self.COK_KELIME_REC_BASLANGIC_COUNTER = 0
                    return self.cokkelimeislemleri(kelime_sayisi,uyak, [ ] , [ ] ,satir_list , 0)
                else : # tekrar denesin belki başka yol bulur
                    return self.cokkelimeislemleri(kelime_sayisi,uyak,sairs,siirs,satir_list ,cikis_olmayan_graf_id)
                    
            else: #sonuc varsa...
                satir_list.append(baslangic_id)
                satir_list.append(baslangic_devam_id)
                return self.cokkelimeislemleri(kelime_sayisi,uyak,sairs,siirs,satir_list , 0)

#-----------------------------------------------------------------------------------------
            
        elif len ( satir_list ) == kelime_sayisi -1 : # bitirme islemleri
            bitir_id = vt.cokkelimecumle_bitir(uyak,sairs,siirs,satir_list [len (satir_list) -1 ] )
            if bitir_id == 0: #bulamamissa
                if len (satir_list) == 2: # yani 3 kelimelik cumle ise
                    temp = satir_list[0]
                    satir_list = [ ]
                    return self.cokkelimeislemleri(kelime_sayisi,uyak,sairs,siirs,satir_list ,temp)
                else: # kelime sayısı 3 den fazla ise
                    temp = satir_list.pop()
                    return self.cokkelimeislemleri(kelime_sayisi,uyak,sairs,siirs,satir_list ,temp)
            else: # bitirecek kelimeye buldu artık recursive geriye donebilir
                satir_list.append(bitir_id)
                self.COK_KELİME_REC_COUNTER = 0
                
                return satir_list 
                
#-----------------------------------------------------------------------------------------
        else :# devam islemleri
            devam_id = vt.cokkelimecumle_devam(sairs,siirs,satir_list [len (satir_list) -1 ])
            if devam_id == 0 :
                if len (satir_list) == 2:
                    temp = satir_list[0]
                    satir_list = [ ]
                    return self.cokkelimeislemleri(kelime_sayisi,uyak,sairs,siirs,satir_list ,temp)
                else :
                    
                    temp = satir_list.pop()
                    return self.cokkelimeislemleri(kelime_sayisi,uyak,sairs,siirs,satir_list ,temp)
            elif  devam_id == cikis_olmayan_graf_id :
                self.COK_KELIME_REC_DEVAM_COUNTER = self.COK_KELIME_REC_DEVAM_COUNTER + 1 
                if self.COK_KELIME_REC_DEVAM_COUNTER == self.COK_KELIME_REC_DEVAM_MAX:
                    self.COK_KELIME_REC_DEVAM_COUNTER = 0
                    if len (satir_list) == 2:
                        temp = satir_list[0]
                        satir_list = [ ]
                        return self.cokkelimeislemleri(kelime_sayisi,uyak,sairs,siirs,satir_list ,temp)
                    else:
                        temp = satir_list.pop()
                        return self.cokkelimeislemleri(kelime_sayisi,uyak,sairs,siirs,satir_list ,temp)
                else : 
                    return self.cokkelimeislemleri(kelime_sayisi,uyak,sairs,siirs,satir_list ,cikis_olmayan_graf_id)

            else : # cikis varsa ekle
                satir_list.append(devam_id)
                return self.cokkelimeislemleri(kelime_sayisi,uyak,sairs,siirs,satir_list ,0)
        

    
    def idToStr(self,satir_ids): # verilen kelime idlerini str ye cevirip gönderir
        kelimeler=[]
        for i in satir_ids:
            _ = vt.idToStr(i)
            kelimeler.append(_)
            
        return kelimeler
    
    # kelimelerin arasına bosluk bırakır.İleride noktalama islemleri bu method degistirilerek yapılabilir
    def kelimelerToSatir(self,kelimeler):
        return " ".join(kelimeler)
        

    def kelime_sayisi_uret(self): #belki burası değişir diye methodla yaptım 
        return random.randint(MIN_KELIME_SAYISI,MAX_KELIME_SAYISI)


def setparams(params):
    global feature_list
    
    if  (params[0] == "random") :#random siir secilmiş
        
        feature_list=generate_feature()

    else:#random değilse
        
        feature_list=featurecontrol (clean_sairsiir ( params ) )


def generate_feature():
    temp_list=[ [ ] , [ [ ] , [ ] ] , [ [ ] , [ ] ] , [ [ ] , [ ] ] ]
    tur=" "
    satir_sayisi = random.randint (MIN_SATIR_SAYISI,MAX_SATIR_SAYISI)
    kita_sayisi,kelime_sayisi=0,0
    if random.random() <=0.5:#kıtalı olsun
        tur ="kitali"
        kita_sayisi = random.randint(MIN_KITA_SAYISI,MAX_KITA_SAYISI)
        
    else:#kıtasız olsun
        tur="kitasiz"
        #kita_sayisi baslangıcta 0 old.dan tekrar 0 yapmadık

    if random.random() <= 0.5: # kelime sayıları random olmasın,sabit olsun
        kelime_sayisi=random.randint(MIN_KELIME_SAYISI,MAX_KELIME_SAYISI)


    temp_list[0] = tur
    temp_list[1][0] , temp_list[1][1] = kita_sayisi , satir_sayisi

    temp_list[2][0] = kelime_sayisi
    
    #Su an için randomda uyak ve şiir-şair seçme yok ama eklenebilir
    temp_list[2][1] = ""
    return temp_list

def featurecontrol(param):
    
    params=param
        
    if params[1][0] == sys.maxsize:
        
        params[1][0] = 1 #kıtasız oldugu için 
    elif params[1][0] < MIN_KITA_SAYISI:
        params[1][0] = MIN_KITA_SAYISI
    elif params[1][0] > MAX_KITA_SAYISI:
        params[1][0] = MAX_KITA_SAYISI
    
    
    if params[1][1] < MIN_SATIR_SAYISI:
        params[1][1] = MIN_SATIR_SAYISI 
    elif params[1][1] > MAX_SATIR_SAYISI:
        params[1][1] = MAX_SATIR_SAYISI

    if params[2][0] == sys.maxsize:
        params[2][0] = 0
    elif params[2][0] < MIN_KELIME_SAYISI:
        params[2][0] = MIN_KELIME_SAYISI
    elif params[2][0] > MAX_KELIME_SAYISI:
        params[2][0] = MAX_KELIME_SAYISI

    if not params[3]: #boşsa
        params[3]= [ [ ] , [ ] ]
    

    return params

def clean_sairsiir(param): # idleri alır,isimleri siler
    cleaning_siir , cleaning_sair = [ ] , [ ]
    for i in param[3][0]:
        
        cleaning_siir.append( i [ 0 ] )
    for i in param[3][1]:
        
        cleaning_sair.append( i [ 0 ] )
    param[3] = [ cleaning_sair , cleaning_siir ]
    return param

def siiruret():
    
    siir=[]
    uyak = feature_list [ 2 ] [ 1 ]
    satir_sayisi = feature_list [ 1 ][ 1 ]
    kita_sayisi = feature_list [ 1 ][ 0 ]
    kelime_sayisi = feature_list [ 2 ][ 0 ]
    siirs,sairs = feature_list [ 3 ]
    satir=SatirUretici(uyak,sairs,siirs)

    if kita_sayisi == 0:
        kita_sayisi =1 
    for i in range (kita_sayisi):
        for i in range (satir_sayisi):
            
            siir.append( satir.uret(kelime_sayisi)  )
        siir.append("\n")
    return siir
        
            
    
    
