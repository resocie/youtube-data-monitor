#!/bin/bash

#Instala o ambiente e ajusta o arquivo activate
install() {

	#Cria o ambiente
	virtualenv -p python3 venv
	pip install -r requirements.txt

	#perguntar qual a key da api
	echo Qual a sua KEY da API do YOUTUBE?
	read varkey
	echo export YOUTUBE_KEY=$varkey >> venv/bin/activate

	#Adiciona o deactivate do enviroment no activate
	sed -i '39s/.*/    fi\n\n    unset YOUTUBE_KEY/' venv/bin/activate

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

#Mostra os comandos
Help() {
	clear
	echo *Caso seja sua primeira vez executando o programa, instale primeiro o ambiente e as configurações da máquina.
	echo 
	echo *Para instalar o ambiente e configurar a máquina para as coletas, digite '"bash Youtube install"' no terminal sem as aspas.
	echo 
	echo *Para fazer uma coleta, digite '"bash Youtube run"' no terminal sem as aspas.
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
help)
 Help
;;
*)
 Help
;;
esac
