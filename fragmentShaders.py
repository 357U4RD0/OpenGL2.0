# FRAGMENT: Portal interdimensional
portal = """
#version 450
in vec2 uvs;
in vec3 norms;
in vec3 worldPos;

uniform sampler2D tex0;
uniform float time;
uniform vec3 pointLight;
uniform float ambientLight;

out vec4 fragColor;

void main() {
    vec4 texColor = texture(tex0, uvs);
    
    // Distorsión de portal giratorio
    vec2 center = vec2(0.5, 0.5);
    vec2 uv = uvs - center;
    float angle = atan(uv.y, uv.x);
    float radius = length(uv);
    
    float spiral = angle + radius * 10.0 - time * 2.0;
    
    // Anillos de energía concéntricos
    float rings = sin(radius * 30.0 - time * 5.0) * 0.5 + 0.5;
    
    // Colores psicodélicos del portal
    vec3 color1 = vec3(0.5, 0.0, 1.0);  // Púrpura
    vec3 color2 = vec3(0.0, 1.0, 1.0);  // Cian
    vec3 color3 = vec3(1.0, 0.0, 0.5);  // Rosa
    vec3 color4 = vec3(0.0, 1.0, 0.3);  // Verde neón
    
    // Mezcla compleja de colores
    float colorMix1 = sin(spiral * 2.0) * 0.5 + 0.5;
    float colorMix2 = cos(spiral * 1.5 + time) * 0.5 + 0.5;
    
    vec3 portalColor = mix(color1, color2, colorMix1);
    portalColor = mix(portalColor, color3, colorMix2);
    portalColor = mix(portalColor, color4, rings);
    
    // Efecto de profundidad infinita
    float depth = 1.0 - radius * 2.0;
    depth = max(depth, 0.0);
    portalColor *= depth + 0.5;
    
    // Fresnel extremo
    vec3 viewDir = normalize(vec3(0.0, 0.0, 1.0));
    float fresnel = pow(1.0 - abs(dot(norms, viewDir)), 4.0);
    vec3 rimGlow = portalColor * fresnel * 5.0;
    
    // Partículas de energía
    float particles = sin(uvs.x * 50.0 + time * 10.0) * cos(uvs.y * 50.0 - time * 8.0);
    particles = step(0.95, particles);
    vec3 sparkles = vec3(1.0) * particles * 2.0;
    
    // Iluminación
    vec3 lightDir = normalize(pointLight - worldPos);
    float diff = max(dot(norms, lightDir), 0.0);
    
    vec3 finalColor = texColor.rgb * 0.2 + portalColor * 1.5 + rimGlow + sparkles;
    finalColor *= (ambientLight * 0.5 + diff * 0.5);
    
    // Pulso hipnótico
    float pulse = sin(time * 4.0) * 0.3 + 0.7;
    finalColor *= pulse;
    
    fragColor = vec4(finalColor, texColor.a);
}
"""

# FRAGMENT: Plasma eléctrico
plasma = """
#version 450
in vec2 uvs;
in vec3 norms;
in vec3 worldPos;

uniform sampler2D tex0;
uniform float time;
uniform vec3 pointLight;
uniform float ambientLight;

out vec4 fragColor;

void main() {
    vec4 texColor = texture(tex0, uvs);
    
    // Rayos eléctricos procedurales
    float electricity1 = sin(uvs.x * 20.0 + time * 15.0 + sin(uvs.y * 30.0)) * 0.5 + 0.5;
    float electricity2 = cos(uvs.y * 25.0 - time * 12.0 + cos(uvs.x * 25.0)) * 0.5 + 0.5;
    float electricity3 = sin(uvs.x * 15.0 + uvs.y * 15.0 + time * 10.0) * 0.5 + 0.5;
    
    // Combinar rayos
    float bolts = electricity1 * electricity2 * electricity3;
    bolts = pow(bolts, 3.0); // Hacer rayos más definidos
    
    // Colores de plasma electrico
    vec3 electric1 = vec3(0.1, 0.3, 1.0);  // Azul eléctrico
    vec3 electric2 = vec3(0.4, 0.8, 1.0);  // Azul claro
    vec3 electric3 = vec3(1.0, 1.0, 1.0);  // Blanco
    vec3 electric4 = vec3(0.6, 0.0, 1.0);  // Púrpura
    
    // Gradiente de temperatura del plasma
    float temp = sin(worldPos.y * 3.0 + time * 2.0) * 0.5 + 0.5;
    vec3 plasmaColor = mix(electric1, electric2, temp);
    plasmaColor = mix(plasmaColor, electric3, bolts * 1.5);
    plasmaColor = mix(plasmaColor, electric4, electricity1 * 0.3);
    
    // Campo magnético visible
    float field = sin(uvs.x * 10.0 + time * 3.0) * cos(uvs.y * 10.0 - time * 4.0);
    field = field * 0.5 + 0.5;
    plasmaColor += vec3(0.2, 0.5, 1.0) * field * 0.4;
    
    // Arcos voltaicos
    float arcs = step(0.98, sin(uvs.y * 100.0 + time * 20.0 + sin(uvs.x * 50.0)));
    vec3 arcGlow = vec3(1.0, 0.8, 1.0) * arcs * 3.0;
    
    // Corona eléctrica
    vec3 viewDir = normalize(vec3(0.0, 0.0, 1.0));
    float corona = pow(1.0 - abs(dot(norms, viewDir)), 2.0);
    vec3 coronaGlow = plasmaColor * corona * 2.0;
    
    // Iluminación
    vec3 lightDir = normalize(pointLight - worldPos);
    float diff = max(dot(norms, lightDir), 0.0);
    
    vec3 finalColor = texColor.rgb * 0.15 + plasmaColor * 1.8 + arcGlow + coronaGlow;
    finalColor *= (ambientLight * 0.4 + diff * 0.6);
    
    // Inestabilidad eléctrica
    float flicker = sin(time * 30.0) * 0.1 + 0.9;
    float surge = sin(time * 5.0) * 0.2 + 0.8;
    finalColor *= flicker * surge;
    
    fragColor = vec4(finalColor, texColor.a);
}
"""

# FRAGMENT: Galaxia cósmica
cosmic = """
#version 450
in vec2 uvs;
in vec3 norms;
in vec3 worldPos;

uniform sampler2D tex0;
uniform float time;
uniform vec3 pointLight;
uniform float ambientLight;

out vec4 fragColor;

void main() {
    vec4 texColor = texture(tex0, uvs);
    
    // Nebulosa en movimiento
    float nebula1 = sin(uvs.x * 5.0 + time * 0.5) * cos(uvs.y * 5.0 - time * 0.3);
    float nebula2 = sin(uvs.x * 3.0 - time * 0.4) * cos(uvs.y * 4.0 + time * 0.6);
    float nebula3 = sin(uvs.x * 7.0 + time * 0.7) * sin(uvs.y * 6.0 - time * 0.5);
    
    float nebulaNoise = (nebula1 + nebula2 + nebula3) / 3.0;
    nebulaNoise = nebulaNoise * 0.5 + 0.5;
    
    // Colores cósmicos profundos
    vec3 space1 = vec3(0.05, 0.0, 0.2);   // Púrpura oscuro
    vec3 space2 = vec3(0.0, 0.1, 0.3);    // Azul profundo
    vec3 nebula = vec3(0.8, 0.2, 0.6);    // Rosa nebulosa
    vec3 star = vec3(0.9, 0.9, 1.0);      // Blanco estelar
    vec3 aurora = vec3(0.0, 0.8, 0.6);    // Verde aurora
    
    // Mezcla de nebulosa
    vec3 cosmicColor = mix(space1, space2, sin(time * 0.5) * 0.5 + 0.5);
    cosmicColor = mix(cosmicColor, nebula, nebulaNoise * 0.7);
    cosmicColor = mix(cosmicColor, aurora, nebula2 * 0.4);
    
    // Campo de estrellas
    float starField = sin(uvs.x * 200.0 + time * 2.0) * sin(uvs.y * 200.0 - time * 1.5);
    starField = step(0.995, starField);
    
    // Estrellas parpadeantes
    float twinkle = sin(uvs.x * 100.0 + time * 10.0) * sin(uvs.y * 100.0 + time * 8.0);
    twinkle = step(0.99, twinkle) * (sin(time * 5.0) * 0.5 + 0.5);
    
    vec3 stars = star * (starField + twinkle) * 2.0;
    
    // Espiral galáctica
    vec2 center = vec2(0.5, 0.5);
    vec2 uv = uvs - center;
    float angle = atan(uv.y, uv.x);
    float radius = length(uv);
    
    float spiral = sin(angle * 3.0 + radius * 10.0 - time * 1.0) * 0.5 + 0.5;
    vec3 spiralGlow = nebula * spiral * radius * 0.5;
    
    // Halo cósmico
    vec3 viewDir = normalize(vec3(0.0, 0.0, 1.0));
    float halo = pow(1.0 - abs(dot(norms, viewDir)), 3.0);
    vec3 haloGlow = mix(aurora, nebula, sin(time * 2.0) * 0.5 + 0.5);
    haloGlow *= halo * 1.5;
    
    // Polvo estelar
    float dust = sin(worldPos.x * 20.0 + time) * cos(worldPos.y * 20.0 - time) * 0.5 + 0.5;
    cosmicColor += vec3(0.4, 0.3, 0.5) * dust * 0.2;
    
    // Iluminación
    vec3 lightDir = normalize(pointLight - worldPos);
    float diff = max(dot(norms, lightDir), 0.0);
    
    vec3 finalColor = texColor.rgb * 0.25 + cosmicColor * 1.2 + stars + spiralGlow + haloGlow;
    finalColor *= (ambientLight * 0.6 + diff * 0.4);
    
    // Respiración cósmica
    float breathe = sin(time * 1.5) * 0.2 + 0.8;
    finalColor *= breathe;
    
    fragColor = vec4(finalColor, texColor.a);
}
"""