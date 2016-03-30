import tkinter as tk
import copy
import time



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

    def vstaviVPolje(self,stolpec):
        """Stevilo stolpca od 0-6."""
        vrstica=5
        while vrstica>=0:
            if self.igralnoPolje[vrstica][stolpec]==0:
                self.igralnoPolje[vrstica][stolpec]=self.tip
                gui.narisiZeton((stolpec+1)*50+25,vrstica*50+25,self.tip)
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



class MiniMax():

    
    def vrednostPogoja(self,kombinacija):
        """poisce vrednost vrstice/diagonale/stolpca, zaenkrat se zelo ogabna verzija"""
        l=len(set(kombinacija))
        if l==1 and 0 not in kombinacija:
            return 4400000
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
            
        
          
    def najboljsaPoteza(self,polje,globina,order=True):
        najvisjaVrednost=-100000000000000
        najboljsaPoteza=[-5,0]
        for i in self.veljavnePoteze(polje):
            #poskusi z rdecim zetonom
            self.vstaviVPolje(polje,i,1)
            vrednost=self.minimax(polje,globina,order)
            if vrednost>najvisjaVrednost:
                najvisjaVrednost=vrednost
                najboljsaPoteza[0]=i
                najboljsaPoteza[1]=1
            self.razveljaviPotezo(polje,i)
            #poskusi z modrim zetonom
            self.vstaviVPolje(polje,i,-1)
            vrednost=self.minimax(polje,globina,order)
            if vrednost>najvisjaVrednost:
                najboljsaPoteza[0]=i
                najboljsaPoteza[1]=-1
            self.razveljaviPotezo(polje,i)
        return  najboljsaPoteza

    def najboljsaPotezaC(self,polje,globina,order=False):
        najnizjaVrednost=10000000000000000
        najboljsaPoteza=[-5,0]
        for i in self.veljavnePoteze(polje):
            #poskusi z rdecim zetonom
            self.vstaviVPolje(polje,i,1)
            vrednost=self.minimax(polje,globina,order)
            if vrednost<najnizjaVrednost:
                najnizjaVrednost=vrednost
                najboljsaPoteza[0]=i
                najboljsaPoteza[1]=1
            self.razveljaviPotezo(polje,i)
            #poskusi z modrim zetonom
            self.vstaviVPolje(polje,i,-1)
            vrednost=self.minimax(polje,globina,order)
            if vrednost<najnizjaVrednost:
                najboljsaPoteza[0]=i
                najboljsaPoteza[1]=-1
            self.razveljaviPotezo(polje,i)
        return  najboljsaPoteza
    

    
    #ta je tle za testiranje 
    def odigraj(self):
        najboljsaPoteza=self.najboljsaPoteza(igra.igralnoPolje,2)
        igra.tip=najboljsaPoteza[1]
        igra.vstaviVPolje(najboljsaPoteza[0])





#bova sla do profesorja da malo pohejta nas spaghetti code :D            
#za zdej naj bo kot da igra order (zato maxplayer=true)       
    def minimax(self,veja,globina,maxPlayer=True):
        if globina==0 or len(self.veljavnePoteze(veja))==0:
            return self.vrednostPolja(veja)
        elif maxPlayer:
            bestValue=-1000000000
            for i in self.veljavnePoteze(veja):
                #proba oba zetona, nas ne zanima kam bi jih igral tako da nima smisla jih shranit
                veja1=copy.deepcopy(veja)
                veja2=copy.deepcopy(veja)
                bestValue=max(self.minimax(self.vstaviVPolje(veja1,i,1),globina-1,False),self.minimax(self.vstaviVPolje(veja2,i,-1),globina-1,False))
            return bestValue    

        else:
            bestValue=+1000000000
            for i in self.veljavnePoteze(veja):
                veja1=copy.deepcopy(veja)
                veja2=copy.deepcopy(veja)
                bestValue=min(self.minimax(self.vstaviVPolje(veja1,i,1),globina-1,True),self.minimax(self.vstaviVPolje(veja2,i,-1),globina-1,True))
            return bestValue    




  
class GUI():

    VelikostPolja=50
    TAG_OKVIR='okvir'
    
    def __init__(self,master):


        #Glavni menu
        menu = tk.Menu(master)
        master.config(menu=menu)

        menu_igra = tk.Menu(menu)
        menu.add_cascade(label="Igra", menu=menu_igra)

        menu_uredi=tk.Menu(menu)
        menu.add_cascade(label="Uredi", menu=menu_uredi)

        #podmenu za izbiro igre
        menu_igra.add_command(label="Igraj proti prijatelju",command=self.novaIgra)
        menu_igra.add_command(label="Igraj kot Order")
        menu_igra.add_command(label="Igraj kot Chaos")
        menu_igra.add_command(label="Simulacija igre",command=lambda:self.narisiZeton(250,250,2))

        #podmenu za urejanje velikosti okna
        menu_uredi.add_command(label="Majhno okno",command=lambda:self.spremeniVelikost(15))
        menu_uredi.add_command(label="Srednje okno",command=lambda:self.spremeniVelikost(30))
        menu_uredi.add_command(label="Veliko okno",command=lambda:self.spremeniVelikost(50))
        


        #Stanje igre(kdo je na vrsti, kdo je zmagal,...)
        self.napis = tk.StringVar(master, value="Chaos na vrsti")
        tk.Label(master, textvariable=self.napis).grid(row=0, column=0)

        #Igralno območje
        self.plosca = tk.Canvas(master, width=10*GUI.VelikostPolja, height=7*GUI.VelikostPolja)
        self.plosca.bind("<Button-1>",self.odigraj)
        self.plosca.grid(row=1,column=0)
        self.narisiCrte()
        
        

        #zetoni
        self.moder=tk.PhotoImage(file="moder_zeton.gif")
        self.rdec=tk.PhotoImage(file="rdec_zeton.gif")
        self.plosca.create_image(450,150,image=self.rdec)
       


    def odigraj(self,event):
        j=event.x//50
        if j-1 in mini.veljavnePoteze(igra.igralnoPolje):
                igra.vstaviVPolje(j-1)
                self.napis.set("Računalnik razmišlja!")
                self.plosca.after(100,mini.odigraj)
                self.narisiTip(igra.tip)
        else:
            if igra.tip==1:
                igra.tip=-1
                self.narisiTip(-1)
            elif igra.tip==-1:
                igra.tip=1
                self.narisiTip(1)
        
                
                    

    
    
    
    def narisiCrte(self):
        """Narise crte na igralnem obmocju"""
        #self.plosca.delete(Gui.TAG_OKVIR) ali je to sploh potrebno?
        d=GUI.VelikostPolja
        #navpicne crte 
        self.plosca.create_line(1*d,0*d,1*d,6*d,tag=GUI.TAG_OKVIR)
        self.plosca.create_line(2*d,0*d,2*d,6*d,tag=GUI.TAG_OKVIR)
        self.plosca.create_line(3*d,0*d,3*d,6*d,tag=GUI.TAG_OKVIR)
        self.plosca.create_line(4*d,0*d,4*d,6*d,tag=GUI.TAG_OKVIR)
        self.plosca.create_line(5*d,0*d,5*d,6*d,tag=GUI.TAG_OKVIR)
        self.plosca.create_line(6*d,0*d,6*d,6*d,tag=GUI.TAG_OKVIR)
        self.plosca.create_line(7*d,0*d,7*d,6*d,tag=GUI.TAG_OKVIR)
        self.plosca.create_line(8*d,0*d,8*d,6*d,tag=GUI.TAG_OKVIR)
        #vodoravne crte
        self.plosca.create_line(1*d,0*d,8*d,0*d,tag=GUI.TAG_OKVIR)
        self.plosca.create_line(1*d,1*d,8*d,1*d,tag=GUI.TAG_OKVIR)
        self.plosca.create_line(1*d,2*d,8*d,2*d,tag=GUI.TAG_OKVIR)
        self.plosca.create_line(1*d,3*d,8*d,3*d,tag=GUI.TAG_OKVIR)
        self.plosca.create_line(1*d,4*d,8*d,4*d,tag=GUI.TAG_OKVIR)
        self.plosca.create_line(1*d,5*d,8*d,5*d,tag=GUI.TAG_OKVIR)
        self.plosca.create_line(1*d,6*d,8*d,6*d,tag=GUI.TAG_OKVIR)
       
        
        
        
        
   
    def narisiTip(self,tip):
        if tip==1:
            self.plosca.create_image(450,150,image=self.moder)
        if tip==-1:
            self.plosca.create_image(450,150,image=self.rdec)

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
        self.napis.set("Igra order")
            
    def brisi(self):
        self.plosca.delete("zeton")

    
    def spremeniVelikost(self,velikost):
        """spremeni velikost polja"""                       
        GUI.VelikostPolja=velikost
        self.narisiCrte()
    


        
        
    

mini=MiniMax()

root=tk.Tk()
root.title("Order and Chaos")

gui=GUI(root)

igra=Igra()

root.mainloop()

polje=[[0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]]

