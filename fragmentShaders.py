default_basic = """
#version 450
in vec2 uvs;
uniform sampler2D tex0;
out vec4 fragColor;

void main() {
    fragColor = texture(tex0, uvs);
}
"""