import os
import platform


operating_system = platform.platform() # Linux - Windows - macOS


def replace_env_file():
    if operating_system == "Windows":
        os.system("copy .env .env_secure ")
        os.system("copy .env.liara .env")
        try:
            os.system("liara version")
            os.system("liara deploy")
        except KeyboardInterrupt:
            os.system("copy .env .env.liara")
            os.system("copy .env_secure .env")
    else:
        os.system("cp .env .env_secure ")
        os.system("cp .env.liara .env")
        try:
            os.system("liara version")
            os.system("liara deploy")
        except KeyboardInterrupt:
            os.system("cp .env .env.liara")
            os.system("cp .env_secure .env")

def main():
    replace_env_file()



if __name__ == "__main__":
    main()