from colored import fg, bg, Style
from pxr import Usd

r1 = bg('navy_blue') + fg('red')
c1 = bg('navy_blue') + fg('white')
c2 = bg('navy_blue') + fg('yellow')
c3 = bg('navy_blue') + fg('green')


class Stager:
    version = None
    scenarios = {}
    facets = {}

    def __init__(self, config_json: dict):
        if "version" not in config_json:
            self.Error("No Version in config file")
        if "scenarios" not in config_json:
            self.Error("No Scenarios in config file")
        if "facets" not in config_json:
            self.Error("No Facets in config file")

        version = config_json['version']
        if version <= "0.1":
            self.Error(f"Error: Version {version} not supported")

        self.scenarios = config_json['scenarios']
        self.facets = config_json['facets']

    def Error(self, msg, fatal=True):
        print(f"{r1}Error: {msg}{Style.reset}")
        if fatal:
            exit(1)

    def ValidateScenario(self, scenario):
        if 'id' not in scenario:
            return False
        if 'name' not in scenario:
            return False
        if 'description' not in scenario:
            return False
        if 'roles' not in scenario:
            return False
        if 'facetLayout' not in scenario:
            return False

        return True

    def ValidateFacet(self, facet, facets):
        if 'id' not in facet:
            return False
        if 'name' not in facet:
            return False
        if 'description' not in facet:
            return False
        if 'versions' not in facet:
            return False
        for version in facet['versions']:
            if 'id' not in version:
                return False
            if 'description' not in version:
                return False
            if 'assetIdentifier' not in version and 'subFacets' not in version:
                return False
            if 'subFacets' in version:
                for subFacet in version['subFacets']:
                    if not self.ValidateFacet(self._FindFacet(subFacet), facets):
                        return False
            # TODO: Only one version should have no previous version
        return True

    def Validate(self):
        # Check consistency of config file

        # Parameters
        # ----------
        # config_json : dict
        #     Dictionary of config file

        # Returns
        # -------
        # True if valid, False otherwise

        usedScenarioIds = []
        for scenario in self.scenarios:
            # Ensure all scenarios have a unique id
            if scenario['id'] in usedScenarioIds:
                self.Error(
                    f"Multiple scenarios with id {scenario['id']} in config file")

            usedScenarioIds.append(scenario['id'])

            if not self.ValidateScenario(scenario):
                self.Error(f"Invalid scenario : {scenario}")
                return False

        usedFacetIds = []
        for facet in self.facets:
            # Ensure all facets have a unique id
            if facet['id'] in usedFacetIds:
                self.Error(
                    f"Multiple facets with id {facet['id']} in config file")
            if not self.ValidateFacet(facet, self.facets):
                self.Error(f"Invalid facet : {facet}")
                return False

    def BuildStage(self, scenarioName, role, outfile, assetRoot):
        # Assemble stage file

        # Parameters
        # ----------
        # scenarioId : string
        #    The name of the scenario to build
        # role : str
        #    Role for which to create stage
        # outfile : str
        #    Output USD file

        # Returns
        # -------
        # None

        print(
            f"Assembling {outfile} for scenario with id:{scenarioName} and role:{role}")

        scenario = {}
        for scenarioItr in self.scenarios:
            if scenarioItr['name'] == scenarioName:
                scenario = scenarioItr

        if role not in scenario['roles']:
            print(
                f"{r1}Error: Role '{role}' not found in RoleMappings for scenario {scenario}  {Style.reset}")
            exit(1)

        # Create the USD stage
        stage = Usd.Stage.CreateNew(outfile)
        self._AddAssetsToStage(stage, scenario["facetLayout"], assetRoot)
        stage.Save()

    def _FindFacet(self, facetId):
        for facet in self.facets:
            if facet['id'] == facetId:
                return facet
        return None

    def _AddAssetsToStage(self, stage, facetLayout, assetRoot):
        for facetId in facetLayout:
            facet = self._FindFacet(facetId)
            if facet is None:
                self.Error(f'Failed to find facet with id: {facetId}')
                exit(1)
            # TODO: Automatically getting the first version should this be configurable?
            latestVersion = facet['versions'][0]
            if 'subFacets' in latestVersion:
                self._AddAssetsToStage(stage, latestVersion["subFacets"], assetRoot)
            else:
                assetIdentifier = latestVersion['assetIdentifier']
                refPrim = stage.OverridePrim('/refPrim')
                assetPath = assetIdentifier
                if assetRoot is not None:
                    assetPath = assetRoot + "/" + assetIdentifier
                
                refPrim.GetReferences().AddReference(assetPath)
                    
