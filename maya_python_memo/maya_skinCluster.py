import time
from maya import cmds
from maya.api import OpenMaya as om2
from maya.api import OpenMayaAnim as oma2

# 実行時間を取得するラッパー
def timeit(func):
  def wrapper(*args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    print(f"{func.__name__} took {end - start:.4f} seconds")
    return result
  return wrapper


# スキンクラスターを取得
def getSkinCluster(node):
    histories = cmds.listHistory(node, pruneDagObjects=True, interestLevel=2)
    skinCluster = None
    for history in histories:
        if cmds.nodeType(history) == "skinCluster":
            skinCluster = history
            break
    if skinCluster is not None:
        return skinCluster
    return skinCluster


# maya.cmdsを利用したスキンウェイト値の取得
def cmds_get_per_vtx_skin_value(node):
    skinCluster = getSkinCluster(node)
    vertex_count = cmds.polyEvaluate(node, vertex=True)
    vertex_weights = [None] * vertex_count
    for i in range(vertex_count):
        weight = cmds.skinPercent(
                    skinCluster,
                    f"{node}.vtx[{i}]",
                    q=True,
                    value=True
                )
        vertex_weights[i] = weight
    return vertex_weights


# maya.cmdsを利用したスキンウェイト値の取得
def api2_get_per_vtx_skin_value(node):
    def split_list(lst, n):
        return [lst[i:i+n] for i in range(0, len(lst), n)]
    selection = om2.MSelectionList()
    selection.add(node)
    mesh_obj, mesh_comp = selection.getComponent(0)
    skinCluster = getSkinCluster(node)
    selection = om2.MSelectionList()
    selection.add(skinCluster)
    skin_obj = selection.getDependNode(0)
    skinCluster = oma2.MFnSkinCluster(skin_obj)
    weights = skinCluster.getWeights(mesh_obj, mesh_comp)
    weights = split_list(weights[0], weights[1])
    return weights


@timeit
def main_cmds():
    nodes = cmds.ls(sl=True, type="transform")
    for node in nodes:
        cmds_get_per_vtx_skin_value(node)
    return

@timeit
def main_api2():
    nodes = cmds.ls(sl=True, type="transform")
    for node in nodes:
        api2_get_per_vtx_skin_value(node)
    return

if __name__ == "__main__": 
    main_cmds() 
    main_api2()