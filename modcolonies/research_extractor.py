import json
from collections import defaultdict
import os
import re


class ResearchData:
    def __init__(self, researches_path: str):
        self.researches_path = researches_path
        self.all_research_data = defaultdict(dict)
        self.script_dir = os.path.dirname(__file__)

    def write_to_TSV(self):
        with open(fr'{self.script_dir}\output\research_data.tsv', 'w') as tsv_file:
            for unlock in self.all_research_data:
                tsv_file.write(unlock + '\t')
                for data in self.all_research_data[unlock]:
                    if data == 'requirements':
                        for req in self.all_research_data[unlock][data]:
                            tsv_file.write(req + '\t')
                    else:
                        tsv_file.write(str(self.all_research_data[unlock][data]))
                        tsv_file.write('\t')
                tsv_file.write('\n')


    def import_research(self, research_name: str):
        research_folderpath = f'{self.researches_path}\{research_name}'
        unlock_files = os.listdir(research_folderpath)

        research_data = []
        for unlock_file in unlock_files:
            with open(f'{research_folderpath}\{unlock_file}', 'r') as unlock:
                unlock_name = re.sub('.json', '', unlock_file)
                unlock_data = json.loads(unlock.read())
                research_data.append((unlock_name, unlock_data))
        
        research_data = sorted(research_data, key = lambda x: x[1]['researchLevel'])

        for data in research_data:
            unlock = data[0]
            data = data[1]

            self.all_research_data[unlock] = {'unlock_level': data['researchLevel'], 'parent': None, 'requirements': []}
            if 'parentResearch' in data:
                data['parentResearch'] = re.sub(f'modcolonies:{research_name}/', '', data['parentResearch'])
                self.all_research_data[unlock]['parent'] = data['parentResearch']
            for req in data['requirements']:
                if 'mandatory-building' in req:
                    self.all_research_data[unlock]['requirements'].append(f"{req['mandatory-building']}:{req['level']}")
                if 'item' in req:
                    while len(self.all_research_data[unlock]['requirements']) < 3:
                        self.all_research_data[unlock]['requirements'].append('')
                    self.all_research_data[unlock]['requirements'].append(f"{req['item']}:{req['quantity']}")
