# -*- coding: utf-8 -*-
"""
A collection of functions used in the model
Many of these are based on work by Sterman et al (2018)
"Does replacing coal with wood lower CO2 emissions? Dynamic lifecycle
analysis of wood bioenergy" DOI 10.1088/1748-9326/aaa512/

List of all functions goes here:
    energy2fuel
    fuel2energy

    fuel2forest
    forest2fuel

    fuel2emission
    emission2fuel

    co2_fertilisation
    tonnes2ppm
    growth

Diagram of how the interlinked equations relate to one another.

              +-----------+
              |   ENERGY  |
              +------^----+
                   | |
       energy2fuel | | fuel2energy
                   | |
              +----v------+    fuel2forest >  +-----------+
              |    FUEL   |<=================>|  FOREST * |
              +------^----+  < forest2fuel    +-----------+
                   | |
     fuel2emission | | emission2fuel
                   | |
              +----v------+
              | EMISSIONS |
              +-----------+

* FOREST includes variable:
- biomass (quantity of carbon on site calculated using "growth" function)
- area (forest size in ha)
- felling intensity (exogenous input)

TODO add docstings

"""
# ==============================================================================
#                           Functions
# ==============================================================================

from variables import forest_variables as fv
import math as m


# ------------------------------------------------------------------------------
def energy2fuel(energy, eff1, eff2):
    """calculates fuel energy requirement (in GJ) based on energy demand and
    efficiencies of production and use. Inverse of fuel2energy
    From Sterman et al (2018) """
    fuel = energy / (eff1 * eff2)
    return fuel


# ------------------------------------------------------------------------------
def fuel2energy(fuel, eff1, eff2):
    """calculates energy available (in GJ) from a known quantity of fuel
    assuming specified efficiencies of production and use
    Inverse of energy2fuel"""
    energy = fuel * eff1 * eff2
    return energy


# ------------------------------------------------------------------------------
def fuel2forest(emit2, fuel, fell_int, biomass):
    """calculates area of forest needed to supply fuel energy, based on the
    intensity of emission, fuel energy required, felling intensity
    and biomass present on a forest site. Inverse of forest2fuel.
    From Sterman et al (2018) """
    area = emit2 * (fuel / (fell_int * biomass))
    return area


# ------------------------------------------------------------------------------
def forest2fuel(emit2, area, fell_int, biomass):
    """calculates the amount of fuel supplied by a known area of forest
    based on the intensity of emission, area, felling intensity
    and biomass present on a forest site. Inverse of fuel2forest."""
    fuel = (area * fell_int * biomass) / emit2
    return fuel


# ------------------------------------------------------------------------------
def fuel2emission(fuel, emit1, emit2):
    """calculates carbon emissions based on the amount of fuel used (GJ) and
    the carbon intensities of production and use (emit1 and emit2)
    Inverse of emission2fuel. From Sterman et al (2018) """
    emission = fuel * (emit1 + emit2)
    return emission


# ------------------------------------------------------------------------------
def emission2fuel(emission, emit1, emit2):
    """calculates carbon emissions based on the amount of fuel used (GJ) and
    the carbon intensities of production and use (emit1 and emit2)
    Inverse of fuel2emission."""
    fuel = emission / (emit1 + emit2)
    return fuel


# ------------------------------------------------------------------------------
def growth(pb, ps, B, phi_ab, k, v, phi_ba, phi_bs, phi_sa, f, soil_only=False):
    """returns a dict of (biomass carbon, soil carbon, carbon emission) as used in
    Sterman et al (2018)

    where:
    pb = previous value of biomass carbon (tonnes)
    ps = previous value of soil carbon (tonnes)
    B = max possible carbon stored (tonnes)
    phi_ab = Reference rate of C flux from atmosphere to biomass in Richards model
    k = fractional flux (constant)
    v = shape parameter (constant)
    phi_ba = Fractional rate of C flux from biomass to atmosphere
    phi_bs = Fractional rate of C flux from biomass to soils
    phi_sa = Fractional rate of C flux from soils to atmosphere
    f = the carbon fertilisation effect.
    """
    if soil_only is True:
        soils_emission = ps * phi_sa
        soils = ps - soils_emission
        result = {"biomass": 0, "soils": soils, "emission": soils_emission}
    else:
        forest_growth = (((phi_ab * pb) + (k * B)) * (1 - (pb / B) ** v)) * f
        # photosynthesis based on previous growth
        resp_emission = pb * phi_ba  # respiration. IE reemission of C to atmos
        soils_addition = pb * phi_bs  # movement of C from biomass to soils
        biomass = (
            pb + forest_growth - resp_emission - soils_addition
        )  # new biomass figure
        soils_emission = ps * phi_sa
        soils = ps + soils_addition - soils_emission
        emissions = resp_emission + soils_emission - forest_growth

        result = {"biomass": biomass, "soils": soils, "emission": emissions}
    return result


# ------------------------------------------------------------------------------
def co2_fertilisation(co2_now=760, co2_then=590, biostimm=0.42):
    """returns the biostimm coefficient
    which reflects the carbon fertilisation effect
    based on the difference between preindustrial CO2 (co2_then) in Gt and a
    modern CO2 quantity (CO2_now) and a paper by ?? which addesses
    plant responses."""
    ans = 1 + biostimm * m.log(co2_now / co2_then)
    print("\n\nf value (for CO2 fertilisation) : " + str(ans))
    return ans


# ------------------------------------------------------------------------------
def tonnes2ppm(t):
    """converts x tonnes of carbon to ppm atmospheric concentration CO2"""
    gt = t * 10 ** -9
    return gt * 0.471


# ------------------------------------------------------------------------------
def missing_elements(L, start, end):
    """
    """
    if end - start <= 1:
        if L[end] - L[start] > 1:
            yield from range(L[start] + 1, L[end])
        return

    index = start + (end - start) // 2

    # is the lower half consecutive?
    consecutive_low = L[index] == L[start] + (index - start)
    if not consecutive_low:
        yield from missing_elements(L, start, index)

    # is the upper part consecutive?
    consecutive_high = L[index] == L[end] - (end - index)
    if not consecutive_high:
        yield from missing_elements(L, index, end)


# ------------------------------------------------------------------------------
def payback(l, n=10):
    """
    """
    result = []
    x = list(missing_elements(l, -1, len(l) - 1))
    #    print(x)
    result.append(max(x) + 1)
    for _ in range(n):
        try:
            x = list(missing_elements(x, 0, len(x) - 1))
            #            print(x)
            result.append(min(x))
        except:
            pass
    result.sort()
    #    result = [i-1 for i in result]
    return result


if __name__ == "__main__":

    x = energy2fuel(5, 4, 3)
    print(x, end=" ")
    y = fuel2energy(x, 4, 3)
    print(y)

    x = fuel2forest(5, 4, 3, 4)
    print(x, end=" ")
    y = forest2fuel(5, x, 4, 3)
    print(y)

    x = fuel2emission(5, 4, 3)
    print(x, end=" ")
    y = emission2fuel(x, 4, 3)
    print(y)

    var = {
        "B": fv["NE_MBB"]["B"],
        "phi_ab": fv["NE_MBB"]["phi_ab"],
        "k": fv["NE_MBB"]["k"],
        "v": fv["NE_MBB"]["v"],
        "phi_ba": fv["NE_MBB"]["phi_ba"],
        "phi_bs": fv["NE_MBB"]["phi_bs"],
        "phi_sa": fv["NE_MBB"]["phi_sa"],
    }

    x = growth(1, 1, **var, f=1, soil_only=False)
    print(x["biomass"])
    print(x["soils"])
    print(x["emission"])
