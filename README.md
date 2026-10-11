# Group 7 Project 2
## Installation and Running

Requires Python 3.8+

### Linux

If using a Wayland compositor:  
```sh
# Debian
sudo apt install qtwayland5
# Fedora
sudo dnf install qt5-qtwayland
# Arch
sudo pacman -S qt5-wayland
```
To clone down and run the program:

```sh
git clone https://github.com/lbrookskanost/group7_eecs581_prj2
cd group7_eecs581_prj2
chmod +x minesweeper.sh
./minesweeper.sh
```

### Windows

`minesweeper.sh` will not work in the Windows terminal.  
```bat
git clone https://github.com/lbrookskanost/group7_eecs581_prj2
cd group7_eecs581_prj2
python -m venv .venv
.venv\Scripts\activate
pip install pyqt5
python main.py
```

### macOS

```sh
git clone https://github.com/lbrookskanost/group7_eecs581_prj2
cd group7_eecs581_prj2
chmod +x minesweeper.sh
./minesweeper.sh
```