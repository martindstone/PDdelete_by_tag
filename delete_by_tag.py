#!/usr/bin/env python

import sys
import requests
import json
import argparse
import urllib
import inflect

import pd

parser = argparse.ArgumentParser(description='Delete PagerDuty objects with the specified tags and types')
parser.add_argument('token', type=str, help='PagerDuty API Token')
parser.add_argument('cdl_tags', type=str, help='Comma-delimited list of tags')
parser.add_argument('cdl_types', type=str, help='Comma-delimited list of types (one of users, teams or escalation_policies)')
args = parser.parse_args()

p = inflect.engine()

tags = args.cdl_tags.split(",")
types = args.cdl_types.split(",")

obj_types = []
things_to_delete = {}
total_objects_found = 0

# Check object types against those supported by tags
for obj_type in types:
    if obj_type in ["users", "escalation_policies", "teams"]:
        obj_types.append(obj_type)
        things_to_delete[obj_type] = []
    else:
        print(f"\"{obj_type}\" is not a valid PagerDuty object type; skipping")

print(f"Looking for tags... ", end="", flush=True)
tag_objs = pd.fetch(token=args.token, endpoint="tags")
tag_objs = [tag_obj for tag_obj in tag_objs if tag_obj['label'] in tags]
print(f"Found {len(tag_objs)} {p.plural('tag', len(tag_objs))}.")

# find objects of the given types in the found tags
for tag_obj in tag_objs:
    for obj_type in obj_types:
        print(f"  Looking for {obj_type} with tag {tag_obj['id']}... ", end="", flush=True)
        objects = pd.fetch(token=args.token, endpoint=f"tags/{tag_obj['id']}/{obj_type}")
        print(f"  Found {len(objects)} {p.plural(p.singular_noun(obj_type), len(objects))}")
        things_to_delete[obj_type].extend(objects)
        total_objects_found += len(objects)

if total_objects_found == 0:
    print("Nothing to delete.\n")
    sys.exit(0)

# Give the user a summary and confirmation
print(f"\nFound {total_objects_found} {p.plural('object', total_objects_found)} to delete:")
for obj_type, objects in things_to_delete.items():
    if len(objects) > 0:
        print(f"{len(objects)} {p.plural(p.singular_noun(obj_type), len(objects))}:")
        for obj in objects:
            print(f"  {obj['id']}")

user_input = input('\nAre you sure you want to delete? [y/N] ')

if user_input.lower() in ('y', 'yes'):
    # do the delete
    print("OK, deleting...")
    for obj_type in sorted(things_to_delete):
        objects = things_to_delete[obj_type]
        for obj in objects:
            print(f"Deleting {p.singular_noun(obj_type)} {obj['id']}... ", end="", flush=True)
            r = pd.request(token=args.token, endpoint=f"{obj_type}/{obj['id']}", method="DELETE")
            if r.status_code >= 200 and r.status_code < 300:
                print("Deleted.")
            else:
                try:
                    print(f"Error {r.status_code}:\n{json.dumps(r.json()['error'], indent=4)}")
                except:
                    print(f"Error {r.status_code}")
else:
    print("OK, leaving everything alone.")
