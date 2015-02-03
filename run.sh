#!/bin/bash

# Copyright (c) 2014, Linus Östberg
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of kimenu nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

PARSER=./parse_menus2.py
OUT_FILE=index.html
# an attempt to compensate for the instability in the naming of the menu page for glada restaurangen
function get_glada {
    GLADA=glada.html
    week=$(($(date +%W | sed 's/^0*//')+1))
    year=`date +%Y`
    wget -nv "http://www.dengladarestaurangen.se/meny-vecka-${week}" -O ${GLADA} 1&> /dev/null
    if [ -s ${GLADA} ] ; then
	return
    fi
    wget -nv "http://www.dengladarestaurangen.se/vecka-${week}" -O ${GLADA} 1&> /dev/null
}

function get_matmakarna {
    year2=`date +%y`
    week=$(($(date +%W | sed 's/^0*//')+1))
    if [ ${#week} -eq 1 ] ; then
	week=0${week}
    fi
    echo $week
    wget -nv "http://www.matmakarna.nu/Veckomeny_Restaurang_Matmakarna/index_Vecka_${week}${year2}.html" -O matmakarna.html 1&> /dev/null
}
    

function dl_menus {
    wget -nv "http://mollanasiankok.se/veckansmeny.html" -O mollan.html 1&> /dev/null
    wget -nv "http://gastrogate.com/restaurang/jonsjacob/page/3/" -O jons.html 1&> /dev/null
    wget -nv "http://gastrogate.com/restaurang/restauranghjulet/page/3/" -O hjulet.html 1&> /dev/null
    wget -nv "http://restaurangkonigs.se/" -O konigs.html 1&> /dev/null
    get_glada
    get_matmakarna
    wget -nv "http://mmcatering.nu/mfs-kafe-kok/meny" -O mf.html 1&> /dev/null
    wget -nv "http://gastrogate.com/restaurang/tango/page/3/" -O tango.html 1&> /dev/null
    wget -nv "http://restaurang-ns.com/restaurang-nanna-svartz/" -O nanna.html 1&> /dev/null
    wget -nv "http://gastrogate.com/restaurang/ksrestaurangen/page/3/" -O karolina.html 1&> /dev/null
    wget -nv "http://alfredsrestaurang.com/veckans_meny.html" -O alfred.html 1&> /dev/null
    wget -nv "http://gastrogate.com/restaurang/tango/page/3/" -O tango.html 1&> /dev/null
    wget -nv "http://61an.kvartersmenyn.se/" -O 61an.html 1&> /dev/null
    wait
}

dl_menus

${PARSER} glada=glada.html karolina=karolina.html hjulet=hjulet.html jons=jons.html konigs=konigs.html mollan=mollan.html nanna=nanna.html subway=true mf=mf.html jorpes=true alfred=alfred.html tango=tango.html 61an=61an.html haga=true, stories=true matmakarna=matmakarna.html > ${OUT_FILE}
