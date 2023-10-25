import sys
import struct

# The class ImageProcessor for processing and saving an image
class ImageProcessor:

    # The constuctor of an instance which should get a file object as an argument
    def __init__(self, file):
        # Reading the BMP header
        self.header = {
            'signature': struct.unpack('H', file.read(2))[0],
            'filesize': struct.unpack('I', file.read(4))[0],
            'reserved1': struct.unpack('H', file.read(2))[0],
            'reserved2': struct.unpack('H', file.read(2))[0],
            'dataOffset': struct.unpack('I', file.read(4))[0],
            'headerSize': struct.unpack('I', file.read(4))[0],
            'width': struct.unpack('I', file.read(4))[0],
            'height': struct.unpack('I', file.read(4))[0],
            'planes': struct.unpack('H', file.read(2))[0],
            'bitsPerPixel': struct.unpack('H', file.read(2))[0],
            'compression': struct.unpack('I', file.read(4))[0],
            'imageSize': struct.unpack('I', file.read(4))[0],
            'xPixelsPerMeter': struct.unpack('I', file.read(4))[0],
            'yPixelsPerMeter': struct.unpack('I', file.read(4))[0],
            'colorsUsed': struct.unpack('I', file.read(4))[0],
            'colorsImportant': struct.unpack('I', file.read(4))[0]
        }
        if self.header['signature'] != 0x4D42:
            sys.exit('The file is not a BMP image.')

        if self.header['bitsPerPixel'] != 8:
            sys.exit('The image should have a color depth of 8 bits.')

        rowSize = self.header['width'] + padding(self.header['width'])  # Size of a row with padding
        #file.seek(self.header['dataOffset']) # Moving to pixels in the file

        # Reading crap between the header and pixels
        self.dataBetween = file.read(self.header['dataOffset'] - 54)

        # Reading image pixels in a list of rows
        self.pixels = []
        for rows in range(self.header['height']):
            row = file.read(rowSize)
            self.pixels.append(row)

    # The method rotating an image for 90 degrees CW
    def rotateCW(self):
        newWidth = self.header['height']
        newHeight = self.header['width']
        newPixels = []

        for y in range(newHeight):
            row = []
            for x in range(newWidth):
                row.append(self.pixels[newWidth - 1 - x][y])
            for i in range(padding(newWidth)):
                row.append(0)
            newPixels.append(bytes(row))

        self.pixels = newPixels
        self.header['height'] = newHeight
        self.header['width'] = newWidth


    # The method rotating an image for 90 degrees CCW
    def rotateCCW(self):
        newWidth = self.header['height']
        newHeight = self.header['width']
        newPixels = []

        for y in range(newHeight):
            row = []
            for x in range(newWidth):
                row.append(self.pixels[x][newHeight - 1 - y])
            for i in range(padding(newWidth)):
                row.append(0)
            newPixels.append(bytes(row))

        self.pixels = newPixels
        self.header['height'] = newHeight
        self.header['width'] = newWidth

    #The method applying Gaussian filter
    def gauss(self):
        pass

    #The method saving an image in the specified file
    def saveImage(self, file):
        headerpack = struct.pack('<HIHHIIIIHHIIIIII',
                                 self.header['signature'],
                                 self.header['filesize'],
                                 self.header['reserved1'],
                                 self.header['reserved1'],
                                 self.header['dataOffset'],
                                 self.header['headerSize'],
                                 self.header['width'],
                                 self.header['height'],
                                 self.header['planes'],
                                 self.header['bitsPerPixel'],
                                 self.header['compression'],
                                 self.header['imageSize'],
                                 self.header['xPixelsPerMeter'],
                                 self.header['yPixelsPerMeter'],
                                 self.header['colorsUsed'],
                                 self.header['colorsImportant']
                                 )
        file.write(headerpack)
        file.write(self.dataBetween)
        for i in range(len(self.pixels)):
            file.write(self.pixels[i])

# The function calculating a padding value
def padding(width, bitCount = 8):
    return int((4 - (width * (bitCount / 8)) % 4)) & 3
