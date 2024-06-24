# https://medium.com/fragmentblog/simulating-flocking-with-the-boids-algorithm-92aef51b9e00

import pygame
import sys
import math
import random

pygame.init()
display = pygame.display
surface = display.set_mode((900, 900))
display.set_caption("Boids")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DT = 1/60
ANGLE_FACTOR = 1

class Boid:
    def __init__(self, pos: list[float], vel: float, angle: float) -> None:
        self._pos = pos
        self._vel = vel
        self._angle = angle

    def draw_boid(self):
        x1 = (-8)*math.cos(self._angle)-(18)*math.sin(self._angle)+self._pos[0]
        y1 = (-8)*math.sin(self._angle)+(18)*math.cos(self._angle)+self._pos[1]

        x2 = (8)*math.cos(self._angle)-(18)*math.sin(self._angle)+self._pos[0]
        y2 = (8)*math.sin(self._angle)+(18)*math.cos(self._angle)+self._pos[1]
        pygame.draw.polygon(surface, WHITE, [self._pos, (x1, y1), (x2, y2)])

    def goal_velocity_vector(self, boids: list["Boid"]) -> list[float]:
        num_close_boids = 0
        avg_x, avg_y = 0, 0
        svec = [0, 0]
        avg_angle = 0
        for boid in boids:
            if self != boid and vector_magnitude(self.calculate_distance_vector(boid)) < 250:
                num_close_boids += 1

                avg_x += boid.pos[0]
                avg_y += boid.pos[1]
                
                avg_angle += boid.angle
       

        if num_close_boids == 0:
            return [450-self.pos[0], 450-self.pos[1]]

        com = [(avg_x/num_close_boids-self._pos[0]*5), (avg_y/num_close_boids-self._pos[1])*5]
        svec = [-(avg_x-self.pos[0]*num_close_boids*0.01), -(avg_y-self.pos[1]*num_close_boids*0.01)] #relative 'goal' velocity vector?

        avg_angle /= num_close_boids # 'goal' angle
        avec = [ANGLE_FACTOR*math.cos(avg_angle)*200, ANGLE_FACTOR*math.sin(avg_angle)*200]


        return [com[i]+svec[i]+avec[i] for i in range(len(com))]



    def calculate_distance_vector(self, other: "Boid") -> list[float]:
        return [self._pos[i]-other.pos[i] for i in range(len(self._pos))]
    
    @property
    def pos(self) -> list[float]:
        return self._pos

    @pos.setter
    def pos(self, newpos: list[float]) -> None:
        self._pos = newpos

    @property
    def vel(self) -> float:
        return self._vel

    @vel.setter
    def vel(self, newvel: float) -> None:
        self._vel = newvel

    @property
    def angle(self) -> float:
        return self._angle

    @angle.setter
    def angle(self, newangle: float) -> None:
        self._angle = newangle


def dproduct(vec1: list[float], vec2: list[float]) -> list[float]:
    return sum([vec1[i]*vec2[i] for i in range(len(vec1))])

def vector_magnitude(v: list[float]) -> float:
    return sum([s * s for s in v]) ** 0.5

def update(boids: list[Boid]) -> None:
    for i, boid in enumerate(boids):
        theta = boid.angle + math.pi + 1.15257199722 #arctan(18/8)
        if theta > 2 * math.pi:
            theta -= 2 * math.pi

        vx = boid.vel*math.cos(theta)
        vy = boid.vel*math.sin(theta)

        tvec = boid.goal_velocity_vector(boids)
        #if i == 0:
            #print(tvec)]
        """
        temp_tvec = tvec
        if boid.pos[0] < 200: #and theta > math.pi/2 and theta < 3*math.pi/2:
            if i == 0:
                print("ran")
            temp_tvec[0] = tvec[0] + 1000
        if boid.pos[0] > 700:
            temp_tvec[0] = tvec[0] - 1000
        if boid.pos[1] > 700:
            temp_tvec[1] = tvec[1] + 1000
        if boid.pos[1] < 200:
            temp_tvec[1] = tvec[1] - 1000
        """
        flag = False
        if boid.pos[1] <= 0:
            print("ran")
            boid.pos = [boid.pos[0], 900]
            print(boid.pos)
            flag = True
        elif boid.pos[1] >= 900:
            boid.pos[1] = 0
        if boid.pos[0] <= 0:
            boid.pos[0] = 900
        elif boid.pos[0] >= 900:
            boid.pos[0] = 0


        
        diff_angle = math.acos(dproduct([vx, vy], tvec)/(vector_magnitude([vx, vy])*vector_magnitude(tvec)))
    
        if tvec[1] > vy:
            diff_angle *= -1
        
        boid.vel = abs(math.cos(diff_angle))*100#*vector_magnitude() #distance from center of mass
        boid.angle += diff_angle*DT#*vector_magnitude() #distance from com
        boid.pos[0] += vx*DT
        boid.pos[1] += vy*DT


def main():
    run = True
    clock = pygame.time.Clock()
    boids = []
    for i in range(10):
        angle = random.uniform(-1, 1) + math.pi
        pos = [random.randint(0, 900), random.randint(0,900)]
        b = Boid(pos, 20, angle)
        boids.append(b)
        
    #b1 = Boid([400, 470], 20, math.pi)
    #b2 = Boid([500, 500], 5, 0)
    #b3 = Boid([400, 500], 50, math.pi-2)
    #boids = [b1, b2, b3]
    while run:
        clock.tick(60)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if keys[pygame.K_q]:
            run = False

        surface.fill(BLACK)
        update(boids)
        for b in boids:
            b.draw_boid()


        display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
