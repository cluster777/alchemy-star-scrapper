import json
def generate_charlist(data):
    with open("./json/charlist.json", "w") as f:
        f.write('[')
        for char in data:
            if(char["name"]==""):
                break
            f.write("{")
            f.write("  \"char_name\":\"{name}\",".format(name=char["name"]))
            f.write("  \"element_main\":\"{ele}\",".format(ele=char["element_main"]))
            f.write("  \"element_sub\":\"{ele}\",".format(ele=char["element_sub"]))
            f.write("  \"faction\":\"{fac}\",".format(fac=char["faction"]))
            f.write("  \"class\":\"{clas}\",".format(clas=char["class"]))
            f.write("  \"char_rarity\":\"{rare}\"".format(rare=char["rarity"]))
            f.write('},')
            
        f.write(']')

def generate_char(data):
    with open("./json/{name}.json".format(name=data["name"]), "w") as f:
        json.dump(data, f, indent = 6)