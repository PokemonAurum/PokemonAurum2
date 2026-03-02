#!/usr/bin/env python3
import csv
import sys

SPECIES_FILE = "asm/include/species.inc"
CSV_FILE = "hidden_abilities.csv"
OUTPUT_FILE = "armips/data/hiddenabilities.s"

# Read species order from species.inc
species_order = []
with open(SPECIES_FILE, "r") as f:
    for line in f:
        line = line.strip()
        if line.startswith(".equ SPECIES_") and "," in line:
            name = line.split(".equ ")[1].split(",")[0].strip()
            species_order.append(name)

# Read HA assignments from CSV
ha_map = {}
with open(CSV_FILE, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        ha_map[row["species"].strip()] = row["ability"].strip()

# Write output
with open(OUTPUT_FILE, "w") as f:
    f.write(".align 2\n")
    f.write(".global gHiddenAbilityTable\n")
    f.write("gHiddenAbilityTable:\n\n")
    for species in species_order:
        ability = ha_map.get(species, "ABILITY_NONE")
        f.write(f"    // {species}\n")
        f.write(f"    .halfword {ability}\n")

print(f"Done! Written {len(species_order)} entries to {OUTPUT_FILE}")
