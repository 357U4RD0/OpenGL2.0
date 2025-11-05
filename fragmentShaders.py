# GLSL

fragment_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;

void main()
{
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max(0.0, dot(fragNormal, lightDir)) + ambientLight;
    fragColor = texture(tex0, fragTexCoords) * intensity;
}

'''

neon = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;
uniform float time;

void main()
{
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max(0.0, dot(fragNormal, lightDir)) + ambientLight;
    
    // Rim lighting for neon edge glow
    vec3 viewDir = normalize(-fragPosition.xyz);
    float rimPower = 3.0;
    float rim = 1.0 - max(0.0, dot(viewDir, fragNormal));
    rim = pow(rim, rimPower);
    
    // Animated neon colors
    vec3 neonColor1 = vec3(
        0.9 + 0.1 * sin(time * 2.0),
        0.1 + 0.2 * sin(time * 2.3),
        0.9 + 0.1 * sin(time * 1.7)
    ); // Cyan-Magenta
    
    vec3 neonColor2 = vec3(
        0.1 + 0.3 * sin(time * 1.8),
        0.9 + 0.1 * sin(time * 2.1),
        0.3 + 0.2 * sin(time * 2.5)
    ); // Green-Cyan
    
    // Blend between two neon colors
    float colorMix = sin(fragTexCoords.y * 5.0 + time) * 0.5 + 0.5;
    vec3 neonColor = mix(neonColor1, neonColor2, colorMix);
    
    // Pulsating effect
    float pulse = sin(time * 3.0) * 0.3 + 0.7;
    
    vec4 texColor = texture(tex0, fragTexCoords);
    
    // Combine texture with neon glow
    vec3 baseColor = texColor.rgb * intensity * 0.4;
    vec3 glowColor = neonColor * rim * 2.0 * pulse;
    
    vec3 finalColor = baseColor + glowColor;
    
    // Add extra brightness to edges
    finalColor += neonColor * rim * rim * 0.5;
    
    fragColor = vec4(finalColor, 1.0);
}
'''

# FRAGMENT SHADER 2: Chromatic Aberration + Distortion
kaleidoscope = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;
uniform float time;

void main()
{
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max(0.0, dot(fragNormal, lightDir)) + ambientLight;
    
    // Create kaleidoscope effect with rotating mirrors
    vec2 center = vec2(0.5, 0.5);
    vec2 uv = fragTexCoords - center;
    
    // Polar coordinates for kaleidoscope
    float angle = atan(uv.y, uv.x) + time * 0.8;
    float radius = length(uv);
    
    // Create mirror segments (8 segments)
    float segments = 8.0;
    float segmentAngle = 6.28318 / segments;
    angle = mod(angle, segmentAngle);
    angle = abs(angle - segmentAngle * 0.5);
    
    // Convert back to cartesian
    vec2 kaleidoUV = vec2(cos(angle), sin(angle)) * radius + center;
    
    // Multiple layers of energy with different speeds
    float energy1 = sin(radius * 20.0 - time * 4.0) * 0.5 + 0.5;
    float energy2 = cos(radius * 15.0 + time * 3.0) * 0.5 + 0.5;
    float energy3 = sin(angle * 10.0 + time * 5.0) * 0.5 + 0.5;
    
    // Pulsating energy rings
    float rings = sin(radius * 30.0 - time * 6.0);
    rings = smoothstep(0.4, 0.6, rings);
    
    // Rainbow spectrum based on angle and time
    vec3 color1 = vec3(
        0.5 + 0.5 * sin(time * 2.0 + angle * 3.0),
        0.5 + 0.5 * sin(time * 2.5 + angle * 3.0 + 2.0),
        0.5 + 0.5 * sin(time * 3.0 + angle * 3.0 + 4.0)
    );
    
    vec3 color2 = vec3(
        0.5 + 0.5 * cos(time * 1.8 + radius * 10.0),
        0.5 + 0.5 * cos(time * 2.2 + radius * 10.0 + 2.0),
        0.5 + 0.5 * cos(time * 2.7 + radius * 10.0 + 4.0)
    );
    
    // Mix colors based on energy fields
    vec3 energyColor = mix(color1, color2, energy1);
    energyColor = mix(energyColor, color1 * color2 * 2.0, energy2);
    
    // Add bright core
    float core = 1.0 - smoothstep(0.0, 0.3, radius);
    energyColor += vec3(1.0) * core * (0.5 + 0.5 * sin(time * 4.0));
    
    // Sample texture with kaleidoscope UV
    vec4 texColor = texture(tex0, kaleidoUV);
    
    // Combine everything
    vec3 finalColor = texColor.rgb * 0.3;
    finalColor += energyColor * (energy1 + energy2) * 0.7;
    finalColor += vec3(1.0) * rings * 0.4;
    finalColor *= intensity;
    
    // Add shimmer
    float shimmer = sin(time * 10.0 + radius * 50.0 + angle * 20.0) * 0.1 + 0.9;
    finalColor *= shimmer;
    
    fragColor = vec4(finalColor, 1.0);
}
'''

# FRAGMENT SHADER 3: Iridescent/Oil Slick Effect
iridescent = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;
uniform float time;

void main()
{
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max(0.0, dot(fragNormal, lightDir)) + ambientLight;
    
    // View-dependent iridescence
    vec3 viewDir = normalize(-fragPosition.xyz);
    float viewDot = dot(viewDir, fragNormal);
    float fresnel = pow(1.0 - abs(viewDot), 2.0);
    
    // Create rainbow spectrum based on viewing angle and position
    float spectrum = fresnel * 3.0 + fragTexCoords.x + fragTexCoords.y + time * 0.5;
    
    // Convert spectrum to RGB (rainbow colors)
    vec3 rainbow;
    spectrum = fract(spectrum);
    
    if (spectrum < 0.166) {
        rainbow = mix(vec3(1.0, 0.0, 0.0), vec3(1.0, 0.5, 0.0), spectrum * 6.0);
    } else if (spectrum < 0.333) {
        rainbow = mix(vec3(1.0, 0.5, 0.0), vec3(1.0, 1.0, 0.0), (spectrum - 0.166) * 6.0);
    } else if (spectrum < 0.5) {
        rainbow = mix(vec3(1.0, 1.0, 0.0), vec3(0.0, 1.0, 0.0), (spectrum - 0.333) * 6.0);
    } else if (spectrum < 0.666) {
        rainbow = mix(vec3(0.0, 1.0, 0.0), vec3(0.0, 1.0, 1.0), (spectrum - 0.5) * 6.0);
    } else if (spectrum < 0.833) {
        rainbow = mix(vec3(0.0, 1.0, 1.0), vec3(0.0, 0.0, 1.0), (spectrum - 0.666) * 6.0);
    } else {
        rainbow = mix(vec3(0.0, 0.0, 1.0), vec3(1.0, 0.0, 1.0), (spectrum - 0.833) * 6.0);
    }
    
    // Add metallic shimmer
    float shimmer = sin(time * 5.0 + fragPosition.x * 20.0 + fragPosition.y * 20.0) * 0.5 + 0.5;
    rainbow *= (0.7 + shimmer * 0.3);
    
    vec4 texColor = texture(tex0, fragTexCoords);
    
    // Blend texture with iridescent effect
    vec3 baseColor = texColor.rgb * intensity * 0.3;
    vec3 iridescent = rainbow * (fresnel * 0.8 + 0.2);
    
    vec3 finalColor = baseColor + iridescent;
    
    fragColor = vec4(finalColor, 1.0);
}
'''