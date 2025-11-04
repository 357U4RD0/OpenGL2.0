# VERTEX: Básico sin deformaciones
basic = """
#version 450
layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texCoords;
layout(location = 2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

out vec2 uvs;
out vec3 norms;
out vec3 worldPos;

void main() {
    vec4 worldPosition = modelMatrix * vec4(position, 1.0);
    gl_Position = projectionMatrix * viewMatrix * worldPosition;
    
    uvs = texCoords;
    norms = normalize(mat3(modelMatrix) * normals);
    worldPos = worldPosition.xyz;
}
"""

# VERTEX: Ondas suaves
wave = """
#version 450
layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texCoords;
layout(location = 2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;

out vec2 uvs;
out vec3 norms;
out vec3 worldPos;

void main() {
    float wave = sin(position.y * 2.0 + time) * 0.05;
    vec3 pos = position + normals * wave;
    
    vec4 worldPosition = modelMatrix * vec4(pos, 1.0);
    gl_Position = projectionMatrix * viewMatrix * worldPosition;
    
    uvs = texCoords;
    norms = normalize(mat3(modelMatrix) * normals);
    worldPos = worldPosition.xyz;
}
"""

# VERTEX: Pulso
pulse = """
#version 450
layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texCoords;
layout(location = 2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;

out vec2 uvs;
out vec3 norms;
out vec3 worldPos;

void main() {
    float pulsate = sin(time * 2.0) * 0.03 + 1.0;
    vec3 pos = position * pulsate;
    
    vec4 worldPosition = modelMatrix * vec4(pos, 1.0);
    gl_Position = projectionMatrix * viewMatrix * worldPosition;
    
    uvs = texCoords;
    norms = normalize(mat3(modelMatrix) * normals);
    worldPos = worldPosition.xyz;
}
"""