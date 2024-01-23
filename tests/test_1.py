from pathlib import Path
from typing import List, Type
from pxr import Usd, UsdGeom
import json
from stager.stager import Stager


def setup_module():
    Path("./test_usd_files").mkdir(parents=True, exist_ok=True)
    # print('This is setup_module method, executed only once when there are multiple test classes.')


def teardown_module():
    # print('This is teardown_module method, executed only once when there are multiple test classes.')
    pass


def setup_function():
    # print('This is setup_function method, executed only once when there are multiple test classes.')
    pass


def teardown_function():
    # print('This is teardown_function method, executed only once when there are multiple test classes.')
    pass


def find_prims_by_type(stage: Usd.Stage, prim_type: Type[Usd.Typed]) -> List[Usd.Prim]:
    found_prims = [x for x in stage.Traverse() if x.IsA(prim_type)]
    return found_prims


def delete_file_if_exists(fname: str):
    if Path(fname).exists():
        Path(fname).unlink()  # the modern way to delete a file
    if Path(fname).exists():
        assert False  # oppsie, we failed to delete the file

    # parser.add_argument("-c", "--config", action='store', required=True, help="Configuration File",
    #                     default="config.json")
    # parser.add_argument("-a", "--action", action='store',
    #                     required=False, help="List or Assemble", default="list")
    # parser.add_argument("-s", "--scenario", action='store', required=False, help="Senario for stage creation",
    #                     default="Default")
    # parser.add_argument("-r", "--role", action='store', required=False, help="Role for which to create stage",
    #                     default="User")
    # parser.add_argument("-of", "--outfile", action='store',
    #                     required=True, help="Output file", default="")
    # parser.add_argument("-v", "--verbose", action='store_true', default=False)
    # parser.add_argument("-ar", "--assetroot", action='store', required=False, help="Asset root path for USD files")

    # python buildstage.py -c BaeDefs.json -s DroneDesign -of out.usda -a a -r


def do_generate_model(scenario, usdname, role):
    config = open("tests/DroneDefs.json", 'r')
    config_json: dict = json.load(config)

    stager = Stager(config_json)
    stager.Validate()

    usdfile = "./test_usd_files/" + usdname
    delete_file_if_exists(usdfile)
    assetroot = None

    stager.BuildStage(scenario, role, usdfile, assetroot)


def test_complete_model():
    do_generate_model("DroneComplete", "drone_complete_model.usda", "Admin")


def test_minimal_model():
    do_generate_model("DroneMinimal", "drone_minimal_model.usda", "ProgramManager")


def test_drone_design_model():
    do_generate_model("DroneDesign", "drone_design_model.usda", "DroneDesigner")


def test_payload_camera_design_model():
    do_generate_model("PayloadDesignCamera", "payload_design_model.usda", "PayloadDesigner")
