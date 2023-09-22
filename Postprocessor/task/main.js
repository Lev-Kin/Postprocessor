const fs = require('fs');

// Read the database.csv file
fs.readFile('database.csv', 'utf8', (err, data) => {
    if (err) {
        console.error("Error reading the file:", err);
        return;
    }

    // Split the file content into lines
    const lines = data.trim().split('\n');

    // Take the last line and split it into columns
    const lastLine = lines[lines.length - 1].split(',');

    const nickname = lastLine[1].trim();
    const consent = lastLine[3].trim() === "yes" ? "yes" : (lastLine[3].trim() === "no" ? "no" : "unknown");

    console.log(`The user ${nickname} has "${consent}" consent status for sending emails`);
});

