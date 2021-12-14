import os
from time import sleep


def suppress_qt_warnings():
    os.environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"


if __name__ == "__main__":
    suppress_qt_warnings()

    try:
        os.mkdir("files")
    except FileExistsError:
        pass

    with open("files\\logs.txt", "w") as f:
        f.write("")

    print("Select the settings you want for the simulation...")
    os.system("python ui\\ui.py")
    # This sleep is the only way I could find to avoid the modeling.py having an empty config file 
    # (when the file is written from ui.py, it seems that modeling.py launches just before sometimes)
    sleep(1)
    print("Simulating...")
    os.system("python modeling\\modeling.py files\\config.txt")
    print("Generating plot...")
    os.system("python modeling\\graph.py files\\logs.txt")
    print("Done!")
