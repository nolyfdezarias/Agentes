
from random import randint ,sample

def in_range(i,j,x,y):
    return i >= 0 and j >= 0 and i < x and j < y

moves_x = [-1,0,1,0]
moves_y = [0,1,0,-1]

def generate_XY(x,y):
    return (randint(0,x-1),randint(0,y-1))

class World:
    def __init__(self,rows,columns,childs,p_obst,p_dirty):
        self.r = rows
        self.c = columns
        self.amount_childs = childs
        self.amount_childsI = childs
        self.childs = []
        self.robot = None
        self.amount_obst = int(rows * columns * p_obst / 100)
        self.amount_dirty = int(rows * columns * p_dirty / 100)
        self.freeCells = rows * columns - self.amount_childs - self.amount_obst - 1 
        
                


    def __call__(self):
        self.world = []

        for i in range(0,self.r):
            self.world.append([])
            for j in range(0,self.c):
                self.world[i].append([])
        self.gen_Babyyard()
        self.gen_Obst()
        self.gen_Dirty()
        self.gen_Childs()
        self.gen_Robot()

    def build_Babyyard(self,x,y):

        if len(self.babyyard) == self.amount_childsI:
            return
        
        self.babyyard.append((x,y))
        self.world[x][y].append("C")

        for i in range(0,len(moves_x)):
            new_x = x + moves_x[i]
            new_y = y + moves_y[i]
            if in_range(new_x,new_y,self.r,self.c) and "C"  not in self.world[new_x][new_y]:
                self.build_Babyyard(new_x,new_y)

    def gen_Babyyard(self):
        x,y = generate_XY(self.r,self.c)
        
        self.babyyard = []
        
        self.build_Babyyard(x,y)

   

    def gen_Dirty(self):
        
        for i in range(0,self.amount_dirty):
            x = 0
            y = 0
            while True:
                x,y = generate_XY(self.r,self.c)
                if len(self.world[x][y]) == 0 :
                    self.world[x][y].append("S") 
                    break
    
    def visit(self,ix,iy,x,y,visited):
        visited[ix][iy] = 1

        amount_visited = 1

        for i in range(len(moves_x)):
            new_x = ix + moves_x[i]
            new_y = iy + moves_y[i]
            if new_x == x and new_y == y:
                continue

            if in_range(new_x,new_y,self.r,self.c) and "O" not in self.world[new_x][new_y] and visited[new_x][new_y] == 0:
                amount_visited += self.visit(new_x,new_y,x,y,visited)
        
        return amount_visited
        

    def gen_Obst(self):

         for k in range(self.amount_obst):
            while True :
                x,y = generate_XY(self.r,self.c)
                if len(self.world[x][y]) == 0 :
                    init_i = 0
                    init_j = 0
                    for i in range(self.r):
                        for j in range(self.c):
                            if len(self.world[i][j]) == 0 :
                                if x == i and y == j:
                                    continue
                                init_i = i
                                init_j = j
                                break
                    
                    markWorld = []
                    for i in range(0,self.r):
                        markWorld.append([0] * self.c)

                    amount_visited = self.visit(init_i,init_j,x,y,markWorld)
                    if amount_visited + k + 1 == self.r * self.c:
                        self.world[x][y].append("O")
                        break


    def gen_Childs(self):
        
        for i in range(0,self.amount_childs):
            x = 0
            y = 0
            while True:
                x,y = generate_XY(self.r,self.c)
                if len(self.world[x][y]) == 0 :
                    self.world[x][y].append("N")
                    self.childs.append(Child(x,y))
                    break
        
    def gen_Robot(self):
        
        while True:
            x,y = generate_XY(self.r,self.c)
            if len(self.world[x][y]) == 0 :
                self.world[x][y].append("R")
                self.robot = Robot(x,y)
                break
    
    def print_World(self):
        #puede q existan 3 elementos en una casilla
        for i in range(0,self.r):
            to_print = ""
            for j in range(0,self.c):
                if len(self.world[i][j]) == 0:
                    to_print += "_  " 
                elif len(self.world[i][j]) == 1:
                    to_print += self.world[i][j][0] + "  " 
                else:
                    to_print += self.world[i][j][0] + "/" + self.world[i][j][1]  + " "
            print(to_print)

    def worldVariation(self):
        self.world = []
        for i in range(0,self.r):
            self.world.append([])
            for j in range(0,self.c):
                self.world[i].append([])
        
        self.gen_Babyyard()
        self.gen_Obst()
        self.gen_Dirty()
        child_in_chard = []
        for i in range(len(self.childs)):
            if self.childs[i].in_yard:
                child_in_chard.append(i)
            elif self.childs[i].in_robot:
                continue
            else:
                while True:
                    x,y = generate_XY(self.r,self.c)
                    if len(self.world[x][y]) == 0 :
                        self.world[x][y].append("N")
                        self.childs[i].pos_x = x
                        self.childs[i].pos_y = y
                        break
        
        fBabyYard = sample(self.babyyard,len(child_in_chard))
        for i in range(len(child_in_chard)):
            new_x ,new_y = fBabyYard[i]
            self.childs[child_in_chard[i]].pos_x = new_x
            self.childs[child_in_chard[i]].pos_y = new_y
            self.world[new_x][new_y].append("N")
        
        while True:
            x,y = generate_XY(self.r,self.c)
            if len(self.world[x][y]) == 0 :
                self.world[x][y].append("R")
                self.robot.pos_x = x
                self.robot.pos_y = y
                break

    
        

class Child:
    def __init__(self,x,y):
        self.in_robot = False
        self.in_yard = False
        self.pos_x = x
        self.pos_y = y


    def generateDirty(self,world):
        #dirty = randint(0,1)
        #if dirty:
        des_x = [-1,-1,0,1,1,1,0,-1]
        des_y = [0,1,1,1,0,-1,-1,-1]
        amount_childs = 1
        free_spaces = 0
        one_child = [0,1]
        two_childs = [0,1,2,3]
        more_childs = [0,1,2,3,4,5,6]
        amount_dirty = 0
        for k in range(len(des_x)):
            new_x = self.pos_x + des_x[k]
            new_y = self.pos_y + des_y[k]

            if in_range(new_x,new_y,world.r,world.c):
                if "N" in world.world[new_x][new_y]:
                    amount_childs += 1
                elif len(world.world[new_x][new_y]) == 0:
                    free_spaces += 1 

        if amount_childs == 1:
            amount_dirty = one_child[ randint (0,1)]
        elif amount_childs == 2:
            amount_dirty = two_childs[ randint (0,3)]
        else:
            amount_dirty = more_childs[ randint (0,6)]
        
        amount_dirty = min(amount_dirty,free_spaces)
        world.amount_dirty += amount_dirty

        if amount_dirty == 0:
            print(f'el nino en {self.pos_x},{self.pos_y} no ensucio')
        else:
            print(f'el nino en {self.pos_x},{self.pos_y} ensucio {amount_dirty} casillas')
            
        while amount_dirty > 0 :
            k = randint(0,7)
            new_x = self.pos_x + des_x[k]
            new_y = self.pos_y + des_y[k]
            if in_range(new_x,new_y,world.r,world.c) and len(world.world[new_x][new_y]) == 0:
                world.world[new_x][new_y].append("S")
                amount_dirty -= 1

        #else:
        #    print(f'el nino en {self.pos_x},{self.pos_y} no ensucio')

    def try_move(self,x,y,mdir,world):
        if in_range(x,y,world.r,world.c) :
            if "S" in world.world[x][y] or "N" in  world.world[x][y] or "R" in world.world[x][y] or "C" in world.world[x][y]:
                return False , None
            elif "O" in world.world[x][y]:
                return self.try_move(x + moves_x[mdir], y + moves_y[mdir],mdir,world)
            return True , (x,y)

        return False, None

    def move(self,world):
        move = randint(0,1)
        
        if move:
            move_dir = randint(0,3)
            
            print(f'El ninno de {self.pos_x}, {self.pos_y} se movio en direccion {move_dir}')
            new_x = self.pos_x + moves_x[move_dir]
            new_y = self.pos_y + moves_y[move_dir]
            ans , lpos = self.try_move(new_x,new_y,move_dir,world)
            if ans :
                world.world[self.pos_x][self.pos_y].remove("N")
                to_insert = "N"
                self.pos_x = new_x
                self.pos_y = new_y

                while True:
                    world.world[new_x][new_y].append(to_insert)
                    to_insert = world.world[new_x][new_y][0]
                    if len(world.world[new_x][new_y]) > 1:
                   
                        world.world[new_x][new_y].remove(to_insert)
                        

                    if (new_x,new_y) == lpos:
                        break

                    new_x = new_x + moves_x[move_dir]
                    new_y = new_y + moves_y[move_dir]
                
                self.generateDirty(world)
        else : 
            print("El ninno decidio no moverse")


    

class Robot:
    def __init__(self,x,y):
        self.with_child = False
        self.pos_x = x
        self.pos_y = y
        self.target = []

    def getTargetRoad(self,ambiente,target):
        road = []
        queue = [(self.pos_x,self.pos_y)]
        visited = []
        ant_dic = {}
        ant_dic[(self.pos_x,self.pos_y)] = (-1,-1)
        x = 0
        y = 0
        while len(queue) > 0:
            x , y= queue.pop(0)
            if target in ambiente.world[x][y] and (x,y) != (self.pos_x,self.pos_y):
                break 
            visited.append((x,y))
            
            for i in range(0,len(moves_x)):
                new_x = x + moves_x[i]
                new_y = y + moves_y[i]
                
                if in_range(new_x,new_y,ambiente.r,ambiente.c) and "O" not in ambiente.world[new_x][new_y] and (new_x,new_y) not in visited and not ("N" in ambiente.world[new_x][new_y] and "C" in ambiente.world[new_x][new_y]) and not(self.with_child and "N" in ambiente.world[new_x][new_y] ):
                    queue.append((new_x,new_y))
                    ant_dic[(new_x,new_y)] = (x,y)


        road.append((x,y))
        while True:
            x,y = ant_dic[(x,y)]
            if x == -1:
                break
            road.append((x,y))

        road.reverse()
        print(road)
        road = road[1:]
        
        return road

    def getTarget(self,ambiente,target):
        road = self.getTargetRoad(ambiente,target)
        
        if self.with_child and len(road) >= 2:
            return road[1]
        elif len(road) > 0:
            return road[0]
        else:
            return (-1,-1)


    def move2(self,ambiente):
        if ambiente.amount_dirty * 100 / ambiente.freeCells > 30 or ambiente.amount_childs == 0 :
            if ambiente.amount_childs ==  0 and ambiente.amount_dirty == 0:
                print("I have finish my work")
                print(f'Tengo Ninno {self.with_child}')
            else:
                if "S" in ambiente.world[self.pos_x][self.pos_y]:
                    ambiente.world[self.pos_x][self.pos_y].remove("S")
                    ambiente.amount_dirty -= 1
                else:
                    new_x , new_y = self.getTarget(ambiente,"S")
                    if (new_x,new_y) == (-1,-1):
                        print("No puedo llegar a mi objetivo")
                    else:
                        
                        ambiente.world[self.pos_x][self.pos_y].remove("R")
                        self.pos_x = new_x
                        self.pos_y = new_y
                        ambiente.world[new_x][new_y].append("R")

                        if "N" in ambiente.world[new_x][new_y]:
                            self.with_child = True
                            ambiente.world[new_x][new_y].remove("N")
                            for ch in ambiente.childs:
                                if ch.pos_x == new_x and ch.pos_y == new_y:
                                    ch.in_robot = True
                                    ch.pos_x = -1
                                    ch.pos_y = -1
                                    break
                        
                        if "C" in ambiente.world[new_x][new_y] and self.with_child :
                            self.with_child = False
                            ambiente.world[new_x][new_y].append("N")
                            ambiente.amount_childs -= 1
                            
                            for ch in ambiente.childs:
                                if ch.pos_x == -1 and ch.pos_y == -1:
                                    ch.in_robot = False
                                    ch.in_yard = True
                                    ch.pos_x = new_x
                                    ch.pos_y = new_y
                                    break

        else:
            if self.with_child:
                #LLevar al corral
                new_x , new_y = self.getTarget(ambiente,"C")
                if (new_x,new_y) == (-1,-1):
                    print("No puedo llegar a mi objetivo")
                else:
                    ambiente.world[self.pos_x][self.pos_y].remove("R")
                    self.pos_x = new_x
                    self.pos_y = new_y
                    ambiente.world[new_x][new_y].append("R")
                    if "C" in ambiente.world[new_x][new_y]:
                        self.with_child = False
                        ambiente.world[new_x][new_y].append("N")
                        ambiente.amount_childs -= 1
                            
                        for ch in ambiente.childs:
                            if ch.pos_x == -1 and ch.pos_y == -1:
                                ch.in_robot = False
                                ch.in_yard = True
                                ch.pos_x = new_x
                                ch.pos_y = new_y
                                break
            else:
                #Buscar Nino
                new_x , new_y = self.getTarget(ambiente,"N")
                
                if (new_x,new_y) == (-1,-1):
                    print("No puedo llegar a mi objetivo")
                else:
                    ambiente.world[self.pos_x][self.pos_y].remove("R")
                    self.pos_x = new_x
                    self.pos_y = new_y
                    ambiente.world[new_x][new_y].append("R")
                    if "N" in ambiente.world[new_x][new_y]:
                        self.with_child = True
                        ambiente.world[new_x][new_y].remove("N")
                        #ambiente.amount_childs -= 1
                        for ch in ambiente.childs:
                            if ch.pos_x == new_x and ch.pos_y == new_y:
                                ch.in_robot = True
                                ch.pos_x = -1
                                ch.pos_y = -1
                                break


    def moveProActive(self,ambiente):
        if len(self.target)  > 0:
            #have target
            if "S" in ambiente.world[self.pos_x][self.pos_y]:
                ambiente.world[self.pos_x][self.pos_y].remove("S")
                ambiente.amount_dirty -= 1
            else:
                new_x , new_y = self.target.pop(0)
                if "O" not in ambiente.world[new_x][new_y]  and not ("N" in ambiente.world[new_x][new_y] and "C" in ambiente.world[new_x][new_y]) and not(self.with_child and "N" in ambiente.world[new_x][new_y] ):
                    #valid Move
                    ambiente.world[self.pos_x][self.pos_y].remove("R")
                    self.pos_x = new_x
                    self.pos_y = new_y
                    ambiente.world[new_x][new_y].append("R")
                    if "C" in ambiente.world[new_x][new_y] and self.with_child:
                        self.with_child = False
                        ambiente.world[new_x][new_y].append("N")
                        for ch in ambiente.childs:
                            if ch.pos_x == -1 and ch.pos_y == -1:
                                ch.in_robot = False
                                ch.in_yard = True
                                ch.pos_x = new_x
                                ch.pos_y = new_y
                                break
                    elif "N" in ambiente.world[new_x][new_y]:
                        self.with_child = True
                        ambiente.world[new_x][new_y].remove("N")
                        ambiente.amount_childs -= 1
                        for ch in ambiente.childs:
                            if ch.pos_x == new_x and ch.pos_y == new_y:
                                ch.in_robot = True
                                ch.pos_x = -1
                                ch.pos_y = -1
                                break
                else:
                    self.target = []
                    self.moveProActive(ambiente)
        else:
            #get Target
            if ambiente.amount_childs == 0 and not self.with_child:
                print("no hay ninos por recoger")
                if ambiente.amount_dirty == 0:
                    print("Termine")
                else:
                    #Buscar Basura
                    if "S" in ambiente.world[self.pos_x][self.pos_y]:
                        ambiente.world[self.pos_x][self.pos_y].remove("S")
                        ambiente.amount_dirty -= 1
                    else:
                        road = self.getTargetRoad(ambiente,"S")
                        if len(road) == 0:
                            print("No puedo llegar a mi objetivo")
                        else:
                            self.target = list(road)
                            self.moveProActive(ambiente)
                        
            elif "S" in ambiente.world[self.pos_x][self.pos_y]:
                ambiente.world[self.pos_x][self.pos_y].remove("S")
                ambiente.amount_dirty -= 1
            else:
                if self.with_child:
                    #Entregar Ninno
                    road = self.getTargetRoad(ambiente,"C")
                else:
                    road = self.getTargetRoad(ambiente,"N")
                    #Buscar ninno

                if len(road) == 0:
                        print("No puedo llegar a mi objetivo")
                else:
                    self.target = list(road)
                    self.moveProActive(ambiente)
                    
    def move(self,ambiente):
        if ambiente.amount_childs == 0 and not self.with_child:
            print("no hay ninos por recoger")
            if ambiente.amount_dirty == 0:
                print("Termine")
            else:
                #Buscar Basura
                if "S" in ambiente.world[self.pos_x][self.pos_y]:
                    ambiente.world[self.pos_x][self.pos_y].remove("S")
                    ambiente.amount_dirty -= 1
                    
                else:
                    new_x , new_y = self.getTarget(ambiente,"S")
                    if (new_x,new_y) == (-1,-1):
                        print("No puedo llegar a mi objetivo")
                    else:
                        ambiente.world[self.pos_x][self.pos_y].remove("R")
                        self.pos_x = new_x
                        self.pos_y = new_y
                        ambiente.world[new_x][new_y].append("R")

        elif "S" in ambiente.world[self.pos_x][self.pos_y]:
            ambiente.world[self.pos_x][self.pos_y].remove("S")
            ambiente.amount_dirty -= 1
        else:
            if self.with_child:
                #Entregar Ninno
                new_x , new_y = self.getTarget(ambiente,"C")
                if (new_x,new_y) == (-1,-1):
                    print("No puedo llegar a mi objetivo")
                else:
                    ambiente.world[self.pos_x][self.pos_y].remove("R")
                    self.pos_x = new_x
                    self.pos_y = new_y
                    ambiente.world[new_x][new_y].append("R")
                    if "C" in ambiente.world[new_x][new_y]:
                        self.with_child = False
                        ambiente.world[new_x][new_y].append("N")
                        for ch in ambiente.childs:
                            if ch.pos_x == -1 and ch.pos_y == -1:
                                ch.in_robot = False
                                ch.in_yard = True
                                ch.pos_x = new_x
                                ch.pos_y = new_y
                                break
            else:
                new_x , new_y = self.getTarget(ambiente,"N")
                #Buscar ninno
                if (new_x,new_y) == (-1,-1):
                    print("No puedo llegar a mi objetivo")
                else:
                    ambiente.world[self.pos_x][self.pos_y].remove("R")
                    self.pos_x = new_x
                    self.pos_y = new_y
                    ambiente.world[new_x][new_y].append("R")
                    if "N" in ambiente.world[new_x][new_y]:
                        self.with_child = True
                        ambiente.world[new_x][new_y].remove("N")
                        ambiente.amount_childs -= 1
                        for ch in ambiente.childs:
                            if ch.pos_x == new_x and ch.pos_y == new_y:
                                ch.in_robot = True
                                ch.pos_x = -1
                                ch.pos_y = -1
                                break


    