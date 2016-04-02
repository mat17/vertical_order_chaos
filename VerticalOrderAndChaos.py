import tkinter as tk
import copy


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
        vrstica=5
        while vrstica>=0:
            if self.igralnoPolje[vrstica][stolpec]==0:
                self.igralnoPolje[vrstica][stolpec]=self.tip
                gui.narisiZeton((stolpec+1)*50+25,vrstica*50+25,self.tip)
                if self.naVrsti=="Na vrsti je Order":
                    self.naVrsti="Na vrsti je Chaos"
                    gui.napis.set(self.naVrsti)
                else:
                    self.naVrsti="Na vrsti je Order"
                    gui.napis.set(self.naVrsti)
                self.stanjeIgre()    
                break
            else: vrstica-=1    

    def vstolpec(self,j):
        """Naredi seznam stolpca."""
        return [self.igralnoPolje[i][j] for i in range(6)]
                    
    def stanjeIgre(self):
        
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
            gui.napis.set("Zmagal je CHAOS !")
            self.konec="Da"
            
            




#veliki mojster iger, gospod Dr. Alfa Bet, tudi poznan kot algoritem alfa beta rezanje
class AlfaBet():
    
    def __init__(self):
        self.tezavnost=0
    
    def vrednostPogoja(self,kombinacija):
        """poisce vrednost vrstice/diagonale/stolpca, zaenkrat se zelo ogabna verzija"""
        l=len(set(kombinacija))
        if l==1 and 0 not in kombinacija:
            return 440000000000000
        elif l==2 and 0 not in kombinacija:
            return -100000
        elif l==2:
            return 10*abs(sum(kombinacija))
        elif l==3:
            return -100000
        else:
            return 0
        
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
            if len(dia)==6:
                kombinacijeDiagonale+=[dia[:5]]+[dia[1:]]
            else:
                kombinacijeDiagonale+=[dia]
                

        stolpci=[self.vstolpec(polje,j) for j in range(7)]
        kombinacijeStolpci=[]
        for s in stolpci:
            kombinacijeStolpci+=[s[:5]]+[s[1:]]
        
        vrstice=[polje[i] for i in range(6)]
        kombinacijeVrstice=[]
        for v in vrstice:
            kombinacijeVrstice+=[v[:5]]+[v[1:6]]+[v[2:]]
        
        kombinacije=kombinacijeDiagonale+kombinacijeStolpci+kombinacijeVrstice
        
        return sum([self.vrednostPogoja(kombinacija) for kombinacija in kombinacije])


    def veljavnePoteze(self,polje):
        veljavne=[]
        for i in range(7):
            if polje[0][i]==0:
                veljavne.append(i)
        return veljavne        

    def razveljaviPotezo(self,polje,stolpec):
        vrstica=0
        while 0<6:
            if polje[vrstica][stolpec]!=0:
                polje[vrstica][stolpec]=0
                break
            else: vrstica+=1
            
        
    #najboljsa ptoeza za order      
    def najboljsaPotezaO(self,polje,globina):
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
    
    #najboljsa poteza za chaos
    def najboljsaPotezaC(self,polje,globina,order=False):
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
                najboljsaPoteza[0]=i
                najboljsaPoteza[1]=-1
            self.razveljaviPotezo(polje,i)
        return  najboljsaPoteza
    

    
    #alfabet poisce najboljso potezo in jo uporabi, pred tem se "zaklene" kanvas da ga ne motimo
    def odigraj(self,order=True):
        if igra.konec=="Ne":
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
                gui.plosca.after(20,gui.canvasUnlock)
                
    def simulacijaIgre(self,order=True):
        if igra.konec=="Ne":
            if order:
                mini.odigraj(order)
                gui.plosca.after(100,lambda:self.simulacijaIgre(False))
            else:
                mini.odigraj(False)
                gui.plosca.after(100,lambda:self.simulacijaIgre(True))




           
#za zdej naj bo kot da igra order (zato maxplayer=true)       
    def alfabet(self,veja,globina,a=-1000000000,b=1000000000,maxPlayer=True):
        if globina==0 or len(self.veljavnePoteze(veja))==0:
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
        self.tezavnost=t



  
class GUI():
    #Na zalost nisva naredila tega s spremenljivkami (se pa bi moglo dokaj hitro nardit ce bi zetone resizala)
    VelikostPolja=50
    
    def __init__(self,master):


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
        menu_tezavnost.add_command(label="Zelo lahko",command=lambda:mini.spremeniTezavnost(0))
        menu_tezavnost.add_command(label="Lahko",command=lambda:mini.spremeniTezavnost(1))
        menu_tezavnost.add_command(label="Težko",command=lambda:mini.spremeniTezavnost(2))
        menu_tezavnost.add_command(label="EXTREME",command=lambda:mini.spremeniTezavnost(3))
        menu_tezavnost.add_command(label="EVEN MORE EXTREME",command=lambda:mini.spremeniTezavnost(4))
        
        
        #Stanje igre(kdo je na vrsti, kdo je zmagal,...)
        self.napis = tk.StringVar(master, value="Na vrsti je Order")
        tk.Label(master, textvariable=self.napis).grid(row=0, column=0)

        #Igralno območje
        self.plosca = tk.Canvas(master, width=10*GUI.VelikostPolja, height=7*GUI.VelikostPolja)
        self.plosca.bind("<Button-1>",self.odigraj)
        self.plosca.grid(row=1,column=0)
        self.narisiCrte()
        
        

        #zetoni
        self.moder=tk.PhotoImage(file="moder_zeton.gif")
        self.rdec=tk.PhotoImage(file="rdec_zeton.gif")
        self.plosca.create_image(9*self.VelikostPolja,3*self.VelikostPolja,image=self.rdec)
       

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
        
        
    #odklene kanvas ko racunalnik odigra            
    def canvasUnlock(self):
        self.plosca.bind("<Button-1>",self.odigraj)

    
    
    
    def narisiCrte(self):
        """Narise crte na igralnem obmocju"""
        d=self.VelikostPolja
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
       
        
        
        
        
   
    def narisiTip(self,tip):
        d=self.VelikostPolja
        if tip==1:
            self.plosca.create_image(9*d,3*d,image=self.moder)
        if tip==-1:
            self.plosca.create_image(9*d,3*d,image=self.rdec)

    def narisiZeton(self,x,y,tip):
        if tip==1:
            self.plosca.create_image(x,y,image=self.moder,tag="zeton")
        if tip==-1:
            self.plosca.create_image(x,y,image=self.rdec,tag="zeton")
            
    def novaIgra(self,t):
        igra.igralnoPolje=[[0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0]]
        self.brisi()
        self.napis.set("Na vrsti je Order")
        igra.vrstaIgre=t
        igra.konec="Ne"
        self.plosca.bind("<Button-1>",self.odigraj)
        if t==3:
            mini.odigraj()
        if t==4:
            mini.simulacijaIgre()

            
    def brisi(self):
        self.plosca.delete("zeton")

    



        

mini=AlfaBet()

root=tk.Tk()
root.title("Order and Chaos")

gui=GUI(root)

igra=Igra()

root.mainloop()



