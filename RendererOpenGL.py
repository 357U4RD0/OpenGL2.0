import pygame
from pygame.locals import *
import glm
from gl import Renderer
from model import Model
from vertexShaders import *
from fragmentShaders import *

width = 960
height = 540

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.pointLight = glm.vec3(1, 1, 1)

# Crear Skybox
skyboxTextures = ["skybox/right.png",
				  "skybox/left.png",
				  "skybox/top.png",
				  "skybox/bottom.png",
				  "skybox/front.png",
				  "skybox/back.png"]

rend.CreateSkybox(skyboxTextures)

# Cargar modelo
MasterChief = Model("models/ChiefMaster.obj")
MasterChief.AddTexture("textures/m_9bac2ffc-e51f-7210-2ba4-e09401d31fb3_baseColor.png")
MasterChief.AddTexture("textures/m_70695387-6504-7cbe-0590-e640ab45d163_baseColor.png")
MasterChief.AddTexture("textures/m_fec53d62-b190-ebba-3617-4e25f7011c55_baseColor.png")
MasterChief.position.z = -20
MasterChief.rotation.y = 180
MasterChief.visible = True

rend.scene.append(MasterChief)

vertexShaders = []
fragmentShaders = []

currentVertex = 0
currentFragment = 0

#rend.SetShaders(vertexShaders[currentVertex], fragmentShaders[currentFragment])

isRunning = True

while isRunning:
	clock.tick(60)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False
		
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_1:
				currentVertex = 0
				rend.SetShaders(vertexShaders[currentVertex], fragmentShaders[currentFragment])
			elif event.key == pygame.K_2:
				currentVertex = 1
				rend.SetShaders(vertexShaders[currentVertex], fragmentShaders[currentFragment])
			elif event.key == pygame.K_3:
				currentVertex = 2
				rend.SetShaders(vertexShaders[currentVertex], fragmentShaders[currentFragment])
			elif event.key == pygame.K_4:
				currentFragment = 0
				rend.SetShaders(vertexShaders[currentVertex], fragmentShaders[currentFragment])
			elif event.key == pygame.K_5:
				currentFragment = 1
				rend.SetShaders(vertexShaders[currentVertex], fragmentShaders[currentFragment])
			elif event.key == pygame.K_6:
				currentFragment = 2
				rend.SetShaders(vertexShaders[currentVertex], fragmentShaders[currentFragment])

	rend.elapsedTime += clock.get_time() / 1000.0
	rend.Render()
	pygame.display.flip()

pygame.quit()