#! /usr/bin/env bash

function help() {
	echo "Inicializa el Sistema de Turnos."
	echo -e "Uso: $0 [parametros]\n"
	echo "Parametros:"
	echo -e "\t-m, --medic <numero>\t\tCantidad de Medicos a inicializar."
	echo -e "\t-r, --reception <numero>\t\tCantidad de Recepcionistas a inicializar."
	echo -e "\t-w, --waiting-room <numero>\t\tCantidad de Salas de Espera a inicializar.\n"
	exit 2
}

# -- Parse Args -- #
MEDIC=1
RECEPTION=1
WAITING_ROOM=1

SHORT=m,r,w,?
LONG=medic:,reception:,waiting-room:,help
OPTS=$(getopt -a -n run --options $SHORT --longoptions $LONG -- "$@")

if [ $? != 0 ]; then
	echo "[Error] - Operacion desconocida"
	echo "Intenta $0 --help/-h/-? para descubrir como funciona el programa"
	exit 1
fi

eval set -- "$OPTS"

while :
do
	case "$1" in
		-m | --medic)
			MEDIC="$2"; shift 2;;
		-r | --reception)
			RECEPTION="$2"; shift 2;;
        -w | --waiting-room)
			WAITING_ROOM="$2"; shift 2;;
		-h | --help)
			help;;
		--)
			shift; break;;
		*)
			echo "Opcion invalida: $1";;
	esac
done

# -- Main -- #
rm -rf logs
mkdir -p logs

for i in $( seq 1 $RECEPTION ); do
    echo "Inicializando Recepcion N°$i..."
    python src/Reception.py > logs/reception_$i.log 2>&1 &
done

for i in $( seq 1 $MEDIC ); do
    echo "Inicializando Medico N°$i..."
    python src/Medic.py $i > logs/medic_$i.log 2>&1 &
done

for i in $( seq 1 $WAITING_ROOM ); do
    echo "Inicializando Sala de Esperas N°$i..."
    python src/WaitingRoom.py > logs/waiting_room_$i.log 2>&1 &
done

echo -e "\n Pueden ver el output de cada programa dentro de la carpeta \"logs\"."

echo "Iniciando servidor como demonio..."
python src/Server.py
