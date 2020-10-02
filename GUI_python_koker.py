import math
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import *
from PIL import Image, ImageTk
from tkinter import scrolledtext 
import tkinter as tk
import os.path
#----------------window instellingen-----------------------------------------------------------------------------------------------
window = Tk()
window.title("Hertel-kokerprogramma")
window.geometry('1280x680')
photo = PhotoImage(file="icon.png")
window.iconphoto(False, photo)
window['bg'] = '#49A'                #achtergrondkleur
#---------------variables------------------------------------------------------------------------------------------------------------------------------------
grid_breedte = 50                 #verander de grid groote 
grid_hoogte = 50   
eenheid = "lengte"   
titel = "(gegenereerde cnc code)"  
Cnc_code =""
global res_lengte
res_lengte = 1.1111111111
global afwijking
afwijking = 5

 
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
    global n_Onder
    global n_Boven
    global Lg_O
    global Lg_B
    global VgB
    global VgO

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

    if (C > Ov2 - 5 - (Dg /2)) or (-C >= D - 5 - (Dg /2)):                                  #dit zijn een paar checks of de getallen die ingevoerd worden                    
        messagebox.showinfo('error','dat gaten zijn te dicht bij de rand')                  #wel gebruikt kunnen worden en geeft de gebruiker een bericht terug wat er fout ging
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

    if eenheid == "diameter":
        D = ((D * math.pi) - Ov1 - Ov2)
        print(D)

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
          window.rowconfigure(rows, weight=1)
          rows += 1

     while columns < width:
          window.columnconfigure(columns, weight=1)
          columns += 1

def btn_GenereerCodeclicked():
    global einde
    global Cnc_code
    global D
    Cnc_code = ''
    

    try:
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

        if res_lengte != 1.1111111111:
            Aantal_Herhalingen()
        else:
            Aantal_Her_Msnij()

        Cnc_code += "M30  (einde programma)\n"
        canvas.itemconfig(canvas_id, text= Cnc_code)

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
            file1.write(Cnc_code)
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
    first_xcord = (temp_sx - Ov1)
    first_ycord = RGo
    first_xcord_straal = first_xcord + (Dg / 2)
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
            
            while n > 1:                                                #gaten links
                str_gat_num = str(gat_num)
                new_ycord = round(new_ycord, 3)
                new_xcord = round(new_xcord, 3)
                xcord_straal = new_xcord + (Dg / 2)
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
            
                xcord_straal = new_xcord + (Dg / 2)
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
                xcord_straal = new_xcord + (Dg / 2)
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
        gaatjes = "(gaten bovenste deel)\n(gat1)\nG00 X- "+str_FO_xcord +" Y "+str_FO_ycord +"\nM21  (Laser aan)\nG01 X-"+str_EO_straal +" Y "+str_FO_ycord +"\nG03 X-"+str_EO_straal +" Y "+str_FO_ycord +" I "+str_straal+" J 0.0\nM20  (Laser uit)\nM16\n"
       
        if var1.get() == 1:
            new_xcordO -= VgO
        elif var2.get() == 1:
            new_xcordO -= VgO
        else:
            pass
        
        if hele_D  == sx:
        
            while n_Onder > 1:                                                #gaten links onder
                str_gat_num = str(gat_num)
                new_ycordO = round(new_ycordO, 3)
                new_xcordO = round(new_xcordO, 3)
                new_xcordO_straal = new_xcordO + (Dg / 2)
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
                new_xcordB_straal = new_xcordB + (Dg / 2)
                str_xcordB_straal = str(new_xcordB_straal)
                str_new_xcordB = str(new_xcordB)
                str_new_ycordB = str(new_ycordB)


                gaatjes_binnen_sx +="(gat"+str_gat_num +")\nG00 X- "+str_new_xcordB +" Y "+str_new_ycordB +"\nM21  (Laser aan)\nG01 X-"+str_xcordB_straal +" Y "+str_new_ycordB +"\nG03 X-"+str_xcordB_straal +" Y "+str_new_ycordB+" I "+str_straal+" J 0.0\nM20  (Laser uit)\nM16\n"


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

                xcordO_straal = new_xcordO + (Dg / 2)
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

            while n_Boven > 1:                                                #gaten linksv boven   #TO DO
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
                xcordB_straal = float(str_xcordB_straal)


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
            gaatjes += "(gaten onderste deel)\n(gat"+str_gat_num +")\nG00 X- "+str_FB_xcord +" Y "+str_FB_ycord +"\nM21  (Laser aan)\nG01 X-"+str_EB_straal +" Y "+str_FB_ycord +"\nG03 X-"+str_EB_straal +" Y "+str_FB_ycord +" I "+str_straal+" J 0.0\nM20  (Laser uit)\nM16\n"
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
            
            xcord_straal = new_xcord + (Dg / 2)
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
        laatstegaatjes += "(gaten bovenste deel)\n(gat1)\nG00 X- "+str_first_xcordB +" Y "+str_first_ycordB +"\nM21  (Laser aan)\nG01 X-"+str_first_xcordB_straal +" Y "+str_first_ycordB +"\nG03 X-"+str_first_xcordB_straal +" Y "+str_first_ycordB+" I "+str_straal+" J 0.0\nM20  (Laser uit)\nM16\n"
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
            xcordB_straal = float(str_xcordB_straal)
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
            
def Aantal_Herhalingen():
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

def Aantal_Her_Msnij():
    global Cnc_code
    global nk
    global gaatjes_binnen_sx
    code = ""
    start ="G90(absolute positionering)\nG17\nM16\nM11  (Tang los)\nG00 X-"+str_sx+"Y 0.0\nM10  (Tang vast)\n"
    k = 1 
    Cnc_code = ""
    str_k  = str(k)    


    if nk > 1: 
        snijgaten()                                 
        while nk >= 1:
            aanhang ="(koker"+str_k +")\n"
            code = aanhang +start +gaatjes_binnen_sx +grootte +doorsnijden +einde
            Cnc_code += code
            nk -= 1
            int_k = int(str_k)
            int_k += 1 
            str_k = str(int_k)

    elif nk == 1:
            snijgaten()
            aanhang ="(koker1)\n"   
            code = aanhang +start +gaatjes_binnen_sx +grootte +doorsnijden +einde
            Cnc_code += code
    else:
        messagebox.showinfo('error','aantal platen/kokers moet groter zijn dan 0') 

def MeerdereSnijvlakken():
    global tangoverpak
    global midden
    global laatste
    global res_lengte
    global str_sx
    res_lengte = hele_D
    midden = ""
    temp =""
    laatste = ""
    str_sx = str(sx)


    while res_lengte > sx:
        Breette_plaat()
        FuncitieDoorsnijden()
        
        if res_lengte == hele_D:
            snijgaten()   
            tangoverpak ="(TangOverpak)\n(overname1)\nG00 X0.0 Y0.0\nM11  (Tang los) \nG00 X-" +str_sx +" Y0.0\nM10 (Tang vast)\nM16\n"
            temp = tangoverpak +"(segment)\n"+gaatjes +grootte +doorsnijden
            midden += temp
            res_lengte -= sx
            print(res_lengte)
        
        else:
            tangoverpak ="(TangOverpak)\n(overname1)\nG00 X0.0 Y0.0\nM11  (Tang los) \nG00 X-" +str_sx +" Y0.0\nM10 (Tang vast)\nM16\n"
            temp = tangoverpak +"(segment)\n" +grootte +doorsnijden 
            midden += temp
            res_lengte -= sx
            print(res_lengte)

    if res_lengte < sx and res_lengte > 0:
        str_sx = str(res_lengte)  
        tangoverpak ="(TangOverpak)\n(overname1)\nG00 X0.0 Y0.0\nM11  (Tang los) \nG00 X-" +str_sx +" Y0.0\nM10 (Tang vast)\nM16\n"
        Breette_plaat()
        FuncitieDoorsnijden()
        laatstesnijgaten()
        laatste = tangoverpak +"(segment)\n" +laatstegaatjes +grootte +doorsnijden 
    else:
        pass

    
define_grid(grid_breedte,grid_hoogte)
#-----------------text boxes-----------------------------------------------------------------------------------------------
txt_nk = Entry(window,width=10)                 #dit zijn alle invoer boxen met een standard waarde 
txt_nk.insert(END, '1')
txt_nk.grid(column=10, row=3)

txt_B = Entry(window,width=10)
txt_B.insert(END, '1000')
txt_B.grid(column=10, row=4)

txt_D = Entry(window,width=10)
txt_D.insert(END, '570')
txt_D.grid(column=10, row=5)

txt_SX = Entry(window,width=10)
txt_SX.insert(END, '500')
txt_SX.grid(column=10, row=6)

txt_C = Entry(window,width=10)
txt_C.insert(END, '0')
txt_C.grid(column=10, row=7)

txt_Ov1 = Entry(window,width=10)
txt_Ov1.insert(END, '15')
txt_Ov1.grid(column=10, row=8)

txt_Ov2 = Entry(window,width=10)
txt_Ov2.insert(END, '15')
txt_Ov2.grid(column=10, row=9)

txt_RGb = Entry(window,width=10)
txt_RGb.insert(END, '62.5')
txt_RGb.grid(column=10, row=10)

txt_RGo = Entry(window,width=10)
txt_RGo.insert(END, '62.5')
txt_RGo.grid(column=10, row=11)

txt_n = Entry(window,width=10)
txt_n.insert(END, '8')
txt_n.grid(column=10, row=12)

txt_Dg = Entry(window,width=10)
txt_Dg.insert(END, '3')
txt_Dg.grid(column=10, row=13)

txt_E = Entry(window,width=10)
txt_E.insert(END, '500')
txt_E.grid(column=10, row=14)

var1 = tk.IntVar()
txt_CL = tk.Checkbutton(window,text="conisch links?",variable=var1, onvalue=1, offvalue=0)
txt_CL.grid(column=5, row=7)

var2 = tk.IntVar()
txt_CL = tk.Checkbutton(window,text="beide conisch?",variable=var2, onvalue=1, offvalue=0)
txt_CL.grid(column=6, row=7)

txt_bestandsnaam = Entry(window,width=30)
txt_bestandsnaam.insert(END, 'Hertel_CNC')
txt_bestandsnaam.grid(column=34, row=2, sticky='w')

txt_locatie = Entry(window,width=30)
txt_locatie.insert(END, '.\ ')
txt_locatie.grid(column=34, row=3, sticky='w')
txt_locatie.bind("<1>", OpenFile)

#------------------knoppen--------------------------------------------------------------------------------------------
btn_Bereken = Button(window, text="bereken", command=btn_berekenclicked, bg="#ccffff", fg="black", padx=22, pady=5, cursor = "hand2")   #knoppen met welke command ze aanroepen
btn_Bereken.grid(column=1, row=2)

btn_GenereerCode = Button(window, text="genereer code",command=btn_GenereerCodeclicked, bg="#ccffff", fg="black", padx=5.3, pady=5, cursor = "hand2")
btn_GenereerCode.grid(column=1, row=4)

btn_BestandOpslaan = Button(window, text="bestand opslaan",command=btn_BestandOpslaanclicked, bg="#ccffff", fg="black", padx=0, pady=5, cursor = "hand2")
btn_BestandOpslaan.grid(column=1, row=6)

btn_switch = Button(window, text="switch van eenheid",command=btn_switchclicked, bg="#ccffff", fg ="black" ,padx=2, pady=5, cursor = "hand2")
btn_switch.grid(column=1, row=8)

#-----------labels----------------------------------------------------------------------------------------------------
lbl_in = Label(window, text="Invoer waarden", anchor='w', font=("Arial Bold", 18))
lbl_in.grid(column=4, row=2, sticky = "w")

lbl_nk = Label(window, text="nk       Aantal platen", anchor='w')
lbl_nk.grid(column=4, row=3, sticky = W)

lbl_B = Label(window, text="B         Breedte plaat", anchor='w')
lbl_B.grid(column=4, row=4, sticky = W)

lbl_D = Label(window, text="D         Lengte plaat", anchor='w')
lbl_D.grid(column=4, row=5, sticky = W)

lbl_SX = Label(window, text="SX       Slag van de X-as", anchor='w')
lbl_SX.grid(column=4, row=6, sticky = W)

lbl_C = Label(window, text="C        Conisch", anchor='w')
lbl_C.grid(column=4, row=7, sticky = W)

lbl_Ov1 = Label(window, text="Ov1    Overslag 1", anchor='w')
lbl_Ov1.grid(column=4, row=8, sticky = W)

lbl_Ov2 = Label(window, text="Ov2    Overslag 2", anchor='w')
lbl_Ov2.grid(column=4, row=9, sticky = W)

lbl_RGb = Label(window, text="RGb    Afstand rand - 1e gat boven", anchor='w')
lbl_RGb.grid(column=4, row=10, sticky = W)

lbl_RGo = Label(window, text="RGo    Afstand rand - 1e gat onder", anchor='w')
lbl_RGo.grid(column=4, row=11, sticky = W)

lbl_n = Label(window, text="n         Aantal gaten", anchor='w')
lbl_n.grid(column=4, row=12, sticky = W)

lbl_Dg = Label(window, text="Dg      Diameter gat", anchor='w')
lbl_Dg.grid(column=4, row=13, sticky = W)

lbl_E = Label(window, text="E       Grootte koker", anchor='w')
lbl_E.grid(column=4, row=14, sticky = W)

lbl_uit = Label(window, text="berekende waarden", anchor='w', font=("Arial Bold", 18))
lbl_uit.grid(column=4, row=15, sticky = "w")

lbl_Lu = Label(window, text="Lu      Uitslag tussen de gaten ", anchor='w')
lbl_Lu.grid(column=4, row=16, sticky = W, columnspan=10)

lbl_Lut = Label(window, text="Lut     Totale uitslag", anchor='w')
lbl_Lut.grid(column=4, row=17, sticky = W, columnspan=10)

lbl_Nx = Label(window, text="Nx      aantal tang overnames", anchor='w')
lbl_Nx.grid(column=4, row=18, sticky = W, columnspan=10)

lbl_Dx = Label(window, text="Dx      X maat overnames", anchor='w')
lbl_Dx.grid(column=4, row=19, sticky = W, columnspan=10)

lbl_Lg = Label(window, text="Lg      Afstand tussen de gaten", anchor='w')
lbl_Lg.grid(column=4, row=20, sticky = W, columnspan=10)

lbl_Vg = Label(window, text="Vg      Verloop per gat", anchor='w')
lbl_Vg.grid(column=4, row=21, sticky = W, columnspan=10)

lbl_nB = Label(window, text="nB      aantal gaten bover", anchor='w')
lbl_nB.grid(column=4, row=22, sticky = W, columnspan=10)

lbl_nO = Label(window, text="nO      aantal gaten onder", anchor='w')
lbl_nO.grid(column=4, row=23, sticky = W, columnspan=10)

lbl_naam = Label(window, text="Naam:", anchor='w')
lbl_naam.grid(column=33, row=2, sticky = W,)

lbl_locatie = Label(window, text="locatie:", anchor='w')
lbl_locatie.grid(column=33, row=3, sticky = W,)

lbl_CNC = Label(window, text="gegenereerde code", anchor='w', font=("Arial Bold", 18))
lbl_CNC.grid(column=33, row=4, columnspan= 2, sticky = "w")


#-----------------foto-----------------------------------------------------------------------------------------------------------------------------------
image = Image.open("foto.png")          #foto
photo = ImageTk.PhotoImage(image)
label = Label(image=photo)
label.image = photo # this line need to prevent gc
label.grid(column=20, row=3, columnspan=10, rowspan=25, sticky=W+E+N+S, padx=5, pady=5)


#----------------canvas----------------------------------------------------------------------------------------------------------------------------------------

frame=Frame(window,width=400, height=600)
frame.grid(row=5, column=33, rowspan=20, columnspan=5, sticky = "w")
canvas=Canvas(frame,bg='#FFFFFF',width=400,height=600,scrollregion=(0,0,600,10000))
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


window.mainloop()
