import os, argparse


parser = argparse.ArgumentParser(description="boot patch")

parser.add_argument("--patch", type=str, dest="boot_path", help="string path to boot image")
parser.add_argument("--flash", type=bool, dest="patched_boot_path", default=False, help="bool")
parser.add_argument("--output", type=str, dest="output_path", default="./", help="output path")


args = parser.parse_args()


def main():
    originalBoot = args.boot_path
    outputPath = args.output_path

    os.system("adb install ./magisk.apk")
    os.system("adb push ./magisk/ /data/local/tmp")
    os.system("adb push " + originalBoot + " /data/local/tmp/magisk")
    os.system("adb shell chmod +x /data/local/tmp/magisk/*")
    os.system("adb shell /data/local/tmp/magisk/boot_patch.sh boot.img")
    os.system("adb pull /data/local/tmp/magisk/new-boot.img " + outputPath)
    
    if args.patched_boot_path and outputPath == "./":
        os.system("adb reboot bootloader")
        os.system("ping>nul 2>nul localhost")
        os.system("fastboot flash boot new-boot.img")
        os.system("fastboot reboot")
    else:
        print('''
if you want to flash the boot image, please do not modify the value of --output''')

if __name__ == '__main__':
    main()