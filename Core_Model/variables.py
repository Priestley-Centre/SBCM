#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""variables.py
All the variables required for model functionality
Explanations are within the code.
"""

# Species codes
SPP = ["NE_MBB", "NE_OH", "NE_OP", "SC_OH", "SC_OP", "SC_SLP", "SE_SLP", "SE_LSP"]

# value for carbon fertilisation effect (this is only static at present, but could be made dynamic later)
f_value = 1.106342276479857


# X values for original forest carbon data
x_type1 = [0, 5, 15, 25, 35, 45, 55, 65, 75, 85, 95, 105, 115, 125]
x_type2 = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90]

# Y values for original forest carbon data (broken down by species)
original_biomass_data = {
    "NE_MBB": {
        "x": x_type1,
        "y": [
            2.1,
            9.5,
            33.7,
            55.0,
            74.5,
            89.5,
            102.8,
            114.8,
            125.5,
            135.2,
            143.8,
            151.3,
            157.9,
            163.7,
        ],
    },
    "NE_OH": {
        "x": x_type1,
        "y": [
            2.1,
            9,
            44.9,
            73.8,
            98.0,
            120,
            138.6,
            156.1,
            172.4,
            187.8,
            202.2,
            215.6,
            228.2,
            239.9,
        ],
    },
    "NE_OP": {
        "x": x_type1,
        "y": [
            4.2,
            10.4,
            30.3,
            51.5,
            70.5,
            87.2,
            101.5,
            115.3,
            125.9,
            135.4,
            143.9,
            151.4,
            157.9,
            163.5,
        ],
    },
    "SC_OH": {
        "x": x_type2,
        "y": [
            4.2,
            14.4,
            24.9,
            33.7,
            42.9,
            51.5,
            59.7,
            68.6,
            79.1,
            88.5,
            97.5,
            106.0,
            114.0,
            121.4,
            128.6,
            134.9,
            140.8,
            146.5,
            151.6,
        ],
    },
    "SC_OP": {
        "x": x_type2,
        "y": [
            4.2,
            13.1,
            25.1,
            35.4,
            45.1,
            54.1,
            62.3,
            70.9,
            79.4,
            87.3,
            94.2,
            101.0,
            108.0,
            113.4,
            118.7,
            124.5,
            129.2,
            133.4,
            137.8,
        ],
    },
    "SC_SLP": {
        "x": x_type2,
        "y": [
            4.1,
            14.9,
            38.1,
            72.5,
            102.9,
            122.0,
            130.5,
            131.6,
            132.5,
            133.5,
            134.4,
            134.4,
            134.4,
            134.4,
            134.4,
            134.4,
            134.4,
            134.4,
            134.4,
        ],
    },
    "SE_SLP": {
        "x": x_type2,
        "y": [
            4.1,
            15.0,
            35.7,
            71.1,
            106.0,
            127.9,
            137.8,
            139.1,
            140.2,
            141.1,
            142.2,
            142.2,
            142.2,
            142.2,
            142.2,
            142.2,
            142.2,
            142.2,
            142.2,
        ],
    },
    "SE_LSP": {
        "x": x_type2,
        "y": [
            4.1,
            12.8,
            31.1,
            63.9,
            94.9,
            117.2,
            126.5,
            127.7,
            128.7,
            129.7,
            130.7,
            130.7,
            130.7,
            130.7,
            130.7,
            130.7,
            130.7,
            130.7,
            130.7,
        ],
    },
}

# Y values for original forest *soil* carbon data (broken down by species)
original_soil_data = {
    "NE_MBB": {
        "x": x_type1,
        "y": [
            129.3,
            112.3,
            100.6,
            100.3,
            102.8,
            106.2,
            109.4,
            112.6,
            115.3,
            117.7,
            119.8,
            121.6,
            123.4,
            124.8,
        ],
    },
    "NE_OH": {
        "x": x_type1,
        "y": [
            108.0,
            90.9,
            77.3,
            72.4,
            71.8,
            73.1,
            74.9,
            76.8,
            78.7,
            80.6,
            82.2,
            83.7,
            85.3,
            86.7,
        ],
    },
    "NE_OP": {
        "x": x_type1,
        "y": [
            126.6,
            110.7,
            99.4,
            97.6,
            99.3,
            102.1,
            105.1,
            108.3,
            111.1,
            113.6,
            115.9,
            118.0,
            119.9,
            121.6,
        ],
    },
    "SC_OH": {
        "x": x_type2,
        "y": [
            56.3,
            49.2,
            48.1,
            47.9,
            48.6,
            49.3,
            50.4,
            51.4,
            52.6,
            53.7,
            54.7,
            55.7,
            56.6,
            57.5,
            58.3,
            59.0,
            59.7,
            60.4,
            60.9,
        ],
    },
    "SC_OP": {
        "x": x_type2,
        "y": [
            64.4,
            58.2,
            57.6,
            57.9,
            58.5,
            59.2,
            60.0,
            60.8,
            61.6,
            62.4,
            63.2,
            63.9,
            64.5,
            65.2,
            65.8,
            66.4,
            66.9,
            67.5,
            68.0,
        ],
    },
    "SC_SLP": {
        "x": x_type2,
        "y": [
            74.5,
            64.6,
            62.2,
            61.9,
            62.2,
            62.4,
            62.4,
            62.3,
            62.4,
            62.4,
            62.5,
            62.7,
            62.9,
            63.0,
            63.2,
            63.4,
            63.5,
            63.7,
            63.9,
        ],
    },
    "SE_SLP": {
        "x": x_type2,
        "y": [
            105.5,
            96.0,
            93.6,
            93.7,
            94.2,
            94.7,
            94.8,
            94.8,
            94.8,
            94.8,
            94.9,
            95.1,
            95.3,
            95.4,
            95.6,
            95.8,
            95.9,
            96.2,
            96.3,
        ],
    },
    "SE_LSP": {
        "x": x_type2,
        "y": [
            143.3,
            133.2,
            130.3,
            129.7,
            129.9,
            130.2,
            130.1,
            130.0,
            130.0,
            130.0,
            130.1,
            130.3,
            130.5,
            130.6,
            130.8,
            131.0,
            131.1,
            131.3,
            131.5,
        ],
    },
}

# Forest growth variables
"""forest variables:
    B = max possible carbon stored
    phi_ab = Reference rate of C flux from atmosphere to biomass in Richards model
    k = fractional flux (constant)
    v = shape parameter (constant)
    phi_ba = Fractional rate of C flux from biomass to atmosphere
    phi_bs = Fractional rate of C flux from biomass to soils
    phi_sa = Fractional rate of C flux from soils to atmosphere
    forest_start = starting value for forest carbon (at the end of year 0)
    soil_start = starting value for forest soil carbon (at the end of year 0)
    biomass_eqm = final equilibrium for forest carbon (calculated using single use code)
    soil_eqm = final equilibrium for soil carbon (calculated using single use code)"""

forest_variables = {
    "NE_MBB": {
        "B": 1437.04,
        "phi_ab": 0.140193,
        "k": 0.00342002,
        "v": 0.0899299,
        "phi_ba": 0.0190583,
        "phi_bs": 0.0117339,
        "phi_sa": 0.0101687,
        "forest_start": 2.1,
        "soil_start": 129.3,
        "biomass_eqm": 187.68065529741608,
        "soil_eqm": 216.56908367778937,
    },
    "NE_OH": {
        "B": 1358.99,
        "phi_ab": 0.0665428,
        "k": 0.00439655,
        "v": 0.120641,
        "phi_ba": 0.00680838,
        "phi_bs": 0.00842004,
        "phi_sa": 0.0160806,
        "forest_start": 2.1,
        "soil_start": 108,
        "biomass_eqm": 316.66315186927415,
        "soil_eqm": 165.80950992284795,
    },
    "NE_OP": {
        "B": 338.89,
        "phi_ab": 0.160851,
        "k": 0.00945311,
        "v": 0.126451,
        "phi_ba": 0.00403601,
        "phi_bs": 0.0116687,
        "phi_sa": 0.0103839,
        "forest_start": 4.2,
        "soil_start": 126.6,
        "biomass_eqm": 176.32746559581733,
        "soil_eqm": 198.14446381397158,
    },
    "SC_OH": {
        "B": 294.396,
        "phi_ab": 0.188609,
        "k": 0.0192067,
        "v": 0.079026,
        "phi_ba": 0,
        "phi_bs": 0.00564449,
        "phi_sa": 0.00700899,
        "forest_start": 4.2,
        "soil_start": 56.3,
        "biomass_eqm": 217.13590147824436,
        "soil_eqm": 174.8641993404073,
    },
    "SC_OP": {
        "B": 601.541,
        "phi_ab": 0.0255501,
        "k": 0.00319981,
        "v": 1.07631,
        "phi_ba": 0.0244426,
        "phi_bs": 0.00465856,
        "phi_sa": 0.00488477,
        "forest_start": 4.2,
        "soil_start": 64.4,
        "biomass_eqm": 180.47288844101357,
        "soil_eqm": 172.11532562961082,
    },
    "SC_SLP": {
        "B": 166.721,
        "phi_ab": 0.23104,
        "k": 0.00491518,
        "v": 0.866791,
        "phi_ba": 0.0377219,
        "phi_bs": 0.0072412,
        "phi_sa": 0.0145183,
        "forest_start": 4.1,
        "soil_start": 74.5,
        "biomass_eqm": 134.2148441774475,
        "soil_eqm": 66.94148279466094,
    },
    "SE_SLP": {
        "B": 147.342,
        "phi_ab": 0.18459,
        "k": 0.00507295,
        "v": 0.983193,
        "phi_ba": 0.00118025,
        "phi_bs": 0.00636347,
        "phi_sa": 0.00877681,
        "forest_start": 4.1,
        "soil_start": 105.5,
        "biomass_eqm": 141.96145393361965,
        "soil_eqm": 102.92662747205006,
    },
    "SE_LSP": {
        "B": 136.134,
        "phi_ab": 0.19312,
        "k": 0.00353541,
        "v": 0.95263,
        "phi_ba": 0.0009154,
        "phi_bs": 0.00774907,
        "phi_sa": 0.00728868,
        "forest_start": 4.1,
        "soil_start": 143.3,
        "biomass_eqm": 130.45314552144953,
        "soil_eqm": 138.6932279048998,
    },
}

# Efficiency and carbon intensity parameters for coal and biomass use
# Original value and new (revised values)

forest_use = {
    "eff1": 0.25,  # combustion efficiency for biomass fuels (%)
    "eff2": 0.725,  # processing efficiency for biomass fuels (%)
    "emit1": 0.0012,  # carbon intensity of biomass fuel supply chain (tC/GJ)
    "emit2": 0.027,
}  # carbon intensity of biomass fuel combustion (tC/GJ)}

coal_use = {
    "eff1": 0.35,  # combustion efficiency for fossil fuels (%)
    "eff2": 0.89,  # processing efficiency for fossil fuels (%)
    "emit1": 0.0015,  # carbon intensity of fossil fuel supply chain (tC/GJ)
    "emit2": 0.025,
}  # carbon intensity of fossil fuel combustion (tC/GJ)}

new_forest_use = {
    "eff1": 0.385,  # combustion efficiency for biomass fuels (%)
    "eff2": 0.725,  # processing efficiency for biomass fuels (%)
    "emit1": 0.0012,  # carbon intensity of biomass fuel supply chain (tC/GJ)
    "emit2": 0.027,
}  # carbon intensity of biomass fuel combustion (tC/GJ)}

new_coal_use = {
    "eff1": 0.356,  # combustion efficiency for fossil fuels (%)
    "eff2": 0.89,  # processing efficiency for fossil fuels (%)
    "emit1": 0.0015,  # carbon intensity of fossil fuel supply chain (tC/GJ)
    "emit2": 0.025,
}  # carbon intensity of fossil fuel combustion (tC/GJ)}
