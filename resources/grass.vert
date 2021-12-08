#version 430

in vec3 v_vert;

out vec3 tesc_pos;

void main() {
    tesc_pos = v_vert;
}
