# SBCM model version 0.3

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A simple model designed to compare the relative emissions associated with
electricity generation from biomass and coal. The original version was based
on a model by Sterman et al discussed in Sterman et al (2018)
"Does replacing coal with wood lower CO2 emissions? Dynamic lifecycle
analysis of wood bioenergy" DOI 10.1088/1748-9326/aaa512/

Notes:
    https://numpydoc.readthedocs.io/en/latest/format.html for docstring formatting

Outline of file structure
TODO explain why they are in a funny order

Scenario
    __init__
    initialise
    fell
    runstep
    report
    spinup
    describe

"""
# Libraries
import pandas as pd
import numpy as np
import functions as func
import formatting as form
import variables as var
from variables import forest_variables as fv


class Scenario:
    """Sets up a felling and counterfactual scenario for comparison
    """

    def __init__(self, spp):
        """
        based on a common energy input, and a range of variables describing the
        behaviour of forest growth and management. Most are fairly self-explanatory.
        TODO More info to go here if there is time.
        """
        # Input Variables
        self.energy = 1 * 10 ** 9
        self.spp = spp
        self.forest_variables = {
            "B": fv[spp]["B"],
            "phi_ab": fv[spp]["phi_ab"],
            "k": fv[spp]["k"],
            "v": fv[spp]["v"],
            "phi_ba": fv[spp]["phi_ba"],
            "phi_bs": fv[spp]["phi_bs"],
            "phi_sa": fv[spp]["phi_sa"],
        }
        self.cf_variables = var.new_coal_use
        self.bio_variables = var.new_forest_use

        # Starting conditions - these can be varied but are set to initial values
        # based on Sterman et al.
        self.no_fell = False
        self.soil_only = False  # <-- Sterman scenario s5 - soil emissions only
        self.biomass = fv[spp]["biomass_eqm"]  # <-- import eqm values for biomass
        self.soil = fv[spp]["soil_eqm"]  # <--  and soil
        self.forest_start = fv[spp]["forest_start"]
        self.soil_start = fv[spp]["soil_start"]

        self.max_carbon = self.biomass + self.soil  # <--  max possible carbon on site

        # Felling info
        self.fell_age = False  # <-- false unless we have a specific age
        self.felling_intensity = 0.95  # <-- decimal percent
        self.thinning_ages = False  # <-- False or a list of ages which must be equal to
        self.thinning_intensities = []  # <-- this which is a list of decimal %

        # Dynamic variables
        self.area = 0  # <-- not really dynamic
        self.age = 0  # <-- changes every year...
        self.payback = -999

        # Output variables
        self.cf_emission = 0.0  # <-- these change every year
        self.bio_emission = 0.0
        self.felled_biomass = 0.0
        self.carbon_saved = 0.0
        self.gross_carbon_debt = 0.0

        # Output variables (lists)
        self.time_list = [-1]
        self.cf_emissions_list = [0]
        self.bio_emissions_list = [0]
        self.felled_biomass_list = [0]  # <-- TODO SET THIS AS ZERO?
        self.biomass_carbon_list = [0]
        self.soil_carbon_list = [0]
        self.gross_carbon_debt_list = [0]
        self.carbon_saved_list = [0]
        # TODO check that we've included all the variables we need here
        # (to avoid confusion from adding variables on the fly)

    def initialise(self):
        """An artificial initialisation function to allow us to modify variables
        before we set up the model ready to run.
        Calculates values for year zero
        """
        # CF emissions at year zero
        cf_fuel = func.energy2fuel(
            self.energy, self.cf_variables["eff1"], self.cf_variables["eff2"]
        )

        self.cf_emission = func.fuel2emission(
            cf_fuel, self.cf_variables["emit1"], self.cf_variables["emit2"]
        )

        #  Biomass emissions at year zero
        bio_fuel = func.energy2fuel(
            self.energy, self.bio_variables["eff1"], self.bio_variables["eff2"]
        )

        self.bio_emission = func.fuel2emission(
            bio_fuel, self.bio_variables["emit1"], self.bio_variables["emit2"]
        )

        self.area = func.fuel2forest(
            self.bio_variables["emit2"], bio_fuel, self.felling_intensity, self.biomass
        )

        # Year zero output
        if self.no_fell == False:
            self.felled_biomass = self.biomass * self.felling_intensity
            self.felled_biomass_list.append(self.felled_biomass)
            self.biomass = self.biomass - self.felled_biomass
            self.soil = self.soil  # <-- put this in just to make it clear

        elif self.no_fell == True:
            self.felled_biomass = 0
            self.felled_biomass_list.append(self.felled_biomass)
            self.biomass = self.forest_start
            self.soil = self.soil_start

        self.gross_carbon_debt = self.max_carbon - (self.biomass + self.soil)

        #        # update running values
        self.cf_emissions_list.append(self.cf_emission)
        self.bio_emissions_list.append(self.bio_emission)
        self.biomass_carbon_list.append(self.forest_start)
        self.soil_carbon_list.append(self.soil_start)
        self.gross_carbon_debt_list.append(self.gross_carbon_debt)
        self.time_list.append(self.time_list[-1] + 1)
        self.carbon_saved = self.cf_emission - self.bio_emission
        self.carbon_saved_list.append(self.carbon_saved)

    def fell(self, intensity, final=False):
        """fells forests based on a felling intesnity
        changes the standing volume, as well as the resulting emissions from both the
        biomass and CF scenarios
        """
        # Identify how much biomass has been felled
        self.felled_biomass = self.biomass * intensity
        if self.felled_biomass_list == []:
            self.felled_biomass_list.append(self.felled_biomass)
        else:
            self.felled_biomass_list.append(
                self.felled_biomass + self.felled_biomass_list[-1]
            )

        # What is that in embodied fuel GJ?
        bio_fuel = func.forest2fuel(
            self.bio_variables["emit2"], self.area, intensity, self.biomass
        )
        # What is the new biomass value?
        self.biomass = self.biomass - self.felled_biomass  # <-- this must come here
        # because otherwise we can't use the previous standing value to caluclate the
        # fuel energy yield

        # How much useful energy have we produced from that much fuel?
        energy = func.fuel2energy(
            bio_fuel, self.bio_variables["eff1"], self.bio_variables["eff2"]
        )
        # and how much CF fuel ould we need to achieve the same result?
        cf_fuel = func.energy2fuel(
            energy, self.cf_variables["eff1"], self.cf_variables["eff2"]
        )
        # And what would the emissions from that look like?
        self.cf_emission = (
            func.fuel2emission(
                cf_fuel, self.cf_variables["emit1"], self.cf_variables["emit2"]
            )
            + self.cf_emission
        )

        # Add this emission to the running total
        self.cf_emissions_list.append(self.cf_emission)

        # do the same calculation for biomass and add it to the *running* total
        self.bio_emission = (
            func.fuel2emission(
                bio_fuel, self.bio_variables["emit1"], self.bio_variables["emit2"]
            )
            + self.bio_emission
        )

        # Check if it's a final felling, and if it is, reset the forest age to zero.
        if final is True:
            self.age = 0

    def runstep(self):
        """Calculates the changes taking place, if we advance the forest age on by
        one year. We check to see if any felling or thinning takes place, and then
        update all the running totals based on growth, yield and emissions.
        """

        # This series of if functions checks whether it's a felling year or a thinning
        # year, and calls the fell function accordingly.
        if self.fell_age is not False and self.age >= self.fell_age:
            self.fell(self.felling_intensity, final=True)
        elif self.thinning_ages is not False and self.age in self.thinning_ages:
            i = self.thinning_ages.index(self.age)
            self.fell(self.thinning_intensities[i], final=False)
        else:
            self.cf_emissions_list.append(self.cf_emission)  # cf emission unchanged
            self.felled_biomass_list.append(self.felled_biomass_list[-1])

        # Annual growth. This is the really important bit.
        # it takes place *after* felling, so we enforce the fell, plant, grow sequence
        # as described in ch3
        calc = func.growth(
            self.biomass,
            self.soil,
            **self.forest_variables,
            f=var.f_value,
            soil_only=self.soil_only,
        )

        # update running values
        self.bio_emission = self.bio_emission + (calc["emission"] * self.area)
        self.biomass = calc["biomass"]  # per ha
        self.soil = calc["soils"]  # per ha
        self.gross_carbon_debt = self.max_carbon - (self.biomass + self.soil)
        self.carbon_saved = self.cf_emission - self.bio_emission
        # and add them to lists to show change over time
        self.bio_emissions_list.append(self.bio_emission)
        self.biomass_carbon_list.append(self.biomass)
        self.soil_carbon_list.append(self.soil)
        self.gross_carbon_debt_list.append(self.gross_carbon_debt)
        self.time_list.append(self.time_list[-1] + 1)
        self.carbon_saved_list.append(self.carbon_saved)
        # increment forest age.
        self.age = self.age + 1

    def report(self, verbose=False):
        """ returns a pandas dataframe with all the gubbins in.
        """
        # set up dataframe
        output = pd.DataFrame(index=self.time_list)
        if verbose:  # <-- printed output, if the lists don't come out at the right
            # length
            print("Checking data list lengths before adding to dataframe...\n")
            print(f"time_list length \t\t {len(self.time_list)}")
            print(f"cf_emissions length \t\t {len(self.cf_emissions_list)}")
            print(f"bio_emissions length \t\t {len(self.bio_emissions_list)}")
            print(f"felled_biomass_list length \t {len(self.felled_biomass_list)}")
            print(f"biomass_carbon_list length \t {len(self.biomass_carbon_list)}")
            print(f"soil_carbon_list length \t {len(self.soil_carbon_list)}")
            print(
                f"gross_carbon_debt_list length \t {len(self.gross_carbon_debt_list)}\n"
            )

        self.felled_biomass_list[0] = 0  # <-- fudge because of how the calculation
        # works when we initialise -
        # it just puts things out of sequence.

        # Dump it all in.
        output["cf_emissions"] = self.cf_emissions_list
        output["bio_emissions"] = self.bio_emissions_list
        output["felled_biomass"] = self.felled_biomass_list
        output["biomass_carbon"] = self.biomass_carbon_list
        output["soil_carbon"] = self.soil_carbon_list
        output["gross_c_debt"] = self.gross_carbon_debt_list
        output["carbon_saved"] = self.carbon_saved_list

        # try and work out time to payback
        try:  # <-- this doesn't always work, so if we Try, it just skips it on failure
            payback = output.index[
                output["bio_emissions"] <= output["cf_emissions"]
            ].tolist()
            #            print(payback)
            result = func.payback(payback)
            if verbose == True:
                print(f"Payback occurs during year(s) = {str(result).strip('[]')}")
            self.payback = result
        except:
            pass  # <-- just skip joyfully on if it doesn't work.
        return output

    def spinup(self, n=10, verbose=False):
        """runs the model like a maniac until we have an indication of equilibrium values
        """
        if (
            self.fell_age is False and verbose is True
        ):  # <-- skip if we've already got values
            print("Equilibrium values used, no spinup required")

        else:  # <-- otherwise give some visual indication of what's going on.
            if verbose is True:
                print(f"spinning up model for {n} rotations of {self.fell_age} years")
            duration = range(n * self.fell_age)
            for _ in duration:
                self.runstep()  # <basically run the model for evar and return the biomass
                # and soil values

    def describe(self):
        """ Gives a brief printed summary of the scenario
        """
        ha = self.area
        km = self.area * 0.01
        site_ha = f"{ha:,.0f}ha"
        site_km = f"{km:,.0f}km{chr(0x00B2)}"
        a = f"{site_ha} ({site_km})"
        b = self.fell_age
        if b is False:
            b = "no-fell strategy,"
            c = ""
        else:
            b = f"{b}-year rotation"
            c = f" ({int(np.round(self.felling_intensity*100,0))}% fell)"
        s = form.forest_labels(self.spp, short=True, eng=True)
        if self.thinning_ages is not False:
            d = f"{str([n*100 for n in self.thinning_intensities]).strip('[]')}%"
            e = f"{str(self.thinning_ages).strip('[]')}"
            d = f"with thinnings in years: {e} of intensities: {d}."
        else:
            d = "with no thinning."
            e = ""

        output = f" is {a} of {s} forest managed on a {b}{c} {d}"
        return output


if __name__ == "__main__":

    def rpt(scn):
        """Just report the soil and forest carbon"""
        print(f"soil = {scn.soil}, forest = {scn.biomass}, area={scn.area}\n")

    print("Testing basic growth model\n")
    sp = "SC_SLP"
    x = Scenario(sp)
    x.felling_intensity = 0.95
    x.cf_variables = var.coal_use
    x.bio_variables = var.forest_use
    print(x.soil)

    x.initialise()
    rpt(x)

    for _ in range(500):
        x.runstep()

    r = x.report()
    print(x.payback)

    r.to_clipboard()
