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
            'Trait',
            'PossiblyBasePrice', 'Flag4',
            'FlavorText', 'DLC', 'Effect'
        ],
        'itemmix': [
            'ItemMixId',
            'Item1', 'Item2', 'Item3', 'Skill',
            'Number1', 'Number2',
            'Unknown2', 'Unknown3',
            'SkillId','ItemId1', 'ItemId2', 'ItemId3'
        ],
        'itemeffects': [
            'ItemId', 'Item',
            'Name1', 'Name2','Name3', 'Name4', 'Name5',
            'SkillId1', 'SkillId2','SkillId3', 'SkillId4', 'SkillId5',
            'EffectId1', 'EffectId2','EffectId3', 'EffectId4', 'EffectId5'
        ],
        'NpcShopMerchandise': [
            'text_ENG', 'ItemName',
            'Price', 'Limited', 'UnlockFlagId',
            'TraitName1',
            'LevelMin', 'LevelMax',
            'GradeMin', 'GradeMax',
            'ItemId','TraitId1',
            'text_JPN', 'text_CHS', 'text_CHT', 'text_KOR'
        ],
        'GiftTraitTable': [
            'GiftTraitTableId', 'Numbers1',
            'TraitName0','TraitName1','TraitName2','TraitName3','TraitName4',
            'TraitName5','TraitName6','TraitName7','TraitName8','TraitName9',
            'Numbers2', 'TraitIds'
        ],
        'recipe': [
            'RecipeId', 'Index', 'Quantity','Uses','Flag',
            'ItemName', 'IngredientName1', 'IngredientName2', 'IngredientName3', 'IngredientName4',
            'Category1','Category2','Category3',
            'ItemId', 'IngredientId1', 'IngredientId2', 'IngredientId3', 'IngredientId4'
        ],
        'recipemorph': [
            'ItemBaseName', 'IngredientName', 'ItemResultName',
            'ItemBaseId', 'IngredientId', 'ItemResultId',
        ],
        'recipebook': [
            'Book', 'RecipeName1', 'RecipeName2', 'RecipeName3',
            'ItemId', 'RecipeId1', 'RecipeId2', 'RecipeId3'
        ],
        'EnemyLibraryInfo': [
            'text_ENG', 'Race',
            #'Flag1', 'Integer', 'Flag2', 'Decimal1', 'Unknown4', 'Integer2', 'Decimal2', 'Integer3',
            #'Floats1', 'Floats2', 'Unknown1', 'Unknown2', 'EnemySizeTypeId', 'Flag',
            'Number', 'Number2',
            'ElemRes1', 'ElemRes2', 'ElemRes3',
            'ElemRes4', 'ElemRes5', 'ElemRes6',
            'AilRes1', 'AilRes2', 'AilRes3', 'AilRes4',
            'AilRes5', 'AilRes6', 'AilRes7', 'AilRes8',
            'DropReward0','DropReward1','DropReward2','DropReward3','DropReward4',
            'DropGift0','DropGift1','DropGift2','DropGift3','DropGift4',
            'text_JPN', 'text_CHS', 'text_CHT', 'text_KOR',
            'FlavorText', 'EnemyLibraryInfoId',
        ],
        'recipemap': [
            'Index',
            'Node0', 'Node1', 'Node2', 'Node3', 'Node4',
            'RightArrows', 'DownArrows',
        ],
        'gather': [
            'Index', 'Area', 'GatherType',
            'ItemName1','ItemName2','ItemName3',
            'Floors'
        ],
        'enemylocations': [
            'Index', 'Area',
            'EnemyName1','EnemyName2','EnemyName3','EnemyName4','EnemyName5',
            'Floors'
        ],
        'quest': [
            'text_ENG',
            'Gift1', 'Gift2', 'Gift3',
            'text_JPN', 'text_CHS', 'text_CHT', 'text_KOR',
            'Char', 'Flag'
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
    dic = {}
    finalized['race'] = dic
    j = open_file('EnemyKind')
    for item in j['File']['Object']:
        try:
            d = {}
            copy_keys(d, item, ['EnemyKindId'])
            d = d | localize[item['MessageId']].copy()
            dic[item['EnemyKindId']] = d
        except:
            print('EnemyKind issue', item)

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
                    d[f'SkillId{i}'] = item[f'SkillId{i}']
                    d[f'Name{i}'] = finalized['skill'][item[f'SkillId{i}']]['text_ENG']
                if item[f'EffectId{i}'] != 0:
                    d[f'EffectId{i}'] = item[f'EffectId{i}']
                    d[f'Name{i}'] = finalized['effect'][item[f'EffectId{i}']]['text_ENG']

            dic[item['ItemPotentialId']] = d
        except:
            print('ItemPotential issue', d)


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
    dic2 = {}
    finalized['itemeffects'] = dic2
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
            if item['DLCId']:
                d['DLC'] = True
            d['FlavorText'] = hold['ItemFlavorText'][item['FlavorTextId']]
            if item['ItemPotentialId']:
                if hold['ItemPotential'][item['ItemPotentialId']][f'Name1']:
                    d2 = {}
                    d2['ItemId'] = item['ItemId']
                    d2['Item'] = d['text_ENG']
                    for i in range(1,6):
                        copy_keys(d2, hold['ItemPotential'][item['ItemPotentialId']],
                            ['Name1', 'Name2','Name3', 'Name4', 'Name5',
                            'SkillId1', 'SkillId2','SkillId3', 'SkillId4', 'SkillId5',
                            'EffectId1', 'EffectId2','EffectId3', 'EffectId4', 'EffectId5'])
                    dic2[item['ItemId']] = d2
        except:
            print('Item issue', item)
    dic = {}
    finalized['itemmix'] = dic
    j = open_file('ItemMix')
    for item in j['File']['Object']:
        try:
            d = {}
            copy_keys(d, item, ['ItemMixId', 'Unknown2', 'Unknown3',
                'Number1', 'Number2', 'SkillId',
                'ItemId1', 'ItemId2', 'ItemId3'])
            d['Skill'] = finalized['skill'][item['SkillId']]['text_ENG']
            for i in range(1,4):
                if item[f'ItemId{i}']:
                    d[f'Item{i}'] = finalized['item'][item[f'ItemId{i}']]['text_ENG']
            dic[item['ItemMixId']] = d
        except:
            print('ItemMix issue', item)

    dic = {}
    finalized['recipe'] = dic
    j = open_file('Recipe')
    for item in j['File']['Object']:
        try:
            d = {}
            copy_keys(d, item, ['RecipeId', 'Index', 'Quantity', 'Uses','Flag',
                'ItemId', 'IngredientId1', 'IngredientId2', 'IngredientId3', 'IngredientId4'])
            if item[f'ItemId']:
                d[f'ItemName'] = finalized['item'][item[f'ItemId']]['text_ENG']
            for i in range(1,5):
                if item[f'IngredientId{i}']:
                    d[f'IngredientName{i}'] = finalized['item'][item[f'IngredientId{i}']]['text_ENG']
            for i in range(1,4):
                if item[f'CategoryId{i}']:
                    d[f'Category{i}'] = finalized['category'][item[f'CategoryId{i}']]['text_ENG']
            dic[item['RecipeId']] = d
        except Exception as e:
            print('Recipe issue', e, item)
    dic = {}
    finalized['recipemorph'] = dic
    j = open_file('RecipeChange')
    for item in j['File']['Object']:
        try:
            d = {}
            copy_keys(d, item, ['IngredientId', 'ItemBaseId', 'ItemResultId',])
            if 'IngredientId' in item and item['IngredientId'] > 0:
                d['IngredientName'] = finalized['item'][item['IngredientId']]['text_ENG']
            if 'ItemBaseId' in item and item['ItemBaseId'] > 0:
                d['ItemBaseName'] = finalized['recipe'][item['ItemBaseId']]['ItemName']
            if 'ItemResultId' in item and item['ItemResultId'] > 0:
                d['ItemResultName'] = finalized['recipe'][item['ItemResultId']]['ItemName']
            dic[item['RecipeChangeId']] = d
        except Exception as e:
            print('RecipeMorph issue', e, item)
    dic = {}
    finalized['recipebook'] = dic
    j = open_file('RecipeBook')
    for item in j['File']['Object']:
        try:
            d = {}
            copy_keys(d, item, ['ItemId', 'RecipeId1', 'RecipeId2', 'RecipeId3'])
            if item['ItemId']:
                d['Book'] = finalized['item'][item['ItemId']]['text_ENG']
            for i in range(1,4):
                if item[f'RecipeId{i}']:
                    d[f'RecipeName{i}'] = finalized['recipe'][item[f'RecipeId{i}']]['ItemName']
            dic[item['RecipeBookId']] = d
        except Exception as e:
            print('RecipeBook issue', e, item)

    dic = {}
    hold['AncientRecipe'] = dic
    j = open_file('AncientRecipe')
    for item in j['File']['Object']:
        try:
            d = {}
            dic[item['RecipeId']] = d
        except Exception as e:
            print('AncientRecipe issue', e, item)

    dic = {}
    hold['RecipeDerivationBase'] = dic
    j = open_file('RecipeDerivationBase')
    for item in j['File']['Object']:
        try:
            d = {}
            copy_keys(d, item, ['Index', 'RecipeId'])
            if item['RecipeId']:
                d['BaseName'] = finalized['recipe'][item['RecipeId']]['ItemName']
            dic[item['RecipeDerivationBaseId']] = d
        except Exception as e:
            print('RecipeDerivationBase issue', e, item)
    dic = {}
    hold['RecipeDerivationMap'] = dic
    j = open_file('RecipeDerivationMap')
    for item in j['File']['Object']:
        try:
            d = {}
            #if item['RecipeDerivationTypeId'] and item['RecipeDerivationTypeId'] not in [1617690764, 1276508687]:
            #    d['RecipeDerivationTypeId'] = item['RecipeDerivationTypeId']
            if item['RecipeOpenCharaId']:
                match item['RecipeOpenCharaId']:
                    case 1146794032: d['UnlockChar'] = 'Totori'
                    case 1945274091: d['UnlockChar'] = 'Sophie'
                    case _: d['UnlockChar'] = item['RecipeOpenCharaId']
            if item['RecipeId']:
                d['RecipeName'] = finalized['recipe'][item['RecipeId']]['ItemName']
                if item['RecipeId'] in hold['AncientRecipe']:
                    d['AncientRecipe'] = True
            if item['ItemId']:
                d['IngredientName'] = finalized['item'][item['ItemId']]['text_ENG']
            dic[item['RecipeDerivationMapId']] = d
        except Exception as e:
            print('RecipeDerivationMap issue', e, item)
    dic = {}
    finalized['recipemap'] = dic
    j = open_file('RecipeDerivationMapPosition')
    for item in j['File']['Object']:
        try:
            d = {}
            d['Index'] = hold['RecipeDerivationBase'][item['RecipeDerivationBaseId']]['Index']
            temp = {}
            for i in range(0,13):
                if hold['RecipeDerivationMap'][item['RecipeDerivationMapId'][i]]:
                    temp[f'Map{i}'] = hold['RecipeDerivationMap'][item['RecipeDerivationMapId'][i]].copy()

            if 'Map0' in temp:
                d['Node0'] = temp['Map0']
            if 'Map2' in temp:
                d['Node1'] = temp['Map2'] | temp['Map3']
            if 'Map5' in temp:
                d['Node2'] = temp['Map5'] | temp['Map6']
            if 'Map8' in temp:
                d['Node3'] = temp['Map8'] | temp['Map9']
            if 'Map11' in temp:
                d['Node4'] = temp['Map11'] | temp['Map12']
            arrows = {
                1225125243: False,
                1134475172: True,
                711622031: True,
                0: '0'
            }
            right = []
            down = []
            for i in [1, 4, 7, 10]:
                right.append(arrows[item['RecipeDerivationMapArrow'][i]])
                down.append(arrows[item['RecipeDerivationMapArrow'][i+13]])
            d['RightArrows'] = right
            d['DownArrows'] = down
            if len(d) == 3:
                if d['RightArrows'] != [False, False, False, False] and d['DownArrows'] != [False, False, False, False]:
                    dic[item['RecipeDerivationMapPositionId']] = d
            else:
                dic[item['RecipeDerivationMapPositionId']] = d
        except Exception as e:
            print('RecipeDerivationMapPosition issue', e, item)

def quest():
    chars = {
        584317799: 'Shallistera',
        2127577318: 'Meruru',
        138954610: 'Plachta',
        791738845: 'Marie',
        982266313: 'Ayesha',
        457018445: 'Ryza',
        150476128: 'Judie',
        122946833: 'Mu',
        1147706116: 'Elie',
        1521954482: 'Viorate',
        1989955504: 'Shallotte',
        1224435727: 'Vayne',
        1991823604: 'Klaudia',
        1483183933: 'Oskar',
        816975935: 'Firis',
        303402902: 'Corneria',
        181805086: 'Logy'
    }
    dic = {}
    hold['QuestReward'] = dic
    j = open_file('QuestReward')
    for item in j['File']['Object']:
        try:
            d = {}
            for i in range(0,3):
                if 'ItemName' in hold['Gift'][item['GiftId'][i]]:
                    d[f'Gift{i+1}'] = hold['Gift'][item['GiftId'][i]]['ItemName']
            dic[item['QuestRewardId']] = d
        except Exception as e:
            print('QuestReward issue', e, item)
    dic = {}
    finalized['quest'] = dic
    j = open_file('QuestQuest')
    for item in j['File']['Object']:
        try:
            d = {}
            if 'QuestRewardId' in item:
                d = d | localize[item['MessageNameId']]
                d['desc'] = localize[item['MessageDescId']]['text_ENG']
                d = d | hold['QuestReward'][item['QuestRewardId']]
                if 'Gift1' in d:
                    dic[item['QuestQuestId']] = d
                d['Char'] = chars[item['UnknownId1']] if item['UnknownId1'] in chars else item['UnknownId1']
                d['Flag'] = item['Flag']
        except Exception as e:
            print('QuestQuest issue', e, item)

def shop():
    dic = {}
    finalized['GiftTraitTable'] = dic
    j = open_file('GiftTraitTable')
    for item in j['File']['Object']:
        try:
            d = {}
            copy_keys(d, item, ['GiftTraitTableId', 'Numbers1', 'Numbers2', 'TraitIds'])
            for i in range(0,10):
                if item['TraitIds'][i]:
                    d[f'TraitName{i}'] = finalized['trait'][item['TraitIds'][i]]['text_ENG']
            dic[item['GiftTraitTableId']] = d
        except Exception as e: # some issues expected
            pass #print('GiftTraitTable issue', e)
    dic = {}
    hold['GiftTraitLotteryDataTable'] = dic
    j = open_file('GiftTraitLotteryDataTable')
    for item in j['File']['Object']:
        try:
            d = {}
            copy_keys(d, item, ['Numbers1', 'Numbers2',
                'GiftTraitTableId1', 'GiftTraitTableId2', 'GiftTraitTableId3',
                'GiftTraitTableId4', 'GiftTraitTableId5'])
            if item['GiftTraitTableId1'] and not item['GiftTraitTableId2']:
                d['GradeMin'] = finalized['GiftTraitTable'][d['GiftTraitTableId1']]['Numbers1'][0]
                d['GradeMax'] = finalized['GiftTraitTable'][d['GiftTraitTableId1']]['Numbers1'][1]
            dic[item['GiftTraitLotteryDataTableId']] = d
        except Exception as e:
            print('GiftTraitLotteryDataTable issue', e)
    dic = {}
    hold['Gift'] = dic
    j = open_file('Gift')
    for item in j['File']['Object']:
        try:
            d = {}
            copy_keys(d, item, ['LevelMin', 'LevelMax', 'TraitId1', 'TraitId2'])
                #'GiftTraitLotteryDataTableId', 'GiftColorId1', 'GiftColorId2'])
            if item['ItemId']:
                d['ItemId'] = item['ItemId']
                d['ItemName'] = finalized['item'][item['ItemId']]['text_ENG']
            if item['TraitId1']:
                d['TraitName1'] = finalized['trait'][item['TraitId1']]['text_ENG']
            if item['TraitId2']:
                d['TraitName2'] = finalized['trait'][item['TraitId2']]['text_ENG']
            if item['GiftTraitLotteryDataTableId']:
                #print(hold['GiftTraitLotteryDataTable'][item['GiftTraitLotteryDataTableId']])
                if 'GradeMin' in hold['GiftTraitLotteryDataTable'][item['GiftTraitLotteryDataTableId']]:
                    d['GradeMin'] = hold['GiftTraitLotteryDataTable'][item['GiftTraitLotteryDataTableId']]['GradeMin']
                    d['GradeMax'] = hold['GiftTraitLotteryDataTable'][item['GiftTraitLotteryDataTableId']]['GradeMax']
                else:
                    d = d | hold['GiftTraitLotteryDataTable'][item['GiftTraitLotteryDataTableId']].copy()
            dic[item['GiftId']] = d
        except Exception as e:
            print('Gift issue', e, item)
    dic = {}
    finalized['NpcShopMerchandise'] = dic
    j = open_file('NpcShopMerchandise')
    for item in j['File']['Object']:
        shops = {
            601760113: 442483321,
            1162942655: 1590451952,
            870832861: 265721898,
            1318706988: 841588105,
            1463653524: 1000603297,
            1974527760: 1645489886,
            1488394673: 0,
            0: 0,
        }
        try:
            d = {}
            copy_keys(d, item, ['Price', 'Limited', 'UnlockFlagId',
                'Unknown1'])
            if item['ItemId']:
                d['ItemId'] = item['ItemId']
                d['ItemName'] = finalized['item'][item['ItemId']]['text_ENG']
            d = d | localize[shops[item['Shop']]].copy()
            d = d | hold['Gift'][item['GiftId']].copy()
            dic[item['NpcShopMerchandiseId']] = d
        except:
            print('NpcShopMerchandise issue', item)

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

def enemy():
    dic = {}
    hold['DisorderProbability'] = dic
    j = open_file('DisorderProbability')
    for item in j['File']['Object']:
        try:
            d = {}
            copy_keys(d, item, ['AilRes1', 'AilRes2', 'AilRes3', 'AilRes4',
                'AilRes5', 'AilRes6', 'AilRes7', 'AilRes8'])
            dic[item['AilmentResistanceId']] = d
        except:
            print('DisorderProbability issue', item)
    dic = {}
    hold['ElementResistance'] = dic
    j = open_file('ElementResistance')
    for item in j['File']['Object']:
        try:
            d = {}
            copy_keys(d, item, ['ElemRes1', 'ElemRes2', 'ElemRes3', 'ElemRes4',
                'ElemRes5', 'ElemRes6'])
            dic[item['ElementResistanceId']] = d
        except:
            print('ElementResistance issue', item)
    dic = {}
    hold['EnemyBaseInfo'] = dic
    j = open_file('EnemyBaseInfo')
    for item in j['File']['Object']:
        try:
            d = {}
            #copy_keys(d, item, ['EnemyBaseInfoId']) #, 'Floats1', 'Floats2', 'Unknown1', 'Unknown2', 'EnemySizeTypeId', 'Flag',])
            d = d | localize[item['NameStringId']].copy()
            d['FlavorText'] = hold['EnemyFlavorText'][item['FlavorTextId']]
            d['Race'] = finalized['race'][item['EnemyKindId']]['text_ENG']
            dic[item['EnemyBaseInfoId']] = d
        except:
            print('EnemyBase issue', item)
    dic = {}
    hold['DropGiftTable'] = dic
    j = open_file('DropGiftTable')
    for item in j['File']['Object']:
        try:
            d = {}
            for i in range(0,5):
                if item['GiftIds'][i]:
                    d[f'Gift{i}'] = hold['Gift'][item['GiftIds'][i]]
            dic[item['DropGiftTableId']] = d
        except:
            print('DropGiftTable issue', item)
    dic = {}
    hold['DropRewardTable'] = dic
    j = open_file('DropRewardTable')
    for item in j['File']['Object']:
        try:
            d = {}
            for i in range(0,5):
                if item['GiftIds'][i]:
                    d[f'Gift{i}'] = hold['Gift'][item['GiftIds'][i]]
            dic[item['DropRewardTableId']] = d
        except:
            print('DropRewardTable issue', item)
    dic = {}
    finalized['EnemyLibraryInfo'] = dic
    j = open_file('EnemyLibraryInfo')
    for item in j['File']['Object']:
        try:
            d = {}
            copy_keys(d, item, ['Number', 'Number2', 'EnemyLibraryInfoId'])
            dic[item['EnemyLibraryInfoId']] = d
        except Exception as e:
            print('EnemyLibraryInfo issue', e)
    dic = {}
    hold['EnemyDataBase'] = dic
    j = open_file('EnemyDataBase')
    for item in j['File']['Object']:
        try:
            d = {}
            copy_keys(d, item, ['Flag1', 'Integer', 'Flag2', 'Decimal1', 'Unknown4', 'Integer2', 'Decimal2', 'Integer3',])
            d = d | hold['EnemyBaseInfo'][item['EnemyBaseInfoId']].copy()
            d = d | hold['ElementResistance'][item['ElementResistanceId']]
            d = d | hold['DisorderProbability'][item['DisorderProbabilityId']]
            for i in range(0,5):
                if f'Gift{i}' in hold['DropRewardTable'][item['DropRewardTableId']]:
                    d[f'DropReward{i}'] = hold['DropRewardTable'][item['DropRewardTableId']][f'Gift{i}']
                if f'Gift{i}' in hold['DropGiftTable'][item['DropGiftTableId']]:
                    d[f'DropGift{i}'] = hold['DropGiftTable'][item['DropGiftTableId']][f'Gift{i}']

            dic[item['EnemyDataBaseId']] = d
            thing = finalized['EnemyLibraryInfo'][item['EnemyLibraryInfoId']]
            if 'text_ENG' not in thing:
                finalized['EnemyLibraryInfo'][item['EnemyLibraryInfoId']] = thing | d.copy()
            else:
                for i in range(0,5):
                    if f'DropGift{i}' in d and f'DropGift{i}' not in thing:
                        finalized['EnemyLibraryInfo'][item['EnemyLibraryInfoId']][f'DropGift{i}'] = d[f'DropGift{i}']

        except Exception as e:
            print('EnemyBase issue', e)


def area():
    dic = {}
    hold['GimEnemy'] = dic
    j = open_file('GimEnemy')
    for item in j['File']['Object']:
        try:
            d = {}
            for i in range(1, 6):
                if item[f'EnemyDataBaseId{i}']:
                    d[f'EnemyName{i}'] = hold['EnemyDataBase'][item[f'EnemyDataBaseId{i}']]['text_ENG']
            dic[item['GimEnemyId']] = d
        except Exception as e:
            print('GimEnemy issue', e, item)
    dic = {}
    hold['GimGathering'] = dic
    j = open_file('GimGathering')
    for item in j['File']['Object']:
        try:
            d = {}
            match item['ExploreEquipTypeId']:
                case 1682790261: d['GatherType'] = 'Bug Net'
                case 1192236958: d['GatherType'] = 'Gather'
                case 87204698: d['GatherType'] = 'Axe'
                case 1053834970: d['GatherType'] = 'Sickle'
                case _: d['GatherType'] = item['ExploreEquipTypeId']
            for i in range(1, 4):
                if 'ItemName' in hold['Gift'][item[f'GiftId{i}']]:
                    d[f'ItemName{i}'] = hold['Gift'][item[f'GiftId{i}']]['ItemName']
            dic[item['GimGatheringId']] = d
        except Exception as e:
            print('GimGathering issue', e, item)
    dic = {}
    hold['GimTreasure'] = dic
    j = open_file('GimTreasure')
    for item in j['File']['Object']:
        try:
            d = {}
            if 'ItemName' in hold['Gift'][item[f'GiftId']]:
                d[f'ItemName1'] = hold['Gift'][item[f'GiftId']]['ItemName']
            d['GatherType'] = 'Chest'
            dic[item['TreasureId']] = d
        except Exception as e:
            print('GimTreasure issue', e, item)
    dic = {}
    dic2 = {}
    finalized['areas'] = dic2
    hold['FieldStageInfo'] = dic
    j = open_file('FieldStageInfo')
    for item in j['File']['Object']:
        try:
            d = {}
            copy_keys(d, item, ['Index'])
            dic2[item['FieldStageInfoId']] = d | localize[item['MessageId']]
            d['Area'] = localize[item['MessageId']]['text_ENG']
            dic[item['FieldStageInfoId']] = d
        except Exception as e:
            print('FieldStageInfo issue', e)
    dic = {}
    dic2 = {}
    finalized['enemylocations'] = dic2
    finalized['gather'] = dic
    j = open_file('FieldStageData')
    for item in j['File']['Object']:
        try:
            if item['GimmickTypeId'] == 2059211439:
                d = {}
                d = d | hold['FieldStageInfo'][item['FieldStageInfoId']]
                d = d | hold['GimGathering'][item['GimId']]
                dic[item['FieldStageDataId']] = d
            if item['GimmickTypeId'] == 133625395: # chest
                d = {}
                d = d | hold['FieldStageInfo'][item['FieldStageInfoId']]
                d = d | hold['GimTreasure'][item['GimId']]
                dic[item['FieldStageDataId']] = d
            if item['GimmickTypeId'] == 214669337: #enemy
                d = {}
                d = d | hold['FieldStageInfo'][item['FieldStageInfoId']]
                d = d | hold['GimEnemy'][item['GimId']]
                dic2[item['FieldStageDataId']] = d
        except Exception as e:
            print('FieldStageData issue', e)
    dic = {}
    dic2 = finalized['areas']
    hold['DungeonBase'] = dic
    j = open_file('DungeonBase')
    for item in j['File']['Object']:
        try:
            d = {}
            d['Index'] = -item['Index'] - 1
            dic2[item['DungeonBaseId']] = d | localize[item['DungeonNameId']]
            d['Area'] = localize[item['DungeonNameId']]['text_ENG']
            dic[item['DungeonBaseId']] = d
        except Exception as e:
            print('DungeonBase issue', e)
    dic = finalized['gather']
    j = open_file('DungeonGimGatheringData')
    for item in j['File']['Object']:
        try:
            d = {}
            d = d | hold['GimGathering'][item['GimGatheringId']]
            d = d | hold['DungeonBase'][item['DungeonBaseId']]
            d['Floors'] = item['Numbers'][0:2]
            dic[item['DungeonGimGatheringDataId']] = d
        except Exception as e:
            print('DungeonGimGatheringData issue', e, item)
    dic = finalized['enemylocations']
    j = open_file('DungeonEnemyData')
    for item in j['File']['Object']:
        try:
            d = {}
            d = d | hold['GimEnemy'][item['GimEnemyId']]
            d = d | hold['DungeonBase'][item['DungeonBaseId']]
            d['Floors'] = item['Numbers'][0:2]
            dic[item['DungeonEnemyDataId']] = d
        except Exception as e:
            print('DungeonEnemyData issue', e, item)

def other_text():
    dic = {}
    finalized['neat_localization_strings'] = dic
    ids = [
        #1039643431,
        1874449842, # Item related
        415163688,
        2118667106,
        1028144855,
        1246694977,
        2021223619, # Colors
        259939413,
        971207224,
        1323582114,
        672328932,
        1836057449, # Quest
        1303098226, # Chest
        697448138, # Story
        890260827, # Orders
        1468509602, # Town Requests
        631416882, # Fairies
        1838570837, # Characters
        1709239228,
        888758062,
        1781926429,
        1734538602,
        1355465651,
        1083239891,
        1462635682,
        1872409296,
        657501351,
        1454754738,
        317905507,
        282862935,
        1458645275,
        1444527967,
        1762636429,
        1725636568,
        1989637904,
        2089197013,
        1816378668,
        1827926219,
        380421561,
        652826947,
        1388433053,
        2056829506,
        1673138353,
        1954378129,
        1492300145,
        380399558,
        577407231,
        1045685295,
        1428103756,
        1095721156,
        880618073,
        1926072056,
        2142622195,
        121456110,
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
shop()
quest()
enemy()
area()
other_text()
export_csv()
