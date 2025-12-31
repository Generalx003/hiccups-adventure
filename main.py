import sys
import math
import time
import random

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class StageCompleteScreen:

    def __init__(self):
        self.window_width = 800
        self.window_height = 600
        self.completion_active = False
        self.stage_number = 1
        self.animation_time = 0.0
        self.auto_advance_time = 10.0
        self.auto_advance_enabled = False

        self.crystal_rotation = 0
        self.platform_glow = 0

        self.trees = []
        self.init_trees()

        self.stage_messages = {
            1: {
                'title': 'MEMORY FRAGMENT RECOVERED',
                'subtitle': 'The First Echo Awakens',
                'description': 'A memory of home returns to you.'
            },
            2: {
                'title': 'PATHWAY ILLUMINATED',
                'subtitle': 'Deeper Memories Surface',
                'description': 'Friendship remembered, bonds restored.'
            },
            3: {
                'title': 'GUARDIAN DEFEATED',
                'subtitle': 'The Truth Revealed',
                'description': 'Your true identity is restored.'
            }
        }

        self.colors = {
            'gold': (0.95, 0.85, 0.3),
            'silver': (0.8, 0.8, 0.9),
            'purple': (0.5, 0.3, 0.7),
            'green': (0.3, 0.8, 0.4)
        }

    def init_trees(self):
        import random
        random.seed(123)

        for i in range(12):
            angle = random.uniform(0, 360)
            distance = random.uniform(100, 250)
            x = math.cos(math.radians(angle)) * distance
            y = math.sin(math.radians(angle)) * distance

            self.trees.append({
                'x': x,
                'y': y,
                'length': random.uniform(40, 70),
                'trunk_width': random.uniform(6, 10),
                'fallen_angle': random.uniform(0, 360),
                'tilt': random.uniform(-15, 15),
                'color': (0.15 + random.uniform(0, 0.05), 0.2 + random.uniform(0, 0.05), 0.12)
            })

    def draw_tree(self, tree):
        glPushMatrix()
        glTranslatef(tree['x'], tree['y'], tree['trunk_width'])

        glRotatef(tree['fallen_angle'], 0, 0, 1)
        glRotatef(90 + tree['tilt'], 0, 1, 0)

        glColor3f(0.25, 0.18, 0.12)
        w = tree['trunk_width']
        l = tree['length']

        glBegin(GL_QUADS)

        glVertex3f(-w, -w, 0)
        glVertex3f(w, -w, 0)
        glVertex3f(w, -w, l)
        glVertex3f(-w, -w, l)

        glVertex3f(-w, w, 0)
        glVertex3f(-w, w, l)
        glVertex3f(w, w, l)
        glVertex3f(w, w, 0)

        glVertex3f(-w, -w, 0)
        glVertex3f(-w, -w, l)
        glVertex3f(-w, w, l)
        glVertex3f(-w, w, 0)

        glVertex3f(w, -w, 0)
        glVertex3f(w, w, 0)
        glVertex3f(w, w, l)
        glVertex3f(w, -w, l)
        glEnd()

        glColor3f(0.2, 0.15, 0.1)
        for i in range(3):
            branch_pos = tree['length'] * (0.3 + i * 0.25)
            branch_angle = i * 120

            glPushMatrix()
            glTranslatef(0, 0, branch_pos)
            glRotatef(branch_angle, 0, 0, 1)
            glRotatef(45, 0, 1, 0)

            bw = tree['trunk_width'] * 0.3
            bl = tree['length'] * 0.3
            glBegin(GL_QUADS)
            glVertex3f(-bw, -bw, 0)
            glVertex3f(bw, -bw, 0)
            glVertex3f(bw, -bw, bl)
            glVertex3f(-bw, -bw, bl)
            glVertex3f(-bw, bw, 0)
            glVertex3f(-bw, bw, bl)
            glVertex3f(bw, bw, bl)
            glVertex3f(bw, bw, 0)
            glEnd()
            glPopMatrix()

        glPopMatrix()

    def init_opengl(self):
        glClearColor(0.02, 0.02, 0.05, 1.0)
        glEnable(GL_DEPTH_TEST)

    def setup_3d_projection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, self.window_width / self.window_height, 1, 1000)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def setup_2d_projection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.window_width, 0, self.window_height)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)

    def draw_text(self, text, x, y, color=(1.0, 1.0, 1.0), font=GLUT_BITMAP_HELVETICA_18):
        glColor3f(*color)
        glRasterPos2f(x, y)
        for char in text:
            glutBitmapCharacter(font, ord(char))

    def draw_centered_text(self, text, y, color=(1.0, 1.0, 1.0), font=GLUT_BITMAP_HELVETICA_18):
        text_width = sum(glutBitmapWidth(font, ord(c)) for c in text)
        x = (self.window_width - text_width) / 2.0
        self.draw_text(text, x, y, color, font)

    def draw_3d_crystal(self, size, color):
        glColor3f(*color)

        glBegin(GL_TRIANGLES)
        for i in range(4):
            angle1 = i * 90
            angle2 = (i + 1) * 90
            x1 = math.cos(math.radians(angle1)) * size
            y1 = math.sin(math.radians(angle1)) * size
            x2 = math.cos(math.radians(angle2)) * size
            y2 = math.sin(math.radians(angle2)) * size

            glNormal3f(0, 0, 1)
            glVertex3f(0, 0, size * 2)
            glVertex3f(x1, y1, 0)
            glVertex3f(x2, y2, 0)

            glNormal3f(0, 0, -1)
            glVertex3f(0, 0, -size * 2)
            glVertex3f(x2, y2, 0)
            glVertex3f(x1, y1, 0)
        glEnd()

    def draw_completion_scene(self):
        gluLookAt(0, -180, 200, 0, 0, 0, 0, 0, 1)

        glBegin(GL_QUADS)
        glNormal3f(0, 0, 1)
        glColor3f(0.03, 0.03, 0.06)
        glVertex3f(-500, -500, -5)
        glVertex3f(500, -500, -5)
        glVertex3f(500, 500, -5)
        glVertex3f(-500, 500, -5)
        glEnd()

        for tree in self.trees:
            self.draw_tree(tree)

        pedestal_positions = [(-80, 0), (0, 0), (80, 0)]

        for i, (px, py) in enumerate(pedestal_positions):
            stage_num = i + 1
            is_complete = stage_num <= self.stage_number

            if is_complete:
                glColor3f(0.15, 0.15, 0.22)
            else:
                glColor3f(0.08, 0.08, 0.12)

            glPushMatrix()
            glTranslatef(px, py, 0)

            glBegin(GL_TRIANGLES)
            for j in range(32):
                angle1 = j * (360 / 32)
                angle2 = (j + 1) * (360 / 32)
                x1 = math.cos(math.radians(angle1)) * 35
                y1 = math.sin(math.radians(angle1)) * 35
                x2 = math.cos(math.radians(angle2)) * 35
                y2 = math.sin(math.radians(angle2)) * 35

                glVertex3f(0, 0, 0)
                glVertex3f(x1, y1, 0)
                glVertex3f(x2, y2, 0)
            glEnd()

            glBegin(GL_QUADS)
            for j in range(16):
                angle1 = j * (360 / 16)
                angle2 = (j + 1) * (360 / 16)
                x1 = math.cos(math.radians(angle1)) * 15
                y1 = math.sin(math.radians(angle1)) * 15
                x2 = math.cos(math.radians(angle2)) * 15
                y2 = math.sin(math.radians(angle2)) * 15

                glVertex3f(x1, y1, 0)
                glVertex3f(x2, y2, 0)
                glVertex3f(x2, y2, 40)
                glVertex3f(x1, y1, 40)
            glEnd()

            glPushMatrix()
            glTranslatef(0, 0, 40)
            glBegin(GL_TRIANGLES)
            for j in range(32):
                angle1 = j * (360 / 32)
                angle2 = (j + 1) * (360 / 32)
                x1 = math.cos(math.radians(angle1)) * 18
                y1 = math.sin(math.radians(angle1)) * 18
                x2 = math.cos(math.radians(angle2)) * 18
                y2 = math.sin(math.radians(angle2)) * 18

                glVertex3f(0, 0, 0)
                glVertex3f(x1, y1, 0)
                glVertex3f(x2, y2, 0)
            glEnd()
            glPopMatrix()

            if is_complete:
                glow_pulse = 0.5 + 0.3 * math.sin(self.animation_time * 0.04 + i)
                glColor4f(self.colors['gold'][0] * glow_pulse,
                         self.colors['gold'][1] * glow_pulse,
                         self.colors['gold'][2] * glow_pulse, 0.4)
                glPushMatrix()
                glTranslatef(0, 0, 1)
                glBegin(GL_QUADS)
                for j in range(32):
                    angle1 = j * (360 / 32)
                    angle2 = (j + 1) * (360 / 32)
                    x1 = math.cos(math.radians(angle1)) * 30
                    y1 = math.sin(math.radians(angle1)) * 30
                    x2 = math.cos(math.radians(angle2)) * 30
                    y2 = math.sin(math.radians(angle2)) * 30
                    x3 = math.cos(math.radians(angle2)) * 38
                    y3 = math.sin(math.radians(angle2)) * 38
                    x4 = math.cos(math.radians(angle1)) * 38
                    y4 = math.sin(math.radians(angle1)) * 38

                    glVertex3f(x1, y1, 0)
                    glVertex3f(x2, y2, 0)
                    glVertex3f(x3, y3, 0)
                    glVertex3f(x4, y4, 0)
                glEnd()
                glPopMatrix()

                glPushMatrix()
                float_offset = 5 * math.sin(self.animation_time * 0.03 + i * 1.2)
                glTranslatef(0, 0, 60 + float_offset)
                glRotatef(self.crystal_rotation + i * 120, 0, 0, 1)
                glRotatef(30, 1, 0, 0)

                glColor3f(*self.colors['gold'])
                size = 12
                glBegin(GL_TRIANGLES)
                for j in range(4):
                    angle1 = j * 90
                    angle2 = (j + 1) * 90
                    x1 = math.cos(math.radians(angle1)) * size
                    y1 = math.sin(math.radians(angle1)) * size
                    x2 = math.cos(math.radians(angle2)) * size
                    y2 = math.sin(math.radians(angle2)) * size

                    glVertex3f(0, 0, size * 1.5)
                    glVertex3f(x1, y1, 0)
                    glVertex3f(x2, y2, 0)

                for j in range(4):
                    angle1 = j * 90
                    angle2 = (j + 1) * 90
                    x1 = math.cos(math.radians(angle1)) * size
                    y1 = math.sin(math.radians(angle1)) * size
                    x2 = math.cos(math.radians(angle2)) * size
                    y2 = math.sin(math.radians(angle2)) * size

                    glVertex3f(0, 0, -size * 1.5)
                    glVertex3f(x2, y2, 0)
                    glVertex3f(x1, y1, 0)
                glEnd()

                glColor4f(1.0, 0.9, 0.5, 0.5 * glow_pulse)
                size = size * 1.3
                glBegin(GL_TRIANGLES)
                for j in range(4):
                    angle1 = j * 90
                    angle2 = (j + 1) * 90
                    x1 = math.cos(math.radians(angle1)) * size
                    y1 = math.sin(math.radians(angle1)) * size
                    x2 = math.cos(math.radians(angle2)) * size
                    y2 = math.sin(math.radians(angle2)) * size

                    glVertex3f(0, 0, size * 1.5)
                    glVertex3f(x1, y1, 0)
                    glVertex3f(x2, y2, 0)

                for j in range(4):
                    angle1 = j * 90
                    angle2 = (j + 1) * 90
                    x1 = math.cos(math.radians(angle1)) * size
                    y1 = math.sin(math.radians(angle1)) * size
                    x2 = math.cos(math.radians(angle2)) * size
                    y2 = math.sin(math.radians(angle2)) * size

                    glVertex3f(0, 0, -size * 1.5)
                    glVertex3f(x2, y2, 0)
                    glVertex3f(x1, y1, 0)
                glEnd()
                glPopMatrix()

                glColor4f(self.colors['gold'][0],
                         self.colors['gold'][1],
                         self.colors['gold'][2], 0.2)
                glPushMatrix()
                glTranslatef(0, 0, 60)
                glBegin(GL_QUADS)
                for j in range(16):
                    angle1 = j * (360 / 16)
                    angle2 = (j + 1) * (360 / 16)
                    x1 = math.cos(math.radians(angle1)) * 8
                    y1 = math.sin(math.radians(angle1)) * 8
                    x2 = math.cos(math.radians(angle2)) * 8
                    y2 = math.sin(math.radians(angle2)) * 8
                    x3 = math.cos(math.radians(angle2)) * 2
                    y3 = math.sin(math.radians(angle2)) * 2
                    x4 = math.cos(math.radians(angle1)) * 2
                    y4 = math.sin(math.radians(angle1)) * 2

                    glVertex3f(x1, y1, 0)
                    glVertex3f(x2, y2, 0)
                    glVertex3f(x3, y3, 100)
                    glVertex3f(x4, y4, 100)
                glEnd()
                glPopMatrix()
            else:
                glColor3f(0.15, 0.15, 0.18)
                glPushMatrix()
                glTranslatef(0, 0, 60)
                s = 10
                glBegin(GL_QUADS)
                glVertex3f(-s, -s, s)
                glVertex3f(s, -s, s)
                glVertex3f(s, s, s)
                glVertex3f(-s, s, s)

                glVertex3f(-s, -s, -s)
                glVertex3f(-s, s, -s)
                glVertex3f(s, s, -s)
                glVertex3f(s, -s, -s)

                glVertex3f(-s, s, -s)
                glVertex3f(-s, s, s)
                glVertex3f(s, s, s)
                glVertex3f(s, s, -s)

                glVertex3f(-s, -s, -s)
                glVertex3f(s, -s, -s)
                glVertex3f(s, -s, s)
                glVertex3f(-s, -s, s)

                glVertex3f(s, -s, -s)
                glVertex3f(s, s, -s)
                glVertex3f(s, s, s)
                glVertex3f(s, -s, s)

                glVertex3f(-s, -s, -s)
                glVertex3f(-s, -s, s)
                glVertex3f(-s, s, s)
                glVertex3f(-s, s, -s)
                glEnd()
                glPopMatrix()

            glPopMatrix()
        if self.stage_number >= 2:
            energy_pulse = 0.4 + 0.3 * math.sin(self.animation_time * 0.05)
            glColor4f(self.colors['gold'][0],
                     self.colors['gold'][1],
                     self.colors['gold'][2], energy_pulse)

            beam_thickness = 2
            glBegin(GL_QUADS)
            for i in range(min(self.stage_number - 1, 2)):
                x1, y1 = pedestal_positions[i]
                x2, y2 = pedestal_positions[i + 1]
                dx = x2 - x1
                dy = y2 - y1
                length = math.sqrt(dx*dx + dy*dy)
                if length > 0:
                    px = -dy / length * beam_thickness
                    py = dx / length * beam_thickness
                    glVertex3f(x1 + px, y1 + py, 60)
                    glVertex3f(x1 - px, y1 - py, 60)
                    glVertex3f(x2 - px, y2 - py, 60)
                    glVertex3f(x2 + px, y2 + py, 60)
            glEnd()

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.completion_active:
            self.setup_3d_projection()
            self.draw_completion_scene()

            self.setup_2d_projection()
            msg = self.stage_messages.get(self.stage_number, {
                'title': 'STAGE COMPLETE',
                'subtitle': 'Well Done!',
                'description': 'Continue your journey.'
            })

            title_y = self.window_height - 100

            for offset in [4, 2]:
                glow_intensity = 0.3 / offset
                glow_color = (self.colors['gold'][0] * glow_intensity,
                             self.colors['gold'][1] * glow_intensity,
                             self.colors['gold'][2] * glow_intensity)
                self.draw_centered_text(msg['title'], title_y + offset, glow_color, GLUT_BITMAP_TIMES_ROMAN_24)

            self.draw_centered_text(msg['title'], title_y, self.colors['gold'], GLUT_BITMAP_TIMES_ROMAN_24)

            subtitle_y = self.window_height - 150
            self.draw_centered_text(msg['subtitle'], subtitle_y, self.colors['silver'], GLUT_BITMAP_HELVETICA_18)

            desc_y = self.window_height - 190
            self.draw_centered_text(msg['description'], desc_y, (0.7, 0.7, 0.8), GLUT_BITMAP_HELVETICA_12)

            progress_text = f"Stage {self.stage_number} of 3 Complete"
            text_y = 80
            self.draw_centered_text(progress_text, text_y, self.colors['green'], GLUT_BITMAP_HELVETICA_18)

            dot_y = 50
            dot_spacing = 40
            start_x = (self.window_width - (3 * dot_spacing)) // 2

            for i in range(3):
                dot_x = start_x + i * dot_spacing + 20

                if i < self.stage_number:
                    glColor3f(*self.colors['gold'])
                else:
                    glColor3f(0.3, 0.3, 0.4)

                dot_size = 12
                glBegin(GL_QUADS)
                glVertex2f(dot_x - dot_size/2, dot_y - dot_size/2)
                glVertex2f(dot_x + dot_size/2, dot_y - dot_size/2)
                glVertex2f(dot_x + dot_size/2, dot_y + dot_size/2)
                glVertex2f(dot_x - dot_size/2, dot_y + dot_size/2)
                glEnd()

                if i < self.stage_number:
                    pulse = 0.3 + 0.2 * math.sin(self.animation_time * 0.05)
                    glColor4f(self.colors['gold'][0],
                             self.colors['gold'][1],
                             self.colors['gold'][2], pulse)
                    dot_size = 18
                    glBegin(GL_QUADS)
                    glVertex2f(dot_x - dot_size/2, dot_y - dot_size/2)
                    glVertex2f(dot_x + dot_size/2, dot_y - dot_size/2)
                    glVertex2f(dot_x + dot_size/2, dot_y + dot_size/2)
                    glVertex2f(dot_x - dot_size/2, dot_y + dot_size/2)
                    glEnd()

            if self.animation_time > 30:
                pulse = 0.7 + 0.3 * math.sin(self.animation_time * 0.08)
                prompt_y = 20
                self.draw_centered_text("Press any key to continue...", prompt_y,
                                      (0.9 * pulse, 0.9 * pulse, 1.0 * pulse),
                                      GLUT_BITMAP_HELVETICA_12)

        if not hasattr(self, 'integrated_mode') or not self.integrated_mode:
            glutSwapBuffers()

    def start_completion(self, stage_number, completion_time=0.0, auto_advance=True):
        self.stage_number = stage_number
        self.completion_active = True
        self.animation_time = 0.0
        self.crystal_rotation = 0
        self.auto_advance_enabled = auto_advance
        print(f"Stage {stage_number} completed!")

    def update(self):
        if not self.completion_active:
            return False

        self.animation_time += 0.5
        self.crystal_rotation += 0.8

        if self.auto_advance_enabled and self.animation_time >= self.auto_advance_time * 60:
            self.end_completion()
            return True

        return False

    def end_completion(self):
        self.completion_active = False
        print("Advancing to next stage...")

    def handle_input(self):
        if self.completion_active and self.animation_time > 30:
            self.end_completion()
            return True
        return False

    def is_complete(self):
        return not self.completion_active

    def keyboard(self, key, x, y):
        if key == b'\x1b':
            glutLeaveMainLoop()
        else:
            if self.handle_input():
                print("Completion screen skipped")

def draw_cube(size=1.0):
    s = size / 2
    glBegin(GL_QUADS)
    glNormal3f(0, 0, 1)
    glVertex3f(-s, -s, s)
    glVertex3f(s, -s, s)
    glVertex3f(s, s, s)
    glVertex3f(-s, s, s)
    glNormal3f(0, 0, -1)
    glVertex3f(-s, -s, -s)
    glVertex3f(-s, s, -s)
    glVertex3f(s, s, -s)
    glVertex3f(s, -s, -s)
    glNormal3f(0, 1, 0)
    glVertex3f(-s, s, -s)
    glVertex3f(-s, s, s)
    glVertex3f(s, s, s)
    glVertex3f(s, s, -s)
    glNormal3f(0, -1, 0)
    glVertex3f(-s, -s, -s)
    glVertex3f(s, -s, -s)
    glVertex3f(s, -s, s)
    glVertex3f(-s, -s, s)
    glNormal3f(1, 0, 0)
    glVertex3f(s, -s, -s)
    glVertex3f(s, s, -s)
    glVertex3f(s, s, s)
    glVertex3f(s, -s, s)
    glNormal3f(-1, 0, 0)
    glVertex3f(-s, -s, -s)
    glVertex3f(-s, -s, s)
    glVertex3f(-s, s, s)
    glVertex3f(-s, s, -s)
    glEnd()

def draw_pyramid(size=1.0):
    glBegin(GL_TRIANGLES)
    for i in range(4):
        angle1 = i * 90
        angle2 = (i + 1) * 90
        x1 = math.cos(math.radians(angle1)) * size
        y1 = math.sin(math.radians(angle1)) * size
        x2 = math.cos(math.radians(angle2)) * size
        y2 = math.sin(math.radians(angle2)) * size

        glNormal3f(0, 0, 1)
        glVertex3f(0, 0, size * 1.5)
        glVertex3f(x1, y1, 0)
        glVertex3f(x2, y2, 0)
    glEnd()

def draw_ground(size=500):
    glBegin(GL_QUADS)
    glNormal3f(0, 0, 1)
    glVertex3f(-size, -size, 0)
    glVertex3f(size, -size, 0)
    glVertex3f(size, size, 0)
    glVertex3f(-size, size, 0)
    glEnd()

def draw_character(scale=1.0):
    glPushMatrix()
    glScalef(0.4 * scale, 0.3 * scale, 0.8 * scale)
    draw_cube(1.0)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 0, 0.6 * scale)
    glScalef(0.3 * scale, 0.3 * scale, 0.3 * scale)
    draw_cube(1.0)
    glPopMatrix()

    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(side * 0.25 * scale, 0, 0.2 * scale)
        glScalef(0.1 * scale, 0.1 * scale, 0.5 * scale)
        draw_cube(1.0)
        glPopMatrix()

    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(side * 0.1 * scale, 0, -0.5 * scale)
        glScalef(0.12 * scale, 0.12 * scale, 0.6 * scale)
        draw_cube(1.0)
        glPopMatrix()

def draw_crystal(size=1.0):
    glBegin(GL_TRIANGLES)
    for i in range(4):
        angle1 = i * 90
        angle2 = (i + 1) * 90
        x1 = math.cos(math.radians(angle1)) * size
        y1 = math.sin(math.radians(angle1)) * size
        x2 = math.cos(math.radians(angle2)) * size
        y2 = math.sin(math.radians(angle2)) * size

        glVertex3f(0, 0, size * 1.5)
        glVertex3f(x1, y1, 0)
        glVertex3f(x2, y2, 0)

    for i in range(4):
        angle1 = i * 90
        angle2 = (i + 1) * 90
        x1 = math.cos(math.radians(angle1)) * size
        y1 = math.sin(math.radians(angle1)) * size
        x2 = math.cos(math.radians(angle2)) * size
        y2 = math.sin(math.radians(angle2)) * size

        glVertex3f(0, 0, -size * 1.5)
        glVertex3f(x2, y2, 0)
        glVertex3f(x1, y1, 0)
    glEnd()

class DialogueSystem:

    def __init__(self):
        self.window_width = 800
        self.window_height = 600

        self.dialogue_active = False
        self.character_name = ""
        self.dialogue_lines = []
        self.current_line = 0
        self.current_dialogue = ""
        self.displayed_text = ""
        self.char_index = 0
        self.text_complete = False

        self.text_speed = 0.03
        self.last_char_time = 0

        self.scene_rotation = 0
        self.character_bob = 0
        self.particle_time = 0

        self.characters = {
            'Hiccup': {
                'color': (0.2, 0.5, 0.3),
                'accent': (0.4, 0.7, 0.4),
                'model': 'viking'
            },
            'Mysterious Voice': {
                'color': (0.4, 0.2, 0.6),
                'accent': (0.6, 0.3, 0.8),
                'model': 'spirit'
            },
            'Memory Guardian': {
                'color': (0.6, 0.2, 0.2),
                'accent': (0.8, 0.3, 0.3),
                'model': 'guardian'
            }
        }

        self.colors = {
            'text': (0.95, 0.95, 0.98),
            'name': (0.95, 0.85, 0.3),
            'box_bg': (0.05, 0.05, 0.1),
            'box_border': (0.3, 0.25, 0.4)
        }

    def init_opengl(self):
        glClearColor(0.02, 0.02, 0.05, 1.0)
        glEnable(GL_DEPTH_TEST)

    def setup_3d_projection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(50, self.window_width / self.window_height, 1, 1000)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glEnable(GL_DEPTH_TEST)

        light_pos = [50.0, -100.0, 150.0, 1.0]
        light_ambient = [0.15, 0.15, 0.2, 1.0]
        light_diffuse = [0.7, 0.7, 0.9, 1.0]

    def setup_2d_projection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.window_width, 0, self.window_height)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)

    def draw_text(self, text, x, y, color=(1.0, 1.0, 1.0), font=GLUT_BITMAP_HELVETICA_18):
        glColor3f(*color)
        glRasterPos2f(x, y)
        for char in text:
            glutBitmapCharacter(font, ord(char))

    def draw_centered_text(self, text, y, color=(1.0, 1.0, 1.0), font=GLUT_BITMAP_HELVETICA_18):
        text_width = sum(glutBitmapWidth(font, ord(c)) for c in text)
        x = (self.window_width - text_width) / 2.0
        self.draw_text(text, x, y, color, font)

    def draw_viking_character(self, x, y, z, scale=1.0, color=(0.2, 0.5, 0.3)):
        glPushMatrix()
        glTranslatef(x, y, z)
        glScalef(scale, scale, scale)

        bob = 2 * math.sin(self.character_bob * 0.02)
        glTranslatef(0, 0, bob)

        glColor3f(*color)
        draw_cube(30)

        glPushMatrix()
        glTranslatef(0, 0, 35)
        glColor3f(0.9, 0.75, 0.6)
        draw_cube(25)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0, -5, 43)
        glColor3f(0.35, 0.2, 0.1)
        draw_cube(20)
        glPopMatrix()

        glPopMatrix()

    def draw_spirit_character(self, x, y, z, scale=1.0, color=(0.4, 0.2, 0.6)):
        glPushMatrix()
        glTranslatef(x, y, z)
        glScalef(scale, scale, scale)

        bob = 5 * math.sin(self.character_bob * 0.015)
        glTranslatef(0, 0, bob)

        glColor4f(color[0], color[1], color[2], 0.6)
        draw_crystal(30)

        pulse = 0.4 + 0.2 * math.sin(self.character_bob * 0.08)
        glColor4f(0.8, 0.6, 1.0, pulse)
        draw_crystal(18)

        glColor4f(1.0, 1.0, 1.0, 0.9)
        for side in [-1, 1]:
            glPushMatrix()
            glTranslatef(side * 8, 15, 20)
            draw_cube(8)
            glPopMatrix()

        glColor4f(0.7, 0.5, 0.9, 0.5)
        for i in range(6):
            angle = i * 60 + self.particle_time * 2
            radius = 40 + 10 * math.sin(self.particle_time * 0.05 + i)
            px = math.cos(math.radians(angle)) * radius
            py = math.sin(math.radians(angle)) * radius
            pz = 20 * math.sin(self.particle_time * 0.03 + i * 0.5)

            glPushMatrix()
            glTranslatef(px, py, pz)
            draw_cube(5)
            glPopMatrix()

        glPopMatrix()

    def draw_guardian_character(self, x, y, z, scale=1.0, color=(0.6, 0.2, 0.2)):
        glPushMatrix()
        glTranslatef(x, y, z)
        glScalef(scale, scale, scale)

        bob = 3 * math.sin(self.character_bob * 0.02)
        glTranslatef(0, 0, bob)

        glColor3f(*color)
        glPushMatrix()
        glScalef(1.5, 1.2, 2.0)
        draw_cube(50)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0, 0, 50)
        draw_cube(35)
        glPopMatrix()

        eye_pulse = 0.8 + 0.2 * math.sin(self.character_bob * 0.1)
        glColor3f(1.0 * eye_pulse, 0.2 * eye_pulse, 0.2 * eye_pulse)
        for side in [-1, 1]:
            glPushMatrix()
            glTranslatef(side * 10, 18, 55)
            draw_cube(10)
            glPopMatrix()

        pulse = 0.6 + 0.3 * math.sin(self.character_bob * 0.06)
        glPushMatrix()
        glTranslatef(0, 20, 25)
        glColor3f(0.8 * pulse, 0.2 * pulse, 0.9 * pulse)
        draw_crystal(12)
        glPopMatrix()

        glPopMatrix()

    def draw_3d_scene(self):
        gluLookAt(0, -200, 100, 0, 0, 30, 0, 0, 1)

        glBegin(GL_QUADS)
        glNormal3f(0, 0, 1)
        glColor3f(0.05, 0.05, 0.08)
        glVertex3f(-300, -300, 0)
        glVertex3f(300, -300, 0)
        glColor3f(0.08, 0.08, 0.12)
        glVertex3f(300, 300, 0)
        glVertex3f(-300, 300, 0)
        glEnd()

        glColor3f(0.12, 0.12, 0.18)
        glPushMatrix()
        glTranslatef(0, 50, 1)
        draw_ground(60)
        glPopMatrix()

        char_data = self.characters.get(self.character_name, self.characters['Hiccup'])

        if char_data['model'] == 'viking':
            self.draw_viking_character(0, 50, 0, 1.2, char_data['color'])
        elif char_data['model'] == 'spirit':
            self.draw_spirit_character(0, 50, 20, 1.0, char_data['color'])
        elif char_data['model'] == 'guardian':
            self.draw_guardian_character(0, 50, 0, 0.8, char_data['color'])

    def draw_dialogue_box(self):
        if not self.dialogue_active:
            return

        box_margin = 60
        box_height = 180
        box_y = 40
        box_width = self.window_width - (box_margin * 2)

        shadow_offset = 8
        glColor4f(0.0, 0.0, 0.0, 0.5)
        glBegin(GL_QUADS)
        glVertex2f(box_margin + shadow_offset, box_y - shadow_offset)
        glVertex2f(box_margin + box_width + shadow_offset, box_y - shadow_offset)
        glVertex2f(box_margin + box_width + shadow_offset, box_y + box_height - shadow_offset)
        glVertex2f(box_margin + shadow_offset, box_y + box_height - shadow_offset)
        glEnd()

        glBegin(GL_QUADS)
        glColor4f(0.02, 0.02, 0.06, 0.95)
        glVertex2f(box_margin, box_y)
        glVertex2f(box_margin + box_width, box_y)
        glColor4f(0.04, 0.04, 0.10, 0.95)
        glVertex2f(box_margin + box_width, box_y + box_height)
        glVertex2f(box_margin, box_y + box_height)
        glEnd()

        glColor4f(0.6, 0.5, 0.2, 0.9)
        glBegin(GL_QUADS)
        glVertex2f(box_margin, box_y + box_height - 3)
        glVertex2f(box_margin + box_width, box_y + box_height - 3)
        glVertex2f(box_margin + box_width, box_y + box_height)
        glVertex2f(box_margin, box_y + box_height)
        glEnd()

        glColor4f(0.5, 0.4, 0.3, 0.8)
        border_thickness = 3
        glBegin(GL_QUADS)
        glVertex2f(box_margin, box_y)
        glVertex2f(box_margin + box_width, box_y)
        glVertex2f(box_margin + box_width, box_y + border_thickness)
        glVertex2f(box_margin, box_y + border_thickness)
        glVertex2f(box_margin, box_y + box_height - border_thickness)
        glVertex2f(box_margin + box_width, box_y + box_height - border_thickness)
        glVertex2f(box_margin + box_width, box_y + box_height)
        glVertex2f(box_margin, box_y + box_height)
        glVertex2f(box_margin, box_y)
        glVertex2f(box_margin + border_thickness, box_y)
        glVertex2f(box_margin + border_thickness, box_y + box_height)
        glVertex2f(box_margin, box_y + box_height)
        glVertex2f(box_margin + box_width - border_thickness, box_y)
        glVertex2f(box_margin + box_width, box_y)
        glVertex2f(box_margin + box_width, box_y + box_height)
        glVertex2f(box_margin + box_width - border_thickness, box_y + box_height)
        glEnd()

        char_data = self.characters.get(self.character_name, {'accent': (0.5, 0.5, 0.5)})
        name_y = box_y + box_height - 45
        name_width = len(self.character_name) * 12 + 40
        name_x = box_margin + 20

        glBegin(GL_QUADS)
        glColor4f(char_data['accent'][0] * 0.6, char_data['accent'][1] * 0.6, char_data['accent'][2] * 0.6, 0.95)
        glVertex2f(name_x, name_y - 10)
        glVertex2f(name_x + name_width, name_y - 10)
        glColor4f(char_data['accent'][0] * 0.4, char_data['accent'][1] * 0.4, char_data['accent'][2] * 0.4, 0.95)
        glVertex2f(name_x + name_width, name_y + 28)
        glVertex2f(name_x, name_y + 28)
        glEnd()

        self.draw_text(self.character_name, name_x + 20, name_y, (1.0, 1.0, 1.0), GLUT_BITMAP_HELVETICA_18)

        text_x = box_margin + 30
        text_y = box_y + box_height - 80
        max_width = box_width - 60

        words = self.displayed_text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + " " + word if current_line else word
            test_width = sum(glutBitmapWidth(GLUT_BITMAP_HELVETICA_18, ord(c)) for c in test_line)

            if test_width < max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        for i, line in enumerate(lines[:4]):
            line_y = text_y - i * 28
            self.draw_text(line, text_x, line_y, (0.95, 0.95, 1.0), GLUT_BITMAP_HELVETICA_18)

        if self.text_complete:
            indicator_x = box_margin + box_width - 110
            indicator_y = box_y + 15
            blink_alpha = 0.5 + 0.5 * math.sin(self.particle_time * 0.15)

            glColor4f(0.3, 0.4, 0.5, 0.7 * blink_alpha)
            glBegin(GL_QUADS)
            glVertex2f(indicator_x - 8, indicator_y - 5)
            glVertex2f(indicator_x + 85, indicator_y - 5)
            glVertex2f(indicator_x + 85, indicator_y + 22)
            glVertex2f(indicator_x - 8, indicator_y + 22)
            glEnd()

            self.draw_text("[SPACE]", indicator_x, indicator_y, (0.95, 0.95, 1.0), GLUT_BITMAP_HELVETICA_12)

    def draw_scene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.setup_3d_projection()
        self.draw_3d_scene()

        self.setup_2d_projection()
        self.draw_dialogue_box()

        if not hasattr(self, 'integrated_mode') or not self.integrated_mode:
            glutSwapBuffers()

    def update_text_animation(self):
        if not self.dialogue_active or self.text_complete:
            return

        current_time = time.time()
        if current_time - self.last_char_time >= self.text_speed:
            if self.char_index < len(self.current_dialogue):
                self.displayed_text += self.current_dialogue[self.char_index]
                self.char_index += 1
                self.last_char_time = current_time
            else:
                self.text_complete = True

        self.scene_rotation += 0.2
        self.character_bob += 0.5
        self.particle_time += 0.5

    def show_next_line(self):
        if self.current_line < len(self.dialogue_lines):
            self.current_dialogue = self.dialogue_lines[self.current_line]
            self.displayed_text = ""
            self.char_index = 0
            self.text_complete = False
            self.last_char_time = time.time()
        else:
            self.end_dialogue()

    def advance_dialogue(self):
        if not self.dialogue_active:
            return False

        if not self.text_complete:
            self.displayed_text = self.current_dialogue
            self.text_complete = True
            return False
        else:
            self.current_line += 1
            self.show_next_line()
            return self.current_line >= len(self.dialogue_lines)

    def end_dialogue(self):
        self.dialogue_active = False
        self.current_dialogue = ""
        self.displayed_text = ""

class Game:
    def __init__(self):
        self.width = 1000
        self.height = 800

        self.STATE_MENU = 0
        self.STATE_DIALOGUE = 1
        self.STATE_PUZZLE = 2
        self.STATE_MAZE = 3
        self.STATE_COMBAT = 4
        self.STATE_STAGE_COMPLETE = 5
        self.state = self.STATE_MENU

        self.menu_selection = 0
        self.menu_options = ['START', 'EXIT']
        self.menu_rotation = 0

        self.camera_angle = 0
        self.camera_dist = 300

        self.mouse_x = self.width // 2
        self.mouse_y = self.height // 2
        self.mouse_captured = False

        self.cheat_mode = False

        self.current_stage = 1
        self.stages_complete = [False, False, False]

        self.dialogue_system = DialogueSystem()
        self.dialogue_system.integrated_mode = True
        self.dialogue_system.window_width = self.width
        self.dialogue_system.window_height = self.height

        self.stage_complete = StageCompleteScreen()
        self.stage_complete.integrated_mode = True
        self.stage_complete.window_width = self.width
        self.stage_complete.window_height = self.height

        self.dialogues = {
            'intro': {
                'character': 'Hiccup',
                'lines': [
                    "Where am I? Everything is so dark...",
                    "I can't remember anything about myself.",
                    "I need to find my memories."
                ]
            },
            'stage1_intro': {
                'character': 'Mysterious Voice',
                'lines': [
                    "Lost one, you seek what was taken from you.",
                    "Your memories lie scattered across three realms.",
                    "Solve the puzzle to reclaim your first memory."
                ]
            },
            'stage2_intro': {
                'character': 'Mysterious Voice',
                'lines': [
                    "You have recovered a fragment of your past.",
                    "But the path ahead grows darker.",
                    "Navigate the maze to find the next memory."
                ]
            },
            'stage3_intro': {
                'character': 'Memory Guardian',
                'lines': [
                    "So, you have come at last.",
                    "I am the keeper of your deepest memories.",
                    "Prove your worth in combat!"
                ]
            },
            'ending': {
                'character': 'Hiccup',
                'lines': [
                    "The Guardian... it's fading away...",
                    "Wait! I remember now! Everything is coming back!",
                    "My name is Hiccup. I'm a Viking from Berk.",
                    "I have a dragon... Toothless! My best friend!",
                    "I was exploring ancient ruins when I fell...",
                    "But I made it through. I found myself again.",
                    "Time to go home. Toothless is waiting for me!",
                    "Thank you for helping me remember who I am."
                ]
            }
        }

        self.current_dialogue = None

        self.hopping_player_pos = [0, 0, 50]
        self.hopping_player_vel = [0, 0, 0]
        self.hopping_player_on_ground = True
        self.hopping_player_current_platform = 0
        self.hopping_camera_yaw = 90
        self.hopping_camera_pitch = -10
        self.hopping_platforms = []
        self.hopping_finish_pos = [800, 0, 0]
        self.hopping_game_over = False
        self.hopping_won = False
        self.init_hopping()

        self.maze_size = 15
        self.maze = [[1] * self.maze_size for _ in range(self.maze_size)]
        self.maze_camera_pos = [90, 90, 50]
        self.maze_camera_yaw = 0
        self.maze_camera_pitch = 0
        self.maze_exit_pos = [13, 13]
        self.maze_complete = False
        self.init_maze()
        self.maze[1][1] = 0
        self.maze[1][2] = 0
        self.maze[2][1] = 0

        self.player_hp = 100
        self.player_max_hp = 100
        self.player_stamina = 100
        self.player_max_stamina = 100

        self.guardian_hp = 300
        self.guardian_max_hp = 300

        self.current_weapon = 0
        self.weapons = [
            {'name': 'SWORD', 'damage': (20, 30), 'range': 50, 'cooldown': 0.3, 'stamina': 15},
            {'name': 'GUN', 'damage': (15, 25), 'range': 200, 'cooldown': 0.5, 'stamina': 10}
        ]
        self.weapon_cooldown = 0

        self.special_move_cooldown = 0
        self.special_move_ready = True
        self.special_move_charge = 100
        self.special_move_max_charge = 100
        self.is_using_special = False
        self.special_animation = 0

        self.arena_size = 200
        self.player_pos = [-150, 0, 0]
        self.guardian_pos = [150, 0, 0]
        self.player_velocity = [0, 0, 0]
        self.guardian_velocity = [0, 0, 0]

        self.arena_pillars = [
            {'pos': [-80, -80, 0], 'size': 30},
            {'pos': [-80, 80, 0], 'size': 30},
            {'pos': [80, -80, 0], 'size': 30},
            {'pos': [80, 80, 0], 'size': 30},
            {'pos': [0, -100, 0], 'size': 25},
            {'pos': [0, 100, 0], 'size': 25},
        ]

        self.minions = []
        self.minion_spawn_cooldown = 0
        self.minion_spawn_interval = 5.0
        self.max_minions = 4

        self.is_attacking = False
        self.is_dodging = False
        self.dodge_cooldown = 0
        self.attack_animation = 0

        self.projectiles = []
        self.guardian_projectiles = []

        self.guardian_state = 'idle'
        self.guardian_attack_cooldown = 10.0
        self.guardian_charge_time = 0
        self.guardian_charge_max = 3.0
        self.guardian_attack_radius = 0
        self.guardian_attack_warning = False
        self.guardian_color = [0.6, 0.2, 0.2]

        self.combat_animation = 0
        self.guardian_animation = 0
        self.combat_camera_angle = 0
        self.combat_camera_yaw = 0
        self.combat_camera_pitch = 0
        self.combat_first_person = False
        self.hit_flash = 0
        self.screen_shake = 0

        self.combat_log = []

    def init_hopping(self):
        self.hopping_platforms = []

        self.hopping_platforms.append({
            'pos': [0, 0, 0],
            'size': [80, 80, 30],
            'color': (0.2, 0.5, 0.2),
            'moving': False,
            'vel': [0, 0],
            'range': 0,
            'start_pos': [0, 0, 0]
        })

        platform_configs = [
            {'pos': [140, -80, 0], 'speed': 55, 'range': 130},
            {'pos': [280, 90, 0], 'speed': -65, 'range': 130},
            {'pos': [420, -80, 0], 'speed': 52, 'range': 130},
            {'pos': [560, 90, 0], 'speed': -58, 'range': 140},
            {'pos': [700, -50, 0], 'speed': 55, 'range': 130},
        ]

        for i, cfg in enumerate(platform_configs):
            self.hopping_platforms.append({
                'pos': cfg['pos'].copy(),
                'start_pos': cfg['pos'].copy(),
                'size': [70, 70, 25],
                'color': (0.3 + i * 0.1, 0.3, 0.5 + i * 0.05),
                'moving': True,
                'vel': [0, cfg['speed']],
                'range': cfg['range']
            })

        self.hopping_platforms.append({
            'pos': [840, 0, 0],
            'size': [100, 100, 30],
            'color': (0.2, 0.8, 0.2),
            'moving': False,
            'vel': [0, 0],
            'range': 0,
            'start_pos': [840, 0, 0]
        })

        self.hopping_player_pos = [0, 0, 60]
        self.hopping_player_vel = [0, 0, 0]
        self.hopping_player_on_ground = True
        self.hopping_player_current_platform = 0
        self.hopping_game_over = False
        self.hopping_won = False

    def update_hopping(self, dt):
        if self.hopping_game_over or self.hopping_won:
            return

        for plat in self.hopping_platforms:
            if plat['moving']:
                plat['pos'][1] += plat['vel'][1] * dt
                if abs(plat['pos'][1] - plat['start_pos'][1]) > plat['range']:
                    plat['vel'][1] = -plat['vel'][1]

        self.hopping_player_vel[2] -= 680 * dt

        self.hopping_player_pos[0] += self.hopping_player_vel[0] * dt
        self.hopping_player_pos[1] += self.hopping_player_vel[1] * dt
        self.hopping_player_pos[2] += self.hopping_player_vel[2] * dt

        self.hopping_player_on_ground = False
        landed_platform = -1

        for i, plat in enumerate(self.hopping_platforms):
            px, py, pz = plat['pos']
            sx, sy, sz = plat['size']

            if (px - sx/2 < self.hopping_player_pos[0] < px + sx/2 and
                py - sy/2 < self.hopping_player_pos[1] < py + sy/2):

                platform_top = pz + sz
                if (self.hopping_player_pos[2] <= platform_top + 30 and
                    self.hopping_player_pos[2] > pz and
                    self.hopping_player_vel[2] <= 0):

                    self.hopping_player_pos[2] = platform_top + 25
                    self.hopping_player_vel[2] = 0
                    self.hopping_player_vel[0] *= 0.8
                    self.hopping_player_on_ground = True
                    landed_platform = i

        if landed_platform >= 0:
            self.hopping_player_current_platform = landed_platform
            plat = self.hopping_platforms[landed_platform]
            if plat['moving']:
                self.hopping_player_pos[1] += plat['vel'][1] * dt

        if self.hopping_player_pos[2] < -100:
            self.hopping_game_over = True

        if self.hopping_player_current_platform == len(self.hopping_platforms) - 1 and self.hopping_player_on_ground:
            self.hopping_won = True

    def hopping_jump(self):
        if not self.hopping_player_on_ground or self.hopping_game_over or self.hopping_won:
            return

        self.hopping_player_vel[2] = 200
        self.hopping_player_vel[0] = 180
        self.hopping_player_on_ground = False

    def hopping_move(self, direction):
        if self.hopping_game_over:
            return

        air_control = 0.5 if not self.hopping_player_on_ground else 1.0
        speed = 150 * air_control

        if direction == 'left':
            self.hopping_player_vel[1] = -speed
        elif direction == 'right':
            self.hopping_player_vel[1] = speed
        elif direction == 'up':
            if self.hopping_player_on_ground:
                self.hopping_player_vel[0] = 50
        elif direction == 'down':
            if self.hopping_player_on_ground:
                self.hopping_player_vel[0] = -50
        elif direction == 'stop':
            self.hopping_player_vel[1] *= 0

    def init_maze(self):
        for i in range(self.maze_size):
            for j in range(self.maze_size):
                self.maze[i][j] = 1

        def carve(x, y):
            self.maze[y][x] = 0
            directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
            random.shuffle(directions)

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 < nx < self.maze_size - 1 and 0 < ny < self.maze_size - 1:
                    if self.maze[ny][nx] == 1:
                        self.maze[y + dy // 2][x + dx // 2] = 0
                        carve(nx, ny)

        carve(1, 1)
        self.maze[1][1] = 0
        self.maze[13][13] = 0

    def setup_3d(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, self.width / self.height, 1, 2000)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glEnable(GL_DEPTH_TEST)

    def setup_2d(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.width, 0, self.height)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)

    def draw_text(self, text, x, y, color=(1, 1, 1)):
        glColor3f(*color)
        glRasterPos2f(x, y)
        for char in text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    def draw_centered_text(self, text, y, color=(1, 1, 1)):
        width = sum(glutBitmapWidth(GLUT_BITMAP_HELVETICA_18, ord(c)) for c in text)
        self.draw_text(text, (self.width - width) / 2, y, color)

    def draw_menu(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.setup_3d()
        gluLookAt(
            math.cos(self.camera_angle * 0.01) * self.camera_dist, math.sin(self.camera_angle * 0.01) * self.camera_dist, 150, 0, 0, 0, 0, 0, 1
            )

        glColor3f(0.05, 0.05, 0.1)
        draw_ground(500)

        for i in range(5):
            angle = i * 72 + self.camera_angle
            x = math.cos(math.radians(angle)) * 100
            y = math.sin(math.radians(angle)) * 100
            z = 50 + 20 * math.sin(self.camera_angle * 0.02 + i)

            glPushMatrix()
            glTranslatef(x, y, z)
            glRotatef(self.camera_angle * 2, 0, 0, 1)
            glColor3f(0.3 + i * 0.1, 0.2, 0.5 + i * 0.1)
            draw_crystal(15)
            glPopMatrix()

        self.setup_2d()
        self.draw_centered_text("HICCUP'S ADVENTURE", self.height - 100, (0.9, 0.8, 0.3))
        self.draw_centered_text("A Journey of Memory", self.height - 140, (0.6, 0.6, 0.8))

        for i, option in enumerate(self.menu_options):
            y = self.height // 2 - i * 50
            color = (1, 1, 1) if i == self.menu_selection else (0.5, 0.5, 0.5)
            text = f"> {option} <" if i == self.menu_selection else option
            self.draw_centered_text(text, y, color)

        self.draw_centered_text("UP/DOWN: Select  ENTER: Confirm  C: Cheat", 50, (0.5, 0.5, 0.5))

        if self.cheat_mode:
            self.draw_centered_text("[CHEAT MODE]", 80, (1, 0.3, 0.3))

    def draw_hopping(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.setup_3d()

        cam_distance = 250
        cam_height = 180
        cam_x = self.hopping_player_pos[0] - cam_distance
        cam_y = self.hopping_player_pos[1]
        cam_z = self.hopping_player_pos[2] + cam_height

        look_x = self.hopping_player_pos[0] + 150
        look_y = self.hopping_player_pos[1]
        look_z = self.hopping_player_pos[2]

        gluLookAt(cam_x, cam_y, cam_z, look_x, look_y, look_z, 0, 0, 1)

        glColor3f(0.02, 0.02, 0.05)
        glPushMatrix()
        glTranslatef(500, 0, -200)
        draw_ground(1500)
        glPopMatrix()

        for i, plat in enumerate(self.hopping_platforms):
            glPushMatrix()
            px, py, pz = plat['pos']
            sx, sy, sz = plat['size']
            glTranslatef(px, py, pz + sz/2)

            if i == self.hopping_player_current_platform:
                glColor3f(plat['color'][0] + 0.3, plat['color'][1] + 0.3, plat['color'][2])
            else:
                glColor3f(*plat['color'])

            glScalef(sx/60, sy/60, sz/60)
            draw_cube(60)
            glPopMatrix()

        glPushMatrix()
        glTranslatef(840, 0, 100 + 10 * math.sin(self.camera_angle * 0.05))
        glRotatef(self.camera_angle * 2, 0, 0, 1)
        glColor3f(0.3, 1.0, 0.3)
        draw_crystal(30)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(self.hopping_player_pos[0], self.hopping_player_pos[1], self.hopping_player_pos[2])
        glRotatef(90, 0, 0, 1)
        glColor3f(0.3, 0.5, 0.8)
        draw_character(25)
        glPopMatrix()

        self.setup_2d()
        self.draw_centered_text("HOP TO THE FINISH!", self.height - 50, (0.9, 0.8, 0.3))
        self.draw_centered_text("WASD: Move  SPACE: Jump  R: Restart  P: Skip", 50, (0.6, 0.6, 0.7))

        self.draw_text(f"Platform: {self.hopping_player_current_platform + 1}/{len(self.hopping_platforms)}", 20, self.height - 80, (0.8, 0.8, 0.9))

        if self.hopping_game_over:
            self.draw_centered_text("FELL! Press R to restart", self.height // 2, (1.0, 0.3, 0.3))

        if self.hopping_won or self.cheat_mode:
            self.draw_centered_text("STAGE COMPLETE! Press SPACE for next stage", self.height // 2, (0.3, 1.0, 0.3))

    def draw_maze(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.setup_3d()

        look_x = self.maze_camera_pos[0] + math.cos(math.radians(self.maze_camera_yaw)) * math.cos(math.radians(self.maze_camera_pitch))
        look_y = self.maze_camera_pos[1] + math.sin(math.radians(self.maze_camera_yaw)) * math.cos(math.radians(self.maze_camera_pitch))
        look_z = self.maze_camera_pos[2] + math.sin(math.radians(self.maze_camera_pitch))

        gluLookAt(
            self.maze_camera_pos[0], self.maze_camera_pos[1], self.maze_camera_pos[2],
            look_x, look_y, look_z,
            0, 0, 1
        )

        glColor3f(0.03, 0.03, 0.06)
        draw_ground(self.maze_size * 60)

        for i in range(self.maze_size):
            for j in range(self.maze_size):
                if self.maze[i][j] == 1:
                    glPushMatrix()
                    glTranslatef(j * 60, i * 60, 40)
                    glColor3f(0.2, 0.15, 0.25)
                    draw_cube(60)
                    glPopMatrix()

        glPushMatrix()
        glTranslatef(
            self.maze_exit_pos[1] * 60,
            self.maze_exit_pos[0] * 60,
            30 + 10 * math.sin(self.camera_angle * 0.05)
        )
        glRotatef(self.camera_angle * 2, 0, 0, 1)
        glColor3f(0.2, 0.8, 0.2)
        draw_crystal(20)
        glPopMatrix()

        self.setup_2d()
        self.draw_centered_text("MAZE CHALLENGE", self.height - 50, (0.9, 0.8, 0.3))
        self.draw_centered_text("WASD: Move  QE: Up/Down  Mouse: Look  P: Skip", 50, (0.6, 0.6, 0.7))
        self.draw_centered_text("Find the green crystal!", 80, (0.5, 0.9,            0.5))

        grid_x = int(self.maze_camera_pos[0] // 60)
        grid_y = int(self.maze_camera_pos[1] // 60)
        if abs(grid_y - self.maze_exit_pos[0]) <= 1 and abs(grid_x - self.maze_exit_pos[1]) <= 1 or self.cheat_mode:
            self.maze_complete = True
            self.draw_centered_text("MAZE COMPLETE! Press SPACE for next stage", self.height // 2, (0.3, 0.9, 0.3))

    def draw_combat(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.setup_3d()
        shake_x = random.uniform(-self.screen_shake, self.screen_shake)
        shake_y = random.uniform(-self.screen_shake, self.screen_shake)

        if self.combat_first_person:
            angle_rad = math.radians(self.combat_camera_yaw)
            gun_dir_x = -math.sin(angle_rad)
            gun_dir_y = -math.cos(angle_rad)

            cam_x = self.player_pos[0] + shake_x
            cam_y = self.player_pos[1] + shake_y
            cam_z = self.player_pos[2] + 50

            look_x = self.player_pos[0] + 100 * gun_dir_x
            look_y = self.player_pos[1] + 100 * gun_dir_y
            look_z = self.player_pos[2]

            gluLookAt(cam_x, cam_y, cam_z, look_x, look_y, look_z, 0, 0, 1)
        else:
            cam_distance = 120
            cam_height = 60

            cam_x = self.player_pos[0] - math.cos(math.radians(self.combat_camera_yaw)) * cam_distance + shake_x
            cam_y = self.player_pos[1] - math.sin(math.radians(self.combat_camera_yaw)) * cam_distance + shake_y
            cam_z = self.player_pos[2] + cam_height

            look_x = self.player_pos[0] + math.cos(math.radians(self.combat_camera_yaw)) * 30
            look_y = self.player_pos[1] + math.sin(math.radians(self.combat_camera_yaw)) * 30
            look_z = self.player_pos[2] + 30

            gluLookAt(cam_x, cam_y, cam_z, look_x, look_y, look_z, 0, 0, 1)

        glColor3f(0.02, 0.02, 0.04)
        draw_ground(500)

        glColor3f(0.15, 0.1, 0.2)
        for i in range(8):
            angle = i * 45
            x = math.cos(math.radians(angle)) * self.arena_size
            y = math.sin(math.radians(angle)) * self.arena_size
            glPushMatrix()
            glTranslatef(x, y, 20)
            draw_cube(15)
            glPopMatrix()

        glColor3f(0.2, 0.15, 0.25)
        for pillar in self.arena_pillars:
            glPushMatrix()
            glTranslatef(pillar['pos'][0], pillar['pos'][1], pillar['size'])
            draw_cube(pillar['size'])
            glPopMatrix()

        if not self.combat_first_person:
            glPushMatrix()
            glTranslatef(self.player_pos[0], self.player_pos[1], 25)
            glRotatef(self.combat_camera_yaw - 90, 0, 0, 1)
            glColor3f(0.3, 0.5, 0.8)
            draw_character(25)
            glPopMatrix()

        angle_rad = math.radians(self.combat_camera_yaw)
        gun_dir_x = -math.sin(angle_rad)
        gun_dir_y = -math.cos(angle_rad)

        if self.current_weapon == 0:
            if not self.combat_first_person:
                glPushMatrix()
                glTranslatef(self.player_pos[0], self.player_pos[1], 25)
                glRotatef(self.combat_camera_yaw - 90, 0, 0, 1)

                glPushMatrix()
                glTranslatef(6.25, 0, 17)
                glRotatef(90, 0, 0, 1)

                glColor3f(0.8, 0.8, 0.9)
                glPushMatrix()
                glScalef(0.15, 0.1, 2.5)
                draw_cube(10)
                glPopMatrix()

                glPushMatrix()
                glTranslatef(0, 0, -15)
                glColor3f(0.4, 0.3, 0.2)
                glScalef(0.18, 0.18, 0.8)
                draw_cube(10)
                glPopMatrix()
                glPopMatrix()
                glPopMatrix()
            else:
                glPushMatrix()
                glTranslatef(25, 35, -15)
                glRotatef(45, 0, 0, 1)

                glColor3f(0.8, 0.8, 0.9)
                glPushMatrix()
                glScalef(0.15, 0.1, 2.5)
                draw_cube(10)
                glPopMatrix()

                glPushMatrix()
                glTranslatef(0, 0, -15)
                glColor3f(0.4, 0.3, 0.2)
                glScalef(0.18, 0.18, 0.8)
                draw_cube(10)
                glPopMatrix()
                glPopMatrix()
        else:
            angle_rad = math.radians(self.combat_camera_yaw)

            if not self.combat_first_person:
                aim_dir_x = math.cos(angle_rad)
                aim_dir_y = math.sin(angle_rad)

                gun_start_x = self.player_pos[0]
                gun_start_y = self.player_pos[1]
                gun_start_z = 35

                gun_end_x = gun_start_x + 50 * aim_dir_x
                gun_end_y = gun_start_y + 50 * aim_dir_y
                gun_end_z = gun_start_z

                glColor3f(0.5, 0.5, 0.5)
                gun_thickness = 3
                dx = gun_end_x - gun_start_x
                dy = gun_end_y - gun_start_y
                length = math.sqrt(dx*dx + dy*dy)
                if length > 0:
                    px = -dy / length * gun_thickness
                    py = dx / length * gun_thickness
                    glBegin(GL_QUADS)
                    glVertex3f(gun_start_x + px, gun_start_y + py, gun_start_z)
                    glVertex3f(gun_start_x - px, gun_start_y - py, gun_start_z)
                    glVertex3f(gun_end_x - px, gun_end_y - py, gun_end_z)
                    glVertex3f(gun_end_x + px, gun_end_y + py, gun_end_z)
                    glEnd()

                if self.is_attacking and self.attack_animation < 3:
                    glPushMatrix()
                    glTranslatef(gun_end_x, gun_end_y, gun_end_z)
                    glColor3f(1.0, 0.9, 0.3)
                    draw_crystal(5)
                    glPopMatrix()
            else:
                aim_dir_x = -math.sin(angle_rad)
                aim_dir_y = -math.cos(angle_rad)

                gun_base_x = self.player_pos[0]
                gun_base_y = self.player_pos[1]
                gun_base_z = self.player_pos[2] + 10

                gun_tip_x = gun_base_x + 60 * aim_dir_x
                gun_tip_y = gun_base_y + 60 * aim_dir_y
                gun_tip_z = gun_base_z

                glColor3f(0.5, 0.5, 0.5)
                gun_thickness = 6
                dx = gun_tip_x - gun_base_x
                dy = gun_tip_y - gun_base_y
                length = math.sqrt(dx*dx + dy*dy)
                if length > 0:
                    px = -dy / length * gun_thickness
                    py = dx / length * gun_thickness
                    glBegin(GL_QUADS)
                    glVertex3f(gun_base_x + px, gun_base_y + py, gun_base_z)
                    glVertex3f(gun_base_x - px, gun_base_y - py, gun_base_z)
                    glVertex3f(gun_tip_x - px, gun_tip_y - py, gun_tip_z)
                    glVertex3f(gun_tip_x + px, gun_tip_y + py, gun_tip_z)
                    glEnd()

                if self.is_attacking and self.attack_animation < 3:
                    glPushMatrix()
                    glTranslatef(gun_tip_x, gun_tip_y, gun_tip_z)
                    glColor3f(1.0, 0.9, 0.3)
                    draw_crystal(5)
                    glPopMatrix()

        if self.is_using_special:
            glPushMatrix()
            glTranslatef(self.player_pos[0], self.player_pos[1], 25)
            glRotatef(self.special_animation * 30, 0, 0, 1)
            glColor3f(0.9, 0.2, 0.9)
            glScalef(2.0 + self.special_animation * 0.1, 2.0 + self.special_animation * 0.1, 1.0)
            draw_crystal(20)
            glPopMatrix()

        for minion in self.minions:
            glPushMatrix()
            glTranslatef(minion['pos'][0], minion['pos'][1], 15)
            glColor3f(0.4, 0.1, 0.1)
            draw_character(20)

            glPushMatrix()
            glTranslatef(5, 0, 4)
            glRotatef(90, 0, 0, 1)
            glColor3f(0.7, 0.7, 0.8)
            glPushMatrix()
            glScalef(0.1, 0.08, 1.5)
            draw_cube(8)
            glPopMatrix()
            glPushMatrix()
            glTranslatef(0, 0, -8)
            glColor3f(0.3, 0.2, 0.1)
            glScalef(0.12, 0.12, 0.5)
            draw_cube(8)
            glPopMatrix()
            glPopMatrix()
            glPopMatrix()

        glPushMatrix()
        glTranslatef(self.guardian_pos[0], self.guardian_pos[1], 35)

        glColor3f(*self.guardian_color)

        draw_character(50)

        pulse = 0.7 + 0.3 * math.sin(self.guardian_animation * 0.02)
        glPushMatrix()
        glTranslatef(0, 0, 15)
        glColor3f(0.9 * pulse, 0.2, 0.9 * pulse)
        draw_crystal(15)
        glPopMatrix()
        glPopMatrix()

        for proj in self.projectiles:
            glPushMatrix()
            glTranslatef(proj['pos'][0], proj['pos'][1], proj['pos'][2])
            if proj.get('type') == 'bullet':
                glColor3f(1.0, 1.0, 0.3)
                draw_cube(6)

                glPushMatrix()
                glColor3f(1.0, 0.8, 0.0)
                glScalef(1.8, 1.8, 1.8)
                draw_cube(6)
                glPopMatrix()

                glColor3f(1.0, 0.7, 0.0)
                trail_thickness = 2
                trail_dx = -proj['vel'][0] * 0.5
                trail_dy = -proj['vel'][1] * 0.5
                trail_length = math.sqrt(trail_dx*trail_dx + trail_dy*trail_dy)
                if trail_length > 0:
                    px = -trail_dy / trail_length * trail_thickness
                    py = trail_dx / trail_length * trail_thickness
                    glBegin(GL_QUADS)
                    glVertex3f(px, py, 0)
                    glVertex3f(-px, -py, 0)
                    glVertex3f(trail_dx - px, trail_dy - py, 0)
                    glVertex3f(trail_dx + px, trail_dy + py, 0)
                    glEnd()
            else:
                glColor3f(1.0, 0.9, 0.2)
                draw_cube(8)
            glPopMatrix()

        for proj in self.guardian_projectiles:
            glPushMatrix()
            glTranslatef(proj['pos'][0], proj['pos'][1], proj['pos'][2])
            glColor3f(0.9, 0.2, 0.9)
            draw_crystal(8)
            glPopMatrix()

        if self.guardian_attack_warning and self.guardian_attack_radius > 0:
            glPushMatrix()
            glTranslatef(self.guardian_pos[0], self.guardian_pos[1], 1)

            charge_percent = self.guardian_charge_time / self.guardian_charge_max
            glColor3f(1.0, 0.2 + 0.3 * math.sin(self.guardian_animation * 0.2), 0.0)

            ring_thickness = 3
            inner_radius = self.guardian_attack_radius - ring_thickness
            outer_radius = self.guardian_attack_radius
            glBegin(GL_QUADS)
            for i in range(32):
                angle1 = i * (360 / 32)
                angle2 = (i + 1) * (360 / 32)
                x1_inner = math.cos(math.radians(angle1)) * inner_radius
                y1_inner = math.sin(math.radians(angle1)) * inner_radius
                x1_outer = math.cos(math.radians(angle1)) * outer_radius
                y1_outer = math.sin(math.radians(angle1)) * outer_radius
                x2_inner = math.cos(math.radians(angle2)) * inner_radius
                y2_inner = math.sin(math.radians(angle2)) * inner_radius
                x2_outer = math.cos(math.radians(angle2)) * outer_radius
                y2_outer = math.sin(math.radians(angle2)) * outer_radius
                glVertex3f(x1_inner, y1_inner, 0)
                glVertex3f(x1_outer, y1_outer, 0)
                glVertex3f(x2_outer, y2_outer, 0)
                glVertex3f(x2_inner, y2_inner, 0)
            glEnd()

            for i in range(8):
                angle = i * 45 + self.guardian_animation * 2
                x = math.cos(math.radians(angle)) * self.guardian_attack_radius * 0.8
                y = math.sin(math.radians(angle)) * self.guardian_attack_radius * 0.8
                glPushMatrix()
                glTranslatef(x, y, 5)
                glColor3f(1.0, 0.0, 0.0)
                draw_cube(3)
                glPopMatrix()

            glPopMatrix()

        self.setup_2d()

        self.draw_centered_text("GUARDIAN BATTLE - REAL-TIME COMBAT", self.height - 30, (0.9, 0.3, 0.3))

        hud_x = 20
        hud_y = self.height - 80

        self.draw_text(f"HP: {self.player_hp}/{self.player_max_hp}", hud_x, hud_y, (0.3, 0.9, 0.3))
        bar_width = 200
        hp_fill = int(bar_width * (self.player_hp / self.player_max_hp))
        glColor3f(0.3, 0.7, 0.3)
        glBegin(GL_QUADS)
        glVertex2f(hud_x, hud_y - 20)
        glVertex2f(hud_x + hp_fill, hud_y - 20)
        glVertex2f(hud_x + hp_fill, hud_y - 10)
        glVertex2f(hud_x, hud_y - 10)
        glEnd()

        self.draw_text(f"Stamina: {int(self.player_stamina)}/{self.player_max_stamina}", hud_x, hud_y - 40, (0.9, 0.7, 0.2))
        stam_fill = int(bar_width * (self.player_stamina / self.player_max_stamina))
        glColor3f(0.8, 0.6, 0.1)
        glBegin(GL_QUADS)
        glVertex2f(hud_x, hud_y - 60)
        glVertex2f(hud_x + stam_fill, hud_y - 60)
        glVertex2f(hud_x + stam_fill, hud_y - 50)
        glVertex2f(hud_x, hud_y - 50)
        glEnd()

        weapon = self.weapons[self.current_weapon]
        weapon_color = (0.9, 0.9, 0.3) if self.weapon_cooldown <= 0 else (0.5, 0.5, 0.5)
        self.draw_text(f"Weapon: {weapon['name']} [TAB to switch]", hud_x, hud_y - 80, weapon_color)

        special_color = (0.9, 0.3, 0.9) if self.special_move_ready else (0.4, 0.2, 0.4)
        self.draw_text(f"Special: {'READY [Q]' if self.special_move_ready else 'CHARGING...'}", hud_x, hud_y - 110, special_color)
        special_fill = int(bar_width * (self.special_move_charge / self.special_move_max_charge))
        glColor3f(0.8, 0.2, 0.8)
        glBegin(GL_QUADS)
        glVertex2f(hud_x, hud_y - 130)
        glVertex2f(hud_x + special_fill, hud_y - 130)
        glVertex2f(hud_x + special_fill, hud_y - 120)
        glVertex2f(hud_x, hud_y - 120)
        glEnd()

        hud_x = self.width - 220
        self.draw_text(f"Guardian HP: {self.guardian_hp}/{self.guardian_max_hp}", hud_x, hud_y, (0.9, 0.3, 0.3))
        guardian_hp_fill = int(bar_width * (self.guardian_hp / self.guardian_max_hp))
        glColor3f(0.9, 0.3, 0.3)
        glBegin(GL_QUADS)
        glVertex2f(hud_x, hud_y - 20)
        glVertex2f(hud_x + guardian_hp_fill, hud_y - 20)
        glVertex2f(hud_x + guardian_hp_fill, hud_y - 10)
        glVertex2f(hud_x, hud_y - 10)
        glEnd()

        self.draw_text(f"State: {self.guardian_state.upper()}", hud_x, hud_y - 40, (0.7, 0.5, 0.8))

        camera_mode = "First Person" if self.combat_first_person else "Third Person"
        self.draw_centered_text(f"WASD: Move  SPACE/Click: Attack V: Toggle Camera ({camera_mode})  TAB: Switch  Q: Special  P: Skip", 60, (0.6, 0.6, 0.7))

        log_y = 140
        for i, msg in enumerate(self.combat_log[-2:]):
            self.draw_centered_text(msg, log_y - i * 25, (0.9, 0.9, 0.3))

        if self.guardian_hp <= 0:
            self.draw_centered_text("VICTORY! Press ENTER to continue", self.height // 2, (0.3, 0.9, 0.3))
        elif self.player_hp <= 0:
            self.draw_centered_text("DEFEAT! Press ENTER to retry", self.height // 2, (0.9, 0.3, 0.3))

    def display(self):
        if self.state == self.STATE_MENU:
            self.draw_menu()
        elif self.state == self.STATE_DIALOGUE:
            self.dialogue_system.draw_scene()
        elif self.state == self.STATE_PUZZLE:
            self.draw_hopping()
        elif self.state == self.STATE_MAZE:
            self.draw_maze()
        elif self.state == self.STATE_COMBAT:
            self.draw_combat()
        elif self.state == self.STATE_STAGE_COMPLETE:
            self.stage_complete.display()

        glutSwapBuffers()

    def check_puzzle_solved(self):
        if self.cheat_mode:
            return True

        dist_to_goal = math.sqrt(
            (self.puzzle_camera_pos[0] - self.puzzle_goal_pos[0])**2 +
            (self.puzzle_camera_pos[1] - self.puzzle_goal_pos[1])**2 +
            (self.puzzle_camera_pos[2] - self.puzzle_goal_pos[2])**2
        )

        if dist_to_goal < 100:
            return True

        return False

    def start_dialogue(self, dialogue_key):
        if dialogue_key in self.dialogues:
            dialogue = self.dialogues[dialogue_key]
            self.dialogue_system.character_name = dialogue['character']
            self.dialogue_system.dialogue_lines = dialogue['lines']
            self.dialogue_system.current_line = 0
            self.dialogue_system.dialogue_active = True
            self.dialogue_system.show_next_line()
            self.current_dialogue = dialogue_key
            self.state = self.STATE_DIALOGUE

    def start_stage(self, stage_num):
        self.current_stage = stage_num

        if stage_num == 1:
            self.state = self.STATE_PUZZLE
            self.mouse_captured = True
            glutSetCursor(GLUT_CURSOR_NONE)
        elif stage_num == 2:
            self.state = self.STATE_MAZE
            self.mouse_captured = True
            glutSetCursor(GLUT_CURSOR_NONE)
        elif stage_num == 3:
            self.state = self.STATE_COMBAT
            self.player_hp = self.player_max_hp
            self.guardian_hp = self.guardian_max_hp
            self.mouse_captured = True
            glutSetCursor(GLUT_CURSOR_NONE)

    def complete_stage(self, stage_num):
        self.stages_complete[stage_num - 1] = True
        self.stage_complete.start_completion(stage_num, auto_advance=False)
        self.state = self.STATE_STAGE_COMPLETE
        self.screen_shake = 0
        self.hit_flash = 0

    def check_block_collision(self, new_pos, exclude_index=None):
        collision_radius = 50
        for i, block in enumerate(self.puzzle_blocks):
            if i == exclude_index:
                continue
            dist = math.sqrt(
                (new_pos[0] - block['pos'][0])**2 +
                (new_pos[1] - block['pos'][1])**2
            )
            if dist < collision_radius * 2:
                return True
        return False

    def move_selected_block(self, direction):
        if self.puzzle_selected is None:
            return

        block = self.puzzle_blocks[self.puzzle_selected]

        if not block['movable']:
            print("Can't move this block - it's fixed!")
            return

        move_dist = 60

        new_pos = block['pos'].copy()
        if direction == 'i':
            new_pos[1] += move_dist
        elif direction == 'k':
            new_pos[1] -= move_dist
        elif direction == 'j':
            new_pos[0] -= move_dist
        elif direction == 'l':
            new_pos[0] += move_dist
        elif direction == 'u':
            new_pos[2] += move_dist
        elif direction == 'o':
            new_pos[2] = max(0, new_pos[2] - move_dist)

        if direction in ['i', 'k', 'j', 'l']:
            if not self.check_block_collision(new_pos, self.puzzle_selected):
                block['pos'] = new_pos
                self.puzzle_moves += 1
            else:
                print("Can't move block - collision detected!")
        else:
            block['pos'] = new_pos
            self.puzzle_moves += 1

        self.puzzle_solved = self.check_puzzle_solved()

    def check_puzzle_camera_collision(self, new_x, new_y, new_z):
        camera_radius = 20

        for block in self.puzzle_blocks:
            block_half_size = block.get('size', 60) / 2

            dist_xy = math.sqrt(
                (new_x - block['pos'][0])**2 +
                (new_y - block['pos'][1])**2
            )

            block_bottom = block['pos'][2]
            block_top = block['pos'][2] + block.get('size', 60)

            if block_bottom - 20 <= new_z <= block_top + 20:
                if dist_xy < (camera_radius + block_half_size):
                    return True
        return False

    def move_puzzle_camera(self, direction):
        speed = 20
        forward_x = math.cos(math.radians(self.puzzle_camera_yaw))
        forward_y = math.sin(math.radians(self.puzzle_camera_yaw))
        right_x = math.cos(math.radians(self.puzzle_camera_yaw + 90))
        right_y = math.sin(math.radians(self.puzzle_camera_yaw + 90))

        new_x, new_y, new_z = self.puzzle_camera_pos[0], self.puzzle_camera_pos[1], self.puzzle_camera_pos[2]

        if direction == 'w':
            new_x += forward_x * speed
            new_y += forward_y * speed
        elif direction == 's':
            new_x -= forward_x * speed
            new_y -= forward_y * speed
        elif direction == 'a':
            new_x -= right_x * speed
            new_y -= right_y * speed
        elif direction == 'd':
            new_x += right_x * speed
            new_y += right_y * speed
        elif direction == 'q':
            new_z += speed
            self.puzzle_camera_pos[2] = new_z
            return
        elif direction == 'e':
            new_z = max(10, new_z - speed)
            self.puzzle_camera_pos[2] = new_z
            return

        if not self.check_puzzle_camera_collision(new_x, new_y, new_z):
            self.puzzle_camera_pos[0] = new_x
            self.puzzle_camera_pos[1] = new_y

    def check_maze_collision(self, x, y):

        collision_margin = 35

        for i in range(self.maze_size):
            for j in range(self.maze_size):
                if self.maze[i][j] == 1:
                    block_x = j * 60
                    block_y = i * 60

                    dist_x = abs(x - block_x)
                    dist_y = abs(y - block_y)

                    if dist_x < collision_margin and dist_y < collision_margin:
                        return True

        return False

    def move_maze_camera(self, direction):
        speed = 20
        yaw_rad = math.radians(self.maze_camera_yaw)

        forward_x = math.cos(yaw_rad)
        forward_y = math.sin(yaw_rad)

        right_x = math.sin(yaw_rad)
        right_y = -math.cos(yaw_rad)

        new_x, new_y = self.maze_camera_pos[0], self.maze_camera_pos[1]

        if direction == 'w':
            new_x += forward_x * speed
            new_y += forward_y * speed
        elif direction == 's':
            new_x -= forward_x * speed
            new_y -= forward_y * speed
        elif direction == 'a':
            new_x -= right_x * speed
            new_y -= right_y * speed
        elif direction == 'd':
            new_x += right_x * speed
            new_y += right_y * speed
        elif direction == 'q':
            self.maze_camera_pos[2] += speed
            return
        elif direction == 'e':
            self.maze_camera_pos[2] = max(10, self.maze_camera_pos[2] - speed)
            return

        if not self.check_maze_collision(new_x, new_y):
            self.maze_camera_pos[0] = new_x
            self.maze_camera_pos[1] = new_y

    def player_attack(self):
        if self.weapon_cooldown > 0 or self.is_dodging:
            return

        weapon = self.weapons[self.current_weapon]

        if self.player_stamina < weapon['stamina']:
            self.combat_log.append("Not enough stamina!")
            return

        self.player_stamina -= weapon['stamina']
        self.weapon_cooldown = weapon['cooldown']
        self.is_attacking = True
        self.attack_animation = 0

        dist = math.sqrt(
            (self.player_pos[0] - self.guardian_pos[0])**2 +
            (self.player_pos[1] - self.guardian_pos[1])**2
        )

        if weapon['name'] == 'SWORD':
            hit_something = False

            for minion in self.minions[:]:
                minion_dist = math.sqrt(
                    (self.player_pos[0] - minion['pos'][0])**2 +
                    (self.player_pos[1] - minion['pos'][1])**2
                )
                if minion_dist < weapon['range']:
                    damage = random.randint(*weapon['damage'])
                    minion['hp'] -= damage
                    self.hit_flash = 5
                    self.screen_shake = 3
                    self.combat_log.append(f"Sword hit minion! {damage} damage!")
                    hit_something = True

            if dist < weapon['range']:
                damage = random.randint(*weapon['damage'])
                self.guardian_hp -= damage
                self.hit_flash = 10
                self.screen_shake = 5
                self.combat_log.append(f"Sword hit Guardian! {damage} damage!")
                hit_something = True

            if not hit_something:
                self.combat_log.append("Sword missed!")

        elif weapon['name'] == 'GUN':
            angle_rad = math.radians(self.combat_camera_yaw)

            if not self.combat_first_person:
                direction_x = math.cos(angle_rad)
                direction_y = math.sin(angle_rad)
            else:
                direction_x = -math.sin(angle_rad)
                direction_y = -math.cos(angle_rad)

            spawn_x = self.player_pos[0]
            spawn_y = self.player_pos[1]
            spawn_z = 30

            self.projectiles.append({
                'pos': [spawn_x, spawn_y, spawn_z],
                'vel': [direction_x * 25, direction_y * 25, 0],
                'damage': random.randint(*weapon['damage']),
                'type': 'bullet'
            })

            self.screen_shake = 2
            self.combat_log.append("Gun fired!")

    def player_dodge(self):
        if self.dodge_cooldown > 0 or self.is_dodging:
            return

        if self.player_stamina < 20:
            self.combat_log.append("Not enough stamina to dodge!")
            return

        self.player_stamina -= 20
        self.is_dodging = True
        self.dodge_cooldown = 1.0
        self.attack_animation = 0

    def move_player(self, direction):
        speed = 2.0

        yaw_rad = math.radians(self.combat_camera_yaw)

        if self.combat_first_person:
            forward_x = -math.sin(yaw_rad)
            forward_y = -math.cos(yaw_rad)
            right_x = math.cos(yaw_rad)
            right_y = -math.sin(yaw_rad)
        else:
            forward_x = math.cos(yaw_rad)
            forward_y = math.sin(yaw_rad)
            right_x = math.sin(yaw_rad)
            right_y = -math.cos(yaw_rad)

        if direction == 'w':
            self.player_velocity[0] = forward_x * speed
            self.player_velocity[1] = forward_y * speed
        elif direction == 's':
            self.player_velocity[0] = -forward_x * speed
            self.player_velocity[1] = -forward_y * speed
        elif direction == 'a':
            self.player_velocity[0] = -right_x * speed
            self.player_velocity[1] = -right_y * speed
        elif direction == 'd':
            self.player_velocity[0] = right_x * speed
            self.player_velocity[1] = right_y * speed

    def player_special_move(self):
        if not self.special_move_ready or self.special_move_charge < self.special_move_max_charge:
            self.combat_log.append("Special move not ready!")
            return

        self.special_move_charge = 0
        self.special_move_ready = False
        self.is_using_special = True
        self.special_animation = 0
        self.screen_shake = 15

        dist = math.sqrt(
            (self.player_pos[0] - self.guardian_pos[0])**2 +
            (self.player_pos[1] - self.guardian_pos[1])**2
        )

        if dist < 150:
            damage = random.randint(40, 60)
            self.guardian_hp -= damage
            self.hit_flash = 20
            self.combat_log.append(f"SPECIAL MOVE! Devastating blow! {damage} damage!")
        else:
            self.combat_log.append("Special move missed - too far!")

        self.combat_log.append("Special move used! Recharging...")

    def update_combat(self, dt):
        if self.guardian_hp <= 0 or self.player_hp <= 0:
            return

        if self.weapon_cooldown > 0:
            self.weapon_cooldown -= dt
        if self.dodge_cooldown > 0:
            self.dodge_cooldown -= dt
        if self.special_move_cooldown > 0:
            self.special_move_cooldown -= dt

        if self.special_move_charge < self.special_move_max_charge:
            self.special_move_charge += 0.5
            if self.special_move_charge >= self.special_move_max_charge:
                self.special_move_charge = self.special_move_max_charge
                self.special_move_ready = True

        if self.is_using_special:
            self.special_animation += 1
            if self.special_animation > 30:
                self.is_using_special = False

        if self.is_attacking:
            self.attack_animation += 1
            if self.attack_animation > 15:
                self.is_attacking = False

        if self.is_dodging:
            self.attack_animation += 1
            if self.attack_animation > 20:
                self.is_dodging = False

        self.player_pos[0] += self.player_velocity[0]
        self.player_pos[1] += self.player_velocity[1]

        self.player_pos[0] = max(-self.arena_size, min(self.arena_size, self.player_pos[0]))
        self.player_pos[1] = max(-self.arena_size, min(self.arena_size, self.player_pos[1]))

        self.player_velocity[0] *= 0.8
        self.player_velocity[1] *= 0.8

        self.player_stamina = min(self.player_max_stamina, self.player_stamina + 0.3)

        self.minion_spawn_cooldown -= dt
        if self.minion_spawn_cooldown <= 0 and len(self.minions) < self.max_minions:
            self.spawn_minion()
            self.minion_spawn_cooldown = self.minion_spawn_interval

        self.update_minions(dt)

        for proj in self.projectiles[:]:
            proj['pos'][0] += proj['vel'][0]
            proj['pos'][1] += proj['vel'][1]

            dist = math.sqrt(
                (proj['pos'][0] - self.guardian_pos[0])**2 +
                (proj['pos'][1] - self.guardian_pos[1])**2
            )
            if dist < 30:
                self.guardian_hp -= proj['damage']
                self.hit_flash = 10
                self.screen_shake = 5
                self.combat_log.append(f"Gun hit Guardian! {proj['damage']} damage!")
                self.projectiles.remove(proj)
                continue

            for minion in self.minions[:]:
                minion_dist = math.sqrt(
                    (proj['pos'][0] - minion['pos'][0])**2 +
                    (proj['pos'][1] - minion['pos'][1])**2
                )
                if minion_dist < 25:
                    minion['hp'] -= proj['damage']
                    self.combat_log.append(f"Gun hit minion! {proj['damage']} damage!")
                    if proj in self.projectiles:
                        self.projectiles.remove(proj)
                    break

            if abs(proj['pos'][0]) > 300 or abs(proj['pos'][1]) > 300:
                if proj in self.projectiles:
                    self.projectiles.remove(proj)

        for proj in self.guardian_projectiles[:]:
            proj['pos'][0] += proj['vel'][0]
            proj['pos'][1] += proj['vel'][1]

            if 'lifetime' in proj:
                proj['lifetime'] -= dt
                if proj['lifetime'] <= 0:
                    self.guardian_projectiles.remove(proj)
                    continue

            if proj.get('damage', 0) > 0 and not self.is_dodging:
                dist = math.sqrt(
                    (proj['pos'][0] - self.player_pos[0])**2 +
                    (proj['pos'][1] - self.player_pos[1])**2
                )
                if dist < 25:
                    self.player_hp -= proj['damage']
                    self.player_hp = max(0, self.player_hp)
                    self.hit_flash = 10
                    self.combat_log.append(f"Guardian hit you! {proj['damage']} damage!")
                    self.guardian_projectiles.remove(proj)
                    continue

            if abs(proj['pos'][0]) > 200 or abs(proj['pos'][1]) > 200:
                self.guardian_projectiles.remove(proj)

        self.update_guardian_ai(dt)

        if self.cheat_mode:
            self.player_hp = self.player_max_hp
            self.guardian_hp = 0

    def spawn_minion(self):
        angle = random.uniform(0, 360)
        distance = random.uniform(40, 60)
        spawn_x = self.guardian_pos[0] + math.cos(math.radians(angle)) * distance
        spawn_y = self.guardian_pos[1] + math.sin(math.radians(angle)) * distance

        self.minions.append({
            'pos': [spawn_x, spawn_y],
            'hp': 30,
            'max_hp': 30,
            'speed': 3.0,
            'damage': 10,
            'attack_cooldown': 0
        })
        self.combat_log.append("Guardian spawned a minion!")

    def update_minions(self, dt):
        for minion in self.minions[:]:
            dist = math.sqrt(
                (self.player_pos[0] - minion['pos'][0])**2 +
                (self.player_pos[1] - minion['pos'][1])**2
            )

            if dist > 30:
                direction_x = (self.player_pos[0] - minion['pos'][0]) / dist
                direction_y = (self.player_pos[1] - minion['pos'][1]) / dist
                minion['pos'][0] += direction_x * minion['speed']
                minion['pos'][1] += direction_y * minion['speed']
            else:
                minion['attack_cooldown'] -= dt
                if minion['attack_cooldown'] <= 0 and not self.is_dodging:
                    self.player_hp -= minion['damage']
                    self.player_hp = max(0, self.player_hp)
                    self.hit_flash = 5
                    self.combat_log.append(f"Minion hit you! {minion['damage']} damage!")
                    minion['attack_cooldown'] = 1.5

            if minion['hp'] <= 0:
                self.minions.remove(minion)
                self.combat_log.append("Minion defeated!")

    def update_guardian_ai(self, dt):
        if self.guardian_hp <= 0:
            self.guardian_state = 'defeated'
            return

        dist = math.sqrt(
            (self.player_pos[0] - self.guardian_pos[0])**2 +
            (self.player_pos[1] - self.guardian_pos[1])**2
        )

        if self.guardian_attack_cooldown > 0:
            self.guardian_attack_cooldown -= dt

        if self.guardian_state == 'charging':
            self.guardian_charge_time += dt

            charge_percent = min(1.0, self.guardian_charge_time / self.guardian_charge_max)
            self.guardian_color = [
                0.6 + 0.4 * charge_percent,
                0.2 - 0.1 * charge_percent,
                0.2 - 0.1 * charge_percent
            ]

            self.guardian_attack_radius = 80 * charge_percent
            self.guardian_attack_warning = True

            if self.guardian_charge_time >= self.guardian_charge_max:
                self.execute_splash_attack()
                self.guardian_state = 'idle'
                self.guardian_charge_time = 0
                self.guardian_attack_cooldown = 10.0
                self.guardian_attack_warning = False
                self.guardian_attack_radius = 0
                self.guardian_color = [0.6, 0.2, 0.2]

            return

        hp_percent = self.guardian_hp / self.guardian_max_hp

        if self.guardian_attack_cooldown <= 0:
            if dist < 150:
                self.guardian_state = 'charging'
                self.guardian_charge_time = 0
                self.combat_log.append("Guardian is charging an attack!")
                return

        if dist > 120:
            self.guardian_state = 'chase'
        elif dist < 60:
            self.guardian_state = 'retreat'
        else:
            self.guardian_state = 'idle'

        if self.guardian_state == 'chase':
            direction = [
                (self.player_pos[0] - self.guardian_pos[0]) / dist,
                (self.player_pos[1] - self.guardian_pos[1]) / dist
            ]
            self.guardian_pos[0] += direction[0] * 0.8
            self.guardian_pos[1] += direction[1] * 0.8

        elif self.guardian_state == 'retreat':
            direction = [
                (self.player_pos[0] - self.guardian_pos[0]) / dist,
                (self.player_pos[1] - self.guardian_pos[1]) / dist
            ]
            self.guardian_pos[0] -= direction[0] * 1.0
            self.guardian_pos[1] -= direction[1] * 1.0

        self.guardian_pos[0] = max(-self.arena_size, min(self.arena_size, self.guardian_pos[0]))
        self.guardian_pos[1] = max(-self.arena_size, min(self.arena_size, self.guardian_pos[1]))

    def execute_splash_attack(self):
        dist = math.sqrt(
            (self.player_pos[0] - self.guardian_pos[0])**2 +
            (self.player_pos[1] - self.guardian_pos[1])**2
        )

        if dist < 80 and not self.is_dodging:
            damage = random.randint(25, 40)
            self.player_hp -= damage
            self.player_hp = max(0, self.player_hp)
            self.hit_flash = 15
            self.screen_shake = 10
            self.combat_log.append(f"SPLASH ATTACK! {damage} damage!")
        elif dist < 80 and self.is_dodging:
            self.combat_log.append("Dodged the splash attack!")
        else:
            self.combat_log.append("Guardian's attack missed!")

    def guardian_special_attack(self):
        self.combat_log.append("GUARDIAN SPECIAL ATTACK!")
        self.screen_shake = 10
        self.guardian_color = (0.9, 0.1, 0.9)

        for i in range(12):
            angle = i * 30
            direction = [
                math.cos(math.radians(angle)),
                math.sin(math.radians(angle))
            ]
            self.guardian_projectiles.append({
                'pos': [self.guardian_pos[0], self.guardian_pos[1], 35],
                'vel': [direction[0] * 10, direction[1] * 10, 0],
                'damage': random.randint(15, 25)
            })

        def reset_color():
            self.guardian_color = (0.6, 0.2, 0.2)

        arena_size = 100
        self.guardian_pos[0] = max(-arena_size, min(arena_size, self.guardian_pos[0]))
        self.guardian_pos[1] = max(-arena_size, min(arena_size, self.guardian_pos[1]))

    def keyboard(self, key, x, y):
        if key == b'\x1b':
            if self.state != self.STATE_MENU:
                self.state = self.STATE_MENU
                self.mouse_captured = False
                glutSetCursor(GLUT_CURSOR_INHERIT)
            else:
                glutLeaveMainLoop()

        elif key == b'c' or key == b'C':
            self.cheat_mode = not self.cheat_mode
            print(f"Cheat mode: {'ON' if self.cheat_mode else 'OFF'}")

        elif self.state == self.STATE_MENU:
            if key == b'\r' or key == b' ':
                if self.menu_selection == 0:
                    self.start_dialogue('intro')
                else:
                    glutLeaveMainLoop()

        elif self.state == self.STATE_DIALOGUE:
            if key == b' ':
                finished = self.dialogue_system.advance_dialogue()
                if finished:
                    if self.current_dialogue == 'intro':
                        self.start_dialogue('stage1_intro')
                    elif self.current_dialogue == 'stage1_intro':
                        self.start_stage(1)
                    elif self.current_dialogue == 'stage2_intro':
                        self.start_stage(2)
                    elif self.current_dialogue == 'stage3_intro':
                        self.start_stage(3)
                    elif self.current_dialogue == 'ending':
                        self.state = self.STATE_MENU
                        self.mouse_captured = False
                        glutSetCursor(GLUT_CURSOR_INHERIT)

        elif self.state == self.STATE_STAGE_COMPLETE:
            self.stage_complete.end_completion()
            if self.current_stage == 1:
                self.start_dialogue('stage2_intro')
            elif self.current_stage == 2:
                self.start_dialogue('stage3_intro')
            elif self.current_stage == 3:
                self.start_dialogue('ending')

        elif self.state == self.STATE_PUZZLE:
            if key == b' ':
                if self.hopping_won:
                    self.complete_stage(1)
                    self.mouse_captured = False
                    glutSetCursor(GLUT_CURSOR_INHERIT)
                else:
                    self.hopping_jump()
            elif key == b'w' or key == b'W':
                self.hopping_move('up')
            elif key == b's' or key == b'S':
                self.hopping_move('down')
            elif key == b'a' or key == b'A':
                self.hopping_move('right')
            elif key == b'd' or key == b'D':
                self.hopping_move('left')
            elif key == b'r' or key == b'R':
                self.init_hopping()
            elif key == b'p' or key == b'P':
                self.hopping_won = True

        elif self.state == self.STATE_MAZE:
            if key in b'wasdqeWASDQE':
                self.move_maze_camera(chr(key[0]).lower())
            elif key == b'p' or key == b'P':
                self.complete_stage(2)
                self.mouse_captured = False
                glutSetCursor(GLUT_CURSOR_INHERIT)
            elif key == b' ' and (self.maze_complete or self.cheat_mode):
                self.complete_stage(2)
                self.mouse_captured = False
                glutSetCursor(GLUT_CURSOR_INHERIT)

        elif self.state == self.STATE_COMBAT:
            if key == b' ':
                if self.guardian_hp <= 0:
                    print("Victory! Stage 3 complete!")
                    self.complete_stage(3)
                    self.mouse_captured = False
                    glutSetCursor(GLUT_CURSOR_INHERIT)
                elif self.player_hp <= 0:
                    print("Retrying combat...")
                    self.player_hp = self.player_max_hp
                    self.player_stamina = self.player_max_stamina
                    self.guardian_hp = self.guardian_max_hp
                    self.player_pos = [-80, 0, 0]
                    self.guardian_pos = [80, 0, 0]
                    self.projectiles = []
                    self.guardian_projectiles = []
                    self.combat_log = []
                else:
                    self.player_attack()
            elif key in b'wasdWASD':
                self.move_player(chr(key[0]).lower())
            elif key in b'vV':
                self.combat_first_person = not self.combat_first_person
                mode = "First Person" if self.combat_first_person else "Third Person"
                self.combat_log.append(f"Camera: {mode}")
                print(f"Camera Mode: {mode}")
            elif key in b'qQ':
                self.player_special_move()
            elif key in b'rR':
                self.player_dodge()
            elif key in b'pP':
                print("Skipping combat...")
                self.guardian_hp = 0
                self.combat_log.append("Combat skipped!")
            elif key == b'\t':
                self.current_weapon = (self.current_weapon + 1) % len(self.weapons)
                self.combat_log.append(f"Switched to {self.weapons[self.current_weapon]['name']}")
            elif key == b'\r':
                if self.guardian_hp <= 0 or self.player_hp <= 0:
                    if self.guardian_hp <= 0:
                        print("Victory! Stage 3 complete!")
                        self.complete_stage(3)
                        self.mouse_captured = False
                        glutSetCursor(GLUT_CURSOR_INHERIT)
                    else:
                        print("Retrying combat...")
                        self.player_hp = self.player_max_hp
                        self.player_stamina = self.player_max_stamina
                        self.guardian_hp = self.guardian_max_hp
                        self.player_pos = [-80, 0, 0]
                        self.guardian_pos = [80, 0, 0]
                        self.projectiles = []
                        self.guardian_projectiles = []
                        self.combat_log = []
                        self.special_move_charge = self.special_move_max_charge
                        self.special_move_ready = True

        glutPostRedisplay()

    def special_keyboard(self, key, x, y):
        if self.state == self.STATE_MENU:
            if key == GLUT_KEY_UP:
                self.menu_selection = (self.menu_selection - 1) % len(self.menu_options)
            elif key == GLUT_KEY_DOWN:
                self.menu_selection = (self.menu_selection + 1) % len(self.menu_options)

        elif self.state == self.STATE_COMBAT:
            pass

        glutPostRedisplay()

    def keyboard_up(self, key, x, y):
        if self.state == self.STATE_COMBAT:
            if key in b'wasdWASD':
                direction = chr(key[0]).lower()
                if direction == 'w' or direction == 's':
                    self.player_velocity[1] = 0
                elif direction == 'a' or direction == 'd':
                    self.player_velocity[0] = 0
        elif self.state == self.STATE_PUZZLE:
            if key in b'wasdWASD':
                self.hopping_move('stop')

    def mouse(self, button, state, x, y):
        if self.state == self.STATE_PUZZLE and button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            pass

        elif self.state == self.STATE_COMBAT and button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            if self.current_weapon == 1:
                self.player_attack()
            else:
                self.player_attack()

    def passive_motion(self, x, y):
        if not self.mouse_captured:
            return

        dx = x - self.mouse_x
        dy = y - self.mouse_y

        sensitivity = 0.2

        if self.state == self.STATE_PUZZLE:
            pass

        elif self.state == self.STATE_MAZE:
            self.maze_camera_yaw -= dx * sensitivity
            self.maze_camera_pitch -= dy * sensitivity
            self.maze_camera_pitch = max(-89, min(89, self.maze_camera_pitch))

        elif self.state == self.STATE_COMBAT:
            if self.combat_first_person == False:
                self.combat_camera_yaw -= dx * sensitivity
            else:
                self.combat_camera_yaw += dx * sensitivity

        self.mouse_x = self.width // 2
        self.mouse_y = self.height // 2
        glutWarpPointer(self.mouse_x, self.mouse_y)

    def update(self):
        self.camera_angle += 0.5
        self.menu_rotation += 0.5
        self.combat_animation += 1
        self.guardian_animation += 1
        self.combat_camera_angle += 0.3

        if self.hit_flash > 0:
            self.hit_flash -= 1

        if self.screen_shake > 0:
            self.screen_shake -= 0.5

        if self.state == self.STATE_PUZZLE:
            self.update_hopping(0.016)

        if self.state == self.STATE_COMBAT:
            self.update_combat(0.016)

        if self.state == self.STATE_DIALOGUE:
            self.dialogue_system.update_text_animation()

        if self.state == self.STATE_STAGE_COMPLETE:
            self.stage_complete.update()

        glutPostRedisplay()

    def run(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)
        glutInitWindowPosition(100, 100)
        glutCreateWindow(b"Hiccup's Adventure - 3D Game")

        glutDisplayFunc(self.display)
        glutKeyboardFunc(self.keyboard)
        try:
            glutKeyboardUpFunc(self.keyboard_up)
        except:
            pass
        glutSpecialFunc(self.special_keyboard)
        glutMouseFunc(self.mouse)
        glutPassiveMotionFunc(self.passive_motion)
        glutIdleFunc(self.update)

        glutMainLoop()


        print("=" * 60)
        print("HICCUP'S ADVENTURE - 3D Game (Simplified)")
        print("=" * 60)
        print("Controls:")
        print("  Menu: UP/DOWN, ENTER")
        print("  Puzzle: WASD to move, QE to move up/down, Mouse to look")
        print("          Click to select block, IJKL to move block horizontally")
        print("          UO to stack blocks up/down, P to skip")
        print("  Maze: WASD to move, QE to move up/down, Mouse to look around")
        print("        P to skip")
        print("  Combat: WASD to move, SPACE to attack, E to dodge")
        print("          TAB to switch weapon, ENTER to retry/continue")
        print("  C: Toggle cheat mode (anywhere)")
        print("  ESC: Back to menu / Exit")
        print("=" * 60)
        print("\nStarting game...")

        glutMainLoop()

if __name__ == "__main__":
    game = Game()
    game.run()
