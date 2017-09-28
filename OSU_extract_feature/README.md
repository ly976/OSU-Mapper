

# How to

## Install dependencies
``` shell
pip install --upgrade git+https://github.com/OSU-Mapper/librosa.git@dynamic-tempo
```

## Extract features from audio
``` bash
# all
./extract-feature.sh Data/Beatmaps

# or just two ( for testing )
./extract-feature.sh Data/Beatmaps 2
```

### Default path to Beatmaps
Data/Beatmaps/*


## normalization
``` bash
python global_norm.py Data/Trainables
```

## map created
``` bash 
python coor-map.py refined_predict.csv
```



