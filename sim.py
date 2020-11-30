 
from world import World,Robot,Child

def simEnd(world):
    if world.amount_dirty * 100 / world.freeCells > 60 :
        return True, 0 , 1
    elif world.amount_childs ==  0 and world.amount_dirty == 0:
        return True, 1, 0
    return False, 0,0

def sim(rows,cols,childs,p_dirty,p_obst,t,method):

    win = 0
    lose = 0
    for i in range(30):
        k = 0
        w = World(rows,cols,childs,p_obst,p_dirty)
        w()
        for j in range(100 *t):
            k += 1
            eval(f'w.robot.{method}(w)')
            
            w.print_World()

            for ch in w.childs:
                if not ch.in_robot and not ch.in_yard:
                    ch.move(w)
            w.print_World()

            end , addWin ,addLose  = simEnd(w)
            if end :
                win += addWin
                lose += addLose
                break

            if k % t == 0:
                w.worldVariation()

    return win , lose



def prove():
    #worlds = [(5,10,4,30,10,5) , (5,10,4,40,10,15) , (5,10,8,20,0,5)]
    worlds = [(8,10,5,40,15,10) , (8,10,5,35,15,10) ,(8,10,5,40,15,20) , (5,10,4,30,10,5) , (5,10,4,40,10,15) , (5,10,8,20,0,5)
          ,(8,4,6,30,15,10) , (8,4,6,30,20,20) , (3,5,4,15,10,30) , (3,5,4,25,10,30)]
    methods = ["moveProActive","move","move2"]
    answer = { "move" : {},
               "move2" : {},
               "moveProActive" :{}}

    for j in range(len(methods)):
        for i in range(len(worlds)):
            answer[methods[j]][i] = sim(worlds[i][0],worlds[i][1],worlds[i][2],worlds[i][3],worlds[i][4],worlds[i][5],methods[j])


    print(answer)

prove()