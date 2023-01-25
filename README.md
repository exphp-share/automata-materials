Counting the total number of items required to upgrade all weapons and Pods in NieR Automata, because seemingly nobody else has.

Script output:

| Material | Count |
| ---:| ---:|
|       Copper Ore | 100 |
|     Rusted Clump |  95 |
|     Dented Plate |  80 |
|          Crystal |  80 |
|         Iron Ore |  77 |
|       Broken Key |  75 |
|   Titanium Alloy |  60 |
|       Silver Ore |  59 |
|       Small Gear |  56 |
|       Rusty Bolt |  53 |
|   Broken Battery |  51 |
|   Broken Circuit |  50 |
|    Severed Cable |  50 |
|           Pyrite |  44 |
|         Gold Ore |  40 |
|       Beast Hide |  40 |
|     Memory Alloy |  38 |
|   Stretched Coil |  36 |
|            Amber |  36 |
|   Stripped Screw |  32 |
|      Warped Wire |  32 |
|      Crushed Nut |  32 |
|    Dented Socket |  32 |
|      Machine Arm |  30 |
|            Pearl |  29 |
|         New Bolt |  21 |
|       Large Gear |  21 |
|   Pristine Cable |  21 |
|        Moldavite |  20 |
|        Tree Seed |  20 |
|         Mushroom |  20 |
|       Pure Water |  20 |
|   Natural Rubber |  20 |
|        Torn Book |  20 |
|    Simple Gadget |  20 |
|        Meteorite |  19 |
|      Black Pearl |  18 |
|    Large Battery |  18 |
|      Machine Leg |  18 |
|     Machine Head |  16 |
|    Machine Torso |  14 |
|   Pristine Screw |  12 |
|        Clean Nut |  12 |
|    Sturdy Socket |  12 |
|       Plant Seed |  10 |
|       Eagle Eggs |  10 |
|    Tanning Agent |  10 |
|     Filler Metal |  10 |
|      Tech Manual |  10 |
| Elaborate Gadget |  10 |
|  Meteorite Shard |   6 |
|         Tree Sap |   6 |
|       Giant Eggs |   6 |
|              Dye |   6 |
|      Machine Oil |   6 |
| Thick Dictionary |   6 |
|   Complex Gadget |   6 |
|   Powerup Part S |   3 |
|   Powerup Part M |   3 |
|   Powerup Part L |   3 |

## Extended usage

There are additional features:

* **Exclude costs of upgrades you already have:** Supply `--current-levels current-levels.yaml`, where `current-levels.yaml` is a YAML mapping of weapon names to their current upgrade levels.
* **Filter or reorder the output:** Supply `--item-list itemlist.txt` to display the items in the order from that file. (without this, default is to sort descending by count).  Some item lists are included:
  * `itemlist-all.txt`: all ingredients, in menu display order (on PC)
  * `itemlist-emil.txt`: ingredients that can be bought from Emil's alternate route shop

**Example:** Suppose you want to know how many of each ingredient you need to buy from Emil's (outrageously expensive) precious materials shop:

```
$ python3 compute-totals.py --current-levels current-levels.yaml --item-list itemlist-emil.txt
  Memory Alloy : 18
Pristine Screw : 9
    Large Gear : 12
      New Bolt : 12
     Clean Nut : 6
 Sturdy Socket : 9
Pristine Cable : 6
 Large Battery : 6
```