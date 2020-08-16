import re, json, os, csv
from collections import defaultdict

# need special handing for 
# ForgeCaps???
# tag:{Potion:}
# tag:{StoredEnchantments:[{}]}

def json_data(filename):
    item_aspect_dict = defaultdict(list)
    
    with open(filename, "r") as f:
        aspect_list = json.loads(f.read())
        print(type(aspect_list))
        print(type(aspect_list[0]))
        
        for aspect_dict in aspect_list:
            aspect = aspect_dict["aspect"]
            item_list = aspect_dict["items"]

            # print(aspect)
            # print(item_list)

            for item in item_list: # Item is a string array with id, count, damage, and optionally tags {}

                try:
                    _item_name = re.search("id:\"(.*?)\"", item)
                except AttributeError:
                    _item_name = "no name"
                item_name = _item_name.group(1)

                try:
                    _metadata = re.search("Damage:(\d*)s", item)
                except AttributeError:
                    _item_name = "no metadata"
                metadata = _metadata.group(1)
                item_name_meta = f"{item_name}:{metadata}"


                try:
                    _aspect_count = re.search("Count:(\d*)s", item)
                except AttributeError:
                    _aspect_count = "no count"
                aspect_count = _aspect_count.group(1)

                # if re.search("Potion:", item):
                #     print("need special handling")
                #     try:
                #         _potion = re.search("Potion:\\\"(.*)\\\"", item)
                #         extra_data = _potion.group(1)
                #     except:
                #         extra_data = ""
                #         print("could not process potion")
                #         print(item)
                
                # elif re.search("StoredEnchantments", item):
                #     print("need special handling")
                #     try:
                #         _enchant = re.search("StoredEnchantments:\[{(.*)}\]", item)
                #         extra_data = _enchant.group(1)
                #     except:
                #         extra_data = ""
                #         print("could not process enchant")
                #         print(item)
                # elif re.search("tag:", item):
                #     print("Could not process tag")
                #     print(item)
                if re.search("tag:", item):
                    extra_data = re.search("tag:({.*})", item).group(1)
                else:
                    extra_data = ""
                
                # if item_name_meta not in item_aspect_dict:
                #     item_aspect_dict[item_name_meta].append(f"{extra_data}")
                item_aspect_dict[f"{item_name_meta}{extra_data}"].append(f"{aspect_count} {aspect}")



                # print(item_name_meta)
                # print(aspect_count)
                # print(item_aspect_dict)

                

    script_dir = os.path.dirname(__file__) # get path to script
    with open(f"{script_dir}/json_output.json", "w") as jf:
        jf.write(json.dumps(item_aspect_dict, indent=4, separators=(", ", " : "), sort_keys=True))
        jf.write("\n")
    
    with open(f"{script_dir}/csv_output.csv", "w") as cf:
        for key in item_aspect_dict.keys():
            cf.write(f"{key}")
            for i in item_aspect_dict[key]:
                cf.write(f"|{i}")
            cf.write("\n")

    with open(f"{script_dir}/md_output.md", "w") as mf:
        headers = ["Item Name"]
        for i in range(0, 10):
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


    # csv_file = f"{script_dir}/csv_output.csv"
    # try:
    #     with open(csv_file, "w") as cf:
    #         csv_columns = ["Item Name"]
    #         for i in range(0, 10):
    #             csv_columns.append(f"Aspect {i}")

    #         print(csv_columns)

    #         writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
    #         writer.writeheader()

    #         for data in item_aspect_dict:
    #             writer.writerow(data)


    # except IOError:
    #     print("I/O error")        

        



if __name__ == "__main__":
    json_data("thaumicjei_itemstack_aspects.json")
    # json_data("test.json")
