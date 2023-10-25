from colored import fg, bg
import argparse
import time
import json

r1 = bg('navy_blue') + fg('red')
c1 = bg('navy_blue') + fg('white')
c2 = bg('navy_blue') + fg('yellow')
c3 = bg('navy_blue') + fg('green')


def get_args():
    parser = argparse.ArgumentParser(description="Assemble ",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-c", "--config", action='store', required=True, help="Configuration File", 
                        default="config.json")
    parser.add_argument("-a", "--action", action='store', required=False, help="List or Assemble", 
                        default="list")
    parser.add_argument("-s", "--scenario", action='store', required=False, help="Senario for stage creation", 
                        default="Default")
    parser.add_argument("-r", "--role", action='store', required=False, help="Role for which to create stage", 
                        default="User")
    parser.add_argument("-of", "--outfile", action='store', required=True, help="Output file", default="")
    parser.add_argument("-v", "--verbose", action='store_true', default=False)

    args = parser.parse_args()
    return args


def CheckConsistency(config_json):
    # Check consistency of config file

    # Parameters
    # ----------
    # config_json : dict
    #     Dictionary of config file

    # Returns
    # -------
    # scenarios : dict
    #     Dictionary of scenarios
    # facets : dict
    #     Dictionary of facets
    # roles : dict

    version = config_json['Version']
    if version > "0.1":
        print(f"{r1}Error: Version {version} not supported{c1}")
        exit(1)

    scenarios = config_json['Scenarios']
    facets = config_json['Facets']
    roles = config_json['Roles']

    for k1, v1 in scenarios.items():
        if k1 not in facets:
            for k2, v2 in v1.items():
                if k2 == "FacetLayouts":
                    for k3, v3 in v2.items():
                        if k3 not in roles:
                            print(f"{r1}Error: In Scenario '{k1}' RoleMapping '{k3}' not found in roles{c1}")
                            exit(1)
                        for fname in v3:
                            if fname.find("/") > 0:
                                fname, _ = fname.split("/")
                            if fname not in facets:
                                print(f"{r1}Error: In Scenario '{k1}' FacetLayout '{fname}' not found in facets{c1}")
                                exit(1)
                if k2 == "RoleMappings":
                    for k3, v3 in v2.items():
                        if k3 not in roles:
                            print(f"{r1}Error: In Scenario '{k1}' RoleMapping '{k3}' not found in roles{c1}")
                            exit(1)
    return scenarios, facets, roles


def list_config(scenarios, facets, roles):
    # List config file

    print("Scenarios")
    for k1, v1 in scenarios.items():
        print(f"{c1}  {k1}")
        for k2, v2 in v1.items():
            if k2 == "FacetLayouts":
                for k3, v3 in v2.items():
                    print(f"{c2}  FacetLayout: {k3} - {v3}")
            elif k2 == "RoleMappings":
                for k3, v3 in v2.items():
                    print(f"{c3}  RoleMapping: {k3} - {v3}")

    for k1, v1 in facets.items():
        print(f"{c1}  {k1}")
        for k2, v2 in v1.items():
            print(f"{c2}  {k2} - {v2}")

    for k1, v1 in roles.items():
        print(f"{c1}  {k1}")
        for k2, v2 in v1.items():
            print(f"{c2}  {k2} - {v2}")


def assemble_usdfile(scenarios, facets, roles, scenario, role, outfile):
    # Assemble stage file using the builder pattern from the Go4 book

    print(f"Assembling {outfile} for scenario:{scenario} and role:{role}")

    sdict = scenarios[scenario]

    fldict = sdict["FacetLayouts"]
    # rmdict = sdict["RoleMappings"]
    # rdict = roles[role]

    if role not in fldict:
        print(f"{r1}Error: Role '{role}' not found in RoleMappings for scenario {scenario}  {c1}")
        exit(1)

    fldict = sdict["FacetLayouts"][role]
    olst = []
    for fline in fldict:
        line = f"{fline}\n"
        olst.append(line)

    ofile = open(outfile, "w")
    ofile.writelines(olst)
    ofile.close()
    print(f"Wrote {len(olst)} lines to {outfile}")


def main():
    starttime = time.time()

    args = get_args()

    config = open(args.config, 'r')
    config_json = json.load(config)

    scenarios, facets, roles = CheckConsistency(config_json)

    action = args.action
    if action == "a":
        action = "assemble"

    print(f"There are scenarios:{len(scenarios)} facets:{len(facets)} roles:{len(roles)} roles")

    if action == "list":
        list_config(scenarios, facets, roles)

    elif action == "assemble":

        if args.role not in roles:
            print(f"{r1}Error: Role '{args.role}' not found in configuration{c1}")
            exit(1)

        if args.scenario not in scenarios:
            print(f"{r1}Error: Scenario '{args.scenario}' not found in configuration{c1}")
            exit(1)

        assemble_usdfile(scenarios, facets, roles, args.scenario, args.role, args.outfile)

    elap = time.time()-starttime

    print(f"{c1}Assembly took {c2}{elap:.3f}{c1} secs ")


if __name__ == "__main__":
    main()
