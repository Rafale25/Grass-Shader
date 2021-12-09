#version 430

layout(triangles, equal_spacing, cw) in;

in vec3 tese_pos[];

out vec3 g_normal;

vec3 lerp3D(vec3 v0, vec3 v1, vec3 v2)
{
    return vec3(gl_TessCoord.x) * v0 +
        vec3(gl_TessCoord.y) * v1 +
        vec3(gl_TessCoord.z) * v2;
}

vec3 triangle_normal(vec3 p0, vec3 p1, vec3 p2) {
    return normalize(cross(p1 - p0, p2 - p0));
}

void main(){
    vec3 pos = lerp3D(tese_pos[0], tese_pos[1], tese_pos[2]);

    gl_Position = vec4(pos, 1.0);

    g_normal = triangle_normal(tese_pos[0], tese_pos[2], tese_pos[1]);
}
