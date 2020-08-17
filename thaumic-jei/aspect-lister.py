import re, json, os
from collections import defaultdict

def json_data(filename):
    item_aspect_dict = defaultdict(list)
    
    with open(filename, "r") as f:
        aspect_list = json.loads(f.read()) # Returns a list of dictionaries containing aspects and items
        
        for aspect_dict in aspect_list:
            aspect = aspect_dict["aspect"]
            item_list = aspect_dict["items"] # item_list contains a list of strings

            for item in item_list: # Item is a string array with id, count, damage, and optional tags {}
                # Set registry name by using regex to search for the id
                try:
                    _item_name = re.search("id:\"(.*?)\"", item)
                except AttributeError:
                    _item_name = "no name"
                item_name = _item_name.group(1)

                # Set metadata by using regex to search for damage
                try:
                    _metadata = re.search("Damage:(\d*)s", item)
                except AttributeError:
                    _item_name = "no metadata"
                metadata = _metadata.group(1)
                item_name_meta = f"{item_name}:{metadata}"

                # Set aspect amount by using regex to search for count
                try:
                    _aspect_count = re.search("Count:(\d*)s", item)
                except AttributeError:
                    _aspect_count = "no count"
                aspect_count = _aspect_count.group(1)

                # If item has extra tags, save this data to append to item name
                if re.search("tag:", item):
                    extra_data = re.search("tag:({.*?})", item).group(1)
                else:
                    extra_data = ""

                # Append extra data if available after three dashes
                if extra_data == "":
                    item_aspect_dict[f"{item_name_meta}"].append(f"{aspect_count} {aspect}")
                else:
                    item_aspect_dict[f"{item_name_meta} --- {extra_data}"].append(f"{aspect_count} {aspect}")
                

    script_dir = os.path.dirname(__file__) # Get path to script
    with open(f"{script_dir}/json_output.json", "w") as jf:
        jf.write(json.dumps(item_aspect_dict, indent=4, separators=(", ", " : "), sort_keys=True))
        jf.write("\n")
    
    # Csv is separated by pipe characters `|`, not commas as commas are used in tags
    with open(f"{script_dir}/csv_output.csv", "w") as cf: 
        for key in item_aspect_dict.keys():
            cf.write(f"{key}")
            for i in item_aspect_dict[key]:
                cf.write(f"|{i}")
            cf.write("\n")

    # Markdown table
    with open(f"{script_dir}/md_output.md", "w") as mf:
        headers = ["Item Name"]
        for i in range(0, 10): # Hard coded column numbers
            headers.append(f"Aspect {i}")
        mf.write("|")
        for text in headers:
            mf.write(f"{text}|")
        mf.write("\n|")
        for text in headers:
            mf.write("---|")
        mf.write("\n")
        
        for key in item_aspect_dict.keys():
            mf.write(f"|{key}|")
            for i in item_aspect_dict[key]:
                mf.write(f"|{i}")
            mf.write("\n")

if __name__ == "__main__":
    json_data("thaumicjei_itemstack_aspects.json")
