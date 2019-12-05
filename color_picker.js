// Sample code snippet for use in Node Red
// to convert output of color picker UI element to prefered output for MQTT

str = msg.payload;
start_removed = str.replace("rgb(", "");
end_removed = start_removed.replace(")", "");
spaces_removed = end_removed.replace(/ /g,"");

newmsg = {"payload": spaces_removed}

return newmsg;
