#version 430

in vec3 in_position;
// in vec3 in_color;

// out vec3 f_color;

uniform mat4 u_viewMatrix;
uniform mat4 u_projectionMatrix;

void main() {
    gl_Position = u_projectionMatrix * u_viewMatrix * vec4(in_position * 50.0, 1.0);
    // f_color = in_color;
}
