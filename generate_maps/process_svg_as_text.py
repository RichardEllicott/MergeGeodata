"""


modifying xml:
https://www.geeksforgeeks.org/modify-xml-files-with-python/



"""
import hashlib
from enum import Enum
from colour import Color # https://pypi.org/project/colour/
import random


# import shutil

filename = "BlankMap-Equirectangular.svg"
new_filename = "BlankMap-Equirectangular.modified.svg"


prev_colors = {}



def string_to_color(hash_me):

    hash_me = hash_me.encode('utf-8')

    result = hashlib.md5(hash_me).hexdigest()

    result = "#" + result[0:6]


    if not result in prev_colors:
        prev_colors[result] = None

    else:
        print("warning, duplicate colour: ", result)

    return result


random.seed(10)


def string_to_color2(hash_me):

    # note setting seed to 10 seems okay, some seeds resuly in unclear colors


    # random.seed(hash_me)


    c = Color(hue=random.random(), saturation=1, luminance=0.5)
    result = str(c.hex_l)
    print(result)

    if not result in prev_colors:
        prev_colors[result] = None

    else:
        print("warning, duplicate colour: ", result)

        for i in range(10):

            print("try again to find color ", i)

            c = Color(hue=random.random(), saturation=1, luminance=0.5)
            result = str(c.hex_l)
            if not result in prev_colors:
                prev_colors[result] = None
                print("found unqiue color")
                break
            

            pass


    return result




class Mode(Enum):
    default = 0
    script1 = 1
    script2 = 2


class Main():

    MODE_default = 0
    MODE_allblack = 1
    MODE_outline = 3
    MODE_default_fullsat = 4


    mode = MODE_default_fullsat


    def _default(self, ob):

        ob.set('fill', string_to_color(str(i)))

        pass


    def __init__(self):

        


        i = 0

        # importing the module.
        import xml.etree.ElementTree as ET
        XMLexample_stored_in_a_string ='''<?xml version ="1.0"?>
        <COUNTRIES>
            <country name ="INDIA">
                <neighbor name ="Dubai" direction ="W"/>
            </country>
            <country name ="Singapore">
                <neighbor name ="Malaysia" direction ="N"/>
            </country>
        </COUNTRIES>
        '''
        # parsing directly.
        tree = ET.parse(filename)
        root = tree.getroot()
        # parsing using the string.
        stringroot = ET.fromstring(XMLexample_stored_in_a_string)
        # printing the root.
        print(root)
        print(stringroot)

        for ob in root:

            # print("        ",ob, " ",ob.text)

            for ob2 in ob:
                # print("        ",ob2, " ",ob2.text)
                for ob3 in ob2:
                    # print("        ",ob3, " ",ob3.text)

                    if ob3.tag == "{http://www.w3.org/2000/svg}path":
                        # print("found path tag, adding fill tag...")

                        # ob3.set('fill', '#AB7C94')

                        # 
                        # ob3.set('fill', "#00000000")

                        
                        if self.mode == self.MODE_default:
                            
                            # print("run mode ",self.mode)


                            # self._default(ob3)
                            ob3.set('fill', string_to_color(str(i)))

                        elif self.mode == self.MODE_allblack: # ALL BLACK
                            # fills and strokes:
                            # https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Fills_and_Strokes

                            # print("run mode ",self.mode)

                            stroke_width = str(1.0/16.0)

                            ob3.set('fill', "#000000")  # make all black

                            ob3.set('stroke', "#000000")  # stroke is black
                            ob3.set('stroke-width', stroke_width)  # make all black


                            # ob3.set('width', "1")  # make all black
                            # ob3.set('height', "1")  # make all black
                            
                        elif self.mode == self.MODE_outline: # outline only

                            stroke_width = str(1.0/16.0)

                            ob3.set('stroke', "#FFFFFF")  # stroke is white
                            ob3.set('stroke-width', stroke_width)  # make all black
                            ob3.set('fill-opacity', "0")  # make all black

                        # elif self.mode == self.MODE_default_fullsat: # outline only
                        #     ob3.set('fill', string_to_color2(i)

                        elif self.mode == self.MODE_default_fullsat:
                            ob3.set('fill', string_to_color2(str(i)))
                            pass


                        i += 1

                    # print("        ",ob3, " ",ob3.attrib)
 


                    # for ob4 in ob3:
                    #     print("        ",ob4, " ",ob4.text)


        tree.write(new_filename)


Main()









