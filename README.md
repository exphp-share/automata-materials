Counting the total number of items required to upgrade all weapons and Pods in NieR Automata, because seemingly nobody else has.

Script output:

| Material | Count |
| ---:| ---:|
|       Copper Ore | 100 |
|         Iron Ore |  77 |
|       Silver Ore |  59 |
|         Gold Ore |  40 |
|     Rusted Clump |  95 |
|     Dented Plate |  80 |
|   Titanium Alloy |  60 |
|     Memory Alloy |  38 |
|       Beast Hide |  40 |
|       Broken Key |  75 |
|      Warped Wire |  32 |
|   Stretched Coil |  36 |
|   Broken Circuit |  50 |
|   Stripped Screw |  32 |
|   Pristine Screw |  12 |
|       Small Gear |  56 |
|       Large Gear |  21 |
|       Rusty Bolt |  53 |
|         New Bolt |  21 |
|      Crushed Nut |  32 |
|        Clean Nut |  12 |
|    Dented Socket |  32 |
|    Sturdy Socket |  12 |
|    Severed Cable |  50 |
|   Pristine Cable |  21 |
|   Broken Battery |  51 |
|    Large Battery |  18 |
|      Machine Arm |  30 |
|      Machine Leg |  18 |
|    Machine Torso |  14 |
|     Machine Head |  16 |
|          Crystal |  80 |
|            Pearl |  29 |
|      Black Pearl |  18 |
|           Pyrite |  44 |
|            Amber |  36 |
|        Moldavite |  20 |
|        Meteorite |  19 |
|  Meteorite Shard |   6 |
|    Simple Gadget |  20 |
| Elaborate Gadget |  10 |
|   Complex Gadget |   6 |
|   Powerup Part S |   3 |
|   Powerup Part M |   3 |
|   Powerup Part L |   3 |
|        Tree Seed |  20 |
|       Plant Seed |  10 |
|         Tree Sap |   6 |
|         Mushroom |  20 |
|       Eagle Eggs |  10 |
|        Giant Egg |   6 |
|        Torn Book |  20 |
|      Tech Manual |  10 |
| Thick Dictionary |   6 |
|       Pure Water |  20 |
|    Tanning Agent |  10 |
|              Dye |   6 |
|   Natural Rubber |  20 |
|      Machine Oil |   6 |
|     Filler Metal |  10 |

## Extended usage

There are additional features:

* **Exclude costs of upgrades you already have:** Supply `--current-levels current-levels.yaml`, where `current-levels.yaml` is a YAML mapping of weapon names to their current upgrade levels.
* **Filter or reorder the output:** Supply `--item-list itemlist.txt` to display the items in the order from that file. (without this, default is to sort descending by count).  Some item lists are included:
  * `data/itemlist-all.txt`: all ingredients, in menu display order (on PC)
  * `data/itemlist-emil.txt`: ingredients that can be bought from Emil's alternate route shop

**Example:** Suppose you want to know how many of each ingredient you need to buy from Emil's (outrageously expensive) precious materials shop:

```
$ python3 compute-totals.py --current-levels current-levels.yaml --item-list data/itemlist-emil.txt
  Memory Alloy : 18
Pristine Screw : 9
    Large Gear : 12
      New Bolt : 12
     Clean Nut : 6
 Sturdy Socket : 9
Pristine Cable : 6
 Large Battery : 6
```