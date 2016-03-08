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







igra=Igra()
