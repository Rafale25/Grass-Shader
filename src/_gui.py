import imgui

def imgui_newFrame(self, frametime):
    imgui.new_frame()
    imgui.begin("Properties", True)

    imgui.text("fps: {:.2f}".format(self.fps_counter.get_fps()))
    for query, value in self.query_debug_values.items():
        imgui.text("{}: {:.3f} ms".format(query, value))

    imgui.text("x: {:.2f}\ny: {:.2f}\nz: {:.2f}".format(*self.camera.position.xyz))

    imgui.spacing(); imgui.spacing()

    c, self.wireframe = imgui.checkbox("Wireframe", self.wireframe)
    c, self.cull_face = imgui.checkbox("Cull Face", self.cull_face)

    c, self.camera_active = imgui.checkbox("camera active", self.camera_active)

    imgui.spacing(); imgui.spacing()
    imgui.text("Grass Settings");
    imgui.begin_group()
    c, self.TessLevel = imgui.slider_int(
        label="subdivision",
        value=self.TessLevel,
        min_value=1,
        max_value=64)

    c, self.GrassHeight = imgui.slider_float(
        label="height",
        value=self.GrassHeight,
        min_value=0.1,
        max_value=5.0)

    c, self.GrassWidth = imgui.slider_float(
        label="width",
        value=self.GrassWidth,
        min_value=0.01,
        max_value=0.2)

    c, self.GrassScale = imgui.slider_float(
        label="scale",
        value=self.GrassScale,
        min_value=0.01,
        max_value=2.0)




    imgui.end_group()

    imgui.end()

def imgui_render(self):
    imgui.render()
    self.imgui.render(imgui.get_draw_data())
