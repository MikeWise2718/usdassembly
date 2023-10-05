
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


config = open(args.config, 'r')
config_strucs = json.load(config)
scenarios = config_strucs['Scenarios']
facets = config_strucs['Facets']
roles = config_strucs['Roles']

print(f"There are scenarios:{len(scenarios)} facets:{len(facets)} roles:{len(roles)} roles")

if args.action=="list":
    print("Scenarios")
    for k1, v1 in scenarios.items():
        print(f"  {k1}")
        for k2, v2 in v1.items():
             if k2=="Facets":
                  for k3, v3 in v2.items():
                       print(f"  Facets for Role: {k3} - {v3}")
             else:
                 print(f"  {k2} - {v2}")
else:
    print(f"Assembling {args.outfile} for scenario:{args.scenario} and role:{args.role}")
    sdict = scenarios[args.scenario]
    rdict = roles[args.role]

    olst = []
    facets = sdict["Facets"][args.role]
    for fline in facets:
        line = f"{fline}\n"
        olst.append(line)

    ofile = open(args.outfile,"w")
    ofile.writelines(olst)
    ofile.close()
    print(f"Wrote {len(olst)} lines to {args.outfile}")


c1 = bg('navy_blue') + fg('white')
c2 = bg('navy_blue') + fg('yellow')

elap = time.time()-starttime

print(f"{c1}Assembly  took {c2}{elap:.3f}{c1} secs ")