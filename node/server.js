var http = require("http");
var fs = require("fs");
var os = require("os");
var ip = require('ip');

function formatTime(seconds) {
  seconds = Math.ceil(seconds); // Round up to the nearest full integer
  const days = Math.floor(seconds / (24 * 60 * 60));
  const hours = Math.floor((seconds % (24 * 60 * 60)) / (60 * 60));
  const minutes = Math.floor((seconds % (60 * 60)) / 60);
  seconds = seconds % 60;

  const timeArray = [];

  if (days >= 0) {
    timeArray.push(`${days} d`);
  }
  if (hours > 0) {
    timeArray.push(`${hours} h`);
  }
  if (minutes > 0) {
    timeArray.push(`${minutes} m`);
  }
  if (seconds > 0) {
    timeArray.push(`${seconds} s`);
  }

  return timeArray.join(', ');
}



http.createServer(function(req, res){

    if (req.url === "/") {
        fs.readFile("./public/index.html", "UTF-8", function(err, body){
        res.writeHead(200, {"Content-Type": "text/html"});
        res.end(body);
    });
}
    else if(req.url.match("/sysinfo")) {
        myHostName=os.hostname();
	myUpTime=formatTime(os.uptime());
	myTotalMem=(os.totalmem() / (1024 * 1024)).toFixed(2);
	myFreeMem=(os.freemem() / (1024 * 1024)).toFixed(2);
	myTotalCPU=os.cpus().length;
        html=`    
        <!DOCTYPE html>
        <html>
          <head>
            <title>Node JS Response</title>
          </head>
          <body>
            <p>Hostname: ${myHostName}</p>
            <p>IP: ${ip.address()}</p>
            <p>Server Uptime: ${myUpTime} </p>
            <p>Total Memory: ${myTotalMem} MB </p>
            <p>Free Memory: ${myFreeMem} MB</p>
            <p>Number of CPU cores: ${myTotalCPU}</p> 
          </body>
        </html>` 
        res.writeHead(200, {"Content-Type": "text/html"});
        res.end(html);
    }
    else {
        res.writeHead(404, {"Content-Type": "text/plain"});
        res.end(`404 File Not Found at ${req.url}`);
    }
}).listen(3000);

console.log("Server listening on port 3000");