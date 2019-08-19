pyinstaller -y --clean --windowed gui.spec
pushd dist
hdiutil create ./easyparallel.dmg -srcfolder easyparallel.app -ov
popd
cd dist
codesign --deep -s 'Code Sign Test' easyparallel.dmg
