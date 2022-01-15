import time
import math
from radar import Radar
import copy
import os

colors = {"red" : '\033[91m', "green" : '\033[92m',"yellow" : '\033[93m', "default" : '\033[0m'} 

def adapt(x,in_min,in_max,out_min,out_max): return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

class Matrix :
    
    def __init__(self,l, L, values=None) : 
        self.length = l
        self.width = L
        self.x_size = L
        self.y_size = l
        self.default_values = values
        self.listception = [[None for l in range(self.length)] for k in range(self.width)]
        self.clear(self.default_values)
    
    def setCase(self,x,y,value) : 
        if   0 <= x < self.width and 0 <= y < self.length :
            self.listception[x][(self.length-1)-y] = value
        else : pass

    def getCase(self,x,y) : 

        if 0 <= x < self.width and 0 <= y < self.length:
            return self.listception[x][(self.length-1)-y]

    def getWidth(self) : return self.width

    def getLength(self) : return self.length

    def center(self) : return { 'x' : int((self.getWidth()-1)/2), 'y' : int((self.getLength()-1)/2)}

    def clear(self,value = None) : 
        for k in range(self.width) :
            for l in range(self.length) : self.listception[k][l] = value

    def setLine(self,line,value) : 
        for x in range(self.width) : self.setCase(x,line,value)

    def setColumn(self,column,value) :
        for y in range(self.length) : self.setCase(column,y,value)

    def line(self,xA,yA,xB,yB,value) : 

        def y(xA,yA,xB,yB,x) :
            a = (yB-yA)/(xB-xA)
            return a*x+(yA-a*xA)
        
        if xA != xB :
            if xA < xB :
                for x in range(xA,xB+1) : 
                    self.setCase(x,int(y(xA,yA,xB,yB,x)),value)
            else : 
                for x in range(xB,xA+1) : 
                    self.setCase(x,int(y(xA,yA,xB,yB,x)),value)
        elif yA < yB :
            for i in range(yA,yB+1) : self.setCase(xA,i,value)
        else : 
            for i in range(yB,yA+1) : self.setCase(xA,i,value) 


    def encadre(self,margeX, margeY,x_value,y_value) : 
        self.line(margeX,margeY,self.width-margeX-1,margeY,x_value)
        self.line(margeX,self.length-margeY-1,self.width-margeX-1,self.length-margeY-1,x_value)

        self.line(margeX,margeY,margeX,self.length-margeY-1,y_value)
        self.line(self.width-margeX-1,margeY,self.width-margeX-1,self.length-margeY-1,y_value)

    def polygon(self,*args,fill=False,value) : #prend des points (x,y) en agrgument #reecrire en relaint les points les plus proches #ajouter le remplissage
        for i in range(len(args)-1,-1,-1) : self.line(args[i][0],args[i][1],args[i-1][0],args[i-1][1],value)
        
    def circle(self,center,radius,value,fill=False) :
        for x in range(center[0]-radius,center[0]+radius+1) :
            xa = adapt(x,center[0]-radius,center[0]+radius,-radius,radius)
            yp = center[1] + math.sqrt(radius**2-(xa**2))
            yn = center[1] - math.sqrt(radius**2-(xa**2))
            self.setCase(x,int(yp),value)
            self.setCase(x,int(yn),value)

    def print(self,xb,yb,text,color='default') :
        text = str(text)
        color = colors[color]
        for i in range(len(text)) : 
            if 0 <= i < self.width : self.setCase(xb+i,yb,color+text[i])

    def ray(self,posx,posy,angle,ray=False) :

        a = math.tan(angle)

        if abs(math.sin(angle)) >= math.sqrt(2)/2 :
            
            if math.sin(angle) > 0 :

                for y in range(posy,self.length) :

                    x=int((y+a*posx-posy)/a)

                    if self.getCase(x,y) == '#' : return math.sqrt((x-posx)**2+(y-posy)**2)
                    elif ray : self.setCase(x,y,'.')

            else :

                for y in range(posy,0-1,-1) :

                        x=int((y+a*posx-posy)/a)

                        if self.getCase(x,y) == '#' : return math.sqrt((x-posx)**2+(y-posy)**2)
                        elif ray : self.setCase(x,y,'.')

        else :

            if math.cos(angle) < 0 :
                for x in range(posx,0-1,-1):
                    y = int(a*(x-posx)+posy)
                    if self.getCase(x,y) == '#' : return math.sqrt((x-posx)**2+(y-posy)**2)
                    elif ray : self.setCase(x,y,'.')
            else : 
                for x in range(posx,self.width):
                    y = int(a*(x-posx)+posy)

                    if self.getCase(x,y) == '#' : return math.sqrt((x-posx)**2+(y-posy)**2)
                    elif ray : self.setCase(x,y,'.')
 
        return 1000

    def phagocyte(self,matrix,x_center=None,y_center=None) :

        if x_center == None or y_center == None :
            x_center = self.center()['x']
            y_center = self.center()['y']

        mx_centrer = matrix.center()['x']
        my_center = matrix.center()['y']

        for x in range(matrix.getWidth()):
            for y in range(matrix.getLength()) :
                self.setCase(x_center+x-mx_centrer,y_center+y-my_center,matrix.getCase(x,y))

    def display(self,style=False) :
        output = ""
        if not style :
            for ligne in range(self.length-1,-1,-1) : 
                for colone in range(self.width) : output += str(self.getCase(colone, ligne)) + " "
                output += "\n"
            print(output)
        else :
            for ligne in range(self.length-1,-1,-1) : 
                for colone in range(self.width) : 
                    print(self.getCase(colone, ligne),"",end="")
                    time.sleep(0.0003)
                print()

    def edit(self,mark='#'):

        tmp = copy.deepcopy(self)

        posx = int(self.x_size/2)
        posy = int(self.y_size/2)

        keyRadar = Radar()
        keys = keyRadar.getKeys()

        def update(tmp0) : 
            
            tmp.display()
            time.sleep(0.015)
            tmp.phagocyte(tmp0)
            os.system('clear')

        def wall(self,posx,posy):

            tmp0 = copy.deepcopy(self)

            keys = keyRadar.getKeys()
            Ay = posx
            Ax = posx

            Bx = posx
            By = posx

            while not 'e' in keys:

                keys = keyRadar.getKeys()

                tmp.print(5,self.y_size-5,'Quitter : e')
                tmp.print(5,self.y_size-8,'Point A : a')
                tmp.print(5,self.y_size-9,'Point B : b')
                tmp.print(5,self.y_size-12,'Valider ligne : v')
                tmp.print(5,self.y_size-14,'Gommer : g')
                tmp.print(5,self.y_size-16,'Enregister : h')
                tmp.print(5,self.y_size-18,'Cellule : c')
                tmp.setCase(posx,posy,'@')
                tmp.line(Ax,Ay,Bx,By,'#')
                
                if 'z' in keys : posy += 1
                if 's' in keys : posy -= 1
                if 'd' in keys : posx += 1
                if 'q' in keys : posx -= 1
                if 'g' in keys : tmp0.setCase(posx,posy,' ')
                if 'v' in keys : tmp0.line(Ax,Ay,Bx,By,mark)
                if 'u' in keys : return None
                if 'h' in keys : self.phagocyte(tmp0)
                if 'c' in keys : tmp0.setCase(posx,posy,mark)

                if 'a' in keys : 
                    Ax = posx
                    Ay = posy

                if 'b' in keys : 
                    Bx = posx
                    By = posy

                update(tmp0)

            return 0

        wall(self,posx,posy)
        time.sleep(1)

    def focus(self,center,rangex,rangey) :

        '''retourne une matrice centrée sur center de dimentions rangey par rangex'''

        x = 0
        y = 0

        toreturn = Matrix(rangey,rangex,' ')
        for rx in range(-rangex//2,(rangex//2)+1) :
            for ry in range(-rangey//2,(rangey//2)+1) :

                if (center[0]+rx >= self.width or center[0]+rx < 0) or (center[0]+ry >= self.length or center[0]+ry < 0) :
                    toreturn.setCase(x,y,self.getCase(center[0]+rx,center[1]+ry))

                else : toreturn.setCase(x,y,' ')

                x += 1
                y += 1

        return toreturn