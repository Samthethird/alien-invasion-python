import pygame
import random

# Particle class
class Particle:
    def __init__(self, x, y, color, dx, dy, life_time, size):
        self.x = x
        self.y = y
        (a, b) = dx
        (c, d) = dy
        self.dx = random.uniform(a, b)
        self.dy = random.uniform(c, d)
        self.lifetime = life_time
        self.color = color
        self.size = size

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.lifetime -= 1

    def draw(self, window):
        position = (int(self.x), int(self.y))
        pygame.draw.circle(window, self.color, position, self.size)

# Particle system class
class ParticleSystem:
    def __init__(self):
        self.particles = []

    def add_particle(self, x, y, color, dx, dy, life_time, size):
        self.particles.append(Particle(x, y, color, dx, dy, life_time, size))

    def update(self):
        for particle in self.particles:
            particle.update()
            if particle.lifetime <= 0:
                self.particles.remove(particle)

    def draw(self, window):
        for particle in self.particles:
            particle.draw(window)