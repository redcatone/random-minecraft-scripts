import json
import os
from collections import defaultdict
import re


class CraftData:
    def __init__(self):
        self.script_dir = os.path.dirname(__file__)  # output file generated at script location
        self.worker_recipes = defaultdict(dict)


    def import_recipes(self, recipes_folderpath: str):
        # filename: inputs:[input:amount], outputs:[output:amount], research:research, worker:worker, level:level
        worker_huts_folder = os.listdir(recipes_folderpath)

        # Scan all worker hut folders
        for worker_hut_folder in worker_huts_folder:
            if worker_hut_folder == 'sifter':  # skip sifter since it is uses different format
                continue
                
            recipe_file_list = os.listdir(f'{recipes_folderpath}\{worker_hut_folder}')
            # Scan all recipe files for worker hut
            for recipe_file in recipe_file_list:
                with open(f'{recipes_folderpath}\{worker_hut_folder}\{recipe_file}', 'r') as recipe_data:
                    recipe_data = json.loads(recipe_data.read())

                    # Get Basic Data
                    worker = recipe_data['crafter']
                    worker_level = str(recipe_data.get('min-building-level', "1"))
                    research_requirement = recipe_data.get('research-id', "")
                    research_requirement = re.search("/(.*)", research_requirement)
                    if research_requirement: research_requirement = research_requirement.group(1)

                    # Generate Input Data
                    inputs = recipe_data['inputs']
                    all_inputs = []
                    for input in inputs:
                        input_item = input['item']
                        input_item_count = input.get('count', "1")
                        all_inputs.append(f"{input_item}:{input_item_count}")

                    # Generate Output Data
                    all_outputs = []

                    # Main Output
                    main_output = recipe_data.get('result', '')
                    if not main_output: main_output = recipe_data['additional-output'][0]['item']
                    main_output_count = str(recipe_data.get('count', 1))
                    all_outputs.append(f"{main_output}:{main_output_count}")

                    # Alternate Outputs
                    alt_outputs = recipe_data.get('alternate-output', "")
                    for alt_output in alt_outputs:
                        output_item = alt_output['item']
                        output_count = str(alt_output.get('count', '1'))
                        all_outputs.append(f"{output_item}:{output_count}")

                    self.worker_recipes[recipe_file]['inputs'] = all_inputs
                    self.worker_recipes[recipe_file]['outputs'] = all_outputs
                    self.worker_recipes[recipe_file]['research'] = research_requirement
                    self.worker_recipes[recipe_file]['worker'] = worker
                    self.worker_recipes[recipe_file]['level'] = worker_level


    def write_to_TSV(self):
        # worker:level research [outputs] [input_items]
        with open(f'{self.script_dir}\output\crafter_data.tsv', 'w') as tsv_file:
            # Find max output length to generate empty cells
            max_output_length = 0
            for recipe_data in self.worker_recipes.values():
                current_output_length = len(recipe_data['outputs'])
                max_output_length = max(max_output_length, current_output_length)

            for recipe_data in self.worker_recipes.values():
                outputs = recipe_data['outputs'].copy()
                # Set blank cells
                for _ in range(len(outputs), max_output_length + 1):
                    outputs.append('')
                outputs = '\t'.join(outputs)

                worker = recipe_data['worker']
                level = recipe_data['level']
                research = recipe_data['research']
                input_items = '\t'.join(recipe_data['inputs'])

                row = f'{worker}:{level}\t{research}\t{outputs}\t{input_items}'
                tsv_file.write(row + '\n')


    def generate_JEI_help(self):
        # Crafts 23
        # Requires:
        #  Level 3 mechanic
        #  1 Iron ingot
        #  3 Sand
        #  29 Dirt

        with open(f'{self.script_dir}\output\jei_colony_crafting.zs', 'w') as zs_file:
            for recipe_data in self.worker_recipes.values():
                # Basic Info
                crafter  = recipe_data['worker']
                level = recipe_data['level']

                # Input Info
                input_data = []
                input_items = recipe_data['inputs']
                for input in input_items:
                    input_name, input_amount = input.rsplit(':', 1)
                    item_input_row = f'"  {input_amount} " + <item:{input_name}>.displayName'
                    input_data.append(item_input_row)

                # Output Info
                outputs = recipe_data['outputs']
                for output in outputs:
                    help_data = []
                    output_name, output_amount = output.rsplit(':', 1)

                    help_data.append(f'"Crafts {output_amount}"')
                    help_data.append(f'"Requires:"')
                    help_data.append(f'"  Level {level} {crafter.capitalize()}"')

                    # Write row
                    help_data += input_data
                    row = f'mods.jei.JEI.addInfo(<item:{output_name}>, [{", ".join(help_data)}]);'
                    zs_file.write(row + '\n')
