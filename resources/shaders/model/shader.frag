#version 430

// in vec3 f_color;

out vec4 fragColor;

void main() {
    // fragColor = vec4(f_color, 1.0);
    fragColor = vec4(vec3(0.5), 1.0);
}
