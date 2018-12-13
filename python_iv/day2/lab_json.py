#!/usr/bin/env python3
# *-* coding:utf-8 *-*

"""
:mod:`lab_json` -- JSON to YAML and back again
=========================================

LAB_JSON Learning Objective: Learn to navigate a JSON file and convert to a
                             python object.
::

 a. Create a script that expects 3 command line arguments: -j or -y,
    json_filename, yaml_filename
    The first argument is -j or -y based on whether to convert from JSON to
    YAML (-j) or YAML to JSON (-y)
    The second argument is the name of the json file to parse or save to
    The third argument is the name of the yaml file to parse or save to

 b. Based on the -y/-j selection, parse the contents of the input file using
    the appropriate library.

 c. Using the other library, save the parsed object to the output filename

 d. Test your script using the json and yml files in the data directory.

 e. If you have time, create your own JSON and YAML files and translate between
    the formats.

"""
import json
import yaml
import argparse


# Defining our arguments and help message
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-j", "--json_convert",
        nargs=2,
        default=None,
        help="Provide input files for conversion from json to yaml"
    )
    parser.add_argument(
        "-y", "--yaml_convert",
        nargs=2,
        default=None,
        help="Provide input files for conversion from yaml to json"
    )
    return parser.parse_args()


# Runner
if __name__ == "__main__":
    args = parse_args()

    if not args.json_convert and not args.yaml_convert:
        print("Try using --help")
    else:
        if args.json_convert:
            json_file = args.json_convert[0]
            yaml_file = args.json_convert[1]

            jsn_text = open(json_file, 'r').read()
            jsn_obj = json.loads(jsn_text)
            yml_txt = yaml.dump(jsn_obj)
            open(yaml_file, 'w').write(yml_txt)
        elif args.yaml_convert:
            yaml_file = args.yaml_convert[0]
            json_file = args.yaml_convert[1]

            yml_text = open(yaml_file, 'r').read()
            yml_obj = yaml.load(yml_text)
            jsn_txt = json.dumps(yml_obj)
            open(json_file, 'w').write(jsn_txt)
