var http = require("http");
var data = require("C:/temp/widgets.json");

var server = http.createServer(function (req, res) {
    if (req.url === "/") {
        res.writeHead(200, { "Content-Type": "text/json" });
        res.end(formatData(data));
    } else if (req.url === "/blue") {
        listBlue(res);
    } else if (req.url === "/green") {
        listGreen(res);
    } else if (req.url === "/black") {
        listBlack(res);
    } else {
        res.writeHead(404, { "Content-Type": "text/plain" });
        res.end("Data not found");
    }
});

server.listen(3000);
console.log("Server is listening on port 3000");

function listBlue(res) {
    var colorBlue = data.filter(function (item) {
        return item.color === "blue";
    });

    res.end(formatData(colorBlue));
}

function listGreen(res) {
    var colorGreen = data.filter(function (item) {
        return item.color === "green";
    });

    res.end(formatData(colorGreen));
}

function listBlack(res) {
    var colorBlack = data.filter(function (item) {
        return item.color === "black";
    });

    res.end(formatData(colorBlack));
}

function formatData(jsonArray) {
    if (!Array.isArray(jsonArray)) {
        return "Invalid input; an array of JSON objects is required.";
    }

    const formattedStrings = jsonArray.map(item => {
        if (item.name && item.color) {
            const formattedName = item.name.charAt(0).toUpperCase() + item.name.slice(1);
            return `${formattedName} is the color ${item.color}.`;
        } else {
            return "Invalid JSON data; name and color properties are required.";
        }
    });

    return formattedStrings.join('\n');
}