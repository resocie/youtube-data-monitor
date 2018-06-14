!/bin/bash
#Cria o ambiente
virtualenv -p python3 venv
pip install -r requirements.txt

#perguntar qual a key da api
echo Qual a sua KEY da API do YOUTUBE?
read varkey
echo API KEY $varkey
echo export YOUTUBE_KEY=$varkey >> venv/bin/activate

#Adiciona o deactivate do enviroment no activate
sed -i '39s/.*/    fi\n\n    unset YOUTUBE_KEY/' venv/bin/activate

# Entrar no ambiente
. venv/bin/activate

#Executar o update do youtube
python -m youtube.update

#sair do ambiente
deactivate
