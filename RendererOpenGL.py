import pygame
from pygame.locals import *
import glm
from gl import Renderer
from model import Model
from vertexShaders import default_basic as vertex_default
from fragmentShaders import default_basic as fragment_default

print("="*50)
print("VERIFICANDO SHADERS:")
print(f"vertex_default existe: {vertex_default is not None}")
print(f"fragment_default existe: {fragment_default is not None}")
if vertex_default:
    print(f"Longitud vertex: {len(vertex_default)}")
if fragment_default:
    print(f"Longitud fragment: {len(fragment_default)}")
print("="*50)

width = 1024
height = 600

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

#rend.CreateSkybox(skyboxTextures)

# Cargar modelo
MasterChief = Model("models/ChiefMaster.obj")
MasterChief.AddTexture("textures/m_9bac2ffc-e51f-7210-2ba4-e09401d31fb3_baseColor.png")
MasterChief.AddTexture("textures/m_70695387-6504-7cbe-0590-e640ab45d163_baseColor.png")
MasterChief.AddTexture("textures/m_fec53d62-b190-ebba-3617-4e25f7011c55_baseColor.png")
MasterChief.position.z = -10
MasterChief.rotation.y = 180
MasterChief.visible = False

Nave = Model("models/nave.obj")
Nave.AddTexture("textures/nave_low_poly.png")
Nave.position.z = -10
Nave.rotation.y = 180
Nave.visible = True

print("="*50)
print("POSICIÓN INICIAL NAVE:")
print(f"Cámara: {rend.camera.position}")
print(f"Modelo Z: {Nave.position.z}")
print(f"Modelo visible: {Nave.visible}")
print(f"Vértices del modelo: {Nave.vertexCount}")
print(f"Texturas cargadas: {len(Nave.textures)}")
print("="*50)

rend.scene.append(MasterChief)
rend.scene.append(Nave)

# SOLO SHADER BÁSICO
rend.SetShaders(vertex_default, fragment_default)
print("Shader default_basic activado")

rend.camera.rotation = glm.vec3(0, 0, 0)
rend.camera.position.z = 5

isRunning = True

while isRunning:
	deltaTime = clock.tick(60) / 1000
	rend.elapsedTime += deltaTime
	
	keys = pygame.key.get_pressed()
	mouseVel = pygame.mouse.get_rel()
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False
	
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
		rend.camera.rotation.x = max(-89, min(89, rend.camera.rotation.x))
	
	rend.camera.Update()
	rend.Render()
	pygame.display.flip()

pygame.quit()