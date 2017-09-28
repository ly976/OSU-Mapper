# 

mkdir -p "Data/Beatmaps" 

ext=".osz"
for path in Data/Beatmap-Packs/*/**.osz ;do
    filename=$(basename -s "$ext" "$path")
    if unzip "$path" -d "Data/Beatmaps/$filename"; then
        rm "$path"
    fi
done
