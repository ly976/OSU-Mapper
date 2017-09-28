#

version=1

count=99999
allsets_path="Data/Beatmaps"

while [[ $# -gt 1 ]]
do
    key="$1"

    case $key in
        -n|--number)
            count="$2"
            echo "=== Using $count beatmaps."
            shift # past argument
            ;;
        -f|--file)
            file="$2"
            echo "=== Only beatmap start with \`$file\`."
            shift # past argument
            ;;
        -s|--start|--skip)
            start="$2"
            skip="true"
            echo "=== Start from Beatmap Set: \`$start\`."
            shift # past argument
            ;;
        --nothing)
            if [ "$2" = 1 ] || [ "$2" = "true" ]; then
                nothing="true"
            fi
            shift # past argument
            ;;
        --default) # Does nothing
            DEFAULT=YES
            ;;
        *)
                  # unknown option
            ;;
    esac
    shift # past argument or value
done

case $1 in
    -h|--help)
        echo "Usage: $0 <-f [id]> <-n [number]> DIRECTORY
        arguments:
            -f, --file [beatmapset_id]
                Just Extract filename begining with [beatmapset_id]
                Will match just the begining of a string.
                This will not display what is skipped.
                    e.g. 1 will match 1 11 and 123
            -n, --number [count]
                Maximium number of beatmap sets to extract
            --nothing [true/false/1/0]
                Do nothing just scan files if [true]
            -s, --start, --skip [filename]
                Start from file [filename], skip the previouses.
                You could use either part of the filename or an beatmap set id.

        example:
            $0
                Do everything
            $0 -file 139677 Data/Beatmaps
                Only Extract \`139677\` from Dir: Data/Beatmaps
            $0 -file 1 -n 1
                Only Exteact the first Beatmap Set starting with \`1\` 
            $0 --nothing 1
                See What to be extracted.
            $0 -file 1 --nothing 1
                
            $0 -n 1 --nothing true
                Test to see the first Beatmap Set 
            $0 --nothing 1 -s 307
                Test to see what will be extracted staring from 
                beatmap set id begining with \`307\`
        " >&2
        exit 1
        shift # past argument
        ;;
    *)
        ;;
esac

if [ "$#" -eq 1 ]; then
    allsets_path="$1"
fi

if ! [ -d "$allsets_path" ]; then
    echo "Usage: $0 <-f beatmap id> <-n max beatmapsets to process> DIRECTORY
    See $0 --help" >&2
    exit 1
fi

trainable_gather_path="Data/Trainables"
mkdir -p  "$trainable_gather_path"

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
beatmaps_sets=$(ls "$allsets_path" | grep "^$file")

echo "=== Using $allsets_path/"
for set_name in ${beatmaps_sets[@]}
do
    if [ "$skip" == true ]; then
        if [[ $set_name == *"$start"* ]]; then
            skip="false"
        else
            echo ">     Skiped: $set_name"
            continue
        fi
    fi 
    set_path="$allsets_path/$set_name"
    name=$(ls "$set_path"/*.osu | head -n 1)
    mp3name=$(python script/audioname.py "$name")
    mp3path="$set_path/$mp3name"
    echo ">     Extracting: $set_name"
    set_training_path="$set_path/Trainings" 
    mkdir -p "$set_training_path" 
    
    if ! [ "$nothing" == true ] ; then
        # A
        python script/mp3_to_tp.py "$mp3path" > "$set_training_path/timing_points.v$version.csv"
        # B
        python script/tp_to_mis.py "$set_training_path/timing_points.v$version.csv" > "$set_training_path/mis.v$version.csv"
        # D
        python script/mp3_mis_to_tr_f.py "$mp3path" "$set_training_path/mis.v$version.csv" > "$set_training_path/audio_features.v$version.csv"
    fi

    for osu_path in "$set_path"/*.osu; do
        osu_diff=$(python script/osuDiff.py "$osu_path")
        echo ">>     Difficulty: $osu_diff"
        if ! [ "$nothing" == true ] ; then
            # C
            python script/osu_to_target.py "$osu_path" > "$set_training_path/$osu_diff.target_features.v$version.csv"
            # E
            python script/target_mis_to_tr_t.py  \
                "$set_training_path/$osu_diff.target_features.v$version.csv" \
                "$set_training_path/mis.v$version.csv" \
                > "$set_training_path/$osu_diff.trainable_target.v$version.csv"
            # F
            python script/tr_f_tr_t_to_trainable.py \
                "$set_training_path/audio_features.v$version.csv" \
                "$set_training_path/$osu_diff.trainable_target.v$version.csv" \
                > "$set_training_path/$osu_diff.trainable_all.v$version.csv"
            # Done
            cp "$set_training_path/$osu_diff.trainable_all.v$version.csv" "$trainable_gather_path/$osu_diff.$set_name.trainable_all.v$version.csv" 
        fi
    done

    # Count down
    count=$((count - 1))
    if (("$count" <= "0")) 
    then
        break;
    fi
done
IFS=$SAVEIFS
