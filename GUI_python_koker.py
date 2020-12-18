import math
import configparser
import atexit
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import *
from PIL import Image, ImageTk
from tkinter import scrolledtext 
from tkinter import ttk 
import tkinter as tk
import os.path
import time
from ttkSimpleDialog import ttkSimpleDialog


config = configparser.ConfigParser()
config.read('Instellingen.ini')
grid_breedte = 20             #definier de grid groote 
grid_hoogte = 26   
eenheid = "lengte"   
titel = "(gegenereerde cnc code)"  
Cnc_code =""
global res_lengte
global max_D
global afwijking
global canvas_lengte
global foto_zichtbaarheid
global F_zichtbaarheid
res_lengte = 1.1111111111
max_D = float(config['Instellingen']['max_lengte'])
afwijking = float(config['Instellingen']['afwijking'])
canvas_lengte = 3500
foto_zichtbaarheid = int(config['Instellingen']['foto_zichtbaarheid'])
boolCNC_zichtbaarheid = int(config['Instellingen']['boolCNC_zichtbaarheid'])

GROOT_FONT= ("Verdana", 12)
NORM_FONT= ("Verdana", 10)
KLEIN_FONT= ("Verdana", 8)

# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is een class van de tkinter module. (see Lib/tkinter/__init__)
class Window(Frame):

    def __init__(self, master=None):
        
        Frame.__init__(self, master)   

        # refereer naar de master widget en dat is de tk window              
        self.master = master

        self.init_window()

    #Creation of init_window
    def init_window(self):
        def rad_select():
            global afwijking
            afwijking += var.get()
            afw1 = "afwijking ("+ str(afwijking) +")"
            afw2 = "afwijking ("+ str(afwijking) +")"
            print(afwijking)
            menu.entryconfigure(1, label=afw1)
            menu.entryconfigure(1, label=afw2)
        def handmatig():
            global afwijking
            afwijking = ttkSimpleDialog.askinteger("handmatig invullen","vul de afwijking in:")
            print (afwijking)
            afw3 = "afwijking ("+ str(afwijking) +")" 
            menu.entryconfigure(1, label=afw3)
        def max_lengte():
            global max_D
            max_D = ttkSimpleDialog.askinteger("maxiamale lengte aangeven","vul de maximale lengte in:")
            print(max_D)
        def F_zichtbaarheid():
            global foto_zichtbaarheid
            if foto_zichtbaarheid == 1:
                label.grid_remove()
                foto_zichtbaarheid = 0

            elif foto_zichtbaarheid == 0:
                label.grid(column=12, row=3, rowspan=21, sticky='wens')
                foto_zichtbaarheid = 1
            else :
                pass

        def CNC_zichtbaarheid():
            global boolCNC_zichtbaarheid
            if boolCNC_zichtbaarheid == 1:
                lbl_CNC.grid_remove()
                frame.grid_remove()
                boolCNC_zichtbaarheid = 0
                
            elif boolCNC_zichtbaarheid == 0:
                lbl_CNC.grid(column=15, row=5, columnspan= 2, sticky = "w")
                frame.grid(row=6, column=15, rowspan=20, columnspan=5, sticky = "w")
                canvas.pack(side=LEFT,expand=True,fill=BOTH)
                boolCNC_zichtbaarheid = 1
            else :
                pass
        #de titel van het programma      
        self.master.title("Hertel-kokerprogramma")
        #laat de widget gebruik maken van de hele breedte van de root window
        self.grid()
        # maakt een nieuwe menu instance
        global var
        var = IntVar()
        menu = Menu(self.master)
        
        self.master.config(menu=menu)
        filemenu = Menu(menu, tearoff=0)
        filemenu.add_command(label="afwijking")
        filemenu.add_separator()
        filemenu.add_radiobutton(label="afwijking +1", command = rad_select, variable=var, value= 1)
        filemenu.add_radiobutton(label="afwijking -1", command = rad_select, variable=var, value= -1)
        filemenu.add_command(label="handmatig instellen", command = handmatig)
        menu.add_cascade(label="instellingen", menu=filemenu)
        filemenu.add_separator()
        filemenu.add_command(label="andere instellingen")
        filemenu.add_command(label="Maximale lengte",command = max_lengte)
        filemenu.add_separator()
        filemenu.add_command(label="scherm indeling")
        filemenu.add_command(label="verberg / weergeven foto",command = F_zichtbaarheid)
        filemenu.add_command(label="verberg / weergeven CNC code",command = CNC_zichtbaarheid)
        self.frames = {}

root = Tk()
#---------------tab-bladen-------------------------------------------------------------------------------------------------------------------------------------
tabControl = ttk.Notebook(root)

tab1 = tk.Frame(tabControl, background ='#f2f2f2') 
tab2 = tk.Frame(tabControl, background ='#f2f2f2')
  
tabControl.add(tab1, text ='Invoer 1') 
tabControl.add(tab2, text ='Invoer 2') 
tabControl.grid(row= 0, column= 0, sticky='nesw', rowspan=26 , columnspan=10 )
#----------------defines----------------------------------------------------------------------------------------------------------------------------------------
def btn_switchclicked():
    global eenheid                                          #maak van eenheid een global zadat deze in deze methode veranderd word en buiten de functie gebruikt kan worden
    global D                                                        
    temp =  txt_D.get()
    D = float(temp)
    if lbl_D.cget("text") == str("D         Lengte plaat"):                 #als de eenheid lengte is dan word het diameter en omgekeerd
        eenheid = str("diameter")                                           #eenheid word gebruikt om ze kiezen tussen 2 berekeningen 
    elif lbl_D.cget("text") == str("D         Diameter koker"):   
        eenheid = str("lengte")
    else:
        pass
    if eenheid == str("diameter"):                        
        lbl_D.configure(text="D         Diameter koker")
        lbl_nk.configure(text="nk       Aantal kokers")
        print(D)
        D = (D * math.pi)
        print(D)
    elif eenheid == str("lengte"):
        lbl_D.configure(text="D         Lengte plaat")
        lbl_nk.configure(text="nk       Aantal platen")
    else:
        pass
    btn_berekenclicked() 

def btn_berekenclicked():
    str_n_Boven = ""
    str_n_Onder = ""
    global max_D
    global res_lengte
    res_lengte = 1.1111111111
    value1 =  txt_nk.get()                  #pak alle ingevoerde waardes en stop ze in variabele
    value2 =  txt_B.get()                   
    value3 =  txt_D.get()
    value4 =  txt_SX.get()
    value5 =  txt_C.get()
    value6 =  txt_Ov1.get()
    value7 =  txt_Ov2.get()
    value8 =  txt_RGb.get()
    value9 =  txt_RGo.get()
    value10 = txt_n.get()
    value11 = txt_Dg.get()
    value12 = txt_E.get()
    value13 = txt_G.get()
    value14 = txt_DDH.get()

    global nk
    global B
    global D
    global sx 
    global C 
    global Ov1
    global Ov2
    global RGb
    global RGo
    global n
    global Dg
    global E
    global G
    global DDH
    global F_Lu
    global F_Lut
    global F_Nx
    global F_Dx
    global F_Lg
    global F_Vg
    global n_Onder
    global n_Boven
    global Lg_O
    global Lg_B
    global VgB
    global VgO
    global canvas_lengte
    
    try:
        nk = int(value1)                      #maak een float van de strings die ingevoerd worden zodat er mee gerekend kan worden
        B = float(value2)
        D = float(value3)
        sx = float(value4)
        C = float(value5)
        Ov1 = float(value6)
        Ov2 = float(value7)
        RGb = float(value8)
        RGo = float(value9)
        n = int(value10)
        Dg = float(value11)
        E = float(value12)
        G = int(value13)
        DDH = float(value14)
    except:
        messagebox.showinfo('error','er is/zijn 1 of meerdere waarde(s) niet ondersteund')
    

    if B > 1000:
        messagebox.showinfo('error','breedte kan niet groter zijn dan 1000')             #dit zijn een paar checks of de getallen die ingevoerd worden                                                                         
    else:                                                                               #wel gebruikt kunnen worden en geeft de gebruiker een bericht terug wat er fout ging
      pass
    
    if n <= 1 :
        messagebox.showinfo('error','het aantal gaten moet minimaal 2 zijn!')
    else:
        pass

    if eenheid == "diameter":
        D = round((D * math.pi))
        print(D)
    else:
        pass

    if (C > Ov2 - 5 - (Dg /2)) or (-C >= D - 5 - (Dg /2)):                                  
        messagebox.showinfo('error','dat gaten zijn te dicht bij de rand')                  
    else: 
      pass

    if (nk * D) > max_D:
        messagebox.showinfo('error','de lengte van de plaat is te lang') 
        D = 0
    else:
        pass

    if nk > 1:
        canvas_lengte = 3500 * nk
        canvas.configure(scrollregion=(0,0,600,canvas_lengte))
    else:
        pass


    F_Lu = D
    F_Lut = (D + Ov1 + Ov2 )
    F_Nx = math.ceil((F_Lut / sx))
    F_Dx = F_Lut / math.ceil(F_Nx)
    F_Lg = (B - RGb - RGo) / (n-1)
    F_Vg = C /(n-1)
    if E != 0:
        Deler = B / E
        temp_n_Onder = n / Deler
        temp_n_Boven = n - temp_n_Onder
        n_Onder = round(temp_n_Onder)
        n_Boven = round(temp_n_Boven)
        Lg_O = (E - RGb - RGo) / (n_Onder-1)
        Lg_B = (B - E - RGb - RGo) / (n_Boven-1)
        str_n_Boven = str(n_Boven)
        str_n_Onder = str(n_Onder)
        VgB = C / (n_Boven - 1) 
        VgO = C / (n_Onder - 1)
    else:
        pass
    Lu = str(F_Lu)                                    #verander de floats terug in strings zodat ze terug kunnen worden gezet in de txt boxen
    Lut = str(F_Lut)    
    Nx = str(F_Nx)
    Dx = str(F_Dx)
    Lg = str(F_Lg)
    Vg = str(F_Vg)
    res_Lu = "Lu Uitslag tussen de gaten    " + Lu + " mm" #dit zet de uitgerekende waardes in een variabele en zet het in het bestemde txt vak
    lbl_Lu.configure(text= res_Lu)
    res_Lut = "Lut Totale uitslag   " + Lut + " mm"
    lbl_Lut.configure(text= res_Lut)
    res_Nx = "Nx aantal tang overnames  " + Nx + " X"
    lbl_Nx.configure(text= res_Nx)
    res_Dx = "Dx X maat overnames   " + Dx + " mm"
    lbl_Dx.configure(text= res_Dx)

    res_Lg = "Lg Afstand tussen de gaten    " + Lg + " mm"
    lbl_Lg.configure(text= res_Lg)

    res_Vg = "Vg Verloop per gat    " + Vg + " mm"
    lbl_Vg.configure(text= res_Vg)
    res_nB = "nB aantal gaten boven    " + str_n_Boven + " X"
    lbl_nB.configure(text= res_nB)
    res_nO = "nO aantal gaten onder    " + str_n_Onder + " X"
    lbl_nO.configure(text= res_nO)

def define_grid(width, height):
    rows = 0                                                  #geeft alle cellen in de grid een gewicht van 1 zodat deze zichtbaar
    columns = 0                                               # "leeg" zijn en dus niet alle text vakken tegen elkaar staan
    while rows < height:
         root.rowconfigure(rows, weight=1)
         rows += 1

    while columns < width:
         root.columnconfigure(columns, weight=1)
         columns += 1
    
    rows = 0                                                  #geeft alle cellen in de grid van tab1 een gewicht van 1 zodat deze zichtbaar zijn 
    columns = 0 
    while rows < height:
         tab1.rowconfigure(rows, weight=1)
         rows += 1

    while columns < width:
         tab1.columnconfigure(columns, weight=1)
         columns += 1

    rows = 0                                                  #geeft alle cellen in de grid van tab2 een gewicht van 1 zodat deze zichtbaar zijn
    columns = 0 
    while rows < height:
         tab2.rowconfigure(rows, weight=1)
         rows += 1

    while columns < width:
         tab2.columnconfigure(columns, weight=1)
         columns += 1
           
def btn_GenereerCodeclicked():
    global einde
    global Cnc_code
    global D
    global sx 
    global drain
    drain = ""
    Cnc_code = ''
    try:
        GrootteSlagXas()
        if hele_D  == sx:           #als sx gelijk is aan hele_D dan voer dit uit anders sla het over want dan is het al berekend in MeerdereSnijvlakken() zie GrootteSlagXas()
            Breette_plaat()
            FuncitieDoorsnijden()
            if var5.get() == 1 and E == 0:     #als er een drain hole moet zijn doe dan Drain_hole()
                Drain_hole()
            elif var5.get() == 1 and E != 0:
                messagebox.showinfo('error','er kan geen drain hole gesneden worden met een E > 0!')
            else:
                pass
        else:
            pass
        einde ="M16\nG00 X0.0 Y50.0 \nM990 (doorsnijden plaat)\n"
        if res_lengte != 1.1111111111:
            Aantal_Her_Msnij()
        else:
            Aantal_Herhalingen()
        Cnc_code += "M30  (einde programma)\n"
        canvas.itemconfig(canvas_id, text= Cnc_code)


        value4 =  txt_SX.get()
        sx = float(value4)

    except:
        messagebox.showinfo('Error!','Bereken eerst de berekende waarden!')
    else:
        pass

def btn_BestandOpslaanclicked():
    try:
        if txt_bestandsnaam.get()+".CNC" == ".CNC":
            messagebox.showinfo('Error!','Geef het bestand een naam!')    
        else:
            filenaam = txt_bestandsnaam.get()+".CNC"    
            completeName = os.path.join(path, filenaam)
            file1 = open(completeName, "w+")
            try:         
                file1.write(Cnc_code)
            except:
                messagebox.showinfo('Error!','Er ging iets mis ')
            finally:
                file1.close()
    except:
        messagebox.showinfo('Error!','Vul eerst de bestands locatie in, rechts boven in uw scherm!')
    else:
        pass

def OpenFile(event):
    global path
    path = askdirectory(initialdir="\\10.31.64.9\Lasercutter1",
                           title = "kies een bestand."
                           )
    print (path)
    txt_locatie.delete(0,"end")
    txt_locatie.insert(END, path)

def Breette_plaat():
    global grootte
    grootte =""
    Vboven = 0
    if B < 1000:
        Vboven = B + afwijking
        str_Vboven = str(Vboven)
        grootte ="G00 X0 Y"+str_Vboven +"\nM21  (laser aan)\nG91  (relatieve positionering)\nG01 X-"+str_sx +"Y0\nM20  (laser uit)\nM16\nG90  (absolute positionering)\n"
    elif B == 1000:
        grootte =""
    else:
        pass 

def GrootteSlagXas():
    global str_sx
    global hele_D
    global sx
    temp = txt_SX.get()
    temp2 = float(temp)
    sx = temp2
    str_sx = str(sx) 
    hele_D = float (D + Ov1 + Ov2)
    #----------------------------------ckeck de lengte -----------------------------------------------------------------------------------------------------------------------------------       
    if hele_D  < sx and hele_D > 0:            #als de lengte(Diameter + overslag 1 en 2) kleiner is dan de slag van de x as dan word de lengte van de plaat de slag van de x as
        str_sx = str(hele_D)
        sx = float(str_sx)
    elif hele_D  == sx:                   #als die hetzlefde is varanderd er niets 
        pass
    elif hele_D > sx:                
        MeerdereSnijvlakken()
    else:
        messagebox.showinfo('error','lengte of diameter + overslag 1 en2 kan geen - getal zijn')

def FuncitieDoorsnijden():
    global doorsnijden 
    temp = txt_E.get()
    E = float(temp)
    #-----------------------------------------------#check of de plaat moet worden doorgesneden------------------------------------------------------------------------------------------
    if E == 0:                                      #als E(lengte koker) 0 is hoeft die niet worden doorgesneden 
        doorsnijden = ""
    elif E > 0 and E < 1000:
        E += afwijking
        doorsnijden = "G00 X0.0 Y" +str(E) +"\nG91  (relatieve positionering)\nM21  (laser aan)\nG01 X-" +str_sx +" Y0.0\nM20  (laser uit)\nM16\nG90  (absolute positionering)\n"
    else:
        messagebox.showinfo('error','lengte koker waar de plaat doorgesneden moet worden kan geen - getal zijn en niet groter dan 999') 

def snijgaten():
    global gaatjes
    global gaatjes_binnen_sx    
    global n_Onder
    global n_Boven                       
    gaatjes = ""
    gaatjes_binnen_sx = ""
    temp = txt_n.get()
    n = float(temp)
    temp2 = txt_RGo.get()
    temp3 = float(temp2)
    RGo = temp3 + afwijking
    str_RGo = str(RGo)
    gat_num = 2
    temp_sx = float(str_sx) 
    new_xcord = (temp_sx - Ov1)
    new_ycord = (RGo + F_Lg)
    if E != 0:
        new_xcordO = (temp_sx - Ov1)
        new_ycordO = (RGo + Lg_O)
        new_xcordB = (temp_sx - Ov1)         
        new_ycordB = (RGo + E + Lg_B)        
        #-------------------------------------------variabelen eerste gat grootte koker =! 0----------------------------------------------------------------------------------------------------------        
        XE_gatOnder = temp_sx - Ov1
        YE_gatOnder = RGo
        XE_gatBoven = temp_sx - Ov1
        YE_gatBoven = RGo + E
        EO_straal = XE_gatOnder + (Dg / 2)
        EB_straal = XE_gatBoven + (Dg / 2)
        AXE_gatBoven  = round(XE_gatBoven, 3)
        AYE_gatBoven = round(YE_gatBoven, 3)
        AXE_gatOnder = round(XE_gatOnder, 3)
        AYE_gatOnder = round(YE_gatOnder, 3)
        AEO_straal = round(EO_straal, 3)
        AEB_straal = round(EB_straal, 3)
        str_FB_xcord = str(AXE_gatBoven)
        str_FB_ycord = str(AYE_gatBoven)
        str_FO_xcord = str(AXE_gatOnder)
        str_FO_ycord = str(AYE_gatOnder)
        str_EO_straal = str(AEO_straal)
        str_EB_straal = str(AEB_straal)
    else:
        pass
    straal = Dg / 2
    str_straal = str(straal)
    #-------------------------------------------variabelen eerste gat----------------------------------------------------------------------------------------------------------    
    first_xcord = round((temp_sx - Ov1),3)
    first_ycord = round(RGo, 3)
    first_xcord_straal = round(first_xcord + (Dg / 2), 3)
    str_first_xcord_straal = str(first_xcord_straal)
    str_first_xcord = str(first_xcord)
    str_first_ycord = str(first_ycord)
    if E == 0:
        gaatjes_binnen_sx = "(gat1)\nG00 X- "+str_first_xcord +" Y "+str_RGo +"\nM21  (Laser aan)\nG01 X-"+str_first_xcord_straal +" Y "+str_first_ycord +"\nG03 X-"+str_first_xcord_straal +" Y "+str_first_ycord+" I "+str_straal+" J 0.0\nM20  (Laser uit)\nM16\n"
        gaatjes ="(gat1)\nG00 X- "+str_first_xcord +" Y "+str_RGo +"\nM21  (Laser aan)\nG01 X-"+str_first_xcord_straal +" Y "+str_first_ycord +"\nG03 X-"+str_first_xcord_straal +" Y "+str_first_ycord+" I "+str_straal+" J 0.0\nM20  (Laser uit)\nM16\n"
        if var1.get() == 1:
            new_xcord -= F_Vg
        elif var2.get() == 1:
            new_xcord -= F_Vg
        else:
            pass
        if hele_D  == sx:
            if (Var3.get() == 1) and (Var4.get() == 0):
                gaatjes_binnen_sx = ""
            elif (Var3.get() == 0) and (Var4.get() == 0):
                gaatjes_binnen_sx = ""
            else:
                while n > 1:                                                #gaten links
                    str_gat_num = str(gat_num)
                    new_ycord = round(new_ycord, 3)
                    new_xcord = round(new_xcord, 3)
                    xcord_straal = round(new_xcord + (Dg / 2),3)
                    str_xcord_straal = str(xcord_straal)
                    str_new_xcord = str(new_xcord)
                    str_new_ycord = str(new_ycord)
                    gaatjes_binnen_sx +="(gat"+str_gat_num +")\nG00 X- "+str_new_xcord +" Y "+str_new_ycord +"\nM21  (Laser aan)\nG01 X-"+str_xcord_straal +" Y "+str_new_ycord +"\nG03 X-"+str_xcord_straal +" Y "+str_new_ycord+" I "+str_straal+" J 0.0\nM20  (Laser uit)\nM16\n"
                    new_xcord = float(str_new_xcord)
                    new_ycord = float(str_new_ycord)
                    xcord_straal = float(str_xcord_straal)
                    n -= 1
                    gat_num = float(str_gat_num)
                    gat_num += 1
                    new_ycord += F_Lg
                    if var1.get() == 1:
                        new_xcord -= F_Vg    
                    elif var2.get() == 1:
                        new_xcord -= F_Vg
                    else:
                        pass
            if (Var3.get() == 0) and (Var4.get() == 1):                  #als alleen gaten alleen gaten links is aangevinkt dus recht moeten weg
                pass
            elif (Var3.get() == 0) and (Var4.get() == 0):
                pass
            else:        
                temp = txt_n.get()
                n = float(temp)
                str_RGo = str(RGo)
                gat_num = 2
                temp_sx = float(str_sx) 
                new_xcord = (Ov2)
                new_ycord = (RGo + F_Lg)
                straal = Dg / 2
                str_straal = str(straal)
                first_xcord = (Ov2)
                first_ycord = RGo
                first_xcord_straal = first_xcord + (Dg / 2)
                first_xcord_straal = new_xcord + (Dg / 2)
                str_first_xcord_straal = str(first_xcord_straal)
                str_first_xcord = str(first_xcord)
                str_first_ycord = str(first_ycord)
                gaatjes_binnen_sx += "(gat1)\nG00 X- "+str_first_xcord +" Y "+str_RGo +"\nM21  (Laser aan)\nG01 X-"+str_first_xcord_straal +" Y "+str_first_ycord +"\nG03 X-"+str_first_xcord_straal +" Y "+str_first_ycord+" I "+str_straal+" J 0.0\nM20  (Laser uit)\nM16\n"
                if var1.get() == 1:
                     new_xcord -= F_Vg
                elif var2.get() == 1:
                    new_xcord += F_Vg
                else:
                    pass
                
                while n > 1:                                                                    # laatste gaatjes als alles binnen 1 tangoverpak past
                    str_gat_num = str(gat_num)
                    new_ycord = round(new_ycord, 3)
                    new_xcord = round(new_xcord, 3)
                    xcord_straal = round(new_xcord + (Dg / 2),3)
                    str_xcord_straal = str(xcord_straal)
                    str_new_xcord = str(new_xcord)
                    str_new_ycord = str(new_ycord)
                    gaatjes_binnen_sx +="(gat"+str_gat_num +")\nG00 X- "+str_new_xcord +" Y "+str_new_ycord +"\nM21  (Laser aan)\nG01 X-"+str_xcord_straal +" Y "+str_new_ycord +"\nG03 X-"+str_xcord_straal +" Y "+str_new_ycord+" I "+str_straal+" J 0.0\nM20  (Laser uit)\nM16\n"
                    new_xcord = float(str_new_xcord)
                    new_ycord = float(str_new_ycord)
                    xcord_straal = float(str_xcord_straal)
                    n -= 1
                    gat_num = float(str_gat_num)
                    gat_num += 1
                    new_ycord += F_Lg
                    if var1.get() == 1:
                        new_xcord -= F_Vg    
                    elif var2.get() == 1:
                        new_xcord += F_Vg
                    else:
                        pass
        #--------------------------------------eerste gaten als er meerdere tangoverpakken zijn------------------------------------------------------------------------------
        else:                                                                                           
            while n > 1:
                str_gat_num = str(gat_num)
                new_ycord = round(new_ycord, 3)
                new_xcord = round(new_xcord, 3)
                xcord_straal = round(new_xcord + (Dg / 2),3)
                str_xcord_straal = str(xcord_straal)
                str_new_xcord = str(new_xcord)
                str_new_ycord = str(new_ycord)
                gaatjes +="(gat"+str_gat_num +")\nG00 X- "+str_new_xcord +" Y "+str_new_ycord +"\nM21  (Laser aan)\nG01 X-"+str_xcord_straal +" Y "+str_new_ycord +"\nG03 X-"+str_xcord_straal +" Y "+str_new_ycord+" I "+str_straal+" J 0.0\nM20  (Laser uit)\nM16\n"
                new_xcord = float(str_new_xcord)
                new_ycord = float(str_new_ycord)
                xcord_straal = float(str_xcord_straal)
                n -= 1
                gat_num = float(str_gat_num)
                gat_num += 1
                new_ycord += F_Lg
                if (var1.get() == 1) or (var2.get() == 1):
                    new_xcord -= F_Vg
                else:
                    pass
    #---------------------------------als E geen 0 is en dus de plaat gedeeld word in 2 platen------------------------------------------------------------------------------------    
    elif E > 0:
        gaatjes_binnen_sx = "(gaten onderste deel)\n(gat1)\nG00 X- "+str_FO_xcord +" Y "+str_FO_ycord +"\nM21  (Laser aan)\nG01 X-"+str_EO_straal +" Y "+str_FO_ycord +"\nG03 X-"+str_EO_straal +" Y "+str_FO_ycord +" I "+str_straal+" J 0.0\nM20  (Laser uit)\nM16\n"
        gaatjes = "(gaten onderste deel)\n(gat1)\nG00 X- "+str_FO_xcord +" Y "+str_FO_ycord +"\nM21  (Laser aan)\nG01 X-"+str_EO_straal +" Y "+str_FO_ycord +"\nG03 X-"+str_EO_straal +" Y "+str_FO_ycord +" I "+str_straal+" J 0.0\nM20  (Laser uit)\nM16\n"
        if var1.get() == 1:
            new_xcordO -= VgO
        elif var2.get() == 1:
            new_xcordO -= VgO
        else:
            pass
        
        if hele_D  == sx:
            if (Var3.get() == 1) and (Var4.get() == 0):
                gaatjes_binnen_sx = ""
            elif (Var3.get() == 0) and (Var4.get() == 0):
                gaatjes_binnen_sx = ""
            else:
                while n_Onder > 1:                                                #gaten links onder
                    str_gat_num = str(gat_num)
                    new_ycordO = round(new_ycordO, 3)
                    new_xcordO = round(new_xcordO, 3)
                    new_xcordO_straal = round(new_xcordO + (Dg / 2),3)
                    str_xcordO_straal = str(new_xcordO_straal)
                    str_new_xcordO = str(new_xcordO)
                    str_new_ycordO = str(new_ycordO)
                    gaatjes_binnen_sx +="(gat"+str_gat_num +")\nG00 X- "+str_new_xcordO +" Y "+str_new_ycordO +"\nM21  (Laser aan)\nG01 X-"+str_xcordO_straal +" Y "+str_new_ycordO +"\nG03 X-"+str_xcordO_straal +" Y "+str_new_ycordO+" I "+str_straal+" J 0.0\nM20  (Laser uit)\nM16\n"
                    new_xcordO = float(str_new_xcordO)
                    new_ycordO = float(str_new_ycordO)
                    xcordO_straal = float(str_xcordO_straal)
                    n_Onder -= 1
                    gat_num = float(str_gat_num)
                    gat_num += 1
                    new_ycordO += Lg_O
                    if var1.get() == 1:
                        new_xcordO -= VgO    
                    elif var2.get() == 1:
                        new_xcordO -= VgO
                    else:
                        pass
                    
                str_gat_num = str(gat_num)
                gaatjes_binnen_sx += "(gaten bovenste deel)\n(gat"+str_gat_num +")\nG00 X- "+str_FB_xcord +" Y "+str_FB_ycord +"\nM21  (Laser aan)\nG01 X-"+str_EB_straal +" Y "+str_FB_ycord +"\nG03 X-"+str_EB_straal +" Y "+str_FB_ycord +" I "+str_straal+" J 0.0\nM20  (Laser uit)\nM16\n"
                gat_num = float(str_gat_num)
                gat_num += 1
                if var1.get() == 1:
                    new_xcordB -= VgB    
                elif var2.get() == 1:
                    new_xcordB -= VgB
                else:
                    pass
                
                while n_Boven > 1:                                                #gaten linksv boven
                    str_gat_num = str(gat_num)
                    new_ycordB = round(new_ycordB, 3)
                    new_xcordB = round(new_xcordB, 3)
                    new_xcordB_straal = round(new_xcordB + (Dg / 2),3)
                    str_xcordB_straal = str(new_xcordB_straal)
                    str_new_xcordB = str(new_xcordB)
                    str_new_ycordB = str(new_ycordB)
                    gaatjes_binnen_sx +="(gat"+str_gat_num +")\nG00 X- "+str_new_xcordB +" Y "+str_new_ycordB +"\nM21  (Laser aan)\nG01 X-"+str_xcordB_straal +" Y "+str_new_ycordB +"\nG03 X-"+str_xcordB_straal +" Y "+str_new_ycordB+" I "+str_straal+" J 0.0\nM20  (Laser uit)\nM16\n"
                    new_xcordB = float(str_new_xcordB)
                    new_ycordB = float(str_new_ycordB)
                    new_xcordB_straal = float(str_xcordB_straal)
                    n_Boven -= 1
                    gat_num = float(str_gat_num)
                    gat_num += 1
                    new_ycordB += Lg_B
                    if var1.get() == 1:
                        new_xcordB -= VgB    
                    elif var2.get() == 1:
                        new_xcordB -= VgB
                    else:
                        pass
            if (Var3.get() == 0) and (Var4.get() == 1) :      #als alleen gaten alleen gaten links is aangevinkt
                pass
            elif (Var3.get() == 0) and (Var4.get() == 0):
                pass
            else:        
                temp = txt_n.get()
                n = float(temp)
                Deler = B / E
                temp_n_Onder = n / Deler
                temp_n_Boven = n - temp_n_Onder
                n_Onder = round(temp_n_Onder)
                n_Boven = round(temp_n_Boven)
                str_RGo = str(RGo)
                gat_num = 2
                temp_sx = float(str_sx) 
                new_xcordO = (Ov2)
                new_xcordB = (Ov2)
                new_ycordO = (RGo + Lg_O)
                new_ycordB = (RGo + Lg_B + E)
                first_xcordO = (Ov2)
                first_ycordO = RGo
                first_xcordO_straal = first_xcordO + (Dg / 2)
                first_xcordO_straal = new_xcordO + (Dg / 2)
                str_first_xcordO_straal = str(first_xcordO_straal)
                str_first_xcordO = str(first_xcordO)
                str_first_ycordO = str(first_ycordO)
                first_xcordB = (Ov2)
                first_ycordB = (RGo + E)
                first_xcordB_straal = first_xcordB + (Dg / 2)
                first_xcordB_straal = new_xcordB + (Dg / 2)
                str_first_xcordB_straal = str(first_xcordB_straal)
                str_first_xcordB = str(first_xcordB)
                str_first_ycordB = str(first_ycordB)
                gaatjes_binnen_sx += "(gaten onderste deel)\n(gat1)\nG00 X- "+str_first_xcordO +" Y "+str_first_ycordO +"\nM21  (Laser aan)\nG01 X-"+str_first_xcordO_straal +" Y "+str_first_ycordO +"\nG03 X-"+str_first_xcordO_straal +" Y "+str_first_ycordO+" I "+str_straal+" J 0.0\nM20  (Laser uit)\nM16\n"
                if var1.get() == 1:
                     new_xcordO += VgO
                elif var2.get() == 1:
                    new_xcordO += VgO
                else:
                    pass
                
                while n_Onder > 1:                                                                    # laatste gaatjes als alles binnen 1 tangoverpak past
                    str_gat_num = str(gat_num)
                    new_ycordO = round(new_ycordO, 3)
                    new_xcordO = round(new_xcordO, 3)
                    xcordO_straal = round(new_xcordO + (Dg / 2),3)
                    str_xcordO_straal = str(xcordO_straal)
                    str_new_xcordO = str(new_xcordO)
                    str_new_ycordO = str(new_ycordO)
                    gaatjes_binnen_sx +="(gat"+str_gat_num +")\nG00 X- "+str_new_xcordO +" Y "+str_new_ycordO +"\nM21  (Laser aan)\nG01 X-"+str_xcordO_straal +" Y "+str_new_ycordO +"\nG03 X-"+str_xcordO_straal +" Y "+str_new_ycordO+" I "+str_straal+" J 0.0\nM20  (Laser uit)\nM16\n"
                    new_xcordO = float(str_new_xcordO)
                    new_ycordO = float(str_new_ycordO)
                    xcordO_straal = float(str_xcordO_straal)
                    n_Onder -= 1
                    gat_num = float(str_gat_num)
                    gat_num += 1
                    new_ycordO += Lg_O
                    if var1.get() == 1:
                        new_xcordO += VgO    
                    elif var2.get() == 1:
                        new_xcordO += VgO
                    else:
                        pass
                    
                    
                str_gat_num = str(gat_num)
                gaatjes_binnen_sx += "(gaten bovenste deel)\n(gat"+str_gat_num +")\nG00 X- "+str_first_xcordB +" Y "+str_first_ycordB +"\nM21  (Laser aan)\nG01 X-"+str_first_xcordB_straal +" Y "+str_first_ycordB +"\nG03 X-"+str_first_xcordB_straal +" Y "+str_first_ycordB+" I "+str_straal+" J 0.0\nM20  (Laser uit)\nM16\n"
                gat_num = float(str_gat_num)
                gat_num += 1
                if var1.get() == 1:
                     new_xcordB += VgB
                elif var2.get() == 1:
                    new_xcordB += VgB
                else:
                    pass
                while n_Boven > 1:                                                #gaten links boven
                    str_gat_num = str(gat_num)
                    new_ycordB = round(new_ycordB, 3)
                    new_xcordB = round(new_xcordB, 3)
                    new_xcordB_straal = new_xcordB + (Dg / 2)
                    str_xcordB_straal = str(new_xcordB_straal)
                    str_new_xcordB = str(new_xcordB)
                    str_new_ycordB = str(new_ycordB)
                    gaatjes_binnen_sx +="(gat"+str_gat_num +")\nG00 X- "+str_new_xcordB +" Y "+str_new_ycordB +"\nM21  (Laser aan)\nG01 X-"+str_xcordB_straal +" Y "+str_new_ycordB +"\nG03 X-"+str_xcordB_straal +" Y "+str_new_ycordB+" I "+str_straal+" J 0.0\nM20  (Laser uit)\nM16\n"
                    new_xcordB = float(str_new_xcordB)
                    new_ycordB = float(str_new_ycordB)
                    new_xcordB_straal = float(str_xcordB_straal)
                    n_Boven -= 1
                    gat_num = float(str_gat_num)
                    gat_num += 1
                    new_ycordB += Lg_B
                    if var1.get() == 1:
                        new_xcordB += VgB    
                    elif var2.get() == 1:
                        new_xcordB += VgB
                    else:
                        pass
        #-------------------------------------------------------eerste gaten als er meerdere tangoverpakken zijn------------------------------------------------------------------------------
        else:                                                                                         
            while n_Onder > 1:                                                #gaten links onder
                str_gat_num = str(gat_num)
                new_ycordO = round(new_ycordO, 3)
                new_xcordO = round(new_xcordO, 3)
                new_xcordO_straal = new_xcordO + (Dg / 2)
                str_xcordO_straal = str(new_xcordO_straal)
                str_new_xcordO = str(new_xcordO)
                str_new_ycordO = str(new_ycordO)
                gaatjes +="(gat"+str_gat_num +")\nG00 X- "+str_new_xcordO +" Y "+str_new_ycordO +"\nM21  (Laser aan)\nG01 X-"+str_xcordO_straal +" Y "+str_new_ycordO +"\nG03 X-"+str_xcordO_straal +" Y "+str_new_ycordO+" I "+str_straal+" J 0.0\nM20  (Laser uit)\nM16\n"
                new_xcordO = float(str_new_xcordO)
                new_ycordO = float(str_new_ycordO)
                xcordO_straal = float(str_xcordO_straal)
                n_Onder -= 1
                gat_num = float(str_gat_num)
                gat_num += 1
                new_ycordO += Lg_O
                if var1.get() == 1:
                    new_xcordO -= VgO    
                elif var2.get() == 1:
                    new_xcordO -= VgO
                else:
                    pass
                
            str_gat_num = str(gat_num)
            gaatjes += "(gaten bovenste deel)\n(gat"+str_gat_num +")\nG00 X- "+str_FB_xcord +" Y "+str_FB_ycord +"\nM21  (Laser aan)\nG01 X-"+str_EB_straal +" Y "+str_FB_ycord +"\nG03 X-"+str_EB_straal +" Y "+str_FB_ycord +" I "+str_straal+" J 0.0\nM20  (Laser uit)\nM16\n"
            gat_num = float(str_gat_num)
            gat_num += 1
            if var1.get() == 1:
                new_xcordB -= VgB    
            elif var2.get() == 1:
                new_xcordB -= VgB
            else:
                pass
            while n_Boven > 1:                                                #gaten links boven
                str_gat_num = str(gat_num)
                new_ycordB = round(new_ycordB, 3)
                new_xcordB = round(new_xcordB, 3)
                new_xcordB_straal = new_xcordB + (Dg / 2)
                str_xcordB_straal = str(new_xcordB_straal)
                str_new_xcordB = str(new_xcordB)
                str_new_ycordB = str(new_ycordB)
                gaatjes +="(gat"+str_gat_num +")\nG00 X- "+str_new_xcordB +" Y "+str_new_ycordB +"\nM21  (Laser aan)\nG01 X-"+str_xcordB_straal +" Y "+str_new_ycordB +"\nG03 X-"+str_xcordB_straal +" Y "+str_new_ycordB+" I "+str_straal+" J 0.0\nM20  (Laser uit)\nM16\n"
                new_xcordB = float(str_new_xcordB)
                new_ycordB = float(str_new_ycordB)
                xcordB_straal = float(str_xcordB_straal)
                n_Boven -= 1
                gat_num = float(str_gat_num)
                gat_num += 1
                new_ycordB += Lg_B
                if var1.get() == 1:
                    new_xcordB -= VgB    
                elif var2.get() == 1:
                    new_xcordB -= VgB
                else:
                    pass
    else:
        pass

def laatstesnijgaten():
    global laatstegaatjes
    laatstegaatjes = ""
    temp = txt_n.get()
    n = float(temp)
    temp2 = txt_RGo.get()
    temp3 = float(temp2)
    RGo = temp3 + afwijking
    str_RGo = str(RGo)
    gat_num = 2
    temp_sx = float(str_sx) 
    new_xcord = (Ov2)
    new_ycord = round((RGo + F_Lg),3)
    straal = round((Dg / 2) ,3)
    str_straal = str(straal)
    first_xcord = (Ov2)
    first_ycord = RGo
    first_xcord_straal = round(first_xcord + (Dg / 2),3)
    first_xcord_straal = round(new_xcord + (Dg / 2),3)
    str_first_xcord_straal = str(first_xcord_straal)
    str_first_xcord = str(first_xcord)
    str_first_ycord = str(first_ycord)
    if E == 0:
        laatstegaatjes ="(gat1)\nG00 X- "+str_first_xcord +" Y "+str_RGo +"\nM21  (Laser aan)\nG01 X-"+str_first_xcord_straal +" Y "+str_first_ycord +"\nG03 X-"+str_first_xcord_straal +" Y "+str_first_ycord+" I "+str_straal+" J 0.0\nM20  (Laser uit)\nM16\n"
        if (var1.get() == 0) or (var2.get() ==1):
            new_xcord += F_Vg
        else:
            pass
        
        while n > 1:
            str_gat_num = str(gat_num)
            new_ycord = round(new_ycord, 3)
            new_xcord = round(new_xcord, 3)
            xcord_straal = round(new_xcord + (Dg / 2),3)
            str_xcord_straal = str(xcord_straal)
            str_new_xcord = str(new_xcord)
            str_new_ycord = str(new_ycord)
            laatstegaatjes +="(gat"+str_gat_num +")\nG00 X- "+str_new_xcord +" Y "+str_new_ycord +"\nM21  (Laser aan)\nG01 X-"+str_xcord_straal +" Y "+str_new_ycord +"\nG03 X-"+str_xcord_straal +" Y "+str_new_ycord+" I "+str_straal+" J 0.0\nM20  (Laser uit)\nM16\n"
            new_xcord = float(str_new_xcord)
            new_ycord = float(str_new_ycord)
            xcord_straal = float(str_xcord_straal)
            n -= 1
            gat_num = float(str_gat_num)
            gat_num += 1
            new_ycord += F_Lg
            if (var1.get() == 0) or (var2.get == 1):
                new_xcord += F_Vg
            else:
                pass
            
    elif E > 0:
        temp = txt_n.get()
        n = float(temp)
        Deler = B / E
        temp_n_Onder = n / Deler
        temp_n_Boven = n - temp_n_Onder
        n_Onder = round(temp_n_Onder)
        n_Boven = round(temp_n_Boven)
        str_RGo = str(RGo)
        gat_num = 2
        temp_sx = float(str_sx) 
        new_xcordO = (Ov2)
        new_xcordB = (Ov2)
        new_ycordO = round((RGo + Lg_O),3)
        new_ycordB = round((RGo + Lg_B + E),3)
        first_xcordO = (Ov2)
        first_ycordO = RGo
        first_xcordO_straal = first_xcordO + (Dg / 2)
        first_xcordO_straal = new_xcordO + (Dg / 2)
        str_first_xcordO_straal = str(first_xcordO_straal)
        str_first_xcordO = str(first_xcordO)
        str_first_ycordO = str(first_ycordO)
        first_xcordB = (Ov2)
        first_ycordB = (RGo + E)
        first_xcordB_straal = first_xcordB + (Dg / 2)
        first_xcordB_straal = new_xcordB + (Dg / 2)
        str_first_xcordB_straal = str(first_xcordB_straal)
        str_first_xcordB = str(first_xcordB)
        str_first_ycordB = str(first_ycordB)
        laatstegaatjes += "(gaten onderste deel)\n(gat1)\nG00 X- "+str_first_xcordO +" Y "+str_first_ycordO +"\nM21  (Laser aan)\nG01 X-"+str_first_xcordO_straal +" Y "+str_first_ycordO +"\nG03 X-"+str_first_xcordO_straal +" Y "+str_first_ycordO+" I "+str_straal+" J 0.0\nM20  (Laser uit)\nM16\n"
        if (var1.get() == 0) or (var2.get() ==1):
            new_xcordO += VgO
        else:
            pass
        
        while n_Onder > 1:                                                                    # laatste gaatjes als alles binnen 1 tangoverpak past
            str_gat_num = str(gat_num)
            new_ycordO = round(new_ycordO, 3)
            new_xcordO = round(new_xcordO, 3)
            xcordO_straal = new_xcordO + (Dg / 2)
            str_xcordO_straal = str(xcordO_straal)
            str_new_xcordO = str(new_xcordO)
            str_new_ycordO = str(new_ycordO)
            laatstegaatjes +="(gat"+str_gat_num +")\nG00 X- "+str_new_xcordO +" Y "+str_new_ycordO +"\nM21  (Laser aan)\nG01 X-"+str_xcordO_straal +" Y "+str_new_ycordO +"\nG03 X-"+str_xcordO_straal +" Y "+str_new_ycordO+" I "+str_straal+" J 0.0\nM20  (Laser uit)\nM16\n"
            new_xcordO = float(str_new_xcordO)
            new_ycordO = float(str_new_ycordO)
            xcordO_straal = float(str_xcordO_straal)
            n_Onder -= 1
            gat_num = float(str_gat_num)
            gat_num += 1
            new_ycordO += Lg_O
            if var1.get() == 0:
                new_xcordO += VgO 
            elif var2.get() == 1:
                new_xcordO += VgO
            else:
                pass
            
            
        str_gat_num = str(gat_num)
        laatstegaatjes += "(gaten bovenste deel)\n(gat"+str_gat_num+")\nG00 X- "+str_first_xcordB +" Y "+str_first_ycordB +"\nM21  (Laser aan)\nG01 X-"+str_first_xcordB_straal +" Y "+str_first_ycordB +"\nG03 X-"+str_first_xcordB_straal +" Y "+str_first_ycordB+" I "+str_straal+" J 0.0\nM20  (Laser uit)\nM16\n"
        gat_num = float(str_gat_num)
        gat_num += 1
        if var1.get() == 0:
            new_xcordB += VgB    
        elif var2.get() == 1:
            new_xcordB += VgB
        else:
            pass
        while n_Boven > 1:                                                #gaten linksv boven   #TO DO
            str_gat_num = str(gat_num)
            new_ycordB = round(new_ycordB, 3)
            new_xcordB = round(new_xcordB, 3)
            new_xcordB_straal = new_xcordB + (Dg / 2)
            str_xcordB_straal = str(new_xcordB_straal)
            str_new_xcordB = str(new_xcordB)
            str_new_ycordB = str(new_ycordB)
            laatstegaatjes +="(gat"+str_gat_num +")\nG00 X- "+str_new_xcordB +" Y "+str_new_ycordB +"\nM21  (Laser aan)\nG01 X-"+str_xcordB_straal +" Y "+str_new_ycordB +"\nG03 X-"+str_xcordB_straal +" Y "+str_new_ycordB+" I "+str_straal+" J 0.0\nM20  (Laser uit)\nM16\n"
            new_xcordB = float(str_new_xcordB)
            new_ycordB = float(str_new_ycordB)
            new_xcordB_straal = float(str_xcordB_straal)
            n_Boven -= 1
            gat_num = float(str_gat_num)
            gat_num += 1
            new_ycordB += Lg_B
            if var1.get() == 0:
                new_xcordB += VgB    
            elif var2.get() == 1:
                new_xcordB += VgB
            else:
                pass
            
    else:
        pass 

def Aantal_Her_Msnij():
    global Cnc_code
    global nk
    global gaatjes
    start ="G90(absolute positionering)\nG17\nM16\nM11"
    k = 1 
    code = ""
    Cnc_code = ""
    str_k  = str(k)                                #groote x as
    if nk > 1:
        while nk >= 1:
            aanhang ="(koker"+str_k +")\n"
            code = aanhang +start +midden +laatste +einde
            Cnc_code += code
            nk -= 1
            int_k = int(str_k)
            int_k += 1 
            str_k = str(int_k)
    elif nk == 1:
            aanhang ="(koker1)\n"
            code = aanhang +start +midden +laatste +einde
            Cnc_code += code
    else:
        messagebox.showinfo('error','aantal platen/kokers moet groter zijn dan 0') 

def Aantal_Herhalingen():
    global Cnc_code
    global nk
    global gaatjes_binnen_sx
    global drain
    code = ""
    start ="G90(absolute positionering)\nG17\nM16\nM11  (Tang los)\nG00 X-"+str_sx+"Y 0.0\nM10  (Tang vast)\n"
    k = 1 
    Cnc_code = ""
    str_k  = str(k)    
    if nk > 1: 
        snijgaten()                                 
        while nk >= 1:
            aanhang ="(koker"+str_k +")\n"
            code = aanhang +start +gaatjes_binnen_sx +drain +grootte +doorsnijden +einde
            Cnc_code += code
            nk -= 1
            int_k = int(str_k)
            int_k += 1 
            str_k = str(int_k)
    elif nk == 1:
            snijgaten()
            aanhang ="(koker1)\n"   
            code = aanhang +start +gaatjes_binnen_sx +drain +grootte +doorsnijden +einde
            Cnc_code += code
    else:
        messagebox.showinfo('error','aantal platen/kokers moet groter zijn dan 0') 

def MeerdereSnijvlakken():
    global tangoverpak
    global midden
    global laatste
    global res_lengte
    global str_sx
    global laatstegaatjes
    global gaatjes
    global drain
    global EPositie
    EPositie = 0                  #Eind positie
    temp_D = D / 360 * G + Ov2
    Gekozen_D = round(temp_D, 3)
    TEPositie = Gekozen_D         #Temp Eind positie
    HPositie = 0                  #huidige positie
    VPositie = sx                 #volgende positie

    res_lengte = hele_D
    midden = ""
    temp =""
    laatste = ""
    gaatjes = ""
    laatstegaatjes =""
    drain = ""
    str_sx = str(sx)
    while res_lengte > sx:
        Breette_plaat()
        FuncitieDoorsnijden()
        if res_lengte == hele_D:
            snijgaten()   
            if (Var3.get() == 1) and (Var4.get() == 0):
                gaatjes = ""
                tangoverpak ="(TangOverpak)\n(overname1)\nG00 X0.0 Y0.0\nM11  (Tang los) \nG00 X-" +str_sx +" Y0.0\nM10 (Tang vast)\nM16\n"
                temp = tangoverpak +"(segment)\n"+gaatjes +grootte +doorsnijden
                midden += temp
                res_lengte -= sx
            elif (Var3.get() == 0) and (Var4.get() == 0):
                gaatjes = ""
                tangoverpak ="(TangOverpak)\n(overname1)\nG00 X0.0 Y0.0\nM11  (Tang los) \nG00 X-" +str_sx +" Y0.0\nM10 (Tang vast)\nM16\n"
                temp = tangoverpak +"(segment)\n"+gaatjes +grootte +doorsnijden
                midden += temp
                res_lengte -= sx
            else:
                tangoverpak ="(TangOverpak)\n(overname1)\nG00 X0.0 Y0.0\nM11  (Tang los) \nG00 X-" +str_sx +" Y0.0\nM10 (Tang vast)\nM16\n"
                temp = tangoverpak +"(segment)\n"+gaatjes +grootte +doorsnijden
                midden += temp
                res_lengte -= sx
            
            if (var5.get() == 1) and (Gekozen_D > HPositie) and (Gekozen_D < VPositie) and E == 0:
                EPositie = round(TEPositie, 3)
                Drain_hole()
                midden += drain
            elif (var5.get() == 1) and (Gekozen_D > HPositie) and (Gekozen_D < VPositie) and E != 0:
                messagebox.showinfo('error','er kan geen drain hole gesneden worden met een E > 0!')
            elif ((var5.get() == 1) and (Gekozen_D == HPositie)) or ((Gekozen_D == VPositie) and (var5.get() == 1)):
                messagebox.showinfo('Error!','het drain hole valt precies op een tangoverpak, verander sx naar (oude sx +- diameter drain hole + 5)!')
            else:
                TEPositie -= sx

            HPositie += sx
            VPositie += sx

        else:
            tangoverpak ="(TangOverpak)\n(overname1)\nG00 X0.0 Y0.0\nM11  (Tang los) \nG00 X-" +str_sx +" Y0.0\nM10 (Tang vast)\nM16\n"
            temp = tangoverpak +"(segment)\n" +grootte +doorsnijden 
            midden += temp
            res_lengte -= sx
            
            if (var5.get() == 1) and (Gekozen_D > HPositie) and (Gekozen_D < VPositie) and E == 0:
                EPositie = round(TEPositie, 3)
                Drain_hole()
                midden += drain
            elif (var5.get() == 1) and (Gekozen_D > HPositie) and (Gekozen_D < VPositie) and E != 0:
                messagebox.showinfo('error','er kan geen drain hole gesneden worden met een E > 0!')
            elif ((var5.get() == 1) and (Gekozen_D == HPositie)) or ((Gekozen_D == VPositie) and (var5.get() == 1)):
                messagebox.showinfo('Error!','het drain hole val precies op een tangoverpak, verander sx naar (oude sx +- diameter drain hole + 5)!')
            else:
                TEPositie -= sx
        
            HPositie += sx
            VPositie += sx


    if res_lengte <= sx and res_lengte > 0:
        if res_lengte <= 50:
            messagebox.showinfo('error','de laatste tangoverpak is kleiner dan 50\ndoordat (D - ((Nx -1) * SX)) < 50 \nverander de slag van de x as totdat deze melding niet meer terug komt')
        else:
            pass
        str_sx = str(res_lengte)  
        tangoverpak ="(TangOverpak)\n(overname1)\nG00 X0.0 Y0.0\nM11  (Tang los) \nG00 X-" +str_sx +" Y0.0\nM10 (Tang vast)\nM16\n"
        Breette_plaat()
        FuncitieDoorsnijden()
        laatstesnijgaten()
        if (Var3.get() == 0) and (Var4.get() == 1):
            laatstegaatjes = ""
        elif (Var3.get() == 0) and (Var4.get() == 0):
            laatstegaatjes = ""
        else:
            pass
        laatste = tangoverpak +"(segment)\n" +laatstegaatjes +grootte +doorsnijden
    else:
        pass

def Drain_hole():
    global drain
    RDH = DDH / 2
    str_RDH = str(RDH)
    drain = ""
    Halve_B = (B - RGo - RGb) / 2 + afwijking + RGo
    str_Halve_B = str(Halve_B)

    if res_lengte != 1.1111111111:
        print (EPositie)
        Xdrain = sx - EPositie
        str_XdrainPlusRDh = str(Xdrain + RDH)
        str_Xdrain = str(Xdrain)
        drain = "(Drain hole)\nG00 X- "+str_Xdrain +" Y "+str_Halve_B +"\nM21  (Laser aan)\nG01 X-"+str_XdrainPlusRDh +" Y "+str_Halve_B +"\nG03 X-"+str_XdrainPlusRDh +" Y "+str_Halve_B +" I "+str_RDH+" J 0.0\nM20  (Laser uit)\nM16\n"
    else:
        temp = D / 360 * G + Ov2
        Xdrain = round(temp, 3)
        str_Xdrain = str(Xdrain)
        str_XdrainPRDH = str(Xdrain + RDH)
        drain = "(Drain hole)\nG00 X- "+str_Xdrain +" Y "+str_Halve_B +"\nM21  (Laser aan)\nG01 X-"+str_XdrainPRDH +" Y "+str_Halve_B +"\nG03 X-"+str_XdrainPRDH +" Y "+str_Halve_B +" I "+str_RDH+" J 0.0\nM20  (Laser uit)\nM16\n"

def SaveHuidigeWaardes():
    try:
        config = configparser.ConfigParser()
        config['Entry'] = {  'nk': nk,
                             'B': B,
                             'D': D,
                             'SX': sx,
                             'C': C,
                             'Ov1': Ov1,
                             'Ov2': Ov2,
                             'RGb': RGo,
                             'RGo': RGb,
                             'n': n,
                             'Dg': Dg,
                             'E': E,
                             'G': G,
                             'DDH': DDH}

        config['Checkbutton'] = {  'ConischLinks': var1.get(),
                             'BeideConisch': var2.get(),
                             'GatenLinks': Var3.get(),
                             'GatenRechts': Var4.get(),
                             'Drain_Hole': 0 }


        config['Instellingen'] = { 'afwijking': afwijking,
                                'max_lengte': max_D,
                                'foto_zichtbaarheid': foto_zichtbaarheid,
                                'boolCNC_zichtbaarheid': boolCNC_zichtbaarheid}

        config['Opslaan'] = {'Locatie': path}

        with open('Instellingen.ini', 'w') as configfile:
          config.write(configfile)
    except:
        print("niet alle waardes zijn beschikbaar")
    
def Alleen_Nummers(char):
    return char.isdigit()


define_grid(grid_breedte,grid_hoogte)                      #lees Instellingen.ino

photo = PhotoImage(file="icon.png")                  #root window instellingen zoals iconfoto grootte van het programma  wanneer opgestart en de achtergronfd kleur   
root.iconphoto(False, photo)
root.geometry('1280x680')
root['bg'] = '#cccccc' 

IntValidation = tab1.register(Alleen_Nummers)        #zorgt evoor dat er alleen nummer in de entry box ingevoerd kan worden 

#-----------entry box tab1---------------------------------------------------------------------------------------------------------------------------
txt_nk = ttk.Entry(tab1,width=10, validate="key", validatecommand=(IntValidation, '%S'))               #dit zijn alle invoer boxen met een standard waarde die uit instellingen.ini gehaald wordt 
txt_nk.insert(END, config['Entry']['nk'])
txt_nk.grid(column=10, row=3)

txt_B = ttk.Entry(tab1,width=10)
txt_B.insert(END, config['Entry']['B'])
txt_B.grid(column=10, row=4)

txt_D = ttk.Entry(tab1,width=10)
txt_D.insert(END, config['Entry']['D'])
txt_D.grid(column=10, row=5)

txt_SX = ttk.Entry(tab1,width=10)
txt_SX.insert(END, config['Entry']['sx'])
txt_SX.grid(column=10, row=6)

txt_C = ttk.Entry(tab1,width=10)
txt_C.insert(END, config['Entry']['C'])
txt_C.grid(column=10, row=7)

txt_Ov1 = ttk.Entry(tab1,width=10)
txt_Ov1.insert(END, config['Entry']['Ov1'])
txt_Ov1.grid(column=10, row=8)

txt_Ov2 = ttk.Entry(tab1,width=10)
txt_Ov2.insert(END, config['Entry']['Ov2'])
txt_Ov2.grid(column=10, row=9)

txt_RGb = ttk.Entry(tab1,width=10)
txt_RGb.insert(END, config['Entry']['RGb'])
txt_RGb.grid(column=10, row=10)

txt_RGo = ttk.Entry(tab1,width=10)
txt_RGo.insert(END, config['Entry']['RGo'])
txt_RGo.grid(column=10, row=11)

txt_n = ttk.Entry(tab1,width=10, validate="key", validatecommand=(IntValidation, '%S'))
txt_n.insert(END, config['Entry']['n'])
txt_n.grid(column=10, row=12)

txt_Dg = ttk.Entry(tab1,width=10)
txt_Dg.insert(END, config['Entry']['Dg'])
txt_Dg.grid(column=10, row=13)

txt_E = ttk.Entry(tab1,width=10)
txt_E.insert(END, config['Entry']['E'])
txt_E.grid(column=10, row=14)

txt_bestandsnaam = ttk.Entry(tab1,width=30)
txt_bestandsnaam.insert(END, '')
txt_bestandsnaam.grid(column=5, row=15, sticky='w')

txt_locatie = ttk.Entry(tab1,width=30)
txt_locatie.insert(END, config['Opslaan']['locatie'])

txt_locatie.grid(column=5, row=16, sticky='w')
txt_locatie.bind("<1>", OpenFile)
#--------entry box tab2-------------------------------------------------------------------------------------------------------------------------
txt_G = ttk.Entry(tab2,width=10, validate="key", validatecommand=(IntValidation, '%S'))    
txt_G.insert(END, config['Entry']['G'])
txt_G.grid(column=10, row=2)

txt_DDH = ttk.Entry(tab2,width=10)               
txt_DDH.insert(END, config['Entry']['DDH'])
txt_DDH.grid(column=10, row=3)
#--------checkbox tab1--------------------------------------------------------------------------------------------------------------------------
var1 = tk.IntVar(value= config['Checkbutton']['ConischLinks'])
txt_CL = ttk.Checkbutton(tab1,text="conisch links?",variable=var1, onvalue=1, offvalue=0)
txt_CL.grid(column=5, row=7)

var2 = tk.IntVar(value= config['Checkbutton']['BeideConisch'])
txt_CB = ttk.Checkbutton(tab1,text="beide conisch?",variable=var2, onvalue=1, offvalue=0)
txt_CB.grid(column=6, row=7)

Var3 = tk.IntVar(value= config['Checkbutton']['GatenLinks'])
txt_GR = ttk.Checkbutton(tab1,text="gaten rechts?",variable=Var3, onvalue=1, offvalue=0)
txt_GR.grid(column=6, row=12)

Var4 = tk.IntVar(value= config['Checkbutton']['GatenRechts'])
txt_GL = ttk.Checkbutton(tab1,text="gaten links?",variable=Var4, onvalue=1, offvalue=0) 
txt_GL.grid(column=5, row=12)
#--------checkbox tab2--------------------------------------------------------------------------------------------------------------------------
var5 = tk.IntVar(value= config['Checkbutton']['Drain_Hole'])
txt_DH = ttk.Checkbutton(tab2,text="Drain hole?",variable=var5, onvalue=1, offvalue=0)
txt_DH.grid(column=7, row=2)
#------------------knoppen--------------------------------------------------------------------------------------------
style = ttk.Style()
style.configure("TButton", foreground="black", padding=6)

btn_Bereken = ttk.Button(tab1, text="bereken", command=btn_berekenclicked, cursor = "hand2", style ="TButton")   #knoppen met welke command ze aanroepen
btn_Bereken.grid(column=0, row=2)

btn_GenereerCode = ttk.Button(tab1, text="genereer code",command=btn_GenereerCodeclicked, cursor = "hand2", style ="TButton")
btn_GenereerCode.grid(column=0, row=4)

btn_switch = ttk.Button(tab1, text="switch van eenheid",command=btn_switchclicked, cursor = "hand2", style ="TButton")
btn_switch.grid(column=0, row=6)

btn_BestandOpslaan = ttk.Button(tab1, text="bestand opslaan",command=btn_BestandOpslaanclicked, cursor = "hand2", style ="TButton")
btn_BestandOpslaan.grid(column=0, row=15)
#-----------labels tab1----------------------------------------------------------------------------------------------------
lbl_in = ttk.Label(tab1, text="Invoer waarden", anchor='w', font=("Arial Bold", 18))
lbl_in.grid(column=4, row=2, sticky = "w")

lbl_nk = ttk.Label(tab1, text="nk       Aantal platen", anchor='w')
lbl_nk.grid(column=4, row=3, sticky = 'w')

lbl_B = ttk.Label(tab1, text="B         Breedte plaat", anchor='w')
lbl_B.grid(column=4, row=4, sticky = 'w')

lbl_D = ttk.Label(tab1, text="D         Lengte plaat", anchor='w')
lbl_D.grid(column=4, row=5, sticky = 'w')

lbl_SX = ttk.Label(tab1, text="SX       Slag van de X-as", anchor='w')
lbl_SX.grid(column=4, row=6, sticky = 'w')

lbl_C = ttk.Label(tab1, text="C        Conisch", anchor='w')
lbl_C.grid(column=4, row=7, sticky = 'w')

lbl_Ov1 = ttk.Label(tab1, text="Ov1    Overslag 1", anchor='w')
lbl_Ov1.grid(column=4, row=8, sticky = 'w')

lbl_Ov2 = ttk.Label(tab1, text="Ov2    Overslag 2", anchor='w')
lbl_Ov2.grid(column=4, row=9, sticky = 'w')

lbl_RGb = ttk.Label(tab1, text="RGb    Afstand rand - 1e gat boven", anchor='w')
lbl_RGb.grid(column=4, row=10, sticky = 'w')

lbl_RGo = ttk.Label(tab1, text="RGo    Afstand rand - 1e gat onder", anchor='w')
lbl_RGo.grid(column=4, row=11, sticky = 'w')

lbl_n = ttk.Label(tab1, text="n         Aantal gaten", anchor='w')
lbl_n.grid(column=4, row=12, sticky = 'w')

lbl_Dg = ttk.Label(tab1, text="Dg      Diameter gat", anchor='w')
lbl_Dg.grid(column=4, row=13, sticky = 'w')

lbl_E = ttk.Label(tab1, text="E       Grootte koker", anchor='w')
lbl_E.grid(column=4, row=14, sticky = 'w')

lbl_naam = tk.Label(tab1, text="Naam:", anchor='w')
lbl_naam.grid(column=4, row=15, sticky = 'w',)

lbl_locatie = tk.Label(tab1, text="Locatie:", anchor='w')
lbl_locatie.grid(column=4, row=16, sticky = 'w',)
#---------labels root---------------------------------------------------------------------------------------
lbl_CNC = tk.Label(root, text="Gegenereerde code", anchor='w', font=("Arial Bold", 18), bg='#cccccc')
if boolCNC_zichtbaarheid != 0:
    lbl_CNC.grid(column=15, row=5, columnspan= 2, sticky = "w")
else:
    pass
#---------labels tab2---------------------------------------------------------------------------------------
lbl_in2 = ttk.Label(tab2, text="Invoer waarden", anchor='w', font=("Arial Bold", 18))
lbl_in2.grid(column=4, row=1, sticky = "w")

lbl_G = ttk.Label(tab2, text="G       Positie drain hole in Graden ∠", anchor='w')
lbl_G.grid(column=4, row=2, sticky = 'w')

lbl_DDH = ttk.Label(tab2, text="DDH       Diameter drain hole ", anchor='w')
lbl_DDH.grid(column=4, row=3, sticky = 'w')

lbl_uit = ttk.Label(tab2, text="Berekende waarden", anchor='w', font=("Arial Bold", 18))
lbl_uit.grid(column=4, row=15, sticky = "w")

lbl_Lu = ttk.Label(tab2, text="Lu      Uitslag tussen de gaten ", anchor='w')
lbl_Lu.grid(column=4, row=16, sticky = 'w')

lbl_Lut = ttk.Label(tab2, text="Lut     Totale uitslag", anchor='w')
lbl_Lut.grid(column=4, row=17, sticky = 'w')

lbl_Nx = ttk.Label(tab2, text="Nx      Aantal tang overnames", anchor='w')
lbl_Nx.grid(column=4, row=18, sticky = 'w')

lbl_Dx = ttk.Label(tab2, text="Dx      X maat overnames", anchor='w')
lbl_Dx.grid(column=4, row=19, sticky = 'w')

lbl_Lg = ttk.Label(tab2, text="Lg      Afstand tussen de gaten", anchor='w')
lbl_Lg.grid(column=4, row=20, sticky = 'w', columnspan = 4)

lbl_Vg = ttk.Label(tab2, text="Vg      Verloop per gat", anchor='w')
lbl_Vg.grid(column=4, row=21, sticky = 'w', columnspan = 4)

lbl_nB = ttk.Label(tab2, text="nB      Aantal gaten bover", anchor='w')
lbl_nB.grid(column=4, row=22, sticky = 'w')

lbl_nO = ttk.Label(tab2, text="nO      Aantal gaten onder", anchor='w')
lbl_nO.grid(column=4, row=23, sticky = 'w')
#-----------------foto-----------------------------------------------------------------------------------------------------------------------------------
image = Image.open("foto.png")          #foto
photo = ImageTk.PhotoImage(image)
label = Label(root,image=photo,bg='#cccccc')
label.image = photo # this line need to prevent gc
if foto_zichtbaarheid != 0:
    label.grid(column=12, row=3, rowspan=21, sticky=W+E+N+S)
else:
    pass
#----------------canvas----------------------------------------------------------------------------------------------------------------------------------------
frame1=Frame(tab1,height=20)
frame1.grid(row=0, column=0, columnspan=20, rowspan = 2, sticky = "nesw")
canvas1=Canvas(frame1,bg='#b30000',height=20)
canvas_text = canvas1.create_text(15, 15, anchor="nw", font=("Courier", 16), fill='white')
canvas1.itemconfig(canvas_text, text="Nino André Leo Poppe, Altrad services Benelux ©")
canvas1.pack(side=LEFT,expand=True,fill=BOTH)

frame1=Frame(tab2,height=18)
frame1.grid(row=0, column=0, columnspan=20, rowspan = 1, sticky = "nesw")
canvas1=Canvas(frame1,bg='#b30000',height=18)
canvas_text = canvas1.create_text(15, 15, anchor="nw", font=("Courier", 16), fill='white')
canvas1.itemconfig(canvas_text, text="Nino André Leo Poppe, Altrad services Benelux ©")
canvas1.pack(side=LEFT,expand=True,fill=BOTH)

frame=Frame(root,width=400, height=600)
if boolCNC_zichtbaarheid != 0:
    frame.grid(row=6, column=15, rowspan=20, columnspan=5, sticky = "w")
else:
    pass
canvas=Canvas(frame,bg='#f2f2f2',width=400,height=600,scrollregion=(0,0,600,canvas_lengte))
hbar=Scrollbar(frame,orient=HORIZONTAL)
hbar.pack(side=BOTTOM,fill=X)
hbar.config(command=canvas.xview)
vbar=Scrollbar(frame,orient=VERTICAL)
vbar.pack(side=RIGHT,fill=Y)
canvas_id = canvas.create_text(10, 10, anchor="nw")
vbar.config(command=canvas.yview)
canvas.config(width=400,height=600)
canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
canvas.pack(side=LEFT,expand=True,fill=BOTH)
#-----------------------------------dit MOET worden uitgevoerd aan het einde van het programma----------------------------------------------------------------------------------------------------------------------------
atexit.register(SaveHuidigeWaardes)
#creation of an instance
app = Window(root)

#mainloop 
root.mainloop()  