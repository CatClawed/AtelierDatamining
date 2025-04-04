import os, json, struct, re

root = 'Data/pak/master/eng/eventmessagedata/'
choices = {}

def extract_text(file):
    index = 0
    ls = []
    with open(root+file, 'rb') as f:
        ebm = f.read()
        dialog_count = struct.unpack('<I', ebm[index:index+4])[0]
        index += 4
        wtf = struct.unpack('<I', ebm[index:index+4])[0]
        index += 4
        while index < len(ebm) and dialog_count != len(ls):
            d = {}
            char_tag_length = struct.unpack('<I', ebm[index:index+4])[0]
            index += 4
            if char_tag_length > 0 and char_tag_length < 4294967295:
                d['char_tag'] = ebm[index:index+char_tag_length-1].decode('utf8')
                index += char_tag_length
            elif char_tag_length == 4294967295:
                index += 24
            else:
                index += 4
            kind = struct.unpack('<I', ebm[index:index+4])[0]
            index += 4
            if kind == 0 and index != len(ebm):
                name_tag_length = struct.unpack('<I', ebm[index:index+4])[0]
                index +=4
                d['name_tag'] = ebm[index:index+name_tag_length-1].decode('utf8')
                index += 60+name_tag_length
                str_length = struct.unpack('<I', ebm[index:index+4])[0]
                index += 4
                d['line'] = ebm[index:index+str_length-1].decode('utf8')
                if not d['name_tag']:
                    del d['name_tag']
                if not d['char_tag']:
                    del d['char_tag']
                sel_tag = re.findall("<SEL[^<]+>", d['line'])
                if len(sel_tag) > 0:
                    d['selection_tag'] = sel_tag[0][1:-1]
                    d['line'] = d['line'].split('<CR>')[1]
                    choices[d['selection_tag']] = {
                        'file': file,
                        'line': d['line']
                    }
                index += str_length
            elif kind == 4294967295:
                index += 28
            else:
                if index != len(ebm):
                    wtf2 = struct.unpack('<I', ebm[index:index+4])[0]
                    index +=4
                    if wtf2 == 1:
                        index += 4
                else:
                    index += 4
            if 'line' in d:
                ls.append(d)

        with open(f'scenario/{file[:-3]}json', 'w') as f2:
            json.dump(ls, f2, ensure_ascii=False, indent=4)


for f in os.listdir(f'{os.getcwd()}/{root}'):
    extract_text(f)

with open(f'output/choices.json', 'w') as f2:
    json.dump(choices, f2, ensure_ascii=False, indent=4)
