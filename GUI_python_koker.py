import math
from tkinter import *
from tkinter import messagebox

from PIL import Image, ImageTk

#----------------window instellingen-----------------------------------------------------------------------------------------------
window = Tk()
window.title("Hertel-kokerprogramma")
window.geometry('1280x680')
#---------------variables------------------------------------------------------------------------------------------------------------------------------------
grid_breedte = 50                 #verander de grid groote 
grid_hoogte = 50   
eenheid = "lengte"   
Cnc_code = "(gegenereerde cnc code)\n"    
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
    
    if C >= Ov2:                                                                  #dit zijn een paar checks of de getallen die ingevoerd worden 
        print("conisch kan niet groter zijn dan overslag 2!")                     #wel gebruikt kunnen worden en geeft de gebruiker een 
        messagebox.showinfo('error','conisch kan niet groter zijn dan overslag 2')#bericht terug wat er fout ging
    else: 
        pass


    if (C > Ov2 - 5 - (Dg /2)) or (-C >= D - 5 - (Dg /2)):
        print("dat gaten zijn te dicht bij de rand")
        messagebox.showinfo('error','dat gaten zijn te dicht bij de rand')
    else: 
      pass
    

    if n <= 1 :
        print("het aantal gaten moet minimaal 2 zijn!")
        messagebox.showinfo('error','het aantal gaten moet minimaal 2 zijn!')
    else:
        pass

    if eenheid == str("diameter"):                            #berekening als de eenheid diameter gekozen is
        print('diameter')
        F_Lu = D * math.pi
        F_Lut = ((D*math.pi) + Ov1 + Ov2 )
        F_Nx = math.ceil((F_Lut / sx))
        F_Dx = F_Lut / math.ceil(F_Nx)
        F_Lg = (B - RGb - RGo) / (n-1)
        F_Vg = C /(n-1)
    elif eenheid == str("lengte"):                           #berekening als de eenheid lengte is 
        print('lengte')
        F_Lu = D
        F_Lut = (D + Ov1 + Ov2 )
        F_Nx = math.ceil((F_Lut / sx))
        F_Dx = F_Lut / math.ceil(F_Nx)
        F_Lg = (B - RGb - RGo) / (n-1)
        F_Vg = C /(n-1)
    elif eenheid == str(""): 
        F_Lu = D
        F_Lut = (D + Ov1 + Ov2 )
        F_Nx = math.ceil((F_Lut / sx))
        F_Dx = F_Lut / math.ceil(F_Nx)
        F_Lg = (B - RGb - RGo) / (n-1)
        F_Vg = C /(n-1)
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
    global Cnc_code
    Cnc_code = ""
    print (nk)
    print (B)
    print (D)
    print (sx)
    print (C)
    print (Ov1)
    print (Ov2)
    print (RGb)
    print (RGo)
    print (n)
    print (Dg)  
    print (F_Lu)  
    print (F_Lut)
    print (F_Nx)
    print (F_Dx)
    print (F_Lg)
    print (F_Vg)

    #--------------------------naar string------------------------------------------------------------------------------------------------------------------------------------------------- 
    str_doorsnijden = str(txt_E.get())              #bij de helft snij je hem door
    str_sx = str(sx)                    #groote x as 
    

    start ="(gegenereerde cnc code)\nG90\nG17\nM16\nM11  (Tang los) \nG00 X-" +str_sx +"Y0.0\nM10 (Tang vast)\n"
    doorsnijden ="G00 X0.0 Y" +str_doorsnijden +"\nG91  (relatieve positionering)\nM21  (laser aan)\nG01 X-" +str_sx +" Y0.0\nM20  (laser uit)\nG90  (absolute positionering)\n"
    berekening = start +doorsnijden +"M16\nG00 X0.0 Y50.0 \nM990 (doorsnijden plaat)\n (einde programma)\nM30" 
    code = berekening +"\n"
    Cnc_code += code 
    CNCLabel.configure(text = Cnc_code)
    
 
    print (Cnc_code)


def btn_BestandOpslaanclicked():
    filenaam = txt_bestandsnaam.get()+".CNC"    
    f=open(filenaam, "w+")
    f.write(Cnc_code)
    f.close() 

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

CNCLabelframe = LabelFrame(window)
CNCLabelframe.grid(column=32, row=5, padx=10, pady=10, ipadx=20, ipady=20, columnspan=10, rowspan=20, sticky=W+E+N+S)

CNCLabel = Label(CNCLabelframe, text= Cnc_code, anchor='w')
CNCLabel.grid()

#-----------------foto-----------------------------------------------------------------------------------------------------------------------------------
image = Image.open("foto.png")          #foto
photo = ImageTk.PhotoImage(image)
label = Label(image=photo)
label.image = photo # this line need to prevent gc
label.grid(column=20, row=2, columnspan=10, rowspan=25, sticky=W+E+N+S, padx=5, pady=5)
#-----------------------text file----------------------------------------------------------------------------------------------------------------------------


window.mainloop()
