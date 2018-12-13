#!/usr/bin/env python3
# *-* coding:utf-8 *-*

"""

:mod:`lab_yaml` -- YAML Parsing
=========================================

LAB_YAML Learning Objective: Learn to parse a YAML file using the PyYAML
                             library and use the information.
::

 a. Load the data/widget.yml file using the PyYAML library.

 b. Change the value for the width and height of the window element to be 1/2
    their current value.
    Change the size of the text element to be 1/4 it's current value.
    Change the image alignment element to 'justified'.

 c. Save your updated object to widget_updated.yaml using the PyYAML library.

"""
import yaml

yml_text = open('../RU_Python_IV/data/widget.yml', 'r').read()
yml_obj = yaml.load(yml_text)

widget_height = int(yml_obj['widget']['window']['height'])/2
widget_width = int(yml_obj['widget']['window']['width'])/2
text_size = int(yml_obj['widget']['text']['size'])/4
image_alignment = 'justified'

yml_obj['widget']['window']['height'] = widget_height
yml_obj['widget']['window']['width'] = widget_width
yml_obj['widget']['text']['size'] = text_size
yml_obj['widget']['image']['alignment'] = image_alignment

yml_text = yaml.dump(yml_obj, width=60)
open('lab_yaml_widget.yml', 'w').write(yml_text)
