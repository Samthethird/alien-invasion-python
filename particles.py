import pygame
import random

# Particle class
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.dx = random.uniform(-1.7, 1.7)
        self.dy = random.uniform(-0.3, 2)
        self.lifetime = 55  
        self.color = color

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.lifetime -= 1

    def draw(self, window):
        position = (int(self.x), int(self.y))
        pygame.draw.circle(window, self.color, position, 3)

# Particle system class
class ParticleSystem:
    def __init__(self):
        self.particles = []

    def add_particle(self, x, y, color):
        self.particles.append(Particle(x, y, color))

    def update(self):
        for particle in self.particles:
            particle.update()
            if particle.lifetime <= 0:
                self.particles.remove(particle)

    def draw(self, window):
        for particle in self.particles:
            particle.draw(window)

# falling Particle class
class FallingParticle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.dx = random.uniform(-0.7, 0.7)
        self.dy = random.uniform(-1, 0.3)
        self.lifetime = 100
        self.color = color

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.lifetime -= 1

    def draw(self, window):
        position = (int(self.x), int(self.y))
        pygame.draw.circle(window, self.color, position, 3)

# Falling particle system class
class FallingParticlesystem(ParticleSystem):
    def __init__(self):
        super().__init__()

    def add_particle(self, x, y, color):
        self.particles.append(FallingParticle(x,y, color))