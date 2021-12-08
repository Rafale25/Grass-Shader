#! /usr/bin/python3

import sys
import math
import random
import struct
import time

import moderngl
import imgui
import pyglet
import glm

import moderngl_window
from moderngl_window.integrations.imgui import ModernglWindowRenderer
from moderngl_window.scene import KeyboardCamera
from moderngl_window.opengl.vao import VAO
# from moderngl_window import geometry

from glm import vec3, vec4
from math import pi, cos, sin, fabs
from random import uniform
from array import array

from fps_counter import FpsCounter

def dump(obj):
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, getattr(obj, attr)))


class MyWindow(moderngl_window.WindowConfig):
    title = 'Grass'
    gl_version = (4, 3)
    window_size = (1280, 720)
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
        self.camera.position.xyz = (0.5, 0.5, 1.5)
        self.camera.pitch = -22

        self.program = {
            'GRASS':
                self.load_program(
                    vertex_shader='./grass.vert',
                    tess_control_shader='./grass.tesc',
                    tess_evaluation_shader='./grass.tese',
                    fragment_shader='./grass.frag')
        }
        # geometry_shader='./grass.geom',
        # defines={
        #     'NB_SEGMENTS': Tree.NB_SEGMENTS,
        #     'NB_FACES': Tree.NB_FACES}),

        vertices = array('f', [
            #position       #normals
            0.0, 0.0, 0.0,  #0.0, 1.0, 0.0,
            0.0, 0.0, 1.0,  #0.0, 1.0, 0.0,
            1.0, 0.0, 0.0,  #0.0, 1.0, 0.0,

            0.0, 0.0, 1.0,  #0.0, 1.0, 0.0,
            1.0, 0.0, 1.0,  #0.0, 1.0, 0.0,
            1.0, 0.0, 0.0,  #0.0, 1.0, 0.0,
        ])

        self.vbo = self.ctx.buffer(vertices)
        self.vao = VAO(name="grass", mode=moderngl.TRIANGLES)
        self.vao.buffer(self.vbo, '3f', ['v_vert'])
        # self.vao.buffer(self.vbo, '3f 3f', ['v_vert', 'v_normal'])
        self.ctx.patch_vertices = 3 # for tesselation


    def update_uniforms(self, frametime):
        self.program['GRASS']['u_TessLevel'] = self.TessLevel

        for str, program in self.program.items():
            if 'viewMatrix' in program:
                program['viewMatrix'].write(self.camera.matrix)
            if 'projectionMatrix' in program:
                program['projectionMatrix'].write(self.camera.projection.matrix)

    def update(self, time_since_start, frametime):
        # Light.x = cos(time_since_start*0.2) * 6.0
        # Light.y = 6.0
        # Light.z = sin(time_since_start*0.2) * 6.0
        self.fps_counter.update(frametime)

        # self.camera.look_at(vec=[0,0,0], pos=[0, 0, 0])
        self.update_uniforms(frametime)

    def render(self, time_since_start, frametime):
        self.update(time_since_start, frametime)

        self.ctx.enable_only(moderngl.CULL_FACE * self.cull_face | moderngl.DEPTH_TEST)
        self.ctx.wireframe = self.wireframe

        # self.ctx.screen.use()

        with self.query:
            self.vao.render(
                program=self.program['GRASS'],
                mode=moderngl.PATCHES)
        self.query_debug_values['grass render'] = self.query.elapsed * 10e-7


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
