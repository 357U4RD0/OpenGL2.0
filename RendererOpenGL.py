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

# Inicializar pygame PRIMERO
pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
pygame.display.set_caption("OpenGL Renderer 2025")
clock = pygame.time.Clock()

rend = Renderer(screen)

rend.pointLight = glm.vec3(5, 5, 10)  # Luz desde arriba y adelante
rend.ambientLight = 0.8  # Más luz ambiental para ver mejor

# Current shader configuration
currVertexShader = vertex_shader
currFragmentShader = fragment_shader

orbitDistance = 5.0  # Distancia radial de la cámara respecto al centro

rend.SetShaders(currVertexShader, currFragmentShader)

# Camera setup
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

try:
    Nave = Model("models/nave.obj")
    Nave.AddTexture("textures/nave_low_poly.png")    
    Nave.position = glm.vec3(0, -0.2, 0)
    Nave.rotation.y = 180  # Que mire hacia la cámara al iniciar
    Nave.scale = glm.vec3(1.0, 1.0, 1.0)
    
    rend.scene.append(Nave)

except Exception as e:
    print("  Verifica que los modelos estén bien cargados")

# Time and value uniforms for shaders
elapsedTime = 0.0
value = 0.5

# Camera rotation
camAngle = 0

isRunning = True

print("\nFRAGMENT SHADERS:")
print("  1 - Default fragment shader (with lighting)")
print("  2 - Hologram shader")
print("  3 - Plasma/Fire shader")
print("  4 - Matrix Digital Rain shader")
print("VERTEX SHADERS:")
print("  7 - Default vertex shader")
print("  8 - Spiral/Twist shader")
print("  9 - Pulse/Heartbeat shader")
print("  0 - Glitch/Displacement shader")
print("\nCONTROLESS:")
print("  Click IZQUIERDO/DERECHO - Rotate camera")
print("  Mouse Wheel - Zoom in/out")
print("  SPACE - Auto-rotate camera")
print("  ESC - Quit")
print("=======================\n")

autoRotate = False

while isRunning:
    
    keys = pygame.key.get_pressed()
    mouseVel = pygame.mouse.get_rel()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        
        elif event.type == pygame.MOUSEWHEEL:
            orbitDistance = max(1.5, min(25.0, orbitDistance - event.y * 0.5))
        
        elif event.type == pygame.KEYDOWN:
            # Fragment shader selection
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
                print("Fragment Shader: Chromatic")
            
            elif event.key == pygame.K_4:
                currFragmentShader = iridescent
                rend.SetShaders(currVertexShader, currFragmentShader)
                print("Fragment Shader: Iridescent")
            
            # Vertex shader selection
            elif event.key == pygame.K_7:
                currVertexShader = vertex_shader
                rend.SetShaders(currVertexShader, currFragmentShader)
                print("Vertex Shader: Default")
            
            elif event.key == pygame.K_8:
                currVertexShader = wave
                rend.SetShaders(currVertexShader, currFragmentShader)
                print("Vertex Shader: Wave")
            
            elif event.key == pygame.K_9:
                currVertexShader = vortex
                rend.SetShaders(currVertexShader, currFragmentShader)
                print("Vertex Shader: Vortex")
            
            elif event.key == pygame.K_0:
                currVertexShader = explode
                rend.SetShaders(currVertexShader, currFragmentShader)
                print("Vertex Shader: Explode")
            
            elif event.key == pygame.K_f:
                rend.ToggleFilledMode()
                print("Wireframe mode:", "ON" if not rend.filledMode else "OFF")
            
            elif event.key == pygame.K_SPACE:
                autoRotate = not autoRotate
                print("Auto-rotate:", "ON" if autoRotate else "OFF")
            
            elif event.key == pygame.K_ESCAPE:
                isRunning = False

    deltaTime = clock.tick(60) / 1000
    elapsedTime += deltaTime
    
    # Handle Z/X keys for value control
    if keys[K_z]:
        value = max(0.0, value - 1.0 * deltaTime)
    if keys[K_x]:
        value = min(2.0, value + 1.0 * deltaTime)
    
    # Camera rotation with mouse
    if pygame.mouse.get_pressed()[0]:  # Left click
        camAngle -= mouseVel[0] * deltaTime * 100
    if pygame.mouse.get_pressed()[2]:  # Right click
        camAngle += mouseVel[0] * deltaTime * 100
    
    # Auto-rotate
    if autoRotate:
        camAngle += deltaTime * 30
    
    # Update camera position (orbit around model)
    if len(rend.scene) > 0:
        distance = max(1.5, min(25.0, orbitDistance))
        target = rend.scene[0].position
        targetFocus = glm.vec3(target.x, target.y + 0.5, target.z)

        rend.camera.position = glm.vec3(
            targetFocus.x + sin(radians(camAngle)) * distance,
            targetFocus.y + 0.8,
            targetFocus.z + cos(radians(camAngle)) * distance
        )

        rend.camera.viewMatrix = glm.lookAt(
            rend.camera.position,
            targetFocus,
            glm.vec3(0, 1, 0)
        )
        
       
    # Pass time and value to renderer
    rend.elapsedTime = elapsedTime
    rend.value = value

    rend.Render()
    
    # Asegurar que todo el rendering se complete
    glFinish()

    err = glGetError()
    if err != GL_NO_ERROR:
        print(f"GL ERROR: {err}")
    if err != GL_NO_ERROR:
        print(f"GL ERROR: {err}")
    
    pygame.display.flip()
    clock.tick(60)  # Limitar a 60 FPS

pygame.quit()