#version 430

layout(triangles, equal_spacing) in;

in vec3 tese_pos[];

uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

vec3 lerp3D(vec3 v0, vec3 v1, vec3 v2)
{
    return vec3(gl_TessCoord.x) * v0 +
        vec3(gl_TessCoord.y) * v1 +
        vec3(gl_TessCoord.z) * v2;
}

void main(){
    vec3 pos = lerp3D(tese_pos[0], tese_pos[1], tese_pos[2]);
    gl_Position = projectionMatrix * viewMatrix * vec4(pos, 1.0);
}
