"""
Test to see if the advanced options work as expected
"""
import sys
from pathlib import Path
from typing import Tuple

import numpy as np
import PySide6.QtWidgets as QtW
import pandas as pd

from GHEtool import Borefield, FOLDER, FluidData, GroundConstantTemperature, GroundFluxTemperature, PipeData, GroundTemperatureGradient
from GHEtool.gui.data_2_borefield_func import data_2_borefield
from GHEtool.gui.gui_classes.gui_combine_window import MainWindow
from GHEtool.gui.gui_classes.translation_class import Translations
from GHEtool.gui.gui_structure import GUI, GuiStructure
from ScenarioGUI import load_config
import pygfunction as gt

load_config(Path(__file__).parent.parent.joinpath("gui_config.ini"))

sys.setrecursionlimit(1500)


def test_advanced_options(qtbot):
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=Borefield,
                             data_2_results_function=data_2_borefield)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=Borefield,
                             data_2_results_function=data_2_borefield)
    main_window.save_scenario()

    gs = main_window.gui_structure

    assert gs.category_advanced_options.is_hidden()
    gs.option_advanced_options.set_value(1)
    assert not gs.category_advanced_options.is_hidden()
    gs.aim_req_depth.widget.click()

    main_window.start_current_scenario_calculation(True)
    with qtbot.waitSignal(main_window.threads[-1].any_signal, raising=False) as blocker:
        main_window.threads[-1].run()
        main_window.threads[-1].any_signal.connect(main_window.thread_function)

    main_window.display_results()
    assert gs.result_text_depth.label.text() == 'Depth: 115.13 m'

    gs.option_atol.set_value(25)
    gs.option_rtol.set_value(20)
    main_window.start_current_scenario_calculation(True)
    with qtbot.waitSignal(main_window.threads[-1].any_signal, raising=False) as blocker:
        main_window.threads[-1].run()
        main_window.threads[-1].any_signal.connect(main_window.thread_function)

    main_window.display_results()
    assert gs.result_text_depth.label.text() == 'Depth: 115.15 m'