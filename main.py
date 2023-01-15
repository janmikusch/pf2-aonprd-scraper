import requests
import json
import os

import classes
import config

from pathlib import Path


def create_valid_text(str):
    result = str.strip()
    result = result.replace('  ', '\n')
    result = result.replace('’', '\'')
    result = result.replace('\u2013', '-')
    result = result.replace('\u2014', '-')
    result = result.replace('\u2018', '\'')
    result = result.replace('\u201c', '"')
    result = result.replace('\u201d', '"')
    result = result.replace('\u2026', '...')
    return result.replace(' .', '.')


def remove_first_line(str):
    result = str.split('\n\n', 1)
    if len(result) == 1:
        return str
    else:
        return result[1]


def scrap_feats(print_all_keys=False):
    results = requests.post(config.url, json=config.post_data_get_feats, headers=config.headers)

    # save original data
    filename = config.output_folder + "json_original/aonprd_feats.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        file.write(results.text)
        file.close()

    # restructure json
    data = json.loads(results.text)
    feats_arr_original = data['hits']['hits']
    feats_arr = []
    keys = []
    for f in feats_arr_original:
        new_feat = classes.Feat()
        new_feat.name = create_valid_text(f['_source']['name'])
        new_feat.src = create_valid_text(f['_source']['source'][0])
        new_feat.page = f['_source']['source_raw'][0].split('pg.')[1]
        new_feat.src_raw = f['_source']['source_raw']
        new_feat.src_category = f['_source']['source_category']
        if 'pfs' in f['_source']:
            new_feat.pfs = f['_source']['pfs']
        new_feat.rarity = f['_source']['rarity']
        new_feat.level = f['_source']['level']
        new_feat.summary = create_valid_text(f['_source']['summary'])
        new_feat.text_original = create_valid_text(f['_source']['text'])
        new_feat.text = remove_first_line(create_valid_text(f['_source']['text'].strip()))
        new_feat.trait = f['_source']['trait']
        new_feat.resistance = f['_source']['resistance']
        new_feat.speed = f['_source']['speed']
        new_feat.weakness = f['_source']['weakness']
        if 'actions' in f['_source']:
            new_feat.actions = f['_source']['actions']
        if 'frequency' in f['_source']:
            new_feat.frequency = create_valid_text(f['_source']['frequency'])
        if 'trigger' in f['_source']:
            new_feat.trigger = create_valid_text(f['_source']['trigger'])
        if 'skill' in f['_source']:
            new_feat.skill = f['_source']['skill']
        if 'archetype' in f['_source']:
            new_feat.archetype = f['_source']['archetype']
        if 'requirement' in f['_source']:
            new_feat.requirement = create_valid_text(f['_source']['requirement'])
        if 'school' in f['_source']:
            new_feat.school = f['_source']['school']
        if 'cost' in f['_source']:
            new_feat.cost = f['_source']['cost']
        if 'spoilers' in f['_source']:
            new_feat.spoilers = f['_source']['spoilers']
        if 'access' in f['_source']:
            new_feat.access = f['_source']['access']

        feats_arr.append(new_feat)

        if print_all_keys:
            key_list = [key for key in f['_source']]
            for k in key_list:
                if k not in keys:
                    keys.append(k)

    if print_all_keys:
        print("All Feat keys:")
        print(keys)

    filename = config.output_folder + "json/aonprd_feats.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-16") as file:
        file.write(json.dumps(feats_arr, cls=classes.Encoder, indent=4))
        file.close()


def check_pf2etools():
    results = requests.post(config.url, json=config.post_data_get_feats, headers=config.headers)

    data = json.loads(results.text)
    feats_arr_original = data['hits']['hits']
    feat_names = []
    for f in feats_arr_original:
        name = create_valid_text(f['_source']['name']).lower()
        if name.__contains__(" ("):
            name = name.split(" (")[0]
        if name not in feat_names:
            feat_names.append(name)

    tool_feat_names = []

    for p in Path('./pf2etools/').glob('*.json'):
        tools_data = json.loads(p.read_text())
        for feat in tools_data['feat']:
            name = feat['name'].lower()
            tool_feat_names.append(name)

    feat_names.sort()
    tool_feat_names.sort()

    for x in feat_names:
        if x not in tool_feat_names:
            print(x)

    print("---------------------------------------------------------------------------------------------------")



    for x in feat_names:
        print(x)
    print("---------------------------------------------------------------------------------------------------")
    for x in tool_feat_names:
        print(x)


if __name__ == '__main__':
    scrap_feats()
