[ "v-"  `9000 ] '?' define
[ "-"   `9010 ] '.s' define
[ "-"   `9020 ] 'bye' define
[ "-"   `9030 ] 'words' define
[ "-p"  `9040 ] 'wordlist' define

"File Operations"
[ "string:name string:mode - number:file-id"  `3000 ] 'open-file' define
[ "number:file-id -"  `3001 ] 'close-file' define
[ "number:file-id - character"  `3002 :c ] 'read-file' define
[ "character number:file-id -"  `3003 ] 'write-file' define
[ "number:file-id - number:position"  `3004 ] 'file-position' define
[ "number:offset number:file-id -"  `3005 ] 'file-seek' define
[ "number:file-id - number:length"  `3006 ] 'file-size' define
[ "string:name -"  `3007 ] 'delete-file' define

[ 'FID'  'S' ] {
  [ "string:name - string:contents" \
    'r' open-file !FID \
    request !S @S pop drop \
    @FID file-size [ @FID read-file @S push ] times \
    @FID close-file \
    @S :s \
  ] 'slurp-file' define
}

[ "string:name - flag"  `3008 ] 'file-exists?' define

[ "s-" `4000 ] 'include' define



"Conditionals"
[ eq? ] '=' define
[ -eq? ] '<>' define
[ gt? ] '>' define
[ lt? ] '<' define
[ gteq? ] '>=' define
[ lteq? ] '<=' define
