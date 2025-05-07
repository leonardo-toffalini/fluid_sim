# Presentation outline
<img width="484" alt="Screenshot 2025-05-06 at 9 57 26" src="https://github.com/user-attachments/assets/6af3d8c1-0798-4269-95c5-fb99d894d7b1" />

### Motivation
Miért fontos a hallgatónak az előadas témája?
A folyadék áramlása a hétköznapokban körül vesz minket pl. felszálló füst, felhők, köd, folyók, óceánok áramlása. Ezeket a jelenségeket a Naiver-Stokes egyenletek írnak le, melyek a folyadékáramlás fizikájáról szólnak. Ezekről az egyenletekről a későbbiekben lesz szó. Az ilyen típusú szimulációkat a való életben is használnak, de azok a fizikai pontosságra törekszenek. (Ezek időigényesek, bonyolultak.) Azonban indokolt, hogy a pontosságra törekszenek, mivel pl egy repülőgépen fontos, hogy pl. a légellenállást pontosan meghatározzák. A mi modellünkben a cél, ahogy a cikkben is, hogy a vizualizáció meggyőzően nézzen ki és gyors legyen. A projektben az optimalizációra fektettük a hangsúlyt. 
Kedvcsináló:
https://paveldogreat.github.io/WebGL-Fluid-Simulation/


### Navier-Stokes equations
Elmagyarázzuk nagyvonalakban a Navier-Stokes egyenleteket, és hogy mit jelentenek:
Ez a két egyenlet írja le a folyékony anyagok mozgását, áramlását. A fenti egyenlet a sebességre vonatkozik, míg a lenti a sűrűségre. Mindkét egyenlet rendre a sebesség, illetve a sűrűség idő szerinti változását írja le, mely a következő komponensekből áll össze:  \
$$\frac{\partial u}{\partial t} = -(u \cdot \nabla) u+\nu \nabla^2 u+\mathbf{f}$$ esetén: \
$$u$$: sebesség; $$-(u \cdot \nabla)u$$: folyadék elmozdulása; $$\nu \nabla^2 u$$: diffuzió; $$\mathbf{f}$$: külső hatás, forrás (pl.szél). \
A folyadék elmozdulásáért az $$\texttt{advect()}$$, a diffúzióért a $$\texttt{diff()}$$, a külső hatásért a $$\texttt{add source()}$$ függvény felel a kódban. \
$$\frac{\partial \rho}{\partial t} = -(u \cdot \nabla) \rho+\kappa \nabla^2 \rho+S$$ \
$$\rho$$: sűrűség; $$-(u \cdot \nabla) \rho$$: sűrűség elmozdulása; $$\kappa \nabla^2 \rho$$: diffúzió; $$S$$: külső hatás, forrás (pl.festék befecskendezése) \
A kódban az előző esethez hasonlóan alakulnak a függvények, melyeket a későbbiekben részletesen kifejtünk.  
The following two partial differential equations characterize fluids. Our goal is to solve these equations to simulate the behaviour of fluids.

$$\frac{\partial u}{\partial t} = -(u \cdot \nabla) u+\nu \nabla^2 u+\mathbf{f}$$

$$\frac{\partial \rho}{\partial t} = -(u \cdot \nabla) \rho+\kappa \nabla^2 \rho+S$$

### Kiindulás
A szimulációt egy véges térben fogjuk implementálni, erre gondolhatunk úgy, mint egy négyzetre, amit felosztunk cellákra, majd az összes cella középpontjában mintát teszünk a folyadékból. A vizsgált tartomány köré fogunk készíteni egy "falat", hogy a folyékony anyag ne tudjon kifolyni, illetve a határok kezelésének egyszerűsítése céljából. Tehát kiindulunk egy kezdeti sűrűségből.
![image](https://github.com/user-attachments/assets/8c33e212-30e2-4b7b-b0fe-86244361bb24)

### Diagram of the flow of the simulation
Elmagyarázzuk a mile-high lépéseit a szimulációnak \
![image](https://github.com/user-attachments/assets/db3dd9c7-5ba0-4644-989c-4b222779a90e) \
Ezen az ábrán a szimuláció lépései láthatók, melyeket a Navier-Stokes egyenlet jobb oldalán láthatunk. 
1. Add source
2. Dense step
3. Vel step

### Dense step
A sűrűségmező update-telő függvénye. Az alábbi függvényekből áll elő:
1. Add source
2. Diffuse
3. Advect

#### Add source
Hozzáadunk valamilyen forrást a sűrűséghez, ezek a mi esetünkben ezek a következők: \
E : Erase - radírozás
W : Wall - fal
S: Source - forrás
Ezekkel a billentűkkel tudunk mode-t váltani a különböző mode-k között, és a bal egér segítségével tudjuk aktiválni.  
#### Diffuse
Ebben a lépésben a megvizsgáljuk a lehetséges diffuziót. Amennyiben a $$diff>0$$, akkor a folyadék elkezd szétterjedni. Egyetlen rácspont esetén azt feltételezzük, hogy csak a négy közvetlen szomszédjával "cserél" sűrűséget. Csökkenthet is a sűrűség a vizsgált cellában, mivel átad belőle a szomszédjainak, és a sűrűség növekedhet is, amennyiben a szomszédeiból beárad a sűrűség. Így a nettó változás (mennyire tér el az őt körülvevőktől a középső):\
$$x_0(i-1,j)+ x_0(i+1,j) + x_0(i,j-1) + x_0(i,j+1) - 4 \cdot x_0(i,j)$$ \
A $$\texttt{diff bad()}$$ függvény kiszámítja minden rácsponton a "sűrűségcseréket", majd hozzáadja őket a meglévő értékekhez. 
$$a = dt \cdot diff \cdot rows \cdot cols$$, ahol $$a$$: diffuziós ráta; $$dt$$: időlépés; $$rows$$: sorok száma; $$cols$$: oszlopok száma
$$x(i,j) = x_0(i,j) + a \cdot (x_0(i-1,j)+ x_0(i+1,j) + x_0(i,j-1) + x_0(i,j+1) - 4 \cdot x_0(i,j))$$
Ez az eljárás egyszerűen implementálható, és intuitív, de nagy $$a$$ esetén nagyon instabillá válhat a szimulációnk, és oszcillálni fog. Emiatt az explicit módszer helyett implicit módszert kell alkalmaznunk, hogy garantáljuk a stabilitását a szimulációnak, ezt a Gauss-Seidel iteráció segítségével tesszük meg. Tehát olyan módszert kell találnunk, ami "backtracking"-gel (visszafelé diffunálva) megkapjuk a kiinduló sűrűséget. \
$$x_0(i,j) = x(i,j)-a \cdot (x(i-1,j)+ x(i+1,j) + x(i,j-1) + x(i,j+1) - 4 \cdot x(i,j))$$
Így egy lineáris egyenletrendszer. A $$\texttt{diff()}$$ függvényben tehát kiszámoljuk minden cella új értékét a megelőző szomszédos cellák aktuális értékeinek súlyozott átlaga segítségével, a Gauss-Seidel-iteráció 20 iterációt fog végre hajtani, ez nem pontos megoldás, de a szimulációhoz elegendő. (Persze lehetne több iterációval is.)  Tehát, így fogjuk kiszámítani az új sűrűséget minden cellára:
$$x(i,j) = x_0(i,j)+a \cdot (x(i-1,j)+ x(i+1,j) + x(i,j-1) + x(i,j+1) - 4 \cdot x(i,j))/(1+4\cdot a)$$
Az implicit módszer, illetve az $$1+4 \cdot a$$-val való leosztással lesz stabil a szimulációnk. 
![image](https://github.com/user-attachments/assets/629bc39f-4b10-4885-a8c2-d96619e757d7)

#### Advect
Az $$\texttt{advect()}$$ függvény azért felelős, hogy a sűrűség egy adott sebességmezőt kövessen, az $$u$$ és $$v$$ mentén. Alapötlet az advekciós lépés mögött: ahelyett, hogy az (a) ábrán látható sebességmező mentén előre haladnánk az időben a cellák középpontjaival (b), inkább azokat a részecskéket keressük meg, amelyek pontosan a cellák középpontjába érkeznek meg – ezt úgy tesszük, hogy visszafelé követjük az időben a cellák középpontjaitól indulva a pályájukat (c).
![image](https://github.com/user-attachments/assets/08325a6e-2a23-4ef6-b117-6ceea2aee6e0)
A függvény főlépései: 
1. rácspontok visszakövetkése
2. az ottani értéket interpolálja
3. megkapjuk az új rácsot
### Vel step
A sűrűségmező bemutatása után térjünk rá a sebességmezőre. Ebben a függvényben egy függvényt kivéve minden más ismerős lesz már az előzőekben említett $$\texttt{avect()}, \texttt{diff()}, \texttt{add source()}$$ függvények miatt. 
1. Add source
2. Diffuse
3. Project
4. Advect
5. Project
#### Project
Ez a függvény vizuálisan azt segíti, hogy örvényes, élethű mozgásokat tudjunk létrehozni. A tömegmegmaradás céljából a Hodge-felbontást használjuk, ami azt mondja ki, hogy minden sebességmező felbontható egy tömegmegmaradó mezőre és egy gradiensmezőre.
![image](https://github.com/user-attachments/assets/9ac15df2-6949-44d6-8744-1faab7d0e93d)
### Demo (Live demo, maybe)
TODO felvételek elkészítése
...

