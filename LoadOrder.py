##
# NOAH - LoadOrder
##

import os
import re
import requests
from bs4 import BeautifulSoup

MODS_PATH = r"Ton Fichier ici" ################ TON CHEMIN ICI ############
OUTPUT_FILE = "resultat_complet.txt"

CATEGORIES = {
    1: "Tiles",
    2: "Maps",
    3: "Dépendances",
    4: "Ressources Système",
    5: "Mods QOL",
    6: "Craft et Items",
    7: "Véhicules"
}

class PZMod:
    def __init__(self, workshop_id):
        self.workshop_id = workshop_id
        self.mod_ids = []
        self.name = "Inconnu"
        self.description_fr = ""
        self.category = 5
        self.dependencies = []
        self.map_folders = []
        self.path = os.path.join(MODS_PATH, workshop_id)
        self.steam_url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={workshop_id}"

    def analyze_local(self):
        for root, dirs, files in os.walk(self.path):
            if "mod.info" in files:
                try:
                    with open(os.path.join(root, "mod.info"), 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        m_id = re.search(r"id=(.*)", content)
                        m_name = re.search(r"name=(.*)", content)
                        m_req = re.search(r"require=(.*)", content)
                        if m_id: self.mod_ids.append(m_id.group(1).strip())
                        if m_name and self.name == "Inconnu": self.name = m_name.group(1).strip()
                        if m_req: self.dependencies.extend([x.strip() for x in m_req.group(1).split(',') if x.strip()])
                except: pass

            if "maps" in dirs: 
                self.category = 2
                map_path = os.path.join(root, "maps")
                if os.path.exists(map_path):
                    self.map_folders.extend([d for d in os.listdir(map_path) if os.path.isdir(os.path.join(map_path, d))])
            
            if "tiledefs" in dirs: self.category = 1
            
            for f in files:
                f_low = f.lower()
                if self.category not in [1, 2]:
                    if "vehicle" in f_low: self.category = 7
                    elif any(x in f_low for x in ["item", "recipe", "weapon", "clothing"]): self.category = 6
                    elif any(x in f_low for x in ["admin", "debug", "core", "framework", "lib"]): self.category = 4

    def fetch_steam_info(self):
        try:
            res = requests.get(self.steam_url, timeout=5)
            soup = BeautifulSoup(res.text, 'html.parser')
            desc_tag = soup.find("div", class_="workshopItemDescription")
            if desc_tag:
                desc = desc_tag.text.strip().replace('\n', ' ').replace('\r', '')
                self.description_fr = (desc[:100] + '...') if len(desc) > 100 else desc
        except: self.description_fr = "Erreur Steam"

def run():
    folder_list = [d for d in os.listdir(MODS_PATH) if d.isdigit()]
    total = len(folder_list)
    all_mods = []
    all_required_ids = set()

    for i, w_id in enumerate(folder_list, 1):
        print(f"\rProgression: {i}/{total} ({int(i/total*100)}%)", end="", flush=True)
        mod = PZMod(w_id)
        mod.analyze_local()
        mod.fetch_steam_info()
        all_mods.append(mod)
        all_required_ids.update(mod.dependencies)

    
    for mod in all_mods:
        if any(m_id in all_required_ids for m_id in mod.mod_ids): mod.category = 3

   
    all_mods.sort(key=lambda x: (x.category, x.name.lower()))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        # --- PARTIE 1 : GOOGLE SHEETS ---
        f.write("=== PARTIE 1 : Tableau ===\n")
        f.write("Lien | Workshop ID | Mod ID | Commentaire | Load Order | Dépendance | Map\n")
        f.write("-" * 100 + "\n")
        for mod in all_mods:
            f.write(f"{mod.steam_url} | {mod.workshop_id} | {';'.join(mod.mod_ids)} | {mod.description_fr} | {mod.category} | {';'.join(mod.dependencies)} | {';'.join(mod.map_folders)}\n")

        
        f.write("\n\n=== PARTIE 2 : servertest.ini ===\n")
        
      
        mods_list = []
        workshop_list = []
        maps_list = []

        for mod in all_mods:
            if mod.mod_ids: mods_list.extend(mod.mod_ids)
            workshop_list.append(mod.workshop_id)
            if mod.map_folders: maps_list.extend(mod.map_folders)

        f.write("\n# Liste des Mod IDs (Mods=)\n")
        f.write(f"Mods={';'.join(mods_list)}\n")

        f.write("\n# Liste des Maps (Map=)\n")
        # Note: Muldraugh, KY doit souvent être à la fin, le script respecte ton ordre de catégorie
        f.write(f"Map={';'.join(maps_list)}\n")

        f.write("\n# Liste des Workshop IDs (WorkshopItems=)\n")
        f.write(f"WorkshopItems={';'.join(workshop_list)}\n")

    print(f"\nTerminé ! Fichier généré : {OUTPUT_FILE}")

if __name__ == "__main__":
    run()
