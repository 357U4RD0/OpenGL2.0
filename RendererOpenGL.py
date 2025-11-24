import pygame
import pygame.display
from pygame.locals import *
from math import sin, cos, radians
from OpenGL.GL import glFlush, glGetError, glFinish, GL_NO_ERROR
import glm
from gl import Renderer
from model import Model
from vertexShaders import *
from fragmentShaders import *

width = 960
height = 540

deltaTime = 0.0

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
pygame.display.set_caption("OpenGL Renderer 2025")
clock = pygame.time.Clock()

rend = Renderer(screen)

rend.pointLight = glm.vec3(5, 5, 10)
rend.ambientLight = 0.8

currVertexShader = vertex_shader
currFragmentShader = fragment_shader

orbitDistance = 5.0
camHeight = 0.8

rend.SetShaders(currVertexShader, currFragmentShader)

rend.camera.position = glm.vec3(0, 1.2, orbitDistance)
rend.camera.viewMatrix = glm.lookAt(
    rend.camera.position,
    glm.vec3(0, 0.5, 0),
    glm.vec3(0, 1, 0)
)

skyboxTextures = ["skybox/right.png",
                  "skybox/left.png",
                  "skybox/top.png",
                  "skybox/bottom.png",
                  "skybox/front.png",
                  "skybox/back.png"]

rend.CreateSkybox(skyboxTextures)
print("Skybox cargado exitosamente!")

models = []
activeModelIndex = 1 

try:
    Nave = Model("models/nave.obj")
    Nave.AddTexture("textures/nave_low_poly.png")
    Nave.position = glm.vec3(-3.9, 1.8, -4)
    Nave.rotation.y = 215
    Nave.scale = glm.vec3(1.0)
    models.append(Nave)
    print("Cargada: Nave")
except Exception as e:
    print(f"Error cargando Nave: {e}")

try:
    MasterChief = Model("models/ChiefMaster.obj")
    MasterChief.AddTexture("textures/m_9bac2ffc-e51f-7210-2ba4-e09401d31fb3_baseColor.png")
    MasterChief.AddTexture("textures/m_70695387-6504-7cbe-0590-e640ab45d163_baseColor.png")
    MasterChief.AddTexture("textures/m_fec53d62-b190-ebba-3617-4e25f7011c55_baseColor.png")
    MasterChief.position = glm.vec3(0, 0.2, 0)
    MasterChief.rotation.y = 180
    MasterChief.scale = glm.vec3(1.0)
    models.append(MasterChief)
    print("Cargado: MasterChief")
except Exception as e:
    print(f"Error cargando MasterChief: {e}")

try:
    Falcon = Model("models/falcon.obj")
    Falcon.AddTexture("textures/default_baseColor.png")
    Falcon.AddTexture("textures/default_metallicRoughness.png")
    Falcon.AddTexture("textures/default_normal.png")
    Falcon.position = glm.vec3(2.8, 2.8, -7)
    Falcon.rotation.y = 155
    Falcon.scale = glm.vec3(2.3)
    models.append(Falcon)
    print("Cargado: Falcon")
except Exception as e:
    print(f"Error cargando Falcon: {e}")

try:
    Planeta = Model("models/Planeta.obj")
    Planeta.AddTexture("textures/material_baseColor.jpeg")
    Planeta.AddTexture("textures/material_normal.png")
    Planeta.position = glm.vec3(-5.5, -0.8, -25)
    Planeta.scale = glm.vec3(5)
    models.append(Planeta)
    print("Cargado: Planeta")
except Exception as e:
    print(f"Error cargando Planeta: {e}")

try:
    Espada = Model("models/Energy_sword.obj")
    Espada.AddTexture("textures/lambert8_baseColor.jpeg")
    Espada.position = glm.vec3(-0.7, 0.13, 0.5)
    Espada.scale = glm.vec3(0.7)
    Espada.rotation.x = 45
    Espada.rotation.y = 180
    models.append(Espada)
    print("Cargado: Espada")
except Exception as e:
    print(f"Error cargando Espada: {e}")

if len(models) == 0:
    print("No se cargó ningún modelo.")
    pygame.quit()
    raise SystemExit("No models loaded.")

for m in models:
    try:
        rend.scene.append(m)
    except Exception as e:
        print(f"Error añadiendo modelo a la escena: {e}")

if len(models) > 0:
    if activeModelIndex < 0 or activeModelIndex >= len(models):
        activeModelIndex = 0
else:
    activeModelIndex = 0

print(f"Modelos cargados: {len(models)}. Cámara inicialmente sobre: {activeModelIndex + 1}")

elapsedTime = 0.0
value = 0.5

camAngle = 0
autoRotate = False

print("\nFRAGMENT SHADERS:")
print("  1 - Default fragment shader (with lighting)")
print("  2 - Neon shader")
print("  3 - Kaleidoscope shader")
print("  4 - Iridescent shader")
print("VERTEX SHADERS:")
print("  5 - Default vertex shader")
print("  6 - Wave shader")
print("  7 - Vortex shader")
print("  8 - Explode shader")
print("\nCONTROLES:")
print("  Flecha IZQUIERDA/DERECHA - Cambiar modelo objetivo de la cámara")
print("  Flecha ARRIBA/ABAJO - Subir/bajar cámara")
print("  Click IZQUIERDO/DERECHO - Rotar cámara")
print("  Rueda del mouse - Zoom")
print("  Espacio - Auto-rotar")
print("  ESC - Salir")
print("=======================\n")

isRunning = True

while isRunning:

    keys = pygame.key.get_pressed()
    mouseVel = pygame.mouse.get_rel()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

        elif event.type == pygame.MOUSEWHEEL:
            orbitDistance = max(1.5, min(25.0, orbitDistance - event.y * 0.5))

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1:
                currFragmentShader = fragment_shader
                rend.SetShaders(currVertexShader, currFragmentShader)
                print("Fragment Shader: Default")

            elif event.key == pygame.K_2:
                currFragmentShader = neon
                rend.SetShaders(currVertexShader, currFragmentShader)
                print("Fragment Shader: Neon")

            elif event.key == pygame.K_3:
                currFragmentShader = kaleidoscope
                rend.SetShaders(currVertexShader, currFragmentShader)
                print("Fragment Shader: Kaleidoscope")

            elif event.key == pygame.K_4:
                currFragmentShader = iridescent
                rend.SetShaders(currVertexShader, currFragmentShader)
                print("Fragment Shader: Iridescent")

            elif event.key == pygame.K_5:
                currVertexShader = vertex_shader
                rend.SetShaders(currVertexShader, currFragmentShader)
                print("Vertex Shader: Default")

            elif event.key == pygame.K_6:
                currVertexShader = wave
                rend.SetShaders(currVertexShader, currFragmentShader)
                print("Vertex Shader: Wave")

            elif event.key == pygame.K_7:
                currVertexShader = vortex
                rend.SetShaders(currVertexShader, currFragmentShader)
                print("Vertex Shader: Vortex")

            elif event.key == pygame.K_8:
                currVertexShader = explode
                rend.SetShaders(currVertexShader, currFragmentShader)
                print("Vertex Shader: Explode")

            elif event.key == pygame.K_LEFT:
                if len(models) > 0:
                    activeModelIndex = (activeModelIndex - 1) % len(models)
                    print(f"Cámara orbitando: Modelo {activeModelIndex + 1}")
                else:
                    print("No hay modelos cargados para orbitar.")

            elif event.key == pygame.K_RIGHT:
                if len(models) > 0:
                    activeModelIndex = (activeModelIndex + 1) % len(models)
                    print(f"Cámara orbitando: Modelo {activeModelIndex + 1}")
                else:
                    print("No hay modelos cargados para orbitar.")

            elif event.key == pygame.K_UP:
                camHeight += 0.2

            elif event.key == pygame.K_DOWN:
                camHeight -= 0.2

            elif event.key == pygame.K_SPACE:
                autoRotate = not autoRotate
                print("Auto-rotate:", "ON" if autoRotate else "OFF")

            elif event.key == pygame.K_ESCAPE:
                isRunning = False

    deltaTime = clock.tick(60) / 1000
    elapsedTime += deltaTime

    if pygame.mouse.get_pressed()[0]:
        camAngle -= mouseVel[0] * deltaTime * 20
    if pygame.mouse.get_pressed()[2]:
        camAngle += mouseVel[0] * deltaTime * 20

    if autoRotate:
        camAngle += deltaTime * 30

    if len(models) > 0:
        if activeModelIndex < 0 or activeModelIndex >= len(models):
            activeModelIndex = 0

        target = models[activeModelIndex].position
        targetFocus = glm.vec3(target.x, target.y + 0.5, target.z)

        distance = max(1.5, min(25.0, orbitDistance))

        rend.camera.position = glm.vec3(
            targetFocus.x + sin(radians(camAngle)) * distance,
            targetFocus.y + camHeight,
            targetFocus.z + cos(radians(camAngle)) * distance
        )

        rend.camera.viewMatrix = glm.lookAt(
            rend.camera.position,
            targetFocus,
            glm.vec3(0, 1, 0)
        )

    rend.elapsedTime = elapsedTime
    rend.value = value

    try:
        rend.Render()
    except Exception as e:
        print(f"Error en rend.Render(): {e}")

    glFinish()

    err = glGetError()
    if err != GL_NO_ERROR:
        print(f"GL ERROR: {err}")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()