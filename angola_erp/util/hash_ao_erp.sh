#!/bin/bash

Certif="$1"
fichesha="$2"
fichetxt="$3"
fiche64="$4"

echo $Certif
echo $fichesha
echo $fichetxt
echo $fiche64

echo Desenvolvido para gerar HASH em Factura de Compras, Factura de Vendas, Movimentos de Stock,etc... AGT request

echo Leitura dos Ficheiros...

contador=1
exttxt=".txt"
extsha=".sha1"
extb64=".b64"
ficheirotxt='/tmp/registo'$contador$exttxt
ficheirotxta='/tmp/registo'$contador'a'$exttxt
ficheirosha='/tmp/registo'$contador$extsha
ficheirob64='/tmp/registo'$contador$extb64

echo $ficheirotxt
echo $ficheirotxta
echo $ficheirosha
echo $ficheirob64

echo Verifica se o $ficheirotxt existe

while true; do
	if [ -f $ficheirotxt ]; then
		echo SIGNING DOC
		if [ $contador == "1" ]; then
			echo CONTADOR 1
			openssl dgst -sha1 -sign "$HOME/frappe-bench/apps/angola_erp/angola_erp/util/angolaerp-selfsigned-priv.pem" -out $ficheirosha $ficheirotxt

			openssl enc -base64 -in $ficheirosha -out $ficheirob64 -A

			echo Verifying....
			openssl dgst -sha1 -verify "$HOME/frappe-bench/apps/angola_erp/angola_erp/util/publickey.pem" -signature $ficheirosha $ficheirotxt
		else
			echo CONTADOR $contador
                       	openssl dgst -sha1 -sign "$HOME/frappe-bench/apps/angola_erp/angola_erp/util/angolaerp-selfsigned-priv.pem" -out $ficheirosha $ficheirotxta

                        openssl enc -base64 -in $ficheirosha -out $ficheirob64 -A

                        echo Verifying....
                        openssl dgst -sha1 -verify "$HOME/frappe-bench/apps/angola_erp/angola_erp/util/publickey.pem" -signature $ficheirosha $ficheirotxta

		fi
		echo FICHEIROS
		echo $ficheirotxt
		echo $ficheirotxta

                ficheirotxta='/tmp/registo'$((contador+1))'a'$exttxt

		for x in `cat $ficheirob64`
		do 
        		echo "`cat $ficheirotxt`$x" >> $ficheirotxta
		done

		contador=$((contador+1))
		ficheirotxt='/tmp/registo'$contador$exttxt
		ficheirob64='/tmp/registo'$contador$extb64
		ficheirosha='/tmp/registo'$contador$extsha


		echo PROXIMOS FILES
		echo $ficheirotxt
		echo $ficheirotxta
	else
		break
	fi
done
