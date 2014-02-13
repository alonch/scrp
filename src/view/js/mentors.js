function copyEmails(){
    text = ''
    for(i in mentors){
      text += mentors[i]['email'] + ", "
    } 
    text = text.substring(0,text.length-2)

    window.prompt("Copy to clipboard: Ctrl+C, Enter", text);
}