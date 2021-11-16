import json
def generate_charlist(data):
    with open("./json/charlist.json", "w") as f:
        for char in data:

            char["char_name"] = char.pop("name")
            char["char_rarity"] = char.pop("rarity")
        json.dump(data[:-1], f)
    for char in data:

        char["name"] = char.pop("char_name")
        char["rarity"] = char.pop("char_rarity")
def generate_char(data):
    with open("./json/{name}.json".format(name=data["name"]), "w") as f:
        json.dump(data, f,indent=1)