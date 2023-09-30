const fs = require('fs');
const crypto = require('crypto');

// Function to hash a password using SHA-256
function hashPassword(password) {
    return crypto.createHash('sha256').update(password).digest('hex');
}

// Read the database.csv file
fs.readFile('database.csv', 'utf8', (err, data) => {
    if (err) {
        console.error("Error reading the file:", err);
        return;
    }

    // Split the file content into lines
    const lines = data.trim().split('\n');

    // Process each line to hash the password, skipping the header
    const hashedData = lines.map((line, index) => {
        if (index === 0) return line; // If it's the header, return as is

        const parts = line.split(',');
        parts[2] = hashPassword(parts[2].trim());
        return parts.join(', ');
    });

    // Write the hashed data to hash_database.csv
    fs.writeFileSync('hash_database.csv', hashedData.join('\n'));
});
