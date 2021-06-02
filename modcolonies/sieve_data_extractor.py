import json
import os
import collections
import re


class SieveData:
    def __init__(self):
        self.drop_data = collections.defaultdict(list)
        self.mesh_data = collections.defaultdict(dict)
        self.script_dir = os.path.dirname(__file__)


    def import_loottable(self, sieve_folderpath: str):
        self.mesh_tiers = os.listdir(sieve_folderpath)

        # for mesh_tier in self.mesh_tiers:
        for mesh_tier in ["diamond", "iron", "flint", "string"]:  # custom ordering
            file_list = os.listdir(f"{sieve_folderpath}\{mesh_tier}")
            for block_file in file_list:
                with open(f"{sieve_folderpath}\{mesh_tier}\{block_file}", 'r') as block_data:
                    block = re.sub(r".json", "", block_file)
                    drop_data = json.loads(block_data.read())["pools"][0]
                    roll_min = drop_data["rolls"]["min"]
                    roll_max = drop_data["rolls"]["max"]

                    bonus_roll_min = 0
                    bonus_roll_max = 0
                    if "bonus_rolls" in drop_data:
                        bonus_roll_max = drop_data["bonus_rolls"]["max"]
                        bonus_roll_min = drop_data["bonus_rolls"]["min"]
                    self.mesh_data[f"{mesh_tier} - {block}"] = f"{roll_min}, {roll_max}, {bonus_roll_min}, {bonus_roll_max}"

                    for drop in drop_data["entries"]:
                        try:
                            name = drop["name"]
                        except KeyError:
                            name = drop["type"]

                        rate = drop["weight"]

                        self.drop_data[name].append(f"{mesh_tier} - {block}, {rate}")


    def write_to_TSV(self):
        with open(f"{self.script_dir}\output\sieve_data.tsv", "w") as csv_file:
            for drop in self.drop_data:
                row = drop + "\t " + "\t ".join(self.drop_data[drop])
                csv_file.write(row + "\n")

            for mesh_tier_block in self.mesh_data:
                row = mesh_tier_block + "\t " + str(self.mesh_data[mesh_tier_block])
                csv_file.write(row + "\n")
