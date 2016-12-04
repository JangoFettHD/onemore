from cx_Freeze import setup, Executable

setup(
    name = "21",
    version = "0.1",
    description = "OneMore",
    executables = [Executable("E:\onemore\main.py")], requires=['shapely']
)