// SonarLint: eval() is dangerous
function executeCode(code) {
    return eval(code);
}

// Another security issue: using eval in different context
function dynamicCalculation(expression) {
    const result = eval(expression);
    return result;
}

module.exports = { executeCode, dynamicCalculation };
