#!/bin/bash

PARSER=./parse_menus2.py
OUT_FILE=index.html

function dl_menus {
    wget -nv "http://mollanasiankok.se/veckansmeny.html" -O mollan.html 1&> /dev/null
    wget -nv "http://gastrogate.com/restaurang/jonsjacob/page/3/" -O jons.html 1&> /dev/null
    wget -nv "http://web.comhem.se/hjulet/Matsedel.html" -O hjulet.html 1&> /dev/null
    wget -nv "http://restaurangkonigs.se/" -O konigs.html 1&> /dev/null
    week=$(($(date +%W | sed 's/^0*//')+1))
    year=`date +%Y`
    wget -nv "http://www.dengladarestaurangen.se/meny-v-${week}-${year}" -O glada.html 1&> /dev/null
    year2=`date +%y`
    wget -nv "http://www.matmakarna.nu/Veckomeny_Restaurang_Matmakarna/index_Vecka_${week}${year2}.html" -O matmakarna.html 1&> /dev/null
    wget -nv "http://mmcatering.nu/mfs-kafe-kok/meny" -O mf.html 1&> /dev/null
    wget -nv "http://gastrogate.com/restaurang/tango/page/3/" -O tango.html 1&> /dev/null
    wget -nv "http://restaurang-ns.com/restaurang-nanna-svartz/" -O nanna.html 1&> /dev/null
    wget -nv "http://gastrogate.com/restaurang/ksrestaurangen/page/3/" -O karolina.html 1&> /dev/null
    wget -nv "http://alfredsrestaurang.com/veckans_meny.html" -O alfred.html 1&> /dev/null
    wget -nv "http://gastrogate.com/restaurang/tango/page/3/" -O tango.html 1&> /dev/null
    wget -nv "http://61an.kvartersmenyn.se/" -O 61an.html 1&> /dev/null
}

dl_menus

${PARSER} glada=glada.html karolina=karolina.html hjulet=hjulet.html jons=jons.html konigs=konigs.html mollan=mollan.html nanna=nanna.html subway=true mf=mf.html jorpes=true alfred=alfred.html tango=tango.html 61an=61an.html haga=true, stories=true > ${OUT_FILE}
