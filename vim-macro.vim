nnoremap <space>\ :call FindJSON()<cr>
function! FindJSON()
    "let json_path = system('find -name ../json/' . expand('%:r'))
    "execute 'e' json_path
    let @"="find .. -name " . expand('%:r') . ".json | xargs vim"
endfunction
