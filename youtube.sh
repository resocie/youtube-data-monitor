#!/bin/bash

#Instala o ambiente e ajusta o arquivo activate
install() {

	#Cria o ambiente
	virtualenv -p python3 venv &> /dev/null
	source venv/bin/activate
	pip install -r requirements.txt &> /dev/null
	
	#Instala o pycodestyle
	pip install pycodestyle &> /dev/null
	pycodestyle youtube/youtube.py &> /dev/null
	
	#Instala o postgres
	case "$OSTYPE" in
  	darwin*)  brew install postgresql ;; 
  	linux*)   sudo apt-get install postgresql ;;
  	*)        echo "Sistema: $OSTYPE desconhecido, instale manualmente o PostGres" ;;
	esac

	#perguntar qual a key da api
	clear
	printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
	echo 'Digite a sua KEY da API do YouTube'
	read varkey
	echo export YOUTUBE_KEY=$varkey >> venv/bin/activate
	clear
	printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
	echo 'Digite seu usuário do PostGres'
	read varlogin
	echo 'Digite sua senha do PostGres'
	read -sp '' varpassword
	echo export DATABASE_URL=postgresql://$varlogin:$varpassword@localhost/youtube_database >> venv/bin/activate

	#Adiciona o deactivate do enviroment no activate
	sed -i '37s/.*/    fi\n\n    unset YOUTUBE_KEY\n    unset DATABASE_URL/' venv/bin/activate

}

#Faz a coleta dos dados
Run() {

	# Entrar no ambiente
	. venv/bin/activate

	#Executar o update do youtube
	python -m youtube.update

	#sair do ambiente
	deactivate

}

#Executa os testes unitários
Test() {
	# Entrar no ambiente
	. venv/bin/activate

	#Executa os testes
	python -m unittest discover tests
	
	#sair do ambiente
	deactivate
}

#Mostra os comandos
Help() {
	clear
	printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
	echo Caso seja sua primeira vez executando o programa, primeiro instale o ambiente e as configurações da máquina.
	printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
	echo 
	echo *Para instalar o ambiente e configurar a máquina para as coletas, digite '"bash Youtube install"' no terminal sem as aspas.
	echo 
	echo *Para fazer uma coleta, digite '"bash Youtube run"' no terminal sem as aspas.
	echo 
	echo *Para executar os testes unitários, digite '"bash Youtube test"' no terminal sem as aspas.
	echo 
	echo *Para rever essas mensagens de ajuda, digite '"bash Youtube"' ou '"bash Youtube help"' no terminal sem as aspas.
	echo 

}

case $1 in
install)
 clear
 echo Configurando ambiente...
 install
 echo Instalação concluida.
;;
run)
 clear
 echo Fazendo a coleta dos dados...
 Run
 echo Coleta concluida.
;;
test)
 clear
 echo Executando os testes...
 Test
 echo Testes concluidos.
;;
help)
 Help
;;
*)
 Help
;;
esac
