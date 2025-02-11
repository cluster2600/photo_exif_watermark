tell application "Photos"
    set targetAlbum to album "Djanet 2025"
    set filePaths to {}
    
    repeat with aPhoto in (get media items of targetAlbum)
        if aPhoto is RAW then
            set end of filePaths to (POSIX path of (filename of aPhoto))
        end if
    end repeat
    
    return filePaths as text
end tell