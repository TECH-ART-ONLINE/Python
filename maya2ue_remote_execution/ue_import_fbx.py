import unreal
import sys
fbx_path = sys.argv[1]
uasset_name = unreal.Paths.get_base_filename(fbx_path)

# FBXインポート時の設定
fbx_import_options = unreal.FbxImportUI()
fbx_import_options.import_materials = True
fbx_import_options.reset_to_fbx_on_material_conflict = False
fbx_import_options.automated_import_should_detect_type = False
fbx_import_options.static_mesh_import_data.set_editor_property("combine_meshes", True)
fbx_import_options.static_mesh_import_data.build_nanite = True
fbx_import_options.static_mesh_import_data.generate_lightmap_u_vs = False
# FBXインポートのタスクを生成
task = unreal.AssetImportTask()
task.automated = True
task.replace_existing = True
task.replace_existing_settings = True
task.destination_name = uasset_name # UE4上のアセット名
task.destination_path = '/Game/FromMaya' # アセットを保存するフォルダ
task.filename = fbx_path # 読み込みたいFBXファイル名を指定する
task.options = fbx_import_options
tasks = [task]

asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
asset_tools.import_asset_tasks(tasks)