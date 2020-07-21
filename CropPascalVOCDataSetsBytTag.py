#-*- coding: utf-8 -*-

from pathlib import Path
import xml.etree.ElementTree as ET
from typing import Dict
import time
import os
import sys
from PIL import Image

class XMLHandler:
    def __init__(self, xml_path: str or Path):
        self.xml_path = Path(xml_path)
        self.root = self.__open()

    def __open(self):
        with self.xml_path.open() as opened_xml_file:
            self.tree = ET.parse(opened_xml_file)
            return self.tree.getroot()
            

def converter(xml_files: str, output_folder: str) -> None:
    xml_files = sorted(list(Path(xml_files).rglob("*.xml")))
    
    tags = []
    nbtags = 1

    for _, xml in enumerate(xml_files, start=1):
        xml_content = XMLHandler(xml)
        for _,sg_box in enumerate(xml_content.root.iter('annotation')):
            _, tail = os.path.split(sg_box.find("path").text)
            CheminFichier = XML_FOLDER+tail
            print("Traitement du Fichier : %s " % CheminFichier)
            
            for _, sg_box_ in enumerate(xml_content.root.iter('object')):
                Tag = sg_box_.find("name").text
                tags.append(sg_box_.find("name").text)

                #On calcule les boudind boxes
                right = int(sg_box_.find("bndbox").find("xmax").text)
                bottom = int(sg_box_.find("bndbox").find("ymax").text)
                top = int(sg_box_.find("bndbox").find("ymin").text)
                left = int(sg_box_.find("bndbox").find("xmin").text)

                ImageDataset = Image.open(CheminFichier)
                CropBox = (left,top,right,bottom)
                ImageCrop = ImageDataset.crop(CropBox)
                NomFichierCroped = Tag + "_" + str(nbtags) + ".jpg"
                ImageCrop.save(NomFichierCroped)

                nbtags += 1

    ListeTags = list(dict.fromkeys(tags))
    print("Nombre d'items dans le DataSet : %s" %nbtags)
    print("Liste des Tags présents : %s" %ListeTags)
    for item in ListeTags:
        nbItem = tags.count(item)
        print("Nombre de " + str(item) + " dans le DataSet : %s" % nbItem + " soit " + str(round(100 * float (nbItem) /float (nbtags),0)) + "%")
  

if __name__ == '__main__':
	if len(sys.argv) <= 1:
		print('USAGE: {} repertoire'.format(sys.argv[0]))
	else:
		t1 = time.time()
		XML_FOLDER = sys.argv[1]
		OUTPUT_FOLDER =  "."

		converter(XML_FOLDER, OUTPUT_FOLDER)
		print('Temps de Traitement : %d s'%(time.time()-t1))
