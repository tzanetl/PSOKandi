# Parveilualgoritmi
# Taneli Leppanen

# Ohjelman alustaminen tapahtuu asettamalla halutut parametrit main, laske_fitness ja
# laske_sakko -funktioihin.

from random import uniform
from random import random
##import matplotlib.pyplot as plt
import time


# Partikkeli luokan maarittely
class Partikkeli:
    gbest = None
    fbest = None

    def __init__(self, nvars):
        self.__piste = []
        self.__pbest = []
        self.__fitness = 0                            # Kohdefunktion arvo kierroksella
        self.__nopeus = [0 for v in range(nvars)]    # Nopeus kierroksella

    # Print komentoa varten
    def __str__(self):
        return "Piste: " + str(self.__piste) + "\npbest: " + str(self.__pbest) +\
               "\nFitness: " + str(self.__fitness) + "\nNopeus: " + str(self.__nopeus) +\
                "\nGbest: " + str(Partikkeli.gbest) + "\nFbest: " \
               +  str(Partikkeli.fbest) + "\n"


    # Alustaa patikkelin lahtopisteen
    def alusta(self, nvars, x_min, x_max):
        self.__nopeus = [0 for nopeus in range(nvars)]

        for i in range(nvars):
            x = uniform(x_min[i], x_max[i])
            self.__piste.append(x)

        self.__pbest += self.__piste

    # Laskee pisteen sopivuuden
    def sopivuus(self, x_min, x_max):
        fitness = laske_fitness(self.__piste)
        sakko = laske_sakko(self.__piste, x_min, x_max, False)
        self.__fitness = 0 + fitness + sakko

        if Partikkeli.fbest == None:
            Partikkeli.gbest = [] + self.__piste
            Partikkeli.fbest = 0 + self.__fitness

        elif self.__fitness < Partikkeli.fbest:
            Partikkeli.gbest = [] + self.__piste
            Partikkeli.fbest = 0 + self.__fitness


    # Laskee partikkelin nopeuden kierroksella
    def nopeus(self, w, c1, c2, v_max, nvars):
        nopeus_uusi = []

        for i in range(nvars):

            v_uusi = w*self.__nopeus[i] + \
                     random()*c1*(self.__pbest[i] - self.__piste[i]) + \
                     random()*c2*(Partikkeli.gbest[i] - self.__piste[i])

            if abs(v_uusi) > v_max:

                if v_uusi < 0:
                    v_uusi = 0 - v_max

                else:
                    v_uusi = 0 + v_max

            nopeus_uusi.append(v_uusi)

        self.__nopeus = [] + nopeus_uusi


    # Paivittaa partikkelin sijainnin
    def paivita(self, nvars, kokonaislk):

        for i in range(nvars):
            self.__piste[i] += self.__nopeus[i]

        if kokonaislk is True:

            for i in range(len(self.__piste)):
                self.__piste[i] = round(self.__piste[i])


    def hae_paras_fitness(self):
        return Partikkeli.fbest

    def tulosta_tulokset(self):
        param = [1 for i in range(len(Partikkeli.gbest))]
        ehdot = laske_sakko(Partikkeli.gbest, param, param, True)

        print("x = \n   " + str(Partikkeli.gbest) + "\nfval = \n   " + str(Partikkeli.fbest) + "\n")

        for i in range(len(ehdot)):
            print("g(" + str(i + 1) + ") = " + str(ehdot[i]))
        print()

# Alustaa kaikki paven alkio kutsumalla Partikkeli luokan metodia alusta
def alusta_parvi(koko, x_min, x_max, nvars):
    parvi = []

    for i in range(koko):
        partikkeli = Partikkeli(nvars)
        partikkeli.alusta(nvars, x_min, x_max)
        partikkeli.sopivuus(x_min, x_max)
        parvi.append(partikkeli)

    return parvi

# Laskee inertiapainotukset halutulla strategialla
fbest_ed = None
dyn_count = 0

def laske_inertia(w, w_min, w_max, w_type, w_kerroin, dyn_raja, max_iter, k, fbest):

    if w_type == "lin":
        w = w_max - (((w_max - w_min) / max_iter)*k)

    else:
        global fbest_ed
        global dyn_count

        if fbest_ed is None or fbest_ed <= fbest:
            dyn_count += 1

        else:
            fbest_ed = fbest
            dyn_count = 0

        if dyn_count >= dyn_raja:
            w = w*w_kerroin

    return w


# Kohdefunktion maarittely ja lasku
def laske_fitness(x):
    fitness = (2 ** 0.5) * 1000 * (x[0] + x[1])
    return fitness


# Laskee mahdollisen sakko termin suusuuden
# Ehdot maaritellaan G(x) <= 0
def laske_sakko(x, x_min, x_max, tulos):

    try:
        R = 10000000

        ehdot = [((2 * (2 ** 0.5) * 1000 * (x[0] + x[1]) * 10000) /
                 (210000 * (4*x[0]*x[1]) + 4 * x[0] * x[1])) - 0.5,
                 ((2 * (2 ** 0.5) * 1000 * (x[0] - x[1]) * 10000) /
                 (210000 * (4*x[0]*x[1]))) - 1
                 ]


        sakko = 0

        for g in ehdot:

            if g > 0:
                sakko += R*g

        for i in range(len(x)):

            if x[i] > x_max[i]:
                sakko += R*(x[i] - x_max[i])

            elif x[i] < x_min[i]:
                sakko += R*(x_min[i] - x[i])

        if tulos is not True:
            return sakko
        else:
            return ehdot

    except ZeroDivisionError:
        return R*10000


def main():

    t0 = time.time()

    nvars = 2
    iter_max = 350
    x_min = [80, 80]
    x_max = [180, 180]
    v_max = 10000000
    koko = 20

    # Aseta w_type inertiakertoimen määritys strategia
    # vak(vakio kerroin) / lin(lineaarinen) / dyn(dynaaminen)
    w = 0.789
    w_max = 0.8
    w_min = 0.5
    w_kerroin = 0.95
    w_type = "lin"
    dyn_raja = 10
    c1 = 0.97
    c2 = 1.47

    plot = False
    kokonaislk = False


    parvi = alusta_parvi(koko, x_min, x_max, nvars)
    fbest_list = []

    for k in range(iter_max):

        for partikkeli in parvi:
            partikkeli.nopeus(w, c1, c2, v_max, nvars)
            partikkeli.paivita(nvars, kokonaislk)
            partikkeli.sopivuus(x_min, x_max)

        fbest = parvi[0].hae_paras_fitness()
        fbest_list.append(fbest)

        if not w_type == "vak":
            w = laske_inertia(w, w_min, w_max, w_type, w_kerroin, dyn_raja, iter_max, k, fbest)


    parvi[0].tulosta_tulokset()
    t1 = time.time()
    print("Ajoaika: " + str(t1 - t0))

    if plot is True:
        plt.cla()
        plt.plot(fbest_list, marker = 'o', c = 'k', ms = 2)
        plt.ylabel('fbest')
        plt.show()
        osoite = "E:\Dropbox\Kandi\PSO Logs\kuvaSAUVVA_" + str(time.strftime("%H%M%S")) + ".png"
        plt.savefig(osoite)


main()
