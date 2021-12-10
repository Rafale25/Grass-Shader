#! /usr/bin/python3

import sys
import math
import random
import struct
import time

import moderngl
import imgui
import pyglet
from pyrr import Matrix44
# import glm

import moderngl_window
from moderngl_window.integrations.imgui import ModernglWindowRenderer
from moderngl_window.scene import KeyboardCamera
from moderngl_window.opengl.vao import VAO
# from moderngl_window import geometry

from glm import vec3, vec4
from math import pi, cos, sin, fabs, fmod
from random import uniform
from array import array

from fps_counter import FpsCounter

def dump(obj):
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, getattr(obj, attr)))


class MyWindow(moderngl_window.WindowConfig):
    title = 'Grass'
    gl_version = (4, 3)
    window_size = (1920, 1080)
    fullscreen = False
    resizable = False
    vsync = True
    resource_dir = './resources'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.width, self.height = self.window_size
        imgui.create_context()
        self.imgui = ModernglWindowRenderer(self.wnd)

        self.wireframe = False
        self.cull_face = False

        self.TessLevel = 1
        self.GrassHeight = 1.0
        self.GrassWidth = 0.1
        self.GrassScale = 0.1
        self.WindStrength = 0.05

        self.RandomOrientationStrenght = 0.0

        self.start_time = time.time()

        self.query_debug_values = {}
        self.query = self.ctx.query(samples=False, time=True)
        self.fps_counter = FpsCounter()

        self.camera = KeyboardCamera(
            self.wnd.keys,
            fov=60.0,
            aspect_ratio=self.wnd.aspect_ratio,
            near=0.1,
            far=100.0,
        )

        self.camera.mouse_sensitivity = 0.1
        self.camera.velocity = 1
        self.camera.position.xyz = (0, 7, 7)
        self.camera.pitch = -22
        self.camera_active = True

        self.program = {
            'MODEL':
                self.load_program(
                    vertex_shader='./shaders/model/shader.vert',
                    fragment_shader='./shaders/model/shader.frag'),
            'GRASS':
                self.load_program(
                    vertex_shader='./shaders/grass/grass.vert',
                    tess_control_shader='./shaders/grass/grass.tesc',
                    tess_evaluation_shader='./shaders/grass/grass.tese',
                    geometry_shader='./shaders/grass/grass.geom',
                    fragment_shader='./shaders/grass/grass.frag')
        }

        scale = 2.0
        vertices = array('f', [
            #position
            0.0, 0.0, 0.0,
            0.0, 0.0, scale,
            scale, 0.0, 0.0,

            0.0, 0.0, scale,
            scale, 0.0, scale,
            scale, 0.0, 0.0,

            0.0, 0.0, 0.0,
            0.0, -scale, 0.0,
            0.0, 0.0, scale,
        ])

        self.vbo = self.ctx.buffer(vertices)
        self.vao = VAO(name="grass", mode=moderngl.TRIANGLES)
        self.vao.buffer(self.vbo, '3f', ['in_position'])
        # self.vao.buffer(self.vbo, '3f', ['v_vert'])
        self.ctx.patch_vertices = 3 # for tesselation

        self.scene_bunny = self.load_scene(path="./bunny.obj")
        self.scene_cow = self.load_scene(path="./cow.obj")
        # self.modelMatrix = glm.scale(glm.mat4(1.0), glm.vec3(20.0))
        # self.modelMatrix = Matrix44.create_from_scale(20.0)
        # dump(self.scene.meshes[0].vao)

        # print(type(self.camera.matrix))
        # print(type(self.modelMatrix))


    def update_uniforms(self, frametime):
        self.program['GRASS']['u_TessLevel'] = self.TessLevel
        self.program['GRASS']['u_grassHeight'] = self.GrassHeight
        self.program['GRASS']['u_grassWidth'] = self.GrassWidth
        self.program['GRASS']['u_grassScale'] = self.GrassScale
        self.program['GRASS']['u_windStrength'] = self.WindStrength
        self.program['GRASS']['u_randomOrientationStrenght'] = self.RandomOrientationStrenght
        self.program['GRASS']['u_time'] = time.time() - self.start_time

        # self.program['GRASS']['u_modelMatrix'] = self.modelMatrix

        for str, program in self.program.items():
            if 'u_viewMatrix' in program:
                program['u_viewMatrix'].write(self.camera.matrix)
            if 'u_projectionMatrix' in program:
                program['u_projectionMatrix'].write(self.camera.projection.matrix)

    def update(self, time_since_start, frametime):
        self.fps_counter.update(frametime)
        self.update_uniforms(frametime)

    def render(self, time_since_start, frametime):
        self.update(time_since_start, frametime)

        self.ctx.enable_only(moderngl.CULL_FACE * self.cull_face | moderngl.DEPTH_TEST)
        self.ctx.wireframe = self.wireframe

        self.ctx.clear(0.2, 0.2, 0.2)
        # self.ctx.screen.use()

        # with self.query:
        #     self.vao.render(
        #         program=self.program['GRASS'],
        #         mode=moderngl.PATCHES)
        # self.query_debug_values['grass render'] = self.query.elapsed * 10e-7

        # with self.query:
        #     self.scene.meshes[0].vao.render(
        #         program=self.program['MODEL'])
        # self.query_debug_values['bunny render'] = self.query.elapsed * 10e-7

        with self.query:
            self.scene_bunny.meshes[0].vao.render(
                program=self.program['GRASS'],
                mode=moderngl.PATCHES)
        self.query_debug_values['grass bunny render'] = self.query.elapsed * 10e-7

        # self.scene.draw(
        #     projection_matrix=self.camera.projection.matrix,
        #     camera_matrix=self.camera.matrix * self.modelMatrix,
        # )


        # disables wireframe and depth_test for imgui
        self.ctx.wireframe = False
        self.ctx.disable(moderngl.DEPTH_TEST)

        self.imgui_newFrame(frametime)
        self.imgui_render()

    def cleanup(self):
        print('Cleaning up ressources.')
        for str, program in self.program.items():
            program.release()

    def __del__(self):
        self.cleanup()

    ## IMGUI
    from _gui import\
        imgui_newFrame,\
        imgui_render

    ## EVENTS
    from _event import \
        resize,\
        key_event,\
        mouse_position_event,\
        mouse_drag_event,\
        mouse_scroll_event,\
        mouse_press_event,\
        mouse_release_event,\
        unicode_char_entered

def main():
    MyWindow.run()

if __name__ == "__main__":
    main()
