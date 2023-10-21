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
    parser.add_argument("-a", "--action", action='store', required=False, help="List or Assemble", default="list")
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
    if version <= "0.1":
        print(f"{r1}Error: Version {version} not supported{c1}")
        exit(1)

    scenarios = config_json['Scenarios']
    facets = config_json['Facets']
    roles = config_json['Roles']
    ousdfacets = config_json['OpenUsdFacetsSubFacets']

    fchk = 0
    sflchk = 0
    rchk = 0
    for k1, v1 in scenarios.items():
        if k1 not in facets:
            for k2, v2 in v1.items():
                if k2 == "FacetLayout":
                    for v3 in v2:
                        f = v3
                        if "/" in f:
                            f, sf = v3.split("/")
                        if f not in facets:
                            print(f"{r1}CC Error 1: In Scenario '{k1}' Facet '{f}' not found in facets{c1}")
                            exit(1)
                        if type=="OpenUsdFacetSubfacet":
                            if sf not in facets[f]["SubFacets"]:
                                print(f"{r1}CC Error 2: In Scenario '{k1}' SubFacet: '{sf} not found in Facet '{f}'{c1}")
                                exit(1)
                        sflchk += 1
                if k2 == "Roles":
                    for k3 in v2:
                        if k3 not in roles:
                            print(f"{r1}CC Error 3: In Scenario '{k1}' RoleMapping '{k3}' not found in roles {roles}{c1}")
                            exit(1)
                        rchk += 1
        fchk += 1
    print(f"Consistency check passed fchk:{fchk} sflchk:{sflchk} rchk:{rchk}")
    return scenarios, facets,  ousdfacets,  roles


def list_config(scenarios, facets, ousdfacets, roles):
    # List config file

    # Parameters
    # ----------
    # scenarios : dict
    #    Dictionary of scenarios
    # facets : dict
    #    Dictionary of facets
    # roles : dict
    #    Dictionary of roles

    # Returns
    # -------
    # None

    print("Scenarios")
    for k1, v1 in scenarios.items():
        print(f"{c1}  {k1}")
        for k2, v2 in v1.items():
            if k2 == "FacetLayout":
                for v3 in v2.items():
                    print(f"{c2}  FacetLayout: {v3}")
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


def assemble_usdfile(scenarios, facets, ousdfacets, roles,  scenario, role, outfile):
    # Assemble stage file

    # Parameters
    # ----------
    # scenarios : dict
    #    Dictionary of scenarios
    # facets : dict
    #    Dictionary of facets
    # roles : dict
    #    Dictionary of roles
    # scenario : str
    #    Scenario for stage creation
    # role : str
    #    Role for which to create stage
    # outfile : str
    #    Output file

    # Returns
    # -------
    # None

    print(f"Assembling {outfile} for scenario:{scenario} and role:{role}")

    sdict = scenarios[scenario]

    fldict = sdict["FacetLayout"]
    # rmdict = sdict["RoleMappings"]
    # rdict = roles[role]

    if role not in roles:
        print(f"{r1}Error: Role '{role}' not found in RoleMappings for scenario {scenario}  {c1}")
        exit(1)

    fldict = sdict["FacetLayout"]
    olst = []
    for fline in fldict:
        f = fline
        if "/" in f:
            f, sf = fline.split("/")
        fdict = facets[f]
        typ = fdict["Type"]
        if typ == "OpenUsdFacet":
            print(f)
            line = fdict["AssetIdentifier"]
            print(line)
            olst.append(sf)
        if typ == "OpenUsdFacetSubfacet":
            sfdict = ousdfacets["SubFacets"][sf]
            line = f"{fline}\n"
            print(line)
            olst.append(sf)

    ofile = open(outfile, "w")
    ofile.writelines(olst)
    ofile.close()
    print(f"Wrote {len(olst)} lines to {outfile}")


def main():
    starttime = time.time()

    args = get_args()

    config = open(args.config, 'r')
    config_json = json.load(config)

    scenarios, facets, ousdfacets, roles = CheckConsistency(config_json)

    action = args.action
    if action == "a":
        action = "assemble"

    print(f"There are scenarios:{len(scenarios)} facets:{len(facets)} roles:{len(roles)} roles")

    if action == "list":
        list_config(scenarios, facets, ousdfacets, roles)

    elif action == "assemble":

        if args.role not in roles:
            print(f"{r1}Error: Role '{args.role}' not found in configuration{c1}")
            exit(1)

        if args.scenario not in scenarios:
            print(f"{r1}Error: Scenario '{args.scenario}' not found in configuration{c1}")
            exit(1)

        assemble_usdfile(scenarios, facets, ousdfacets, roles, args.scenario, args.role, args.outfile)

    elap = time.time() - starttime

    print(f"{c1}Assembly took {c2}{elap:.3f}{c1} secs ")


if __name__ == "__main__":
    main()
