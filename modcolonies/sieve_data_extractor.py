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
        for mesh_tier in ['diamond', 'iron', 'flint', 'string']:  # custom ordering
            file_list = os.listdir(f'{sieve_folderpath}\{mesh_tier}')
            for block_file in file_list:
                with open(f'{sieve_folderpath}\{mesh_tier}\{block_file}', 'r') as block_data:
                    block = re.sub(r'.json', '', block_file)
                    drop_data = json.loads(block_data.read())['pools'][0]
                    roll_min = drop_data['rolls']['min']
                    roll_max = drop_data['rolls']['max']

                    bonus_roll_min = 0
                    bonus_roll_max = 0
                    if 'bonus_rolls' in drop_data:
                        bonus_roll_max = drop_data['bonus_rolls']['max']
                        bonus_roll_min = drop_data['bonus_rolls']['min']
                    self.mesh_data[f'{mesh_tier} - {block}'] = f'{roll_min}, {roll_max}, {bonus_roll_min}, {bonus_roll_max}'

                    for drop in drop_data['entries']:
                        try:
                            name = drop['name']
                        except KeyError:
                            name = drop['type']

                        rate = drop['weight']

                        self.drop_data[name].append(f'{mesh_tier} - {block}, {rate}')


    def write_to_TSV(self):
        with open(f'{self.script_dir}\output\sieve_data.tsv', 'w') as tsv_file:
            for drop in self.drop_data:
                row = drop + '\t ' + '\t '.join(self.drop_data[drop])
                tsv_file.write(row + '\n')

            for mesh_tier_block in self.mesh_data:
                row = mesh_tier_block + '\t ' + str(self.mesh_data[mesh_tier_block])
                tsv_file.write(row + '\n')


    def generate_nihilo(self):
        mesh_total = collections.defaultdict(int)

        for drop in self.drop_data:
            for tier_block in self.drop_data[drop]:
                tier = re.match('(.*) -', tier_block)[1]
                block = re.match('.* - (.*), ', tier_block)[1]
                weight = int(re.match('.*, (\d*)', tier_block)[1])

                mesh_total[f'{tier}_{block}'] += int(weight)


        with open(f'{self.script_dir}\output\jei_sieve.zs', 'w') as jei_file:
            jei_file.write('import mods.exnihilosequentia.ZenSieveRecipe;' + '\n\n' + '<recipetype:exnihilosequentia:sieve>.removeAll();' + '\n\n')

            for drop in self.drop_data:
                if drop == 'minecraft:empty': continue  # skip empty drop
                for tier_block in self.drop_data[drop]:
                    tier = re.match('(.*) -', tier_block)[1]
                    block = re.match('.* - (.*), ', tier_block)[1]
                    weight = int(re.match('.*, (\d*)', tier_block)[1])
                    rate = round(weight / mesh_total[f'{tier}_{block}'], 4)
                    if block == 'dust':
                        block = 'exnihilosequentia:dust'
                    else:
                        block = f'minecraft:{block}'

                    row = f'<recipetype:exnihilosequentia:sieve>.create("{tier}_{block.replace(":", ".")}_{drop.replace(":", ".")}").setInput(<item:{block}>).addDrop(<item:{drop}>).addRoll("{tier}", {rate});'
                    jei_file.write(row + '\n')
