"""


modifying xml:
https://www.geeksforgeeks.org/modify-xml-files-with-python/



"""
import hashlib
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






def main_script():

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

                    ob3.set('fill', string_to_color(str(i)))

                    i += 1

                # print("        ",ob3, " ",ob3.attrib)



                # for ob4 in ob3:
                #     print("        ",ob4, " ",ob4.text)


    tree.write(new_filename)


main_script()



result = hashlib.md5(b'GeeksforGeeks').hexdigest()


print(result)






