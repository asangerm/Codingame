import sys
import math as m
import random
import numpy as np
import time

# Global

last_luz = [0,0]
targeted = 0
begin = 0
save_mode = 0

# Classes
class Creature:
    def __init__(self, id, color, specie, x, y, vx, vy):
        self.id = id
        self.color = color
        self.specie = specie
        self.position = [x, y]
        self.velocity = [vx, vy]

class Drone:
    def __init__(self, id, x, y, emergency, battery):
        self.id = id
        self.position = [x, y]
        self.emergency = emergency
        self.battery = battery

class Radar:
    def __init__(self, d_id, c_id, direction):
        self.d_id = d_id
        self.c_id = c_id
        self.direction = direction

# Fonctions

# Fonction qui determine si l'id d'une créature est celle d'un monstre
def is_monster(c_id):
    for i in all_creatures:
        if c_id == i.id:
            if i.specie == -1:
                return (1)
    return(0)

# Fonction qui donne la distance entre deux points
def get_distance(pos1, pos2):
    x_delt = pos1[0] - pos2[0]
    y_delt = pos1[1] - pos2[1]
    dist = m.sqrt(x_delt**2 + y_delt**2)
    return (dist)

# Fonction qui réajuste la destination en fonction des contraintes
def reajust(x, y, c, d):
    if x <= 0:
        x = 0
        if y - d >= 0:
            y = d + 600
        else:
            y = d - 600
    if x >= 10000:
        x = 10000
        if y - d >= 0:
            y = d + 600
        else:
            y = d - 600
    if y >= 10000:
        y = 10000
        if x - c >= 0:
            x = c + 600
        else:
            x = c - 600
        if x <= 0:
            x += 1200
        elif x >= 10000:
            x -= 1200
    return x, y

# Fonction qui donne un vecteur en fonction d'une direction
def direction_to_vector(direction):
    v = [0, 0]
    if direction == "TL":
        v = [-424, -424] 
    if direction == "TR":
        v = [424, -424]
    if direction == "BL":
        v = [-424, 424]
    if direction == "BR":
        v = [424, 424]
    if direction == "UP":
        v = [0, -600]
    if direction == "DOWN":
        v = [0, +600]
    return(v)

# Fonction qui donne un vecteur en fonction d'une position
def pos_to_vector(pos, my_drone):
    v = [pos[0] - my_drone.position[0], pos[1] - my_drone.position[1]]
    #print("vector before reajust", v, file = sys.stderr)
    v = reajust_vector(v, my_drone.position)
    return v

# Fonction qui determine si l'id d'une créature correspond a celle d'un crabe 
def is_crab(c_id):
    for i in all_creatures:
        if i.id == c_id:
            if i.specie == 2:
                return (1)
    return(0)

# Fonction qui determine si l'id d'une créature correspond a celle d'un poisson
def is_fish(c_id):
    for i in all_creatures:
        if i.id == c_id:
            if i.specie == 1:
                return (1)
    return(0)

# Fonction qui determine si l'id d'une créature correspond a celle d'une méduse
def is_medusa(c_id):
    for i in all_creatures:
        if i.id == c_id:
            if i.specie == 0:
                return (1)
    return(0)

# Fonction qui par rapport a la position du drone et la direction du radar donne une position vers cette direction
def direction_to_pos(drone_pos, direction):
    pos = [drone_pos[0], 0]
    if direction == "TL":
       pos = [drone_pos[0] - 424, drone_pos[1] - 424] 
    if direction == "TR":
        pos = [drone_pos[0] + 424, drone_pos[1] - 424]
    if direction == "BL":
        pos = [drone_pos[0] - 424, drone_pos[1] + 424]
    if direction == "BR":
        pos = [drone_pos[0] + 424, drone_pos[1] + 424]
    if direction == "UP":
        pos = [drone_pos[0], drone_pos[1] - 600]
    if direction == "DOWN":
        pos = [drone_pos[0], drone_pos[1] + 600]
    return(pos)

# Fonction qui donne la position en fonction d'un vecteur
def vector_to_pos(drone_pos, v):
    pos = [drone_pos[0] + v[0], drone_pos[1] + v[1]]
    return pos

# Fonction qui réajuste le vecteur vitesse du drone pour qu'il garde une norme de 600
def reajust_vector(v, d_pos):
    if get_distance(d_pos, [d_pos[0]+v[0], d_pos[1]+v[1]]) <= 600:
        while get_distance(d_pos, [d_pos[0]+v[0], d_pos[1]+v[1]]) <= 600:
            v = [v[0] * 1.01, v[1] * 1.01]
    else:
        while get_distance(d_pos, [d_pos[0]+v[0], d_pos[1]+v[1]]) >= 600:
            v = [v[0] / 1.01, v[1] / 1.01]
    return v

# Fonction qui defini si je peux me deplacer d'un point A à un point B
def can_i_go(v, my_drone):
    num_segments = 200
    step_size_d = [v[0] / num_segments, v[1] / num_segments]
    for i in monsters:
        step_size_m = [i.velocity[0] / num_segments, i.velocity[1] / num_segments]
        for step in range(0, num_segments + 1):
            segment_pos_d = [step_size_d[0] * step + my_drone.position[0], step_size_d[1] * step + my_drone.position[1]]
            segment_pos_m = [step_size_m[0] * step + i.position[0], step_size_m[1] * step + i.position[1]]
            if get_distance(segment_pos_d, segment_pos_m) < 515:
                return False
    return True

# Fonction qui renvoie la lumière pour la phase 2
def gimme_luz(drone, j):
    if drone.position[1] <= 2500:
        last_luz[j] = 0
        return 0
    if visible_creature_count == 0:
        for i in radar_info:
            if i.direction == "TL" or i.direction == "BL":
                if drone.position[0] <= 2000:
                    last_luz[j] = 1
                    return 1
            if i.direction == "TR" or i.direction == "BR":
                if drone.position[0] >= 8000:
                    last_luz[j] = 1
                    return 1
        last_luz[j] = 0
        return 0
    else:
        for i in visible_creatures:
            if not is_monster(i):
                if i not in common_inv:
                    if i not in  my_saved_scans:
                        if get_distance([i.position[0], i.position[1]], [drone.position[0], drone.position[1]]) >= 800:
                            if last_luz[j] == 0:
                                if len(common_inv) != 12:
                                    last_luz[j] = 1
                                    return 1
    last_luz[j] = 0
    return 0

# Fonction qui renvoie la lumière pour la plongée
def luz_begin(drone):
    if 2500 < drone.position[1] <= 3100:
        return 1
    if 5000 < drone.position[1] <= 5600:
        return 1
    if 7650 < drone.position[1] <= 8400:
        return 1
    return 2

# Fonction principale qui determine le mouvement
def move(my_drone, j, v):
    global begin
    if my_drone.position[1] >= 8300 and begin == 0:
        begin = 1
        return 0
    luz = 0
    if begin == 0:
        luz = luz_begin(my_drone)
    v = reajust_vector(v, my_drone.position)
    #print("before while", v, my_drone.position, file=sys.stderr)
    stop = 0
    while not can_i_go(v, my_drone) and stop < 72:
        v = dodge(my_drone, v)
        v = reajust_vector(v, my_drone.position)
        stop = stop + 1
    if stop == 72:
        print("WAIT", 0, "Im gonna wait")
        return 1
    if luz == 2:
        luz = 0
    elif luz == 0:
        luz = gimme_luz(my_drone, j)
    pos = vector_to_pos(my_drone.position, v)
    pos = reajust(pos[0], pos[1], my_drone.position[0], my_drone.position[1])
    print("MOVE", int(pos[0]), int(pos[1]), luz)
    return 1

# Fonction qui esquive les monstres en faisant tourner le vecteur vitesse du drone de 2 degrès
def dodge(my_drone, original_vector):
    angle_degrees = 14
    # Convertir l'angle en radians
    angle_radians = m.radians(angle_degrees)

    # Décomposer les composantes du vecteur et du centre
    [ox, oy] = original_vector

    # Calculer les nouvelles composantes du vecteur après rotation
    rotated_x = m.cos(angle_radians) * ox - m.sin(angle_radians) * oy
    rotated_y = m.sin(angle_radians) * ox + m.cos(angle_radians) * oy
    # Retourner le nouveau vecteur
    
    return [rotated_x, rotated_y]


# Fonction similaire à go_to mais avec un préference pour les crabes
def submarine(my_drone, j):
    global targeted
    for i in targets:
        if is_crab(i.c_id) and i.d_id == my_drone.id and i.c_id != targeted:
            if move(my_drone, j, direction_to_vector(i.direction)):
                targeted = i.c_id
                return
    for i in targets:
        if is_fish(i.c_id) and i.d_id == my_drone.id and i.c_id != targeted:
            if move(my_drone, j, direction_to_vector(i.direction)):
                targeted = i.c_id
                return
    for i in targets:
        if is_medusa(i.c_id) and i.d_id == my_drone.id and i.c_id != targeted:
            if move(my_drone, j, direction_to_vector(i.direction)):
                targeted = i.c_id
                return
    targeted = 0
    target = pos_to_vector([my_drone.position[0], -5], my_drone)
    while not move(my_drone, j, target):
        #print(my_drone.position[0] + target[0],my_drone.position[1] + target[1] ,file=sys.stderr)
        target = dodge(my_drone, target)
        

# Fonction similaire à go_to mais avec un préference pour les meduses
def beach(my_drone, j):
    global targeted
    for i in targets:
        if is_medusa(i.c_id) and i.d_id == my_drone.id and i.c_id != targeted:
            if move(my_drone, j, direction_to_vector(i.direction)):
                targeted = i.c_id
                return
    for i in targets:
        if is_fish(i.c_id) and i.d_id == my_drone.id and i.c_id != targeted:
            if move(my_drone, j, direction_to_vector(i.direction)):
                targeted = i.c_id
                return
    for i in targets:
        if is_crab(i.c_id) and i.d_id == my_drone.id and i.c_id != targeted:
            if move(my_drone, j, direction_to_vector(i.direction)):
                targeted = i.c_id
                return
    target = pos_to_vector([my_drone.position[0], -5], my_drone)
    targeted = 0
    while not move(my_drone, j, target):
        #print(my_drone.position[0] + target[0],my_drone.position[1] + target[1] ,file=sys.stderr)
        target = dodge(my_drone, target)

# Defini la position de plongée des drones
def first_pos(my_drone):
    if my_drone.position[0] < 5000:
        return [2250, 7800]
    return [7750, 7800]

# Initialisation
creature_count = int(input())       # Nombre de créatures en jeu
all_creatures = []                  # Tableau de toutes les créatures du jeu (id, couleur, type)
for i in range(creature_count):     # Ce tableau ne contient pas les positions ni les vitesses des créatures
    id, color, types = [int(j) for j in input().split()]
    all_creatures.append(Creature(id, color, types, 0, 0, 0, 0))
monsters = []
for i in all_creatures:
            if is_monster(i.id):
                monsters.append(i)

# Tour de jeu
while True:
    start = time.time()
    # Scores
    my_score = int(input())                 # Mon score
    foe_score = int(input())                # Score de l'adversaire

    # Mes scans sauvegardés
    my_saved_scan_count = int(input())      # Nombre de mes scans sauvegardés
    my_saved_scans = []
    for i in range(my_saved_scan_count):
        id = int(input())                   # Créatures que j'ai scanné (id)
        my_saved_scans.append(id)
    
    # Les scans sauvegardés de l'adversaire
    foe_saved_scan_count = int(input())     # Nombre des scans de l'adversaire
    foe_saved_scans = []
    for i in range(foe_saved_scan_count):
        id = int(input())                   # Créatures que l'adv a scanné (id)
        foe_saved_scans.append(id)
    
    # Mes drones
    my_drone_count = int(input())   # Mon nombre de drones
    my_drones = []                  # Tableau de mes drones contenant ces informations
    for i in range(my_drone_count): # id du drone, position x, position y, emmergency?, batterie
        id, x, y, em, bat = [int(j) for j in input().split()]
        my_drones.append(Drone(id, x, y, em, bat))

    # Les drones de l'adversaire
    foe_drone_count = int(input())      # Nombre de drones de l'adversaire
    foe_drones = []                     # Tableau des drones de l'adversaire contenant ces informations
    for i in range(foe_drone_count):    # id du drone, position x, position y, emmergency?, batterie
        id, x, y, em, bat = [int(j) for j in input().split()]
        foe_drones.append(Drone(id, x, y, em, bat))

    # Les scans non sauvegardés de mes drones et de ceux de l'adversaire
    drone_scan_count = int(input())
    not_saved_scan = []                 # Tableau des scans (id du drone, id de la créature)
    for i in range(drone_scan_count):
        did, cid = [int(j) for j in input().split()]
        not_saved_scan.append([did,cid])
    
    # Créatures visibles
    visible_creature_count = int(input())   # Nombre de créatures visibles
    visible_creatures = []
    #print("visible creatures :",file=sys.stderr, end = ' ')
    for i in range(visible_creature_count):
        id, x, y, vx, vy = [int(j) for j in input().split()]
        print(id,file=sys.stderr, end = ' ')
        visible_creatures.append(Creature(id, 0, 0, x, y, vx, vy))
    print(file=sys.stderr) 

    # Radar
    radar_count = int(input())  # Nombre de créatures detectées pas le radar?
    radar_info = []             # id drone, id créature, direction(TL, TR, BR, BL)
    for i in range(radar_count):
        inputs = input().split()
        radar_info.append(Radar(int(inputs[0]), int(inputs[1]), inputs[2]))

    # Inventaire commun a mes drones
    common_inv = []
    for i in not_saved_scan:
        if my_drones[0].id == i[0] or my_drones[1].id == i[0] and i[1] not in common_inv:
            common_inv.append(i[1])
    
	# Liste des creatures disponible pour le scan
    targets = []
    for i in radar_info:
        if i.c_id not in my_saved_scans:
            if i.c_id not in common_inv:
                targets.append(i)
    
    # Liste des monstres
    for i in monsters:
        found = 0
        for j in visible_creatures:
            if j.id == i.id:
                found = 1
                i.position = j.position
                i.velocity = j.velocity
        if found == 0:
            if m.sqrt(i.velocity[0]**2 + i.velocity[1]**2) >= 539:
                i.position[0] = i.position[0] + i.velocity[0]
                i.position[1] = i.position[1] + i.velocity[1]
                i.velocity[0] = i.velocity[0] / 2
                i.velocity[1] = i.velocity[1] / 2
            else:
                i.position[0] = i.position[0] + i.velocity[0]
                i.position[1] = i.position[1] + i.velocity[1]
    
    all_crab=[]
    for i in all_creatures:
        if i.specie == 2:
            all_crab.append(i.id)
    all_fish=[]
    for i in all_creatures:
        if i.specie == 1:
            all_fish.append(i.id)
    all_medusa=[]
    for i in all_creatures:
        if i.specie == 0:
            all_medusa.append(i.id)
    all_blue=[]
    for i in all_creatures:
        if i.color == 3:
            all_blue.append(i.id)
    all_green=[]
    for i in all_creatures:
        if i.color == 2:
            all_green.append(i.id)
    all_yellow=[]
    for i in all_creatures:
        if i.color == 1:
            all_yellow.append(i.id)
    all_pink=[]
    for i in all_creatures:
        if i.color == 0:
            all_pink.append(i.id)

    mfs = 0
    if my_score <= 45 :
        for i in common_inv:
            if is_crab(i):
                mfs+=6
            if is_fish(i):
                mfs+=4
            if is_medusa(i):
                mfs+=2
        if all(i in common_inv for i in all_crab):
            mfs+=8
        if all(i in common_inv for i in all_fish):
            mfs+=8
        if all(i in common_inv for i in all_medusa):
            mfs+=8
        if all(i in common_inv for i in all_blue):
            mfs+=6
        if all(i in common_inv for i in all_green):
            mfs+=6
        if all(i in common_inv for i in all_yellow):
            mfs+=6
        if all(i in common_inv for i in all_pink):
            mfs+=6
        
    
    print(mfs, file=sys.stderr)
    # Action à faire
    for i in range(my_drone_count):
        if save_mode == 0:
            if not mfs>=45 :
                # Plonger jusqu'a 6500
                if begin == 0 and my_drones[i].position[1] < 7800 and my_drones[i].emergency == 0:
                    target =  pos_to_vector(first_pos(my_drones[i]), my_drones[i])
                    while not move(my_drones[i], i, target):
                        target = dodge(my_drones[i], target)
                # Se repartir le haut et le bas
                else:
                    begin = 1
                    if my_drones[i].emergency == 0:
                        if i == 0 :
                            submarine(my_drones[i], i)
                        else:
                            beach(my_drones[i], i)
                    # Touché coulé
                    else:
                        print("WAIT", 0, "Im gonna wait")
                stop = time.time()
                #print((stop-start)/1000, "ms", file = sys.stderr)
            else:
                save_mode = 1
                target =  pos_to_vector([my_drones[i].position[0], -5], my_drones[i])
                while not move(my_drones[i], i, target):
                    target = dodge(my_drones[i], target)
        else:
          if my_drones[i].emergency == 0:
                target =  pos_to_vector([my_drones[i].position[0], -5], my_drones[i])
                print("hey", file=sys.stderr)
                while not move(my_drones[i], i, target):
                    target = dodge(my_drones[i], target)
                if my_drones[0].position[1] <=499 and my_drones[1].position[1] <=499:
                    save_mode = 0
            else:
                print("WAIT", 0, "Im gonna wait")
