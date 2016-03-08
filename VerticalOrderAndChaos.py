##predlagam poenotenje nacina poimenovanja funkcij
##zdaj imava prevec (3) nacinov
##- s podcrtajem (stanje_igre)
## - vse crke z malo (vstolpec)
## - zacetki besed z veliko (vstaviVStolpec)

import tkinter

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
                    
    def stanje_igre(self):
        
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

        stolpci=[self.vstolpec(j) for j in range(7)]
        vrstice=[self.igralnoPolje[i] for i in range(6)]

        pogoji=diagonale+stolpci+vrstice

        for pogoj in pogoji:
            counter=0
            tip=pogoj[0]
            for zeton in pogoj:
                if zeton==tip:
                    counter+=1
                    if counter==5 and zeton is not 0:
##sem dodal "and zeton is not 0", da ne kaze praznih "pogojev" kakor zmage
                        print("ZMAGA")
                else:
                    counter=1
##prej je blo counter=0 in ni blo dobro, ker je ignoriralo prvi zeton novega tipa :)
                    tip=zeton 
        return print(diagonale)


class MiniMax():
#moreva se se odlocit ce bo minimax imel svoje polje oziroma kje ga bo urejal.

    
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
        
        




mini=MiniMax()




igra=Igra()



polje=[[0, 1, 2, 0, 1, 2, 0],
        [0, 2, 2, 0, 1, 1, 1],
        [0, 1, 1, 0, 2, 1, 0],
        [0, 1, 2, 0, 1, 2, 0],
        [0, 1, 1, 1, 2, 1, 0],
        [1, 2, 1, 1, 2, 1, 1]]
