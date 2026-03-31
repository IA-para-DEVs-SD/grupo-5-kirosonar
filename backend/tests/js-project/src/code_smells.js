// SonarLint: Function is too long (>50 lines)
function processUserData(userData) {
    // Validate user data
    if (!userData) {
        return { error: "No user data provided" };
    }

    // Check required fields
    if (!userData.name) {
        return { error: "Name is required" };
    }

    if (!userData.email) {
        return { error: "Email is required" };
    }

    if (!userData.age) {
        return { error: "Age is required" };
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(userData.email)) {
        return { error: "Invalid email format" };
    }

    // Validate age
    if (userData.age < 0) {
        return { error: "Age cannot be negative" };
    }

    if (userData.age > 150) {
        return { error: "Age seems unrealistic" };
    }

    // Process name
    const firstName = userData.name.split(" ")[0];
    const lastName = userData.name.split(" ").slice(1).join(" ");

    // Create user object
    const user = {
        firstName: firstName,
        lastName: lastName,
        email: userData.email.toLowerCase(),
        age: userData.age,
        createdAt: new Date(),
        updatedAt: new Date(),
        status: "active",
        role: "user"
    };

    // Add optional fields
    if (userData.phone) {
        user.phone = userData.phone;
    }

    if (userData.address) {
        user.address = userData.address;
    }

    if (userData.city) {
        user.city = userData.city;
    }

    if (userData.country) {
        user.country = userData.country;
    }

    if (userData.zipCode) {
        user.zipCode = userData.zipCode;
    }

    // Calculate user score
    let score = 0;
    if (user.firstName) score += 10;
    if (user.lastName) score += 10;
    if (user.email) score += 20;
    if (user.phone) score += 15;
    if (user.address) score += 15;
    if (user.city) score += 10;
    if (user.country) score += 10;
    if (user.zipCode) score += 10;

    user.profileCompleteness = score;

    // Return processed user
    return {
        success: true,
        user: user
    };
}

module.exports = { processUserData };
