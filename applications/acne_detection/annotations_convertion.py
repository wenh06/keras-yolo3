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
    'voc_to_yolo',
    'voc_to_yolo_in_batch',
]


_ALL_LESION_TYPES = ['fore', 'cold_sore',]
_VALID_LEISION_TYPES = ['fore',]


def xml_to_csv(xml_dir:str, save_csv_path:Optional[str]=None) -> pd.DataFrame:
    """
    """
    xml_list = []
    for xml_file in glob.glob(os.path.join(xml_dir, '*.xml')):
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
                'xmax': int(member.find('bndbox').find('xmax').text),
                'ymax': int(member.find('bndbox').find('ymax').text),
            }
            xml_list.append(values)
    column_names = ['filename', 'width', 'height', 'segmented', 'class', 'pose', 'truncated', 'difficult', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list)
    xml_df = xml_df[column_names]

    if save_csv_path is not None:
        xml_df.to_csv(save_csv_path, index=False)
        print('Converted xml to csv successfully .')

    return xml_df


def voc_to_yolo(voc_ann_path:str, yolo_save_dir:str) -> NoReturn:
    """
    yolo annotation format:
        <object-class> <x_center> <y_center> <width> <height>
    ref.
        [1] https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects
        [2] https://github.com/tzutalin/labelImg/blob/master/libs/yolo_io.py
    """
    voc_filename = os.path.basename(voc_ann_path)
    tree = ET.parse(voc_filename)
    root = tree.getroot()

    if len(root.findall('object')) == 0:
        print('{} has no acne annotation'.format(voc_filename))
        return
    
    yolo_filename = voc_filename.replace('xml', 'txt')
    with open(os.path.join(yolo_save_dir, yolo_filename), 'w') as yf:
        img_width = int(root.find('size').find('width').text)
        img_height = int(root.find('size').find('height').text)
        for member in root.findall('object'):
            class_idx = _ALL_LESION_TYPES.index(member.find('name').text)
            difficult = member.find('difficult').text if member.find('difficult') is not None else ''
            xmin = int(member.find('bndbox').find('xmin').text)
            ymin = int(member.find('bndbox').find('ymin').text)
            xmax = int(member.find('bndbox').find('xmax').text)
            ymax = int(member.find('bndbox').find('ymax').text)
            xcen = float((xmin + xmax)) / 2 / img_width
            ycen = float((ymin + ymax)) / 2 / img_height
            w = float((xmax - xmin)) / img_width
            h = float((ymax - ymin)) / img_height
            yf.write("%d %.6f %.6f %.6f %.6f\n" % (class_idx, xcen, ycen, w, h))


def voc_to_yolo_in_batch(voc_dir:str, yolo_save_dir:str) -> NoReturn:
    """
    """
    for xml_file in glob.glob(os.path.join(voc_dir, '*.xml')):
        voc_to_yolo(xml_file, yolo_save_dir)


def yolo_to_csv(yolo_dir:str, save_csv_path:Optional[str]=None) -> pd.DataFrame:
    """
    """
    raise NotImplementedError
