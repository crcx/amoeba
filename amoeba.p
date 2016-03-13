[ "v-"  `9000 ] '?' :
[ "-"   `9010 ] '.s' :
[ "-"   `9020 ] 'bye' :
[ "-"   `9030 ] 'words' :
[ "-p"  `9040 ] 'wordlist' :

"File Operations"
[ "string:name string:mode - number:file-id"  `3000 ] 'open-file' :
[ "number:file-id -"  `3001 ] 'close-file' :
[ "number:file-id - character"  `3002 :c ] 'read-file' :
[ "character number:file-id -"  `3003 ] 'write-file' :
[ "number:file-id - number:position"  `3004 ] 'file-position' :
[ "number:offset number:file-id -"  `3005 ] 'file-seek' :
[ "number:file-id - number:length"  `3006 ] 'file-size' :
[ "string:name -"  `3007 ] 'delete-file' :

[ 'FID'  'S' ] {
  dup ::
  [ "string:name - string:contents" \
    'r' open-file !FID \
    request !S @S pop drop \
    @FID file-size [ @FID read-file @S push ] times \
    @FID close-file \
    @S :s \
  ] 'slurp-file' :
}

[ "string:name - flag"  `3008 ] 'file-exists?' :

[ "s-" `4000 ] 'include' :



"Conditionals"
[ eq? ] '=' :
[ -eq? ] '<>' :
[ gt? ] '>' :
[ lt? ] '<' :
[ gteq? ] '>=' :
[ lteq? ] '<=' :
