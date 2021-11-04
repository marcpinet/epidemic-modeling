import os


def suppress_qt_warnings():
    os.environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"


if __name__ == "__main__":
    suppress_qt_warnings()

    with open("files\\logs.txt", "w") as f:
        f.write("")

    os.system("python ui\\ui.py")
    os.system("python math\\modeling.py files\\config.txt")
    os.system("python math\\graph.py files\\logs.txt")