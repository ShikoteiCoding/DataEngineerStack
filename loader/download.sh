#!/bin/sh
# download.sh

# For demo
echo $KAGGLE_USERNAME
echo $KAGGLE_KEY

kaggle datasets download smid80/coronavirus-covid19-tweets-early-april -p /data  --unzip -o
echo "dataset download done"