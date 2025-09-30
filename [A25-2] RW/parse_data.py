import json, csv, os, sys, re
from urllib.parse import unquote

languages = ['ENG']
localize = {}
data_folder = sys.argv[1]
finalized = {}
hold = {}

def copy_keys(dest, source, ls):
    for l in ls:
        if l in source:
            dest[l] = source[l]

def open_file(filename):
    with open(f'{data_folder}{filename}.json') as f:
        return json.load(f)

def get_localization():
    for lang in languages:
        j = open_file(f'Message_{lang}')
        for thing in j['File']['Object']:
            try:
                entry = localize[thing['Id']]
            except:
                entry = {}
                localize[thing['Id']] = entry
            entry[f'text_{lang}'] = re.sub(r'<[^<]+>', '', unquote(thing['String']['Data']))

def export_csv():
    keys = {
        'trait': [
            'TraitId', 'EnabledFlag', 'Index',
            'text_ENG', 'desc_ENG',
            'GatherableFlag', 'Grade', 'Unknown2', 'Value1_1', 'Value1_2',
            'Value2_2', 'Value2_2', 'TraitKindId1', 'TraitKindId2',
            'Combo1', 'Combo2'
        ]
    }
    for k, v in finalized.items():
        head = keys[k] if k in keys else v[list(v.keys())[0]].keys()
        with open(f'output/{k}.csv', 'w+') as f:
            writer = csv.DictWriter(f, head, delimiter='\t', extrasaction='ignore')
            writer.writeheader()
            for v2 in v.values():
                  writer.writerow(v2)

def trait():
    dic = {}
    finalized['trait'] = dic
    j = open_file('Trait')
    for item in j['File']['Object']:
        try:
            d = {}
            copy_keys(d, item, ['TraitId', 'EnabledFlag', 'Index',
                'GatherableFlag', 'Grade', 'Unknown2', 'Value1_1', 'Value1_2',
                'Value2_2', 'Value2_2', 'TraitKindId1', 'TraitKindId2'])
            d = d | localize[item['NameStringIndex']].copy()
            for lang in languages:
                d[f'desc_{lang}'] = localize[item['DescriptionStringIndex']][f'text_{lang}']
            dic[item['TraitId']] = d
        except:
            pass

    j = open_file('TraitMix')
    for item in j['file']['Object']:
        try:
            dic[item['Trait3']]['Combo1'] = dic[item['Trait1']]['text_ENG']
            dic[item['Trait3']]['Combo2'] = dic[item['Trait2']]['text_ENG']
        except:
            pass


get_localization()
trait()
export_csv()

#print(finalized['trait'])
