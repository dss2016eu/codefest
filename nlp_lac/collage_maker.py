# crear un texto con un parrafo de cada lengua
import glob
import random
from random import randint


dokeus=glob.glob("eus/*")
dokcas=glob.glob("cas/*")
dokcat=glob.glob("cat/*")
dokdeu=glob.glob("deu/*")
dokpot=glob.glob("pot/*")
dokeng=glob.glob("eng/*")
dokit=glob.glob("it/*")
dokgal=glob.glob("gal/*")
doknl=glob.glob("nl/*")
dokfra=glob.glob("fra/*")

texts = [
random.choice(dokeus),
random.choice(dokcas),
random.choice(dokcat),
random.choice(dokdeu),
random.choice(dokpot),
random.choice(dokeng),
random.choice(dokit),
random.choice(dokgal),
random.choice(doknl),
random.choice(dokfra),
]




random.shuffle(texts)




for text in texts:
    f = open(text)
    for line in f:
        print(line)
    f.close()
    print
