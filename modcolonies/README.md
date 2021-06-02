# A collection of scripts for the Minecraft modpack [ModColonies](https://www.curseforge.com/minecraft/modpacks/modcolonies/)

Scripts to parse data from datapacks for the [Minecolonies](https://www.curseforge.com/minecraft/mc-mods/minecolonies) mod.

[Example usage file](example_usage.py)

Output is mainly used to display info a [public google sheet](https://docs.google.com/spreadsheets/d/1l69nD1I0XdGxmlce21ke_dPjjNzHXMDjsakUD0mXhKU/edit?usp=sharing)


## crafter_recipe_extractor.py
* Gets recipe data used by workers at their huts.

#### import_recipes(recipes_folderpath)

* Parses data from `recipes_folderpath` to get the custom recipes added to workers.

#### write_to_TSV()
* Writes to `/output/crafter_data.tsv` located next to the location of the script.
* Format is: `worker:level research output(s) input(s)`

#### generate_JEI_help()
* Writes to `/output/jei_help.zs` located next to the location of the script.
* When viewed ingame format is
```
Crafts 23
Requires:
  Level 3 mechanic
  1 Iron ingot
  3 Sand
  29 Dirt
```

#### Example

```python
from crafter_recipe_extractor import CraftData

c = CraftData(r"C:\Curseforge\Instances\ModColonies\openloader\data\modcolonies\data\modcolonies\crafterrecipes")
c.write_to_TSV()
c.generate_JEI_help()

```


## research_extractor.py
* Gets research requirements for custom research.

#### import_research(research_name)
* Parses data from the `research_name` folder in `\ModColonies\openloader\data\modcolonies\data\modcolonies\researches\` to get the custom research.

#### write_to_TSV()
* Writes to `/output/research_data.tsv` located next to the location of the script.
* Format is: `unlock_effect required_level parent_research required_building(s) required_item(s)`

#### Example usage
```python
from research_extractor import ResearchData

c = ResearchData(r"C:\Curseforge\Instances\ModColonies\openloader\data\modcolonies\data\modcolonies\researches")
c.import_research("modology")
c.import_research("ultimate_understanding")
c.write_to_TSV()
```


## sieve_data_extractor.py
* Gets sieve drop rates for custom drops.

#### import_loottable(sieve_folderpath)
* Parses data from `sieve_folderpath` to get the custom drops added to blocks for the sifter

#### write_to_TSV()
* Writes to `/output/sieve_data.tsv` located next to the location of the script.
* Format is `drop mesh_tier-block,drop_rate`

#### Example
```python
c = SieveData()
c.import_loottable(r"C:\Curseforge\Instances\ModColonies\openloader\data\modcolonies\data\modcolonies\loot_tables\recipes")
c.write_to_TSV()
```