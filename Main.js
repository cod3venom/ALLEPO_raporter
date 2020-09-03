const electron = require('electron');
const url = require('url');
const path = require('path');
var net = require('net');
const {app,BrowserWindow} = electron;
let mainWindow;


app.on('ready',function(){
    mainWindow = new BrowserWindow({
        webPreferences:{
            nodeIntegration:true
        }
    });
    mainWindow.loadURL(url.format({
        pathname: path.join(__dirname,'content/HTML/index.html'),
        protocol:'file:',
        slashes: true
    }));
    mainWindow.webContents.openDevTools();
});


var server = net.createServer(function(connection){
    console.log('CLIENT  CONNECTED');
    connection.on('data',function(data){
        data = data.toString();
        if(data.includes('_'))
        {
            command = data.split('_');
            if(command[0] === 'stack')
            {
                if(data.includes('$'))
                {
                    pack = data.replace('stack_','').split('$');
                    console.log(pack)
                    mainWindow.webContents.send('pack',pack);
                }
            }
            
        }
    });
    connection.on('end',function(){
        console.log('CLIENT DISCONNECTED');
    });
    connection.on('error',function(ex){
        console.log(ex)
    });

    connection.write('SERVER IS UP');
    connection.pipe(connection);
});

server.listen(8080,function(){
    console.log('server is listening');
});