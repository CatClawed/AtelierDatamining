import json, os, csv

languages = ['eng', 'jpn', 'chs', 'cht', 'deu', 'fra', 'kor', 'rus', 'spa']
localize = {}
fixed_data = 'Data/pak/master/cmn/fixed_data/'
finalized = {}
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
    combination = {}
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

    max_lv = {}

    with open(fixed_data+'item/item_effect_table.json', encoding=enc) as f:
        obj = json.load(f)
        for item in obj['item_item_effect_table']:
            d = {}
            if item['add_effect'][0] != '':
                d['max_lv'] = max(i for i in item['effect_level'] if i != '')
                max_lv[item['add_effect'][0]] = d

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

    
def item_data():
    kind()
    category()
    material()
    trait()
    effect()

def export_csv():
    keys = {
        'trait': ['item_id', 'text_eng','desc_eng','desc2_eng','text_jpn','desc_jpn','desc2_jpn','text_chs','desc_chs','desc2_chs','text_cht','desc_cht','desc2_cht','text_deu','desc_deu','desc2_deu','text_fra','desc_fra','desc2_fra','text_kor','desc_kor','desc2_kor','text_rus','desc_rus','desc2_rus','text_spa','desc_spa','desc2_spa', 'imageNo', 'min_rarity', 'max_level',
                                'wep', 'arm', 'acc', 'atk', 'heal', 'supEne', 'subPar',
                                'grade_min_value', 'grade_max_value',
                                'lv_min_rand_range_min', 'lv_min_rand_range_max',
                                'lv_max_rand_range_min', 'lv_max_rand_range_max',
                                'trait_base', 'hash', 'item_trait_table_tag',
                                'fire', 'ice', 'bolt', 'air', 'no_level',
                                'combo_1', 'combo_2', 'combo_3', 'combo_4',
                                'disp_flag',],
        'effect': ['item_id','text_eng','desc_eng','desc2_eng','text_jpn','desc_jpn','desc2_jpn','text_chs','desc_chs','desc2_chs','text_cht','desc_cht','desc2_cht','text_deu','desc_deu','desc2_deu','text_fra','desc_fra','desc2_fra','text_kor','desc_kor','desc2_kor','text_rus','desc_rus','desc2_rus','text_spa','desc_spa','desc2_spa','has_range','att_tag','act_tag','prm1_lv_min_rand_range_min','prm1_lv_min_rand_range_max','prm1_lv_max_rand_range_min','prm1_lv_max_rand_range_max','prm2_lv_min_rand_range_max','prm2_lv_max_rand_range_min','prm2_lv_max_rand_range_max','hash_name','disp_flag','page_type_flag','max_lv']
    }
    for k, v in finalized.items():
        head = keys[k] if k in keys else v[list(v.keys())[0]].keys()
        with open(f'output/{k}.csv', 'w+') as f:
            writer = csv.DictWriter(f, head, delimiter='\t', extrasaction='ignore')
            writer.writeheader()
            for k2, v2 in v.items():
                  writer.writerow(v2)
                  

get_localization()
item_data()
#print(finalized['category'])
export_csv()
