#version 440

#define PI 3.1415926538

#define N_SEGMENTS 4

layout (triangles) in;
layout (triangle_strip, max_vertices = 3*2 * N_SEGMENTS) out;
// layout (triangle_strip, max_vertices = 3+3*2 * N_SEGMENTS) out;

in vec3 g_normal[];

out vec3 f_color;

uniform float u_grassHeight;
uniform float u_grassWidth;
uniform float u_grassScale;
uniform float u_windStrength;
uniform float u_randomOrientationStrenght;

uniform mat4 u_viewMatrix;
uniform mat4 u_projectionMatrix;

uniform float u_time;

mat4 calcRotateMat4X(float radian) {
    return mat4(
        1.0, 0.0, 0.0, 0.0,
        0.0, cos(radian), -sin(radian), 0.0,
        0.0, sin(radian), cos(radian), 0.0,
        0.0, 0.0, 0.0, 1.0
    );
}

mat4 calcRotateMat4Y(float radian) {
    return mat4(
        cos(radian), 0.0, sin(radian), 0.0,
        0.0, 1.0, 0.0, 0.0,
        -sin(radian), 0.0, cos(radian), 0.0,
        0.0, 0.0, 0.0, 1.0
    );
}

mat4 calcRotateMat4Z(float radian) {
    return mat4(
        cos(radian), -sin(radian), 0.0, 0.0,
        sin(radian), cos(radian), 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0
    );
}

mat4 calcRotateMat4(vec3 radian) {
    return calcRotateMat4X(radian.x) * calcRotateMat4Y(radian.y) * calcRotateMat4Z(radian.z);
}

mat4 calcTranslateMat4(vec3 v) {
    return mat4(
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        v.x, v.y, v.z, 1.0
    );
}

vec3 hsvTorgb(vec3 c) {
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

float rand(float co) { return fract(sin(co*(91.3458)) * 47453.5453); }
float rand(vec2 co){ return fract(sin(dot(co.xy ,vec2(12.9898,78.233))) * 43758.5453); }
float rand(vec3 co){ return rand(co.xy+rand(co.z)); }


float map(float value, float min1, float max1, float min2, float max2) {
    return min2 + (value - min1) * (max2 - min2) / (max1 - min1);
}

float easeInCubic(float x) {
    return x * x * x;
}

void main() {
    vec3 center = (gl_in[0].gl_Position.xyz +
                    gl_in[1].gl_Position.xyz +
                    gl_in[2].gl_Position.xyz) / 3;

    float angle = map(rand(center.xyz), 0, 1, -PI, PI);
    vec3 offset = vec3(rand(gl_in[0].gl_Position.xyz), 0.0, rand(gl_in[1].gl_Position.xyz)) * 0.1;

    mat4 mvp = u_projectionMatrix * u_viewMatrix;
    mat4 rotateMat = calcRotateMat4Y(angle);
    mat4 transtateMatPos = calcTranslateMat4(center);
    mat4 transtateMatOffset = calcTranslateMat4(offset);

    float yaw = atan(g_normal[0].z, g_normal[0].x);
    float pitch = atan(sqrt(g_normal[0].z * g_normal[0].z + g_normal[0].x * g_normal[0].x), g_normal[0].y) + PI;
    mat4 rotateNormals = calcRotateMat4(vec3(0.0, yaw, pitch));

    yaw = (rand(center.xyz) * 2.0*PI - PI) * u_randomOrientationStrenght;
    pitch = (rand(center.zxy) * 2.0*PI - PI) * u_randomOrientationStrenght;
    mat4 rotateRandom = calcRotateMat4(vec3(0.0, yaw, pitch));

    mat4 mat = mvp * transtateMatPos * rotateNormals * transtateMatOffset;

    // output initial geometry
    // f_color = vec3(0.5);
    // gl_Position = mvp * gl_in[0].gl_Position;
    // EmitVertex();
    // gl_Position = mvp * gl_in[1].gl_Position;
    // EmitVertex();
    // gl_Position = mvp * gl_in[2].gl_Position;
    // EmitVertex();
    // EndPrimitive();

    /*
    2 --- 3      -0.5,1 - 0.5,1
    |  \  |        |        |
    0 --- 1      -0.5,0 - 0.5,0
    */
    vec4 p0 = vec4(-u_grassWidth, 0.0, 0.0, 1.0) * u_grassScale;
    vec4 p1 = vec4(u_grassWidth, 0.0, 0.0, 1.0) * u_grassScale;
    vec4 p2 = vec4(-u_grassWidth, u_grassHeight, 0.0, 1.0) * u_grassScale;
    vec4 p3 = vec4(u_grassWidth, u_grassHeight, 0.0, 1.0) * u_grassScale;

    const float wind_speed = 1.0;
    vec3 wind_offset = vec3(
        sin(u_time * wind_speed + center.x) + sin(u_time * wind_speed + center.z*2.0),
        0.0,
        cos(u_time * wind_speed + center.x * 2.0) + cos(u_time + center.z * wind_speed)
    );

    for (int i = 0 ; i < N_SEGMENTS ; ++i) {
        float c1 = easeInCubic(map(i+0, 0, N_SEGMENTS, 0.5, 0.95));
        float c2 = easeInCubic(map(i+1, 0, N_SEGMENTS, 0.5, 0.95));

        vec3 color1 = hsvTorgb(vec3(0.3, 1.0, c1));
        vec3 color2 = hsvTorgb(vec3(0.3, 1.0, c2));

        float wind_force1 = easeInCubic(map(i+0, 0.0, N_SEGMENTS, 0.0, 1.0)) * u_windStrength;
        float wind_force2 = easeInCubic(map(i+1, 0.0, N_SEGMENTS, 0.0, 1.0)) * u_windStrength;

        vec4 wind_offset1 = vec4(wind_offset * wind_force1, 1.0);
        vec4 wind_offset2 = vec4(wind_offset * wind_force2, 1.0);

        f_color = color1;
        gl_Position = mat * (rotateMat * rotateRandom * p0 + wind_offset1);
        EmitVertex();
        f_color = color2;
        gl_Position = mat * (rotateMat * rotateRandom * p2 + wind_offset2);
        EmitVertex();
        f_color = color1;
        gl_Position = mat * (rotateMat * rotateRandom * p1 + wind_offset1);
        EmitVertex();
        EndPrimitive();

        f_color = color1;
        gl_Position = mat * (rotateMat * rotateRandom * p1 + wind_offset1);
        EmitVertex();
        f_color = color2;
        gl_Position = mat * (rotateMat * rotateRandom * p2 + wind_offset2);
        EmitVertex();
        f_color = color2;
        gl_Position = mat * (rotateMat * rotateRandom * p3 + wind_offset2);
        EmitVertex();
        EndPrimitive();

        p0.y += u_grassHeight * u_grassScale;
        p1.y += u_grassHeight * u_grassScale;
        p2.y += u_grassHeight * u_grassScale;
        p3.y += u_grassHeight * u_grassScale;
    }
}
