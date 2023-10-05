
# flake8: noqa

from colored import fg, bg, attr
import argparse
import time
import json

starttime = time.time()


parser = argparse.ArgumentParser(description="Assemble ",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-c", "--config", action='store', required=True, help="Configuration File", default="config.json")
parser.add_argument("-a", "--action", action='store', required=False, help="List or Assemble", default="list")
parser.add_argument("-s", "--scenario", action='store', required=False, help="Senario for withc to create stage", default="SitAware")
parser.add_argument("-r", "--role", action='store', required=False, help="Role for which to create stage", default="User")
parser.add_argument("-of", "--outfile", action='store', required=True, help="Output file", default="")
parser.add_argument("-v", "--verbose", action='store_true', default=False)

args = parser.parse_args()

r1 = bg('navy_blue') + fg('red')
c1 = bg('navy_blue') + fg('white')
c2 = bg('navy_blue') + fg('yellow')
c3 = bg('navy_blue') + fg('green')

config = open(args.config, 'r')
config_strucs = json.load(config)
scenarios = config_strucs['Scenarios']
facets = config_strucs['Facets']
roles = config_strucs['Roles']

if args.role not in roles:
    print(f"{r1}Error: Role {args.role} not found in configuration{c1}")
    exit(1)

if args.scenario not in scenarios:
    print(f"{r1}Error: Scenario {args.scenario} not found in configuration{c1}")
    exit(1)

action = args.action
if action=="a":
    action="assemble"

print(f"There are scenarios:{len(scenarios)} facets:{len(facets)} roles:{len(roles)} roles")

if action=="list":
    print("Scenarios")
    for k1, v1 in scenarios.items():
        print(f"{c1}  {k1}")
        for k2, v2 in v1.items():
             if k2=="FacetLayouts":
                  for k3, v3 in v2.items():
                       print(f"{c2}  FacetLayout: {k3} - {v3}")
             elif k2=="RoleMappings":
                  for k3, v3 in v2.items():
                       print(f"{c3}  RoleMapping: {k3} - {v3}")
elif action=="assemble":
    print(f"Assembling {args.outfile} for scenario:{args.scenario} and role:{args.role}")
    sdict = scenarios[args.scenario]

    fldict = sdict["FacetLayouts"]
    rmdict = sdict["RoleMappings"]
    rdict = roles[args.role]

    if args.role not in fldict:
        print(f"{r1}Error: Role {args.role} not found in RoleMappings for scenario {args.scenario}  {c1}")
        exit(1)


    fldict = sdict["FacetLayouts"][args.role]
    olst = []
    for fline in fldict:
        line = f"{fline}\n"
        olst.append(line)

    ofile = open(args.outfile,"w")
    ofile.writelines(olst)
    ofile.close()
    print(f"Wrote {len(olst)} lines to {args.outfile}")




elap = time.time()-starttime

print(f"{c1}Assembly  took {c2}{elap:.3f}{c1} secs ")