import maya.cmds as cmds
import maya.OpenMaya as om


def generate_fbx():
    # FBXの出力先
    file_path = cmds.file(query=True, sceneName=True)
    file_path = file_path.replace(".mb", ".fbx")
    
    # FBX書き出しに必要なプラグインをロード
    cmds.loadPlugin('fbxmaya', qt=True)
    
    # 書き出すノードを選択状態から取得
    nodes = cmds.ls(sl=True)
    cmds.file(q=True, loc=True)
    # 現在のFBX書き出し設定をスタックにプッシュ（一時保存）
    cmds.FBXPushSettings()
    # Hoge
    
    try:
        # FBX書き出し設定をリセット
        cmds.FBXResetExport()
        
        # 入力コネクションを書き出さない設定
        cmds.FBXExportInputConnections('-v', 0) 
        cmds.FBXProperty("Export|IncludeGrp|Animation", "-v", 0)
        
        # カメラを書き出さない設定
        cmds.FBXExportCameras('-v', 0)
        
        # コンストレイントを書き出さない設定
        cmds.FBXExportConstraints('-v', 0)
        
        # ライトを書き出さない設定
        cmds.FBXExportLights('-v', 0)
        om.MGlobal.executeCommand('FBXExport("-f", "{}", "-s")'.format(file_path))
    
    # 例外発生時でも必ず実行される処理
    finally:
        # FBX書き出し設定をスタックからポップ（設定を元に戻す）
        cmds.FBXPopSettings()
    return file_path
    
fbx = generate_fbx()