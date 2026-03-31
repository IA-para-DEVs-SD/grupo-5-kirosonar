// SonarLint: Remove console.log in production
function processOrder(order) {
    console.log("Processing order:", order);
    const total = order.items.reduce((sum, item) => sum + item.price, 0);
    console.log("Total:", total);
    return total;
}

module.exports = { processOrder };
