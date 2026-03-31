// SonarLint: Duplicate code blocks - DRY violation

// First duplicate block - user validation
function validateUser(user) {
    if (!user) {
        return { valid: false, error: "User is required" };
    }
    if (!user.name) {
        return { valid: false, error: "Name is required" };
    }
    if (!user.email) {
        return { valid: false, error: "Email is required" };
    }
    if (user.name.length < 2) {
        return { valid: false, error: "Name too short" };
    }
    return { valid: true, error: null };
}

// Second duplicate block - same validation logic repeated
function checkUser(user) {
    if (!user) {
        return { valid: false, error: "User is required" };
    }
    if (!user.name) {
        return { valid: false, error: "Name is required" };
    }
    if (!user.email) {
        return { valid: false, error: "Email is required" };
    }
    if (user.name.length < 2) {
        return { valid: false, error: "Name too short" };
    }
    return { valid: true, error: null };
}

// Third duplicate block - processing data with same pattern
function processOrderData(order) {
    const total = order.items.reduce((sum, item) => sum + item.price, 0);
    const tax = total * 0.1;
    const shipping = total > 100 ? 0 : 10;
    const finalTotal = total + tax + shipping;
    return { total, tax, shipping, finalTotal };
}

// Fourth duplicate block - same processing logic repeated
function calculateOrderTotal(order) {
    const total = order.items.reduce((sum, item) => sum + item.price, 0);
    const tax = total * 0.1;
    const shipping = total > 100 ? 0 : 10;
    const finalTotal = total + tax + shipping;
    return { total, tax, shipping, finalTotal };
}

module.exports = { validateUser, checkUser, processOrderData, calculateOrderTotal };
