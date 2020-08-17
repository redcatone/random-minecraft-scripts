# aspect-lister.py

* Generates output with item registry names, and aspects of those items
    * Output files are `csv_output.csv`, `json_output.json`, and `md_output.md` and generated next to the `aspect-lister.py` file
    * `csv_output.csv` is separated by pipe characters `|` NOT commas as commas are used in the output to separate tags
    * `json_output.json` is the most human-readable without external markup or formatting
    * `md_output.md` is a markdown table but not really legible given how long some registry names are (with the added tags) and the number of columns.
* Uses a json file `thaumicjei_itemstack_aspects.json` generated from the [Thaumic JEI](https://www.curseforge.com/minecraft/mc-mods/thaumic-jei) mod
    * Json file must be named exactly as shown above and placed next to the `aspect-lister.py` file
* Originally created for the FTB Interactions modpack with a google sheet containing resulting data [available here](https://docs.google.com/spreadsheets/d/1tQkFNRyxtorWXO5ohLLPCXmmmlXQdAU0zaN8FJgM-DY/edit?usp=sharing)
