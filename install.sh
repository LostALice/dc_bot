now=$(date +"%s")

docker image build -t dc_bot:$now .

echo "\e[1;35m Build successfully \e[0m"