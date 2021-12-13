now=$(date +"%s")

docker image build -t dc_bot:$now .

echo -e "\e[1;35m Build successfully \e[0m"

docker run -d -v /home/config/dc_bot/mp3:/discord/mp3 --name dc_bot dc_bot:$now

echo -e "\e[1;35m Added container \e[0m"