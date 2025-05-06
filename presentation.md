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
Ez az eljárás egyszerűen implementálható, és intuitív, de nagy $$a$$ esetén nagyon instabillá válhat a szimulációnk, és oszcillálni fog. Emiatt az explicit módszer helyett implicit módszert kell alkalmaznunk, hogy garantáljuk a stabilitását a szimulációnak, ezt a Gauss-Seidel iteráció segítségével tesszük meg. Tehát olyan módszert kell találnunk, ami "backtracking"-gel megkapjuk a kiinduló sűrűséget. \
$$x_0(i,j) = x(i,j)-a \cdot (x(i-1,j)+ x(i+1,j) + x(i,j-1) + x(i,j+1) - 4 \cdot x(i,j))$$
#### Advect

### Vel step
1. Add source
2. Diffuse
3. Project
4. Advect
5. Project

#### Project


### Demo (Live demo, maybe)
...

