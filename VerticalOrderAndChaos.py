import tkinter as tk
from tkinter import SW,S,N
import copy


######################################################################
## Igra

class Igra():
    def __init__(self):
        self.igralnoPolje=[[0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0]]
        """Tip je barva zetona."""
        self.tip=-1
        self.naVrsti="Na vrsti je Order"
        #ali je igra zakljucena ali ne
        self.konec="Ne"
        #Vrsta igre: 1=clovek clovek, 2= order PC,3= Chaos PC,4=PC PC
        self.vrstaIgre=1

    def vstaviVPolje(self,stolpec):
        """Stevilo stolpca od 0-6."""
        #pomika se od spodaj gor po stolpcu dokler ne najde prostega mesta da zeton vstavi
        vrstica=5
        while vrstica>=0:
            if self.igralnoPolje[vrstica][stolpec]==0:
                self.igralnoPolje[vrstica][stolpec]=self.tip
                gui.narisiZeton((stolpec+1)*50+25,vrstica*50+25,self.tip)
                self.spremeniNaVrsti()
                self.stanjeIgre()
                break
            else: vrstica-=1

    def vstolpec(self,j):
        """Naredi seznam stolpca."""
        return [self.igralnoPolje[i][j] for i in range(6)]

    def stanjeIgre(self):
        """spremeni kdo je na vrsti, ali je igre konec itd..."""

        diagonalePolja= [[(0,0),(1,1),(2,2),(3,3),(4,4),(5,5)],
                        [(0,5),(1,4),(2,3),(3,2),(4,1),(5,0)],
                        [(0,6),(1,5),(2,4),(3,3),(4,2),(5,1)],
                        [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6)],
                        [(0,2),(1,3),(2,4),(3,5),(4,6)],
                        [(1,1),(2,2),(3,3),(4,4),(5,5)],
                        [(0,4),(1,3),(2,2),(3,1),(4,0)],
                        [(1,6),(2,5),(3,4),(4,3),(5,2)]]
        diagonale=[]
        for d in diagonalePolja:
            diagonala=[]
            for e in d:
                (i,j)=e
                diagonala.append(self.igralnoPolje[i][j])
            diagonale.append(diagonala)
        kombinacijeDiagonale=[]
        for dia in diagonale:
            if len(dia)==6:
                kombinacijeDiagonale+=[dia[:5]]+[dia[1:]]
            else:
                kombinacijeDiagonale+=[dia]


        stolpci=[self.vstolpec(j) for j in range(7)]
        kombinacijeStolpci=[]
        for s in stolpci:
            kombinacijeStolpci+=[s[:5]]+[s[1:]]

        vrstice=[self.igralnoPolje[i] for i in range(6)]
        kombinacijeVrstice=[]
        for v in vrstice:
            kombinacijeVrstice+=[v[:5]]+[v[1:6]]+[v[2:]]

        kombinacije=kombinacijeDiagonale+kombinacijeStolpci+kombinacijeVrstice
        for kombinacija in kombinacije:
            tip=kombinacija[0]
            if len(list(set(kombinacija)))==1 and tip!=0:
                gui.napis.set("Zmagal je ORDER!")
                self.konec="Da"
                gui.plosca.unbind("<Button-1>")

        if len(mini.veljavnePoteze(self.igralnoPolje))==0:
            if self.konec!="Da":
                gui.napis.set("Zmagal je CHAOS !")
                self.konec="Da"

    def spremeniNaVrsti(self):
        """spremeni kdo je na vrsti"""
        if self.naVrsti=="Na vrsti je Order":
                self.naVrsti="Na vrsti je Chaos"
                gui.napis.set(self.naVrsti)
        else:
            self.naVrsti="Na vrsti je Order"
            gui.napis.set(self.naVrsti)



######################################################################################
#veliki mojster iger, gospod Dr. Alfa Bet, tudi poznan kot algoritem alfa beta rezanje

class AlfaBet():

    def __init__(self):
        self.tezavnost=0

    def vrednostPogoja(self,kombinacija):
        """poisce vrednost vrstice/diagonale/stolpca"""
        l=len(set(kombinacija))
        if l==1 and 0 not in kombinacija:
            return 44000000
        elif l==2 and 0 not in kombinacija:
            return -100
        elif l==2:
           return 100*abs(sum(kombinacija))
        elif l==3:
            return -100000
        elif l==1 and 0 in kombinacija:
            return 50


    def vstaviVPolje(self,polje,stolpec,tip):
        """Stevilo stolpca od 0-6."""
        vrstica=5
        while vrstica>=0:
            if polje[vrstica][stolpec]==0:
                polje[vrstica][stolpec]=tip
                break
            else: vrstica-=1
        return polje

    def vstolpec(self,polje,j):
        """Naredi seznam stolpca"""
        return [polje[i][j] for i in range(6)]


    def vrednostPolja(self,polje):
        """Izracuna vrednost polja = vsota vrednosti vseh vrstic, diagonal in stolpcev"""

        diagonalePolja= [[(0,0),(1,1),(2,2),(3,3),(4,4),(5,5)],
                        [(0,5),(1,4),(2,3),(3,2),(4,1),(5,0)],
                        [(0,6),(1,5),(2,4),(3,3),(4,2),(5,1)],
                        [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6)],
                        [(0,2),(1,3),(2,4),(3,5),(4,6)],
                        [(1,1),(2,2),(3,3),(4,4),(5,5)],
                        [(0,4),(1,3),(2,2),(3,1),(4,0)],
                        [(1,6),(2,5),(3,4),(4,3),(5,2)]]
        diagonale=[]
        for d in diagonalePolja:
            diagonala=[]
            for e in d:
                (i,j)=e
                diagonala.append(polje[i][j])
            diagonale.append(diagonala)
        kombinacijeDiagonale=[]
        for dia in diagonale:
            #zdruzi vse diagonale
            if len(dia)==6:
                #razdeli diagonale ki so dolge 6 polj na 2 dela
                kombinacijeDiagonale+=[dia[:5]]+[dia[1:]]
            else:
                kombinacijeDiagonale+=[dia]

        #ustvari vse stolpce
        stolpci=[self.vstolpec(polje,j) for j in range(7)]
        kombinacijeStolpci=[]
        for s in stolpci:
            kombinacijeStolpci+=[s[:5]]+[s[1:]]

        #ustvari vse vrstice
        vrstice=[polje[i] for i in range(6)]
        kombinacijeVrstice=[]
        for v in vrstice:
            kombinacijeVrstice+=[v[:5]]+[v[1:6]]+[v[2:]]
        #zdruzi vse mozne "5poljne" vrstice/diagonale/stolpce
        kombinacije=kombinacijeDiagonale+kombinacijeStolpci+kombinacijeVrstice
        #sesteje vrednosti "5poljnih" vrstic/diagona/stolpcev
        return sum([self.vrednostPogoja(kombinacija) for kombinacija in kombinacije])


    def veljavnePoteze(self,polje):
        """naredu seznam veljavnih potez"""
        veljavne=[]
        for i in range(7):
            if polje[0][i]==0:
                veljavne.append(i)
        return veljavne

    def razveljaviPotezo(self,polje,stolpec):
        """Razveljavi potezo v stolpcu"""
        vrstica=0
        while 0<6:
            if polje[vrstica][stolpec]!=0:
                polje[vrstica][stolpec]=0
                break
            else: vrstica+=1


    def najboljsaPotezaO(self,polje,globina):
        """najboljsa poteza za order"""
        najvisjaVrednost=-100000000000000
        najboljsaPoteza=[-5,0]
        for i in self.veljavnePoteze(polje):
            #poskusi z rdecim zetonom
            self.vstaviVPolje(polje,i,1)
            vrednost=self.alfabet(polje,globina,True)
            if vrednost>najvisjaVrednost:
                najvisjaVrednost=vrednost
                najboljsaPoteza[0]=i
                najboljsaPoteza[1]=1
            self.razveljaviPotezo(polje,i)
            #poskusi z modrim zetonom
            self.vstaviVPolje(polje,i,-1)
            vrednost=self.alfabet(polje,globina,True)
            if vrednost>najvisjaVrednost:
                najboljsaPoteza[0]=i
                najboljsaPoteza[1]=-1
            self.razveljaviPotezo(polje,i)
        return  najboljsaPoteza

    def najboljsaPotezaC(self,polje,globina,order=False):
        """najboljsa poteza za chaos"""
        najnizjaVrednost=10000000000000000
        najboljsaPoteza=[-5,0]
        for i in self.veljavnePoteze(polje):
            #poskusi z rdecim zetonom
            self.vstaviVPolje(polje,i,1)
            vrednost=self.alfabet(polje,globina,order)
            if vrednost<najnizjaVrednost:
                najnizjaVrednost=vrednost
                najboljsaPoteza[0]=i
                najboljsaPoteza[1]=1
            self.razveljaviPotezo(polje,i)
            #poskusi z modrim zetonom
            self.vstaviVPolje(polje,i,-1)
            vrednost=self.alfabet(polje,globina,order)
            if vrednost<najnizjaVrednost:
                najnizjaVrednost=vrednost
                najboljsaPoteza[0]=i
                najboljsaPoteza[1]=-1
            self.razveljaviPotezo(polje,i)

        return  najboljsaPoteza



    def odigraj(self,order=True):
        """Alfabet poisce najboljso potezo in jo odigra"""
        if igra.konec=="Ne":
            #najprej zaklene kanvas da ga ne motimo ko racuna, ce ne postane zivcen
            gui.plosca.unbind("<Button-1>")
            najboljsaPoteza=[]
            if order:
                najboljsaPoteza=self.najboljsaPotezaO(igra.igralnoPolje,self.tezavnost)
            else:
                najboljsaPoteza=self.najboljsaPotezaC(igra.igralnoPolje,self.tezavnost)
            igra.tip=najboljsaPoteza[1]
            igra.vstaviVPolje(najboljsaPoteza[0])
            gui.narisiTip(igra.tip)
            if igra.konec=="Ne":
                #ce igre ni konec naj se kanvas odpre da odigramo svojo potezo
                gui.plosca.after(20,gui.canvasUnlock)

    def simulacijaIgre(self,order=True):
        """simulira igro med dvema racunalnikoma"""
        if igra.konec=="Ne" and igra.vrstaIgre==4:
            if order:
                mini.odigraj(order)
                gui.plosca.after(100,lambda:self.simulacijaIgre(False))
            else:
                mini.odigraj(False)
                gui.plosca.after(100,lambda:self.simulacijaIgre(True))






    def alfabet(self,veja,globina,a=-1000000000,b=1000000000,maxPlayer=True):
        """navaden algoritem za alfa beta rezanje, ni kaj prevec za povedat"""
        if globina==0 or len(self.veljavnePoteze(veja))==0 and maxPlayer:
            return self.vrednostPolja(veja)
        elif maxPlayer:
            bestValue=-1000000000
            for i in self.veljavnePoteze(veja):
                #proba oba zetona, deepcopy pa zato da nebi slucajno prijatu Max zelel spreminjat pravega igralnega polja
                veja1=copy.deepcopy(veja)
                veja2=copy.deepcopy(veja)
                bestValue=max(self.alfabet(self.vstaviVPolje(veja1,i,1),globina-1,a,b,False),self.alfabet(self.vstaviVPolje(veja2,i,-1),globina-1,a,b,False),bestValue)
                a=max(a,bestValue)
                if b<=a:
                    break
            return bestValue

        else:
            bestValue=+1000000000
            for i in self.veljavnePoteze(veja):
                veja1=copy.deepcopy(veja)
                veja2=copy.deepcopy(veja)
                bestValue=min(self.alfabet(self.vstaviVPolje(veja1,i,1),globina-1,a,b,True),self.alfabet(self.vstaviVPolje(veja2,i,-1),globina-1,a,b,True),bestValue)
                b=min(b,bestValue)
                if b<=a:
                    break
            return bestValue

    def spremeniTezavnost(self,t):
        """Spremeni globino alfabeta"""
        self.tezavnost=t



######################################################################################
#Grafični vmesnik

class GUI():
    #Na zalost nisva naredila tega s spremenljivkami (se pa bi moglo dokaj hitro nardit ce bi zetone resizala)
    #tako da velikost polja je tukaj lahko samo 50
    VelikostPolja=50

    def __init__(self,master):
        
        self.pomoc= None #tukaj je da lahko program pogleda ce je okno z navodili ze odprto
        self.master=master

        #Glavni menu
        menu = tk.Menu(master)
        master.config(menu=menu)

        menu_igra = tk.Menu(menu)
        menu.add_cascade(label="Igra", menu=menu_igra)

        #podmenu za izbiro igre
        menu_igra.add_command(label="Igraj proti prijatelju",command=lambda:self.novaIgra(1))
        menu_igra.add_command(label="Igraj kot Order",command=lambda:self.novaIgra(2))
        menu_igra.add_command(label="Igraj kot Chaos",command=lambda:self.novaIgra(3))
        menu_igra.add_command(label="Simulacija igre",command=lambda:self.novaIgra(4))

        menu_tezavnost=tk.Menu(menu)
        menu.add_cascade(label="Težavnost",menu=menu_tezavnost)

        #podmenu za tezavnost
        menu_tezavnost.add_command(label="Zelo lahko",command=lambda:self.spremeniTezavnost(0))
        menu_tezavnost.add_command(label="Lahko",command=lambda:self.spremeniTezavnost(1))
        menu_tezavnost.add_command(label="Težko",command=lambda:self.spremeniTezavnost(2))
        menu_tezavnost.add_command(label="EXTREME",command=lambda:self.spremeniTezavnost(3))
        menu_tezavnost.add_command(label="EVEN MORE EXTREME",command=lambda:self.spremeniTezavnost(4))

        #podmenu pomoc, kjer najdemo pravila igre
        pomoc_menu = tk.Menu(menu)
        menu.add_cascade(label="Pomoc", menu=pomoc_menu)
        pomoc_menu.add_command(label="Pravila igre", command=lambda:self.pokaziPravila())

        #Igralno območje
        self.plosca = tk.Canvas(master, width=10*GUI.VelikostPolja, height=7*GUI.VelikostPolja)
        self.plosca.bind("<Button-1>",self.odigraj)
        self.plosca.grid(row=2,column=0)
        self.narisiCrte()

        #Stanje igre(kdo je na vrsti, kdo je zmagal,...)
        self.napis = tk.StringVar(master, value="Na vrsti je Order")
        self.napisTezavnost = tk.StringVar(master,value="Težavnost: " + self.kakoLahko(mini.tezavnost))
        tk.Label(master, textvariable=self.napis).grid(row=0,column=0)
        tk.Label(master,textvariable=self.napisTezavnost).grid(row=3,column=0,sticky=SW)

        #zetoni
        self.moder=tk.PhotoImage(file="moder_zeton.gif")
        self.rdec=tk.PhotoImage(file="rdec_zeton.gif")
        self.plosca.create_image(9*self.VelikostPolja,3*self.VelikostPolja,image=self.rdec)

        #pravila
        

    def narisiCrte(self):
        """Narise crte na igralnem obmocju"""
        d=self.VelikostPolja
        #navpicne crte
        self.plosca.create_line(1*d,0*d,1*d,6*d)
        self.plosca.create_line(2*d,0*d,2*d,6*d)
        self.plosca.create_line(3*d,0*d,3*d,6*d)
        self.plosca.create_line(4*d,0*d,4*d,6*d)
        self.plosca.create_line(5*d,0*d,5*d,6*d)
        self.plosca.create_line(6*d,0*d,6*d,6*d)
        self.plosca.create_line(7*d,0*d,7*d,6*d)
        self.plosca.create_line(8*d,0*d,8*d,6*d)
        #vodoravne crte
        self.plosca.create_line(1*d,0*d,8*d,0*d)
        self.plosca.create_line(1*d,1*d,8*d,1*d)
        self.plosca.create_line(1*d,2*d,8*d,2*d)
        self.plosca.create_line(1*d,3*d,8*d,3*d)
        self.plosca.create_line(1*d,4*d,8*d,4*d)
        self.plosca.create_line(1*d,5*d,8*d,5*d)
        self.plosca.create_line(1*d,6*d,8*d,6*d)



    def pokaziPravila(self):
        """napise oziroma zapre pravila"""
        if self.pomoc==None:
            self.pravila = tk.Label(self.master, text=
                            '''Pravila:
Vertical order and chaos je igra za dva igralca, ki se igra na polju
velikosti 7x5, v katerega igralca vstavljata žetone rdeče ali modre barve.
Igralec, ki je na potezi, lahko uporabi en žeton katerekoli barve.
Prvi igralec, imenujmo ga Order, vedno začne igro. Cilj igralca order
je postaviti 5 žetonov enake barve v vrsto, stolpec ali diagonalo.
Cilj drugega igralca, imenujmo ga Chaos, je zapolnitev igralnega polja
na tak način, da v nobeni vrstici, diagonali ali stolpcu ne najdemo
postavljenih petih zaporednih žetonov enake barve.''')
            self.pravila.grid(row=2,column=3,sticky=N+S)
            self.pomoc="Imamo odprta navodila"
            self.pravila.bind("<Button-1>",self.pravilaKlik)
        else:
            self.pomoc=None
            self.pravila.destroy()
            
        
    def pravilaKlik(self,event):
        """zapre pravila"""
        self.pomoc=None
        self.pravila.destroy()
    
    def kakoLahko(self,t):
        """ustvari string za tezavnost"""
        if t==0:
            return "Zelo lahko"
        elif t==1:
            return "Lahko"
        elif t==2:
            return "Težko"
        elif t==3:
            return "EXTREME"
        elif t==4:
            return "EVEN MORE EXTREME"


    def spremeniTezavnost(self,t):
        """Spremeni tezavnost"""
        #spremeni tezavnost v alfabetu
        mini.spremeniTezavnost(t)
        #spremeni napis
        self.napisTezavnost.set("Težavnost: " + self.kakoLahko(mini.tezavnost))



    #vstavi zeton v polje, na to pa da racunalniku potezo (ce je ta v igri)
    def odigraj(self,event):
        j=event.x//50
        if j-1 in mini.veljavnePoteze(igra.igralnoPolje):
                igra.vstaviVPolje(j-1)
                t=igra.vrstaIgre
                if t==2 or t==3:
                    if t==2:
                        self.plosca.after(100,lambda:mini.odigraj(False))

                    else:
                        self.plosca.after(100,lambda:mini.odigraj(True))

        else:
            if igra.tip==1:
                igra.tip=-1
                self.narisiTip(-1)
            elif igra.tip==-1:
                igra.tip=1
                self.narisiTip(1)


    #odklene kanvas
    def canvasUnlock(self):
        self.plosca.bind("<Button-1>",self.odigraj)

    def narisiTip(self,tip):
        """Narise zeton na desni strani kanvasa"""
        d=self.VelikostPolja
        if tip==1:
            self.plosca.create_image(9*d,3*d,image=self.moder)
        if tip==-1:
            self.plosca.create_image(9*d,3*d,image=self.rdec)

    def narisiZeton(self,x,y,tip):
        """Narise zeton na kanvasu na koordinatah x,y"""
        if tip==1:
            self.plosca.create_image(x,y,image=self.moder,tag="zeton") #Tag je tle zato da lahko pobrisemo zetone
        if tip==-1:
            self.plosca.create_image(x,y,image=self.rdec,tag="zeton")

    def novaIgra(self,t):
        """zacne novo igro"""
        #resetira igralno polje
        igra.igralnoPolje=[[0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0]]
        #izbrise zetone
        self.brisi()
        self.napis.set("Na vrsti je Order") #vedno order zacne
        igra.naVrsti="Na vrsti je Order"
        #nastavi vrsto igre
        igra.vrstaIgre=t
        igra.konec="Ne"
        self.plosca.bind("<Button-1>",self.odigraj)
        if t==3:
            self.plosca.after(50,mini.odigraj())
        if t==4:
            mini.simulacijaIgre()


    def brisi(self):
        self.plosca.delete("zeton")
        




######################################################################
## Glavni program


mini=AlfaBet()

root=tk.Tk()
root.title("Order and Chaos")

gui=GUI(root)

igra=Igra()

root.mainloop()



