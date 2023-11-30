cite about-plugin
about-plugin 'History functions'


################################################
alias hist='history' # shows all history
alias gh='history | grep ' # grep all history
# http://thirtysixthspan.com/posts/grep-history-for
# ghf - [G]rep [H]istory [F]or top ten commands and execute one
# usage:
#  Most frequent command in recent history
#   ghf
#  Most frequent instances of {command} in all history
#   ghf {command}
#  Execute {command-number} after a call to ghf
#   !! {command-number}
function hist_nlines {
    about 'Get last N entries from bash history. Defauklt withoutarguments is a 100 lines'
    group 'history'
    param '1: An integer corresponding to the number of history lines to tail'
    example '$ hist_nlines 200'

    if [ $# -eq 0 ]; then num_lines=100; else num_lines=$1; fi

    history | tail -n $num_lines;
}

function grep_history {
    about 'Grep bash history'
    group 'history'
    example '$ grep_history mkdir'

    history | grep "$1" ;
}

function _chop_first_column { awk '{for (i=2; i<NF; i++) printf $i " "; print $NF}' ; }

function _add_line_numbers { awk '{print NR " " $0}' ; }

function _top_ten { sort | uniq -c | sort -r | head -n 10 ; }

function _unique_history { _chop_first_column | _top_ten | _chop_first_column | _add_line_numbers ; }

function ghf {
    about 'Grep bash history Function'
    group 'history'
    param '1: With no args supplied, ghf returns the top 10 most used commands'
    param '2: With 1 search strings ghf returns top 10 uses for that term'
    param '3: With 2 search strings ghf executes a further search filter to the top10'
    example '$ grep_history mkdir'

    if [ $# -eq 0 ]; then hist_nlines | _unique_history; fi
    if [ $# -eq 1 ]; then grep_history "$1" | _unique_history; fi
    if [ $# -eq 2 ]; then
        $(grep_history "$1" | _unique_history | grep ^$2 | _chop_first_column)
    fi

    _fakecheese "boo"
}

################################################
# https://stackoverflow.com/questions/14750650/how-to-delete-history-of-last-10-commands-in-shell

function histdel {
    about 'Delete lines of history between N -> N+n. Excluding histdel iteself.'
    group 'history'
    param '1: starting line to delete'
    param '1: ending line to delete'
    example '$ histdel 1000 1033'

    for h in $(seq $1 $2 | tac); do
        history -d $h
    done
    history -d $(history 1 | awk '{print $1}')
}


function histdeln {
    about 'Delete last N lines of history including histdeln'
    group 'history'
    param '1: Number of lines to delete'
    example '$ histdeln 10'

    # deletes the last n lines of history including del history command

    # Get the current history number
    n=$(history 1 | awk '{print $1}')

    # Call histdel with the appropriate range
    histdel $(( $n - $1 )) $(( $n - 1 ))
}


function _fakecheese {
    group 'history'

    _bacon "yo"
    histdel $(( $n - $1 )) $(( $n - 1 ))
}

function _bacon {
    group 'history'

    _unique_history ""
    mayo ""
}


function mayo {
    group 'history'


}