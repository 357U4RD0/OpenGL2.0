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
MasterChief.visible = False

Nave = Model("models/nave.obj")
Nave.AddTexture("textures/nave_low_poly.png")
Nave.position.z = -20
Nave.rotation.y = 180
Nave.visible = True

print("="*50)
print("POSICIÓN INICIAL:")
print(f"Cámara: {rend.camera.position}")
print(f"Modelo Z: {MasterChief.position.z}")
print(f"Modelo visible: {MasterChief.visible}")
print(f"Vértices del modelo: {MasterChief.vertexCount}")
print(f"Texturas cargadas: {len(MasterChief.textures)}")
print("="*50)

rend.scene.append(MasterChief)
rend.scene.append(Nave)

vertexShaders = [pulse, wave, basic]
fragmentShaders = [portal, plasma, cosmic]

currentVertex = 0
currentFragment = 0

rend.SetShaders(vertexShaders[currentVertex], fragmentShaders[currentFragment])

print("Shader activo:", rend.activeShader)
print("Modelo visible:", MasterChief.visible)
print("Numero de shaders vertex:", len(vertexShaders))
print("Numero de shaders fragment:", len(fragmentShaders))

rend.camera.rotation = glm.vec3(0, 0, 0)

isRunning = True

while isRunning:
	deltaTime = clock.tick(60) / 1000
	rend.elapsedTime += deltaTime
	
	keys = pygame.key.get_pressed()
	mouseVel = pygame.mouse.get_rel()
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False
		
		elif event.type == pygame.KEYDOWN:
			# Cambiar Vertex Shaders (1, 2, 3)
			if event.key == pygame.K_1:
				currentVertex = 0
				rend.SetShaders(vertexShaders[currentVertex], fragmentShaders[currentFragment])
			elif event.key == pygame.K_2:
				currentVertex = 1
				rend.SetShaders(vertexShaders[currentVertex], fragmentShaders[currentFragment])
			elif event.key == pygame.K_3:
				currentVertex = 2
				rend.SetShaders(vertexShaders[currentVertex], fragmentShaders[currentFragment])
			
			# Cambiar Fragment Shaders (4, 5, 6)
			elif event.key == pygame.K_4:
				currentFragment = 0
				rend.SetShaders(vertexShaders[currentVertex], fragmentShaders[currentFragment])
			elif event.key == pygame.K_5:
				currentFragment = 1
				rend.SetShaders(vertexShaders[currentVertex], fragmentShaders[currentFragment])
			elif event.key == pygame.K_6:
				currentFragment = 2
				rend.SetShaders(vertexShaders[currentVertex], fragmentShaders[currentFragment])
	
	# Movimiento WASD en XY
	moveSpeed = 5
	if keys[K_w]:
		rend.camera.position.y += moveSpeed * deltaTime
	if keys[K_s]:
		rend.camera.position.y -= moveSpeed * deltaTime
	if keys[K_a]:
		rend.camera.position.x -= moveSpeed * deltaTime
	if keys[K_d]:
		rend.camera.position.x += moveSpeed * deltaTime
	
	# Zoom con Z y X
	if keys[K_z]:
		rend.camera.position.z += 5 * deltaTime
	if keys[K_x]:
		rend.camera.position.z -= 5 * deltaTime
	
	# Rotar cámara con click izquierdo + arrastrar
	if pygame.mouse.get_pressed()[0]:
		rend.camera.rotation.y -= mouseVel[0] * deltaTime * 20
		rend.camera.rotation.x -= mouseVel[1] * deltaTime * 20
		# Limitar rotación vertical
		rend.camera.rotation.x = max(-89, min(89, rend.camera.rotation.x))
	
	rend.camera.Update()
	rend.Render()
	pygame.display.flip()

pygame.quit()