#version 430

in vec3 tesc_pos[];

layout(vertices=3) out; // (1)
out vec3 tese_pos[];

uniform float u_TessLevel;
// const float u_TessLevel = 8.0;

void main(){
    // (2)
    tese_pos[gl_InvocationID] = tesc_pos[gl_InvocationID];

    // (3)
    gl_TessLevelOuter[0] = u_TessLevel;
    gl_TessLevelOuter[1] = u_TessLevel;
    gl_TessLevelOuter[2] = u_TessLevel;

    // (4)
    gl_TessLevelInner[0] = u_TessLevel;
}
