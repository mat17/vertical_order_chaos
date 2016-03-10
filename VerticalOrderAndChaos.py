import tkinter as tk

class Igra():
    def __init__(self):
        self.igralnoPolje=[[0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0]]
        """Tip je barva zetona."""             
        self.tip=0

    def vstaviVPolje(self,stolpec):
        """Število stolpca od 0-6."""
        vrstica=5
        while vrstica>=0:
            if self.igralnoPolje[vrstica][stolpec]==0:
                self.igralnoPolje[vrstica][stolpec]=self.tip
                break
            else: vrstica-=1

    def vstolpec(self,j):
        """Kliče stolpec, ki nas zanima."""
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
        
        pogoji=diagonale+stolpci+vrstice
##pogoji verjetno niso vec potrebni, ampak ne vem, kaj bova naredila z vsemi
##funkcijami, ki se ukvarjajo s pogoji. zato jih bom zaenkrat pustil pri miru.
##konec koncev so zaenkrat uporabni za "ta grd" minimax
        kombinacije=kombinacijeDiagonale+kombinacijeStolpci+kombinacijeVrstice

        for pogoj in pogoji:
            counter=0
            tip=pogoj[0]
            for zeton in pogoj:
                if zeton==tip:
                    counter+=1
                    if counter==5 and zeton is not 0:
                        print("ZMAGA")
                else:
                    counter=1
                    tip=zeton 
        return print(kombinacije)


class MiniMax():
#moreva se se odlocit ce bo minimax imel svoje polje oziroma kje ga bo urejal.
#problem 1,0,0,2,0,0,1 
    
    def vrednostPogoja(self,pogoj):
        """poisce vrednost vrstice/diagonale/stolpca, zaenkrat se zelo ogabna verzija"""
        MaxCounter=0
        counter=0
        tip=pogoj[0]
        for zeton in pogoj:
            if zeton==0:
                """stevilo praznih polj v nekem zaporedju bo shranjeno v decimalki"""
                counter+=0.1
                if counter>MaxCounter:
                    MaxCounter=counter
            elif zeton!=tip:
                if tip==0:
                    """ce se slucajno zgodi da je nas trenuten tip 0,
                    bo vseeno kateri zeton je, zato se counter poveca za 1, tip pa nastavimo na trenuten zeton"""
                    counter+=1
                    tip=zeton
                    if counter>MaxCounter:
                        MaxCounter=counter
                else:
                    if counter>MaxCounter:
                        MaxCounter=counter
                    else:
                        counter=1
                        tip=zeton
            elif zeton==tip:
                counter+=1
                if counter>MaxCounter:
                    MaxCounter=counter
                if counter>=5:
                    MaxCounter=counter*10
                    
        """c=število prostih mest v najboljsem "zaporedju" """
        c=10*(MaxCounter%1)
        """če je več kot 5 pomeni da imamo se moznost za 5 v vrsto"""
        if MaxCounter + c>=5:
            return MaxCounter//1 * 100 + c*10
        """če je <5 pomeni da nemoremo vec dobiti 5 v vrsto"""
        return 0


        
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
        vrednost=0
        diagonale=[]            
        for d in diagonalePolja:
            diagonala=[]
            for e in d:
                (i,j)=e
                diagonala.append(polje[i][j])
            diagonale.append(diagonala)

        stolpci=[self.vstolpec(polje,j) for j in range(7)]
        vrstice=[polje[i] for i in range(6)]

        pogoji=diagonale+stolpci+vrstice
        
        return sum([self.vrednostPogoja(pogoj) for pogoj in pogoji])
        
        

class GUI():
    def __init__(self,master,globina):
        
        #privzeta velikost polja
        VelikostPolja=30
        TAG_OKVIR='okvir'

        #Glavni menu
        menu = tk.Menu(master)
        master.config(menu=menu)

        menu_igra = tk.Menu(menu)
        menu.add_cascade(label="Igra", menu=menu_igra)

        menu_uredu=tk.Menu(menu)
        menu.add_cascade(label="Uredi", menu=menu_uredi)

        #podmenu za izbiro igre
        menu_igra.add_command(label="Igraj proti prijatelju")
        menu_igra.add_command(label="Igraj kot Order")
        menu_igra.add_command(label="Igraj kot Chaos")
        menu_igra.add_command(label="Simulacija igre")

        #podmenu za urejanje velikosti okna
        menu_uredi.add_command(label="Majhno okno",command=lambda:self.spremeniVelikost(15))
        menu_uredi.add_command(label="Srednje okno",command=lambda:self.spremeniVelikost(30))
        menu_uredi.add_command(label="Veliko okno",command=lambda:self.spremeniVelikost(50))
        


        #Stanje igre(kdo je na vrsti, kdo je zmagal,...)
        self.napis = tk.StringVar(master, value="blah")
        tk.Label(master, textvariable=self.napis).grid(row=0, column=0)

        #Igralno območje
        self.plosca = tk.Canvas(master, width=10*VelikostPolja, height=7*VelikostPolja)

    def narisiCrte(self):
        """Narise crte na igralnem obmocju"""
        #self.plosca.delete(Gui.TAG_OKVIR) ali je to sploh potrebno?
        d=GUI.VelikostPolja
        #navpicne crte
        self.plosca.create_line(0*d,0*d,0*d,7*d,tag=Gui.TAG_OKVIR)
        self.plosca.create_line(1*d,0*d,1*d,7*d,tag=Gui.TAG_OKVIR)
        self.plosca.create_line(2*d,0*d,2*d,7*d,tag=Gui.TAG_OKVIR)
        self.plosca.create_line(3*d,0*d,3*d,7*d,tag=Gui.TAG_OKVIR)
        self.plosca.create_line(4*d,0*d,4*d,7*d,tag=Gui.TAG_OKVIR)
        self.plosca.create_line(5*d,0*d,5*d,7*d,tag=Gui.TAG_OKVIR)
        self.plosca.create_line(6*d,0*d,6*d,7*d,tag=Gui.TAG_OKVIR)
        self.plosca.create_line(7*d,0*d,7*d,7*d,tag=Gui.TAG_OKVIR)
        #vodoravne crte
        self.plosca.create_line(0*d,0*d,8*d,0*d,tag=Gui.TAG_OKVIR)
        self.plosca.create_line(0*d,1*d,8*d,1*d,tag=Gui.TAG_OKVIR)
        self.plosca.create_line(0*d,2*d,8*d,2*d,tag=Gui.TAG_OKVIR)
        self.plosca.create_line(0*d,3*d,8*d,3*d,tag=Gui.TAG_OKVIR)
        self.plosca.create_line(0*d,4*d,8*d,4*d,tag=Gui.TAG_OKVIR)
        self.plosca.create_line(0*d,5*d,8*d,5*d,tag=Gui.TAG_OKVIR)
        self.plosca.create_line(0*d,6*d,8*d,6*d,tag=Gui.TAG_OKVIR)

    def spremeniVelikost(self,velikost):
        """spremeni velikost polja"""                       
        self.VelikostPolja=velikost
    


mini=MiniMax()




igra=Igra()



polje=[[0, 1, 2, 0, 1, 2, 0],
        [0, 2, 2, 0, 1, 1, 0],
        [0, 1, 1, 0, 2, 1, 0],
        [0, 1, 2, 0, 1, 2, 0],
        [0, 1, 1, 1, 2, 1, 0],
        [1, 2, 1, 1, 2, 1, 1]]
