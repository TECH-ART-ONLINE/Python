# maya2ue_remote_execution

MayaからUEに自動で出力したFBXをインポートするサンプルです。
これを利用するにはUnreal Engineのプロジェクト設定で、

Enable Remote Execution? を有効にする必要があります。
またUnreal Engineを起動した状態で行います。

### ue_import_fbx.py
ueで実行するfbxインポートのスクリプトです。

### maya_remote_execution.py
Mayaで実行するスクリプトです。
こちらでue_import_fbx.pyを実行させます。

# optionvar_gui
optionVarを使ったGUIの位置・サイズ保存のサンプル
