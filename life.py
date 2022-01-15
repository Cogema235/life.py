from Matrix import Matrix
from time import sleep
from os import system

system("clear")

cell_marker = input("marker de cellule vivante (Un seul caractère) : ")
void_marker = input("marker de cellule morte (Un seul caractère) : ")
dt = int(input("Dt : "))

scene = Matrix(75,150,values=void_marker)
grid = Matrix(75,150,values=void_marker)
tmp_grid = Matrix(75,150,values=void_marker)

grid.edit(mark=cell_marker)

n = 1

while True :

    for x in range(2,grid.width-1) :
        for y in range(2,grid.length-1) : 

            outline = 0
            
            for ex in range(-1,2) : 
                for ey in range(-1,2) : 

                    if (ex,ey) != (0,0) : 
                        if grid.getCase(x+ex,y+ey) == cell_marker : outline += 1

            if outline == 3 : tmp_grid.setCase(x,y,cell_marker)
            elif outline == 2 : tmp_grid.setCase(x,y,grid.getCase(x,y))
            else : tmp_grid.setCase(x,y,void_marker)

    grid.phagocyte(tmp_grid)
    scene.phagocyte(grid)
    tmp_grid.clear(value=void_marker)

    system("clear")
    scene.encadre(0,0,'+','+')
    scene.print(10,60,'Generation : '+str(n))
    scene.display()
    sleep(dt)

    n += 1 
