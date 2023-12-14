from argparse import ArgumentParser

def get_debug_mode():
    parser = ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='Run the program in debug mode')
    arguments = parser.parse_args()
    return arguments.debug