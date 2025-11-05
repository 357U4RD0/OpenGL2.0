vertex_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(inPosition, 1.0);
    fragPosition = modelMatrix * vec4(inPosition, 1.0);
    fragNormal = normalize(vec3(modelMatrix * vec4(inNormals, 0.0)));
    fragTexCoords = inTexCoords;
}

'''

# VERTEX SHADER 1: Wave Distortion (Ocean/Fabric Effect)
wave = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;
uniform float value;

void main()
{
    // Multi-directional wave effect with more movement
    float wave1 = sin(inPosition.x * 7.0 + time * 3.5) * 0.15;
    float wave2 = cos(inPosition.z * 6.0 + time * 2.8) * 0.12;
    float wave3 = sin((inPosition.x + inPosition.z) * 4.0 + time * 4.0) * 0.08;
    float wave4 = cos(inPosition.x * 3.0 - inPosition.z * 3.0 + time * 3.2) * 0.1;
    float wave5 = sin(length(inPosition.xz) * 5.0 + time * 2.5) * 0.09;
    
    // Add circular waves
    float radialWave = sin(length(inPosition.xz) * 8.0 - time * 4.5) * 0.07;
    
    // Combine all waves with varying intensities
    float totalWave = wave1 + wave2 + wave3 + wave4 + wave5 + radialWave;
    
    // Add horizontal displacement for more dynamic movement
    vec3 displacement = vec3(
        sin(inPosition.z * 4.0 + time * 2.0) * 0.05 * value,
        totalWave * value,
        cos(inPosition.x * 4.0 + time * 2.3) * 0.05 * value
    );
    
    vec3 wavedPos = inPosition + displacement;
    
    // Calculate new normal for proper lighting
    vec3 tangent = normalize(vec3(1.0, cos(inPosition.x * 7.0 + time * 3.5) * value, 0.0));
    vec3 bitangent = normalize(vec3(0.0, cos(inPosition.z * 6.0 + time * 2.8) * value, 1.0));
    vec3 newNormal = normalize(cross(tangent, bitangent));
    
    fragPosition = modelMatrix * vec4(wavedPos, 1.0);
    gl_Position = projectionMatrix * viewMatrix * fragPosition;
    fragNormal = normalize(vec3(modelMatrix * vec4(newNormal, 0.0)));
    fragTexCoords = inTexCoords;
}
'''

# VERTEX SHADER 2: Vortex/Black Hole Effect
vortex = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;
uniform float value;

void main()
{
    vec3 center = vec3(0.0, 0.0, 0.0);
    vec3 toCenter = inPosition - center;
    float dist = length(toCenter);
    
    // Increased spiral rotation with distortion waves
    float angle = (1.0 / (dist + 0.05)) * value * 3.5 + time * 1.5;
    
    // Add warping waves that increase near center
    float warp = sin(dist * 8.0 - time * 4.0) * (1.0 / (dist + 0.5)) * value * 0.3;
    angle += warp;
    
    float cosA = cos(angle);
    float sinA = sin(angle);
    
    // Rotation around Y axis with more intensity
    mat3 rotation = mat3(
        cosA, 0.0, -sinA,
        0.0, 1.0, 0.0,
        sinA, 0.0, cosA
    );
    
    // Stronger pull with exponential falloff
    float pull = value * 0.6 * (1.0 - dist / 3.0);
    pull += sin(time * 2.0) * value * 0.15;
    
    // Add vertical stretching near center
    float stretch = 1.0 + (1.0 / (dist + 0.3)) * value * 0.4;
    
    vec3 pulledPos = inPosition - normalize(toCenter) * pull;
    pulledPos.y *= stretch;
    
    // Add turbulence
    float turbulence = sin(dist * 15.0 + time * 3.0) * value * 0.08;
    pulledPos += vec3(turbulence, turbulence * 0.5, turbulence);
    
    vec3 vortexPos = center + rotation * (pulledPos - center);
    
    fragPosition = modelMatrix * vec4(vortexPos, 1.0);
    gl_Position = projectionMatrix * viewMatrix * fragPosition;
    fragNormal = normalize(vec3(modelMatrix * vec4(rotation * inNormals, 0.0)));
    fragTexCoords = inTexCoords;
}
'''

# VERTEX SHADER 3: Explode/Shatter Effect
explode = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;
uniform float value;

void main()
{
    // Each vertex explodes outward based on its normal direction
    float explosionForce = value * 2.0;
    
    // Add some variation to the explosion
    float randomOffset = fract(sin(dot(inPosition.xy, vec2(12.9898, 78.233))) * 43758.5453);
    float explosionAmount = explosionForce * (sin(time * 2.0 + randomOffset * 6.28) * 0.5 + 0.5);
    
    // Add rotation during explosion
    float rotationSpeed = time * 3.0 + randomOffset * 6.28;
    float cosR = cos(rotationSpeed);
    float sinR = sin(rotationSpeed);
    
    mat3 rotation = mat3(
        cosR, sinR, 0.0,
        -sinR, cosR, 0.0,
        0.0, 0.0, 1.0
    );
    
    vec3 explodedPos = inPosition + inNormals * explosionAmount;
    explodedPos = rotation * explodedPos;
    
    fragPosition = modelMatrix * vec4(explodedPos, 1.0);
    gl_Position = projectionMatrix * viewMatrix * fragPosition;
    fragNormal = normalize(vec3(modelMatrix * vec4(rotation * inNormals, 0.0)));
    fragTexCoords = inTexCoords;
}
'''