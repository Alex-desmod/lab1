import sys
import imaging

def main():
    try:
        if len(sys.argv) == 2:
            with open(sys.argv[1], 'rb') as inputfile:
                bmp = imaging.ImageProcessor(inputfile)
                print(f"Allocated memory size for image loading: {bmp.header['filesize']} bytes")

                bmp.rotateCW()
                fn = sys.argv[1][0:-4] + '_rotatedCW.bmp'
                recording(bmp, fn)
                print('Image rotated 90 degrees clockwise and saved successfully.')

                inputfile.seek(0)
                bmp = imaging.ImageProcessor(inputfile)
                bmp.rotateCCW()
                fn = sys.argv[1][0:-4] + '_rotatedCCW.bmp'
                recording(bmp, fn)
                print('Image rotated 90 degrees counterclockwise and saved successfully.')



        else:
            sys.exit('Invalid input')

    except FileNotFoundError:
        sys.exit(f'Could not find {sys.argv[1]}')

def recording(instance, filename):
    with open(filename, 'wb') as outputfile:
        instance.saveImage(outputfile)




if __name__ == '__main__':
    main()