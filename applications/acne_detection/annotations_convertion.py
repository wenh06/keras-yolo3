# -*- coding: utf-8 -*-
import os
import glob
import shutil
import random
import pandas as pd
import xml.etree.ElementTree as ET
from typing import Optional, NoReturn


__all__ = [
    'xml_to_csv',
]


_ALL_LESION_TYPES = ['fore', 'cold_sore',]
_VALID_LEISION_TYPES = ['fore',]


def xml_to_csv(xml_path:str, save_csv_path:Optional[str]=None) -> pd.DataFrame:
    """
    """
    xml_list = []
    for xml_file in glob.glob(xml_path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        if len(root.findall('object')) == 0:
            print('{} has no acne annotation'.format(xml_file))
        for member in root.findall('object'):
            values = {
                'filename': root.find('filename').text if root.find('filename') is not None else '',
                'width': int(root.find('size').find('width').text),
                'height': int(root.find('size').find('height').text),
                'segmented': root.find('segmented').text if root.find('segmented') is not None else '',
                'class': member.find('name').text,
                'pose': member.find('pose').text if member.find('pose') is not None else '',
                'truncated': member.find('truncated').text if member.find('truncated') is not None else '',
                'difficult': member.find('difficult').text if member.find('difficult') is not None else '',
                'xmin': int(member.find('bndbox').find('xmin').text),
                'ymin': int(member.find('bndbox').find('ymin').text),
                'xmax': int(member.find('bndbox').find('xmax').text)-1,
                'ymax': int(member.find('bndbox').find('ymax').text)-1,
            }
            xml_list.append(values)
    column_names = ['filename', 'width', 'height', 'segmented', 'class', 'pose', 'truncated', 'difficult', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list)
    xml_df = xml_df[column_names]

    if save_csv_path is not None:
        xml_df.to_csv(save_csv_path, index=False)
        print('Converted xml to csv successfully .')

    return xml_df


def voc_to_yolo(voc_ann_path:str, yolo_save_path:str) -> NoReturn:
    """
    """
    
