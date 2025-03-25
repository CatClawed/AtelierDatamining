import json, csv, os
#from PIL import Image
from matplotlib import image
from matplotlib import pyplot as plt

languages = ['eng', 'jpn', 'chs', 'cht', 'deu', 'fra', 'kor', 'rus', 'spa']
localize = {}
fixed_data = 'Data/pak/master/cmn/fixed_data/'
map_data = 'Data/pak/master/cmn/placementgimmick/'
finalized = {}
hold = {}
enc = 'utf-8-sig'

def clean_text(text, lang):
    if lang in ['chs', 'cht', 'kor', 'jpn']:
        text = text.replace('<CR>', '')
    else:
        text = text.replace('<CR>', ' ')
    for rep in ['<CLEG>', '<CLNR>', '<CLGR>', '<CLYL>', '<CLRE>', '<CLBL>']:
        text = text.replace(rep, '')
    #if '<' in text and lang == 'eng':
    #    print(text)
    return text

def get_localization():
    for lang in languages:
        with open(f'Data/pak/master/{lang}/fixed_data/message/message.json', encoding=enc) as f:
            j = json.load(f)
            for m in j['message_message']:
                try:
                    entry = localize[m['NAME_LABEL']]
                except:
                    entry = {}
                    localize[m['NAME_LABEL']] = entry
                entry[f'text_{lang}'] = clean_text(m['MESSAGE'], lang)

def copy_keys(dest, source, ls):
    for l in ls:
        if l in source:
            dest[l] = source[l]

def kind():
    with open(fixed_data+'item/item_kind.json', encoding=enc) as f:
        obj = json.load(f)
        dic = {}
        finalized['kind'] = dic
        for item in obj['item_item_kind']:
            d = localize[item['nameID']]
            d['tag'] = item['item_kind_tag']
            d['image_no'] = item['image_no']
            dic[item['item_kind_tag']] = d

def material():
    with open(fixed_data+'item/item_material.json', encoding=enc) as f:
        obj = json.load(f)
        dic = {}
        finalized['material'] = dic
        for item in obj['item_item_material']:
            d = localize[item['name_id']]
            d['tag'] = item['item_material_id']
            d['image_no'] = item['image_no']
            dic[item['item_material_id']] = d

def category():
    with open(fixed_data+'item/item_category.json', encoding=enc) as f:
        obj = json.load(f)
        dic = {}
        finalized['category'] = dic
        for item in obj['item_item_category']:
            d = localize[item['nameID']]
            d['tag'] = item['item_category_tag']
            d['image_no'] = item['ImageNo']
            dic[item['item_category_tag']] = d

def trait():
    dic = {}
    finalized['trait'] = dic
    lib = {}
    nolevel = []
    with open(fixed_data+'trait/trait_nolevel.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['trait_trait_nolevel']:
            if 'trait_nameid' in item:
                nolevel.append(item['trait_nameid'])

    with open(fixed_data+'library/library_trait.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['library_library_trait']:
            d = {}
            if 'description_str' in item:
                d = localize[item['description_str']].copy()
                for lang in languages:
                    d[f'desc_{lang}'] = d.pop(f'text_{lang}')
            d['disp_flag'] = item['disp_flag']
            if 'description_str_far' in item:
                for lang in languages:
                    d[f'desc2_{lang}'] = localize[item['description_str_far']][f'text_{lang}']
            lib[item['item_trait_tag']] = d

    with open(fixed_data+'item/item_trait.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['item_item_trait']:
            if 'nameID' in item:
                d = localize[item['nameID']].copy()
                for k, v in lib[item['item_id']].items():
                    if 'desc_' in k:
                        d[k] = v.replace('<NUM0>', str(item['lv_min_rand_range_min'][0])).replace('<NUM1>',str(item['lv_min_rand_range_min'][1]))
                    elif 'desc2' in k:
                        d[k] = v.replace('<NUM0>', str(item['lv_min_rand_range_min'][2])).replace('<NUM1>',str(item['lv_min_rand_range_min'][3]))
                    else:
                        d[k] = v
            else:
                d = {}
                try:
                    d['disp_flag'] = lib[item['item_id']]['disp_flag']
                except:
                    d['disp_flag'] = 0
            copy_keys(d, item, ['item_id', 'imageNo', 'min_rarity', 'max_level',
                                'wep', 'arm', 'acc', 'atk', 'heal', 'supEne', 'subPar',
                                'grade_min_value', 'grade_max_value',
                                'lv_min_rand_range_min', 'lv_min_rand_range_max',
                                'lv_max_rand_range_min', 'lv_max_rand_range_max',
                                'trait_base', 'hash', 'item_trait_table_tag',
                                ]
                      )
            if 'item_trait_table_tag' in d:
                temp = d['item_trait_table_tag'][-4:]
                d['item_trait_table_tag'] = temp.lstrip('0') if temp != '0000' else 0

            if item['element_flag'][0] == True:
                d['fire'] = True
            elif item['element_flag'][1] == True:
                d['ice'] = True
            elif item['element_flag'][2] == True:
                d['bolt'] = True
            elif item['element_flag'][3] == True:
                d['air'] = True

            if item['item_id'] in nolevel:
                d['no_level'] = True

            dic[item['item_id']] = d

    with open(fixed_data+'trait/trait_combination.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['trait_trait_combination']:
            d = dic[item['trait_nameid']]
            for i in range(0,4):
                d[f'combo_{i+1}'] = dic[item['material'][i]]['text_eng']

def effect():
    dic = {}
    finalized['effect'] = dic
    lib = {}

    with open(fixed_data+'library/library_effect.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['library_library_effect']:
            d = {}
            copy_keys(d, item, ['page_type_flag', 'disp_flag'])
            lib[item['item_effect_tag']] = d

    desc_attr = []
    desc_text = []

    with open(fixed_data+'library/library_effect_text_table.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['library_library_effect_text_table']:
            d = {}
            try:
                for lang in languages:
                    d[f'desc_{lang}'] = localize[item['id']][f'text_{lang}']
            except:
                pass
                #print("error:", item['id'])
            desc_text.append(d)
            attr = {}
            attr['act_tag'] = item['act_tags']
            attr['hash_name'] = item['act_param_hashes']
            attr['att_tag'] = item['attributes']
            desc_attr.append(attr)

    dic2 = {}
    hold['item_effect_table'] = dic2
    max_lv = {}

    with open(fixed_data+'item/item_effect_table.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['item_item_effect_table']:
            d = {}
            d2 = {}
            if item['add_effect'][0] != '':
                d['max_lv'] = max(i for i in item['effect_level'] if i != '')
                max_lv[item['add_effect'][0]] = d
                d2['max_lv'] = d['max_lv']
                d2['effect_tag'] = item['add_effect'][0]
                d2['effect_name'] = localize[item['nameID']]['text_eng']

            dic2[item['item_effect_table_tag']] = d2

    with open(fixed_data+'item/item_effect.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['item_item_effect']:
            d = {}
            if 'nameID' in item:
                try:
                    d = localize[item['nameID']]
                except:
                    pass
                    #print("error:", item['nameID'])
            if item['item_id'] in lib:
                d = d | lib[item['item_id']]
            else:
                d['disp_flag'] = -1
                d['page_type_flag'] = -1
            copy_keys(d, item, ['item_id', 'has_range', 'att_tag', 'act_tag',
                    'prm1_lv_min_rand_range_min', 'prm1_lv_min_rand_range_max',
                    'prm1_lv_max_rand_range_min', 'prm1_lv_max_rand_range_max',
                    'prm1_lv_max_rand_range_max', 'prm2_lv_min_rand_range_max',
                    'prm2_lv_max_rand_range_min', 'prm2_lv_max_rand_range_max',
                    'hash_name'
                ])

            for j in range(0,2):
                mat = {}
                mat['act_tag'] = d['act_tag'][0:4] if j == 0 else d['act_tag'][4:]
                mat['hash_name'] = d['hash_name'][0:4] if j == 0 else d['hash_name'][4:]
                m = []
                for i in range(0,4):
                    match d['att_tag'][i]:
                        case 'ATT_FIRE':
                            m.append(2)
                        case 'ATT_ICE':
                            m.append(3)
                        case 'ATT_THUN':
                            m.append(4)
                        case 'ATT_WIND':
                            m.append(5)
                        case _:
                            m.append(-1)
                mat['att_tag'] = m

                try:
                    if 'text_eng' in d:
                        ind = desc_attr.index(mat)
                        if ind > 0:
                            for lang in languages:
                                txt = desc_text[ind][f'desc_{lang}']
                                offset = 0 if j == 0 else 4
                                for i in range(0,4):
                                    txt = txt.replace(f'<NUM{i*2}>', str(d['prm1_lv_min_rand_range_min'][i+offset]))
                                    txt = txt.replace(f'<NUM{i*2+1}>', str(d['prm2_lv_min_rand_range_max'][i+offset]))

                                if j == 0:
                                    d[f'desc_{lang}'] = txt
                                else:
                                    d[f'desc2_{lang}'] = txt
                except Exception as e:
                    #print(e)
                    pass

            if item['item_id'] in max_lv:
                d = d | max_lv[item['item_id']]

            dic[item['item_id']] = d

def item():
    lib = {}
    with open(fixed_data+'library/library_item.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['library_library_item']:
            d = {}
            if 'description_str' in item:
                d = localize[item['description_str']].copy()
                for lang in languages:
                    d[f'desc_{lang}'] = d.pop(f'text_{lang}')
                d['disp_flag'] = item['disp_flag']
            lib[item['item_tag']] = d

    dic = {}
    hold['item_wep_status'] = dic
    with open(fixed_data+'item/item_wep_status.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['item_item_wep_status']:
            d = {}
            copy_keys(d, item, ['atk', 'def', 'spd'])
            dic[item['item_id']] = d

    dic = {}
    hold['item_use'] = dic
    with open(fixed_data+'item/item_use.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['item_item_use']:
            d = {}
            copy_keys(d, item, ['use_num', 'mana', 'cool_time', 'target_type'])
            d['aoe'] = item['range'] # needs renaming to merge
            dic[item['item_tag']] = d

    dic = {}
    finalized['item'] = dic
    with open(fixed_data+'item/item.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['item_item']:
            d = {}
            if 'nameID' in item:
                try:
                    d = localize[item['nameID']]
                except Exception as e:
                    pass
                    #print(e)
            if item['item_id'] in lib:
                d = d | lib[item['item_id']]
            copy_keys(d, item, ['item_id', 'imgNo', 'multiImgNo', 'lv', 'duplicate_cost', 'range', 'convert_material_num', 'exchange_rate'])

            for i in range(0,4):
                match i:
                    case 0:
                        d['fire'] = item['has_element'][i]
                    case 1:
                        d['ice'] = item['has_element'][i]
                    case 2:
                        d['bolt'] = item['has_element'][i]
                    case 3:
                        d['air'] = item['has_element'][i]

            cat = []
            for c in item['category']:
                if c != '':
                    cat.append(finalized['category'][c]['text_eng'])
            d['category']=cat

            mat = []
            for m in item['convert_material']:
                if m != '':
                    mat.append(finalized['material'][m]['text_eng'])
            d['material']=mat

            if item['item_id'] in hold['item_wep_status']:
                d = d | hold['item_wep_status'][item['item_id']]
            if item['item_id'] in hold['item_use']:
                d = d | hold['item_use'][item['item_id']]

            dic[item['item_id']] = d

    # item status
    dic = {}
    finalized['item_status'] = dic
    with open(fixed_data+'item/item_status.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['item_item_status']:
            d = {}
            d['status_id'] = item['status_tag']
            try:
                d['text_eng'] = finalized['item'][item['item_id']]['text_eng']
            except:
                pass
                #print(finalized['item'][item['item_id']])
            copy_keys(d, item, ['item_id', 'quality', 'effect', 'effect_lv'])

            names = []
            for e in item['effect']:
                if e:
                    names.append(finalized['effect'][e]['text_eng'])
            d['effect_names'] = names

            match item['rank']:
                case 0: d['rank'] = 'E'
                case 1: d['rank'] = 'D'
                case 2: d['rank'] = 'C'
                case 3: d['rank'] = 'B'
                case 4: d['rank'] = 'A'
                case 5: d['rank'] = 'S'

            dic[item['status_tag']] = d

    # recipe recall reward
    dic = {}
    finalized['recipe_recall_reward'] = dic

    with open(fixed_data+'recipe_recall/recipe_recall_reward.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['recipe_recall_recipe_recall_reward']:
            d = {}
            for lang in languages:
                d[f'text_{lang}'] = localize[item['recipe_recall_reward_brief_text']][f'text_{lang}']
                d[f'desc_{lang}'] = localize[item['recipe_recall_reward_text']][f'text_{lang}']
            dic[item['recipe_recall_reward_tag']] = d


    dic = {}
    hold['recipe_recall_base'] = dic

    with open(fixed_data+'recipe_recall/recipe_recall_base.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['recipe_recall_recipe_recall_base']:
            d = {}
            copy_keys(d, item, ['reward_prm1','get_scenario_flag','unlock_scenario_flag',
                      'residue_cost_fire', 'residue_cost_ice', 'residue_cost_thunder',
                      'residue_cost_air','reward_prm1'])

            rewards = []
            for r in item['reward_tag']:
                if r:
                    rewards.append(finalized['recipe_recall_reward'][r]['text_eng'])
            d['reward'] = rewards

            dic[item['recipe_recall_tag']] = d


    # item recipe
    dic = {}
    finalized['recipe'] = dic

    with open(fixed_data+'item/item_recipe.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['item_item_recipe']:
            d = {}

            # mix_reward_tag
            # this tag is where all the effect thresholds are, needs mix/mix_reward.json
            # problem: manual fetching the non-effect strings (reduce item cooldown by X etc)
            # and substituting all the params. effort to payoff ratio seems bad.
            copy_keys(d, item, ['item_tag', 'make_num', 'obtain_skill_point', 'recipe_category','material_tag'])

            d['text_eng'] = finalized['item'][item['item_tag']]['text_eng']
            ing = []
            for i in range(0,4):
                if item['material_tag'][i]:
                    if item['is_category'][i]:
                        ing.append(finalized['category'][item['material_tag'][i]]['text_eng'])
                    else:
                        ing.append(finalized['item'][item['material_tag'][i]]['text_eng'])
                match i:
                    case 0: d['fire'] = item['has_element'][i] if item['has_element'][i] else False
                    case 1: d['ice'] = item['has_element'][i] if item['has_element'][i] else False
                    case 2: d['bolt'] = item['has_element'][i] if item['has_element'][i] else False
                    case 3: d['air'] = item['has_element'][i] if item['has_element'][i] else False
            d['materials'] = ing

            effs = []
            for eff in item['effect_table']:
                if eff:
                    effs.append(hold['item_effect_table'][eff])
            d['effects'] = effs

            d = d | hold['recipe_recall_base'][item['recipe_recall_tag']]

            dic[item['item_recipe_tag']] = d

def monster():
    """
    monster_race: ignoring all the stat modifiers, is_old, single turn
    monster_param: elements, ailment resist, default lv and stat adjustments?
    monster: ignoring a lot of fields
    """
    lib = {}
    with open(fixed_data+'library/library_monster.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['library_library_monster']:
            d = {}
            if 'description_str' in item:
                d = localize[item['description_str']].copy()
                for lang in languages:
                    d[f'desc_{lang}'] = d.pop(f'text_{lang}')
            copy_keys(d, item, ['star_hp', 'star_atk', 'star_def', 'star_spd', 'disp_flag'])
            lib[item['monster_tag']] = d

    dic = {}
    finalized['monster_race'] = dic
    with open(fixed_data+'monster/monster_race.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['monster_monster_race']:
            d = {}
            if 'text_id' in item:
                try:
                    d = localize[item['text_id']]
                except Exception as e:
                    pass
                    #print(e)
            copy_keys(d, item, ['icon_no', 'monster_race_id'])
            dic[item['monster_race_id']] = d

    dic = {}
    hold['monster_param'] = dic
    with open(fixed_data+'monster/monster_param.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['monster_monster_param']:
            d = {}
            copy_keys(d, item, ['break_symbol', 'status_resist', 'break_weak_phys'])
            d['fire'] = item['resist_fire'].split('_')[-1] if 'resist_fire' in item else ''
            d['ice'] = item['resist_ice'].split('_')[-1] if 'resist_ice' in item else ''
            d['bolt'] = item['resist_thun'].split('_')[-1] if 'resist_thun' in item else ''
            d['air'] = item['resist_wind'].split('_')[-1] if 'resist_wind' in item else ''
            dic[item['monster_param_id']] = d

    dic = {}
    hold['monster_drop'] = dic
    # There are three drop slots, but only one ever seems to be used.
    # lv is always 20 and 50, not sure what this is.
    # trait_num and num appears to always be 1
    # why are the drop tables the same
    with open(fixed_data+'monster/monster_drop.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['monster_monster_drop']:
            d = {}
            copy_keys(d, item, ['piece_rate', 'trait_id', 'trait_rate', 'table_id'])
            if 'trait_id' in item:
                d['trait'] = finalized['trait'][item['trait_id']]['text_eng']
            if item['rate'][0]:
                d['rate'] = item['rate'][0]
                d['rare_rate'] = item['rare_rate'][0]
                d['piece'] = item['reverberation_piece_collect_info'].split('_')[-3]
                d['drop'] = finalized['item'][item['item_id'][0]]['text_eng']
                d['drop_tag'] = item['item_id'][0]
                d['rare_drop'] = finalized['item'][item['rare_item_id'][0]]['text_eng']
                d['rare_drop_tag'] = item['rare_item_id'][0]
            dic[item['monster_drop_id']] = d

    dic = {}
    finalized['monster'] = dic
    with open(fixed_data+'monster/monster.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['monster_monster']:
            d = {}
            if 'monster_name_id' in item:
                try:
                    d = localize[item['monster_name_id']].copy()
                except Exception as e:
                    pass
                    #print(e)
            if item['monster_id'] in lib:
                d = d | lib[item['monster_id']]
            if item['monster_id'] in hold['monster_param']:
                d = d | hold['monster_param'][item['monster_id']]
            copy_keys(d, item, ['img_no', 'monster_id'])
            d['size'] = item['size_id'].split('_')[-1] if 'size_id' in item else ''
            if 'race_id' in item:
                d['race'] = finalized['monster_race'][item['race_id']]['text_eng']
            d = d | hold['monster_drop'][item['monster_id']]
            dic[item['monster_id']] = d


def item_data():
    kind()
    category()
    material()
    trait()
    effect()
    item()

def building():
    dic = {}
    finalized['item_craft_furniture_category'] = dic
    with open(fixed_data+'craft/item_craft_furniture_category.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['craft_item_craft_furniture_category']:
            d = {}
            if 'text_id' in item:
                try:
                    d = localize[item['text_id']]
                except Exception as e:
                    pass
                    #print(e)
            copy_keys(d, item, ['item_craft_furniture_recipe_category_id', 'image_no'])
            dic[item['item_craft_furniture_recipe_category_id']] = d

    dic = {}
    hold['housing_comfort_reward'] = dic
    with open(fixed_data+'housing/housing_comfort_reward.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['housing_housing_comfort_reward']:
            d = {}
            if 'param_hash' in item:
                d['reward'] = finalized['item'][item['param_hash']]['text_eng']

            dic[item['housing_comfort_reward_id']] = d

    # housing object
    # housing object category? for img no?

    dic = {}
    hold['housing_object'] = dic
    with open(fixed_data+'housing/housing_object.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['housing_housing_object']:
            d = {}
            copy_keys(d, item, ['image_no', 'comfort_level', 'cost', 'category'])
            dic[item['item_id']] = d


    dic = {}
    finalized['housing_area'] = dic
    with open(fixed_data+'housing/housing_area.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['housing_housing_area']:
            d = {}
            copy_keys(d, item, ['housing_area_id', 'comfort_goal'])
            reward = []
            if 'comfort_reward' in item:
                for r in item['comfort_reward']:
                    if r:
                        if 'reward' in hold['housing_comfort_reward'][r]:
                            reward.append(hold['housing_comfort_reward'][r]['reward'])
                        else:
                            reward.append('')
                    else:
                        reward.append('')
            d['comfort_reward'] = reward

            dic[item['housing_area_id']] = d

    dic = {}
    finalized['item_craft_recipe'] = dic
    with open(fixed_data+'craft/item_craft_recipe.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['craft_item_craft_recipe']:
            d = {}
            d['name'] = finalized['item'][item['item_tag']]['text_eng']
            for i in range(0,4):
                if f'need_item_{i}' in item:
                    d[f'need_item_{i}'] = finalized['material'][item[f'need_item_{i}']]['text_eng']
            copy_keys(d, item, ['item_craft_recipe_id', 'create_senario_flag', 'energy_core_cost', 'create_num_at_once', 'need_num_0', 'need_num_1', 'need_num_2', 'need_num_3'])
            if item['item_tag'] in hold['housing_object']:
                d = d | hold['housing_object'][item['item_tag']]

            dic[item['item_craft_recipe_id']] = d

def gather_nodes():
    dic = {}
    hold['item_craft_to_recipe_name'] = dic
    with open(fixed_data+'craft/item_craft_to_recipe_name.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['craft_item_craft_to_recipe_name']:
            dic[item['recipe_name']] = {
                "item_id": item['item_tag'],
                "item": finalized['item'][item['item_tag']]['text_eng']
            }

    dic = {}
    hold['chapter_all'] = dic
    with open('Data/pak/master/cmn/gamedata/scenario/chapter_all.json', encoding=enc) as f:
        obj = json.load(f)
        for chap in obj.values():
            for item in chap:
                if 'pp_type' in item:
                    if item['pp_type'] == 'get_craft_recipe':
                        try:
                            dic[int(item['trigger_param'])] = hold['item_craft_to_recipe_name'][item['pp_param']]
                        except:
                            dic[int(item['trigger_param'])] = {'item': "DUMMY LOL"}

    dic = {}
    hold['gimmick_event'] = dic
    with open(fixed_data+'gimmick/gimmick_event.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['gimmick_gimmick_event']:
            if item['scenario'] in hold['chapter_all']:
                dic[item['tag']] = hold['chapter_all'][item['scenario']]



    dic = {}
    hold['ex_item_group'] = dic
    with open(fixed_data+'collect/ex_item_group.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['collect_ex_item_group']:
            d = {}
            #ignoring rank, quality, priority, level, rank
            copy_keys(d, item, ['item_id', 'potential_0'])
            if 'item_id' in d:
                if d['item_id'] != 'ITEM_OTHER_01':
                    d['item'] = finalized['item'][d['item_id']]['text_eng']
            if 'potential_0' in d:
                d['trait'] = finalized['trait'][d['potential_0']]['text_eng']

            if item['group'] in dic:
                dic[item['group']].append(d)
            else:
                dic[item['group']] = [d]

    hold['gather'] = {}
    with open(fixed_data+'collect/ex_collect_info.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['collect_ex_collect_info']:
            hold['gather'][item['place_id']] = hold['ex_item_group'][item['group']]

    dic = {}
    hold['common_item_group'] = dic
    with open(fixed_data+'collect/common_item_group.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['collect_common_item_group']:
            d = {}
            #ignoring rank, quality, priority, level, rank
            copy_keys(d, item, ['item_id', 'priority'])
            if 'item_id' in d:
                d['item'] = finalized['item'][d['item_id']]['text_eng']

            if item['group'] in dic:
                dic[item['group']].append(d)
            else:
                dic[item['group']] = [d]

    with open(fixed_data+'collect/common_collect_info.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['collect_common_collect_info']:
            if 'group0' in item:
                hold['gather'][item['place_id']] = hold['common_item_group'][item['group0']]

# theoretically normalized, it was guesswork
def get_position(pos):
    pos = pos.split(',')
    return (float(pos[0])-90000)/722000, (float(pos[2])-90000)/297000

def plot(x, z, point='ob'):
    plt.plot(x*8704, z*3584, point)

def get_item(item, note, location, label):
    d = {}
    d['id'] = item['ID']
    d['note'] = note
    d['location'] = location
    d['x'], d['z'] = get_position(item['pos'])
    app = None
    if 'elem' in item:
        for elem in item['elem']:
            if 's_flag' in elem:
                if elem['s_flag']:
                    app = hold['gimmick_event'][elem['s_flag']]
                    break
    try:
        res = hold['gather'][item['param'][0]['v']].copy()
        if app:
            res.append(app)
        d['reward'] = res
        finalized[label][item['ID']] = d
    except Exception as e:
        print(e)

def map():
    exclude = ['jimen', 'housing', 'blend', 'test', 'file_info', 'event_', 'void',
               'env_effect', 'menu', 'quest_', '_npc', 'seamless', 'destructive',
               'district', 'prologue', 'indoor_', '_mana_', 'dummy', 'border',
               'metal_gimmick_area06_gimmick']

    maps = os.listdir(map_data)
    files = []

    for e in exclude:
        for map in maps:
            if e in map:
                files.append(map)
    maps = [m for m in maps if m not in files]
    print(maps)

    gather_nodes()
    finalized['chests'] = {}
    finalized['gather'] = {}

    """
    1157243747 shrine
    1254731747 chest enemy
    1056368472 pressure plate
    1802197613 cube
    685462064 another enemy?
    2366441374 crack rock
    # wtf is this
        3113086705: 'Etc 1',
        3944769136: 'Etc 2',
        1095892315: 'Etc 3',
        2275777035: 'Etc 4',
        685462064: 'NPCs?', ## ???

        4069313403: 'Button',
        1184117056: 'Fast Travel',
        771256160: 'Fishing',
        2725809807: 'NPCs',
    """

    types = {
        4281547523: 'Chest',
        2470424865: 'Minigame Chest',
        1154842166: 'Shoot Chest',
        3376427666: 'Memory Vial',
        685462064: 'Monsters', # needs symbol group and encount group
        2722217191: 'Gather (Hand)',
        805069512: 'Gather (Staff)',
        441698374: 'Gather (Gun)',
        2029820134: 'Monster 2',
    }
    im = image.imread('combined.webp')
    count = 0
    for map in maps:
        with open(map_data+map, encoding=enc) as f:
            obj = json.load(f)
            point = 'og'
            location = ''
            if 'forest' in map or 'submap01' in map:
                point = 'or'
                location = 'Ligneus'
            elif 'rottensea' in map or 'submap5' in map:
                point = 'om'
                location = 'Sivash'
            elif 'metal' in map or 'submap3' in map or 'submap4' in map:
                point = 'oy'
                location = 'Auruma'
            elif 'kingdom' in map or 'castle' in map:
                point = 'ok'
                location = 'Lacuna'
            for item in obj:
                match item['type']:
                    case 4281547523: get_item(item, types[item['type']], location, "chests")
                    case 2470424865: get_item(item, types[item['type']], location, "chests")
                    case 1154842166: get_item(item, types[item['type']], location, "chests")
                    case 2722217191: get_item(item, types[item['type']], location, "gather")
                    case 805069512:  get_item(item, types[item['type']], location, "gather")
                    case 441698374:  get_item(item, types[item['type']], location, "gather")
                """ plotting
                if item['type'] == 2725809807:
                    count += 1
                    pos = item['pos'].split(',')
                    #zplt.plot(float(pos[0]), float(pos[2]), point)
                    plt.plot((float(pos[0])-90000)/722000*8704, (float(pos[2])-90000)/297000*3584, point)
                """


    #print(count)
    #plt.gca().invert_yaxis()
    plt.imshow(im)
    plt.show()


"""
Notes
cmn/placementgimmick - locations I guess. I assume pos is xyz coords, but how do I
map this to a 2D map?

fixed_data/collect/
    common_item_group.json -- groups items (note the group val) and their priority
    common_item_material_group -- the same for materials
    common_collect_info -- the actual gathering node, refers to group numbers and
                           gives ranges on how many of each item/material you can get
                           The place_id tags get referenced in placementgimmick
    adjust_parameter -- no idea. has rank by rank data, it's all the same.
    adjust_parameter_trait -- same as above.
    ex_item_group -- like common item group, seems more specific. Priority 100,
                     exact quality, trait levels, etc. Is this chest stuff?
                     Referred to in scramble.json sometimes as a place_id
    ex_collect_info -- Quantities for the groups. SOmetimes used in field map reward.
    ex_item_material_group -- Not sure where this is used.
                              some ex_collects call for a material_group...
    reverberation collect -- I do not care to comprehend this xd
    reverberation info -- looks like those challenge battles (scramble.json)

"""

def export_csv():
    keys = {
        'trait': [
            'item_id', 'text_eng','desc_eng','desc2_eng','text_jpn','desc_jpn','desc2_jpn','text_chs','desc_chs','desc2_chs','text_cht','desc_cht','desc2_cht','text_deu','desc_deu','desc2_deu','text_fra','desc_fra','desc2_fra','text_kor','desc_kor','desc2_kor','text_rus','desc_rus','desc2_rus','text_spa','desc_spa','desc2_spa', 'imageNo', 'min_rarity', 'max_level',
            'wep', 'arm', 'acc', 'atk', 'heal', 'supEne', 'subPar',
            'grade_min_value', 'grade_max_value',
            'lv_min_rand_range_min', 'lv_min_rand_range_max',
            'lv_max_rand_range_min', 'lv_max_rand_range_max',
            'trait_base', 'hash', 'item_trait_table_tag',
            'fire', 'ice', 'bolt', 'air', 'no_level',
            'combo_1', 'combo_2', 'combo_3', 'combo_4',
            'disp_flag',],
        'effect': [
            'item_id','text_eng','desc_eng','desc2_eng','text_jpn','desc_jpn','desc2_jpn','text_chs','desc_chs','desc2_chs','text_cht','desc_cht','desc2_cht','text_deu','desc_deu','desc2_deu','text_fra','desc_fra','desc2_fra','text_kor','desc_kor','desc2_kor','text_rus','desc_rus','desc2_rus','text_spa','desc_spa','desc2_spa',
            'has_range','att_tag','act_tag','prm1_lv_min_rand_range_min',
            'prm1_lv_min_rand_range_max','prm1_lv_max_rand_range_min',
            'prm1_lv_max_rand_range_max','prm2_lv_min_rand_range_max',
            'prm2_lv_max_rand_range_min','prm2_lv_max_rand_range_max',
            'hash_name','disp_flag','page_type_flag','max_lv'],
        'item': [
            'item_id','text_eng','desc_eng','text_jpn','desc_jpn','text_chs','desc_chs','text_cht','desc_cht','text_deu','desc_deu','text_fra','desc_fra','text_kor','desc_kor','text_rus','desc_rus','text_spa','desc_spa',
            'imgNo', 'multiImgNo', 'lv', 'duplicate_cost', 'range',
            'fire', 'ice', 'bolt', 'air',
            'category', 'material',
            'convert_material_num', 'exchange_rate', 'disp_flag', 'atk', 'def', 'spd',
            'use_num', 'mana', 'cool_time', 'target_type', 'aoe'],
        'monster': [
            'monster_id','text_eng','desc_eng','text_jpn','desc_jpn','text_chs','desc_chs','text_cht','desc_cht','text_deu','desc_deu','text_fra','desc_fra','text_kor','desc_kor','text_rus','desc_rus','text_spa','desc_spa',
            'img_no', 'race',
            'break_symbol','break_weak_phys','fire','ice','bolt','air',
            'star_hp','star_atk','star_def','star_spd','status_resist','disp_flag',
            'rate', 'drop', 'rare_rate', 'rare_drop',
            'trait', 'trait_rate', 'piece', 'piece_rate',
            'table_id', 'drop_tag', 'rare_drop_tag', 'trait_id',
        ],
        'item_craft_recipe': [
            'item_craft_recipe_id', 'name', 'create_senario_flag', 'energy_core_cost', 'create_num_at_once',
            'need_item_0', 'need_num_0', 'need_item_1', 'need_num_1',
            'need_item_2','need_num_2', 'need_item_3','need_num_3',
            'image_no', 'comfort_level', 'cost', 'category',
        ],
        'chests': [
            'id', 'x', 'z', 'reward', 'location', 'note',
        ],
        'gather': [
            'id', 'x', 'z', 'reward', 'location', 'note',
        ],

    }
    for k, v in finalized.items():
        head = keys[k] if k in keys else v[list(v.keys())[0]].keys()
        with open(f'output/{k}.csv', 'w+') as f:
            writer = csv.DictWriter(f, head, delimiter='\t', extrasaction='ignore')
            writer.writeheader()
            for v2 in v.values():
                  writer.writerow(v2)


get_localization()
item_data()
monster()
building()
map()
export_csv()
