import UnityPy
import os, re, json, sys

bundle_folder = sys.argv[1]
destination_folder = sys.argv[2]

""" if you want more assets you're gonna have to code them in """
def unpack_assets():
    for root, dirs, files in os.walk(bundle_folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            env = UnityPy.load(file_path)
            for path,obj in env.container.items():
                #if obj.type.name not in ["Texture2D", "Sprite", "MonoBehaviour"]:
                #    print(obj.type.name)

                if obj.type.name == "TextAsset":
                    # export asset
                    data = obj.read()
                    insert = '/scenario' if 'TIMELINEEVENT_' in data.m_Name else ''
                    path = os.path.join(destination_folder, f"textasset{insert}", f"{data.m_Name}.txt")
                    index = 2
                    while os.path.exists(path):
                        path = os.path.join(destination_folder, f"textasset{insert}", f"{data.m_Name}_{index}.txt")
                        index += 1
                    with open(path, "wb") as f:
                        f.write(data.m_Script.tobytes())

                if obj.type.name == "MonoBehaviour":
                    if obj.serialized_type.nodes:
                        try:
                            tree = obj.read_typetree()
                            fp = os.path.join(destination_folder, 'mono', f"{tree['m_Name']}.json")
                            with open(fp, "wt", encoding = "utf8") as f:
                                json.dump(tree, f, ensure_ascii = False, indent = 4)
                        except:
                            #print(dir(obj))
                            print(obj.external_name, obj.file_id, obj.__str__)
                if obj.type.name in ["Texture2D", "Sprite"]:
                    data = obj.read()
                    try:
                        subfolder = 'other'
                        ignored_regex = ["^O_BM", "^BD_", "^BM_", "^BN_", "^BTL_", "^EFF_", "^EVT_", "^ICON_S_", "^IPU_", "^KTG_", "^MIX_",
                                 "^P_", "^QST_", "^S[0-9][0-9]", "^s[0-9][0-9]", "^STL_RND_", "^STL_TOWN_", "^STR_", "^W_"]
                        kill = False
                        for r in ignored_regex:
                            if re.search(r, data.m_Name):
                                kill = True
                        if kill:
                            continue
                        elif 'STL_M_' in data.m_Name:
                            subfolder = 'monster'
                        elif 'STL_P_' in data.m_Name:
                            subfolder = 'chara'
                        elif 'STL_ITEM_' in data.m_Name or 'STL_MOD_ITEM' in data.m_Name:
                            subfolder = 'item'
                        elif 'STL_MINIMAP_' in data.m_Name:
                            subfolder = 'map'
                        elif 'STL_EVT_' in data.m_Name:
                            subfolder = 'event'
                        dest = os.path.join(destination_folder, "image", subfolder, data.m_Name)
                        dest, ext = os.path.splitext(dest)
                        dest = dest + ".png"
                        data.image.save(dest)
                    except:
                        print(data.m_Name)

if os.path.isdir(destination_folder) and os.path.isdir(bundle_folder):
    for o in ['textasset', 'mono', 'image']:
        os.makedirs(os.path.join(destination_folder, o), exist_ok = True)
    os.makedirs(os.path.join(destination_folder, 'textasset', 'scenario'), exist_ok = True)
    for o in ['chara', 'event', 'item', 'map', 'monster', 'other']:
        os.makedirs(os.path.join(destination_folder, 'image', o), exist_ok = True)
    unpack_assets()
else:
    print('One of your folders does not exist.')
