import json, csv, os, sys, re
from urllib.parse import unquote

languages = ['ENG', 'JPN', 'CHT', 'CHS', 'KOR']
localize = {}
data_folder = sys.argv[1]
finalized = {}
hold = {}

colors = {
    1824922885 : 'Red',
    1465702656 : 'Blue',
    667823249  : 'Green',
    553397017  : 'Yellow',
    444446048  : 'Purple'
}

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
            'TraitId', 'Index',
            'text_ENG', 'desc_ENG',
            'Combo1', 'Combo2',
            'Grade', 'Value1_1', 'Value1_2',
            'Value2_2', 'Value2_2',
            'Synthesis', 'Combat',
            'Restoratives', 'Inhibitor', 'Boost', 'Weapons', 'Armor', 'Accessories',
            'Starpearls', 'Exploration', 'Unknown',
            'TraitKindId1', 'TraitKindId2',
            'GatherableFlag', 'EnabledFlag',
            'text_JPN', 'desc_JPN',
            'text_CHS', 'desc_CHS',
            'text_CHT', 'desc_CHT',
            'text_KOR', 'desc_KOR',
        ],
        'effect': [
            'EffectId', 'Index',
            'text_ENG', 'desc_ENG',
            'Flag',
            'CombatTag', 'ExplorationTag',
            'ValueTag0', 'Value0_1', 'Value0_2',
            'ValueTag1', 'Value1_1', 'Value1_2',
            'ValueTag2', 'Value2_1', 'Value2_2',
            'ValueTag3', 'Value3_1', 'Value3_2',
            'text_JPN', 'desc_JPN',
            'text_CHS', 'desc_CHS',
            'text_CHT', 'desc_CHT',
            'text_KOR', 'desc_KOR',
        ],
        'skill': [
            'SkillId',
            'text_ENG', 'desc_ENG',
            'Unknown1', 'Numbers1', 'Unknown2',
            'Power1', 'Values1',
            'Power2', 'Values2',
            'Number', 'Flag', 'Index', 'Unknown3',
            'text_JPN', 'desc_JPN',
            'text_CHS', 'desc_CHS',
            'text_CHT', 'desc_CHT',
            'text_KOR', 'desc_KOR',
        ],
        'item': [
            'ItemId', 'Index',
            'text_ENG',
            'Category1', 'Category2', 'Category3', 'Category4',
            'Color1', 'Color2', 'Color3', 'Color4','Color5', 'Color6',
            'Color7', 'Color8', 'Color9', 'Color10','Color11', 'Color12',
            'PossiblyBasePrice', 'Flag4',
            'FlavorText',
        ]
    }
    for k, v in finalized.items():
        head = keys[k] if k in keys else v[list(v.keys())[0]].keys()
        with open(f'output/{k}.csv', 'w+') as f:
            writer = csv.DictWriter(f, head, delimiter='\t', extrasaction='ignore')
            writer.writeheader()
            for v2 in v.values():
                  writer.writerow(v2)

def desc_copy(d, item):
    for lang in languages:
        d[f'desc_{lang}'] = localize[item][f'text_{lang}']

def colortype():
    dic = {}
    hold['ItemColorType'] = dic
    j = open_file('ItemColorType')
    for item in j['File']['Object']:
        if item['ItemColorTypeId']:
            try:
                d = {}
                for i in range(1, 11):
                    d[f'Color{i}'] = colors[item[f'Color{i}']]
                dic[item['ItemColorTypeId']] = d
            except:
                print('ItemColorType issue', item)

def category():
    dic = {}
    finalized['category'] = dic
    j = open_file('ItemCategory')
    for item in j['File']['Object']:
        try:
            d = {}
            copy_keys(d, item, ['CategoryId'])
            d = d | localize[item['NameStringId']].copy()
            dic[item['CategoryId']] = d
        except:
            print('Category issue', item)

def effect():
    dic = {}
    finalized['effect'] = dic
    j = open_file('Potential')
    for item in j['File']['Object']:
        try:
            d = {}
            copy_keys(d, item, ['EffectId', 'Flag', 'Index',
                'CombatTag', 'ExplorationTag',
                'ValueTag0','ValueTag1', 'ValueTag2', 'ValueTag3',
                'Value0_1','Value1_1', 'Value2_1','Value3_1',
                'Value0_2','Value1_2', 'Value2_2','Value3_2',])
            d = d | localize[item['EffectNameId']].copy()
            desc_copy(d, item['EffectDescId'])
            for i in range(0,4):
                if d[f'ValueTag{i}'] == 1560167472:
                    d[f'ValueTag{i}'] = 'CHANGE_COLOR'
                    d[f'Value{i}_1'] = colors[d[f'Value{i}_1']]
                    d[f'Value{i}_2'] = colors[d[f'Value{i}_2']]
                elif d[f'ValueTag{i}'] == 499040286:
                    d[f'ValueTag{i}'] = 'CHANGE_CATEGORY'
            dic[item['EffectId']] = d
        except:
            print('Effect issue', item)
    dic = {}
    finalized['skill'] = dic
    j = open_file('Skill')
    for item in j['File']['Object']:
        try:
            d = {}
            copy_keys(d, item, ['SkillId', 'Number', 'Flag', 'Index',
                'Unknown1', 'Numbers1', 'Unknown2', 'Power1', 'Power2',
                'Values1', 'Values2', 'Numbers3', 'Unknown3'])
            d = d | localize[item['SkillNameId']].copy()
            desc_copy(d, item['SkillDescId'])
            dic[item['SkillId']] = d
        except:
            print('Skill issue', item)

    dic = {}
    hold['ItemPotential'] = dic
    j = open_file('ItemPotential')
    for item in j['File']['Object']:
        try:
            d = {}
            for i in range(1, 6):
                if item[f'SkillId{i}'] != 0:
                    #print('heck', item[f'SkillId{i}'])
                    d[f'SkillId{i}'] = item[f'SkillId{i}']
                    d[f'Name{i}'] = finalized['skill'][item[f'SkillId{i}']]['text_ENG']
                if item[f'EffectId{i}'] != 0:
                    d[f'EffectId{i}'] = item[f'EffectId{i}']
                    d[f'Name{i}'] = finalized['effect'][item[f'EffectId{i}']]['text_ENG']

            dic[item['PotentialId']] = d
        except:
            print('ItemPotential issue', item)
    #print(hold['ItemPotential'])


def flavor_text():
    # brute force baby
    chars = {
        2438102613 : 'Slade',
        1672439580 : 'Rias',
        1938933111 : 'El',
        1195643787 : 'Camilla',
        2945308662 : 'Heiter',
        3474295971 : 'Raze',
        3806937114 : 'Totori',
        1011208790 : 'Wilbell',
        424696390  : 'Sophie',
        3047332170 : 'Corneria',
        3304537638 : 'Ayesha',
        1831647589 : 'Oskar',
        2005173899 : 'Firis',
        791636945  : 'Vayne',
        219288777  : 'Shallistera',
        4088261028 : 'Ryza',
        3881335411 : 'Meruru',
        196936793  : 'Klaudia',
        2700974998 : 'Elie',
        1016542661 : 'Shallotte',
        1043128081 : 'Logy',
        2900069525 : 'Judie',
        1377937521 : 'Viorate',
        3968093192 : 'Mu',
        2129580665 : 'Marie',
        2606235912 : 'Randolf',
        1819653990 : 'Izana',
        3633319608 : 'Resna',
        3964000330 : 'Valeria',
        2651181797 : 'Heidi',
        621438385  : 'Plachta',
    }
    for thing in ['ItemFlavorText', 'EnemyFlavorText']:
        dic = {}
        hold[thing] = dic
        j = open_file(thing)
        for item in j['File']['Object']:
            try:
                d = {}
                j = 5;
                for i in range(1, 5):
                    if item[f'FlavorTextStringId{i}'] and item[f'UnknownId{j}']:
                        d[f'flavor{i}'] = localize[item[f'FlavorTextStringId{i}']].copy()
                        try:
                            d[f'char{i}'] = chars[item[f'UnknownId{j}']]
                        except:
                            d[f'char{i}'] = item[f'UnknownId{j}']
                            if item[f'UnknownId{j}'] > 0:
                                print('Unknown Chara')
                    j += 2
                dic[item['FlavorTextId']] = d
            except:
                print('Flavor issue', item['FlavorTextId'])

def item():
    dic = {}
    finalized['item'] = dic
    j = open_file('Item')
    for item in j['File']['Object']:
        try:
            d = {}
            copy_keys(d, item, ['ItemId', 'Index', 'PossiblyBasePrice', 'Flag4'])
            d = d | localize[item['NameStringId']].copy()
            dic[item['ItemId']] = d
            for i in range(1,5):
                if item[f'CategoryId{i}'] != 0:
                    d[f'Category{i}'] = finalized['category'][item[f'CategoryId{i}']]['text_ENG']
            if item['GiftColorId1']:
                d['Color1'] = colors[item['GiftColorId1']]
                d['Color2'] = colors[item['GiftColorId2']]
            if item['ItemColorTypeId']:
                for i in range(1, 11):
                    d[f'Color{i+2}'] = hold['ItemColorType'][item['ItemColorTypeId']][f'Color{i}']
            d['FlavorText'] = hold['ItemFlavorText'][item['FlavorTextId']]
        except:
            print('Item issue', item)


def trait():
    dic = {}
    finalized['trait'] = dic
    j = open_file('Trait')
    for item in j['File']['Object']:
        try:
            d = {}
            copy_keys(d, item, ['TraitId', 'EnabledFlag', 'Index',
                'GatherableFlag', 'Grade', 'Value1_1', 'Value1_2',
                'Value2_2', 'Value2_2', 'TraitKindId1', 'TraitKindId2',
                'text_JPN', 'desc_JPN',
                'text_CHS', 'desc_CHS',
                'text_CHT', 'desc_CHT',
                'text_KOR', 'desc_KOR',])
            copy_keys(d, item['TraitTransfer'], ['Synthesis', 'Combat',
                'Restoratives', 'Inhibitor', 'Boost', 'Weapons', 'Armor', 'Accessories',
                'Starpearls', 'Exploration', 'Unknown'])
            d = d | localize[item['NameStringIndex']].copy()
            for lang in languages:
                d[f'desc_{lang}'] = localize[item['DescriptionStringIndex']][f'text_{lang}']
            dic[item['TraitId']] = d
        except:
            print('Trait issue', item)

    j = open_file('TraitMix')
    for item in j['File']['Object']:
        try:
            dic[item['Trait3']]['Combo1'] = dic[item['Trait1']]['text_ENG']
            dic[item['Trait3']]['Combo2'] = dic[item['Trait2']]['text_ENG']
        except:
            print('TraitMix issue', item)

def other_text():
    dic = {}
    finalized['neat_localization_strings'] = dic
    ids = [
        1039643431
    ]
    for id in ids:
        d = localize[id].copy()
        dic[id] = d

get_localization()
colortype()
category()
flavor_text()
effect()
trait()
item()
other_text()
export_csv()

#print(finalized['trait'])
