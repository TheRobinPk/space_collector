PORT=$(python -c "import random; print(random.randint(50000, 60000))")
echo "La compétition se passe sur 127.0.0.1:$PORT"

python killall.py
find . -name "*.log" -exec rm \{} \;

python -m space_collector.game.server -p $PORT &
python -m space_collector.viewer -p $PORT &
sleep 2
# python -m serial2tcp -p $PORT &
python -m sample_player_client -p $PORT &
python -m sample_player_client -p $PORT &
python -m sample_player_client -p $PORT &
python -m sample_player_client -p $PORT &

sleep 300
python killall.py
