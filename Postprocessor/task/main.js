const fs = require("node:fs");
const crypto = require("node:crypto");

const header = "id, nickname, password, consent to mailing";

fs.readFile("database.csv", "utf-8", (err, data) => {
    if (err) throw err;

    const rows = data.split("\n");

    // Filter out rows with incomplete data.
    const validRows = rows.filter(row => !row.includes("-"));

    // Reorder the indexes and hash the passwords.
    const reorderedRows = validRows.map((row, index) => {
        if (index === 0) {
            return header;
        }

        const record = row.split(", ");
        record[0] = String(index);
        record[2] = crypto.createHash("sha256").update(record[2]).digest("hex");

        return record.join(", ");
    });

    // Write the reordered and hashed data to filtered_database.csv.
    fs.writeFileSync("filtered_database.csv", reorderedRows.join("\n"));
});