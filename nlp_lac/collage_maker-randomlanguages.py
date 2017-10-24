# escoge un numero random de lenguas y elige al azar un parrafo de cada

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
dokeus,
dokcas,
dokcat,
dokdeu,
dokpot,
dokeng,
dokit,
dokgal,
doknl,
dokfra,
]




random.shuffle(texts)

kopurua = random.randint(1,9)

for langindex in xrange(kopurua+1):
   lang=random.choice(texts)
   text=random.choice(lang) 

   f = open(text)
   for line in f:
       print(line)
   f.close()
   print
