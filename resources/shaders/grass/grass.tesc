#version 430

in vec3 tesc_pos[];

layout(vertices=3) out;
out vec3 tese_pos[];

uniform float u_TessLevel;

void main(){
    tese_pos[gl_InvocationID] = tesc_pos[gl_InvocationID];

    gl_TessLevelOuter[0] = u_TessLevel;
    gl_TessLevelOuter[1] = u_TessLevel;
    gl_TessLevelOuter[2] = u_TessLevel;

    gl_TessLevelInner[0] = u_TessLevel;
}
