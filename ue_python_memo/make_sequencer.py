import unreal

# 関数インスタンス
editor_asset_lib = unreal.EditorAssetLibrary()
editor_level_lib = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
editor_actor_lib = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
unreal_editor_lib = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)

# 定数
package_path = "/Game/Characters/"

# ポストプロセスボリュームが入ったレベル（サブレベル）を作る
subLevel = "{}LV_SubLevel".format(package_path)
editor_level_lib.new_level(subLevel)
ppv = unreal.EditorLevelLibrary.spawn_actor_from_class(
    unreal.PostProcessVolume.static_class(),
    unreal.Vector(0, 0, 0),
    unreal.Rotator(0, 0, 0)
)

ppv.unbound = True
ppv_settings = ppv.get_editor_property("settings") # type: unreal.PostProcessSettings
pm = editor_asset_lib.load_asset('{}/PM_Red'.format(package_path))
ppm_arry = list()
ppm_dict = dict()
ppm_dict["weight"] = 1.0
ppm_dict["object"] = pm
ppm_arry.append(ppm_dict)
weights = unreal.WeightedBlendables()
weights.array = ppm_arry
ppv_settings.set_editor_property("weighted_blendables", weights)
editor_level_lib.save_all_dirty_levels()

# パーシスタントレベル（親レベル）を作る
persistantLevel = "{}LV_Persistant".format(package_path)
editor_level_lib.new_level(persistantLevel)
world_level = unreal_editor_lib.get_editor_world()
unreal.EditorLevelUtils.add_level_to_world(
    world_level,
    subLevel,
    unreal.LevelStreamingAlwaysLoaded
)
editor_level_lib.save_all_dirty_levels()

# シーケンサーを作り、PPVを動かす
sequence = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
    "LS_Test",
    package_path,
    unreal.LevelSequence,
    unreal.LevelSequenceFactoryNew()
    )

ppv = unreal.find_object(editor_level_lib.get_current_level(), "PostProcessVolume_0")
ppv_binding = sequence.add_possessable(ppv)
weight_track = ppv_binding.add_track(unreal.MovieSceneFloatTrack)
weight_track.set_property_name_and_path(
    'Weight(Array[0])',
    'Settings.WeightedBlendables.Array[0].Weight'
)

section = weight_track.add_section()
section.set_blend_type(unreal.MovieSceneBlendType.ABSOLUTE)
editor_asset_lib.save_asset(sequence.get_outermost().get_path_name())