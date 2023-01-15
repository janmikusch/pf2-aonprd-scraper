import requests
import json
import os

import classes
import config

def create_valid_text(str):
    result = str.replace('   ', '\n')
    return result.replace(' .', '.')


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
        new_feat.name = f['_source']['name']
        new_feat.src = f['_source']['source'][0]
        new_feat.page = f['_source']['source_raw'][0].split('pg.')[1]
        new_feat.src_raw = f['_source']['source_raw']
        new_feat.src_category = f['_source']['source_category']
        if 'pfs' in f['_source']:
            new_feat.pfs = f['_source']['pfs']
        new_feat.rarity = f['_source']['rarity']
        new_feat.level = f['_source']['level']
        new_feat.summary = create_valid_text(f['_source']['summary'].strip())
        new_feat.text = create_valid_text(f['_source']['text'].strip())
        new_feat.trait = f['_source']['trait']
        new_feat.resistance = f['_source']['resistance']
        new_feat.speed = f['_source']['speed']
        new_feat.weakness = f['_source']['weakness']
        if 'actions' in f['_source']:
            new_feat.actions = f['_source']['actions']
        if 'frequency' in f['_source']:
            new_feat.frequency = f['_source']['frequency']
        if 'trigger' in f['_source']:
            new_feat.trigger = f['_source']['trigger']
        if 'skill' in f['_source']:
            new_feat.skill = f['_source']['skill']
        if 'archetype' in f['_source']:
            new_feat.archetype = f['_source']['archetype']
        if 'requirement' in f['_source']:
            new_feat.requirement = f['_source']['requirement']
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


if __name__ == '__main__':
    scrap_feats()
