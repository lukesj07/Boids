import pygame
import sys
import math
import random

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DT = 1/60
ANGLE_FACTOR = 1
BOID_LEG = 8
BOID_HEIGHT = 18
SVEC_FACTOR = 0.5
AVEC_FACTOR = 200
MVEC_FACTOR = 5
VISION_RADIUS = 200
VELOCITY_FACTOR = 150

pygame.init()
display = pygame.display
surface = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
display.set_caption("Boids")

class Boid:
    def __init__(self, pos: list[float], vel: float, angle: float) -> None:
        self._pos = pos
        self._vel = vel
        self._angle = angle
    
    def draw_boid(self):
        x1 = (-BOID_LEG)*math.cos(self._angle)-(BOID_HEIGHT)*math.sin(self._angle)+self._pos[0]
        y1 = (-BOID_LEG)*math.sin(self._angle)+(BOID_HEIGHT)*math.cos(self._angle)+self._pos[1]
        x2 = (BOID_LEG)*math.cos(self._angle)-(BOID_HEIGHT)*math.sin(self._angle)+self._pos[0]
        y2 = (BOID_LEG)*math.sin(self._angle)+(BOID_HEIGHT)*math.cos(self._angle)+self._pos[1]
        pygame.draw.polygon(surface, WHITE, [self._pos, (x1, y1), (x2, y2)])

    def loop_distance(self, boid: "Boid") -> float:
        horizontal_dist = SCREEN_WIDTH - max(self.pos[0], boid.pos[0]) + min(self.pos[0], boid.pos[0])
        vertical_dist = SCREEN_HEIGHT - max(self.pos[1], boid.pos[1]) + min(self.pos[1], boid.pos[1])
        return [horizontal_dist, vertical_dist]

    def goal_velocity_vector(self, boids: list["Boid"]) -> list[float]:
        num_close_boids = 0
        avg_x, avg_y = 0, 0
        svec = [0, 0]
        avg_angle = 0
        for boid in boids:
            loop_d = self.loop_distance(boid)
            if self != boid and (vector_magnitude(self.calculate_distance_vector(boid)) < VISION_RADIUS or loop_d[0] < VISION_RADIUS or loop_d[1] < VISION_RADIUS):
                num_close_boids += 1
                avg_x += boid.pos[0]
                avg_y += boid.pos[1]
                avg_angle += boid.angle
       
        if num_close_boids == 0:
            return [SCREEN_WIDTH/2-self.pos[0], SCREEN_HEIGHT/2-self.pos[1]]

        m_vec = [(avg_x/num_close_boids-self._pos[0]*MVEC_FACTOR), (avg_y/num_close_boids-self._pos[1])*MVEC_FACTOR]
        s_vec = [-(avg_x-self.pos[0]*num_close_boids*SVEC_FACTOR), -(avg_y-self.pos[1]*num_close_boids*SVEC_FACTOR)]
        avg_angle /= num_close_boids
        a_vec = [ANGLE_FACTOR*math.cos(avg_angle)*AVEC_FACTOR, ANGLE_FACTOR*math.sin(avg_angle)*AVEC_FACTOR]

        return [m_vec[i]+s_vec[i]+a_vec[i] for i in range(len(m_vec))]

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
    for boid in boids:
        theta = boid.angle + math.pi + 1.15257199722 #arctan(18/8)
        if theta > 2 * math.pi:
            theta -= 2 * math.pi

        vx = boid.vel*math.cos(theta)
        vy = boid.vel*math.sin(theta)
        tvec = boid.goal_velocity_vector(boids)
        
        if boid.pos[1] <= 0:
            boid.pos[1] = SCREEN_HEIGHT
        elif boid.pos[1] >= SCREEN_HEIGHT:
            boid.pos[1] = 0
        if boid.pos[0] <= 0:
            boid.pos[0] = SCREEN_WIDTH
        elif boid.pos[0] >= SCREEN_WIDTH:
            boid.pos[0] = 0

        diff_angle = math.acos(dproduct([vx, vy], tvec)/(vector_magnitude([vx, vy])*vector_magnitude(tvec)))
        if tvec[1] > vy:
            diff_angle *= -1
        
        boid.vel = abs(math.cos(diff_angle))*VELOCITY_FACTOR
        boid.angle += diff_angle*DT
        boid.pos[0] += vx*DT
        boid.pos[1] += vy*DT

def main():
    run = True
    clock = pygame.time.Clock()
    boids = []
    for i in range(60):
        angle = random.uniform(-1, 1) + math.pi
        pos = [random.randint(0, SCREEN_WIDTH), random.randint(0,SCREEN_HEIGHT)]
        b = Boid(pos, random.randint(1, 50), angle)
        boids.append(b)
        
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
