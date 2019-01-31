import tkinter as tk
import sqlite3 as sql
import siirOlustur as sO
import veritabani as vt

import clipboard # pip install clipboard 
import sys

feature_list=[ [] , [] , [] , [ [ ] , [ ] ] ]

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class StartPage(tk.Frame):
    global feature_list
    def __init__(self, master):
        self.master=master
        tk.Frame.__init__(self, master)
        
        tk.Button(self, text="Rastgele Şiir Oluştur",
                  command=self.rasgele_siir).pack()
        tk.Button(self, text="Özelleştirilmiş Şiir Oluştur",
                  command=self.ozel_siir).pack()
    
    def rasgele_siir(self):

        feature_list[0]="random"
        
        self.master.switch_frame(SiirUret)
    def ozel_siir(self):
        
        self.master.switch_frame(OzelSiirSecFrame)


class OzelSiirSecFrame(tk.Frame):
    global feature_list        
    def __init__(self, master):
        self.master=master
        tk.Frame.__init__(self, master)
        tk.Button(self, text="Kıtalı Şiir Oluştur",
                  command=self.kitali_siir).pack()
        tk.Button(self, text="Kıtasız Şiir Oluştur",
                  command=self.kitasiz_siir).pack()

    def kitali_siir(self):
        
        feature_list[0] ="kitali"
        self.master.switch_frame(KitaliSiirSecFrame)
    def kitasiz_siir(self):
        
        feature_list[0] ="kitasiz"
        self.master.switch_frame(KitasizSiirSecFrame)
#------
class KitaliSiirSecFrame(tk.Frame):
    global feature_list
    def __init__(self, master):
        self.master=master
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Kıta sayısı:").pack(side="top", fill="x")
        self.kita_sayisi=tk.Entry(self)
        self.kita_sayisi.pack(pady=10)
        tk.Label(self, text="Her Kıtadaki Satır sayısı:").pack(side="top", fill="x",)
        self.satir_sayisi=tk.Entry(self)
        self.satir_sayisi.pack(pady=10)

        tk.Button(self, text="Sonraki Aşamaya Geç",bg="red",
                  command=self.sonraki_asama).pack(pady=10)
        self.bilgiText=tk.Label(self, state=tk.DISABLED,fg="red")
        self.bilgiText.pack()
        

    def sonraki_asama(self):
        
        if self.kita_sayisi.get().isnumeric() and self.satir_sayisi.get().isnumeric():
            feature_list[1] =list(  (  int(self.kita_sayisi.get()) , int(self.satir_sayisi.get())  ) )
            self.master.switch_frame(KelimeSayisiSecFrame)  
        else:
            if self.kita_sayisi.get()== "" or self.satir_sayisi.get()== "" :
                self.bilgiText["state" ]="normal"
                self.bilgiText["text" ]="Bos alan bırakmayınız!"
            else:
                self.bilgiText["state" ]="normal"
                self.bilgiText["text" ]="Sadece sayisal deger girilebilir!"
        
        
 #------
class KitasizSiirSecFrame(tk.Frame):
    global feature_list
    def __init__(self, master):
        self.master=master
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Satır sayısı:").pack(side="top", fill="x",)
        self.satir_sayisi=tk.Entry(self)
        self.satir_sayisi.pack(pady=10)

        tk.Button(self, text="Sonraki Aşamaya Geç",bg="red",
                  command=self.sonraki_asama).pack(pady=10)
        self.bilgiText=tk.Label(self, state=tk.DISABLED,fg="red")
        self.bilgiText.pack()
        

    def sonraki_asama(self):
        
        if  self.satir_sayisi.get().isnumeric():
            
            feature_list[1] =list(  (  sys.maxsize , int(self.satir_sayisi.get())  ) )
            self.master.switch_frame(KelimeSayisiSecFrame) 
        else:
            if  self.satir_sayisi.get()== "" :
                self.bilgiText["state" ]="normal"
                self.bilgiText["text" ]="Bos alan bırakmayınız!"
            else:
                
                self.bilgiText["state" ]="normal"
                self.bilgiText["text" ]="Sadece sayisal deger girilebilir!"


class KelimeSayisiSecFrame(tk.Frame):
    global feature_list
    def __init__(self, master):
        self.master=master
        self.v=tk.IntVar()
        self.w=tk.IntVar()
        self.w.set(3)
        self.v.set(1)
        tk.Frame.__init__(self, master)
        tk.Radiobutton(self, text="kelime sayısı rastgele olsun",variable=self.v,value=1,
                  command=lambda:self.radio_event(1)).pack()
        
        tk.Radiobutton(self, text="Kelime Sayısı her satırda belli olsun",variable=self.v,value=2,
                  command=lambda:self.radio_event(2)).pack()
        self.lbl=tk.Label(self, text="Kelime Sayısı:",state=tk.DISABLED)
        self.lbl.pack()
        self.kelime_sayisi=tk.Entry(self,state=tk.DISABLED)
        self.kelime_sayisi.pack()

        tk.Radiobutton(self, text="Uyak olmasın",variable=self.w,value=3,
                  command=lambda:self.radio_event(3)).pack()
        
        tk.Radiobutton(self, text="Uyak olsun",variable=self.w,value=4,
                  command=lambda:self.radio_event(4)).pack()        
        self.lbl2=tk.Label(self, text="Uyak harfleri:",state=tk.DISABLED)
        self.lbl2.pack()
        self.uyak=tk.Entry(self,state=tk.DISABLED)
        self.uyak.pack()
        
        tk.Button(self, text="Sonraki Aşamaya Geç",bg="red",
                  command=self.sonraki_asama).pack(pady=10)
        self.bilgiText=tk.Label(self, state=tk.DISABLED,fg="red")
        self.bilgiText.pack()

    def sonraki_asama(self):
        if   (   ( self.v.get() == 2 and self.kelime_sayisi.get().isnumeric()   )  or   (  self.v.get() == 1   )  )  and (   (   self.w.get() == 4 and self.uyak.get().isalpha()  )  or  (  self.w.get() == 3  )   ):       
            
            par1,par2=sys.maxsize,""
            if self.v.get() != 1:
                par1=int(self.kelime_sayisi.get())
            if self.w.get != 3:
                par2=self.uyak.get()
                feature_list[2]=list ( ( par1,par2 ) )
            self.master.switch_frame(SairSiirSecFrame) 
        else:
            if  self.v.get() == 2 and self.kelime_sayisi.get()=="" :
                self.bilgiText["state" ]="normal"
                self.bilgiText["text" ]="Kelime sayisi alanını Bos bırakmayınız!"
                
            elif  self.v.get() == 2 and not self.kelime_sayisi.get().isnumeric() :
                self.bilgiText["state" ]="normal"
                self.bilgiText["text" ]="Kelime sayısı alanına sayısal değer giriniz!"
            elif self.w.get() == 4 and self.uyak.get() == "":
                self.bilgiText["state" ]="normal"
                self.bilgiText["text" ]="uyak alanını Bos bırakmayınız!"
            elif self.w.get() == 4 and not self.uyak.get().isalpha():
                self.bilgiText["state" ]="normal"
                self.bilgiText["text" ]="uyak alanına sadece harf girilebilir!"
        

    def radio_event(self,who):
        if who == 2:
            self.lbl["state" ]="normal"
            self.kelime_sayisi["state"]="normal"
        elif who == 1:
            self.lbl["state" ]=tk.DISABLED
            self.kelime_sayisi["state"]=tk.DISABLED
        elif who == 3:
            self.lbl2["state" ]=tk.DISABLED
            self.uyak["state"]=tk.DISABLED
        elif who == 4:
            self.lbl2["state" ]="normal"
            self.uyak["state"]="normal"
        
class SairSiirSecFrame(tk.Frame):
    global feature_list
    def __init__(self, master):
        self.selected_sair=""
        self.selected_siir=""
        self.selected_siir_id=0
        self.selected_sair_id=0
        

        self.eklenensairliste=[]
        self.eklenensiirliste=[]

        
        self.master=master
        self.v=tk.IntVar()
        self.v.set(1)
        self.siirliste=[ ]
        self.sairliste=vt.tumsairlerigetir()
        
        
        tk.Frame.__init__(self, master)
        tk.Radiobutton(self, text="Şiiri rasgele şair ve şiirlerden oluştur",variable=self.v,value=1,
                  command=lambda:self.radio_event(1)).pack()
        
        tk.Radiobutton(self, text="Şiiri seçilen şair ve şiirlerden oluştur",variable=self.v,value=2,
                  command=lambda:self.radio_event(2)).pack()
        self.sairekle=tk.Button(self, text="Şair Seç:",command=self.sairsec,state=tk.DISABLED)
        self.sairekle.pack()
        self.siirekle=tk.Button(self, text="ŞiirSeç:",command=self.siirsec,state=tk.DISABLED,pady=5)
        self.siirekle.pack()
        
        self.siirolustur=tk.Button(self, text="Şiiri Oluştur:",command=self.siirolustur,pady=5)
        self.siirolustur.pack()
        
        self.eklenenlerlabel=tk.Label(self, text="",state=tk.DISABLED)
        self.eklenenlerlabel.pack()

    def siirolustur(self):
        
        if self.v.get() == 1:
            
            self.master.switch_frame(SiirUret)
        elif self.v.get() == 2:
            feature_list[3]= list(  ( self.eklenensairliste ,  self.eklenensiirliste )  )
            self.master.switch_frame(SiirUret)
        

    def radio_event(self,who):
        if who == 2:
            self.sairekle["state" ]="normal"
            self.siirekle["state"]="normal"
            self.eklenenlerlabel["state"]="normal"
        elif who == 1:
            self.sairekle["state" ]=tk.DISABLED
            self.siirekle["state"]=tk.DISABLED
            self.eklenenlerlabel["state"]=tk.DISABLED
    
#--------------------------------------------------------------------------
    def sairsec(self):
        
        top=tk.Toplevel()
        top.title("Şair Seç")
        top.geometry("550x630+0+0")
        top.resizable(False,False)

        lbl=tk.Label(top,text="",state=tk.DISABLED)
        lbl.place(x=225,y=540,width=100,height=20)

        btn=tk.Button(top,text="Ekle",command=self.sairiekle,bg="red",state=tk.DISABLED)
        btn.place(x=235,y=570,width=100,height=40)
        
        listbox=tk.Listbox(top)
        listbox.bind("<<ListboxSelect>>",lambda x:self.listboxselect(listbox,btn))
        listbox.place(x=10,y=30,width=500,height=500)



        scrollbar=tk.Scrollbar(listbox)
        scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        
        for i in self.sairliste:
            listbox.insert(tk.END,i[1])

        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        

    def listboxselect(self,listbox,btn):
                
        selection=listbox.curselection()
        picked=listbox.get(selection[0])
        self.selected_sair=picked

        
        
        
        btn["state"]="normal"

    def sairiekle(self):
        num=0
        for i in self.eklenensairliste:
            if i[1] == self.selected_sair:
                self.selected_sair = ""
                
                return
        for i in self.sairliste:
            if i[1] == self.selected_sair:
                num=i[0]
                self.eklenensairliste.append( (num,self.selected_sair ) )
                self.eklenenlerlabel["text"]=self.eklenenlerlabel["text"] + "(  {}  )".format(self.selected_sair)
                self.selected_sair = ""
                break
                
        
#--------------------------------------------------------------------------        
    def siirsec(self):
        
        top=tk.Toplevel()
        top.title("Şiir Seç")
        top.geometry("550x630+0+0")
        top.resizable(False,False)

        


        lbl=tk.Label(top,text="sairler")
        lbl.place(x=100,y=15,width=100,height=15)

        lbl2=tk.Label(top,text="siirler")
        lbl2.place(x=350,y=15,width=100,height=15)

        btn=tk.Button(top,text="Ekle",bg="red",command=self.siiriekle,state=tk.DISABLED)
        btn.place(x=235,y=570,width=100,height=40)

        listboxsiir=tk.Listbox(top)
        listboxsiir.bind("<<ListboxSelect>>",lambda x:self.listboxsiirselect(listboxsiir,btn))
        listboxsiir.place(x=280,y=30,width=250,height=500)
        
        listboxsair=tk.Listbox(top)
        listboxsair.bind("<<ListboxSelect>>",lambda x:self.listboxsairselect(listboxsair,btn,listboxsiir))
        listboxsair.place(x=10,y=30,width=250,height=500)



        scrollbar=tk.Scrollbar(listboxsair)
        scrollbar.pack(side=tk.RIGHT,fill=tk.Y)

        scrollbar2=tk.Scrollbar(listboxsiir)
        scrollbar2.pack(side=tk.RIGHT,fill=tk.Y)
        
        for i in self.sairliste:
            listboxsair.insert(tk.END,i[1])
            



        listboxsiir.config(yscrollcommand=scrollbar2.set)
        scrollbar2.config(command=listboxsiir.yview)
        listboxsiir["state"]="normal"
        listboxsair.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listboxsair.yview)
        
             

    def listboxsairselect(self,listbox,btn,listboxdisabled):
        try:
            selection=listbox.curselection()
            picked=listbox.get(selection[0])
            self.selected_sair=picked
        except:
            return
        btn["state"]=tk.DISABLED
        for i in self.sairliste:
            if i[1] == self.selected_sair:
                self.selected_sair_id=i[0]   
                break

        self.siirliste=vt.sairinsiirlerinigetir(self.selected_sair_id)
        
        try:    
            for i in range(listboxdisabled.size()-1,-1,-1):
                listboxdisabled.delete(i)
        except:
            pass

        for i in self.siirliste:
            
            listboxdisabled.insert(tk.END,i[1])
        
    def listboxsiirselect(self,listbox,btn):
        try:
            
            selection=listbox.curselection()
            picked=listbox.get(selection[0])
            btn["state"]="normal"
            self.selected_siir=picked
            
        except:
            return
        

    def siiriekle(self):
        num=0
        for i in self.eklenensiirliste:
            if i[1] == self.selected_siir:
                self.selected_sair = ""
                
                return
        for i in self.siirliste:
            if i[1] == self.selected_siir:
                num=i[0]
                self.eklenensiirliste.append( (num,self.selected_siir ) )
                self.eklenenlerlabel["text"]=self.eklenenlerlabel["text"] +"( {} [ {} ])".format(self.selected_sair,self.selected_siir)
                self.selected_sair = ""
                self.selected_siir = ""
                break     


class SiirUret(tk.Frame):
    def __init__(self, master):
        self.master=master
        tk.Frame.__init__(self, master)
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack( side = tk.RIGHT, fill="y" )

        sO.setparams(feature_list)
        self.siir=sO.siiruret()
        for i in self.siir:
            print(i)

            
        area = tk.Text(self, yscrollcommand = scrollbar.set, background = 'black',
                    foreground = 'green', font = ('Courier New', 11), insertbackground = 'yellow', insertwidth = 5, selectbackground = 'red' )
        area.pack(side="top", fill="x", pady=50)
        area.insert(tk.END,"\n".join(self.siir) )
        scrollbar.config(command = area.yview)
        
        tk.Button(self, text="Şiiri kopyala",bg="red",
                command=self.copy).pack(pady=10)  
        tk.Button(self, text="Sonraki Aşamaya Geç",bg="red",
                  command=self.sonraki_asama).pack(pady=10)
        
        

    def sonraki_asama(self):
            self.master.switch_frame(StartPage)

    def copy(self):
            clipboard.copy("\n".join(self.siir))
        



if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
