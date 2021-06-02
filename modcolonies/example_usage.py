from sieve_data_extractor import SieveData
from crafter_recipe_extractor import CraftData
from research_extractor import ResearchData


c = CraftData()
c.import_recipes(r"C:\Curseforge\Instances\ModColonies\openloader\data\modcolonies\data\modcolonies\crafterrecipes")
c.write_to_TSV()
c.generate_JEI_help()


c = ResearchData(r"C:\Curseforge\Instances\ModColonies\openloader\data\modcolonies\data\modcolonies\researches")
c.import_research("modology")
c.import_research("ultimate_understanding")
c.write_to_TSV()


c = SieveData()
c.import_loottable(r"C:\Curseforge\Instances\ModColonies\openloader\data\modcolonies\data\modcolonies\loot_tables\recipes")
c.write_to_TSV()
