// SonarLint: Use === instead of ==
function checkValue(value) {
    if (value == null) {
        return false;
    }
    if (value == 0) {
        return false;
    }
    return true;
}

module.exports = { checkValue };
