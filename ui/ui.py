# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import sys


config_path = "files\\config.txt"


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(732, 441)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 80, 111, 16))
        self.label.setObjectName("label")
        self.transmission_rate_slider = QtWidgets.QSlider(self.centralwidget)
        self.transmission_rate_slider.setGeometry(QtCore.QRect(60, 100, 160, 22))
        self.transmission_rate_slider.setMaximum(100)
        self.transmission_rate_slider.setSingleStep(1)
        self.transmission_rate_slider.setProperty("value", 50)
        self.transmission_rate_slider.setOrientation(QtCore.Qt.Horizontal)
        self.transmission_rate_slider.setObjectName("transmission_rate_slider")
        self.transmission_rate_slider.setToolTip(
            "Chance of a dot to infect another dot"
        )
        self.mortality_rate_slider = QtWidgets.QSlider(self.centralwidget)
        self.mortality_rate_slider.setGeometry(QtCore.QRect(60, 150, 160, 22))
        self.mortality_rate_slider.setMaximum(1000)
        self.mortality_rate_slider.setSingleStep(1)
        self.mortality_rate_slider.setProperty("value", 15)
        self.mortality_rate_slider.setOrientation(QtCore.Qt.Horizontal)
        self.mortality_rate_slider.setObjectName("mortality_rate_slider")
        self.mortality_rate_slider.setToolTip(
            "Chance of a dot to die (a value of 15 means, in percent, 1.5%)"
        )
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(60, 130, 111, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(60, 180, 161, 16))
        self.label_3.setObjectName("label_3")
        self.time_to_recover_rate_slider = QtWidgets.QSlider(self.centralwidget)
        self.time_to_recover_rate_slider.setGeometry(QtCore.QRect(60, 200, 160, 22))
        self.time_to_recover_rate_slider.setMaximum(50)
        self.time_to_recover_rate_slider.setSingleStep(1)
        self.time_to_recover_rate_slider.setProperty("value", 30)
        self.time_to_recover_rate_slider.setOrientation(QtCore.Qt.Horizontal)
        self.time_to_recover_rate_slider.setObjectName("time_to_recover_rate_slider")
        self.time_to_recover_rate_slider.setToolTip(
            "Time to recover from the disease (in days)"
        )
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(60, 230, 121, 16))
        self.label_4.setObjectName("label_4")
        self.immunity_duration_rate_slider = QtWidgets.QSlider(self.centralwidget)
        self.immunity_duration_rate_slider.setGeometry(QtCore.QRect(60, 250, 160, 22))
        self.immunity_duration_rate_slider.setMaximum(500)
        self.immunity_duration_rate_slider.setSingleStep(1)
        self.immunity_duration_rate_slider.setProperty("value", 167)
        self.immunity_duration_rate_slider.setOrientation(QtCore.Qt.Horizontal)
        self.immunity_duration_rate_slider.setObjectName(
            "immunity_duration_rate_slider"
        )
        self.immunity_duration_rate_slider.setToolTip(
            "Immunity duration (in days), when you don't have symptoms anymore and you can't get the disease nor infect others"
        )
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(300, 140, 111, 16))
        self.label_5.setObjectName("label_5")
        self.number_of_dots_slider = QtWidgets.QSlider(self.centralwidget)
        self.number_of_dots_slider.setGeometry(QtCore.QRect(300, 160, 160, 22))
        self.number_of_dots_slider.setMaximum(500)
        self.number_of_dots_slider.setMinimum(1)
        self.number_of_dots_slider.setSingleStep(1)
        self.number_of_dots_slider.setProperty("value", 500)
        self.number_of_dots_slider.setOrientation(QtCore.Qt.Horizontal)
        self.number_of_dots_slider.setObjectName("number_of_dots_slider")
        self.number_of_dots_slider.setToolTip("Number of individuals in the population")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(300, 190, 171, 16))
        self.label_6.setObjectName("label_6")
        self.minimal_distance_slider = QtWidgets.QSlider(self.centralwidget)
        self.minimal_distance_slider.setGeometry(QtCore.QRect(300, 210, 160, 22))
        self.minimal_distance_slider.setMaximum(15)
        self.minimal_distance_slider.setSingleStep(1)
        self.minimal_distance_slider.setProperty("value", 2)
        self.minimal_distance_slider.setOrientation(QtCore.Qt.Horizontal)
        self.minimal_distance_slider.setObjectName("minimal_distance_slider")
        self.minimal_distance_slider.setToolTip(
            "Minimal distance between two dots (according to what i've found, a dot measures approximately 0.8 unit"
        )
        self.dot_shaped_radio = QtWidgets.QRadioButton(self.centralwidget)
        self.dot_shaped_radio.setGeometry(QtCore.QRect(510, 270, 82, 17))
        self.dot_shaped_radio.setChecked(False)
        self.dot_shaped_radio.setObjectName("dot_shaped_ratio")
        self.dot_shaped_radio.setToolTip("Very little dots")
        self.circle_shaped_radio = QtWidgets.QRadioButton(self.centralwidget)
        self.circle_shaped_radio.setGeometry(QtCore.QRect(510, 290, 82, 17))
        self.circle_shaped_radio.setChecked(True)
        self.circle_shaped_radio.setObjectName("circle_shaped_ratio")
        self.circle_shaped_radio.setToolTip("Normal dots")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(510, 250, 131, 16))
        self.label_7.setObjectName("label_7")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(640, 390, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setToolTip("Start the simulation")
        self.transmission_val = QtWidgets.QLabel(self.centralwidget)
        self.transmission_val.setGeometry(QtCore.QRect(30, 100, 21, 16))
        self.transmission_val.setObjectName("transmission_val")
        self.mortality_val = QtWidgets.QLabel(self.centralwidget)
        self.mortality_val.setGeometry(QtCore.QRect(30, 150, 31, 16))
        self.mortality_val.setObjectName("mortality_val")
        self.recovered_val = QtWidgets.QLabel(self.centralwidget)
        self.recovered_val.setGeometry(QtCore.QRect(30, 200, 21, 16))
        self.recovered_val.setObjectName("recovered_val")
        self.immunity_val = QtWidgets.QLabel(self.centralwidget)
        self.immunity_val.setGeometry(QtCore.QRect(30, 250, 21, 16))
        self.immunity_val.setObjectName("immunity_val")
        self.dots_nb_val = QtWidgets.QLabel(self.centralwidget)
        self.dots_nb_val.setGeometry(QtCore.QRect(270, 160, 21, 16))
        self.dots_nb_val.setObjectName("dots_nb_val")
        self.distance_val = QtWidgets.QLabel(self.centralwidget)
        self.distance_val.setGeometry(QtCore.QRect(270, 210, 18, 13))
        self.distance_val.setObjectName("distance_val")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(60, 330, 131, 16))
        self.label_8.setObjectName("label_8")
        self.initial_infected_val = QtWidgets.QLabel(self.centralwidget)
        self.initial_infected_val.setGeometry(QtCore.QRect(30, 350, 21, 16))
        self.initial_infected_val.setObjectName("initial_infected_val")
        self.initial_infected_val.setProperty("value", 0)
        self.initial_infected_population_slider = QtWidgets.QSlider(self.centralwidget)
        self.initial_infected_population_slider.setGeometry(
            QtCore.QRect(60, 350, 160, 22)
        )
        self.initial_infected_population_slider.setMaximum(
            self.number_of_dots_slider.value()
        )
        self.initial_infected_population_slider.setMinimum(1)
        self.initial_infected_population_slider.setSingleStep(1)
        self.initial_infected_population_slider.setProperty("value", 0)
        self.initial_infected_population_slider.setOrientation(QtCore.Qt.Horizontal)
        self.initial_infected_population_slider.setObjectName(
            "initial_infected_population_slider"
        )
        self.initial_infected_population_slider.setToolTip(
            "Number of infected individuals at the beginning of the simulation (they start as exposed)"
        )
        self.masked_dots_slider = QtWidgets.QSlider(self.centralwidget)
        self.masked_dots_slider.setGeometry(QtCore.QRect(300, 110, 160, 22))
        self.masked_dots_slider.setMinimum(0)
        self.masked_dots_slider.setMaximum(self.number_of_dots_slider.value())
        self.masked_dots_slider.setSingleStep(1)
        self.masked_dots_slider.setProperty("value", 0)
        self.masked_dots_slider.setOrientation(QtCore.Qt.Horizontal)
        self.masked_dots_slider.setObjectName("masked_dots_slider")
        self.masked_dots_slider.setToolTip(
            "Number of dots that are wearing a mask at the beginning of the simulation"
        )
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(300, 90, 141, 16))
        self.label_9.setObjectName("label_9")
        self.masked_dots_val = QtWidgets.QLabel(self.centralwidget)
        self.masked_dots_val.setGeometry(QtCore.QRect(270, 110, 21, 16))
        self.masked_dots_val.setObjectName("masked_dots_val")
        self.masked_dots_val.setProperty("value", 0)
        self.incubation_val = QtWidgets.QLabel(self.centralwidget)
        self.incubation_val.setGeometry(QtCore.QRect(30, 300, 21, 16))
        self.incubation_val.setObjectName("incubation_val")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(60, 280, 121, 16))
        self.label_10.setObjectName("label_10")
        self.incubation_slider = QtWidgets.QSlider(self.centralwidget)
        self.incubation_slider.setGeometry(QtCore.QRect(60, 300, 160, 22))
        self.incubation_slider.setMaximum(20)
        self.incubation_slider.setSingleStep(0)
        self.incubation_slider.setProperty("value", 2)
        self.incubation_slider.setOrientation(QtCore.Qt.Horizontal)
        self.incubation_slider.setObjectName("incubation_slider")
        self.incubation_slider.setToolTip(
            "Number of days an individual is being in the exposed state"
        )
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(540, 80, 171, 16))
        self.label_11.setObjectName("label_11")
        self.simulation_speed_slider = QtWidgets.QSlider(self.centralwidget)
        self.simulation_speed_slider.setGeometry(QtCore.QRect(540, 100, 160, 22))
        self.simulation_speed_slider.setMinimum(2)
        self.simulation_speed_slider.setMaximum(100)
        self.simulation_speed_slider.setSingleStep(1)
        self.simulation_speed_slider.setProperty("value", 20)
        self.simulation_speed_slider.setOrientation(QtCore.Qt.Horizontal)
        self.simulation_speed_slider.setObjectName("simulation_speed_slider")
        self.simulation_speed_slider.setToolTip(
            "Speed of the simulation (0: nothing happens, 100: SPEED)"
        )
        self.simulation_speed_val = QtWidgets.QLabel(self.centralwidget)
        self.simulation_speed_val.setGeometry(QtCore.QRect(510, 100, 18, 13))
        self.simulation_speed_val.setObjectName("simulation_speed_val")
        self.simulation_speed_val.setProperty("value", 20)
        self.collision = QtWidgets.QCheckBox(self.centralwidget)
        self.collision.setGeometry(QtCore.QRect(510, 130, 201, 17))
        self.collision.setObjectName("collision")
        self.collision.setToolTip(
            "If checked, dots can collide with each other (very laggy above 250-300 dots), still in BETA"
        )
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(30, 40, 81, 16))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(270, 40, 111, 16))
        self.label_13.setObjectName("label_13")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(30, 60, 118, 3))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(270, 60, 118, 3))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(230, 30, 16, 341))
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(470, 30, 16, 341))
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(510, 40, 101, 16))
        self.label_14.setObjectName("label_14")
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setGeometry(QtCore.QRect(510, 60, 118, 3))
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.dots_same_speed = QtWidgets.QCheckBox(self.centralwidget)
        self.dots_same_speed.setGeometry(QtCore.QRect(510, 160, 181, 17))
        self.dots_same_speed.setObjectName("dots_same_speed")
        self.dots_same_speed.setToolTip(
            "If checked, dots will travel at the same speed"
        )
        self.infected_wear_mask = QtWidgets.QCheckBox(self.centralwidget)
        self.infected_wear_mask.setGeometry(QtCore.QRect(510, 190, 211, 17))
        self.infected_wear_mask.setObjectName("infected_wear_mask")
        self.infected_wear_mask.setToolTip(
            "If checked, infected will always wear a mask (once they're, and then if they weren't wearing a mask, they'll remove it, else they'll keep it)"
        )
        self.infected_slowdown = QtWidgets.QCheckBox(self.centralwidget)
        self.infected_slowdown.setGeometry(QtCore.QRect(510, 220, 211, 17))
        self.infected_slowdown.setObjectName("infected_slowdown")
        self.infected_slowdown.setToolTip(
            "If checked, infected dots will slow down (they're travelling lessly)"
        )
        self.people_travel_slower = QtWidgets.QCheckBox(self.centralwidget)
        self.people_travel_slower.setGeometry(QtCore.QRect(270, 240, 121, 17))
        self.people_travel_slower.setObjectName("people_travel_slower")
        self.people_travel_slower.setToolTip(
            "If checked, people will travel slower (and there is more chance to have more than 1 wave)"
        )
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(270, 260, 121, 16))
        self.label_15.setObjectName("label_15")
        self.auto_stop = QtWidgets.QCheckBox(self.centralwidget)
        self.auto_stop.setGeometry(QtCore.QRect(560, 390, 70, 17))
        self.auto_stop.setObjectName("auto_stop")
        self.auto_stop.setToolTip(
            "If checked, the simulation will stop automatically when there are no more infected dots"
        )
        self.auto_stop.setChecked(True)
        self.visual = QtWidgets.QCheckBox(self.centralwidget)
        self.visual.setGeometry(QtCore.QRect(480, 390, 70, 17))
        self.visual.setObjectName("visual")
        self.visual.setChecked(True)
        self.visual.setToolTip("If checked, the simulation will be visualized or not")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Transmission rate (%)"))
        self.label_2.setText(_translate("MainWindow", "Mortality rate (‰)"))
        self.label_3.setText(_translate("MainWindow", "Time Before Recovering (days)"))
        self.label_4.setText(_translate("MainWindow", "Immunity duration (days)"))
        self.label_5.setText(_translate("MainWindow", "Population size"))
        self.label_6.setText(
            _translate("MainWindow", "Maximum transmission distance (m)")
        )
        self.dot_shaped_radio.setText(_translate("MainWindow", "Little dot"))
        self.circle_shaped_radio.setText(_translate("MainWindow", "Circle"))
        self.label_7.setText(_translate("MainWindow", "Dots shape without a mask"))
        self.pushButton.setText(_translate("MainWindow", "Go!"))
        self.auto_stop.setText(_translate("MainWindow", "Auto-stop"))
        self.visual.setText(_translate("MainWindow", "Visual"))
        self.transmission_val.setText(
            _translate("MainWindow", str(self.transmission_rate_slider.value()))
        )
        self.mortality_val.setText(
            _translate("MainWindow", str(self.mortality_rate_slider.value()))
        )
        self.recovered_val.setText(
            _translate("MainWindow", str(self.time_to_recover_rate_slider.value()))
        )
        self.immunity_val.setText(
            _translate("MainWindow", str(self.immunity_duration_rate_slider.value()))
        )
        self.dots_nb_val.setText(
            _translate("MainWindow", str(self.number_of_dots_slider.value()))
        )
        self.distance_val.setText(
            _translate("MainWindow", str(self.minimal_distance_slider.value()))
        )
        self.simulation_speed_val.setText(
            _translate("MainWindow", str(self.simulation_speed_slider.value()))
        )

        self.incubation_val.setText(
            _translate("MainWindow", str(self.incubation_slider.value()))
        )
        self.label_10.setText(_translate("MainWindow", "Incubation time (days)"))
        self.label_11.setText(_translate("MainWindow", "Simulation speed"))
        self.simulation_speed_val.setText(_translate("MainWindow", "20"))
        self.collision.setText(
            _translate("MainWindow", "Dots can collide between each other")
        )
        self.collision.setText(
            _translate("MainWindow", "Dots can collide between each other")
        )
        self.label_12.setText(_translate("MainWindow", "Virus properties"))
        self.label_13.setText(_translate("MainWindow", "Population properties"))
        self.label_14.setText(_translate("MainWindow", "Simulation properties"))
        self.dots_same_speed.setText(
            _translate("MainWindow", "Dots move at the same speed")
        )
        self.infected_wear_mask.setText(
            _translate("MainWindow", "Infected dots always wear a mask")
        )
        self.infected_slowdown.setText(
            _translate("MainWindow", "Infected dots move slower")
        )
        self.people_travel_slower.setText(
            _translate("MainWindow", "People travel slower")
        )
        self.label_15.setText(_translate("MainWindow", "(may increase waves)"))

        # Everything here is to connect button and sliders to methods
        self.transmission_rate_slider.valueChanged.connect(self.transmission_val.setNum)
        self.mortality_rate_slider.valueChanged.connect(self.mortality_val.setNum)
        self.time_to_recover_rate_slider.valueChanged.connect(self.recovered_val.setNum)
        self.immunity_duration_rate_slider.valueChanged.connect(
            self.immunity_val.setNum
        )
        self.initial_infected_population_slider.valueChanged.connect(
            self.initial_infected_val.setNum
        )
        self.masked_dots_slider.valueChanged.connect(self.masked_dots_val.setNum)
        self.incubation_slider.valueChanged.connect(self.incubation_val.setNum)
        self.number_of_dots_slider.valueChanged.connect(self.adjust_maximums)
        self.minimal_distance_slider.valueChanged.connect(self.distance_val.setNum)
        self.simulation_speed_slider.valueChanged.connect(
            self.simulation_speed_val.setNum
        )
        self.pushButton.clicked.connect(self.go)
        self.visual.clicked.connect(self.set_visual)
        self.label_8.setText(_translate("MainWindow", "Initial infected population"))
        self.initial_infected_val.setText(
            _translate(
                "MainWindow", f"{self.initial_infected_population_slider.value()}"
            )
        )
        self.label_9.setText(_translate("MainWindow", "Population wearing a mask"))
        self.masked_dots_val.setText(
            _translate("MainWindow", f"{self.masked_dots_slider.value()}")
        )

    def set_visual(self):
        if self.visual.isChecked():
            self.auto_stop.setChecked(True)
            self.circle_shaped_radio.setEnabled(True)
            self.dot_shaped_radio.setEnabled(True)
            self.auto_stop.setEnabled(True)
            self.auto_stop.setChecked(False)
        else:
            self.auto_stop.setChecked(False)
            self.circle_shaped_radio.setEnabled(False)
            self.dot_shaped_radio.setEnabled(False)
            self.auto_stop.setChecked(True)
            self.auto_stop.setEnabled(False)

    def adjust_maximums(self, d: int):
        self.dots_nb_val.setNum(d)
        self.initial_infected_population_slider.setMaximum(d)
        self.masked_dots_slider.setMaximum(d)

    def go(self):
        with open(config_path, "w") as f:
            f.write("")
        with open(config_path, "a") as f:
            f.write(self.transmission_val.text() + "\n")
            f.write(self.mortality_val.text() + "\n")
            f.write(self.recovered_val.text() + "\n")
            f.write(self.immunity_val.text() + "\n")
            f.write(self.dots_nb_val.text() + "\n")
            f.write(self.distance_val.text() + "\n")
            f.write(self.initial_infected_val.text() + "\n")
            f.write(self.masked_dots_val.text() + "\n")
            f.write(self.incubation_val.text() + "\n")
            f.write(("." if self.dot_shaped_radio.isChecked() else "o") + "\n")
            f.write(self.simulation_speed_val.text() + "\n")
            f.write(("1" if self.collision.isChecked() else "0") + "\n")
            f.write(("1" if self.dots_same_speed.isChecked() else "0") + "\n")
            f.write(("1" if self.infected_wear_mask.isChecked() else "0") + "\n")
            f.write(("1" if self.infected_slowdown.isChecked() else "0") + "\n")
            f.write(("1" if self.people_travel_slower.isChecked() else "0") + "\n")
            f.write(("1" if self.auto_stop.isChecked() else "0") + "\n")
            f.write(("1" if self.visual.isChecked() else "0") + "\n")
            sys.exit()


if __name__ == "__main__":
    with open(config_path, "w") as f:
        f.write("")
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
