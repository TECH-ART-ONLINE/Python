from maya import cmds

# スキンクラスターを取得する
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

# スキンクラスターのインフルエンスを取得する
def getSkinInfluences(skinCluster):
    influences = cmds.skinCluster(skinCluster, q=True, inf=True)
    return influences
    
# 使用例
nodes = cmds.ls(sl=True, type="transform")
for node in nodes:
    skinCluster = getSkinCluster(node)
    print(getSkinInfluences(skinCluster))
    

# ローカルアクシスの設定
nodes = cmds.ls(sl=True, type="joint")
value = True
for node in nodes:
    cmds.setAttr("{}.displayLocalAxis".format(node), value)

    
# 選択した階層以下のジョイントの回転を0にする
nodes = cmds.ls(sl=True, dag=True, type="joint")
for node in nodes:
    cmds.setAttr("{}.rotate".format(node), 0, 0, 0)


# 末端ノードの情報だけ取得してJointOrientの値を確認する
def get_end_nodes(node):
  children = cmds.listRelatives(node, children=True, type="transform")
  if not children:
    return [node]
  end_nodes = []
  for child in children:
    end_nodes.extend(get_end_nodes(child))
  return end_nodes

root_node = "Armature"  # ルートノードの名前
end_nodes = get_end_nodes(root_node)
for node in end_nodes:
    print(cmds.getAttr("{}.jointOrient".format(node)))