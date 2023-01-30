# MyFitness Reservation Script

A script for reserving MyFitness (Latvia) classes using Python. The script uses the MyFitness API to reserve the first available training found on either next Monday or next Wednesday.

## Requirements

- Python 3
- Clone this repository: `git clone https://github.com/kwidoo/mfconnect.git`
- requests library (can be installed via pip: `pip install requests`)

## Usage

1. Run the script with `python myfitness_reservation.py`
2. Enter your MyFitness email and password when prompted
3. The script will search for available classes on next Monday and Wednesday, and reserve the first available class found.

## Note

- The script is for educational purposes only and is not affiliated with MyFitness in any way.
- Use the script at your own risk and make sure to review the code before using it.
