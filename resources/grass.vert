#version 430

// in vec3 v_vert;
in vec3 in_position;

out vec3 tesc_pos;

void main() {
    tesc_pos = in_position * 50.0;
    // tesc_pos = v_vert;
}
