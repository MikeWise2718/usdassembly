# Readme for Assembly.py
1 Oct 2023 - Mike Wise

To do:
  - create config for WPP
  - create config for BAE
  - actually generate USD for BAE and WPP examples


Version 1 - assemble.py
============================
Sample:
   `python assemble.py -c ScenarioDefsOrg.json -s SitAware -of out.txt -a a -r Admin`
Output:
   There are scenarios:2 facets:9 roles:3 roles
   Assembling out.txt for scenario:SitAware and role:Admin
   Wrote 8 lines to out.txt
   Assembly  took 0.028 secs

Version 2 - buildstage.py
=========================
- Changed name to avoid cocept collision with OpenUSD's Model Assembly
- Added a subfacet layer to seperate subfacet concerns from versioning
- Made versioning more "git-like"
   `python buildstage.py -c BaeDefs.json -s DroneDesign -of out.txt -a a -r Admin`