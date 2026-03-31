// SonarLint: Implicit global variable
function setConfig() {
    config = { debug: true };  // Missing let/const/var
    return config;
}
