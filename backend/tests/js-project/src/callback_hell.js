// SonarLint: Deeply nested callbacks
function fetchData(callback) {
    getData(function(data) {
        processData(data, function(processed) {
            saveData(processed, function(saved) {
                notifyUser(saved, function(notified) {
                    callback(notified);
                });
            });
        });
    });
}
