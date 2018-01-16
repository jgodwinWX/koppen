import numpy as np
import pandas as pd

df = pd.read_csv('data.csv',header=None)
cities = np.array(df[0])

highs = {}
lows = {}
precip = {}
climate = {}

# convert to metric units
for i in range(len(cities)):
    highs[cities[i]] = (np.array(df.ix[i][1:13]) - 32.0) * (5.0/9.0)
    lows[cities[i]] = (np.array(df.ix[i][13:25]) - 32.0) * (5.0/9.0)
    precip[cities[i]] = np.array(df.ix[i][25:38]) * 25.4

for city in cities:
    avgtemp = (highs[city] + lows[city]) / 2.0
    totalprecip = sum(precip[city])
    climate[city] = ''

    # Group A (Tropical)
    if min(avgtemp) >= 18.0:
        # Tropical Rainforest
        if min(precip[city]) >= 60.0:
            climate[city] = 'Af'
            continue
        # Tropical Monsoon
        elif min(precip[city]) < 60.0 and (min(precip[city]) / totalprecip) > 0.04:
            climate[city] = 'Am'
            continue
        else:
            # Tropical Savanna Dry Summer
            if np.where(precip[city]==min(precip[city]))[0][0] >= 6 and np.where(precip[city]==min(precip[city]))[0][0] <= 8:
                climate[city] = 'As'
                continue
            # Tropical Savanna Dry Winter
            else:
                climate[city] = 'Aw'
                continue

    # Group B (Arid and Semiarid)
    aridity = np.mean(avgtemp) * 20.0
    warmprecip = sum(precip[city][3:9])
    coolprecip = sum(precip[city][0:3]) + sum(precip[city][9:12])
    if warmprecip / totalprecip >= 0.70:
        aridity = aridity + 280.0
    elif warmprecip / totalprecip >= 0.30 and warmprecip / totalprecip < 0.70:
        aridity = aridity + 140.0
    else:
        aridity = aridity + 0.0

    # Arid Desert (BW)
    if totalprecip / aridity < 0.50:
        # Hot Desert (BWh)
        if np.mean(avgtemp) > 18.0:
            climate[city] = 'BWh'
            continue
        # Cold Desert (BWk)
        else:
            climate[city] = 'BWk'
            continue

    if 'A' in climate[city]:
        continue

    # Semi-Arid/Steppe (BS)
    elif totalprecip / aridity >= 0.50 and totalprecip / aridity < 1.00:
        # Hot Semi-Arid (BSh)
        if np.mean(avgtemp) > 18.0:
            climate[city] = 'BSh'
            continue
        # Cold Semi-Arid (BSk)
        else:
            climate[city] = 'BSk'
            continue

    if 'B' in climate[city]:
        continue

    # Group C (Temperate)
    sortavgtemp = avgtemp
    sortavgtemp.sort()
    tempaboveten = np.shape(np.where(avgtemp>10.0))[1]
    coldwarmratio = max(max(precip[city][0:2]),precip[city][11]) / min(precip[city][5:8])
    warmcoldratio = max(precip[city][5:8]) / min(min(precip[city][0:2]),precip[city][11])
    if min(avgtemp) >= 0.0 and min(avgtemp) <= 18.0 and max(avgtemp) >= 10.0:
        # Humid Subtropical (Cfa)
        if min(avgtemp) > 0.0 and max(avgtemp) > 22.0 and tempaboveten >= 4.0:
            climate[city] = 'Cfa'
        # Temperate Oceanic (Cfb)
        elif min(avgtemp) > 0.0 and max(avgtemp) < 22.0 and tempaboveten >= 4.0:
            climate[city] = 'Cfb'
        # Subpolar Oceanic (Cfc)
        elif min(avgtemp) > 0.0 and tempaboveten >= 1 and tempaboveten <= 3:
            climate[city] = 'Cfc'

        # Monsoon-influenced humid subtropical (Cwa)
        if min(avgtemp) > 0.0 and max(avgtemp) > 22.0 and tempaboveten >= 4 and warmcoldratio > 10.0:
            climate[city] = 'Cwa'
        # Subtropical Highland/Temperate Oceanic with Dry Winter (Cwb)
        elif min(avgtemp) > 0.0 and max(avgtemp) < 22.0 and tempaboveten >= 4 and warmcoldratio > 10.0:
            climate[city] = 'Cwb'
        # Cold Subtropical Highland/Subpolar Oceanic with Dry Winter (Cwc)
        elif min(avgtemp) > 0.0 and tempaboveten >= 1 and tempaboveten <= 3 and warmcoldratio > 10.0:
            climate[city] = 'Cwc'

        # Hot summer Mediterranean (Csa)
        if min(avgtemp) > 0.0 and max(avgtemp) > 22.0 and tempaboveten >= 4 and \
            coldwarmratio >= 3.0 and min(precip[city][5:8]) < 30.0:
            climate[city] = 'Csa'
        # Warm summer Mediterranean (Csb)
        elif min(avgtemp) > 0.0 and max(avgtemp) < 22.0 and tempaboveten >= 4 and \
            coldwarmratio >= 3.0 and min(precip[city][5:8]) < 30.0:
            climate[city] = 'Csb'
        # Cool summer Mediterranean (Csc)
        elif min(avgtemp) > 0.0 and tempaboveten >= 1 and tempaboveten <= 3 and \
            coldwarmratio >= 3.0 and min(precip[city][5:8]) < 30.0:
            climate[city] = 'Csc'

        if 'C' in climate[city]:
            continue

    # Group D (Continental)
    if min(avgtemp) < 0.0 and max(avgtemp) > 10.0:
        # Hot summer humid continental (Dfa)
        if max(avgtemp) > 22.0 and tempaboveten >= 4:
            climate[city] = 'Dfa'
        # Warm summer humid continental (Dfb)
        elif max(avgtemp) < 22.0 and tempaboveten >= 4:
            climate[city] = 'Dfb'
        # Subarctic (Dfc)
        elif tempaboveten >= 1 and tempaboveten <= 3:
            climate[city] = 'Dfc'
        # Extremely cold subarctic (Dfd)
        elif min(avgtemp) < -38.0 and tempaboveten >=1 and tempaboveten <= 3:
            climate[city] = 'Dfd'

        # Monsoon-influenced hot humid continental (Dwa)
        if max(avgtemp) > 22.0 and tempaboveten >= 4 and warmcoldratio >= 10:
            climate[city] = 'Dwa'
        # Monsoon-influenced warm humid continental (Dwb)
        elif max(avgtemp) < 22.0 and tempaboveten >= 4 and warmcoldratio >= 10:
            climate[city] = 'Dwb'
        # Monsoon-influenced subarctic (Dwc)
        elif tempaboveten >= 1 and tempaboveten <= 3 and warmcoldratio >= 10:
            climate[city] = 'Dwc'
        # Monsoon-influenced extremely cold subarctic (Dwd)
        elif min(avgtemp) < -38.0 and tempaboveten >= 1 and tempaboveten <= 3 and warmcoldratio >= 10:
            climate[city] = 'Dwd'

        # Hot, dry continental (Dsa)
        if max(avgtemp) > 22.0 and tempaboveten >= 4 and coldwarmratio >= 3 and min(precip[city][5:8]) < 30.0:
            climate[city] = 'Dsa'
        # Warm, dry continental (Dsb)
        elif max(avgtemp) < 22.0 and tempaboveten >= 4 and coldwarmratio >= 3 and min(precip[city][5:8]) < 30.0:
            climate[city] = 'Dsb'
        # Dry, subarctic (Dsc)
        elif tempaboveten >= 1 and tempaboveten <= 3 and coldwarmratio >= 1 and coldwarmratio >= 3 and \
            min(precip[city][5:8]) < 30.0:
            climate[city] = 'Dsc'
        # Extremely cold, dry subarctic (Dsd)
        elif min(avgtemp) < -38.0 and tempaboveten >= 1 and tempaboveten <= 3 and coldwarmratio >= 3 and \
            min(precip[city][5:8]) < 30.0:
            climate[city] = 'Dsd'

        if 'D' in climate[city]:
            continue

    # Group E (Polar and alpine)
    if max(avgtemp) < 10.0:
        # Tundra (ET)
        if max(avgtemp) > 0.0:
            climate[city] = 'ET'
        # Ice cap (EF)
        else:
            climate[city] = 'EF'
