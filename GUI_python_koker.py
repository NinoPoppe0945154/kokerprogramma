import math
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfile 
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename

#----------------window instellingen-----------------------------------------------------------------------------------------------
window = Tk()
window.title("Hertel-kokerprogramma")
window.geometry('1280x680')
#---------------variables------------------------------------------------------------------------------------------------------------------------------------
grid_breedte = 50                 #verander de grid groote 
grid_hoogte = 50   
eenheid = "lengte"   
titel = "(gegenereerde cnc code)"  
Cnc_code =""
global res_lengte
res_lengte = 1.1111111111
#----------------defines----------------------------------------------------------------------------------------------------------------------------------------
def btn_switchclicked():
    global eenheid                                                          #maak van eenheid een global zadat deze in deze methode veranderd word en buiten de functie gebruikt kan worden
    if lbl_D.cget("text") == str("D         Lengte plaat"):                 #als de eenheid lengte is dan word het diameter en omgekeerd
        eenheid = str("diameter")                         #eenheid word gebruikt om ze kiezen tussen 2 berekeningen 
    
    elif lbl_D.cget("text") == str("D         Diameter koker"):   
       eenheid = str("lengte")
    
    else:
        pass

    if eenheid == str("diameter"):                        
        lbl_D.configure(text="D         Diameter koker")
        lbl_nk.configure(text="nk       Aantal kokers")
   
    elif eenheid == str("lengte"):
        lbl_D.configure(text="D         Lengte plaat")
        lbl_nk.configure(text="nk       Aantal platen")
    
    else:
        pass
    btn_berekenclicked() 

def btn_berekenclicked():

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
    global F_Lu
    global F_Lut
    global F_Nx
    global F_Dx
    global F_Lg
    global F_Vg


    nk = float(value1)                      #maak een float van de strings die ingevoerd worden zodat er mee gerekend kan worden
    B = float(value2)
    D = float(value3)
    sx = float(value4)
    C = float(value5)
    Ov1 = float(value6)
    Ov2 = float(value7)
    RGb = float(value8)
    RGo = float(value9)
    n = float(value10)
    Dg = float(value11)
    E = float(value12)
    
    if C >= Ov2:                                                                        #dit zijn een paar checks of de getallen die ingevoerd worden                    
        messagebox.showinfo('error','conisch kan niet groter zijn dan overslag 2')      #wel gebruikt kunnen worden en geeft de gebruiker een bericht terug wat er fout ging                                                                    
    else: 
        pass


    if (C > Ov2 - 5 - (Dg /2)) or (-C >= D - 5 - (Dg /2)):
        messagebox.showinfo('error','dat gaten zijn te dicht bij de rand')
    else: 
      pass

    if B > 1000:
        messagebox.showinfo('error','lengte kan niet groter zijn dan 1000')
    else: 
      pass
    

    if n <= 1 :
        messagebox.showinfo('error','het aantal gaten moet minimaal 2 zijn!')
    else:
        pass

    if eenheid == str("diameter"):                            #berekening als de eenheid diameter gekozen is
        print(D)
        D = (D * math.pi)
        print(D)
    
    else:
       pass

    F_Lu = D
    F_Lut = (D + Ov1 + Ov2 )
    F_Nx = math.ceil((F_Lut / sx))
    F_Dx = F_Lut / math.ceil(F_Nx)
    F_Lg = (B - RGb - RGo) / (n-1)
    F_Vg = C /(n-1)


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

def define_grid(width, height):
     rows = 0                                                  #geeft alle cellen in de grid een gewicht van 1 zodat deze zichtbaar
     columns = 0                                               # "leeg" zijn en dus niet alle text vakken tegen elkaar staan
     while rows < height:
          window.rowconfigure(rows, weight=1)
          rows += 1

     while columns < width:
          window.columnconfigure(columns, weight=1)
          columns += 1

def btn_GenereerCodeclicked():
    global start 
    global einde
    global Cnc_code
    global D
    if eenheid == str("diameter"):                            #berekening als de eenheid diameter gekozen is
        print(D)
        D = (D * math.pi)
        print(D)
    else:
       pass
    
    GrootteSlagXas()
    if hele_D  < sx and hele_D > 0:
        Breette_plaat()
        FuncitieDoorsnijden()
    elif hele_D  == sx:
        Breette_plaat()
        FuncitieDoorsnijden()
    else:
        pass

    einde ="M16\nG00 X0.0 Y50.0 \nM990 (doorsnijden plaat)\n"
    start ="G90(absolute positionering)\nG17\nM16\nM11  (Tang los) \nG00 X-" +str_sx +"Y0.0\nM10 (Tang vast)\n"

    if res_lengte != 1.1111111111:
        Aantal_Herhalingen()
    else:
        Aantal_Her_Msnij()
    
    Cnc_code += "M30  (einde programma)\n"
    CNCLabel.configure(text = Cnc_code)

def btn_BestandOpslaanclicked():
    filenaam = txt_bestandsnaam.get()+".CNC"    
    f=open(filenaam, "w+")
    f.write(Cnc_code)
    f.close() 

def OpenFile(event):
    path = askopenfilename(initialdir="\\10.31.64.9\Lasercutter1",                                      #dit path start die op als je de functie aanroept
                           filetypes =(("CNC Bestand", "*.CNC"),("alle bestanden","*.*")),
                           title = "kies een bestand."
                           )
    print (path)

def Breette_plaat():
    global grootte
    grootte =""
    Vboven = 0
    if B < 1000:
        Vboven = B + 5
        str_Vboven = str(Vboven)
        grootte ="G00 X0 Y"+str_Vboven +"\nM21  (laser aan)\nG91  (relatieve positionering)\nG01 X-"+str_sx +"Y0\nM20  (laser uit)\nM16\nG90  (absolute positionering)\n"
    elif B == 1000:
        grootte =""
    else:
        pass 

def GrootteSlagXas():
    global str_sx
    global hele_D
    str_sx = str(sx) 
    hele_D = float (D + Ov1 + Ov2)
    #----------------------------------ckeck de lengte -----------------------------------------------------------------------------------------------------------------------------------       
    if hele_D  < sx and hele_D > 0:            #als de lengte(Diameter + overslag 1 en 2) kleiner is dan de slag van de x as dan word de lengte van de plaat de slag van de x as
        str_sx = str(hele_D)
    elif hele_D  == sx:                   #als die hetzlefde is varanderd er niets 
        pass

    elif hele_D > sx:                    #als die groter is dan doe je elke tang overname hezelfde behalve de laatste                                                                #TO DO
        MeerdereSnijvlakken()
        
    else:
        messagebox.showinfo('error','lengte of diameter + overslag 1 en2 kan geen - getal zijn')

def FuncitieDoorsnijden():
    global doorsnijden 
    global E
    #-----------------------------------------------#check of de plaat moet worden doorgesneden------------------------------------------------------------------------------------------
    if E == 0:                                      #als E(lengte koker) 0 is hoeft die niet worden doorgesneden 
        doorsnijden = ""
    elif E > 0 and E < 1000:
        E += 5
        doorsnijden = "G00 X0.0 Y" +str(E) +"\nG91  (relatieve positionering)\nM21  (laser aan)\nG01 X-" +str_sx +" Y0.0\nM20  (laser uit)\nM16\nG90  (absolute positionering)\n"
    else:
        messagebox.showinfo('error','lengte koker waar de plaat doorgesneden moet worden kan geen - getal zijn en niet groter dan 999')

def Aantal_Herhalingen():
    global Cnc_code
    global nk
    k = 1 
    Cnc_code = ""
    str_k  = str(k)                                #groote x as
    if nk > 1:
        while nk > 1:
            aanhang ="(koker"+str_k +")\n"
            code = aanhang +start +grootte +doorsnijden +einde
            Cnc_code += code
            nk -= 1
            int_k = int(str_k)
            int_k += 1 
            str_k = str(int_k)
    elif nk == 1:
            aanhang ="(koker1)\n"
            code = aanhang +start +grootte +doorsnijden +einde
            Cnc_code += code
    else:
        messagebox.showinfo('error','aantal platen/kokers moet groter zijn dan 0') 

def Aantal_Her_Msnij():
    global Cnc_code
    global nk
    k = 1 
    Cnc_code = ""
    str_k  = str(k)                             
    if nk > 1:
        while nk >= 1:
            aanhang ="(koker"+str_k +")\n"
            code = aanhang +midden +laatste +einde
            Cnc_code += code
            nk -= 1
            int_k = int(str_k)
            int_k += 1 
            str_k = str(int_k)
    elif nk == 1:
            aanhang ="(koker1)\nG90\nG17\nM16\nM11  (Tang los) \nG00 X-" +str_sx +"Y0.0\nM10 (Tang vast)\n"
            code = aanhang +midden +laatste +einde
            Cnc_code += code
    else:
        messagebox.showinfo('error','aantal platen/kokers moet groter zijn dan 0') 

def MeerdereSnijvlakken():
    global tangoverpak
    global midden
    global laatste
    global str_sx
    res_lengte = hele_D
    midden = ""
    temp =""
    laatste = ""
    str_sx = str(sx)

    
    while res_lengte > sx:
        Breette_plaat()
        FuncitieDoorsnijden()
        tangoverpak ="(TangOverpak)\nM11  (Tang los) \nG00 X-" +str_sx +" Y0.0\nM10 (Tang vast)\nM16\n"
        temp = tangoverpak +"(segment)\n" +grootte +doorsnijden  
        midden += temp
        res_lengte -= sx
        print(res_lengte)
    
    if res_lengte < sx and res_lengte > 0:
        print(res_lengte)
        str_sx = str(res_lengte)
        tangoverpak ="(TangOverpak)\nM11  (Tang los) \nG00 X-" +str_sx +" Y0.0\nM10 (Tang vast)\n"
        Breette_plaat()
        FuncitieDoorsnijden()
        laatste = tangoverpak +"(segment)\n" +grootte +doorsnijden
    else:
        pass



    
define_grid(grid_breedte,grid_hoogte)
#-----------------text boxes-----------------------------------------------------------------------------------------------
txt_nk = Entry(window,width=10)                 #dit zijn alle invoer boxen met een standard waarde 
txt_nk.insert(END, '1')
txt_nk.grid(column=10, row=2)

txt_B = Entry(window,width=10)
txt_B.insert(END, '1000')
txt_B.grid(column=10, row=3)

txt_D = Entry(window,width=10)
txt_D.insert(END, '570')
txt_D.grid(column=10, row=4)

txt_SX = Entry(window,width=10)
txt_SX.insert(END, '500')
txt_SX.grid(column=10, row=5)

txt_C = Entry(window,width=10)
txt_C.insert(END, '0')
txt_C.grid(column=10, row=6)

txt_Ov1 = Entry(window,width=10)
txt_Ov1.insert(END, '15')
txt_Ov1.grid(column=10, row=7)

txt_Ov2 = Entry(window,width=10)
txt_Ov2.insert(END, '15')
txt_Ov2.grid(column=10, row=8)

txt_RGb = Entry(window,width=10)
txt_RGb.insert(END, '62.5')
txt_RGb.grid(column=10, row=9)

txt_RGo = Entry(window,width=10)
txt_RGo.insert(END, '62.5')
txt_RGo.grid(column=10, row=10)

txt_n = Entry(window,width=10)
txt_n.insert(END, '8')
txt_n.grid(column=10, row=11)

txt_Dg = Entry(window,width=10)
txt_Dg.insert(END, '3')
txt_Dg.grid(column=10, row=12)
txt_E = Entry(window,width=10)
txt_E.insert(END, '500')
txt_E.grid(column=10, row=13)

txt_bestandsnaam = Entry(window,width=30)
txt_bestandsnaam.insert(END, 'Hertel_CNC')
txt_bestandsnaam.grid(column=34, row=2, sticky='w')

txt_locatie = Entry(window,width=30)
txt_locatie.insert(END, '.\ ')
txt_locatie.grid(column=34, row=3, sticky='w')
txt_locatie.bind("<1>", OpenFile)

#------------------knoppen--------------------------------------------------------------------------------------------
btn_Bereken = Button(window, text="bereken", command=btn_berekenclicked, bg="grey", fg="black", padx=22, pady=5)   #knoppen met welke command ze aanroepen
btn_Bereken.grid(column=1, row=2)

btn_GenereerCode = Button(window, text="genereer code",command=btn_GenereerCodeclicked, bg="grey", fg="black", padx=5.3, pady=5)
btn_GenereerCode.grid(column=1, row=4)

btn_BestandOpslaan = Button(window, text="bestand opslaan",command=btn_BestandOpslaanclicked, bg="grey", fg="black", padx=0, pady=5)
btn_BestandOpslaan.grid(column=1, row=6)

btn_switch = Button(window, text="switch van eenheid",command=btn_switchclicked, bg="grey", fg="blue", padx=2, pady=5)
btn_switch.grid(column=1, row=8)

#-----------labels----------------------------------------------------------------------------------------------------
lbl_in = Label(window, text="Invoer waarden", anchor='w', font=("Arial Bold", 18))
lbl_in.grid(column=4, row=1)

lbl_nk = Label(window, text="nk       Aantal platen", anchor='w')
lbl_nk.grid(column=4, row=2, sticky = W)

lbl_B = Label(window, text="B         Breedte plaat", anchor='w')
lbl_B.grid(column=4, row=3, sticky = W)

lbl_D = Label(window, text="D         Lengte plaat", anchor='w')
lbl_D.grid(column=4, row=4, sticky = W)

lbl_SX = Label(window, text="SX       Slag van de X-as", anchor='w')
lbl_SX.grid(column=4, row=5, sticky = W)

lbl_C = Label(window, text="C        Conisch", anchor='w')
lbl_C.grid(column=4, row=6, sticky = W)

lbl_Ov1 = Label(window, text="Ov1    Overslag 1", anchor='w')
lbl_Ov1.grid(column=4, row=7, sticky = W)

lbl_Ov2 = Label(window, text="Ov2    Overslag 2", anchor='w')
lbl_Ov2.grid(column=4, row=8, sticky = W)

lbl_RGb = Label(window, text="RGb    Afstand rand - 1e gat boven", anchor='w')
lbl_RGb.grid(column=4, row=9, sticky = W)

lbl_RGo = Label(window, text="RGo    Afstand rand - 1e gat onder", anchor='w')
lbl_RGo.grid(column=4, row=10, sticky = W)

lbl_n = Label(window, text="n         Aantal gaten", anchor='w')
lbl_n.grid(column=4, row=11, sticky = W)

lbl_Dg = Label(window, text="Dg      Diameter gat", anchor='w')
lbl_Dg.grid(column=4, row=12, sticky = W)

lbl_E = Label(window, text="E      Lengte koker", anchor='w')
lbl_E.grid(column=4, row=13, sticky = W)

lbl_uit = Label(window, text="berekende waarden", anchor='w', font=("Arial Bold", 18))
lbl_uit.grid(column=4, row=14)

lbl_Lu = Label(window, text="Lu      Uitslag tussen de gaten ", anchor='w')
lbl_Lu.grid(column=4, row=15, sticky = W, columnspan=5)

lbl_Lut = Label(window, text="Lut     Totale uitslag", anchor='w')
lbl_Lut.grid(column=4, row=16, sticky = W, columnspan=5)

lbl_Nx = Label(window, text="Nx      aantal tang overnames", anchor='w')
lbl_Nx.grid(column=4, row=17, sticky = W, columnspan=5)

lbl_Dx = Label(window, text="Dx      X maat overnames", anchor='w')
lbl_Dx.grid(column=4, row=18, sticky = W, columnspan=5)

lbl_Lg = Label(window, text="Lg      Afstand tussen de gaten", anchor='w')
lbl_Lg.grid(column=4, row=19, sticky = W, columnspan=5)

lbl_Vg = Label(window, text="Vg      Verloop per gat", anchor='w')
lbl_Vg.grid(column=4, row=20, sticky = W, columnspan=5)

lbl_naam = Label(window, text="Naam:", anchor='w')
lbl_naam.grid(column=32, row=2, sticky = W,)

lbl_locatie = Label(window, text="locatie:", anchor='w')
lbl_locatie.grid(column=32, row=3, sticky = W,)

lbl_CNC = Label(window, text="gegenereerde code", anchor='w', font=("Arial Bold", 18))
lbl_CNC.grid(column=32, row=4)

CNCLabelframe = LabelFrame(window, text= titel)
CNCLabelframe.grid(column=32, row=5, padx=10, pady=10, ipadx=20, ipady=20, columnspan=10, rowspan=20, sticky=W+E+N+S)

CNCLabel = Label(CNCLabelframe, text= Cnc_code, anchor='w')
CNCLabel.grid()

#-----------------foto-----------------------------------------------------------------------------------------------------------------------------------
image = Image.open("foto.png")          #foto
photo = ImageTk.PhotoImage(image)
label = Label(image=photo)
label.image = photo # this line need to prevent gc
label.grid(column=20, row=2, columnspan=10, rowspan=25, sticky=W+E+N+S, padx=5, pady=5)
#--------------------------------------------------------------------------------------------------------------------------------------------------------
window.mainloop()
