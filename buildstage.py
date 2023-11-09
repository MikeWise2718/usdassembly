from colored import fg, bg, Style
import argparse
import time
import json
from stager.stager import Stager

r1 = bg('navy_blue') + fg('red')
c1 = bg('navy_blue') + fg('white')
c2 = bg('navy_blue') + fg('yellow')
c3 = bg('navy_blue') + fg('green')


def get_args():
    parser = argparse.ArgumentParser(description="Build Stage ",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-c", "--config", action='store', required=True, help="Configuration File",
                        default="config.json")
    parser.add_argument("-a", "--action", action='store', required=False, help="List or Assemble", default="list")
    parser.add_argument("-s", "--scenario", action='store', required=False, help="Senario for stage creation",
                        default="Default")
    parser.add_argument("-r", "--role", action='store', required=False, help="Role for which to create stage",
                        default="User")
    parser.add_argument("-of", "--outfile", action='store', required=True, help="Output file", default="")
    parser.add_argument("-v", "--verbose", action='store_true', default=False)

    args = parser.parse_args()
    return args


def main():
    starttime = time.time()

    args = get_args()

    config = open(args.config, 'r')
    config_json: dict = json.load(config)

    stager = Stager(config_json)
    stager.CheckConsistency()

    scenarios, facets, ousdfacets, roles = stager.CheckConsistency()

    action = args.action
    if action == "a":
        action = "assemble"

    print(f"There are scenarios:{len(scenarios)} facets:{len(facets)} roles:{len(roles)} roles")

    if action == "list":
        stager.ListConfig()

    elif action == "assemble":

        if args.role not in roles:
            print(f"{r1}Error: Role '{args.role}' not found in configuration{Style.reset}")
            exit(1)

        if args.scenario not in scenarios:
            print(f"{r1}Error: Scenario '{args.scenario}' not found in configuration{Style.reset}")
            exit(1)

        stager.BuildStage(args.scenario, args.role, args.outfile)

    elap = time.time() - starttime

    print(f"{c1}Assembly took {c2}{elap:.3f}{Style.reset} secs ")


if __name__ == "__main__":
    main()
