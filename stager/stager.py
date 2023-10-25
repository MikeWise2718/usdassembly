from colored import fg, bg

r1 = bg('navy_blue') + fg('red')
c1 = bg('navy_blue') + fg('white')
c2 = bg('navy_blue') + fg('yellow')
c3 = bg('navy_blue') + fg('green')


class Stager:

    version = None
    scenarios = {}
    facets = {}
    roles = {}
    ousdfacets = {}

    def __init__(self, config_json: dict):
        if "Version" not in config_json:
            self.Error("Stager.__init__", "No Version in config file")
        if "Scenarios" not in config_json:
            self.Error("Stager.__init__", "No Scenarios in config file")
        if "Facets" not in config_json:
            self.Error("Stager.__init__", "No Facets in config file")
        if "Roles" not in config_json:
            self.Error("Stager.__init__", "No Roles in config file")
        if "OpenUsdFacetSubFacets" not in config_json:
            self.Error("Stager.__init__", "No OpenUsdFacetSubFacets in config file")

        version = config_json['Version']
        if version <= "0.1":
            print(f"{r1}Error: Version {version} not supported{c1}")
            exit(1)

        self.scenarios = config_json['Scenarios']
        self.facets = config_json['Facets']
        self.roles = config_json['Roles']
        self.ousdfacets = config_json['OpenUsdFacetSubFacets']
        pass

    def Error(self, location, msg, fatal=True):
        print(f"{r1}Error: {msg}{c1}")
        if fatal:
            exit(1)

    def CheckConsistency(self):
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

        # version = config_json['Version']
        # if version <= "0.1":
        #     print(f"{r1}Error: Version {version} not supported{c1}")
        #     exit(1)
        # scenarios = config_json['Scenarios']
        # facets = config_json['Facets']
        # roles = config_json['Roles']
        # ousdfacets = config_json['OpenUsdFacetSubFacets']

        fchk = 0
        sflchk = 0
        rchk = 0
        for k1, v1 in self.scenarios.items():
            if k1 not in self.facets:
                for k2, v2 in v1.items():
                    if k2 == "FacetLayout":
                        for v3 in v2:
                            f = v3
                            sf = ""
                            if "/" in f:
                                f, sf = v3.split("/")
                            if f not in self.facets:
                                print(f"{r1}CC Error 1: In Scenario '{k1}' Facet '{f}' not found in facets{c1}")
                                exit(1)
                            if type == "OpenUsdFacetSubFacets":
                                if sf not in self.facets[f]["SubFacets"]:
                                    print(f"{r1}CC Error 2: In Scenario '{k1}' SubFacet: '{sf} not found in Facet '{f}'{c1}")
                                    exit(1)
                            sflchk += 1
                    if k2 == "Roles":
                        for k3 in v2:
                            if k3 not in self.roles:
                                print(f"{r1}CC Error 3: In Scenario '{k1}' RoleMapping '{k3}' not found in roles {roles}{c1}")
                                exit(1)
                            rchk += 1
            fchk += 1
        print(f"Consistency check passed fchk:{fchk} sflchk:{sflchk} rchk:{rchk}")
        return self.scenarios, self.facets,  self.ousdfacets,  self.roles

    def ListConfig(self):
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
        for k1, v1 in self.scenarios.items():
            print(f"{c1}  {k1}")
            for k2, v2 in v1.items():
                if k2 == "FacetLayout":
                    for v3 in v2:
                        print(f"{c2}  FacetLayout: {v3}")
                elif k2 == "RoleMappings":
                    for k3, v3 in v2.items():
                        print(f"{c3}  RoleMapping: {k3} - {v3}")

        for k1, v1 in self.facets.items():
            print(f"{c1}  {k1}")
            for k2, v2 in v1.items():
                print(f"{c2}  {k2} - {v2}")

        for k1, v1 in self.roles.items():
            print(f"{c1}  {k1}")
            for k2, v2 in v1.items():
                print(f"{c2}  {k2} - {v2}")

    def BuildStage(self, scenario, role, outfile):
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

        sdict = self.scenarios[scenario]

        fldict = sdict["FacetLayout"]
        # rmdict = sdict["RoleMappings"]
        # rdict = roles[role]

        if role not in self.roles:
            print(f"{r1}Error: Role '{role}' not found in RoleMappings for scenario {scenario}  {c1}")
            exit(1)

        fldict = sdict["FacetLayout"]
        olst = []
        for fline in fldict:
            f = fline
            sf = ""
            if "/" in f:
                f, sf = fline.split("/")
            fdict = self.facets[f]
            typ = fdict["Type"]
            if typ == "OpenUsdFacet":
                print(f)
                line = fdict["AssetIdentifier"] + "\n"
                print(line)
                olst.append(line)
            elif typ == "OpenUsdFacetSubFacets":
                sfdict = self.ousdfacets[f]["SubFacets"][sf]
                if "Versions" in sfdict:
                    latest = sfdict["Latest"]
                    v = sfdict["Versions"][latest]
                    line = v["AssetIdentifier"] + "\n"
                else:
                    print(f)
                    line = sfdict["AssetIdentifier"] + "\n"
                print(line)
                olst.append(line)
            else:
                print(f"Unknown type:{typ}")

        ofile = open(outfile, "w")
        ofile.writelines(olst)
        ofile.close()
        print(f"Wrote {len(olst)} lines to {outfile}")
