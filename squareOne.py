#!/usr/bin/env python

# squareOne.py
# by Daniel Larsen
#
# Used to track Square-1 Cube move repository.  First, copy endValue.json data to
# startValue.json (assuming you haven't messed with the cube).  Then do your move,
# filling out the appropriate startValue/endValue fields.  Run consolidateMove, which
# will create a consolidated.json.  Replace the call to 'moves.json' with that file
# to verify the move before adding it to the list.  When you are satisfied, call
# addConsolidated to add the move to the list (don't forget to point back to 'moves.json')
# Moves are documented as a 'U' (top) 'D' (bottom) and a 'F' (180 rotate).  With U & D,
# it's clockwise, and the number is how many possible turn spots it should pass.

from math import *
import pyglet
from pyglet.gl import *
from pyglet.window import key
from OpenGL.GLUT import *
import json

CUBE_HEIGHT = 100
BASIC_ANGLE = 15
MIDDLE_WIDTH = CUBE_HEIGHT * tan(radians(BASIC_ANGLE))
CORNER_WIDTH = (CUBE_HEIGHT - MIDDLE_WIDTH) / 2
SQUARE_OFFSET = MIDDLE_WIDTH / (2 * cos(radians(45)))
TRIANGLE_LENGTH = CUBE_HEIGHT / (2 * cos(radians(BASIC_ANGLE)))
CORNER_LENGTH = CUBE_HEIGHT / (2 * cos(radians(45)))

CUBE_HEIGHT = 100


class Segment:
    def __init__(self, verts, color):
        self.color = color
        self.verts = verts


class Piece:
    RED = (1, 0, 0)
    ORANGE = (1, 0.5, 0)
    YELLOW = (1, 1, 0)
    GREEN = (0, 1, 0)
    BLUE = (0, 0, 1)
    WHITE = (0.85, 0.85, 0.85)
    BLACK = (0, 0, 0)

    def toColor(colorString):
        if colorString == "red":
            return Piece.RED
        elif colorString == "orange":
            return Piece.ORANGE
        elif colorString == "yellow":
            return Piece.YELLOW
        elif colorString == "green":
            return Piece.GREEN
        elif colorString == "blue":
            return Piece.BLUE
        elif colorString == "white":
            return Piece.WHITE
        return Piece.BLACK

    def __init__(self, shape, colors, isBottom=False, invisible=False):
        self.shape = shape
        self.colors = []
        for color in colors:
            self.colors.append(Piece.toColor(color))
        self.segments = []
        self.invisible = invisible
        uVerts = []
        mVerts = []
        dVerts = []
        lVerts = []
        rVerts = []
        if shape == "triangle":
            uVerts.append((0, 0, 0))
            uVerts.append(
                (
                    TRIANGLE_LENGTH * cos(radians(BASIC_ANGLE)),
                    0,
                    TRIANGLE_LENGTH * sin(radians(BASIC_ANGLE)),
                )
            )
            uVerts.append(
                (
                    TRIANGLE_LENGTH * cos(radians(-BASIC_ANGLE)),
                    0,
                    TRIANGLE_LENGTH * sin(radians(-BASIC_ANGLE)),
                )
            )
            self.segments.append(Segment(uVerts, self.colors[0]))
            mVerts.append(uVerts[2])
            mVerts.append(uVerts[1])
            mVerts.append((uVerts[1][0], -CORNER_WIDTH, uVerts[1][2]))
            mVerts.append((uVerts[2][0], -CORNER_WIDTH, uVerts[2][2]))
            self.segments.append(Segment(mVerts, self.colors[1]))
            for vert in uVerts:
                dVerts.append([vert[0], vert[1] - CORNER_WIDTH, vert[2]])
            self.segments.append(Segment(dVerts, Piece.BLACK))
            self.segments.append(
                Segment([uVerts[0], uVerts[1], dVerts[1], dVerts[0]], Piece.BLACK)
            )
            self.segments.append(
                Segment([uVerts[0], uVerts[2], dVerts[2], dVerts[0]], Piece.BLACK)
            )
            self.angularWidth = 2 * BASIC_ANGLE
        elif shape == "corner":
            uVerts.append((0, 0, 0))
            uVerts.append(
                (
                    TRIANGLE_LENGTH * cos(radians(+BASIC_ANGLE * 2)),
                    0,
                    (TRIANGLE_LENGTH * sin(radians(+BASIC_ANGLE * 2))),
                )
            )
            uVerts.append((CORNER_LENGTH, 0, 0))
            uVerts.append(
                (
                    TRIANGLE_LENGTH * cos(radians(-BASIC_ANGLE * 2)),
                    0,
                    (TRIANGLE_LENGTH * sin(radians(-BASIC_ANGLE * 2))),
                )
            )
            self.segments.append(Segment(uVerts, self.colors[0]))
            lVerts.append(uVerts[2])
            lVerts.append(uVerts[1])
            lVerts.append((uVerts[1][0], -CORNER_WIDTH, uVerts[1][2]))
            lVerts.append((uVerts[2][0], -CORNER_WIDTH, uVerts[2][2]))
            self.segments.append(Segment(lVerts, self.colors[1]))
            rVerts.append(uVerts[3])
            rVerts.append(uVerts[2])
            rVerts.append((uVerts[2][0], -CORNER_WIDTH, uVerts[2][2]))
            rVerts.append((uVerts[3][0], -CORNER_WIDTH, uVerts[3][2]))
            self.segments.append(Segment(rVerts, self.colors[2]))
            for vert in uVerts:
                dVerts.append([vert[0], vert[1] - CORNER_WIDTH, vert[2]])
            self.segments.append(Segment(dVerts, Piece.BLACK))
            self.segments.append(
                Segment([uVerts[0], uVerts[1], dVerts[1], dVerts[0]], Piece.BLACK)
            )
            self.segments.append(
                Segment([uVerts[0], uVerts[3], dVerts[3], dVerts[0]], Piece.BLACK)
            )
            self.angularWidth = 4 * BASIC_ANGLE
        elif shape == "middle":
            mVerts.append(
                (
                    TRIANGLE_LENGTH * cos(radians(BASIC_ANGLE)),
                    (TRIANGLE_LENGTH * sin(radians(BASIC_ANGLE))),
                    CUBE_HEIGHT / 2,
                )
            )
            mVerts.append(
                (
                    TRIANGLE_LENGTH * cos(radians(180 - BASIC_ANGLE)),
                    (TRIANGLE_LENGTH * sin(radians(180 - BASIC_ANGLE))),
                    CUBE_HEIGHT / 2,
                )
            )
            mVerts.append(
                (
                    TRIANGLE_LENGTH * cos(radians(180 + BASIC_ANGLE)),
                    (TRIANGLE_LENGTH * sin(radians(180 + BASIC_ANGLE))),
                    CUBE_HEIGHT / 2,
                )
            )
            mVerts.append(
                (
                    TRIANGLE_LENGTH * cos(radians(-BASIC_ANGLE)),
                    (TRIANGLE_LENGTH * sin(radians(-BASIC_ANGLE))),
                    CUBE_HEIGHT / 2,
                )
            )
            self.segments.append(Segment(mVerts, self.colors[1]))
            lVerts.append(mVerts[2])
            lVerts.append(mVerts[1])
            lVerts.append(
                (
                    mVerts[1][0],
                    mVerts[1][1],
                    mVerts[1][2] - (CUBE_HEIGHT - CORNER_WIDTH),
                )
            )
            lVerts.append(
                (
                    mVerts[2][0],
                    mVerts[2][1],
                    mVerts[2][2] - (CUBE_HEIGHT - CORNER_WIDTH),
                )
            )
            self.segments.append(Segment(lVerts, self.colors[0]))
            rVerts.append(mVerts[0])
            rVerts.append(mVerts[3])
            rVerts.append((mVerts[3][0], mVerts[3][1], mVerts[3][2] - CORNER_WIDTH))
            rVerts.append((mVerts[0][0], mVerts[0][1], mVerts[0][2] - CORNER_WIDTH))
            self.segments.append(Segment(rVerts, self.colors[2]))
            self.segments.append(
                Segment([lVerts[2], lVerts[3], rVerts[2], rVerts[3]], Piece.BLACK)
            )
            self.segments.append(
                Segment([mVerts[0], mVerts[1], lVerts[2], rVerts[3]], Piece.BLACK)
            )
            self.segments.append(
                Segment([mVerts[2], mVerts[3], rVerts[2], lVerts[3]], Piece.BLACK)
            )
            self.angularWidth = 180

        if isBottom:
            segments = []
            for segment in self.segments:
                verts = []
                for vertex in segment.verts:
                    verts.append((-vertex[0], -vertex[1], vertex[2]))
                segment.verts = verts

    def draw(self, origin, angle, isTop=True):
        if self.invisible:
            return
        for segment in self.segments:
            CubeWindow.drawSegment(segment.verts, segment.color, origin, angle)


class SquareOne:
    def __init__(self, data):
        self.setState(data)

    def setState(self, data):
        self.topPieces = []
        self.middlePieces = []
        self.bottomPieces = []

        for piece in data["top"]:
            self.topPieces.append(Piece(piece["shape"], piece["colors"]))
        for piece in data["middle"]:
            self.middlePieces.append(Piece(piece["shape"], piece["colors"]))
        for piece in data["bottom"]:
            self.bottomPieces.append(
                Piece(piece["shape"], piece["colors"], isBottom=True)
            )

    def draw(self):
        angle = +self.topPieces[0].angularWidth / 2
        for piece in self.topPieces:
            angle -= piece.angularWidth / 2
            piece.draw((0, CUBE_HEIGHT / 2, 0), angle)
            angle -= piece.angularWidth / 2

        angle = 0
        for piece in self.middlePieces:
            angle -= piece.angularWidth / 2
            piece.draw((0, 0, 0), angle)
            angle -= piece.angularWidth / 2

        angle = 180 + self.bottomPieces[0].angularWidth / 2
        for piece in self.bottomPieces:
            angle -= piece.angularWidth / 2
            piece.draw((0, -CUBE_HEIGHT / 2, 0), angle)
            angle -= piece.angularWidth / 2


INCREMENT = 5


class CubeWindow(pyglet.window.Window):
    def drawSegment(verts, color, origin, angle):
        if len(verts) == 3:
            drawType = GL_TRIANGLES
        else:
            drawType = GL_QUADS
        glBegin(drawType)
        glColor3f(color[0], color[1], color[2])
        for x, y, z in verts:
            rotated_x = origin[0] + x * cos(radians(angle)) - z * sin(radians(angle))
            rotated_y = origin[1] + y
            rotated_z = origin[2] + x * sin(radians(angle)) + z * cos(radians(angle))
            glVertex3f(rotated_x, rotated_y, rotated_z)
        glEnd()
        glBegin(GL_LINE_LOOP)
        glColor3f(0, 0, 0)
        for x, y, z in verts:
            rotated_x = origin[0] + x * cos(radians(angle)) - z * sin(radians(angle))
            rotated_y = origin[1] + y
            rotated_z = origin[2] + x * sin(radians(angle)) + z * cos(radians(angle))
            glVertex3f(rotated_x, rotated_y, rotated_z)
        glEnd()

    # Cube 3D start rotation
    xRotation = 30
    yRotation = 45

    def __init__(self, width, height, title, cube, opposite=False):
        super(CubeWindow, self).__init__(width, height, title)
        glClearColor(0.5, 0.5, 0.5, 1)
        glLineWidth(4)
        glEnable(GL_DEPTH_TEST)
        self.cube = cube
        self.opposite = opposite

    def on_draw(self):
        # Clear the current GL Window
        self.clear()

        # Push Matrix onto stack
        glPushMatrix()

        if self.opposite:
            glRotatef(self.xRotation, 1, 0, 0)
            glRotatef(self.yRotation + 90, 0, 1, 0)
            glRotatef(180, 0, 0, 1)
        else:
            glRotatef(self.xRotation, 1, 0, 0)
            glRotatef(self.yRotation, 0, 1, 0)

        self.cube.draw()

        # Pop Matrix off stack
        glPopMatrix()

    def on_resize(self, width, height):
        # set the Viewport
        glViewport(0, 0, width, height)

        # using Projection mode
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        aspectRatio = width / height
        gluPerspective(35, aspectRatio, 1, 1000)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, -300)

    def on_text_motion(self, motion):
        if motion == key.UP:
            CubeWindow.xRotation -= INCREMENT
        elif motion == key.DOWN:
            CubeWindow.xRotation += INCREMENT
        elif motion == key.LEFT:
            CubeWindow.yRotation -= INCREMENT
        elif motion == key.RIGHT:
            CubeWindow.yRotation += INCREMENT


def update(Hz):
    pass


class MoveTracker(pyglet.window.Window):
    def __init__(self, width, height, moveData, updateCubeFunc):
        super(MoveTracker, self).__init__(width, height, "Square One Move Display")
        self.moveIndex = 0
        self.numMoves = len(moveData["list"])
        self.moveData = moveData
        self.currentMove = moveData["list"][self.moveIndex]
        self.updateCubeFunc = updateCubeFunc
        self.moveText = pyglet.text.Label(
            "",
            font_name="Times New Roman",
            font_size=24,
            x=200,
            y=410,
            width=width - 40,
            anchor_x="center",
            anchor_y="center",
            multiline=True,
        )

    def on_draw(self):
        self.clear()
        self.moveText.text = "{}:\n\n{}".format(
            self.currentMove["name"], self.currentMove["moves"]
        )
        self.moveText.draw()

    def on_text_motion(self, motion):
        if motion == key.UP:
            self.moveIndex += 1
            if self.moveIndex == self.numMoves:
                self.moveIndex = 0
        elif motion == key.DOWN:
            self.moveIndex -= 1
            if self.moveIndex < 0:
                self.moveIndex = self.numMoves - 1
        elif motion == key.LEFT:
            self.moveIndex += 1
            if self.moveIndex == self.numMoves:
                self.moveIndex = 0
        elif motion == key.RIGHT:
            self.moveIndex -= 1
            if self.moveIndex < 0:
                self.moveIndex = self.numMoves - 1
        self.currentMove = moveData["list"][self.moveIndex]
        self.updateCubeFunc(self.currentMove)


if __name__ == "__main__":
    file = open("solved.json", "r")
    solvedData = json.loads(file.read())
    file.close()
    endCube = SquareOne(solvedData)
    firstEndWindow = CubeWindow(400, 400, "Square One Ending Front View", endCube)
    firstEndWindow.set_location(816, 25)
    secondEndWindow = CubeWindow(
        400, 400, "Square One Ending Back View", endCube, opposite=True
    )
    secondEndWindow.set_location(816, 450)

    file = open("moves.json", "r")
    moveData = json.loads(file.read())
    file.close()
    stateCube = SquareOne(moveData["list"][0])
    firstWindow = CubeWindow(400, 400, "Square One Starting Front View", stateCube)
    firstWindow.set_location(10, 25)
    secondWindow = CubeWindow(
        400, 400, "Square One Starting Back View", stateCube, opposite=True
    )
    secondWindow.set_location(10, 450)
    myWindow = MoveTracker(400, 825, moveData, stateCube.setState)
    myWindow.set_location(413, 25)

    pyglet.clock.schedule_interval(update, 1 / 60.0)
    pyglet.app.run()
