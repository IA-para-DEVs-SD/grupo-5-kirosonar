// SonarLint: Missing catch block
function parseJSON(text) {
    try {
        return JSON.parse(text);
    }
    // Missing catch block
}
