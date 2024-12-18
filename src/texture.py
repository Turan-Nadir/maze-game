from OpenGL.GL import *
from PIL.Image import open
class Texture:
    def loadImage(self, filename):
        try:
            image = open(filename)
        except IOError as ex:
            print('IOError: failed to open texture file')
            print(ex)
            return -1

        print('Opened image file: size =', image.size, 'format =', image.format)

        texture_id = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 4)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)

        image_data = image.convert('RGBA').tobytes()

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.size[0], image.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

        image.close()

        return texture_id