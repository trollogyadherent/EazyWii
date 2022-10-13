#!/usr/bin/python

import os, shutil, sys, subprocess

from modules.colorama import init
from modules.colorama import Fore
from modules.colorama import Style


init()

# COLORS
NC  = Style.RESET_ALL
RED = Fore.RED
MAG = Fore.MAGENTA
GRE = Fore.GREEN
CYA = Fore.CYAN
BLU = Fore.BLUE

##########################
##### IMPORTANT VARS #####
##########################
MAC_ADDR = None
WII_REGION = None

SDCARD_FOLDER = 'sdcard'
UPDATE_GAMES = ['Call of Duty: Black Ops', 'De Blob 2', 'Donkey Kong: Country Returns', 'EA Sports Active 2', 'FIFA12', 'FlingSmash', 'Hello Kitty Seasons', 'Kirby Epic Yarn', 'Mario Party 9', 'Metroid Other M', 'Nickelodeon Fit Wii', 'Pandora`s Tower', 'Raving Rabbids: Travel in Time', 'Schlag den Raab', 'Schlag den Raab - Das 2. Spiel', 'Skylanders: Giants', 'Super Mario All-Stars', 'The Last Story', 'The Legend of Zelda - Skyward Sword', 'Wii Party', 'Worms: Battle Island', 'Xenoblade Chronicles']
FILES = [
	os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files', 'boot_elf', 'boot.elf'),
	os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files', 'usb_loader_wads', 'IOS38-64-v4123.wad'),
	os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files', 'usb_loader_wads', 'IOS56-64-v5661.wad'),
	os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files', 'usb_loader_wads', 'IOS57-64-v5918.wad')
]
FOLDERS = [
	os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files', 'apps'),
	os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files', 'wad')
]


def mac_valid(mac):
	mac = mac.replace(':', '')
	if not mac.isalnum() or len(mac) != 12:
		return False
	return True

def prettify_mac(mac):
	# just in case someone does 12::ad::33....
	mac = mac.replace(':', '').upper()
	ls = []
	for i in range(0, 12, 2):
		ls.append(mac[i:i + 2])
	return CYA + ':'.join(ls) + NC

def prettify_region(region):
	r = {
		'e': 'Europe',
		'j': 'Japan',
		'k': 'Korea',
		'u': 'USA'
	}
	return f'{CYA}{region.upper()}{NC} ({r[region.lower()]})'

def newline():
	print('')

def confirm_or_exit_dialog(dialog=None):
	inp = '-'
	while inp.lower() not in ['', 'exit']:
		if not dialog is None:
			print(dialog)
		inp = input(f'Press {CYA}Enter{NC} to continue, or type {RED}exit{NC} to quit.\n>>> ')
	if inp.lower() == 'exit':
		exit()
	newline()

def printn(*args):
	print(*args)
	newline()

def python_check():
	major_ver = int(sys.version[0])
	if major_ver < 3:
		exit(RED + 'Python ' + CYA + '3' + RED + ' is required to run this script.' + NC)
	elif major_ver > 3:
		printn(CYA + 'Warning' + NC + ': Python version greater than ' + CYA + '3' + NC + ', things may go wrong.')

def get_mac_input():
	inp = '-'
	mac = '-'
	while inp.lower() not in ['', 'exit']:
		while not mac_valid(mac):
			mac = input(f'Please enter the {MAG}MAC address{NC} of your Wii, or type {RED}exit{NC} to quit.\nIt can be found in {CYA}Wii Settings{NC} -> {CYA}Internet{NC} -> {CYA}Console Information{NC}.\n>>> ')
			if mac.lower() == 'exit':
				exit()
			if not mac_valid(mac):
				printn(f'{RED}Invalid {MAG}MAC address{NC}.{NC}')
		newline()
		inp = input(f'Is {prettify_mac(mac)} correct?\nPress {CYA}Enter{NC} if yes, otherwise type anything else. To quit type {RED}exit{NC}.\n>>> ')
		if inp.lower() == 'exit':
			exit()
		if inp != '':
			mac = '-'
	return mac.lower()

def get_region_input():
	inp = '-'
	region = '-'
	while inp.lower() not in ['', 'exit']:
		while not region.lower() in ['u', 'e', 'j', 'k']:
			region = input(f'Please enter the {MAG}region{NC} of your Wii, or type {RED}exit{NC} to quit.\nIt is a single letter at the end of your Wii system version.\nPossible values: {CYA}U{NC}, {CYA}E{NC}, {CYA}J{NC}, {CYA}K{NC}.\n>>> ')
			if region == 'exit':
				exit()
			if not region.lower() in ['u', 'e', 'j', 'k']:
				printn(f'{RED}Invalid region.{NC}')
		newline()
		inp = input(f'Is {prettify_region(region)} correct?\nPress {CYA}Enter{NC} if yes, otherwise type anything else. To quit type {RED}exit{NC}.\n>>> ')
		if inp.lower() == 'exit':
			exit()
		if inp != '':
			region = '-'
	return region.lower()

print(
	'''Welcome to

	███████╗ █████╗ ███████╗██╗   ██╗██╗    ██╗██╗██╗
	██╔════╝██╔══██╗╚══███╔╝╚██╗ ██╔╝██║    ██║██║██║
	█████╗  ███████║  ███╔╝  ╚████╔╝ ██║ █╗ ██║██║██║
	██╔══╝  ██╔══██║ ███╔╝    ╚██╔╝  ██║███╗██║██║██║
	███████╗██║  ██║███████╗   ██║   ╚███╔███╔╝██║██║
	╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚══╝╚══╝ ╚═╝╚═╝
	                                                 '''
	)

python_check()

printn('This prompt will guide you how to softmod your Wii and play game dumps on it.')
#newline()
printn(f'For this guide, you need your Wii system to be on version {CYA}4.3{NC}.\nYou also need a {CYA}512M{NC} to {CYA}32GB{NC} SD card.\n')

# Info on ver 4.3
inp = '-'
while inp.lower() not in ['', 'exit']:
	inp = input(f'Press {CYA}Enter{NC} to continue, or type {RED}exit{NC} to quit.\nTo see a non-exhaustive, non-verified list of games that contain a 4.3 update, type {CYA}list{NC}.\n>>> ')
	if inp.lower() == 'exit':
		exit()
	elif inp.lower() == 'list':
		for game in UPDATE_GAMES:
			print(f'{CYA}{game}{NC}')
		newline()
		print(f'Source: {BLU}https://forum.wii-homebrew.com/index.php/Thread/5280-Wii-Games-mit-Systemupdate/{NC}')
		print(f'Archive: {BLU}https://archive.ph/pS5Y3#selection-1307.1-1307.21{NC}')
	newline()

# MAC input
MAC_ADDR = get_mac_input()

newline()

# Wii region input
WII_REGION = get_region_input()

newline()

if os.path.exists(SDCARD_FOLDER):
	printn('Removing old sdcard folder.')
	shutil.rmtree(SDCARD_FOLDER)
printn('Creating sdcard folder.')
os.makedirs(SDCARD_FOLDER, exist_ok=True)

ret_code = -1
while ret_code != 0:
	printn('Generating LetterBomb payload...')
	child = subprocess.run([sys.executable, f"{os.path.join('software', 'LetterBombCLI', 'letterbomb.py')}", '--mac', MAC_ADDR, '--region' ,WII_REGION, '--output', SDCARD_FOLDER, '--nobundle'])
	ret_code = child.returncode
	if ret_code == 1:
		printn(f'{RED}The inputted MAC looks like a Dolphin emulator mac.{NC}')
		MAC_ADDR = get_mac_input()
	elif ret_code == 2:
		printn(f'{RED}The inputted MAC does not look like a Wii MAC.{NC}')
		MAC_ADDR = get_mac_input()
	elif ret_code == 3:
		printn(f'{RED}Incorrect region.{NC}')
		WII_REGION = get_region_input()
newline()

print('Copying files...')
for file in FILES:
	print(f'copying {CYA}{file}{NC}')
	shutil.copyfile(file, os.path.join(SDCARD_FOLDER, os.path.basename(file)))

for folder in FOLDERS:
	print(f'copying {CYA}{folder}{NC}')
	shutil.copytree(folder, os.path.join(SDCARD_FOLDER, os.path.basename(folder)))
newline()

confirm_or_exit_dialog(f'Copy the contents of the newly created {CYA}{SDCARD_FOLDER}{NC} folder to the root of your SD card.')

confirm_or_exit_dialog(f'Insert the card into the {MAG}front slot{NC} of the Wii.\nOn your Wii, return to the Wii Menu and then open the {MAG}Wii Message Board{NC}.\nLoad the {MAG}red letter with a bomb icon{NC}.\n * Ensure the date on your Wii is correct, otherwise you might be unable to find the letter.\n * In various scenarios, you may need to look at the previous or next day to find it.\n * If you don’t see the {MAG}red letter{NC}, you may be using an unsupported SD card that’s greater than {CYA}32GB{NC} in size.\n * If your Wii freezes after clicking on the letter, you probably chose the wrong region when downloading the exploit. Exit and retry, while choosing the right region.')

confirm_or_exit_dialog(f'You will see a scam warning screen. Wait {CYA}30{NC} seconds for the text “{CYA}Press 1 to continue{NC}” to appear, then press {CYA}1{NC}.\nPress {CYA}Continue{NC}, then select the {MAG}Homebrew Channel{NC}, and press {CYA}Install{NC}.\nPress {CYA}Continue{NC} when finished. Once installed, press back and go to {MAG}BootMii{NC}.\nIf the main screen says you can install {MAG}BootMii{NC} as {MAG}boot2{NC}, do so. This offers the best possible brick protection you can have. Skip this step if the option doesn’t show up, in that case your Wii is not one of the earlier models that supports it.\nInstall {MAG}BootMii{NC} as {MAG}IOS{NC}, even if you already installed {MAG}BootMii{NC} as {MAG}boot2{NC} in the previous step. If you couldn’t install {MAG}BootMii{NC} as {MAG}boot2{NC}, this will still allow you to create a {MAG}NAND backup{NC}.')

has_done_nand = False
inp = '-'
while inp.lower() not in ['', 'no', 'exit']:
	inp = input(f'Press {CYA}Enter{NC} to continue and create a {MAG}NAND backup{NC} (highly recommended), type {CYA}no{NC} to skip, or {RED}exit{NC} to quit.\n>>> ')
	if inp.lower() == 'exit':
		exit()
	elif inp.lower() == '':
		has_done_nand = True
		newline()
		confirm_or_exit_dialog(f'{MAG}Reboot{NC} your console to enter {MAG}BootMii{NC}.\nTo switch between options, press the {MAG}Power Button{NC}. To choose an option, press the {MAG}Reset Button{NC}.\nSelect the {MAG}Options{NC} button (the icon with the gears).\nSelect the {MAG}BackupMii{NC} button (the icon with the green arrow, aka the first icon on your left).\n * A {MAG}NAND backup{NC} will start. You can watch the progress on the screen.\n* “Bad Blocks” are normal. Don’t worry when you see some on a {MAG}NAND backup{NC}.\n * After this step, it will verify the backup. While it is recommended, it can be skipped by pressing the {MAG}EJECT{NC} button on your Wii. Note that if you have a disc inserted in the disc drive, pressing {MAG}EJECT{NC} will also eject the disc.\nWhen the backup is fully complete, exit the {MAG}NAND backup{NC} screen by pressing any button.\nTo restore from a {MAG}NAND backup{NC} on your SD card, do so from {MAG}BootMii{NC} using {MAG}RestoreMii{NC} (the icon with the red arrow, aka the second icon on your left).')

	newline()

# cios
confirm_or_exit_dialog(f'Reboot. You can now optionally install {MAG}Priiloader{NC}. To do so, open the {MAG}Homebrew Channel{NC}, launch the {MAG}Priiloader Installer{NC} and follow the instructions.\n{MAG}cIOS{NC} Installation:\nLaunch the {MAG}d2x cIOS Installer{NC} from the {MAG}Homebrew Channel{NC}.\nPress continue, then set the options to the following:\n - Select cIOS: {GRE}v10 beta52 d2x-v10-beta52{NC}\n - Select cIOS base: {GRE}57{NC}\n - Select cIOS slot: {GRE}249{NC}\n - Select cIOS version: {GRE}65535{NC}\nPress {MAG}A{NC} twice to install.')
confirm_or_exit_dialog(f'Press {MAG}A{NC} to return, and set the options to the following:\n - Select cIOS: {GRE}v10 beta52 d2x-v10-beta52{NC}\n - Select cIOS base: {GRE}56{NC}\n - Select cIOS slot: {GRE}250{NC}\n - Select cIOS version: {GRE}65535{NC}\nPress {MAG}A{NC} twice to install.')
confirm_or_exit_dialog(f'Press {MAG}A{NC} to return, and set the options to the following:\n - Select cIOS: {GRE}v10 beta52 d2x-v10-beta52{NC}\n - Select cIOS base: {GRE}38{NC}\n - Select cIOS slot: {GRE}251{NC}\n - Select cIOS version: {GRE}65535{NC}\nPress {MAG}A{NC} twice to install. Once done, exit the installer.\nRead about different cIOS\'s here: {BLU}https://wiki.gbatemp.net/wiki/Wii_cIOS_base_Compatibility_List{NC}. Archive: {BLU}https://archive.ph/kZ08E{NC}.')

confirm_or_exit_dialog(f'Now you can run game backups from {MAG}USBLoaderGX{NC}, which should be available in the {MAG}Homebrew Channel{NC}.\nFor best results, it is recommended to put games on a {CYA}FAT32{NC} formatted {CYA}HDD{NC}.\nThe HDD has to be plugged to the USB port closest to the edge of the Wii.\nRecommended program that to move files to the disk: {MAG}Wii Backup Fusion 2.0{NC}, link: {BLU}https://github.com/larsenv/Wii-Backup-Fusion{NC}.\nThe final recommendation is to use {CYA}wbfs{NC} formatted games and put them into a "wbfs" folder in the root of the HDD.')

printn(f'A lot of information comes from {BLU}https://wii.guide{NC}.')
