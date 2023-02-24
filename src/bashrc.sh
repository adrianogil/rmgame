export RMGAME_DATA_DIR=$RMGAME_DIR/../data/

if [ -z "$RMGAME_PYTHON_PATH" ]
then
    export RMGAME_PYTHON_PATH=$RMGAME_DIR/python/
    export PYTHONPATH=$RMGAME_PYTHON_PATH:$PYTHONPATH
fi

alias txtmgame="python3 -m rmgame.game"
