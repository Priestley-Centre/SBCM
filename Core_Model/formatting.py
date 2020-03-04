# -*- coding: utf-8 -*-
"""
contains three functions:
mpl_font_setup which sets up the correct fonts for graph output
sfig saves the current figure with common variables
forest labels which returns the text labels for each forest type for presentation.
"""
# ==============================================================================
#                           Functions
# ==============================================================================
import warnings
import matplotlib
import matplotlib.pyplot as plt
from time import perf_counter, strftime, localtime
from datetime import timedelta
from variables import SPP as spp


def mpl_font_setup(font_type="times New Roman"):
    """
    """
    try:
        # This is bnecessary to correct the weird mpl handling of italic TNR
        del matplotlib.font_manager.weight_dict["roman"]
        matplotlib.font_manager._rebuild()
    # https://stackoverflow.com/a/44386835/4741979
    except:
        pass

    with warnings.catch_warnings():
        # gets rid of an annoying matplotlib warning because spyder is already
        # running a graphic backend
        warnings.simplefilter("ignore")
    #        matplotlib.use('TkAgg')
    plt.ioff()

    matplotlib.rcParams["mathtext.fontset"] = "custom"
    matplotlib.rcParams["mathtext.cal"] = font_type
    matplotlib.rcParams["mathtext.rm"] = font_type
    matplotlib.rcParams["mathtext.it"] = font_type + ":italic"
    matplotlib.rcParams["mathtext.bf"] = font_type + ":bold"
    plt.rcParams["font.family"] = font_type


# def timelog(log="log", time_log=[0, 0]):
#    now = perf_counter()
#    if time_log[1] == 0:
#        output = f"{'-'*120}\n{strftime('%H:%M:%S', localtime())}\t{log:30}"
#    else:
#        output = (
#            f"{'-'*120}\n{strftime('%H:%M:%S', localtime())}"
#            + f"\t{log:30}\t{timedelta(seconds=now-time_log[0])} "
#            + f"elapsed\t({timedelta(seconds=now-time_log[1])} for this block)\n"
#        )
#    print(output)
#    return [time_log[0], now]


def forest_labels(text, short="star", eng=False):
    """Returns the text label of the species code"""
    name_dict = {
        "NE_MBB": r"NE $Acer$ / $Fagus$ / $Betula$",
        "NE_OH": r"NE $Quercus$ / $Carya$",
        "NE_OP": r"NE $Quercus$ / $Pinus$",
        "SC_OH": r"SC $Quercus$ / $Carya$",
        "SC_OP": r"SC $Quercus$ / $Pinus$",
        "SC_SLP": r"SC $P. taeda$ / $P. echinata$ plantation",  # shortleaf / loblolly
        "SE_SLP": r"SE $P. taeda$ / $P. echinata$ plantation",  # shortleaf / loblolly
        "SE_LSP": r"SE $P. palustris$ / $P. elliottii$ plantation",  # longleaf / slash
    }

    name_dict_short = {
        "NE_MBB": r"NE $Acer$ / $Fagus$ / $Betula$",
        "NE_OH": r"NE $Quercus$ / $Carya$",
        "NE_OP": r"NE $Quercus$ / $Pinus$",
        "SC_OH": r"SC $Quercus$ / $Carya$",
        "SC_OP": r"SC $Quercus$ / $Pinus$",
        "SC_SLP": r"SC $P. taeda$ / $P. echinata$",  # shortleaf / loblolly
        "SE_SLP": r"SE $P. taeda$ / $P. echinata$",  # shortleaf / loblolly
        "SE_LSP": r"SE $P. palustris$ / $P. elliottii$",  # longleaf / slash
    }

    name_dict_star = {
        "NE_MBB": r"NE $Acer$ / $Fagus$ / $Betula$",
        "NE_OH": r"NE $Quercus$ / $Carya$",
        "NE_OP": r"NE $Quercus$ / $Pinus$",
        "SC_OH": r"SC $Quercus$ / $Carya$",
        "SC_OP": r"SC $Quercus$ / $Pinus$",
        "SC_SLP": r"SC $P. taeda$ / $P. echinata$*",  # shortleaf / loblolly
        "SE_SLP": r"SE $P. taeda$ / $P. echinata$*",  # shortleaf / loblolly
        "SE_LSP": r"SE $P. palustris$ / $P. elliottii$*",  # longleaf / slash
    }

    name_dict_eng = {
        "NE_MBB": r"NE maple / beech / birch",
        "NE_OH": r"NE oak / hickory",
        "NE_OP": r"NE oak / pine",
        "SC_OH": r"SC oak / hickory",
        "SC_OP": r"SC oak / pine",
        "SC_SLP": r"SC shortleaf / loblolly pine plantation",
        "SE_SLP": r"SE shortleaf / loblolly pine plantation",
        "SE_LSP": r"SE longleaf / slash pine plantation",
    }

    name_dict_eng_short = {
        "NE_MBB": r"NE maple / beech / birch",
        "NE_OH": r"NE oak / hickory",
        "NE_OP": r"NE oak / pine",
        "SC_OH": r"SC oak / hickory",
        "SC_OP": r"SC oak / pine",
        "SC_SLP": r"SC shortleaf / loblolly pine",
        "SE_SLP": r"SE shortleaf / loblolly pine",
        "SE_LSP": r"SE longleaf / slash pine",
    }

    name_dict_eng_star = {
        "NE_MBB": r"NE maple / beech / birch",
        "NE_OH": r"NE oak / hickory",
        "NE_OP": r"NE oak / pine",
        "SC_OH": r"SC oak / hickory",
        "SC_OP": r"SC oak / pine",
        "SC_SLP": r"SC shortleaf / loblolly pine*",
        "SE_SLP": r"SE shortleaf / loblolly pine*",
        "SE_LSP": r"SE longleaf / slash pine*",
    }

    if short is True and eng is False:
        output = name_dict_short[text]
    elif short is False and eng is False:
        output = name_dict[text]
    elif short == "star" and eng is False:
        output = name_dict_star[text]

    elif short is True and eng is True:
        output = name_dict_eng_short[text]
    elif short is False and eng is True:
        output = name_dict_eng[text]
    elif short == "star" and eng is True:
        output = name_dict_eng_star[text]
    else:
        output = name_dict_eng_star[text]

    return output


title = """
                        ███████╗██╗███╗   ███╗██████╗ ██╗     ███████╗
                        ██╔════╝██║████╗ ████║██╔══██╗██║     ██╔════╝
                        ███████╗██║██╔████╔██║██████╔╝██║     █████╗
                        ╚════██║██║██║╚██╔╝██║██╔═══╝ ██║     ██╔══╝
                        ███████║██║██║ ╚═╝ ██║██║     ███████╗███████╗
                        ╚══════╝╚═╝╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝

            ██████╗ ██╗ ██████╗ ███████╗███╗   ██╗███████╗██████╗  ██████╗██╗   ██╗
            ██╔══██╗██║██╔═══██╗██╔════╝████╗  ██║██╔════╝██╔══██╗██╔════╝╚██╗ ██╔╝
            ██████╔╝██║██║   ██║█████╗  ██╔██╗ ██║█████╗  ██████╔╝██║  ███╗╚████╔╝
            ██╔══██╗██║██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗██║   ██║ ╚██╔╝
            ██████╔╝██║╚██████╔╝███████╗██║ ╚████║███████╗██║  ██║╚██████╔╝  ██║
            ╚═════╝ ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝   ╚═╝

     ██████╗ ██████╗ ███╗   ███╗██████╗  █████╗ ██████╗ ██╗███████╗ ██████╗ ███╗   ██╗
    ██╔════╝██╔═══██╗████╗ ████║██╔══██╗██╔══██╗██╔══██╗██║██╔════╝██╔═══██╗████╗  ██║
    ██║     ██║   ██║██╔████╔██║██████╔╝███████║██████╔╝██║███████╗██║   ██║██╔██╗ ██║
    ██║     ██║   ██║██║╚██╔╝██║██╔═══╝ ██╔══██║██╔══██╗██║╚════██║██║   ██║██║╚██╗██║
    ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║     ██║  ██║██║  ██║██║███████║╚██████╔╝██║ ╚████║
     ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝

                        ███╗   ███╗ ██████╗ ██████╗ ███████╗██╗
                        ████╗ ████║██╔═══██╗██╔══██╗██╔════╝██║
                        ██╔████╔██║██║   ██║██║  ██║█████╗  ██║
                        ██║╚██╔╝██║██║   ██║██║  ██║██╔══╝  ██║
                        ██║ ╚═╝ ██║╚██████╔╝██████╔╝███████╗███████╗
                        ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚══════╝
"""

if __name__ == "__main__":  # Horrible code.
    for sp in spp:
        for lan in [True]:
            print(forest_labels(sp, eng=lan, short=False))
