import os
from sys import argv
from shutil import copyfile

from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def main():
    """
    The main logic goes here.
    This function is going to be executed
    on startup
    """

    # Get the home config path
    folder = os.getenv("XDG_CONFIG_HOME", default=os.path.expanduser("~") + "/.config")

    # Check whether the home config exists
    if not os.path.exists(folder):
        raise SystemExit(
            "Config folder was not found. \n"
            "Try setting/changing XDG_CONFIG_HOME env variable."
        )

    # Check whether a config folder exists
    config_folder = folder + "/march"
    if not os.path.exists(config_folder):
        try:
            os.mkdir(config_folder)
        except OSError:
            raise SystemExit("Config folder creation has failed.")

    # Check whether a config file exists
    config_file = config_folder + "/config.yml"
    if not os.path.exists(config_file):
        try:
            copyfile(os.getcwd() + "/sample.yml", config_file)
        except OSError:
            raise SystemExit("Config file creation has failed.")

    # At this point we're 100% sure that the
    # config file exists and we can parse it
    with open(config_file) as file:
        config = load(file, Loader=Loader)

    # Show help message if it's asked for or no arguments were passed
    if not argv[1:] or argv[1] in ("help", "--help", "-h"):
        return print_help(config)

    # Parse entries into a list
    if argv[1].startswith("-"):
        entries = list(argv[1][1:])
    else:
        entries = argv[1].split(",")

    # Generate a command list
    commands = []
    for name, value in config.items():
        if name in entries or value["short"] in entries:
            commands.append(value["command"])

    if not commands:
        raise SystemExit("Nothing to execute...")

    # Ask if a user is fine with executing such commands
    print("These commands are going to be executed:\n" + "\n".join(commands) + "\n")

    try:
        prompt = input("Proceed? [y/N] ").strip().lower()
    except KeyboardInterrupt:
        return SystemExit()

    if not prompt in ("y", "yep", "yes"):
        return SystemExit()

    # Execute commands
    for command in commands:
        print(f"-> {command}")
        os.system(command)


def print_help(conf: dict):
    """
    This piece of code looks
    embarrasing, but I made so that
    it looks sexy on output.
    """

    print(
        """Usage:
 • march <args> (e.g. `-uo` OR `upgrade,oprhans`)
    
Available commands:"""
    )

    for name, value in conf.items():
        print(" • {name}, -{short} ({command})".format(name=name, **value))

    print(
        """
* Commands are configured in
$XDG_CONFIG_HOME/march/config.yml"""
    )


if __name__ == "__main__":
    """
    Call the main function if the
    file was launched directly
    """

    main()
