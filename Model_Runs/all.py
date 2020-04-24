# -*- coding: utf-8 -*-
"""

"""

note = """
########################################################################################

                    Running everything. This will take a LONG TIME.

                    Please be aware that the progress bar is deceptive
                    it will look a lot like it has stopped working.
                    Of course this *might* have happened, but you can't
                    really be sure until you have allowed the code to
                    run for a good long time. In particular, stages
                    2 and 5 are very slow (5 minutes plus) so I recommend
                    a tea break while it all chugs away. The whole thing 
                    takes about 25 minutes on my machine ~WR

########################################################################################


"""
import warnings
from formatting import title

# https://progressbar-2.readthedocs.io/en/latest/index.html
import progressbar

print(title)
print(note)
warnings.simplefilter("ignore")
with progressbar.ProgressBar(max_value=15) as bar:
    import _01_biomass_equilibrium as _01

    #    _01 runs when it is imported
    bar.update(1)

    import _02_biomass_rmse as _02

    #    _02 runs when it is imported
    bar.update(2)

    import _03_curve_fit as _03

    bar.update(3)
    #    _03 runs when it is imported

    import _04_curve_fit_subset as _04

    bar.update(4)
    #    _04 runs when it is imported

    import _04a_curve_fit_best as _04a

    bar.update(5)
    #    _04a runs when it is imported

    import _05_full_params_run as _05

    bar.update(6)
    #    _05 runs when it is imported

    import _05a_uncertainty_plumes as _05a

    bar.update(7)
    #    _05a runs when it is imported

    import _06_years_to_maturity_forest as _06

    bar.update(8)
    #    _06 runs when it is imported

    import _06a_years_to_maturity_soil as _06a

    bar.update(9)
    #    _06a runs when it is imported

    import _07_years_to_payback as _07

    bar.update(10)
    #    _07 runs when it is imported

    import _07a_fx_on_payback as _07a

    bar.update(11)
    #    _07a runs when it is imported

    import _08_time_variability_comparison as _08

    bar.update(12)
    #    _08 runs when it is imported

    import _08a_time_variability_comaprison as _08a

    bar.update(13)
    #    _08a runs when it is imported

    import _09_growth_model_illustration as _09

    bar.update(14)
    #    _09 runs when it is imported

    import _10_error_margins as _10

    bar.update(15)
#    _10 runs when it is imported
